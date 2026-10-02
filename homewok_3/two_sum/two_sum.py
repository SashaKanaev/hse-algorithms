from two_sum import two_sum

def two_sum(arr, k):
    seen = {}

    for i, num in enumerate(arr):
        need = k - num

        if need in seen:
            return seen[need], i

        seen[num] = i
