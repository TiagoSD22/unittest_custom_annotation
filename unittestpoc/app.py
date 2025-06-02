import unittest

from unittestpoc.annotations.parametrize import parametrize


# Example usage
class MyTestCase(unittest.TestCase):
    @parametrize([1, 2, 3])
    def test_example(self, value):
        print(f"Running parametrized test with value: {value}")
        self.assertTrue(value > 0)

    @parametrize("x, y", [(1, 2), (3, 4)])
    def test_example_multi(self, x, y):
        print(f"Running parametrized multiple variables test with x={x}, y={y}")
        self.assertTrue(x < y)

if __name__ == "__main__":
    unittest.main()
