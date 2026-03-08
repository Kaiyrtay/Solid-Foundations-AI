import unittest
from functools import wraps
import inspect

##################### Decorators #####################


def index_validation(allow_end=False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, index=None, *args, **kwargs):
            if index is None:
                param = inspect.signature(func).parameters.get("index")
                if param and param.default is not inspect.Parameter.empty:
                    index = param.default
                else:
                    raise TypeError(
                        f"{func.__name__}() missing required argument: 'index'")

            if index < 0:
                index = self.size + index

            upper = self.size if allow_end else self.size - 1
            if index < 0 or index > upper:
                raise IndexError(f"Index out of range: 0 - {self.size - 1}")

            return func(self, index, *args, **kwargs)
        return wrapper
    return decorator


class CustomList:

    ####################### Initialization #######################

    def __init__(self):
        self.__data = {}
        self.size = 0

    ###################### Getters and Setters ######################

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    ####################### Methods #######################

    def append(self, value):
        self.__data[self.__size] = value
        self.__size += 1

    def remove(self, value):
        for i in range(self.size):
            if self.__data[i] == value:
                return self.pop(i)
        raise ValueError(f"{value} not in list")

    @index_validation()
    def pop(self, index=-1):
        value = self.__data[index]
        for i in range(index, self.size - 1):
            self.__data[i] = self.__data[i + 1]
        del self.__data[self.size - 1]
        self.size -= 1
        return value

    @index_validation(allow_end=True)
    def insert(self, index, value):
        self.append(None)
        for i in range(self.size - 1, index, -1):
            self.__data[i] = self.__data[i - 1]
        self.__data[index] = value

    def extend(self, iterable):
        for i in iterable:
            self.append(i)

    ####################### Magic Methods #######################

    @index_validation()
    def __getitem__(self, index):
        return self.__data[index]

    @index_validation()
    def __setitem__(self, index, value):
        self.__data[index] = value

    def __len__(self):
        return self.__size

    def __iter__(self):
        for i in range(self.__size):
            yield self.__data[i]

    def __contains__(self, item):
        for i in range(self.__size):
            if self.__data[i] == item:
                return True
        return False

    ######################### String Representation #######################

    def __str__(self):
        return f"CustomList : {[self.__data[i] for i in range(self.__size)]}"

    def __repr__(self):
        return f"CustomList({[self.__data[i] for i in range(self.__size)]})"


class TestCustomList(unittest.TestCase):

    # ── APPEND ──────────────────────────────────────────
    def test_append_single(self):
        c = CustomList()
        c.append(1)
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0], 1)

    def test_append_none(self):
        c = CustomList()
        c.append(None)
        self.assertIsNone(c[0])

    def test_append_duplicates(self):
        c = CustomList()
        c.append(5)
        c.append(5)
        self.assertEqual(len(c), 2)

    def test_append_mixed_types(self):
        c = CustomList()
        for v in [1, "hi", 3.14, True, None]:
            c.append(v)
        self.assertEqual(len(c), 5)

    def test_append_large(self):
        c = CustomList()
        for i in range(10_000):
            c.append(i)
        self.assertEqual(len(c), 10_000)
        self.assertEqual(c[-1], 9999)

    # ── INDEXING ─────────────────────────────────────────
    def test_get_index_zero(self):
        c = CustomList()
        c.append(42)
        self.assertEqual(c[0], 42)

    def test_get_negative_index(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertEqual(c[-1], 3)
        self.assertEqual(c[-3], 1)

    def test_get_out_of_range(self):
        c = CustomList()
        c.append(1)
        with self.assertRaises(IndexError):
            c[5]

    def test_get_negative_out_of_range(self):
        c = CustomList()
        c.append(1)
        with self.assertRaises(IndexError):
            c[-5]

    def test_get_empty_list(self):
        c = CustomList()
        with self.assertRaises(IndexError):
            c[0]

    def test_set_middle(self):
        c = CustomList()
        c.extend([1, 2, 3])
        c[1] = 99
        self.assertEqual(c[1], 99)
        self.assertEqual(c[0], 1)
        self.assertEqual(c[2], 3)

    def test_set_negative_index(self):
        c = CustomList()
        c.extend([1, 2, 3])
        c[-1] = 100
        self.assertEqual(c[2], 100)

    # ── POP ──────────────────────────────────────────────
    def test_pop_default(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertEqual(c.pop(), 3)
        self.assertEqual(len(c), 2)

    def test_pop_index_zero(self):
        c = CustomList()
        c.extend([10, 20, 30])
        self.assertEqual(c.pop(0), 10)
        self.assertEqual(c[0], 20)

    def test_pop_middle(self):
        c = CustomList()
        c.extend([1, 2, 3, 4])
        self.assertEqual(c.pop(2), 3)
        self.assertEqual(list(c), [1, 2, 4])

    def test_pop_negative(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertEqual(c.pop(-2), 2)
        self.assertEqual(list(c), [1, 3])

    def test_pop_single_element(self):
        c = CustomList()
        c.append(99)
        self.assertEqual(c.pop(), 99)
        self.assertEqual(len(c), 0)

    def test_pop_empty_list(self):
        c = CustomList()
        with self.assertRaises(IndexError):
            c.pop()

    def test_pop_out_of_range(self):
        c = CustomList()
        c.extend([1, 2, 3])
        with self.assertRaises(IndexError):
            c.pop(10)

    # ── INSERT ───────────────────────────────────────────
    def test_insert_at_zero(self):
        c = CustomList()
        c.extend([2, 3, 4])
        c.insert(0, 1)
        self.assertEqual(list(c), [1, 2, 3, 4])

    def test_insert_at_end(self):
        c = CustomList()
        c.extend([1, 2, 3])
        c.insert(3, 4)
        self.assertEqual(list(c), [1, 2, 3, 4])

    def test_insert_middle(self):
        c = CustomList()
        c.extend([1, 3, 4])
        c.insert(1, 2)
        self.assertEqual(list(c), [1, 2, 3, 4])

    def test_insert_empty_list(self):
        c = CustomList()
        c.insert(0, 42)
        self.assertEqual(list(c), [42])

    def test_insert_out_of_range(self):
        c = CustomList()
        c.extend([1, 2])
        with self.assertRaises(IndexError):
            c.insert(99, 5)

    # ── REMOVE ───────────────────────────────────────────
    def test_remove_existing(self):
        c = CustomList()
        c.extend([1, 2, 3])
        c.remove(2)
        self.assertEqual(list(c), [1, 3])

    def test_remove_first_occurrence_only(self):
        c = CustomList()
        c.extend([1, 2, 2, 3])
        c.remove(2)
        self.assertEqual(list(c), [1, 2, 3])

    def test_remove_not_found(self):
        c = CustomList()
        c.extend([1, 2, 3])
        with self.assertRaises(ValueError):
            c.remove(99)

    def test_remove_empty_list(self):
        c = CustomList()
        with self.assertRaises(ValueError):
            c.remove(1)

    def test_remove_none(self):
        c = CustomList()
        c.extend([1, None, 3])
        c.remove(None)
        self.assertEqual(list(c), [1, 3])

    # ── EXTEND ───────────────────────────────────────────
    def test_extend_list(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertEqual(list(c), [1, 2, 3])

    def test_extend_empty(self):
        c = CustomList()
        c.append(1)
        c.extend([])
        self.assertEqual(list(c), [1])

    def test_extend_generator(self):
        c = CustomList()
        c.extend(x**2 for x in range(4))
        self.assertEqual(list(c), [0, 1, 4, 9])

    def test_extend_tuple(self):
        c = CustomList()
        c.extend((10, 20, 30))
        self.assertEqual(list(c), [10, 20, 30])

    def test_extend_string(self):
        c = CustomList()
        c.extend("abc")
        self.assertEqual(list(c), ['a', 'b', 'c'])

    # ── CONTAINS ─────────────────────────────────────────
    def test_contains_existing(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertIn(2, c)

    def test_contains_missing(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertNotIn(99, c)

    def test_contains_none(self):
        c = CustomList()
        c.extend([1, None, 3])
        self.assertIn(None, c)

    def test_contains_empty(self):
        c = CustomList()
        self.assertNotIn(1, c)

    # ── ITERATION ────────────────────────────────────────
    def test_iter_order(self):
        c = CustomList()
        c.extend([5, 4, 3, 2, 1])
        self.assertEqual(list(c), [5, 4, 3, 2, 1])

    def test_iter_empty(self):
        c = CustomList()
        self.assertEqual(list(c), [])

    def test_iter_no_mutation(self):
        c = CustomList()
        c.extend([1, 2, 3])
        _ = list(c)
        self.assertEqual(len(c), 3)

    # ── STR / REPR ───────────────────────────────────────
    def test_str(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertEqual(str(c), "CustomList : [1, 2, 3]")

    def test_repr(self):
        c = CustomList()
        c.extend([1, 2, 3])
        self.assertEqual(repr(c), "CustomList([1, 2, 3])")

    def test_str_empty(self):
        c = CustomList()
        self.assertEqual(str(c), "CustomList : []")

    # ── STRESS ───────────────────────────────────────────
    def test_append_then_pop_all(self):
        c = CustomList()
        for i in range(100):
            c.append(i)
        for _ in range(100):
            c.pop()
        self.assertEqual(len(c), 0)

    def test_setitem_reflected_in_contains(self):
        c = CustomList()
        c.extend([1, 2, 3])
        c[1] = 42
        self.assertIn(42, c)
        self.assertNotIn(2, c)

    def test_remove_all_duplicates(self):
        c = CustomList()
        c.extend([7, 7, 7])
        c.remove(7)
        c.remove(7)
        c.remove(7)
        self.assertEqual(len(c), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
