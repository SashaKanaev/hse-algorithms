def count_primes(N):
    if N <= 2:
        return 0

    is_prime = [True] * N
    is_prime[0] = False
    is_prime[1] = False

    p = 2

    while p * p < N:
        if is_prime[p]:
            for multiple in range(p * p, N, p):
                is_prime[multiple] = False

        p += 1

    return sum(is_prime)
