import cv2
import numpy as np
from pathlib import Path

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec
from core.algorithms.topology.total_foreground_area import execute as ta
from core.algorithms.topology.largest_component_area import execute as la
from core.algorithms.topology.smallest_component_area import execute as sa
from core.algorithms.topology.mean_component_area import execute as ma
from core.algorithms.topology.component_area_ratio import execute as ar
from core.algorithms.topology.component_density import execute as cd
from core.algorithms.topology.foreground_density import execute as fd

IMAGE_DIR = Path("validation/synthetic/images")
MAX_SHIFT = 5

def features(img):
    ctx = FeatureContext(img)
    return {
        "cc": cc(ctx),
        "hc": hc(ctx),
        "ec": ec(ctx),
        "ta": ta(ctx),
        "la": la(ctx),
        "sa": sa(ctx),
        "ma": ma(ctx),
        "ar": ar(ctx),
        "cd": cd(ctx),
        "fd": fd(ctx),
    }

print("M7.2B V4A Safe Translation Invariance")
print("=====================================")

passed = 0
total = 0

for path in sorted(IMAGE_DIR.glob("*.png")):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    ctx = FeatureContext(img)
    ref = features(img)

    bbox = ctx.bounding_box

    left = bbox.x
    top = bbox.y
    right = 64 - (bbox.x + bbox.width)
    bottom = 64 - (bbox.y + bbox.height)

    dxs = [0]
    dys = [0]

    if left >= MAX_SHIFT:
        dxs.append(-MAX_SHIFT)
    if right >= MAX_SHIFT:
        dxs.append(MAX_SHIFT)
    if top >= MAX_SHIFT:
        dys.append(-MAX_SHIFT)
    if bottom >= MAX_SHIFT:
        dys.append(MAX_SHIFT)

    ok = True

    for dx in dxs:
        for dy in dys:
            if dx == 0 and dy == 0:
                continue

            M = np.float32([[1,0,dx],[0,1,dy]])
            shifted = cv2.warpAffine(
                img,
                M,
                (64,64),
                borderValue=255,
            )

            cur = features(shifted)

            if ref != cur:
                ok = False
                break

        if not ok:
            break

    total += 1

    if ok:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(f"{path.stem:20} {status}")

print()
print(f"V4A Safe Translation validation: {passed}/{total} PASS")
