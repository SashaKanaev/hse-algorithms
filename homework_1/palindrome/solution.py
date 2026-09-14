def palindrome(nums):
    num = nums
    divide = 1

    while divide * 10 <= num:
        divide *= 10

    while num > 0:
        last = num % 10
        first = num // divide

        if first != last:
            return False

        num = num % divide
        num = num // 10
      
        divide = divide // 100

    return True
