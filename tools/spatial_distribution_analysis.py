from pathlib import Path
import json
import csv
import cv2
import numpy as np

IMG_DIR = Path("datasets/egyptian/images")
OUT_DIR = Path("datasets/egyptian/signatures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "structural_signatures_v1_1.json"
CSV_OUT = OUT_DIR / "structural_signatures_v1_1.csv"
REPORT_OUT = Path("reports/metrology/spatial_distribution_report.json")

def safe_div(a, b):
    return float(a) / float(b) if b else 0.0

records = []

for img_path in sorted(IMG_DIR.glob("*.png")):
    gray = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    h, w = binary.shape
    total_mass = cv2.countNonZero(binary)

    ys, xs = np.where(binary > 0)
    if total_mass == 0:
        cx = 0.0
        cy = 0.0
    else:
        cx = float(xs.mean()) / w
        cy = float(ys.mean()) / h

    mid_x = w // 2
    mid_y = h // 2

    q1 = cv2.countNonZero(binary[0:mid_y, 0:mid_x])
    q2 = cv2.countNonZero(binary[0:mid_y, mid_x:w])
    q3 = cv2.countNonZero(binary[mid_y:h, 0:mid_x])
    q4 = cv2.countNonZero(binary[mid_y:h, mid_x:w])

    t1 = h // 3
    t2 = 2 * h // 3

    top = cv2.countNonZero(binary[0:t1, :])
    middle = cv2.countNonZero(binary[t1:t2, :])
    bottom = cv2.countNonZero(binary[t2:h, :])

    l1 = w // 3
    l2 = 2 * w // 3

    left = cv2.countNonZero(binary[:, 0:l1])
    center = cv2.countNonZero(binary[:, l1:l2])
    right = cv2.countNonZero(binary[:, l2:w])

    yy, xx = np.indices(binary.shape)
    dist = np.sqrt((xx - w/2.0)**2 + (yy - h/2.0)**2)
    radius = min(w, h) * 0.25

    core_mask = dist <= radius
    outer_mask = dist > radius

    core = int(np.count_nonzero(binary[core_mask]))
    outer = int(np.count_nonzero(binary[outer_mask]))

    records.append({
        "image_id": img_path.stem,
        "centroid_x_normalized": round(cx, 6),
        "centroid_y_normalized": round(cy, 6),
        "mass_q1": round(safe_div(q1, total_mass), 6),
        "mass_q2": round(safe_div(q2, total_mass), 6),
        "mass_q3": round(safe_div(q3, total_mass), 6),
        "mass_q4": round(safe_div(q4, total_mass), 6),
        "mass_top": round(safe_div(top, total_mass), 6),
        "mass_middle": round(safe_div(middle, total_mass), 6),
        "mass_bottom": round(safe_div(bottom, total_mass), 6),
        "mass_left": round(safe_div(left, total_mass), 6),
        "mass_center": round(safe_div(center, total_mass), 6),
        "mass_right": round(safe_div(right, total_mass), 6),
        "mass_core": round(safe_div(core, total_mass), 6),
        "mass_outer": round(safe_div(outer, total_mass), 6)
    })

JSON_OUT.write_text(json.dumps({
    "structural_signature_version": "1.1",
    "feature_count": 14,
    "signatures": records
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

report = {
    "module": "M10.1C Spatial Distribution Analysis",
    "structural_signature_version": "1.1",
    "images_processed": len(records),
    "feature_count": 14,
    "status": "PASS"
}

REPORT_OUT.write_text(json.dumps(report, indent=2))

print("M10.1C Spatial Distribution Analysis")
print("====================================")
print(f"Images processed : {len(records)}")
print(f"Feature count    : 14")
print(f"JSON dataset     : {JSON_OUT}")
print(f"CSV dataset      : {CSV_OUT}")
print(f"Metrology report : {REPORT_OUT}")
