from functools import wraps


def str_not_empty(attribute_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, str):
                raise TypeError(f"{attribute_name} must be a string")
            if not value.strip():
                raise ValueError(f"{attribute_name} must not be empty")
            return func(self, value)
        return wrapper
    return decorator


def non_negative_int(attribute_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, int):
                raise TypeError(f"{attribute_name} must be an integer")
            if value < 0:
                raise ValueError(f"{attribute_name} cannot be negative")
            return func(self, value)
        return wrapper
    return decorator


def non_negative_float(attribute_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError(f"{attribute_name} must be a number")
            if value < 0:
                raise ValueError(f"{attribute_name} cannot be negative")
            return func(self, value)
        return wrapper
    return decorator
