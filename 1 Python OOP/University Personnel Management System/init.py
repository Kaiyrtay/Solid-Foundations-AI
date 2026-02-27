from abc import ABCMeta
from classes import (
    Staff, Teacher, Administrator, Security,
    Student, UndergraduateStudent, GraduateStudent
)
from base import Person


# ─────────────────────────────────────────────────────────────
#  Helper utilities
# ─────────────────────────────────────────────────────────────

PASS = "✅ PASS"
FAIL = "❌ FAIL"


def section(title):
    print(f"\n{'═' * 60}")
    print(f"  {title}")
    print(f"{'═' * 60}")


def check(label, condition):
    status = PASS if condition else FAIL
    print(f"  {status}  {label}")


def expect_error(label, exc_type, fn):
    try:
        fn()
        print(f"  {FAIL}  {label}  (no error raised)")
    except exc_type as e:
        print(f"  {PASS}  {label}  → {exc_type.__name__}: {e}")
    except Exception as e:
        print(f"  {FAIL}  {label}  → Unexpected {type(e).__name__}: {e}")


# ─────────────────────────────────────────────────────────────
#  1. Abstract Class Enforcement
# ─────────────────────────────────────────────────────────────

section("1. Abstract Class Enforcement")

expect_error(
    "Person cannot be instantiated directly",
    TypeError,
    lambda: Person.__new__(Person)
)

expect_error(
    "Staff cannot be instantiated directly (get_salary is abstract)",
    TypeError,
    lambda: Staff("X", 30, 999)
)

expect_error(
    "Student cannot be instantiated directly (calculate_tuition is abstract)",
    TypeError,
    lambda: Student.__new__(Student)
)

check(
    "Person subclass that implements all abstract methods can be instantiated",
    True  # Confirmed by Teacher instantiation below
)


# ─────────────────────────────────────────────────────────────
#  2. Teacher — Inheritance & Role
# ─────────────────────────────────────────────────────────────

section("2. Teacher (Person → Staff → Teacher)")

teacher = Teacher("Dr. Smith", 45, 1001)

check("Teacher instance created",              isinstance(teacher, Teacher))
check("Teacher is a Staff",                    isinstance(teacher, Staff))
check("Teacher is a Person",                   isinstance(teacher, Person))
check("get_role() returns 'Teacher'",          teacher.get_role() == "Teacher")
check("get_salary() returns 50000",            teacher.get_salary() == 50000)
check("__str__ contains 'Teacher'",            "Teacher" in str(teacher))
print(f"         str  → {teacher}")
print(f"         repr → {repr(teacher)}")


# ─────────────────────────────────────────────────────────────
#  3. Administrator — Inheritance & Role
# ─────────────────────────────────────────────────────────────

section("3. Administrator (Person → Staff → Administrator)")

admin = Administrator("Jane Doe", 38, 2002)

check("Administrator instance created",
      isinstance(admin, Administrator))
check("Administrator is a Staff",              isinstance(admin, Staff))
check("Administrator is a Person",             isinstance(admin, Person))
check("get_role() returns 'Administrator'",
      admin.get_role() == "Administrator")
check("get_salary() returns 60000",            admin.get_salary() == 60000)
check("__str__ contains 'Administrator'",      "Administrator" in str(admin))
print(f"         str  → {admin}")


# ─────────────────────────────────────────────────────────────
#  4. Security — Inheritance & Role
# ─────────────────────────────────────────────────────────────

section("4. Security (Person → Staff → Security)")

guard = Security("John Guard", 35, 3003)

check("Security instance created",             isinstance(guard, Security))
check("Security is a Staff",                   isinstance(guard, Staff))
check("Security is a Person",                  isinstance(guard, Person))
check("get_role() returns 'Security'",         guard.get_role() == "Security")
check("get_salary() returns 40000",            guard.get_salary() == 40000)
print(f"         str  → {guard}")


# ─────────────────────────────────────────────────────────────
#  5. Staff Polymorphism — get_salary() & get_role()
# ─────────────────────────────────────────────────────────────

section("5. Staff Polymorphism — get_salary() and get_role()")

staff_members = [
    Teacher("Dr. Smith",  45, 1001),
    Administrator("Jane Doe", 38, 2002),
    Security("John Guard", 35, 3003),
]

expected_roles = ["Teacher", "Administrator", "Security"]
expected_salaries = [50000, 60000, 40000]

print("\n  Iterating over mixed Staff list polymorphically:")
print(f"  {'Role':<20} {'Name':<15} {'Salary':>10}")
print(f"  {'-'*20} {'-'*15} {'-'*10}")

for member, role, salary in zip(staff_members, expected_roles, expected_salaries):
    check(
        f"{role}: get_role() → '{role}', get_salary() → {salary}",
        member.get_role() == role and member.get_salary() == salary
    )
    print(
        f"  {'':>4}{member.get_role():<20} {member.name:<15} {member.get_salary():>10,}")


# ─────────────────────────────────────────────────────────────
#  6. UndergraduateStudent — Full Chain Validation
# ─────────────────────────────────────────────────────────────

section("6. UndergraduateStudent (Person → Student → UndergraduateStudent)")

ug = UndergraduateStudent("Alice", 20, 4001, credits=15, per_credit_fee=300.0)

check("Instance created",
      isinstance(ug, UndergraduateStudent))
check("Is a Person",                           isinstance(ug, Person))
check("get_role() returns 'Student'",          ug.get_role() == "Student")
check("calculate_tuition() → 4500.0",
      ug.calculate_tuition() == 4500.0)
check("credits getter works",                  ug.credits == 15)
check("per_credit_fee getter works",           ug.per_credit_fee == 300.0)
print(f"         str  → {ug}")

ug.credits = 18
check("credits setter updated",                ug.credits == 18)

expect_error("Negative credits rejected",          ValueError,
             lambda: setattr(ug, "credits", -1))
expect_error("Non-int credits rejected",           TypeError,
             lambda: setattr(ug, "credits", "ten"))
expect_error("Negative per_credit_fee rejected",   ValueError,
             lambda: setattr(ug, "per_credit_fee", -50))
expect_error("Non-number per_credit_fee rejected", TypeError,
             lambda: setattr(ug, "per_credit_fee", "free"))


# ─────────────────────────────────────────────────────────────
#  7. GraduateStudent — Full Chain Validation
# ─────────────────────────────────────────────────────────────

section("7. GraduateStudent (Person → Student → GraduateStudent)")

grad = GraduateStudent("Bob", 28, 5001,
                       thesis_title="Deep Learning in NLP",
                       advisor=teacher)

check("Instance created",                      isinstance(grad, GraduateStudent))
check("Is a Person",                           isinstance(grad, Person))
check("get_role() returns 'Student'",          grad.get_role() == "Student")
check("calculate_tuition() → 2000",
      grad.calculate_tuition() == 2000)
check("thesis_title getter works",
      grad.thesis_title == "Deep Learning in NLP")
check("advisor getter returns Teacher",
      isinstance(grad.advisor, Teacher))
check("advisor name correct",                  grad.advisor.name == "Dr. Smith")
print(f"         str  → {grad}")

new_teacher = Teacher("Prof. Lee", 50, 1002)
grad.advisor = new_teacher
check("Advisor updated via setter",
      grad.advisor.name == "Prof. Lee")

expect_error("Non-Teacher advisor rejected",   TypeError,
             lambda: setattr(grad, "advisor", "Not a teacher"))
expect_error("Empty thesis_title rejected",    ValueError,
             lambda: setattr(grad, "thesis_title", "   "))
expect_error("Non-string thesis rejected",     TypeError,
             lambda: setattr(grad, "thesis_title", 123))


# ─────────────────────────────────────────────────────────────
#  8. Student Polymorphism — calculate_tuition()
# ─────────────────────────────────────────────────────────────

section("8. Student Polymorphism — calculate_tuition()")

students = [
    UndergraduateStudent("Alice", 20, 4001, credits=15, per_credit_fee=300.0),
    UndergraduateStudent("Carol", 22, 4002, credits=12, per_credit_fee=250.0),
    GraduateStudent("Bob", 28, 5001, thesis_title="AI Ethics",
                    advisor=teacher),
]

expected_tuitions = [4500.0, 3000.0, 2000]

print("\n  Iterating over mixed Student list polymorphically:")
print(f"  {'Type':<25} {'Name':<10} {'Tuition':>10}")
print(f"  {'-'*25} {'-'*10} {'-'*10}")

for student, expected in zip(students, expected_tuitions):
    result = student.calculate_tuition()
    check(
        f"{type(student).__name__} ({student.name}): tuition → {expected}",
        result == expected
    )
    print(
        f"  {'':>4}{type(student).__name__:<25} {student.name:<10} {result:>10,.1f}")


# ─────────────────────────────────────────────────────────────
#  9. Person Base Validation (via Teacher as concrete class)
# ─────────────────────────────────────────────────────────────

section("9. Person Base Validation (tested through Teacher)")

expect_error("Non-string name rejected",       TypeError,
             lambda: Teacher(123, 30, 10))
expect_error("Empty name rejected",            ValueError,
             lambda: Teacher("  ", 30, 10))
expect_error("Bool age rejected",              TypeError,
             lambda: Teacher("X", True, 10))
expect_error("Age < 16 rejected",              ValueError,
             lambda: Teacher("X", 15, 10))
expect_error("Age > 100 rejected",             ValueError,
             lambda: Teacher("X", 101, 10))
expect_error("Bool ID rejected",               TypeError,
             lambda: Teacher("X", 30, False))
expect_error("Negative ID rejected",           ValueError,
             lambda: Teacher("X", 30, -5))

expect_error("name setter: non-string",        TypeError,
             lambda: setattr(teacher, "name", 99))
expect_error("age setter: out of range",       ValueError,
             lambda: setattr(teacher, "age", 200))
expect_error("ID setter: negative",            ValueError,
             lambda: setattr(teacher, "ID", -1))


# ─────────────────────────────────────────────────────────────
#  10. Cross-type isinstance / boundary checks
# ─────────────────────────────────────────────────────────────

section("10. Inheritance Chain — isinstance() Verification")

check("Teacher      → is Person",                  isinstance(teacher, Person))
check("Teacher      → is Staff",                   isinstance(teacher, Staff))
check("Admin        → is Staff",                   isinstance(admin, Staff))
check("Security     → is Staff",                   isinstance(guard, Staff))
check("UGStudent    → is Person",                  isinstance(ug, Person))
check("GradStudent  → is Person",                  isinstance(grad, Person))
check("Teacher      → NOT Student", not isinstance(teacher, Student))
check("Admin        → NOT Teacher", not isinstance(admin, Teacher))
check("UGStudent    → NOT GraduateStudent",
      not isinstance(ug, GraduateStudent))
check("GradStudent  → NOT UndergraduateStudent",
      not isinstance(grad, UndergraduateStudent))
check("GradStudent  → NOT Staff", not isinstance(grad, Staff))


# ─────────────────────────────────────────────────────────────
#  11. Method Resolution Order (MRO)
# ─────────────────────────────────────────────────────────────

section("11. Method Resolution Order (MRO)")

for cls in [Teacher, Administrator, Security, UndergraduateStudent, GraduateStudent]:
    mro_names = " → ".join(c.__name__ for c in cls.__mro__)
    print(f"  {cls.__name__}:\n    {mro_names}\n")


print(f"\n{'═' * 60}")
print("  All tests completed.")
print(f"{'═' * 60}\n")
