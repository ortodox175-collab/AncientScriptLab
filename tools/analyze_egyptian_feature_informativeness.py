from pathlib import Path
import csv
import json
import math
from collections import Counter
from statistics import mean, median

CSV_PATH = Path("datasets/egyptian/features/egyptian_feature_vectors.csv")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "feature_informativeness.json"
CSV_OUT = OUT_DIR / "feature_ranking.csv"
MD_OUT = OUT_DIR / "baseline_egyptian_profile_v1.md"

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

rows = []
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

N = len(rows)
results = {}

for feature in FEATURES:
    values = [float(r[feature]) for r in rows]
    counts = Counter(values)

    m = mean(values)
    var = sum((x - m) ** 2 for x in values) / N
    std = math.sqrt(var)

    cv = std / abs(m) if abs(m) > 1e-12 else 0.0

    h = 0.0
    for c in counts.values():
        p = c / N
        h -= p * math.log2(p)

    unique_ratio = len(counts) / N
    dominant_ratio = counts.most_common(1)[0][1] / N

    discriminative_power = 1.0 - dominant_ratio

    score = (
        0.35 * (h / max(math.log2(len(counts)), 1e-9))
        + 0.25 * min(cv, 1.0)
        + 0.20 * unique_ratio
        + 0.20 * discriminative_power
    )

    results[feature] = {
        "mean": m,
        "median": median(values),
        "variance": var,
        "std": std,
        "coefficient_of_variation": cv,
        "entropy": h,
        "unique_values": len(counts),
        "unique_value_ratio": unique_ratio,
        "dominant_value_ratio": dominant_ratio,
        "discriminative_power": discriminative_power,
        "informativeness_score": score,
    }

ranking = sorted(
    results.items(),
    key=lambda x: x[1]["informativeness_score"],
    reverse=True,
)

with open(JSON_OUT, "w") as f:
    json.dump(results, f, indent=2)

with open(CSV_OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(
        [
            "rank",
            "feature",
            "score",
            "entropy",
            "cv",
            "unique_ratio",
            "discriminative_power",
        ]
    )
    for i, (feature, r) in enumerate(ranking, 1):
        w.writerow(
            [
                i,
                feature,
                r["informativeness_score"],
                r["entropy"],
                r["coefficient_of_variation"],
                r["unique_value_ratio"],
                r["discriminative_power"],
            ]
        )

core = [f for f, r in ranking if r["informativeness_score"] >= 0.60]
supporting = [
    f
    for f, r in ranking
    if 0.40 <= r["informativeness_score"] < 0.60
]
weak = [f for f, r in ranking if r["informativeness_score"] < 0.40]

with open(MD_OUT, "w") as f:
    f.write("# Baseline Egyptian structural profile v1.0\\n\\n")
    f.write(f"Images analyzed: {N}\\n\\n")

    f.write("## Feature ranking\\n\\n")
    for i, (feature, r) in enumerate(ranking, 1):
        f.write(
            f"{i}. {feature}: {r['informativeness_score']:.3f}\\n"
        )

    f.write("\\n## Core Feature Set\\n\\n")
    for feature in core:
        f.write(f"- {feature}\\n")

    f.write("\\n## Supporting features\\n\\n")
    for feature in supporting:
        f.write(f"- {feature}\\n")

    f.write("\\n## Weak features\\n\\n")
    for feature in weak:
        f.write(f"- {feature}\\n")

print("M8.2A Egyptian feature informativeness analysis")
print("==============================================")
print(f"Images analyzed : {N}")
print(f"JSON report     : {JSON_OUT}")
print(f"CSV ranking     : {CSV_OUT}")
print(f"Markdown report : {MD_OUT}")
print()
print("Top 5 informative features:")
for i, (feature, r) in enumerate(ranking[:5], 1):
    print(f"{i}. {feature}: {r['informativeness_score']:.3f}")
