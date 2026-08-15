import numpy as np

from core.context.feature_context import FeatureContext


# valid uint8 grayscale
source = np.full((5, 5), 255, dtype=np.uint8)
source[2, 2] = 0

ctx = FeatureContext(source)

assert ctx.image.dtype == np.uint8
assert ctx.image.ndim == 2
assert ctx.image.flags.writeable is False

# context must own an independent copy
source[2, 2] = 255
assert ctx.image[2, 2] == 0
assert ctx.binary[2, 2] == 255

# cached binary must also be protected
assert ctx.binary.flags.writeable is False

# wrong dimensionality
try:
    FeatureContext(np.zeros((5, 5, 3), dtype=np.uint8))
    raise AssertionError("3D image accepted unexpectedly")
except ValueError:
    pass

# wrong dtype
try:
    FeatureContext(np.zeros((5, 5), dtype=np.float32))
    raise AssertionError("float32 image accepted unexpectedly")
except TypeError:
    pass

print("FEATURE CONTEXT CONTRACT: PASS")
