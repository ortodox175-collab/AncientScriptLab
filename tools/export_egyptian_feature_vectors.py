from pathlib import Path
import json
import csv
from datetime import datetime
import cv2

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as connected_components
from core.algorithms.topology.hole_count import execute as hole_count
from core.algorithms.topology.euler_characteristic import execute as euler_characteristic
from core.algorithms.topology.total_foreground_area import execute as total_foreground_area
from core.algorithms.topology.largest_component_area import execute as largest_component_area
from core.algorithms.topology.smallest_component_area import execute as smallest_component_area
from core.algorithms.topology.mean_component_area import execute as mean_component_area
from core.algorithms.topology.component_area_ratio import execute as component_area_ratio
from core.algorithms.topology.foreground_density import execute as foreground_density
from core.algorithms.topology.component_density import execute as component_density

IMAGE_DIR = Path("datasets/egyptian/images")
OUT_DIR = Path("datasets/egyptian/features")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = OUT_DIR / "egyptian_feature_vectors.csv"
JSON_PATH = OUT_DIR / "egyptian_feature_vectors.json"
META_PATH = OUT_DIR / "export_metadata.json"

FIELDNAMES = [
    "image_id",
    "topology.connected_components",
    "topology.hole_count",
    "topology.euler_characteristic",
    "topology.total_foreground_area",
    "topology.largest_component_area",
    "topology.smallest_component_area",
    "topology.mean_component_area",
    "topology.component_area_ratio",
    "topology.foreground_density",
    "topology.component_density",
]

rows = []

for path in sorted(IMAGE_DIR.glob("*.png")):
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue

    ctx = FeatureContext(img)

    row = {
        "image_id": path.stem,
        "topology.connected_components": float(connected_components(ctx)),
        "topology.hole_count": float(hole_count(ctx)),
        "topology.euler_characteristic": float(euler_characteristic(ctx)),
        "topology.total_foreground_area": float(total_foreground_area(ctx)),
        "topology.largest_component_area": float(largest_component_area(ctx)),
        "topology.smallest_component_area": float(smallest_component_area(ctx)),
        "topology.mean_component_area": float(mean_component_area(ctx)),
        "topology.component_area_ratio": float(component_area_ratio(ctx)),
        "topology.foreground_density": float(foreground_density(ctx)),
        "topology.component_density": float(component_density(ctx)),
    }

    rows.append(row)

with open(CSV_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(rows)

with open(JSON_PATH, "w") as f:
    json.dump(rows, f, indent=2)

metadata = {
    "corpus": "Egyptian",
    "images_processed": len(rows),
    "feature_count": len(FIELDNAMES) - 1,
    "metrology_standard": "METROLOGY.md v1.0",
    "reference_corpus": "Reference Corpus v2.0 (CERTIFIED 10/10 PASS)",
    "validation_status": "Certified topology pipeline",
    "export_timestamp_utc": datetime.utcnow().isoformat() + "Z",
}

with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print("M8.1 Egyptian Feature Vector Export")
print("=================================")
print(f"Images processed : {len(rows)}")
print(f"CSV             : {CSV_PATH}")
print(f"JSON            : {JSON_PATH}")
print(f"Metadata        : {META_PATH}")
