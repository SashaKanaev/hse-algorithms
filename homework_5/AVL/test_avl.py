from itertools import permutations
from math import log2
from pathlib import Path
import random
import subprocess
import sys

import pytest

from avl import AVL


def check_tree(tree, expected):
    visited = set()

    def inspect(node, lower=None, upper=None):
        if node is None:
            return 0, []

        assert id(node) not in visited
        visited.add(id(node))
        if lower is not None:
            assert lower < node.value
        if upper is not None:
            assert node.value < upper

        left_height, left_values = inspect(node.left, lower, node.value)
        right_height, right_values = inspect(node.right, node.value, upper)

        assert abs(left_height - right_height) <= 1
        assert node.height == max(left_height, right_height) + 1
        return node.height, left_values + [node.value] + right_values

    actual_height, values = inspect(tree.root)
    assert values == sorted(expected)
    assert tree.inorder() == values
    assert len(tree) == tree.size == len(expected)
    if not expected:
        assert tree.root is None
        assert actual_height == 0
    else:
        assert tree.root.height == actual_height
        assert actual_height <= 2 * log2(len(expected) + 2)


def make_tree(values):
    tree = AVL()
    for value in values:
        assert tree.insert(value) is True
    return tree


def test_empty_tree():
    tree = AVL()
    assert tree.root is None
    assert tree.inorder() == []
    assert len(tree) == 0
    assert tree.search(10) is False
    assert tree.delete(10) is False
    check_tree(tree, set())


def test_one_element():
    tree = AVL()
    assert tree.insert(4) is True
    assert tree.search(4) is True
    assert tree.search(3) is False
    check_tree(tree, {4})
    assert tree.delete(4) is True
    assert tree.delete(4) is False
    check_tree(tree, set())


@pytest.mark.parametrize(
    "values, expected_root",
    [
        ([30, 20, 10], 20),
        ([10, 20, 30], 20),
        ([30, 10, 20], 20),
        ([10, 30, 20], 20),
    ],
)
def test_four_insertion_rotations(values, expected_root):
    tree = make_tree(values)
    assert tree.root.value == expected_root
    assert tree.root.left.value == 10
    assert tree.root.right.value == 30
    check_tree(tree, set(values))


@pytest.mark.parametrize("values", [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [3, 1, 4, 2, 5]])
def test_insertion_orders(values):
    tree = make_tree(values)
    check_tree(tree, set(values))
    for value in values:
        assert tree.search(value) is True


def test_duplicate_is_ignored_and_structure_does_not_change():
    tree = make_tree([10, 5, 15])
    original_root = tree.root
    original_children = (tree.root.left, tree.root.right)
    assert tree.insert(5) is False
    assert tree.insert(10) is False
    assert tree.insert(15) is False
    assert tree.root is original_root
    assert (tree.root.left, tree.root.right) == original_children
    check_tree(tree, {5, 10, 15})


def test_negative_zero_and_large_values():
    values = [-10**100, -10, 0, 10, 10**100]
    tree = make_tree(values)
    check_tree(tree, set(values))
    assert tree.search(10**100) is True
    assert tree.search(1) is False
    assert tree.delete(-10**100) is True
    check_tree(tree, set(values[1:]))


def test_delete_leaf():
    tree = make_tree([20, 10, 30, 5, 15])
    assert tree.delete(5) is True
    assert tree.search(5) is False
    check_tree(tree, {10, 15, 20, 30})


def test_delete_one_child():
    tree = make_tree([20, 10, 30, 5])
    assert tree.delete(10) is True
    assert tree.root.left.value == 5
    check_tree(tree, {5, 20, 30})


def test_delete_two_children():
    tree = make_tree([20, 10, 40, 5, 15, 30, 50, 25, 35])
    assert tree.delete(20) is True
    assert tree.search(20) is False
    check_tree(tree, {5, 10, 15, 25, 30, 35, 40, 50})


def test_delete_successor_with_right_child():
    tree = make_tree([40, 20, 60, 10, 30, 50, 70, 55])
    assert tree.delete(40) is True
    assert tree.search(55) is True
    check_tree(tree, {10, 20, 30, 50, 55, 60, 70})


def test_delete_root_repeatedly_until_empty():
    values = [13, 6, 20, 4, 9, 17, 25, 2, 5, 8, 11, 16, 18, 23, 27]
    tree = make_tree(values)
    expected = set(values)
    while tree.root is not None:
        root_value = tree.root.value
        assert tree.delete(root_value) is True
        expected.remove(root_value)
        check_tree(tree, expected)
    assert len(tree) == 0


def test_delete_absent_does_not_modify_tree():
    tree = make_tree([10, 5, 15])
    root = tree.root
    left = root.left
    right = root.right
    assert tree.delete(999) is False
    assert tree.delete(-999) is False
    assert tree.root is root
    assert tree.root.left is left
    assert tree.root.right is right
    check_tree(tree, {5, 10, 15})


@pytest.mark.parametrize("initial, removed", [
    ([30, 20, 40, 10, 25, 35, 50, 5], [35, 50]),
    ([30, 20, 40, 10, 25, 35, 50, 5], [50, 35]),
    ([20, 10, 30, 5, 15, 25, 35, 2], [25, 35]),
    ([10, 5, 20, 15, 25, 13], [5, 25]),
    ([9, 5, 15, 3, 7, 11, 18, 1], [18, 15]),
])
def test_delete_can_require_rotations(initial, removed):
    tree = make_tree(initial)
    expected = set(initial)
    for value in removed:
        assert tree.delete(value) is True
        expected.remove(value)
        check_tree(tree, expected)



@pytest.mark.parametrize(
    "initial, removed, rotations",
    [
        ([8, 21, 33, 7], 21, "R"),
        ([17, 23, 25, 33], 17, "L"),
        ([28, 31, 10, 15], 28, "LR"),
        ([27, 1, 4, 7], 1, "RL"),
    ],
)
def test_four_deletion_rotation_scenarios(initial, removed, rotations):
    class TrackedAVL(AVL):
        def __init__(self):
            super().__init__()
            self.rotations = ""

        def _rotate_left(self, node):
            self.rotations += "L"
            return super()._rotate_left(node)

        def _rotate_right(self, node):
            self.rotations += "R"
            return super()._rotate_right(node)

    tree = TrackedAVL()
    for value in initial:
        tree.insert(value)
    tree.rotations = ""
    assert tree.delete(removed) is True
    assert tree.rotations == rotations
    check_tree(tree, set(initial) - {removed})


def test_sorted_inserts_stay_logarithmic():
    tree = AVL()
    for value in range(5000):
        assert tree.insert(value) is True
    check_tree(tree, set(range(5000)))
    for value in (0, 1, 1250, 2500, 4999):
        assert tree.search(value)


def test_reverse_sorted_inserts_and_deletes():
    tree = make_tree(range(3499, -1, -1))
    expected = set(range(3500))
    check_tree(tree, expected)
    for value in range(0, 3500, 2):
        assert tree.delete(value) is True
        expected.remove(value)
    check_tree(tree, expected)
    for value in range(1, 3500, 2):
        assert tree.delete(value) is True
        expected.remove(value)
    check_tree(tree, expected)


def test_all_orders_of_five_elements():
    for order in permutations(range(5)):
        tree = make_tree(order)
        check_tree(tree, set(order))
        for value in reversed(order):
            assert tree.delete(value) is True
            check_tree(tree, set(order) - set(order[order.index(value):]))


def test_mixed_random_operations_against_set():
    rng = random.Random(2026)
    for _ in range(18):
        tree = AVL()
        reference = set()
        for step in range(380):
            value = rng.randint(-90, 90)
            operation = rng.randrange(3)
            if operation == 0:
                assert tree.insert(value) is (value not in reference)
                reference.add(value)
            elif operation == 1:
                assert tree.delete(value) is (value in reference)
                reference.discard(value)
            else:
                assert tree.search(value) is (value in reference)
            check_tree(tree, reference)


def test_search_does_not_modify_tree():
    tree = make_tree(range(-40, 41))
    before = tree.inorder()
    root = tree.root
    for value in range(-50, 51):
        assert tree.search(value) is (value in before)
    assert tree.root is root
    assert tree.inorder() == before
    check_tree(tree, set(before))


def test_independent_trees():
    first = make_tree([2, 1, 3])
    second = make_tree([4, 5, 6])
    first.delete(2)
    second.insert(7)
    check_tree(first, {1, 3})
    check_tree(second, {4, 5, 6, 7})


def test_import_does_not_execute_demo():
    result = subprocess.run(
        [sys.executable, "-c", "from homework_5.AVL.avl import AVL"],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == ""
    assert result.stderr == ""


def test_demo_runs_as_file_and_matches_actions():
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("avl.py"))],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == [
        "[10, 20, 25, 30, 35, 40, 50]",
        "True",
        "[10, 20, 25, 35, 40, 50]",
    ]
    assert result.stderr == ""
