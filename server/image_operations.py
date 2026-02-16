"""Pure image transformation functions.

Each function takes a PIL.Image and returns a new PIL.Image.
Parameterised operations are implemented as factory functions that return
a closure matching the same signature.
"""

from PIL import Image, ImageOps


def flip_horizontal(image: Image.Image) -> Image.Image:
    """Flip the image top-to-bottom (horizontal axis mirror)."""
    return ImageOps.flip(image)


def flip_vertical(image: Image.Image) -> Image.Image:
    """Flip the image left-to-right (vertical axis mirror)."""
    return ImageOps.mirror(image)


def rotate_degrees(angle: float):
    """Return a function that rotates the image by *angle* degrees CCW."""
    def _rotate(image: Image.Image) -> Image.Image:
        return image.rotate(angle, expand=True)
    return _rotate


def convert_grayscale(image: Image.Image) -> Image.Image:
    """Convert the image to grayscale (mode 'L'), then back to 'RGB'."""
    return image.convert("L").convert("RGB")


def resize(width: int, height: int):
    """Return a function that resizes the image to exact *width* x *height*."""
    def _resize(image: Image.Image) -> Image.Image:
        return image.resize((width, height), Image.Resampling.LANCZOS)
    return _resize


def thumbnail(max_width: int, max_height: int):
    """Return a function that shrinks the image to fit within the given bounds."""
    def _thumbnail(image: Image.Image) -> Image.Image:
        img = image.copy()
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        return img
    return _thumbnail


def rotate_left(image: Image.Image) -> Image.Image:
    """Rotate the image 90 degrees counter-clockwise."""
    return image.rotate(90, expand=True)


def rotate_right(image: Image.Image) -> Image.Image:
    """Rotate the image 90 degrees clockwise."""
    return image.rotate(-90, expand=True)
