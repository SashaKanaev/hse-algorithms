def sift_up(arr, i):
    while i > 0:
        parent = (i - 1) // 2
        if arr[parent] <= arr[i]:
            break
        arr[parent], arr[i] = arr[i], arr[parent]
        i = parent


def sift_down(arr, i, size):
    while 2 * i + 1 < size:
        child = 2 * i + 1
        if child + 1 < size and arr[child + 1] < arr[child]:
            child += 1
        if arr[i] <= arr[child]:
            break
        arr[i], arr[child] = arr[child], arr[i]
        i = child


def makeheap_n_log_n(arr):
    for i in range(1, len(arr)):
        sift_up(arr, i)
    return arr


def makeheap(arr):
    for i in range(len(arr) // 2 - 1, -1, -1):
        sift_down(arr, i, len(arr))
    return arr
