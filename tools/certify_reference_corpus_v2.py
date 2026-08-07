import json
from pathlib import Path
import cv2

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec

IMAGE_DIR = Path("validation/reference_v2/images")
META_PATH = Path("validation/reference_v2/metadata.json")
REPORT_DIR = Path("reports/metrology")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

meta = json.load(open(META_PATH))

report = {
    "corpus": "Reference Corpus v2.0",
    "version": "2.0",
    "objects": len(meta),
    "results": {},
}

passed = 0
total = 0

print("M7.3A Reference Corpus Certification")
print("====================================")

for name, truth in sorted(meta.items()):
    img = cv2.imread(str(IMAGE_DIR / f"{name}.png"), cv2.IMREAD_GRAYSCALE)
    ctx = FeatureContext(img)

    measured = {
        "components": int(cc(ctx)),
        "holes": int(hc(ctx)),
        "euler": int(ec(ctx)),
    }

    ok = measured == truth

    report["results"][name] = {
        "truth": truth,
        "measured": measured,
        "pass": ok,
    }

    total += 1

    if ok:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(
        f"{name:20} {status}  "
        f"truth={truth} measured={measured}"
    )

report["passed"] = passed
report["total"] = total
report["certified"] = (passed == total)

out = REPORT_DIR / "reference_corpus_v2_certification.json"

with open(out, "w") as f:
    json.dump(report, f, indent=2)

print()
print(f"Certification: {passed}/{total} PASS")

if passed == total:
    print("Reference Corpus v2.0 CERTIFIED")
else:
    print("Reference Corpus v2.0 NOT CERTIFIED")

print(f"Report saved to: {out}")
