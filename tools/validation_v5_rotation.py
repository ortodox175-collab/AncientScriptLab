import cv2
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

print("M7.2B V5 Rotation Invariance")
print("============================")

passed = 0
total = 0

rotations = [
    cv2.ROTATE_90_CLOCKWISE,
    cv2.ROTATE_180,
    cv2.ROTATE_90_COUNTERCLOCKWISE,
]

for path in sorted(IMAGE_DIR.glob("*.png")):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    ref = features(img)

    ok = True

    for rot in rotations:
        rotated = cv2.rotate(img, rot)
        cur = features(rotated)

        if ref != cur:
            ok = False
            break

    total += 1

    if ok:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(f"{path.stem:20} {status}")

print()
print(f"V5 Rotation validation: {passed}/{total} PASS")
