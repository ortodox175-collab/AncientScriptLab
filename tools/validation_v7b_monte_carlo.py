import cv2
import numpy as np
import json
from pathlib import Path

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec

IMAGE_DIR = Path("validation/reference_v2/images")
REPORT_DIR = Path("reports/metrology/noise/v7b_monte_carlo")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

NOISE_LEVELS = [0.001, 0.003, 0.005, 0.01, 0.02, 0.03, 0.05]
TRIALS = 100

def topo(img):
    ctx = FeatureContext(img)
    return (
        int(cc(ctx)),
        int(hc(ctx)),
        int(ec(ctx)),
    )

def add_salt_pepper(img, amount, rng):
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

print("M7.3B V7B Monte Carlo Noise Metrology")
print("====================================")
print(f"Trials per level: {TRIALS}\\n")

summary = {}

for path in sorted(IMAGE_DIR.glob("*.png")):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    ref = topo(img)

    print(path.stem)
    object_result = {}

    for level in NOISE_LEVELS:
        preserved = 0

        for seed in range(TRIALS):
            rng = np.random.default_rng(seed)
            noisy = add_salt_pepper(img, level, rng)
            _, noisy = cv2.threshold(noisy, 127, 255, cv2.THRESH_BINARY)

            if topo(noisy) == ref:
                preserved += 1

        probability = preserved / TRIALS
        object_result[f"{level:.3f}"] = probability

        print(
            f"  {level*100:4.1f}% noise : "
            f"P={probability:.3f} ({preserved}/{TRIALS})"
        )

    summary[path.stem] = object_result
    print()

out = REPORT_DIR / "noise_probability_profiles.json"

with open(out, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Report saved to: {out}")
