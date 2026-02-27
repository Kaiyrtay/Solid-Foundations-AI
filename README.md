# Week 2 — Inheritance, Abstract Classes & SOLID

Second week of the AI & Data Engineer journey. Still OOP — built the University Personnel Management System (Console Based) using inheritance and abstract base classes, then ran it through SOLID. Also started reading into what Python is actually doing under the hood.

---

## Folder Structure

```
AI and Data Engineer/
│
├── 1 Python OOP/
│   ├── Student Grade Management System/   # Week 1
│   │
│   └── University Personnel Management System/
│       ├── base.py        # Abstract Person base class
│       ├── classes.py     # Staff, Teacher, Administrator, Security, Student, Undergraduate, Graduate
│       └── init.py        # Entry point / test runner
│
├── The Zen of Python.txt
└── requirements.txt
```

---

## What I Built

Two-file hierarchy rooted in an abstract `Person` base class. `Staff` and `Student` inherit from it — `Staff` adds an abstract `get_salary()`, `Student` adds an abstract `calculate_tuition()`. Concrete subclasses (`Teacher`, `Administrator`, `Security`, `UndergraduateStudent`, `GraduateStudent`) handle their own implementations.

Every attribute is private and rejects bad data before storing it — wrong type or invalid value raises an error immediately. Also checked the design against SOLID principles — found one bug where creating a GraduateStudent and updating their advisor had different rules, which meant the same object could end up in a state that should never be allowed. Fixed that. One remaining issue is that GraduateStudent is hardcoded to only accept a Teacher as advisor, meaning if a Professor class gets added later, the code breaks. Left it for now.

---

## Materials I Read

**SOLID**

- [SOLID Principles in Python — Real Python](https://realpython.com/solid-principles-python/#the-solid-design-principles-in-python)
- [SOLID — YouTube](https://www.youtube.com/watch?v=pTB30aXS77U)
- [SOLID — YouTube](https://www.youtube.com/watch?v=k9u40DxhTTk)

**Under the Hood**

- [File Management — Medium](https://medium.com/@ayushkalathiya50/file-management-in-python-6613c0b57a85)
- [Garbage Collection — GeeksforGeeks](https://www.geeksforgeeks.org/python/garbage-collection-python/)
- [Memory Management — GeeksforGeeks](https://www.geeksforgeeks.org/python/memory-management-in-python/)
- [Does Python Have Pointers — Ned Batchelder](https://nedbatchelder.com/blog/202403/does_python_have_pointers)
- [Python Variables Are Pointers — Medium](https://medium.com/analytics-vidhya/python-variables-are-pointers-not-containers-608644af9131)

**Big O**

- [What Is Big O — Towards Data Science](https://towardsdatascience.com/what-is-big-o-notation-and-why-you-should-care-5638895a1693/)
- [Big O Practical Guide — Medium](https://medium.com/@rozy.sinha2711/understanding-big-o-notation-a-practical-guide-for-developers-45fcbbb5e84b)

---

## Next

SOLID principle
