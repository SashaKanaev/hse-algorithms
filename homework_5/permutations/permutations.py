import argparse
import ast
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from homework_5.tracer.tracer import tracer


def permutations(nums, trace=False):
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack(current):
        if len(current) == len(nums):
            result.append(current.copy())
            return 1

        seen = set()
        count = 0

        for i, number in enumerate(nums):
            if used[i] or number in seen:
                continue

            seen.add(number)
            used[i] = True
            current.append(number)

            count += search(current)

            current.pop()
            used[i] = False

        return count

    search = tracer(backtrack) if trace else backtrack
    search(path)
    return result


def main():
    parser = argparse.ArgumentParser(description="Все перестановки массива")
    parser.add_argument("--trace", action="store_true", help="Показать стек рекурсивных вызовов")
    args = parser.parse_args()

    nums = ast.literal_eval(input().strip())
    if not isinstance(nums, list) or any(type(num) is not int for num in nums):
        raise ValueError("Ожидается список целых чисел")

    print(permutations(nums, trace=args.trace))


if __name__ == "__main__":
    main()
