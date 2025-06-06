import unittest

from unittestpoc.annotations.parametrize import parametrize


# Example usage
class MyTestCase(unittest.TestCase):
    # Parallel execution with 3 threads
    @parametrize([(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)], threads=3)
    def test_example_multi_threaded(self, x, y):
        print(f"Running threaded test with x={x}, y={y}.")
        self.assertTrue(x < y)

if __name__ == "__main__":
    unittest.main()
