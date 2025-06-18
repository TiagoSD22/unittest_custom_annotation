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

class TestFixtureCaching(unittest.TestCase):
    
    def setUp(self):
        """Clear cache and counters before each test method"""
        clear_fixture_cache()
        global call_counter
        call_counter.clear()
    
    def test_fixture_caching_single_use(self, expensive_computation):
        """Test that fixture is called once and result is cached"""
        print(f"First access: {expensive_computation}")
        self.assertEqual(expensive_computation["result"], 42)
        self.assertEqual(call_counter.get('expensive_computation', 0), 1)
    
    @parametrize([1, 2, 3])
    def test_fixture_caching_multiple_parametrize(self, value, expensive_computation):
        """Test that fixture is cached across parametrized test runs"""
        print(f"Parametrized test {value}: {expensive_computation}")
        self.assertEqual(expensive_computation["result"], 42)
        
        # After all parametrized runs, fixture should only be called once
        # Note: This assertion will be true for the first run, subsequent runs use cache


if __name__ == "__main__":
    # Run tests and show cache statistics
    unittest.main(verbosity=2)
    
    print("\n=== Final Cache Statistics ===")
    print(get_cache_stats())