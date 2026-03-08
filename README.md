# CustomList

A custom Python list implementation built on a dictionary with decorator-driven validation, logging, and timing.

---

## Usage

```python
c = CustomList()
```

---

## Operations

| Operation        | Behaviour                           |
| ---------------- | ----------------------------------- |
| `c.append(v)`    | Adds value to the end               |
| `c.insert(i, v)` | Inserts value at index              |
| `c.pop(i=-1)`    | Removes and returns value at index  |
| `c.remove(v)`    | Removes first occurrence of value   |
| `c.extend(it)`   | Appends all items from any iterable |
| `c[i]`           | Get item by index                   |
| `c[i] = v`       | Set item by index                   |
| `v in c`         | True if value exists in list        |
| `len(c)`         | Returns number of items             |
| `for v in c`     | Iterates in order                   |

---

## Decorators

This is the core of the implementation. Every method behaviour is controlled by one or more decorators stacked on top.

### `@timer`

Measures and prints how long a function took to run.

```python
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        stop = time()
        print(f"Function : {func.__name__!r} , executed in {(stop - start):.4f}s'")
        return result
    return wrapper
```

Applied to `extend`. Every time you extend the list, execution time is printed to the console.

```python
c.extend([1, 2, 3])
# Function : 'extend' , executed in 0.0001s'
```

---

### `@logger`

Records every call to a log file at `./storage/log.txt` with timestamps and the return value.

```python
def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logged_at = datetime.now()
        result = func(*args, **kwargs)
        finished_at = datetime.now()
        with open("./storage/log.txt", "a") as file:
            file.write(
                f"{logged_at.strftime(fmt)} :: {func.__name__!r} :: {result} :: {finished_at.strftime(fmt)}\n"
            )
        return result
    return wrapper
```

Applied to `append`, `remove`, `pop`, `insert`. Every mutation is persisted to the log.

```
2025-01-01 12:00:00 :: 'append' :: None :: 2025-01-01 12:00:00
2025-01-01 12:00:01 :: 'pop' :: 99 :: 2025-01-01 12:00:01
```

---

### `@not_negative`

A **parametrised decorator** — it takes an attribute name and validates that the value passed to a setter is a non-negative integer.

```python
def not_negative(attr_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, int):
                raise TypeError(f"{attr_name} must be type of integer(countable)!")
            if value < 0:
                raise ValueError(f"{attr_name} can not be negative!")
            return func(self, value)
        return wrapper
    return decorator
```

Three layers deep: outer function receives the config (`attr_name`), middle function receives the target function, inner function is the actual wrapper that runs on every call. This pattern is called a **decorator factory**.

```python
@not_negative("size")
def size(self, value):
    self.__size = value
```

---

### `@index_validation`

The most complex decorator. Also a **decorator factory** — accepts `allow_end=False` to control whether index == size is a valid position (needed for `insert`, which can append at the end).

```python
def index_validation(allow_end=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, index=None, *args, **kwargs):
            if index is None:
                param = inspect.signature(func).parameters.get("index")
                if param and param.default is not inspect.Parameter.empty:
                    index = param.default
                else:
                    raise TypeError(f"{func.__name__}() missing required argument: 'index'")

            if index < 0:
                index = self.size + index

            upper = self.size if allow_end else self.size - 1
            if index < 0 or index > upper:
                raise IndexError(f"Index out of range: 0 - {self.size - 1}")

            return func(self, index, *args, **kwargs)
        return wrapper
    return decorator
```

What it does step by step:

1. **Default handling** — if no index is passed, reads the default from the function signature using `inspect`. This is how `pop()` with no argument still works as `pop(-1)`.
2. **Negative resolution** — converts negative indices to their positive equivalent (`-1` on a 3-element list becomes `2`).
3. **Bounds check** — rejects anything out of range. `allow_end=True` widens the upper bound by one for `insert`.

```python
@index_validation()          # allow_end=False  → upper bound = size - 1
def pop(self, index=-1): ...

@index_validation(allow_end=True)   # upper bound = size (insert at end allowed)
def insert(self, index, value): ...
```

---

### Decorator stacking

Some methods use two decorators at once:

```python
@logger
@index_validation()
def pop(self, index=-1):
    ...
```

Python applies decorators **bottom-up**: `index_validation` wraps `pop` first, then `logger` wraps the result. So execution order is top-down: `logger` runs → calls `index_validation` wrapper → calls the real `pop`.

---

## Validation Summary

| What                     | How                                        | Error raised |
| ------------------------ | ------------------------------------------ | ------------ |
| Negative index           | Resolved to positive by `index_validation` | —            |
| Out-of-range index       | Caught by `index_validation`               | `IndexError` |
| Index on empty list      | Caught by `index_validation`               | `IndexError` |
| Remove value not in list | Caught inside `remove`                     | `ValueError` |
| Non-integer size         | Caught by `not_negative`                   | `TypeError`  |
| Negative size            | Caught by `not_negative`                   | `ValueError` |

---

## Unit Tests

Run the included test suite:

```bash
python decorators.py
```

All 47 cases cover `append`, `pop`, `insert`, `remove`, `extend`, `__getitem__`, `__setitem__`, `__contains__`, `__iter__`, `__str__`, `__repr__`, and stress scenarios.
