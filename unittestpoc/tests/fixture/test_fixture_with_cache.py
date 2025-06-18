import unittest
import time
from unittestpoc.annotations.parametrize import parametrize
from unittestpoc.annotations.fixture import fixture, clear_fixture_cache, get_cache_stats

# Counter to track how many times fixtures are called
call_counter = {}

@fixture
def expensive_computation():
    """Simulate an expensive computation that should be cached"""
    global call_counter
    call_counter['expensive_computation'] = call_counter.get('expensive_computation', 0) + 1
    
    print(f"Computing expensive result... (call #{call_counter['expensive_computation']})")
    time.sleep(0.1)  # Simulate expensive operation
    return {"result": 42, "computed_at": time.time()}

@fixture
def database_mock():
    """Simulate database connection setup"""
    global call_counter
    call_counter['database_mock'] = call_counter.get('database_mock', 0) + 1
    
    print(f"Setting up database mock... (call #{call_counter['database_mock']})")
    return {"connection": "mock_db", "tables": ["users", "orders"]}

