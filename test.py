from __future__ import print_function
from PIL import Image

path = "./input/john.png"

# Open an Image
def open_image(path):
    image = Image.open(path)
    print(image.format, image.size, image.mode)
    return image

# Save Image
def save_image(image, path):
    image.save(path, 'png')

# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image

# Get the pixel from the given image
def get_pixel(image, i, j):
# Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

# Show image
def show_image (image):
    image.show()
    
"""
Main function
"""
img = open_image (path)
