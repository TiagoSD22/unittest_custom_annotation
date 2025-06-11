# Import all fixtures to ensure they are registered when the package is imported
from .fixtures import my_favorite_color, primary_colors, color_count, Color

__all__ = ['my_favorite_color', 'primary_colors', 'color_count', 'Color']