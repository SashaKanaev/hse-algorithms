class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListStack:
    def __init__(self):
        self.head = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def pop(self):
        if self.is_empty():
            raise IndexError("Empty stack")

        popped_node = self.head
        self.head = self.head.next
        self._size -= 1

        return popped_node.data

    def __len__(self):
        return self._size

    def peek(self):
        if self.is_empty():
            raise IndexError("Empty stack")

        return self.head.data

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node
        self._size += 1


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def enqueue(self, item):
        new_node = Node(item)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def is_empty(self):
        return self.head is None

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Empty queue")

        dequeue_node = self.head
        self.head = self.head.next
        self._size -= 1

        if self.head is None:
            self.tail = None

        return dequeue_node.data

    def peek(self):
        if self.is_empty():
            raise IndexError("Empty queue")

        return self.head.data

    def __len__(self):
        return self._size
