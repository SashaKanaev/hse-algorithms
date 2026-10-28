import random
import subprocess
import sys
from pathlib import Path

import pytest

from bst_traversal import BinarySearchTree


METHODS = (
    "preorder", "inorder", "postorder",
    "reverse_preorder", "reverse_inorder", "reverse_postorder",
)


@pytest.fixture
def example_tree():
    return BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])


@pytest.mark.parametrize(
    "method, expected",
    [
        ("preorder", [8, 3, 1, 6, 4, 7, 10, 14, 13]),
        ("inorder", [1, 3, 4, 6, 7, 8, 10, 13, 14]),
        ("postorder", [1, 4, 7, 6, 3, 13, 14, 10, 8]),
        ("reverse_preorder", [8, 10, 14, 13, 3, 6, 7, 4, 1]),
        ("reverse_inorder", [14, 13, 10, 8, 7, 6, 4, 3, 1]),
        ("reverse_postorder", [13, 14, 10, 7, 4, 6, 1, 3, 8]),
    ],
)
def test_example_traversals(example_tree, method, expected):
    assert getattr(example_tree, method)() == expected


@pytest.mark.parametrize("method", METHODS)
def test_empty_tree(method):
    assert getattr(BinarySearchTree(), method)() == []


@pytest.mark.parametrize("method", METHODS)
def test_single_node(method):
    assert getattr(BinarySearchTree([42]), method)() == [42]


def test_insertion_preserves_bst_property():
    values = [5, -10, 18, 0, -3, 20, 7]
    tree = BinarySearchTree()

    for value in values:
        assert tree.insert(value) is True

    assert tree.inorder() == sorted(values)
    assert tree.reverse_inorder() == sorted(values, reverse=True)
    assert tree.root.value == 5
    assert tree.root.left.value == -10
    assert tree.root.right.value == 18


def test_insert_duplicate_does_not_change_tree():
    tree = BinarySearchTree([5, 3, 7, 3, 5, 7])
    root = tree.root
    left = root.left
    right = root.right

    assert tree.insert(5) is False
    assert tree.insert(3) is False
    assert tree.insert(7) is False
    assert tree.inorder() == [3, 5, 7]
    assert tree.root is root
    assert tree.root.left is left
    assert tree.root.right is right


def test_insert_into_empty_tree():
    tree = BinarySearchTree()
    assert tree.root is None
    assert tree.insert(0) is True
    assert tree.root.value == 0
    assert tree.inorder() == [0]


def test_original_input_does_not_change():
    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    original = values.copy()
    tree = BinarySearchTree(values)
    assert values == original
    assert tree.inorder() == sorted(values)


@pytest.mark.parametrize(
    "values, expected",
    [
        ([3, 2, 1], {
            "preorder": [3, 2, 1], "inorder": [1, 2, 3],
            "postorder": [1, 2, 3], "reverse_preorder": [3, 2, 1],
            "reverse_inorder": [3, 2, 1], "reverse_postorder": [1, 2, 3],
        }),
        ([1, 2, 3], {
            "preorder": [1, 2, 3], "inorder": [1, 2, 3],
            "postorder": [3, 2, 1], "reverse_preorder": [1, 2, 3],
            "reverse_inorder": [3, 2, 1], "reverse_postorder": [3, 2, 1],
        }),
    ],
)
def test_one_sided_trees(values, expected):
    tree = BinarySearchTree(values)
    for method in METHODS:
        assert getattr(tree, method)() == expected[method]


def test_traversals_do_not_modify_tree(example_tree):
    before = example_tree.inorder()
    original_root = example_tree.root
    original_left = original_root.left
    original_right = original_root.right

    for method in METHODS:
        getattr(example_tree, method)()

    assert example_tree.inorder() == before
    assert example_tree.root is original_root
    assert example_tree.root.left is original_left
    assert example_tree.root.right is original_right


def test_all_traversals_have_each_value_once(example_tree):
    expected = example_tree.inorder()
    for method in METHODS:
        result = getattr(example_tree, method)()
        assert len(result) == len(expected)
        assert sorted(result) == expected


def test_negative_zero_and_unbalanced_values():
    tree = BinarySearchTree([0, -5, 10, -9, -2, 7, 20, 8, 6])
    assert tree.inorder() == [-9, -5, -2, 0, 6, 7, 8, 10, 20]
    assert tree.reverse_inorder() == [20, 10, 8, 7, 6, 0, -2, -5, -9]
    assert tree.preorder() == [0, -5, -9, -2, 10, 7, 6, 8, 20]
    assert tree.postorder() == [-9, -2, -5, 6, 8, 7, 20, 10, 0]


def test_deep_tree_without_recursion():
    tree = BinarySearchTree(range(1800))

    assert tree.inorder() == list(range(1800))
    assert tree.reverse_inorder() == list(range(1799, -1, -1))
    assert tree.preorder() == list(range(1800))
    assert tree.postorder() == list(range(1799, -1, -1))
    assert tree.reverse_preorder() == list(range(1800))
    assert tree.reverse_postorder() == list(range(1799, -1, -1))


def reference_traversal(node, method):
    if node is None:
        return []

    left = reference_traversal(node.left, method)
    right = reference_traversal(node.right, method)
    value = [node.value]

    if method == "preorder":
        return value + left + right
    if method == "inorder":
        return left + value + right
    if method == "postorder":
        return left + right + value
    if method == "reverse_preorder":
        return value + right + left
    if method == "reverse_inorder":
        return right + value + left
    return right + left + value


def test_random_trees_against_reference():
    random_generator = random.Random(42)

    for _ in range(80):
        values = [random_generator.randint(-30, 30) for _ in range(25)]
        tree = BinarySearchTree(values)
        assert tree.inorder() == sorted(set(values))

        for method in METHODS:
            assert getattr(tree, method)() == reference_traversal(tree.root, method)


def test_command_line_output():
    path = Path(__file__).with_name("bst_traversal.py")
    process = subprocess.run(
        [sys.executable, str(path)],
        input="8 3 10 1 6 14 4 7 13\n",
        text=True,
        capture_output=True,
        check=True,
    )
    lines = process.stdout.strip().splitlines()
    assert len(lines) == 6
    assert lines[0] == "preorder: [8, 3, 1, 6, 4, 7, 10, 14, 13]"
    assert lines[1] == "inorder: [1, 3, 4, 6, 7, 8, 10, 13, 14]"
    assert lines[5] == "reverse_postorder: [13, 14, 10, 7, 4, 6, 1, 3, 8]"


def test_command_line_empty_input():
    path = Path(__file__).with_name("bst_traversal.py")
    process = subprocess.run(
        [sys.executable, str(path)],
        input="",
        text=True,
        capture_output=True,
        check=True,
    )
    assert process.stdout.strip().splitlines() == [f"{method}: []" for method in METHODS]
