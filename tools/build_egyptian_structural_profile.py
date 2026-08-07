from pathlib import Path
import csv
import json
import math
from collections import Counter
from statistics import mean, median

CSV_PATH = Path("datasets/egyptian/features/egyptian_feature_vectors.csv")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_PATH = OUT_DIR / "structural_profile.json"
SUMMARY_PATH = OUT_DIR / "distribution_summary.json"

FEATURES = [
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

def percentile(sorted_values, p):
    if not sorted_values:
        return None
    k = (len(sorted_values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_values[int(k)]
    return sorted_values[f] + (sorted_values[c] - sorted_values[f]) * (k - f)

def entropy(values):
    counts = Counter(values)
    total = len(values)
    h = 0.0
    for count in counts.values():
        p = count / total
        h -= p * math.log2(p)
    return h

rows = []
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

profile = {
    "corpus": "Egyptian",
    "images": len(rows),
    "features": {},
}

summary = {}

for feature in FEATURES:
    values = [float(r[feature]) for r in rows]
    values_sorted = sorted(values)

    stats = {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "std": (
            math.sqrt(
                sum((x - mean(values)) ** 2 for x in values) / len(values)
            )
            if values
            else 0.0
        ),
        "min": min(values),
        "max": max(values),
        "q1": percentile(values_sorted, 0.25),
        "q3": percentile(values_sorted, 0.75),
        "entropy": entropy(values),
    }

    profile["features"][feature] = stats

    counts = Counter(values)
    hist_path = OUT_DIR / (
        "histogram_" + feature.split(".")[1] + ".csv"
    )
    with open(hist_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["value", "count"])
        for value in sorted(counts.keys()):
            w.writerow([value, counts[value]])

    summary[feature] = {
        "unique_values": len(counts),
        "most_common": counts.most_common(10),
    }

with open(PROFILE_PATH, "w") as f:
    json.dump(profile, f, indent=2)

with open(SUMMARY_PATH, "w") as f:
    json.dump(summary, f, indent=2)

print("M8.2 Egyptian structural profile")
print("================================")
print(f"Images analyzed : {len(rows)}")
print(f"Profile         : {PROFILE_PATH}")
print(f"Summary         : {SUMMARY_PATH}")
print(f"Histograms      : {OUT_DIR}")
