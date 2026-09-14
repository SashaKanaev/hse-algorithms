from solution import palindrome

def test_examples():
    assert palindrome(121) is True
    assert palindrome(31) is False

def test_single_digit():
    assert palindrome(1) is True
    assert palindrome(5) is True
    assert palindrome(9) is True

def test_even_number_of_digits():
    assert palindrome(11) is True
    assert palindrome(1221) is True
    assert palindrome(123321) is True

def test_odd_number_of_digits():
    assert palindrome(101) is True
    assert palindrome(12321) is True
    assert palindrome(3545453) is True

def test_not_palindrome():
    assert palindrome(12) is False
    assert palindrome(123) is False
    assert palindrome(123421) is False
    assert palindrome(3546453) is False

def test_zeros_inside():
    assert palindrome(1001) is True
    assert palindrome(10001) is True
    assert palindrome(10201) is True
    assert palindrome(10021) is False

def test_large_number():
    assert palindrome(123456789987654321) is True
    assert palindrome(123456789887654321) is False
