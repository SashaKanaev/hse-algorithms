from functools import wraps
from random import Random
from statistics import median
from time import perf_counter


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_elapsed = perf_counter() - start

    wrapper.last_elapsed = None
    return wrapper


def merge_sort(nums):
    if len(nums) < 2:
        return list(nums)

    middle = len(nums) // 2
    left = merge_sort(nums[:middle])
    right = merge_sort(nums[middle:])
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(nums):
    arr = list(nums)

    def partition(left, right):
        pivot = arr[right]
        boundary = left
        for i in range(left, right):
            if arr[i] <= pivot:
                arr[boundary], arr[i] = arr[i], arr[boundary]
                boundary += 1
        arr[boundary], arr[right] = arr[right], arr[boundary]
        return boundary

    def sort(left, right):
        if left >= right:
            return
        pivot_index = partition(left, right)
        sort(left, pivot_index - 1)
        sort(pivot_index + 1, right)

    sort(0, len(arr) - 1)
    return arr


@timer
def timed_merge_sort(nums):
    return merge_sort(nums)


@timer
def timed_quick_sort(nums):
    return quick_sort(nums)


def benchmark(n=600, repeats=5):
    rng = Random(42)
    cases = {
        "random": [rng.randint(-10000, 10000) for _ in range(n)],
        "sorted": list(range(n)),
        "reversed": list(range(n, 0, -1)),
        "equal": [7] * n,
    }

    for name, nums in cases.items():
        expected = sorted(nums)
        measurements = []
        for func in (timed_merge_sort, timed_quick_sort):
            times = []
            for _ in range(repeats):
                assert func(nums) == expected
                times.append(func.last_elapsed)
            measurements.append(median(times) * 1000)
        print(f"{name:8s} merge: {measurements[0]:8.3f} ms | quick: {measurements[1]:8.3f} ms")


if __name__ == "__main__":
    benchmark()
