import inspect
from functools import wraps

# Global registry to store fixture functions
_fixture_registry = {}
# Global cache to store fixture results
_fixture_cache = {}

def fixture(func):
    """
    Custom fixture decorator that registers a function to be called
    when its return value is needed as a parameter in test methods.
    Results are cached to avoid redundant function calls.
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
    Uses caching to avoid redundant calls.
    """
    if fixture_name in _fixture_registry:
        # Create a cache key based on fixture name and arguments
        cache_key = _create_cache_key(fixture_name, args, kwargs)
        
        # Check if value is already cached
        if cache_key in _fixture_cache:
            return _fixture_cache[cache_key]
        
        # Call fixture function and cache the result
        result = _fixture_registry[fixture_name](*args, **kwargs)
        _fixture_cache[cache_key] = result
        return result
    else:
        raise ValueError(f"Fixture '{fixture_name}' not found. Make sure it's decorated with @fixture.")

def _create_cache_key(fixture_name, args, kwargs):
    """
    Create a unique cache key based on fixture name and arguments.
    """
    # Convert args and kwargs to a hashable representation
    args_str = str(args) if args else ""
    kwargs_str = str(sorted(kwargs.items())) if kwargs else ""
    return f"{fixture_name}:{args_str}:{kwargs_str}"

def clear_fixture_cache(fixture_name=None):
    """
    Clear the fixture cache. If fixture_name is provided, only clear that fixture.
    Otherwise, clear the entire cache.
    """
    global _fixture_cache
    if fixture_name is None:
        _fixture_cache.clear()
    else:
        # Remove all cache entries for the specific fixture
        keys_to_remove = [key for key in _fixture_cache.keys() if key.startswith(f"{fixture_name}:")]
        for key in keys_to_remove:
            del _fixture_cache[key]

def get_cache_stats():
    """
    Get cache statistics for debugging and monitoring.
    """
    return {
        "total_cached_fixtures": len(_fixture_cache),
        "cached_fixtures": list(_fixture_cache.keys()),
        "registered_fixtures": list(_fixture_registry.keys())
    }

def resolve_fixtures(func, test_args, test_kwargs):
    """
    Resolve fixture parameters in a test function by calling the appropriate fixture functions.
    Uses caching to improve performance.
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
            # This parameter is a fixture, resolve its value (with caching)
            resolved_kwargs[param_name] = get_fixture_value(param_name)
    
    return resolved_kwargs