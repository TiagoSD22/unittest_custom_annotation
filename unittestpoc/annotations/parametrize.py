import unittest
import inspect
from functools import wraps

def parametrize(variables_or_values, values=None):
    """
    Custom annotation to parametrize a test method with optional variables
    and a list of values or tuples of values for each execution.
    """
    if values is None:
        # If only a list of values is provided, auto-detect parameters from function signature
        values = variables_or_values
        variables = None  # Will be determined from function signature
    else:
        # Handle the case where variables and values are provided
        if isinstance(variables_or_values, str):
            variables = [var.strip() for var in variables_or_values.split(",")]
        else:
            raise TypeError("Variables must be a string of comma-separated names.")

    def decorator(func):
        # Auto-detect parameter names from function signature if not provided
        if variables is None:
            sig = inspect.signature(func)
            # Skip 'self' parameter for instance methods
            param_names = list(sig.parameters.keys())
            if param_names and param_names[0] == 'self':
                param_names = param_names[1:]
            detected_variables = param_names
        else:
            detected_variables = variables

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
                if len(value_tuple) != len(detected_variables):
                    raise ValueError(f"Each tuple of values must match the number of parameters. Expected {len(detected_variables)} parameters: {detected_variables}, got {len(value_tuple)} values.")
                func(*args, **dict(zip(detected_variables, value_tuple)), **kwargs)
        return wrapper
    return decorator