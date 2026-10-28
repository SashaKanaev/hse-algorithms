import random
import subprocess
import sys
from pathlib import Path

import pytest

from validate_bst import Node, build_tree, is_valid_bst


@pytest.mark.parametrize(
    "root, expected",
    [
        (None, True),
        (Node(10), True),
        (Node(10, Node(5), Node(15)), True),
        (Node(10, Node(15), Node(20)), False),
        (Node(10, Node(5), Node(7)), False),
        (Node(10, Node(10), Node(15)), False),
        (Node(10, Node(5), Node(10)), False),
        (Node(10, Node(5, right=Node(10)), Node(15)), False),
        (Node(10, Node(5), Node(15, left=Node(10))), False),
        (Node(10, Node(5), Node(15, left=Node(6))), False),
        (Node(10, Node(5, right=Node(12)), Node(15)), False),
        (Node(0, Node(-10), Node(10)), True),
        (Node(-10, Node(-20), Node(-5)), True),
        (Node(10, Node(5, Node(2), Node(8)), Node(15, Node(12), Node(20))), True),
        (Node(10, Node(5, Node(2), Node(8)), Node(15, Node(6), Node(20))), False),
    ],
)
def test_basic_cases(root, expected):
    assert is_valid_bst(root) is expected


def test_large_positive_and_negative_values():
    huge = 10**100
    root = Node(0, Node(-huge), Node(huge))
    assert is_valid_bst(root) is True

    root.right.left = Node(-1)
    assert is_valid_bst(root) is False


def test_valid_tree_with_missing_children():
    root = Node(10, Node(3, right=Node(7)), Node(20, left=Node(15)))
    assert is_valid_bst(root) is True


def test_violation_many_levels_below_root():
    root = Node(20, Node(10, right=Node(15, left=Node(5))), Node(30))
    assert is_valid_bst(root) is False


def test_repeated_calls_do_not_modify_tree():
    root = Node(10, Node(5, Node(2), Node(8)), Node(15, Node(12), Node(20)))
    original = (
        root.left,
        root.right,
        root.left.left,
        root.left.right,
        root.right.left,
        root.right.right,
    )

    assert is_valid_bst(root) is True
    assert is_valid_bst(root) is True
    assert original == (
        root.left,
        root.right,
        root.left.left,
        root.left.right,
        root.right.left,
        root.right.right,
    )


def test_deep_right_chain_without_recursion():
    root = Node(0)
    current = root

    for value in range(1, 5000):
        current.right = Node(value)
        current = current.right

    assert is_valid_bst(root) is True
    current.right = Node(-1)
    assert is_valid_bst(root) is False


def test_deep_left_chain_without_recursion():
    root = Node(0)
    current = root

    for value in range(-1, -5000, -1):
        current.left = Node(value)
        current = current.left

    assert is_valid_bst(root) is True
    current.left = Node(1)
    assert is_valid_bst(root) is False


def test_valid_tree_built_by_insertion():
    rng = random.Random(2026)

    for _ in range(100):
        values = rng.sample(range(-10000, 10000), rng.randrange(0, 80))
        root = None

        for value in values:
            if root is None:
                root = Node(value)
                continue

            current = root
            while True:
                if value < current.value:
                    if current.left is None:
                        current.left = Node(value)
                        break
                    current = current.left
                else:
                    if current.right is None:
                        current.right = Node(value)
                        break
                    current = current.right

        assert is_valid_bst(root) is True


def inorder_reference(root):
    if root is None:
        return []
    return inorder_reference(root.left) + [root.value] + inorder_reference(root.right)


def test_random_arbitrary_trees_against_independent_reference():
    rng = random.Random(42)

    for _ in range(400):
        count = rng.randrange(0, 45)
        if count == 0:
            assert is_valid_bst(None) is True
            continue

        root = Node(rng.randrange(-50, 51))
        candidates = [root]

        for _ in range(count - 1):
            parent = rng.choice(candidates)
            child = Node(rng.randrange(-50, 51))

            free_sides = [side for side in ("left", "right") if getattr(parent, side) is None]
            side = rng.choice(free_sides)
            setattr(parent, side, child)
            candidates.append(child)

            if parent.left is not None and parent.right is not None:
                candidates.remove(parent)

        values = inorder_reference(root)
        expected = all(a < b for a, b in zip(values, values[1:]))
        assert is_valid_bst(root) is expected


@pytest.mark.parametrize(
    "values, expected",
    [
        ([], None),
        (["null"], None),
        (["None"], None),
        (["10"], Node(10)),
    ],
)
def test_build_tree_roots(values, expected):
    result = build_tree(values)
    if expected is None:
        assert result is None
    else:
        assert result.value == expected.value
        assert result.left is None
        assert result.right is None


def test_build_tree_level_order_and_missing_nodes():
    values = ["10", "5", "15", "null", "8", "12", "20"]
    copy = values.copy()
    root = build_tree(values)

    assert values == copy
    assert root.left.left is None
    assert root.left.right.value == 8
    assert root.right.left.value == 12
    assert root.right.right.value == 20
    assert is_valid_bst(root) is True


def test_build_tree_with_early_missing_children():
    root = build_tree(["8", "null", "12", "10", "15"])
    assert root.left is None
    assert root.right.value == 12
    assert root.right.left.value == 10
    assert root.right.right.value == 15
    assert is_valid_bst(root) is True


@pytest.mark.parametrize("values", [["null", "1"], ["1", "null", "null", "5"]])
def test_build_tree_rejects_unattached_nodes(values):
    with pytest.raises(ValueError):
        build_tree(values)


def run_program(data):
    path = Path(__file__).with_name("validate_bst.py")
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
        ("null\n", "True"),
        ("10\n", "True"),
        ("10 5 15 2 8 12 20\n", "True"),
        ("10 5 15 2 8 6 20\n", "False"),
        ("10 5 15 null 8 10 20\n", "False"),
        ("0 -5 5 null null -3 6\n", "False"),
        ("0 -5 5 null null 3 6\n", "True"),
    ],
)
def test_command_line(data, expected):
    assert run_program(data) == expected
