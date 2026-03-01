from functools import wraps


def str_not_empty_validation(attr_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, str):
                raise TypeError(f"{attr_name} must be a string")
            if not value.strip():
                raise ValueError(f"{attr_name} cannot be empty")
            return func(self, value)
        return wrapper
    return decorator
