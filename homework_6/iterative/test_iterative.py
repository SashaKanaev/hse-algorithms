from random import Random

import pytest

from homework_6.iterative.iterative import merge_sort_iterative, quick_sort_iterative


@pytest.mark.parametrize("sort_func", [merge_sort_iterative, quick_sort_iterative])
@pytest.mark.parametrize("nums", [
    [], [1], [2, 1], [7, 2, 6, 1, 5, 3], [3, 3, 3],
    [-10, 4, 0, -10, 5, 0], list(range(200)),
    list(range(200, 0, -1)),
])
def test_known_cases(sort_func, nums):
    before = nums.copy()
    assert sort_func(nums) == sorted(nums)
    assert nums == before


@pytest.mark.parametrize("sort_func", [merge_sort_iterative, quick_sort_iterative])
def test_random_cases(sort_func):
    rng = Random(19)
    for n in range(70):
        nums = [rng.randint(-100, 100) for _ in range(n)]
        assert sort_func(nums) == sorted(nums)


def test_merge_sort_non_power_of_two_lengths():
    for n in (3, 5, 6, 7, 9, 17, 33, 65):
        nums = list(range(n, 0, -1))
        assert merge_sort_iterative(nums) == sorted(nums)


def test_iterative_quick_sort_avoids_recursion_limit():
    nums = list(range(1600))
    assert quick_sort_iterative(nums) == nums


def test_iterative_merge_sort_large_input():
    nums = list(range(4000, 0, -1))
    assert merge_sort_iterative(nums) == sorted(nums)
