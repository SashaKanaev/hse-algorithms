class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None
        self.size = 0

    def _height(self, node):
        return node.height if node is not None else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rebalance(self, node):
        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def insert(self, value):
        def add(node):
            if node is None:
                return Node(value), True

            if value == node.value:
                return node, False

            if value < node.value:
                node.left, added = add(node.left)
            else:
                node.right, added = add(node.right)

            if not added:
                return node, False
            return self._rebalance(node), True

        self.root, added = add(self.root)
        if added:
            self.size += 1
        return added

    def search(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            if value < node.value:
                node = node.left
            else:
                node = node.right
        return False

    def delete(self, value):
        def remove(node, target):
            if node is None:
                return None, False

            if target < node.value:
                node.left, deleted = remove(node.left, target)
            elif target > node.value:
                node.right, deleted = remove(node.right, target)
            else:
                if node.left is None:
                    return node.right, True
                if node.right is None:
                    return node.left, True

                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.value = successor.value
                node.right, _ = remove(node.right, successor.value)
                deleted = True

            if not deleted:
                return node, False
            return self._rebalance(node), True

        self.root, deleted = remove(self.root, value)
        if deleted:
            self.size -= 1
        return deleted

    def inorder(self):
        result = []
        stack = []
        node = self.root

        while node is not None or stack:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.value)
            node = node.right

        return result

    def __len__(self):
        return self.size


if __name__ == "__main__":
    tree = AVL()
    for value in [30, 20, 40, 10, 25, 35, 50]:
        tree.insert(value)
    print(tree.inorder())
    print(tree.search(25))
    tree.delete(30)
    print(tree.inorder())
