import unittest
from functools import wraps

def parametrize(variables_or_values, values=None):
    """
    Custom annotation to parametrize a test method with optional variables
    and a list of values or tuples of values for each execution.
    """
    if values is None:
        # If only a list of values is provided, treat it as single-variable cases
        variables = ["value"]
        values = variables_or_values
    else:
        # Handle the case where variables and values are provided
        if isinstance(variables_or_values, str):
            variables = [var.strip() for var in variables_or_values.split(",")]
        else:
            raise TypeError("Variables must be a string of comma-separated names.")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Ensure the test method is in a class that extends unittest.TestCase
            instance = args[0] if args else None
            if not isinstance(instance, unittest.TestCase):
                raise TypeError("The @parametrize annotation can only be applied to methods in a class that extends unittest.TestCase.")

            # Execute the test method for each tuple of values
            for value_tuple in values:
                if not isinstance(value_tuple, tuple):
                    value_tuple = (value_tuple,)
                if len(value_tuple) != len(variables):
                    raise ValueError("Each tuple of values must match the number of variables.")
                func(*args, **dict(zip(variables, value_tuple)), **kwargs)
        return wrapper
    return decorator