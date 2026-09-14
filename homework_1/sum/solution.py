def max_even_sum(nums):
    if sum(nums) % 2 == 0:
        return sum(nums)

    all_nums = nums.copy()

    while min(all_nums) % 2 == 0:
        all_nums.remove(min(all_nums))

    nums.remove(min(all_nums))

    return sum(nums)
