import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.foreground_density import execute


# 4x4 image, 4 foreground pixels
img = np.full((4, 4), 255, dtype=np.uint8)
img[1:3, 1:3] = 0

ctx = FeatureContext(img)

value = execute(ctx)

assert value == 4 / 16, value
assert value == 0.25

print("FOREGROUND DENSITY CONTRACT: PASS")
