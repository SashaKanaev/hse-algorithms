from solution import count_primes

def test_example_10():
    assert count_primes(10) == 4

def test_example_1():
    assert count_primes(1) == 0

def test_boundary():
    assert count_primes(2) == 0
    assert count_primes(3) == 1

def test_nontrivial():
    assert count_primes(100) == 25
