import unittest

from unittestpoc.annotations.parametrize import parametrize


# Example usage
class MyTestCase(unittest.TestCase):
    @parametrize([(1, 2), (3, 4)])
    def test_example_multi_without_labels(self, x, y):
        print(f"Running parametrized multiple variables without label test with x={x}, y={y}")
        self.assertTrue(x < y)


if __name__ == "__main__":
    unittest.main()
