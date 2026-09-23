from validate import validateStackSequences


def test_example_true():
    pushed = [1, 2, 3, 4, 5]
    popped = [1, 3, 5, 4, 2]

    assert validateStackSequences(pushed, popped) is True


def test_example_false():
    pushed = [1, 2, 3]
    popped = [3, 1, 2]

    assert validateStackSequences(pushed, popped) is False


def test_same_order():
    pushed = [1, 2, 3, 4, 5]
    popped = [1, 2, 3, 4, 5]

    assert validateStackSequences(pushed, popped) is True


def test_reverse_order():
    pushed = [1, 2, 3, 4, 5]
    popped = [5, 4, 3, 2, 1]

    assert validateStackSequences(pushed, popped) is True


def test_nontrivial_true():
    pushed = [1, 2, 3, 4]
    popped = [2, 4, 3, 1]

    assert validateStackSequences(pushed, popped) is True


def test_nontrivial_false():
    pushed = [1, 2, 3, 4, 5]
    popped = [4, 5, 3, 1, 2]

    assert validateStackSequences(pushed, popped) is False


def test_single_element():
    pushed = [10]
    popped = [10]

    assert validateStackSequences(pushed, popped) is True


def test_max_length():
    pushed = list(range(100_000))
    popped = list(reversed(pushed))

    assert validateStackSequences(pushed, popped) is True
