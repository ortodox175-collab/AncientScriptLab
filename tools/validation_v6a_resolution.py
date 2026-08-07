import cv2
from pathlib import Path

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec

IMAGE_DIR = Path("validation/synthetic/images")
SCALES = [1.00, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30]

def topo(img):
    ctx = FeatureContext(img)
    return (
        int(cc(ctx)),
        int(hc(ctx)),
        int(ec(ctx)),
    )

print("M7.2B V6A Resolution Robustness")
print("================================")

for path in sorted(IMAGE_DIR.glob("*.png")):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    ref = topo(img)

    critical = None

    for scale in SCALES[1:]:
        resized = cv2.resize(
            img,
            None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_NEAREST,
        )

        canvas = 255 * cv2.UMat(64,64,cv2.CV_8UC1).get()

        h, w = resized.shape
        x = (64 - w) // 2
        y = (64 - h) // 2
        canvas[y:y+h, x:x+w] = resized

        cur = topo(canvas)

        if cur != ref:
            critical = scale
            break

    if critical is None:
        result = "stable down to 30%"
    else:
        result = f"changes at {int(critical*100)}%"

    print(f"{path.stem:20} {result}")
