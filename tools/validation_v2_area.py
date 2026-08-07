import json
import cv2

from core.context.feature_context import FeatureContext
from core.algorithms.topology.total_foreground_area import execute as total_area
from core.algorithms.topology.largest_component_area import execute as largest_area
from core.algorithms.topology.smallest_component_area import execute as smallest_area
from core.algorithms.topology.mean_component_area import execute as mean_area
from core.algorithms.topology.component_area_ratio import execute as ratio

meta = json.load(open("validation/synthetic/metadata.json"))

print("M7.2B V2 Area Conservation")
print("===========================")

passed = 0
total = 0

for name, truth in meta.items():
    img = cv2.imread(
        f"validation/synthetic/images/{name}.png",
        cv2.IMREAD_GRAYSCALE,
    )

    ctx = FeatureContext(img)

    t = int(total_area(ctx))
    l = int(largest_area(ctx))
    s = int(smallest_area(ctx))
    m = float(mean_area(ctx))
    r = float(ratio(ctx))

    expected = truth["foreground_area"]

    area_ok = abs(t - expected) <= 5
    conservation_ok = l <= t and s <= m <= l

    ok = area_ok and conservation_ok

    total += 1
    if ok:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(
        f"{name:20} {status:4} "
        f"total={t:4d} expected={expected:4d} "
        f"largest={l:4d} smallest={s:4d} "
        f"mean={m:7.2f} ratio={r:.3f}"
    )

print()
print(f"V2 Area validation: {passed}/{total} PASS")
