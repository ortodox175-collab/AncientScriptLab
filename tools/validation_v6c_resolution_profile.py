import cv2
from pathlib import Path

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec

IMAGE_DIR = Path("validation/synthetic/images")
SCALES = [1.00, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0.50]

def topo(img):
    ctx = FeatureContext(img)
    return (
        int(cc(ctx)),
        int(hc(ctx)),
        int(ec(ctx)),
    )

print("M7.2B V6C Resolution Stability Profile")
print("======================================")

for path in sorted(IMAGE_DIR.glob("*.png")):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    ref = topo(img)

    print(f"\n{path.stem}")
    print(f"  reference: C={ref[0]} H={ref[1]} χ={ref[2]}")

    for scale in SCALES[1:]:
        small = cv2.resize(
            img,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA,
        )

        _, small = cv2.threshold(
            small,
            127,
            255,
            cv2.THRESH_BINARY,
        )

        restored = cv2.resize(
            small,
            (64,64),
            interpolation=cv2.INTER_NEAREST,
        )

        cur = topo(restored)

        changed = cur != ref

        status = "CHANGED" if changed else "stable "

        print(
            f"  {int(scale*100):2d}%  {status}  "
            f"C={cur[0]} H={cur[1]} χ={cur[2]}"
        )

        if changed:
            break
