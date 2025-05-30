import unittest
from functools import wraps

def parametrize(values):
    """
    Custom annotation to parametrize a test method with different values
    since unittest package does not have a parametrize option.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Ensure the test method is in a class that extends unittest.TestCase
            instance = args[0] if args else None
            if not isinstance(instance, unittest.TestCase):
                raise TypeError("The @parametrize annotation can only be applied to methods in a class that extends unittest.TestCase.")

            # Execute the test method for each value in the list
            for value in values:
                func(*args, value, **kwargs)
        return wrapper
    return decorator
