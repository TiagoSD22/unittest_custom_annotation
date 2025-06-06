import inspect
from functools import wraps

# Global registry to store fixture functions
_fixture_registry = {}

def fixture(func):
    """
    Custom fixture decorator that registers a function to be called
    when its return value is needed as a parameter in test methods.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    
    # Register the fixture function globally
    _fixture_registry[func.__name__] = wrapper
    return wrapper

def get_fixture_value(fixture_name, *args, **kwargs):
    """
    Get the value from a registered fixture function.
    """
    if fixture_name in _fixture_registry:
        return _fixture_registry[fixture_name](*args, **kwargs)
    else:
        raise ValueError(f"Fixture '{fixture_name}' not found. Make sure it's decorated with @fixture.")

def resolve_fixtures(func, test_args, test_kwargs):
    """
    Resolve fixture parameters in a test function by calling the appropriate fixture functions.
    """
    sig = inspect.signature(func)
    param_names = list(sig.parameters.keys())
    
    # Skip 'self' parameter for instance methods
    if param_names and param_names[0] == 'self':
        param_names = param_names[1:]
    
    resolved_kwargs = test_kwargs.copy()
    
    # Check each parameter to see if it matches a fixture
    for param_name in param_names:
        if param_name not in resolved_kwargs and param_name in _fixture_registry:
            # This parameter is a fixture, resolve its value
            resolved_kwargs[param_name] = get_fixture_value(param_name)
    
    return resolved_kwargs