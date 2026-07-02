"""
AncientScriptLab

Image Loader Test
"""

from pathlib import Path

from core.io.image_loader import load_image

IMAGE = Path("tests/data/test.png")

image = load_image(IMAGE)

print()

print("Shape :", image.shape)
print("dtype :", image.dtype)

print()

print("IMAGE LOADER READY")
