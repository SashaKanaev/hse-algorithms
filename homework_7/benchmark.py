from random import Random
from statistics import median
from time import perf_counter

from homework_6.compare.compare import merge_sort
from homework_7.heapsort.heapsort import heapsort
from homework_7.makeheap.makeheap import makeheap, makeheap_n_log_n


def measure(func, nums, repeats=5):
    times = []
    for _ in range(repeats):
        arr = nums.copy()
        start = perf_counter()
        func(arr)
        times.append(perf_counter() - start)
    return median(times) * 1000


def benchmark():
    rng = Random(42)
    for n in (1000, 10000, 100000):
        cases = {
            "random": [rng.randint(-100000, 100000) for _ in range(n)],
            "sorted": list(range(n)),
            "reversed": list(range(n, 0, -1)),
            "equal": [7] * n,
        }
        for name, nums in cases.items():
            funcs = (makeheap_n_log_n, makeheap, heapsort, sorted, merge_sort)
            times = [measure(func, nums) for func in funcs]
            print(f"{n:6} {name:8} " + " | ".join(f"{t:.3f}" for t in times))


if __name__ == "__main__":
    print("n, case | makeheap_n_log_n | makeheap | heapsort | sorted | merge_sort (ms)")
    benchmark()
