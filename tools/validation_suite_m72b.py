from pathlib import Path
import json
import cv2

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec

meta = json.load(open("validation/synthetic/metadata.json"))

print("M7.2B Validation Suite")
print("======================")

passed = 0
total = 0

for name, truth in meta.items():
    img = cv2.imread(
        f"validation/synthetic/images/{name}.png",
        cv2.IMREAD_GRAYSCALE,
    )

    ctx = FeatureContext(img)

    c = int(cc(ctx))
    h = int(hc(ctx))
    e = int(ec(ctx))

    ok = (
        c == truth["connected_components"]
        and h == truth["hole_count"]
        and e == truth["euler_characteristic"]
        and e == c - h
    )

    total += 1
    if ok:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(
        f"{name:20} {status:4} "
        f"C={c} H={h} χ={e} "
        f"expected C={truth['connected_components']} "
        f"H={truth['hole_count']} "
        f"χ={truth['euler_characteristic']}"
    )

print()
print(f"V1 Euler validation: {passed}/{total} PASS")
