from solution import max_even_sum

def test_sum_already_even():
    assert max_even_sum([2, 4, 6]) == 12
    assert max_even_sum([1, 3, 4]) == 8

def test_odd_sum():
    assert max_even_sum([2, 5, 7, 13, 14]) == 36
    assert max_even_sum([1, 2, 4]) == 6

def test_minimum_odd_not_minimum_element():
    assert max_even_sum([2, 4, 9, 11, 20]) == 46

def test_only_odd_numbers():
    assert max_even_sum([3, 5, 7]) == 12
    assert max_even_sum([1, 3, 5, 7, 9]) == 24

def test_duplicates():
    assert max_even_sum([2, 2, 3, 3, 5]) == 12
    assert max_even_sum([5, 5, 5]) == 10

def test_single_element():
    assert max_even_sum([8]) == 8
    assert max_even_sum([7]) == 0

def test_large_values():
    assert max_even_sum([1000, 2000, 3001, 5001]) == 11002
