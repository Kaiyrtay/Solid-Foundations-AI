from functools import wraps

##################### Decorators #####################


def str_not_empty(attr_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, str):
                raise TypeError(f"{attr_name} must be a string")
            if not value.split():
                raise ValueError(f"{attr_name} cannot be empty")
            return func(self, value)
        return wrapper
    return decorator

####################### Constants #####################


DEFAULT_CURRENCY_LIST = ("USD", "EUR", "GBP", "JPY", "CNY")

####################### Classes #####################


class BankAccount:

    ####################### Initialization #######################
    def __init__(self, owner, balance=0, currency=DEFAULT_CURRENCY_LIST[0]):
        self.owner = owner
        self.balance = balance
        self.currency = currency

    ###################### Getters and Setters ######################
    @property
    def owner(self):
        return self.__owner

    @owner.setter
    @str_not_empty("Owner")
    def owner(self, value):
        self.__owner = value

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Balance must be a number")
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = value

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    @str_not_empty("Currency")
    def currency(self, value):
        if value not in DEFAULT_CURRENCY_LIST:
            raise ValueError(
                f"Currency must be one of {DEFAULT_CURRENCY_LIST}")
        self.__currency = value

    ####################### Magic Methods #######################

    def __hash__(self):
        return hash((self.owner, self.currency))

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner

    def __lt__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance < other.balance

    def __add__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        if self.owner != other.owner:
            raise ValueError("Cannot add accounts with different owners")
        if self.currency != other.currency:
            raise ValueError("Cannot add accounts with different currencies")
        new_balance = self.balance + other.balance
        return BankAccount(owner=self.owner, balance=new_balance, currency=self.currency)

    def __iadd__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        if self.owner != other.owner:
            raise ValueError("Cannot add accounts with different owners")
        if self.currency != other.currency:
            raise ValueError("Cannot add accounts with different currencies")
        self.balance += other.balance
        return self

    ######################### String Representation #######################

    def __str__(self):
        return f"Account owner: {self.owner}, Balance: {self.balance} {self.currency}"

    def __repr__(self):
        return f"BankAccount(owner={self.owner!r}, balance={self.balance}, currency={self.currency!r})"


# ─── test helpers ─────────────────────────────────────────────────────────────

passed = 0
failed = 0


def check(label, condition):
    global passed, failed
    if condition:
        print(f"  ✅  {label}")
        passed += 1
    else:
        print(f"  ❌  {label}")
        failed += 1


def expect_error(label, exc_type, fn):
    global passed, failed
    try:
        fn()
        print(f"  ❌  {label}  (no error raised)")
        failed += 1
    except exc_type:
        print(f"  ✅  {label}")
        passed += 1
    except Exception as e:
        print(f"  ❌  {label}  (wrong error: {type(e).__name__}: {e})")
        failed += 1


# ─── tests ────────────────────────────────────────────────────────────────────

print("\n Creating accounts")
alice_checking = BankAccount("Alice", 5000, "USD")
alice_savings = BankAccount("Alice", 3000, "EUR")
bob_account = BankAccount("Bob",   2000, "USD")
print(f"  {alice_checking}")
print(f"  {alice_savings}")
print(f"  {bob_account}")


print("\n Basic properties")
check("owner is set correctly",          alice_checking.owner == "Alice")
check("balance is set correctly",        alice_checking.balance == 5000)
check("default currency is USD",         alice_checking.currency == "USD")
check("EUR currency accepted",           alice_savings.currency == "EUR")
check("balance defaults to 0",           BankAccount("Charlie").balance == 0)


print("\n Validation errors")
expect_error("empty owner raises ValueError",       ValueError,
             lambda: BankAccount("",    1000, "USD"))
expect_error("whitespace owner raises ValueError",  ValueError,
             lambda: BankAccount("   ", 1000, "USD"))
expect_error("non-string owner raises TypeError",   TypeError,
             lambda: BankAccount(123,   1000, "USD"))
expect_error("negative balance raises ValueError",  ValueError,
             lambda: BankAccount("X",   -1,   "USD"))
expect_error("string balance raises TypeError",     TypeError,
             lambda: BankAccount("X",   "abc", "USD"))
expect_error("bad currency raises ValueError",      ValueError,
             lambda: BankAccount("X",   1000, "ZZZ"))
expect_error("empty currency raises ValueError",    ValueError,
             lambda: BankAccount("X",   1000, ""))


print("\n Equality & hashing")
alice_other = BankAccount("Alice", 9999, "JPY")
check("same owner == equal",               alice_checking == alice_other)
check("different owner != equal",          alice_checking != bob_account)
alice_usd2 = BankAccount("Alice", 1, "USD")
check("same owner+currency → same hash",
      hash(alice_checking) == hash(alice_usd2))
check("same owner, diff currency → diff hash",
      hash(alice_checking) != hash(alice_savings))
check("diff owner → diff hash",            hash(
    alice_checking) != hash(bob_account))


print("\n Comparison (__lt__)")
check("bob(2000) < alice(5000)",           bob_account < alice_checking)
check("not alice(5000) < bob(2000)", not (alice_checking < bob_account))
check("equal balances are not lt", not (
    BankAccount("X", 100) < BankAccount("Y", 100)))


print("\n Addition (__add__)")
alice_usd = BankAccount("Alice", 5000, "USD")
alice_usd2 = BankAccount("Alice", 3000, "USD")
combined = alice_usd + alice_usd2
check("combined balance is 8000",              combined.balance == 8000)
check("combined keeps owner",                  combined.owner == "Alice")
check("combined keeps currency",               combined.currency == "USD")
check("originals unchanged after __add__",
      alice_usd.balance == 5000 and alice_usd2.balance == 3000)
expect_error("diff owner raises ValueError",
             ValueError, lambda: alice_usd + bob_account)
expect_error("diff currency raises ValueError",
             ValueError, lambda: alice_usd + alice_savings)


print("\n In-place addition (__iadd__)")
alice_a = BankAccount("Alice", 5000, "USD")
alice_b = BankAccount("Alice", 2500, "USD")
alice_a += alice_b
check("balance updated to 7500",               alice_a.balance == 7500)
check("owner unchanged after +=",              alice_a.owner == "Alice")
check("currency unchanged after +=",           alice_a.currency == "USD")
expect_error("diff owner raises ValueError",   ValueError,
             lambda: alice_a.__iadd__(bob_account))
expect_error("diff currency raises ValueError", ValueError,
             lambda: alice_a.__iadd__(alice_savings))


print("\n Sets & dicts (hashing)")
alice_usd_a = BankAccount("Alice", 100, "USD")
alice_usd_b = BankAccount("Alice", 200, "USD")
alice_eur = BankAccount("Alice", 300, "EUR")
account_set = {alice_usd_a, alice_usd_b, alice_eur, bob_account}
check("same owner+currency collapses in set",  len(account_set) == 3)
lookup = {bob_account: "Bob's record"}
check("can use account as dict key",
      lookup[bob_account] == "Bob's record")


print("\n String representations")
check("__str__ contains owner name",       "Alice" in str(alice_checking))
check("__str__ contains balance",          "5000" in str(alice_checking))
check("__str__ contains currency",         "USD" in str(alice_checking))
check("__repr__ is eval-friendly",
      "BankAccount(" in repr(alice_checking))
check("__repr__ contains owner",           "Alice" in repr(alice_checking))


# ─── summary ──────────────────────────────────────────────────────────────────

total = passed + failed
print(f"\n{'='*45}")
print(f"  Results: {passed}/{total} passed  |  {failed} failed")
print(f"{'='*45}\n")
