import json
import cv2
import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.foreground_density import execute as density
from core.algorithms.topology.total_foreground_area import execute as total_area

meta = json.load(open("validation/synthetic/metadata.json"))

IMAGE_AREA = 64 * 64

print("M7.2B V3 Density Identity")
print("=========================")

passed = 0
total = 0

for name in meta.keys():
    img = cv2.imread(
        f"validation/synthetic/images/{name}.png",
        cv2.IMREAD_GRAYSCALE,
    )

    ctx = FeatureContext(img)

    d_alg = float(density(ctx))
    area = int(total_area(ctx))
    d_formula = area / IMAGE_AREA

    binary = ctx.binary
    d_numpy = np.count_nonzero(binary) / IMAGE_AREA

    ok = (
        abs(d_alg - d_formula) < 1e-9
        and abs(d_alg - d_numpy) < 1e-9
    )

    total += 1
    if ok:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(
        f"{name:20} {status:4} "
        f"alg={d_alg:.9f} formula={d_formula:.9f} numpy={d_numpy:.9f}"
    )

print()
print(f"V3 Density validation: {passed}/{total} PASS")
