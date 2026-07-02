"""
AncientScriptLab

Test:
Bounding Box Engine
"""

import numpy as np

from core.features.geometry.bounding_box import BoundingBoxEngine


# ----------------------------------------------------
# Artificial Binary Image
# ----------------------------------------------------

image = np.zeros((100, 100), dtype=np.uint8)

# Rectangle:
# x = 20..59
# y = 30..69

image[30:70, 20:60] = 255

bbox = BoundingBoxEngine.compute(image)

print()

print("Bounding Box")
print("----------------")
print("x      :", bbox.x)
print("y      :", bbox.y)
print("width  :", bbox.width)
print("height :", bbox.height)

print()

print("Feature G-001 (Width)")
print(
    BoundingBoxEngine.feature_g001(image)
)

print()

print("Feature G-002 (Height)")
print(
    BoundingBoxEngine.feature_g002(image)
)

assert bbox.x == 20
assert bbox.y == 30
assert bbox.width == 40
assert bbox.height == 40

assert BoundingBoxEngine.feature_g001(image) == 40.0
assert BoundingBoxEngine.feature_g002(image) == 40.0

print()
print("BOUNDING BOX ENGINE READY")
