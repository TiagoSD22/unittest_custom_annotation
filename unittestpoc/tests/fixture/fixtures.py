from unittestpoc.annotations.fixture import fixture
# Define fixtures

# Example Custom class
class Color:
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        if isinstance(other, Color):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        return False
    
    def __repr__(self):
        return f"Color('{self.name}')"

# Example fixture returning a custom class instance
@fixture
def my_favorite_color():
    return Color("black")

# Example fixture returning a list of custom class objects
@fixture
def primary_colors():
    return [Color("red"), Color("green"), Color("blue")]

# Example fixture returning an integer
@fixture
def color_count():
    return 3

# Example fixture returning a string
@fixture
def my_favorite_color_string():
    return "black"