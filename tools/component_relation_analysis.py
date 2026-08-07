from pathlib import Path
import json
import csv
import cv2
import numpy as np

IMG_DIR = Path("datasets/egyptian/images")
OUT_DIR = Path("datasets/egyptian/component_graphs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "component_relation_graphs.json"
CSV_OUT = OUT_DIR / "component_relation_summary.csv"
REPORT_OUT = Path("reports/metrology/component_relation_report.json")

records = []
csv_rows = []

for img_path in sorted(IMG_DIR.glob("*.png")):
    gray = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

    components = []

    for i in range(1, num_labels):
        x = int(stats[i, cv2.CC_STAT_LEFT])
        y = int(stats[i, cv2.CC_STAT_TOP])
        w = int(stats[i, cv2.CC_STAT_WIDTH])
        h = int(stats[i, cv2.CC_STAT_HEIGHT])
        area = int(stats[i, cv2.CC_STAT_AREA])

        components.append({
            "id": f"C{i}",
            "bbox": [x, y, w, h],
            "centroid": [
                round(float(centroids[i][0]), 3),
                round(float(centroids[i][1]), 3)
            ],
            "area": area
        })

    relations = []

    for i in range(len(components)):
        for j in range(i + 1, len(components)):
            a = components[i]
            b = components[j]

            ax, ay = a["centroid"]
            bx, by = b["centroid"]

            dx = bx - ax
            dy = by - ay

            relation = []

            if abs(dx) < 1e-6:
                relation.append("aligned_x")
            elif dx > 0:
                relation.append("left_of")
            else:
                relation.append("right_of")

            if abs(dy) < 1e-6:
                relation.append("aligned_y")
            elif dy > 0:
                relation.append("above")
            else:
                relation.append("below")

            ax0, ay0, aw, ah = a["bbox"]
            bx0, by0, bw, bh = b["bbox"]

            ax1 = ax0 + aw
            ay1 = ay0 + ah
            bx1 = bx0 + bw
            by1 = by0 + bh

            overlap_x = max(0, min(ax1, bx1) - max(ax0, bx0))
            overlap_y = max(0, min(ay1, by1) - max(ay0, by0))

            if overlap_x > 0 and overlap_y > 0:
                relation.append("overlap")
            elif overlap_x == 0 and overlap_y == 0:
                relation.append("separate")

            relations.append({
                "from": a["id"],
                "to": b["id"],
                "relations": relation,
                "dx": round(float(dx), 3),
                "dy": round(float(dy), 3)
            })

    records.append({
        "image_id": img_path.stem,
        "component_count": len(components),
        "components": components,
        "relations": relations
    })

    csv_rows.append({
        "image_id": img_path.stem,
        "component_count": len(components),
        "relation_count": len(relations)
    })

JSON_OUT.write_text(json.dumps({
    "component_relation_graph_version": "1.0",
    "graphs": records
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
    writer.writeheader()
    writer.writerows(csv_rows)

report = {
    "module": "M10.1D Component Relation Analysis",
    "graphs_processed": len(records),
    "status": "PASS"
}

REPORT_OUT.write_text(json.dumps(report, indent=2))

print("M10.1D Component Relation Analysis")
print("==================================")
print(f"Signs processed : {len(records)}")
print(f"JSON graphs     : {JSON_OUT}")
print(f"CSV summary     : {CSV_OUT}")
print(f"Metrology report: {REPORT_OUT}")
