def test_two_sum():
    assert two_sum([1, 3, 4, 10], 7) == (1, 2)
    assert two_sum([5, 5, 1, 4], 10) == (0, 1)
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum([-3, 4, 3, 90], 0) == (0, 2)
    assert two_sum([0, 4, 0], 0) == (0, 2)
