import cv2
import numpy as np
from pathlib import Path

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec

IMAGE_DIR = Path("validation/reference_v2/images")
NOISE_LEVELS = [0.001, 0.003, 0.005, 0.01, 0.02, 0.03, 0.05]

rng = np.random.default_rng(42)

def topo(img):
    ctx = FeatureContext(img)
    return (
        int(cc(ctx)),
        int(hc(ctx)),
        int(ec(ctx)),
    )

def add_salt_pepper(img, amount):
    noisy = img.copy()

    total = img.size
    n = int(total * amount)

    if n == 0:
        return noisy

    idx = rng.choice(total, size=n, replace=False)

    flat = noisy.reshape(-1)

    half = n // 2

    flat[idx[:half]] = 0
    flat[idx[half:]] = 255

    return noisy

print("M7.3B V7A Noise Stability Profile")
print("=================================")

for path in sorted(IMAGE_DIR.glob("*.png")):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    ref = topo(img)

    critical = None
    critical_state = None

    for level in NOISE_LEVELS:
        noisy = add_salt_pepper(img, level)

        _, noisy = cv2.threshold(
            noisy,
            127,
            255,
            cv2.THRESH_BINARY,
        )

        cur = topo(noisy)

        if cur != ref:
            critical = level
            critical_state = cur
            break

    print(f"\n{path.stem}")
    print(f"  reference : C={ref[0]} H={ref[1]} χ={ref[2]}")

    if critical is None:
        print("  stable to : 5.0% noise")
    else:
        print(f"  critical  : {critical*100:.1f}% noise")
        print(
            f"  changed   : C={critical_state[0]} "
            f"H={critical_state[1]} "
            f"χ={critical_state[2]}"
        )
