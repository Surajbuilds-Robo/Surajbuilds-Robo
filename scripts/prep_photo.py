#!/usr/bin/env python3
"""
prep_photo.py
-------------
Preprocesses an input image for ASCII conversion:
1. Loads the source image (default: my.jpg).
2. Center-crops the image to a perfect 1:1 square ratio.
3. Resizes to high-resolution standard dimensions (500x500).
4. Converts the image to high-contrast grayscale.
5. Applies brightness and contrast enhancements for ASCII rendering.
6. Isolates portrait features and saves the output to source-prepped.png.
"""

import os
import sys
from PIL import Image, ImageEnhance, ImageOps

def prep_photo(input_path: str = "/home/end/Downloads/my.jpg", output_path: str = "source-prepped.png"):
    """
    Reads input_path image, crops to square, enhances contrast, and saves to output_path.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    print(f"Loading image from '{input_path}'...")
    img = Image.open(input_path)

    # 1. Convert RGBA/CMYK images to RGB
    if img.mode != "RGB":
        img = img.convert("RGB")

    # 2. Center crop to 1:1 square
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    
    img_cropped = img.crop((left, top, right, bottom))
    print(f"Cropped {width}x{height} image to {min_dim}x{min_dim} square.")

    # 3. Resize to high-res working square (500x500)
    target_size = (500, 500)
    img_resized = img_cropped.resize(target_size, Image.Resampling.LANCZOS)

    # 4. Convert to Grayscale
    gray = ImageOps.grayscale(img_resized)

    # 5. Contrast & Brightness Enhancement
    # Enhancing contrast highlights edges and textures for clearer ASCII mapping
    contrast_enhancer = ImageEnhance.Contrast(gray)
    high_contrast = contrast_enhancer.enhance(1.8)

    brightness_enhancer = ImageEnhance.Brightness(high_contrast)
    prepped_img = brightness_enhancer.enhance(1.1)

    # 6. Save prepped image
    prepped_img.save(output_path, "PNG")
    print(f"Successfully saved prepped image to '{output_path}'.")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "my.jpg"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "source-prepped.png"
    prep_photo(input_file, output_file)
