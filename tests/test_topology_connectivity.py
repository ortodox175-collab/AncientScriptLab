import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as components
from core.algorithms.topology.hole_count import execute as holes


def context_from_binary(binary):
    # FeatureContext expects dark foreground in source image.
    image = np.where(binary > 0, 0, 255).astype(np.uint8)
    return FeatureContext(image)


# ------------------------------------------------------------
# TEST 1
# Diagonally touching foreground pixels belong to one component
# under foreground 8-connectivity.
# ------------------------------------------------------------

binary = np.array([
    [255,   0,   0],
    [  0, 255,   0],
    [  0,   0,   0],
], dtype=np.uint8)

ctx = context_from_binary(binary)

assert components(ctx) == 1.0, (
    f"Expected 1 foreground component, got {components(ctx)}"
)


# ------------------------------------------------------------
# TEST 2
# Central background pixel touches exterior only diagonally.
#
# With correct complementary topology:
#   foreground = 8-connectivity
#   background = 4-connectivity
#
# the central pixel is a hole.
#
# Old 8/8 implementation incorrectly returned 0.
# ------------------------------------------------------------

binary = np.array([
    [255, 255,   0],
    [255,   0, 255],
    [255, 255, 255],
], dtype=np.uint8)

ctx = context_from_binary(binary)

assert components(ctx) == 1.0, (
    f"Expected 1 foreground component, got {components(ctx)}"
)

assert holes(ctx) == 1.0, (
    f"Expected 1 hole with background 4-connectivity, got {holes(ctx)}"
)

print("TOPOLOGY CONNECTIVITY REGRESSION: PASS")
print("foreground connectivity = 8")
print("background connectivity = 4")
