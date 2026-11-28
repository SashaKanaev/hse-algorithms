from random import Random

import pytest

from homework_7.heapsort.heapsort import heapsort


@pytest.mark.parametrize("nums", [
    [], [1], [2, 1], [1, 2, 3], [4, 3, 2, 1],
    [0, -5, 2, -1, 2, 0], [7] * 30, list(range(100, 0, -1)),
])
def test_known_cases(nums):
    arr = nums.copy()
    assert heapsort(arr) is arr
    assert arr == sorted(nums)


def test_random_cases():
    rng = Random(13)
    for n in range(101):
        nums = [rng.randint(-30, 30) for _ in range(n)]
        expected = sorted(nums)
        heapsort(nums)
        assert nums == expected
