def sift_down_max(arr, i, size):
    while 2 * i + 1 < size:
        child = 2 * i + 1
        if child + 1 < size and arr[child + 1] > arr[child]:
            child += 1
        if arr[i] >= arr[child]:
            break
        arr[i], arr[child] = arr[child], arr[i]
        i = child


def heapsort(arr):
    for i in range(len(arr) // 2 - 1, -1, -1):
        sift_down_max(arr, i, len(arr))
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down_max(arr, 0, end)
    return arr
