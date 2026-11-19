from random import Random

import pytest

from homework_6.compare.compare import (
    benchmark,
    merge_sort,
    quick_sort,
    timer,
)


@pytest.mark.parametrize("nums", [
    [], [1], [2, 1], [1, 2, 3, 4], [4, 3, 2, 1],
    [4, 1, 3, 2], [0, -5, 2, -1, 2, 0], [7] * 30,
    list(range(100)), list(range(100, 0, -1)),
])
@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
def test_known_cases(sort_func, nums):
    before = nums.copy()
    assert sort_func(nums) == sorted(nums)
    assert nums == before


@pytest.mark.parametrize("sort_func", [merge_sort, quick_sort])
def test_random_cases(sort_func):
    rng = Random(13)
    for n in range(0, 51):
        nums = [rng.randint(-20, 20) for _ in range(n)]
        assert sort_func(nums) == sorted(nums)


def test_timer_returns_result_and_preserves_name():
    @timer
    def add(a, b):
        return a + b

    assert add(2, 3) == 5
    assert add.__name__ == "add"
    assert isinstance(add.last_elapsed, float) and add.last_elapsed >= 0


def test_timer_handles_exception():
    @timer
    def fail():
        raise RuntimeError("test")

    with pytest.raises(RuntimeError):
        fail()
    assert fail.last_elapsed is not None


def test_benchmark_prints_all_cases(capsys):
    benchmark(n=20, repeats=2)
    output = capsys.readouterr().out
    assert all(name in output for name in ("random", "sorted", "reversed", "equal"))
