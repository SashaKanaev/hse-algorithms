from random import Random

import pytest

from homework_7.makeheap.makeheap import makeheap, makeheap_n_log_n


def check_heap(func, nums):
    arr = nums.copy()
    assert func(arr) is arr
    assert sorted(arr) == sorted(nums)
    assert all(arr[(i - 1) // 2] <= arr[i] for i in range(1, len(arr)))


@pytest.mark.parametrize("func", [makeheap, makeheap_n_log_n])
@pytest.mark.parametrize("nums", [
    [], [1], [2, 1], [1, 2, 3], [4, 3, 2, 1],
    [0, -5, 2, -1, 2, 0], [7] * 30, list(range(100, 0, -1)),
])
def test_known_cases(func, nums):
    check_heap(func, nums)


@pytest.mark.parametrize("func", [makeheap, makeheap_n_log_n])
def test_random_cases(func):
    rng = Random(13)
    for n in range(101):
        check_heap(func, [rng.randint(-30, 30) for _ in range(n)])
