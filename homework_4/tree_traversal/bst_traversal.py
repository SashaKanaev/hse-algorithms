class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self, values=None):
        self.root = None

        if values is not None:
            for value in values:
                self.insert(value)

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return True

        current = self.root

        while True:
            if value == current.value:
                return False

            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(value)
                    return True
                current = current.right

    def _traverse(self, order):
        result = []
        stack = [(self.root, False)]

        while stack:
            node, visit = stack.pop()

            if node is None:
                continue

            if visit:
                result.append(node.value)
                continue

            for step in reversed(order):
                if step == "N":
                    stack.append((node, True))
                elif step == "L":
                    stack.append((node.left, False))
                else:
                    stack.append((node.right, False))

        return result

    def preorder(self):
        return self._traverse("NLR")

    def inorder(self):
        return self._traverse("LNR")

    def postorder(self):
        return self._traverse("LRN")

    def reverse_preorder(self):
        return self._traverse("NRL")

    def reverse_inorder(self):
        return self._traverse("RNL")

    def reverse_postorder(self):
        return self._traverse("RLN")


if __name__ == "__main__":
    import sys

    numbers = [int(value) for value in sys.stdin.read().split()]
    tree = BinarySearchTree(numbers)

    for name in (
        "preorder", "inorder", "postorder",
        "reverse_preorder", "reverse_inorder", "reverse_postorder",
    ):
        print(f"{name}: {getattr(tree, name)()}")
