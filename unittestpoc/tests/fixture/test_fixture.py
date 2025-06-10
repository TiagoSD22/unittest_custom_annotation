import unittest
from unittestpoc.annotations.parametrize import parametrize
from unittestpoc.annotations.fixture import fixture

# Example Color class
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

# Define fixtures
@fixture
def my_favorite_color():
    return Color("black")

@fixture
def primary_colors():
    return [Color("red"), Color("green"), Color("blue")]

@fixture
def color_count():
    return 3

# Test class
class TestColorFixtures(unittest.TestCase):
    
    @parametrize(['orange', 'yellow', 'black'])
    def test_favorite_color_guess(self, guess, my_favorite_color):
        """Test if the guess matches the favorite color"""
        print(f"Testing guess: {guess} against favorite: {my_favorite_color}")
        if guess == 'black':
            self.assertEqual(my_favorite_color, guess)
        else:
            self.assertNotEqual(my_favorite_color, guess)
    
    @parametrize([1, 2, 3, 4])
    def test_color_count(self, count, color_count):
        """Test color count fixture"""
        print(f"Testing count: {count} against fixture count: {color_count}")
        if count == 3:
            self.assertEqual(count, color_count)
        else:
            self.assertNotEqual(count, color_count)
    
    def test_primary_colors_fixture(self, primary_colors):
        """Test primary colors fixture without parametrize"""
        print(f"Primary colors: {primary_colors}")
        self.assertEqual(len(primary_colors), 3)
        self.assertIn(Color("red"), primary_colors)

if __name__ == "__main__":
    unittest.main()