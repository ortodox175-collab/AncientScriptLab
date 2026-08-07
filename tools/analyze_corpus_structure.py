from pathlib import Path
import json
import math
import csv
import sys
from collections import Counter
from statistics import mean, median

if len(sys.argv) != 3:
    print("Usage: python tools/analyze_corpus_structure.py <corpus_sequence.json> <corpus_name>")
    sys.exit(1)

SEQ_PATH = Path(sys.argv[1])
CORPUS = sys.argv[2]

OUT_DIR = Path(f"reports/statistics/{CORPUS}")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "structural_corpus_passport.json"
CSV_OUT = OUT_DIR / "inscription_structure_metrics.csv"
MD_OUT = OUT_DIR / "structural_corpus_passport_v1.md"

data = json.loads(SEQ_PATH.read_text())

rows = []
lengths = []
diversities = []
entropies = []
repeat_densities = []

for ins in data["inscriptions"]:
    signs = ins["signs"]
    L = len(signs)
    lengths.append(L)

    unique = len(set(signs))
    diversity = unique / L if L else 0.0
    diversities.append(diversity)

    cnt = Counter(signs)
    entropy = 0.0
    for c in cnt.values():
        p = c / L
        entropy -= p * math.log2(p)
    entropies.append(entropy)

    repeated_tokens = sum(c - 1 for c in cnt.values() if c > 1)
    repeat_density = repeated_tokens / L if L else 0.0
    repeat_densities.append(repeat_density)

    rows.append({
        "id": ins["id"],
        "length": L,
        "unique_signs": unique,
        "lexical_diversity": diversity,
        "inscription_entropy": entropy,
        "repeat_density": repeat_density,
    })

passport = {
    "corpus": CORPUS,
    "inscriptions": len(rows),
    "mean_length": mean(lengths) if lengths else 0.0,
    "median_length": median(lengths) if lengths else 0.0,
    "min_length": min(lengths) if lengths else 0,
    "max_length": max(lengths) if lengths else 0,
    "mean_lexical_diversity": mean(diversities) if diversities else 0.0,
    "median_lexical_diversity": median(diversities) if diversities else 0.0,
    "mean_inscription_entropy": mean(entropies) if entropies else 0.0,
    "median_inscription_entropy": median(entropies) if entropies else 0.0,
    "mean_repeat_density": mean(repeat_densities) if repeat_densities else 0.0,
    "median_repeat_density": median(repeat_densities) if repeat_densities else 0.0,
}

JSON_OUT.write_text(json.dumps(passport, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=[
        "id",
        "length",
        "unique_signs",
        "lexical_diversity",
        "inscription_entropy",
        "repeat_density",
    ])
    w.writeheader()
    w.writerows(rows)

with open(MD_OUT, "w") as f:
    f.write(f"# Structural corpus passport v1.0 ({CORPUS})\\n\\n")
    for k, v in passport.items():
        if isinstance(v, float):
            f.write(f"- {k}: {v:.6f}\\n")
        else:
            f.write(f"- {k}: {v}\\n")

print("M9.1A Structural Corpus Passport")
print("=================================")
print(f"Corpus                    : {CORPUS}")
print(f"Inscriptions              : {passport['inscriptions']}")
print(f"Mean inscription length   : {passport['mean_length']:.3f}")
print(f"Median inscription length : {passport['median_length']:.3f}")
print(f"Mean lexical diversity    : {passport['mean_lexical_diversity']:.3f}")
print(f"Mean inscription entropy  : {passport['mean_inscription_entropy']:.3f}")
print(f"Mean repeat density       : {passport['mean_repeat_density']:.3f}")
print()
print(f"JSON report               : {JSON_OUT}")
print(f"CSV metrics               : {CSV_OUT}")
print(f"Markdown passport         : {MD_OUT}")
