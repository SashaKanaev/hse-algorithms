def find_kth_largest(nums, k):
    if type(k) is not int or not 1 <= k <= len(nums):
        raise ValueError("k должно быть от 1 до длины массива")

    arr = list(nums)
    target = len(arr) - k
    left, right = 0, len(arr) - 1

    while left <= right:
        pivot = arr[(left + right) // 2]
        lt, i, gt = left, left, right

        # После прохода: [left:lt] < pivot, [lt:gt+1] == pivot,
        # [gt+1:right+1] > pivot.
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[i], arr[gt] = arr[gt], arr[i]
                gt -= 1
            else:
                i += 1

        if target < lt:
            right = lt - 1
        elif target > gt:
            left = gt + 1
        else:
            return arr[target]

    raise RuntimeError("Недостижимое состояние")


if __name__ == "__main__":
    print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))
    print(find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))
