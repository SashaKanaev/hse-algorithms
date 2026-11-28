from random import Random

import pytest

from homework_7.k_th.k_th import find_kth_largest, find_kth_largest_heapq


@pytest.mark.parametrize("func", [find_kth_largest, find_kth_largest_heapq])
@pytest.mark.parametrize("nums,k,expected", [
    ([3, 2, 1, 5, 6, 4], 2, 5),
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
    ([7], 1, 7), ([9, 9, 9], 2, 9),
    ([-5, -1, -10], 1, -1), ([-5, -1, -10], 3, -10),
    ([2, 2, 3, 3, 1], 3, 2), (list(range(100)), 50, 50),
])
def test_known_cases(func, nums, k, expected):
    before = nums.copy()
    assert func(nums, k) == expected
    assert nums == before


@pytest.mark.parametrize("func", [find_kth_largest, find_kth_largest_heapq])
def test_random_cases(func):
    rng = Random(21)
    for n in range(1, 61):
        nums = [rng.randint(-10, 10) for _ in range(n)]
        for k in range(1, n + 1):
            assert func(nums, k) == sorted(nums)[-k]


@pytest.mark.parametrize("func", [find_kth_largest, find_kth_largest_heapq])
@pytest.mark.parametrize("nums,k", [
    ([], 1), ([1], 0), ([1], -1), ([1], 2), ([1], 1.5), ([1], True),
])
def test_invalid_k(func, nums, k):
    with pytest.raises(ValueError):
        func(nums, k)
