import unittest
import inspect
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
import threading
from .fixture import resolve_fixtures

def parametrize(variables_or_values, values=None, threads=1):
    """
    Custom annotation to parametrize a test method with optional variables
    and a list of values or tuples of values for each execution.
    
    Args:
        variables_or_values: Either variable names (str) or values list
        values: List of value tuples (when variables_or_values is str)
        threads: Number of threads for parallel execution (default: 1)
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

    # Validate threads parameter
    if not isinstance(threads, int) or threads < 1:
        raise ValueError("threads parameter must be an integer >= 1")

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

            # Prepare test executions
            test_executions = []
            for value_tuple in values:
                if not isinstance(value_tuple, tuple):
                    value_tuple = (value_tuple,)
                
                # Only validate against parametrized variables, not fixture parameters
                parametrized_vars = [var for var in detected_variables if var not in resolve_fixtures(func, args, kwargs)]
                
                if len(value_tuple) != len(parametrized_vars):
                    raise ValueError(f"Each tuple of values must match the number of parametrized parameters. Expected {len(parametrized_vars)} parameters: {parametrized_vars}, got {len(value_tuple)} values.")
                test_executions.append(value_tuple)

            def execute_single_test(value_tuple):
                """Execute a single test with the given parameters"""
                try:
                    # Create kwargs with parametrized values
                    param_kwargs = dict(zip([var for var in detected_variables if var not in resolve_fixtures(func, args, kwargs)], value_tuple))
                    
                    # Resolve fixtures and merge with parametrized values
                    resolved_kwargs = resolve_fixtures(func, args, {**kwargs, **param_kwargs})
                    
                    func(*args, **resolved_kwargs)
                    return None  # Success
                except Exception as e:
                    return e  # Return exception for later handling

            if threads == 1:
                # Sequential execution (original behavior)
                for value_tuple in test_executions:
                    result = execute_single_test(value_tuple)
                    if result is not None:  # Exception occurred
                        raise result
            else:
                # Parallel execution using ThreadPoolExecutor
                exceptions = []
                with ThreadPoolExecutor(max_workers=threads) as executor:
                    # Submit all test executions
                    futures = [executor.submit(execute_single_test, value_tuple) 
                             for value_tuple in test_executions]
                    
                    # Collect results and exceptions
                    for future in futures:
                        result = future.result()
                        if result is not None:  # Exception occurred
                            exceptions.append(result)
                
                # If any exceptions occurred, raise the first one
                if exceptions:
                    raise exceptions[0]

        return wrapper
    return decorator