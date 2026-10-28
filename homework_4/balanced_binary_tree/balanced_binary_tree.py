from collections import deque
import sys


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def is_balanced(root):
    if root is None:
        return True

    stack = [(root, False)]
    heights = []

    while stack:
        node, visited = stack.pop()

        if not visited:
            stack.append((node, True))
            if node.right is not None:
                stack.append((node.right, False))
            if node.left is not None:
                stack.append((node.left, False))
            continue

        right_height = heights.pop() if node.right is not None else 0
        left_height = heights.pop() if node.left is not None else 0

        if abs(left_height - right_height) > 1:
            return False

        heights.append(max(left_height, right_height) + 1)

    return True


def build_tree(values):
    if not values:
        return None

    def make_node(value):
        if value.lower() in ("null", "none"):
            return None
        return Node(int(value))

    root = make_node(values[0])
    if root is None:
        if len(values) != 1:
            raise ValueError("Unexpected values after empty root")
        return None

    queue = deque([root])
    index = 1

    while queue and index < len(values):
        node = queue.popleft()

        node.left = make_node(values[index])
        index += 1
        if node.left is not None:
            queue.append(node.left)

        if index < len(values):
            node.right = make_node(values[index])
            index += 1
            if node.right is not None:
                queue.append(node.right)

    if index != len(values):
        raise ValueError("Unexpected values after the last node")

    return root


if __name__ == "__main__":
    root = build_tree(sys.stdin.read().split())
    print(is_balanced(root))
