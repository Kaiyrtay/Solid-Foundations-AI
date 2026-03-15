# Log Analysis Tool

A lightweight Python tool for parsing and analyzing Android log files.

---

## Project Structure

```
Log Analysis Tool/
├── datasets/
│   ├── Android.log
│   └── README.md
└── __init__.py
```

---

## What It Does

Reads a raw Android `.log` file line by line, parses each line into a structured `LogEntry`, and lets you compare two loading approaches — generator vs list.

---

## How It Works

### LogEntry

Parses a single raw log line into typed fields: `date`, `time`, `pid`, `tid`, `level`, `tag`, `message`

- `parse()` — takes a raw string, returns a `LogEntry` or `None` if the line doesn't match
- `severity` — returns the numeric value of the log level (`V=0` up to `F=5`)
- `__str__` — prints the entry in a readable bordered format

### Log Reader

A generator that opens the file and yields one `LogEntry` at a time — never loads the whole file into memory.

### Approaches Compared

| Approach  | How                         | Memory |
| --------- | --------------------------- | ------ |
| Generator | streams one entry at a time | low    |
| List      | loads all entries at once   | high   |

Both are timed and memory-tracked using decorators.

---

## Usage

```python
FILE = "./datasets/Android.log"
count = approach_generator(FILE)
count = approach_list(FILE)
```

---

## References

- [Data Classes — RealPython](https://realpython.com/ref/stdlib/dataclasses/)
- [classmethod — RealPython](https://realpython.com/ref/builtin-functions/classmethod/)
