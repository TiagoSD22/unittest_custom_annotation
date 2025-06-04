# Parametrize with Unittest

This project demonstrates how to implement a `@parametrize` annotation inspired by the `pytest` package, leveraging Python's standard `unittest` library. The goal is to provide a simple and reusable way to parametrize test methods in `unittest` test cases.

## Project Structure

```
unittestpoc/
    __init__.py
    annotations/
        __init__.py
        parametrize.py
    app.py
```

- **`unittestpoc/annotations/parametrize.py`**: Contains the implementation of the `@parametrize` annotation.
- **`app.py`**: Demonstrates the usage of the `@parametrize` annotation in a `unittest.TestCase` class.

## How It Works

The `@parametrize` annotation allows you to run a single test method with multiple sets of input values. It ensures that the test method is executed for each value in the provided list.

### Example Usage

#### Single Parameter

```python
import unittest
from unittestpoc.annotations.parametrize import parametrize

class MyTestCase(unittest.TestCase):
    @parametrize([1, 2, 3])
    def test_example(self, value):
        print(f"Running test with value: {value}")
        self.assertTrue(value > 0)

if __name__ == "__main__":
    unittest.main()
```

#### Multiple Parameters with Labels

```python
class MyTestCase(unittest.TestCase):
    @parametrize("x, y", [(1, 2), (3, 4)])
    def test_example_multi(self, x, y):
        print(f"Running parametrized multiple variables test with x={x}, y={y}")
        self.assertTrue(x < y)
```

#### Multiple Parameters without Labels (Auto-detection)

The decorator can automatically detect parameter names from the function signature:

```python
class MyTestCase(unittest.TestCase):
    @parametrize([(1, 2), (3, 4)])
    def test_example_multi_without_labels(self, x, y):
        print(f"Running parametrized multiple variables without label test with x={x}, y={y}")
        self.assertTrue(x < y)
```

### Output

When running the above examples, the tests will execute multiple times:

**Single parameter:**
```
Running test with value: 1
Running test with value: 2
Running test with value: 3
```

**Multiple parameters:**
```
Running parametrized multiple variables test with x=1, y=2
Running parametrized multiple variables test with x=3, y=4
Running parametrized multiple variables without label test with x=1, y=2
Running parametrized multiple variables without label test with x=3, y=4
```

## Installation

No installation is required as this project uses Python's standard library. Clone the repository and run the `app.py` file to see the example in action.

## Running the Tests

To run the tests, execute the following command:

```bash
python app.py
```

## License

This project is for educational purposes and does not include a specific license.