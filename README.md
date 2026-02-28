# Library Management System

### SOLID Principles in Python — Level 1 Challenge

---

## The Challenge

This project was built as part of a competitive SOLID principles challenge.
The task was designed and judged by Claude (Anthropic).

### Task Requirements (as given):

- Build a console-based Library Management System
- Add, remove, save, load books
- Support multiple storage types: JSON and CSV
- Support multiple notification types: Email and SMS
- Split into `backend.py` (zero console) and `frontend.py` (zero logic)
- Every class must have one reason to change
- Dependencies must be injected — nothing hardcoded

---

## SOLID Breakdown

| Principle                     | Where it lives                                                             | How                                                                         |
| ----------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **S** — Single Responsibility | `Book`, `Library`, `ReportGenerator`, `LibraryService`, notifiers, storage | Every class has exactly one job                                             |
| **O** — Open/Closed           | `FileManagement`, `NotificationService`                                    | Add `CSVFileManagement` or `SlackNotifier` with zero edits to existing code |
| **L** — Liskov Substitution   | `CSVFileManagement`, `JSONFileManagement`                                  | Either storage swaps in without breaking anything                           |
| **I** — Interface Segregation | `FileManagement`, `NotificationService`                                    | Interfaces are lean — no class implements what it doesn't need              |
| **D** — Dependency Inversion  | `LibraryService`                                                           | Never hardcodes storage or notifier — both injected from frontend           |

---

## Project Structure

```
├── backend.py     # All logic — zero print(), zero input()
├── frontend.py    # All console interaction — zero business logic
└── README.md
```

---

## How to Run

```bash
python frontend.py
```

### Menu:

```
=== Library Management System ===
1. Add Book
2. Remove Book
3. Show Report
4. Save Library
5. Load Library
6. Exit
```

---

## Swapping Dependencies

To switch storage or notifier — one line change in `frontend.py`:

```python
# Swap storage
file_manager = JSONFileManagement()   # or CSVFileManagement()

# Swap notifier
notification_service = EmailNotificationService()  # or SMSNotificationService()
```

Zero changes to `backend.py`. That's the point.

---

## Honest Weaknesses

- No duplicate book detection
- Frontend input validation is minimal (bad year input will crash)
- No unit tests

---

## Verdict from the Judge (Claude, Anthropic)

### Where they got it wrong — every single time:

1. **Duplicate methods** — wrote `add_book` and `remove_book` twice in `Library`. Python silently killed the first one. Didn't know that.

2. **`remove_book` was broken** — compared objects by identity not value. Would never find a book. Missing `__eq__` meant two identical books were strangers to each other.

3. **`print()` inside backend** — first version of notifiers had `print()` right in the backend. Direct violation of the entire frontend/backend split.

4. **`LibraryService` inherited `Library`** — used inheritance where composition was needed. `LibraryService` IS NOT a `Library`. Took a full round of feedback to fix.

5. **`LibraryService` had no methods** — built the class, injected dependencies, then left it empty. A shell with nothing inside.

6. **`ReportGenerator` missing** — forgot it existed for multiple rounds even though it was in the original requirements.

7. **`__hash__` missing** — defined `__eq__` without knowing Python automatically breaks `__hash__` when you do that.

8. **Imports inside methods** — `import csv` and `import json` buried inside every method instead of top of file. Basic Python practice missed.

9. **`generate_report` called `.get_all_books()`on a `Library`** — that method doesn't exist on `Library`. Called it three different wrong ways across three submissions before it was fixed.

10. **Year hardcoded as 2026 in setter** — added `DEFAULT_CURRENT_YEAR` to `__init__` then forgot to update the setter. Same bug, two places.

### Bottom line:

Got there. But nothing was right the first time.
Every single class had at least one mistake on first submission.
That's not an insult — that's the job. You fixed every one of them.

---

_Task designed and judged by Claude (Anthropic) — Level 1_
