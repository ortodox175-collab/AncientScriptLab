import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.geometry.aspect_ratio import execute, ALGORITHM
from core.packs.geometry_pack import GeometryPack


img = np.full((10, 10), 255, dtype=np.uint8)
img[2:6, 3:9] = 0

ctx = FeatureContext(img)

direct = execute(ctx)
packed = GeometryPack().get("aspect_ratio").implementation(ctx)

assert direct == 1.5
assert packed == direct
assert GeometryPack().get("aspect_ratio") is ALGORITHM

print("ASPECT RATIO ARCHITECTURE: PASS")
