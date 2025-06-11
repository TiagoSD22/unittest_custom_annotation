import unittest
from unittestpoc.annotations.parametrize import parametrize
from unittestpoc.annotations.fixture import fixture

# Test class
class TestColorFixtures(unittest.TestCase):

    def test_int_fixture(self, color_count):
        """Test color count fixture without parametrize"""
        print(f"Color count: {color_count}")
        self.assertEqual(color_count, 3)
        
    def test_list_fixture(self, primary_colors):
        """Test primary colors fixture without parametrize"""
        print(f"Primary colors: {primary_colors}")
        self.assertEqual(len(primary_colors), 3)
        self.assertIn(Color("red"), primary_colors)
    
    def test_custom_class_fixture(self, my_favorite_color):
        """Test custom class fixture without parametrize"""
        print(f"My favorite color: {my_favorite_color}")
        self.assertEqual(my_favorite_color, Color("black"))

    def test_string_fixture(self, my_favorite_color_string):
        """Test string fixture without parametrize"""
        print(f"My favorite color as string: {my_favorite_color_string}")
        self.assertEqual(my_favorite_color_string, "black")

if __name__ == "__main__":
    unittest.main()