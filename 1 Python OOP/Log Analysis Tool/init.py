import re
import time
import tracemalloc
from dataclasses import dataclass
from typing import Optional
import functools

# ─────────────────────────────────────────────
#  Decorators
# ─────────────────────────────────────────────


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [TIMER]  {func.__name__}() → {elapsed:.4f}s")
        return result
    return wrapper


def memory_tracker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(
            f"  [MEMORY] {func.__name__}() → current: {current/1024:.2f} KB | peak: {peak/1024:.2f} KB")
        return result
    return wrapper


# ─────────────────────────────────────────────
#  LogEntry
# ─────────────────────────────────────────────
@dataclass
class LogEntry:
    date: str
    time: str
    pid: int
    tid: int
    level: str
    tag: str
    message: str

    LEVELS = {"V": 0, "D": 1, "I": 2, "W": 3, "E": 4, "F": 5}

    _PATTERN = re.compile(
        r"^(\d{2}-\d{2})\s+"
        r"(\d{2}:\d{2}:\d{2}\.\d+)"
        r"\s+(\d+)\s+(\d+)"
        r"\s+([A-Z])\s+"
        r"([^:]+):\s*"
        r"(.*)"
    )

    @classmethod
    def parse(cls, line: str) -> Optional["LogEntry"]:
        m = cls._PATTERN.match(line)
        if not m:
            return None
        date, time_, pid, tid, level, tag, message = m.groups()
        return cls(
            date=date, time=time_,
            pid=int(pid), tid=int(tid),
            level=level,
            tag=tag.strip(),
            message=message.strip(),
        )

    @property
    def severity(self) -> int:
        return self.LEVELS.get(self.level, -1)

    def __str__(self) -> str:
        return (
            f"┌─ [{self.date}  {self.time}]\n"
            f"│  PID     : {self.pid}\n"
            f"│  TID     : {self.tid}\n"
            f"│  Level   : {self.level}\n"
            f"│  Tag     : {self.tag}\n"
            f"└─ Message : {self.message}\n"
        )


# ─────────────────────────────────────────────
#  Reader
# ─────────────────────────────────────────────
def log_reader(filename: str):
    if not isinstance(filename, str):
        raise TypeError("File name must be str.")
    if not filename.strip():
        raise ValueError("File name must not be empty.")
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        for raw_line in file:
            entry = LogEntry.parse(raw_line.strip())
            if entry:
                yield entry


# ─────────────────────────────────────────────
#  Comparison functions
# ─────────────────────────────────────────────
@timer
@memory_tracker
def approach_generator(filename: str) -> int:
    """Streams one entry at a time — never holds the full file in RAM."""
    count = 0
    for entry in log_reader(filename):
        count += 1          # process and immediately discard
    return count


@timer
@memory_tracker
def approach_list(filename: str) -> int:
    """Loads every entry into a list at once — full file in RAM."""
    entries = list(log_reader(filename))
    return len(entries)


# ─────────────────────────────────────────────
#  Run comparison
# ─────────────────────────────────────────────
FILE = "./datasets/Android.log"

print("=" * 50)
print("  GENERATOR  (lazy, one line at a time)")
print("=" * 50)
count = approach_generator(FILE)
print(f"  Entries processed : {count}\n")

print("=" * 50)
print("  LIST  (eager, entire file into RAM)")
print("=" * 50)
count = approach_list(FILE)
print(f"  Entries loaded    : {count}\n")
