# E-Commerce Order Processing System

### SOLID Principles in Python — Level 3 (Final)

---

## The Challenge

This project was built as part of a competitive SOLID principles challenge.
The task was designed and judged by Claude (Anthropic).

### Task Requirements (as given):

- Build a console-based E-Commerce Order Processing System
- Add products, register customers, create and process orders
- Apply discount strategies, choose shipping methods, process payments
- Validate orders, calculate totals with full breakdown
- Generate invoices, export to JSON or TXT
- Send notifications on confirmed orders
- Update stock and loyalty points after successful orders
- Split into `backend.py` (zero console) and `frontend.py` (zero logic)
- Every dependency injected — nothing hardcoded

---

## SOLID Breakdown

| Principle                     | Where it lives                                                                                                                                             | How                                                                                           |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **S** — Single Responsibility | `Product`, `Customer`, `OrderItem`, `Order`, `PriceCalculator`, `OrderValidator`, `InvoiceGenerator`, `InventoryService`, `LoyaltyService`, `OrderService` | Every class has one job. Data classes hold data. Services do work. Orchestrator orchestrates. |
| **O** — Open/Closed           | `DiscountStrategy`, `ShippingStrategy`, `PaymentProcessor`, `Export`, `NotificationService`                                                                | Add any new strategy or service with one new class. Zero edits to existing code.              |
| **L** — Liskov Substitution   | All strategy and service implementations                                                                                                                   | Every concrete class fulfills its contract. Any swap works without breaking anything.         |
| **I** — Interface Segregation | All ABCs                                                                                                                                                   | Every interface has exactly one method. No class implements what it doesn't need.             |
| **D** — Dependency Inversion  | `PriceCalculator`, `InvoiceGenerator`, `OrderService`                                                                                                      | All 8 dependencies injected into `OrderService`. Nothing hardcoded anywhere in backend.       |

---

## Project Structure

```
├── backend.py      # All logic — zero print(), zero input()
├── decorators.py   # Reusable validation decorators
└── frontend.py     # All console interaction — zero business logic
```

---

## How to Run

```bash
python frontend.py
```

### Menu:

```
=== E-Commerce Management System ===
1. Add Product
2. Add Customer
3. Create Order
4. Process Order
5. Show Customer Info
6. Show Product Info
7. Exit
8. Export Order/Invoice
```

---

## Swapping Dependencies

One line in `frontend.py`. Zero changes to `backend.py`:

```python
discount_strategy = PercentageDiscount(10)  # or FlatDiscount, LoyaltyDiscount, NoDiscount
shipping_strategy = ExpressShipping()        # or StandardShipping, FreeShipping
payment_processor = PayPalPayment()          # or CreditCardPayment
notifier = SMSNotificationService()          # or EmailNotificationService
exporter = JSONExport()                      # or TXTExport
```

---

## Honest Weaknesses

- No persistence — all data lost on exit
- Frontend uses plain dicts for product and customer registries instead of proper registry classes
- Input validation in frontend is minimal — bad input types will crash
- No unit tests

---

## Verdict from the Judge (Claude, Anthropic)

### Did they get in touch with SOLID?

Partially.

The concepts landed. The ideas are there. But there is still a gap between understanding something and consistently applying it without mistakes. The concept lives in the head — it does not fully live in the hands yet.

That gap closes with more practice. Not with more reading.

---

## Grade.

78/100.
Three real mistakes. All implementation, none architectural. The design was right throughout. The principles were understood and applied correctly where it actually matters — the hard stuff, the traps, the boundaries between classes.

<br>It means two different things went wrong in this challenge — design mistakes and implementation mistakes.

- Design is the thinking. Where does this class go, what is its job, who depends on who, how do the pieces connect. That's the SOLID part. You got this right. OrderService clean from day one, no logic leaking into data classes, all the right abstractions in the right places.
- Implementation is the execution. Actually writing the code correctly after the thinking is done. That's where the three mistakes were — price not added to Product, InvoiceGenerator missing the injection, the dict/float mismatch. Not wrong thinking. Just things that slipped when writing.
  <br>So the verdict is — your understanding of SOLID is solid. Your hands just need more reps to match your head.

---

_Task designed and judged by Claude (Anthropic) — Level 3 (Final)_
