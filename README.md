# Generators

A collection of Python generators for primes, Fibonacci, and file reading.

---

## Functions

### `is_prime(number)`

Returns `True` if the number is prime, `False` otherwise.

### `prime_numbers()`

Infinite generator that yields prime numbers one by one.
Three versions written — the active one is the most efficient, dividing only by previously found primes.

### `fibonacci()`

Infinite generator that yields Fibonacci numbers one by one.
Three versions written — the active one uses `yield` to stream values endlessly.

### `filereader(filename)`

Yields each line of a file with whitespace stripped.

---

## References

- [GeeksforGeeks — Prime Numbers](https://www.geeksforgeeks.org/maths/prime-numbers/)
- [Brilliant — Prime Numbers](https://brilliant.org/wiki/prime-numbers/)
- [Wikipedia — Fibonacci Sequence](https://en.wikipedia.org/wiki/Fibonacci_sequence)
