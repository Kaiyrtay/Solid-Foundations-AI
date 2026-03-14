# Python Concepts

---

## Context Manager

A custom file manager using the `with` statement. Automatically closes the file on exit, even if an exception occurs.

Supported modes: `r`, `r+`, `rb`, `rb+`, `w`, `w+`, `wb`, `wb+`, `a`, `a+`, `ab`, `ab+`

### Magic Methods

- `__enter__` — opens the file
- `__exit__` — closes the file, re-raises exceptions with line number
- `__str__` — human-readable representation
- `__repr__` — developer representation

---

## References

- [Context Managers — LevelUp](https://levelup.gitconnected.com/decoding-python-magic-enter-and-exit-bef77457606f)
- [Python `with` Statement — RealPython](https://realpython.com/python-with-statement/)
