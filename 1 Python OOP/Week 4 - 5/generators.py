import math


def is_prime(number: int) -> bool:
    """Return True if number has no divisors except 1 and itself."""
    if number <= 1:
        return False
    for i in range(2, int(math.sqrt(number))+1):
        if number % i == 0:
            return False
    return True

# def prime_numbers():
#     """Generate primes using trial division up to sqrt(number); simple but less efficient."""
#     number = 2
#     while True:
#         is_prime = True
#         for i in range(2, int(math.sqrt(number)) + 1):
#             if number % i == 0:
#                 is_prime = False
#                 break
#         if is_prime:
#             yield number
#         number += 1
# def prime_numbers():
#     """Generate primes using trial division up to sqrt(number); simple for/else."""
#     number = 2
#     while True:
#         for i in range(2, int(math.sqrt(number))+1):
#             if number % i == 0:
#                 break
#         else:
#             yield number
#         number += 1


def prime_numbers():
    """Generate primes using previously found primes for efficiency."""
    number = 2
    prime_numbers = []
    while True:
        is_prime = True
        for prime in prime_numbers:
            if prime**2 > number:
                break
            if number % prime == 0:
                is_prime = False
                break
        if is_prime:
            prime_numbers.append(number)
            yield number

        number += 1

# Fibonacci version 0
# def fibonacci(n):
#     """Generate Fibonacci numbers endlessly (sum of previous two)."""
#     if n == 0:
#         return 0
#     if n == 1:
#         return 1
#     return fibonacci(n-1) + fibonacci(n - 2)
# Fibonacci version 1
# def fibonacci(n):
#     """Generate Fibonacci numbers endlessly (sum of previous two)."""
#     a, b = 0, 1
#     for _ in range(n):
#         a, b = b, a + b
#     return a


def fibonacci():
    """Generate Fibonacci numbers endlessly (sum of previous two)."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def filereader(filename):
    """Yield each line of a file without extra whitespace."""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()
