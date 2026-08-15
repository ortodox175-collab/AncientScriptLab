"""
AncientScriptLab

Bounding Box regression test.

Uses canonical FeatureContext foreground convention.
"""

import numpy as np

from core.context.feature_context import FeatureContext
from core.features.geometry.bounding_box import BoundingBoxFeatures


image = np.full((100, 100), 255, dtype=np.uint8)

# Foreground rectangle:
# x = 20..59
# y = 30..69
image[30:70, 20:60] = 0

ctx = FeatureContext(image)
bbox = ctx.bounding_box

assert bbox.x == 20
assert bbox.y == 30
assert bbox.width == 40
assert bbox.height == 40

assert BoundingBoxFeatures.feature_g001(ctx) == 40.0
assert BoundingBoxFeatures.feature_g002(ctx) == 40.0

print("BOUNDING BOX CONTRACT: PASS")
