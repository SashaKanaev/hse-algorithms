import heapq

from homework_7.makeheap.makeheap import makeheap, sift_down


def validate_k(nums, k):
    if type(k) is not int or not 1 <= k <= len(nums):
        raise ValueError("k must be an integer between 1 and len(nums)")


def find_kth_largest(nums, k):
    validate_k(nums, k)
    heap = makeheap(nums[:k])
    for i in range(k, len(nums)):
        if nums[i] > heap[0]:
            heap[0] = nums[i]
            sift_down(heap, 0, k)
    return heap[0]


def find_kth_largest_heapq(nums, k):
    validate_k(nums, k)
    heap = nums[:k]
    heapq.heapify(heap)
    for i in range(k, len(nums)):
        if nums[i] > heap[0]:
            heapq.heapreplace(heap, nums[i])
    return heap[0]
