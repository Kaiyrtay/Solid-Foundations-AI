# Week 1 — Python OOP Mastery

First week of the AI & Data Engineer journey. The focus was purely OOP — building a Student Management System from zero, one hour a day, Monday to Friday.

---

## Folder Structure

```
AI and Data Engineer/
│
├── 1 Python OOP/
│   ├── Student Grade Management System/
│   │   ├── classes.py              # Student, Course, University
│   │   ├── init.py                 # Entry point / test runner
│   │   ├── university_data.json    # Generated output (structured)
│   │   └── university_report.txt  # Generated output (human-readable)
│   │
│   └── materials.txt               # Reading articles / materials
│
├── The Zen of Python.txt           # PEP 20 notes
└── requirements.txt
```

---

## What I Built

Three classes — `Student`, `Course`, and `University` — each with private attributes, validated getters/setters, and proper `__str__`/`__repr__`. The entry point generates 3 random universities with 4 courses and 5 students each, prints a full report, and saves it to both `.txt` and `.json`.

Took me longer than I'd like to admit to understand that encapsulation isn't just about slapping double underscores on everything — it's about making sure the data you store is actually trustworthy. Also spent way too long staring at why `@property.setter` was crashing before realising the decorator needs the property name, not the word "property".

---

## Materials I Read

**Philosophy**

- [The Zen of Python — PEP 20](https://pep20.org/)

**OOP**

- [Python Classes — Real Python](https://realpython.com/python-classes/)
- [Python Inheritance — DataCamp](https://www.datacamp.com/tutorial/python-inheritance)
- [Abstract Classes — Medium](https://medium.com/@prashampahadiya9228/abstract-classes-and-abstract-methods-in-python-e632ea34bc79)

**Decorators**

- [Demystifying Decorators — The Python Coding Stack](https://www.thepythoncodingstack.com/p/demystifying-python-decorators)
- [Primer on Decorators — Real Python](https://realpython.com/primer-on-python-decorators/)

---

## Next

Inheritance and Abstract Classes. Plan is to refactor with a base `Person` class and explore where `ABC` makes the design cleaner.
