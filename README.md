# CustomList

A custom Python list implementation built on a dictionary with index validation and full iteration support.

## Usage

```python
c = CustomList()
```

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

## Validation

- `index` — resolved via `index_validation` decorator
- Negative indices — supported, resolved to positive equivalent
- Out of range — raises `IndexError`
- `remove` on missing value — raises `ValueError`

## Unit Test

- https://realpython.com/python-unittest/
