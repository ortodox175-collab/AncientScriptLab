from pathlib import Path
import json
import csv
import math
from collections import Counter
from statistics import mean, median, pstdev

SIG_PATH = Path("datasets/egyptian/signatures/structural_signatures.json")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "structural_primitive_informativeness.json"
CSV_OUT = OUT_DIR / "structural_primitive_ranking.csv"
MD_OUT = OUT_DIR / "structural_primitive_report_v1.md"

data = json.loads(SIG_PATH.read_text())
rows = data["signatures"]

features = [k for k in rows[0].keys() if k != "image_id"]

results = []

for feat in features:
    values = [r[feat] for r in rows]
    cnt = Counter(values)

    entropy = 0.0
    for c in cnt.values():
        p = c / len(values)
        entropy -= p * math.log2(p)

    unique = len(cnt)
    vmin = min(values)
    vmax = max(values)
    m = mean(values)
    med = median(values)
    std = pstdev(values)
    cv = std / abs(m) if abs(m) > 1e-9 else 0.0

    score = 0.45 * (entropy / math.log2(unique) if unique > 1 else 0.0) + 0.35 * min(cv, 2.0) / 2.0 + 0.20 * min(unique / len(values), 1.0)

    results.append({
        "feature": feat,
        "entropy": entropy,
        "unique_values": unique,
        "min": vmin,
        "max": vmax,
        "mean": m,
        "median": med,
        "std": std,
        "cv": cv,
        "informativeness": score,
    })

results.sort(key=lambda x: x["informativeness"], reverse=True)

JSON_OUT.write_text(json.dumps(results, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank", "feature", "informativeness", "entropy", "unique_values", "cv"])
    for i, r in enumerate(results, 1):
        w.writerow([i, r["feature"], round(r["informativeness"], 6), round(r["entropy"], 6), r["unique_values"], round(r["cv"], 6)])

with open(MD_OUT, "w") as f:
    f.write("# Structural primitive informativeness report v1.0\\n\\n")
    f.write(f"Signs analyzed: {len(rows)}\\n\\n")
    f.write("## Ranking\\n\\n")
    for i, r in enumerate(results, 1):
        f.write(f"{i}. {r['feature']} — {r['informativeness']:.3f}\\n")

print("M10.1B Structural primitive informativeness")
print("==========================================")
print(f"Signs analyzed : {len(rows)}")
print(f"Features       : {len(features)}")
print()
print("Top 5 informative primitives:")
for i, r in enumerate(results[:5], 1):
    print(f"{i}. {r['feature']}: {r['informativeness']:.3f}")
print()
print(f"JSON report    : {JSON_OUT}")
print(f"CSV ranking    : {CSV_OUT}")
print(f"Markdown report: {MD_OUT}")
