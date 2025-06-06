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

