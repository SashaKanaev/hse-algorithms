import pytest

from stack_vs_queue import LinkedListStack, Queue


def test_stack_lifo():
    stack = LinkedListStack()

    stack.push(1)
    stack.push(2)
    stack.push(3)

    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_stack_peek():
    stack = LinkedListStack()

    stack.push(10)
    stack.push(20)

    assert stack.peek() == 20
    assert len(stack) == 2   # peek ничего не удалил


def test_stack_empty():
    stack = LinkedListStack()

    assert stack.is_empty()
    assert len(stack) == 0

    with pytest.raises(IndexError):
        stack.pop()

    with pytest.raises(IndexError):
        stack.peek()


def test_stack_push_after_pop():
    stack = LinkedListStack()

    stack.push(1)
    stack.push(2)

    assert stack.pop() == 2

    stack.push(3)

    assert stack.pop() == 3
    assert stack.pop() == 1


def test_queue_fifo():
    queue = Queue()

    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    assert queue.dequeue() == 1
    assert queue.dequeue() == 2
    assert queue.dequeue() == 3


def test_queue_peek():
    queue = Queue()

    queue.enqueue(10)
    queue.enqueue(20)

    assert queue.peek() == 10
    assert len(queue) == 2


def test_queue_empty():
    queue = Queue()

    assert queue.is_empty()
    assert len(queue) == 0

    with pytest.raises(IndexError):
        queue.dequeue()

    with pytest.raises(IndexError):
        queue.peek()


def test_queue_reuse_after_empty():
    queue = Queue()

    queue.enqueue(1)
    assert queue.dequeue() == 1

    assert queue.is_empty()

    queue.enqueue(2)

    assert queue.peek() == 2
    assert queue.dequeue() == 2
    assert queue.is_empty()
