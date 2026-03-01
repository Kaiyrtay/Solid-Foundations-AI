# Student Grade Management System

### SOLID Principles in Python — Level 2 Challenge

---

## The Challenge

This project was built as part of a competitive SOLID principles challenge.
The task was designed and judged by Claude (Anthropic).

### Task Requirements (as given):

- Build a console-based Student Grade Management System
- Add students, add grades, calculate averages, evaluate pass/fail
- Support multiple export types: JSON and TXT
- Send a notification when a student fails
- Split into `backend.py` (zero console) and `frontend.py` (zero logic)
- `Student` holds grades — `Grade` is its own class
- `GradeCalculator` is a separate class — `Student` does not calculate its own average
- `PassFailEvaluator` is a separate class — calculator does not decide pass/fail
- Dependencies must be injected — nothing hardcoded

---

## SOLID Breakdown

| Principle                     | Where it lives                                                                  | How                                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **S** — Single Responsibility | `Student`, `Grade`, `GradeCalculator`, `PassFailEvaluator`, `ReportGenerator`   | Each class has one job — student holds data, calculator computes, evaluator decides |
| **O** — Open/Closed           | `Export`, `NotificationService`                                                 | Add `CSVExport` or `SlackNotifier` without touching existing classes                |
| **L** — Liskov Substitution   | `TXTExport`, `JSONExport`, `EmailNotificationService`, `SMSNotificationService` | Any export or notifier swaps in without breaking the system                         |
| **I** — Interface Segregation | `Export`, `NotificationService`                                                 | Interfaces are lean — exporters only export, notifiers only notify                  |
| **D** — Dependency Inversion  | `PassFailEvaluator`, `ReportGenerator`, `TXTExport`                             | All receive their dependencies — nothing hardcoded inside                           |

---

## Project Structure

```
├── backend.py      # All logic — zero print(), zero input()
├── decorators.py   # Reusable validation decorator for string setters
└── frontend.py     # All console interaction — zero business logic
```

---

## How to Run

```bash
python frontend.py
```

### Menu:

```
=== Student Management System ===
1. Add Student
2. Add Grade to Student
3. Show Student Report
4. Export Report (TXT/JSON)
5. Exit
```

---

## Swapping Dependencies

To switch export format or notifier — one line change in `frontend.py`:

```python
# Swap notifier
notifier = EmailNotificationService()  # or SMSNotificationService()

# Swap export format
exporter = TXTExport(report_generator)  # or JSONExport()
```

Zero changes to `backend.py`. That's the point.

---

## Honest Weaknesses

- No persistence — all students are lost on exit
- Frontend input validation is minimal (non-numeric score input will crash)
- No unit tests

---

## Verdict from the Judge (Claude, Anthropic)

### What they got right — all of it:

1. **Clean class separation** — `Student` has zero calculation logic. `GradeCalculator`, `PassFailEvaluator`, and `ReportGenerator` are genuinely separate with proper dependency injection throughout.

2. **`Grade` is a real class** — not a dict, not a tuple, not a raw number. Proper validation on both `subject` and `score`. Done right.

3. **`StudentRegistry` is a proper class** — state is encapsulated in the frontend where it belongs. Not a global variable.

4. **Notification system works end to end** — `NotificationService` is abstract, `EmailNotificationService` and `SMSNotificationService` both implement it, the notifier is injected in frontend and called when a student fails a subject.

5. **Both exporters are complete** — `TXTExport` takes a `ReportGenerator` via injection and writes the full formatted report. `JSONExport` writes structured data. Both implement `Export`. Either swaps in with one line.

6. **`str_not_empty_validation` decorator** — reusable, extracted to its own file, applied consistently across `Student` and `Grade` setters.

7. **Frontend/backend split is clean** — zero `print()` or `input()` in backend. Zero logic in frontend. The line was drawn and held the entire way through.

### Where they got it wrong:

Nothing. This submission is complete and correct.

### Bottom line:

Every requirement met. Every SOLID principle applied correctly. The architecture is clean, the dependencies flow the right direction, and the code does what it says it does. This is what Level 2 looks like when it's done.

---

_Task designed and judged by Claude (Anthropic) — Level 2_
