# Week 7–8 — Function Arguments Mastery

A focused set of Python exercises exploring every combination of function argument signatures.

---

## Project Structure

```
Week 7 - 8/
└── function_arguments_mastery.py
```

---

## What It Does

Defines and tests functions that accept different combinations of positional and keyword arguments, then applies them in a practical `api_call()` URL builder.

---

## Topics Covered

### Argument Signatures

Step-by-step breakdown of every signature pattern:

| Function                | Signature                        |
| ----------------------- | -------------------------------- |
| `test_att`              | single positional arg            |
| `test_args`             | `*args` only                     |
| `test_kwargs`           | `**kwargs` only                  |
| `test_attr_args`        | fixed arg + `*args`              |
| `test_attr_kwargs`      | fixed arg + `**kwargs`           |
| `test_args_kwargs`      | `*args` + `**kwargs`             |
| `test_attr_args_kwargs` | fixed arg + `*args` + `**kwargs` |

### Practical Example — `api_call()`

Builds a URL from a base endpoint, path segments (`*args`), and query parameters (`**kwargs`).

```python
api_call("https://api.example.com", "users", 42, active=True, page=2)
# → "https://api.example.com/users/42?active=True&page=2"
```

---

## References

**`*args` and `**kwargs`\*\*

- [W3Schools — \*args and \*\*kwargs](https://www.w3schools.com/python/python_args_kwargs.asp)
- [Mimo — args/kwargs](https://mimo.org/glossary/python/args-kwargs)

**Lambda**

- [The Python Coding Stack — Lambda](https://www.thepythoncodingstack.com/p/whats-all-the-fuss-about-python-lambda-functions)
- [Codecademy — Lambda](https://www.codecademy.com/article/python-lambda-function)

**map()**

- [thecode.media — map() (RU)](https://thecode.media/funktsiya-map-v-python/)
- [RealPython — map() reference](https://realpython.com/ref/builtin-functions/map/)
- [RealPython — map() function](https://realpython.com/python-map-function/)
- [GeeksforGeeks — reduce()](https://www.geeksforgeeks.org/python/reduce-in-python/)
- [Wikipedia — MapReduce](https://en.wikipedia.org/wiki/MapReduce)

**List, Dict & Set Comprehensions**

- [PyNEng — Comprehensions (RU)](https://pyneng.readthedocs.io/ru/latest/book/08_useful_basics/x_comprehensions.html)
- [Medium — List, Dict & Set Comprehensions](https://medium.com/@vinodkumargr/list-dictionary-and-set-comprehension-in-python-9823719a67da)
- [RealPython — Set comprehension](https://realpython.com/python-set-comprehension/)
- [RealPython — Dict comprehension](https://realpython.com/python-dictionary-comprehension/)
- [W3Schools — Tuples](https://www.w3schools.com/python/python_tuples.asp)
- [MyGreatLearning — Choosing the right data structure](https://www.mygreatlearning.com/blog/choose-right-python-data-structure/)

**try / except**

- [Server Academy — try/except](https://serveracademy.com/blog/python-try-except/)
- [Pythonchik — try/except (RU)](https://pythonchik.ru/osnovy/python-try-except)

**Mypy**

- [hrekov.com — What is Mypy](https://hrekov.com/blog/what-is-mypy-how-to-use-it)
