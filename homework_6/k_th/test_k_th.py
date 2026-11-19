from random import Random

import pytest

from homework_6.k_th.k_th import find_kth_largest


@pytest.mark.parametrize("nums,k,expected", [
    ([3, 2, 1, 5, 6, 4], 2, 5),
    ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4),
    ([7], 1, 7),
    ([9, 9, 9, 9], 3, 9),
    ([5, -1, 0, -10], 1, 5),
    ([5, -1, 0, -10], 4, -10),
    ([2, 2, 3, 3, 1], 2, 3),
    ([2, 2, 3, 3, 1], 3, 2),
    (list(range(100)), 50, 50),
    (list(range(100, 0, -1)), 100, 1),
])
def test_known_cases(nums, k, expected):
    before = nums.copy()
    assert find_kth_largest(nums, k) == expected
    assert nums == before


def test_random_cases():
    rng = Random(21)
    for n in range(1, 61):
        nums = [rng.randint(-10, 10) for _ in range(n)]
        for k in (1, (n + 1) // 2, n):
            assert find_kth_largest(nums, k) == sorted(nums)[-k]


@pytest.mark.parametrize("nums,k", [
    ([], 1), ([1, 2, 3], 0), ([1, 2, 3], -1),
    ([1, 2, 3], 4), ([1, 2, 3], 1.5), ([1, 2, 3], True),
])
def test_invalid_k(nums, k):
    with pytest.raises(ValueError):
        find_kth_largest(nums, k)
