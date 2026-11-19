def merge_sort_iterative(nums):
    arr = list(nums)
    n = len(arr)
    buffer = [None] * n
    width = 1

    while width < n:
        for left in range(0, n, 2 * width):
            middle = min(left + width, n)
            right = min(left + 2 * width, n)
            i, j, pos = left, middle, left

            while i < middle and j < right:
                if arr[i] <= arr[j]:
                    buffer[pos] = arr[i]
                    i += 1
                else:
                    buffer[pos] = arr[j]
                    j += 1
                pos += 1

            while i < middle:
                buffer[pos] = arr[i]
                i += 1
                pos += 1
            while j < right:
                buffer[pos] = arr[j]
                j += 1
                pos += 1

        arr, buffer = buffer, arr
        width *= 2

    return arr


def quick_sort_iterative(nums):
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

    stack = [(0, len(arr) - 1)]
    while stack:
        left, right = stack.pop()
        while left < right:
            pivot_index = partition(left, right)
            # Меньшую часть обрабатываем сразу, большую откладываем в стек.
            if pivot_index - left < right - pivot_index:
                if pivot_index + 1 < right:
                    stack.append((pivot_index + 1, right))
                right = pivot_index - 1
            else:
                if left < pivot_index - 1:
                    stack.append((left, pivot_index - 1))
                left = pivot_index + 1

    return arr


if __name__ == "__main__":
    example = [7, 2, 6, 1, 5, 3]
    print("Merge:", merge_sort_iterative(example))
    print("Quick:", quick_sort_iterative(example))
