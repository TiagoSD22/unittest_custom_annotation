import unittest
from unittestpoc.annotations.parametrize import parametrize
from .fixtures import my_favorite_color  # Import to register the fixture

class TestFavoriteColor(unittest.TestCase):
    
    @parametrize(['orange', 'yellow', 'black'])
    def test_favorite_color_guess(self, guess, my_favorite_color):
        """Test if the guess matches the favorite color"""
        print(f"Testing guess: {guess} against favorite: {my_favorite_color}")
        if guess == 'black':
            self.assertEqual(my_favorite_color, guess)
        else:
            self.assertNotEqual(my_favorite_color, guess)

if __name__ == "__main__":
    unittest.main()