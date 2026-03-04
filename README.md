# BankAccount

A simple Python bank account class with validation and operator support.

## Usage

```python
acc = BankAccount(owner, balance=0, currency="USD")
```

**Supported currencies:** `USD`, `EUR`, `GBP`, `JPY`, `CNY`

## Operations

| Operation | Behaviour                                 |
| --------- | ----------------------------------------- |
| `a + b`   | Returns new account with combined balance |
| `a += b`  | Adds balance in-place                     |
| `a == b`  | True if same `owner`                      |
| `a < b`   | Compares by `balance`                     |
| `hash(a)` | Based on `(owner, currency)`              |

Both `+` and `+=` require the same `owner` **and** `currency`.

## Validation

- `owner` — non-empty string, required
- `balance` — number ≥ 0, defaults to `0`
- `currency` — must be in the supported list, defaults to `USD`

## Magic methods:

- https://www.tutorialsteacher.com/python/magic-methods-in-python
- https://realpython.com/python-magic-methods/
