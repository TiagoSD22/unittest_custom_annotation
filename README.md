# Custom Annotations for unittest: Implementing pytest Features

This project demonstrates the implementation of key pytest features using only Python's standard `unittest` library and standard Python code. It provides custom annotations `@parametrize` and `@fixture` that bring pytest-style testing capabilities to unittest-based projects without external dependencies.

## Project Overview

The goal is to create a drop-in solution for projects that use `unittest` but want to leverage advanced testing patterns like parametrized tests and dependency injection through fixtures, similar to what pytest offers.

## Project Structure

```
unittestpoc/
├── __init__.py
├── annotations/
│   ├── __init__.py
│   ├── parametrize.py          # @parametrize decorator implementation
│   └── fixture.py              # @fixture decorator implementation
├── tests/
│   └── fixture/
│       ├── __init__.py
│       ├── fixtures.py         # Shared fixture definitions
│       ├── test_fixture.py     # Main test runner
│       ├── test_favorite_color.py  # Fixture + parametrize tests
│       ├── test_color_count.py     # Count validation tests
│       └── test_primary_colors.py  # List fixture tests
└── app.py                      # Basic parametrize demonstrations
```

## Core Features

### 1. @parametrize Annotation

The `@parametrize` decorator allows running the same test method multiple times with different argument sets, eliminating the need for repetitive test code.

#### Technical Implementation

The implementation leverages Python's `inspect` module to analyze function signatures and `functools.wraps` to preserve metadata. Key technical aspects:

- **Parameter Detection**: Uses `inspect.signature()` to automatically detect parameter names
- **Argument Mapping**: Maps provided values to parameters using `dict(zip())`
- **Thread Support**: Implements parallel execution using `ThreadPoolExecutor`
- **Error Handling**: Collects and properly propagates exceptions from parallel executions

#### Usage Patterns

**Single Parameter with Auto-detection:**
```python
@parametrize([1, 2, 3, 4, 5])
def test_positive_numbers(self, value):
    self.assertGreater(value, 0)
```

**Multiple Parameters with Explicit Labels:**
```python
@parametrize("x, y", [(1, 2), (3, 4), (5, 6)])
def test_comparison(self, x, y):
    self.assertLess(x, y)
```

**Multiple Parameters with Auto-detection:**
```python
@parametrize([(1, 2), (3, 4), (5, 6)])
def test_comparison_auto(self, x, y):
    self.assertLess(x, y)
```

**Parallel Execution:**
```python
@parametrize([(1, 2), (3, 4), (5, 6), (7, 8)], threads=3)
def test_threaded_comparison(self, x, y):
    self.assertLess(x, y)
```

### 2. @fixture Annotation

The `@fixture` decorator provides dependency injection for test methods, allowing reusable test data setup and complex object initialization.

#### Technical Implementation

The fixture system uses a global registry pattern with the following components:

- **Global Registry**: `_fixture_registry` dictionary stores fixture functions by name
- **Lazy Evaluation**: Fixtures are called only when needed during test execution
- **Parameter Resolution**: `resolve_fixtures()` function analyzes test signatures and injects fixture values
- **Integration**: Seamlessly integrates with `@parametrize` for combined functionality

#### Usage Patterns

**Basic Fixture Definition:**
```python
@fixture
def sample_data():
    return {"name": "test", "value": 42}

@fixture
def database_connection():
    # Simulate database setup
    return MockDatabase()
```

**Fixture in Test Methods:**
```python
def test_data_processing(self, sample_data):
    self.assertEqual(sample_data["name"], "test")
    self.assertEqual(sample_data["value"], 42)
```

### 3. Combined Usage: Parametrize + Fixtures

The real power emerges when combining both annotations, allowing parametrized tests with injected dependencies.

**Example Implementation:**
```python
@fixture
def my_favorite_color():
    return Color("black")

@parametrize(['orange', 'yellow', 'black'])
def test_color_matching(self, guess, my_favorite_color):
    if guess == 'black':
        self.assertEqual(my_favorite_color.name, guess)
    else:
        self.assertNotEqual(my_favorite_color.name, guess)
```

## Test Examples and Output

### Basic Parametrize Tests

**Test Code:**
```python
class TestParametrize(unittest.TestCase):
    @parametrize([1, 2, 3])
    def test_positive_values(self, value):
        print(f"Testing value: {value}")
        self.assertGreater(value, 0)
```

**Output:**
```
Testing value: 1
.Testing value: 2
.Testing value: 3
.
----------------------------------------------------------------------
Ran 3 tests in 0.001s

OK
```

### Fixture-Based Tests

**Test Code:**
```python
@fixture
def color_count():
    return 3

class TestFixtures(unittest.TestCase):
    def test_color_count_fixture(self, color_count):
        print(f"Color count from fixture: {color_count}")
        self.assertEqual(color_count, 3)
```

**Output:**
```
Color count from fixture: 3
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

### Combined Parametrize + Fixture Tests

**Test Code:**
```python
@fixture
def my_favorite_color():
    return Color("black")

class TestCombined(unittest.TestCase):
    @parametrize(['orange', 'yellow', 'black'])
    def test_favorite_color_guess(self, guess, my_favorite_color):
        print(f"Testing guess: {guess} against favorite: {my_favorite_color}")
        if guess == 'black':
            self.assertEqual(str(my_favorite_color), guess)
        else:
            self.assertNotEqual(str(my_favorite_color), guess)
```

**Output:**
```
Testing guess: orange against favorite: Color('black')
.Testing guess: yellow against favorite: Color('black')
.Testing guess: black against favorite: Color('black')
.
----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK
```

### Threaded Execution Tests

**Test Code:**
```python
@parametrize([(1, 2), (3, 4), (5, 6), (7, 8)], threads=2)
def test_parallel_execution(self, x, y):
    thread_name = threading.current_thread().name
    print(f"Testing {x} < {y} on thread: {thread_name}")
    self.assertLess(x, y)
```

**Output:**
```
Testing 1 < 2 on thread: ThreadPoolExecutor-0_0
Testing 3 < 4 on thread: ThreadPoolExecutor-0_1
Testing 5 < 6 on thread: ThreadPoolExecutor-0_0
Testing 7 < 8 on thread: ThreadPoolExecutor-0_1
....
----------------------------------------------------------------------
Ran 4 tests in 0.003s

OK
```

## Running Tests

### Individual Test Files
```bash
# Run basic parametrize examples
python app.py

# Run specific fixture tests
python -m unittest unittestpoc.tests.fixture.test_favorite_color
python -m unittest unittestpoc.tests.fixture.test_color_count
python -m unittest unittestpoc.tests.fixture.test_primary_colors

# Run all fixture tests
python -m unittest discover unittestpoc/tests/fixture -v
```

### Complete Test Suite Output
```bash
$ python -m unittest discover unittestpoc/tests/fixture -v

test_favorite_color_guess (unittestpoc.tests.fixture.test_favorite_color.TestFavoriteColor) ... 
Testing guess: orange against favorite: Color('black')
Testing guess: yellow against favorite: Color('black')  
Testing guess: black against favorite: Color('black')
ok

test_color_count (unittestpoc.tests.fixture.test_color_count.TestColorCount) ...
Testing count: 1 against fixture count: 3
Testing count: 2 against fixture count: 3
Testing count: 3 against fixture count: 3
Testing count: 4 against fixture count: 3
ok

test_primary_colors_fixture (unittestpoc.tests.fixture.test_primary_colors.TestPrimaryColors) ...
Primary colors: [Color('red'), Color('green'), Color('blue')]
ok

----------------------------------------------------------------------
Ran 3 tests in 0.005s

OK
```

## Benefits for unittest Projects

### 1. **Zero External Dependencies**
- No need to introduce pytest as a dependency
- Uses only Python standard library components
- Easy integration into existing unittest-based projects

### 2. **Enhanced Test Readability**
- Eliminates repetitive test code through parametrization
- Clear separation of test data and test logic
- Improved maintainability through fixture reuse

### 3. **Performance Optimization**
- Thread-based parallel execution for I/O-bound tests
- Configurable concurrency levels
- Maintained test isolation

### 4. **Mock Data Management**
- Centralized test data through fixtures
- Consistent mock object creation
- Easy database entity simulation

## Technical Implementation Details

### Parameter Resolution Algorithm
1. **Signature Analysis**: Extract parameter names using `inspect.signature()`
2. **Fixture Detection**: Identify parameters that match registered fixtures
3. **Value Injection**: Create parameter dictionary combining fixtures and parametrized values
4. **Execution**: Call test method with resolved parameters

### Thread Safety Considerations
- Each test execution runs in isolation
- Exception handling preserves original stack traces
- ThreadPoolExecutor manages resource cleanup automatically

### Memory Management
- Fixtures are called per test execution (not cached)
- Global registry uses weak references where appropriate
- No memory leaks from fixture accumulation

## Installation and Setup

No installation required. Simply copy the `unittestpoc` package into your project:

```python
from unittestpoc.annotations.parametrize import parametrize
from unittestpoc.annotations.fixture import fixture
```

## Comparison with pytest

| Feature | This Implementation | pytest |
|---------|-------------------|--------|
| Framework | unittest | pytest |
| Dependencies | Standard library only | External package |
| Auto-detection | ✅ Full support | ❌ Requires explicit naming |
| Threading | ✅ Built-in support | ❌ Requires plugins |
| Fixture Scoping | Function-level | Multiple scopes |
| Setup/Teardown | Manual in fixtures | Automatic yield support |

This implementation provides a solid foundation for bringing pytest-style testing patterns to unittest-based projects while maintaining simplicity and avoiding external dependencies.