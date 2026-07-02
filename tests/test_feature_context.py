"""
AncientScriptLab

FeatureContext Test
"""

import numpy as np

from core.context.feature_context import FeatureContext
from core.features.geometry.bounding_box import BoundingBoxFeatures

image = np.zeros((100, 100), dtype=np.uint8)

image[30:70, 20:60] = 255

ctx = FeatureContext(image)

print()
print("Bounding Box")
print(ctx.bounding_box)

print()
print("Width :", BoundingBoxFeatures.feature_g001(ctx))
print("Height:", BoundingBoxFeatures.feature_g002(ctx))

assert ctx.bounding_box.x == 20
assert ctx.bounding_box.y == 30
assert ctx.bounding_box.width == 40
assert ctx.bounding_box.height == 40

assert BoundingBoxFeatures.feature_g001(ctx) == 40.0
assert BoundingBoxFeatures.feature_g002(ctx) == 40.0

print()
print("FEATURE CONTEXT V2 READY")
