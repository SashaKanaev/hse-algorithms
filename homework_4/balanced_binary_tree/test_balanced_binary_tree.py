import random
import subprocess
import sys
from pathlib import Path
from functools import lru_cache

import pytest

from balanced_binary_tree import Node, build_tree, is_balanced


@pytest.mark.parametrize(
    "root, expected",
    [
        (None, True),
        (Node(10), True),
        (Node(10, Node(5), Node(15)), True),
        (Node(10, Node(5)), True),
        (Node(10, right=Node(15)), True),
        (Node(10, Node(5, Node(2))), False),
        (Node(10, right=Node(15, right=Node(20))), False),
        (Node(10, Node(5, Node(2), Node(8)), Node(15)), True),
        (Node(10, Node(5, Node(2, Node(1)), Node(8)), Node(15)), False),
        (Node(10, Node(5, Node(3, Node(2)), Node(8)), Node(15, Node(12), Node(20))), True),
        (
            Node(
                10,
                Node(5, Node(3, Node(2, Node(1))), Node(8)),
                Node(15, Node(12, Node(11)), Node(20)),
            ),
            False,
        ),
        (Node(10, Node(5, Node(2)), Node(15, right=Node(20))), True),
        (Node(7, Node(7), Node(7)), True),
        (Node(0, Node(-10), Node(10)), True),
        (Node(1, Node(2), Node(3)), True),
        (Node("root", Node("left"), Node("right")), True),
    ],
)
def test_basic_cases(root, expected):
    assert is_balanced(root) is expected


def test_one_level_difference_is_allowed():
    root = Node(10, Node(5, Node(2)), Node(15))
    assert is_balanced(root) is True


def test_two_level_difference_is_not_allowed():
    root = Node(10, Node(5, Node(2), Node(8)), Node(15, right=Node(20, right=Node(25))))
    assert is_balanced(root) is False


def test_balanced_does_not_mean_bst():
    root = Node(1, Node(100), Node(-100))
    assert is_balanced(root) is True


def test_violation_in_subtree_with_balanced_root():
    root = Node(
        10,
        Node(5, Node(3, Node(2, Node(1))), Node(8)),
        Node(15, Node(12, Node(11)), Node(20)),
    )
    assert is_balanced(root) is False


def test_many_identical_values():
    root = Node(0, Node(0, Node(0), Node(0)), Node(0, Node(0), Node(0)))
    assert is_balanced(root) is True
    root.left.left.left = Node(0)
    assert is_balanced(root) is True
    root.left.left.left.left = Node(0)
    assert is_balanced(root) is False


def test_tree_is_unchanged_and_calls_are_repeatable():
    root = Node(10, Node(5, Node(3), Node(7)), Node(15, left=Node(12)))
    nodes = [root, root.left, root.right, root.left.left, root.left.right, root.right.left]
    before = [(node.value, node.left, node.right) for node in nodes]

    assert is_balanced(root) is True
    assert is_balanced(root) is True
    assert before == [(node.value, node.left, node.right) for node in nodes]

    root.left.left.left = Node(1, Node(0))
    assert is_balanced(root) is False
    assert is_balanced(root) is False


def make_perfect_tree(levels):
    if levels == 0:
        return None
    return Node(levels, make_perfect_tree(levels - 1), make_perfect_tree(levels - 1))


@pytest.mark.parametrize("levels", [0, 1, 2, 3, 6, 10, 12])
def test_perfect_trees(levels):
    assert is_balanced(make_perfect_tree(levels)) is True


@pytest.mark.parametrize("side", ["left", "right"])
def test_deep_chains_without_recursion(side):
    root = Node(0)
    current = root

    for value in range(1, 5001):
        child = Node(value)
        setattr(current, side, child)
        current = child

    assert is_balanced(root) is False


def test_large_balanced_root_with_an_unbalanced_deep_subtree():
    root = make_perfect_tree(12)
    current = root
    for _ in range(11):
        current = current.left
    current.left = Node(0, Node(0, Node(0)))

    assert is_balanced(root) is False


def recursive_reference(node):
    if node is None:
        return True, 0

    left_balanced, left_height = recursive_reference(node.left)
    right_balanced, right_height = recursive_reference(node.right)
    return (
        left_balanced and right_balanced and abs(left_height - right_height) <= 1,
        1 + max(left_height, right_height),
    )


def test_random_arbitrary_trees_against_independent_reference():
    rng = random.Random(2026)

    for _ in range(600):
        count = rng.randrange(0, 61)
        if count == 0:
            root = None
        else:
            root = Node(rng.randrange(-5, 6))
            candidates = [root]

            for _ in range(count - 1):
                parent = rng.choice(candidates)
                child = Node(rng.randrange(-5, 6))
                free_sides = [side for side in ("left", "right") if getattr(parent, side) is None]
                side = rng.choice(free_sides)
                setattr(parent, side, child)
                candidates.append(child)

                if parent.left is not None and parent.right is not None:
                    candidates.remove(parent)

        assert is_balanced(root) is recursive_reference(root)[0]


@lru_cache(maxsize=None)
def tree_shapes(count):
    if count == 0:
        return (None,)

    result = []
    for left_count in range(count):
        right_count = count - 1 - left_count
        for left in tree_shapes(left_count):
            for right in tree_shapes(right_count):
                result.append((left, right))
    return tuple(result)


def tree_from_shape(shape):
    if shape is None:
        return None
    left, right = shape
    return Node(0, tree_from_shape(left), tree_from_shape(right))


def test_all_small_tree_shapes_against_independent_reference():
    for count in range(9):
        for shape in tree_shapes(count):
            root = tree_from_shape(shape)
            assert is_balanced(root) is recursive_reference(root)[0]


@pytest.mark.parametrize(
    "values, expected",
    [
        ([], None),
        (["null"], None),
        (["None"], None),
        (["10"], 10),
        (["-10"], -10),
    ],
)
def test_build_tree_roots(values, expected):
    root = build_tree(values)
    if expected is None:
        assert root is None
    else:
        assert root.value == expected
        assert root.left is None
        assert root.right is None


def test_build_tree_level_order_and_missing_nodes():
    values = ["10", "5", "15", "3", "8", "12", "20", "2", "null"]
    original = values.copy()
    root = build_tree(values)

    assert values == original
    assert root.left.value == 5
    assert root.left.left.value == 3
    assert root.left.left.left.value == 2
    assert root.left.left.right is None
    assert root.left.right.value == 8
    assert root.right.left.value == 12
    assert root.right.right.value == 20
    assert is_balanced(root) is True


def test_build_tree_with_missing_left_child():
    root = build_tree(["8", "null", "12", "10", "15"])
    assert root.left is None
    assert root.right.value == 12
    assert root.right.left.value == 10
    assert root.right.right.value == 15
    assert is_balanced(root) is False


@pytest.mark.parametrize("values", [["null", "1"], ["1", "null", "null", "5"]])
def test_build_tree_rejects_unattached_values(values):
    with pytest.raises(ValueError):
        build_tree(values)


def run_program(data):
    path = Path(__file__).with_name("balanced_binary_tree.py")
    return subprocess.run(
        [sys.executable, str(path)],
        input=data,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


@pytest.mark.parametrize(
    "data, expected",
    [
        ("", "True"),
        ("null", "True"),
        ("3", "True"),
        ("10 5 15 3 8 12 20 2", "True"),
        ("10 5 15 3 8 null null 2", "False"),
        ("10 5 15 3 8 12 20 2 null null null 11 null null null 1", "False"),
        ("1 100 -100", "True"),
    ],
)
def test_command_line(data, expected):
    assert run_program(data) == expected
