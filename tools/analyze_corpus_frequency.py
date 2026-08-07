from pathlib import Path
import json
import math
import csv
import sys
from collections import Counter
from statistics import mean, median

if len(sys.argv) != 3:
    print("Usage: python tools/analyze_corpus_frequency.py <corpus_sequence.json> <corpus_name>")
    sys.exit(1)

SEQ_PATH = Path(sys.argv[1])
CORPUS = sys.argv[2]

OUT_DIR = Path(f"reports/statistics/{CORPUS}")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "statistical_corpus_passport.json"
CSV_OUT = OUT_DIR / "sign_frequency_distribution.csv"
MD_OUT = OUT_DIR / "statistical_corpus_passport_v1.md"

data = json.loads(SEQ_PATH.read_text())

counter = Counter()
lengths = []

for ins in data["inscriptions"]:
    signs = ins["signs"]
    counter.update(signs)
    lengths.append(len(signs))

N = sum(counter.values())
U = len(counter)

freq = sorted(counter.items(), key=lambda x: x[1], reverse=True)

entropy = 0.0
for c in counter.values():
    p = c / N
    entropy -= p * math.log2(p)

top10 = sum(c for _, c in freq[:10]) / N if N else 0.0
top20 = sum(c for _, c in freq[:20]) / N if N else 0.0

rare = sum(1 for c in counter.values() if c <= 3) / U if U else 0.0
hapax = sum(1 for c in counter.values() if c == 1)

vals = sorted(counter.values())
if vals:
    cum = 0
    for i, x in enumerate(vals, 1):
        cum += i * x
    gini = (2 * cum) / (len(vals) * sum(vals)) - (len(vals) + 1) / len(vals)
else:
    gini = 0.0

passport = {
    "corpus": CORPUS,
    "inscriptions": len(lengths),
    "total_sign_tokens": N,
    "unique_signs": U,
    "frequency_entropy": entropy,
    "top10_coverage": top10,
    "top20_coverage": top20,
    "rare_sign_ratio": rare,
    "hapax_legomena": hapax,
    "gini_coefficient": gini,
    "mean_inscription_length": mean(lengths) if lengths else 0.0,
    "median_inscription_length": median(lengths) if lengths else 0.0,
    "max_inscription_length": max(lengths) if lengths else 0,
    "min_inscription_length": min(lengths) if lengths else 0,
}

JSON_OUT.write_text(json.dumps(passport, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank", "sign_id", "count", "frequency"])
    for i, (sid, c) in enumerate(freq, 1):
        w.writerow([i, sid, c, c / N])

with open(MD_OUT, "w") as f:
    f.write(f"# Statistical corpus passport v1.0 ({CORPUS})\\n\\n")
    for k, v in passport.items():
        if isinstance(v, float):
            f.write(f"- {k}: {v:.6f}\\n")
        else:
            f.write(f"- {k}: {v}\\n")
    f.write("\\n## Top 20 signs\\n\\n")
    for sid, c in freq[:20]:
        f.write(f"- {sid}: {c} ({c / N:.4%})\\n")

print("M9.1 Statistical Corpus Passport")
print("================================")
print(f"Corpus                 : {CORPUS}")
print(f"Inscriptions           : {passport['inscriptions']}")
print(f"Total sign tokens      : {N}")
print(f"Unique signs           : {U}")
print(f"Frequency entropy      : {entropy:.3f}")
print(f"Top-10 coverage        : {top10:.3%}")
print(f"Top-20 coverage        : {top20:.3%}")
print(f"Rare sign ratio        : {rare:.3%}")
print(f"Hapax legomena         : {hapax}")
print(f"Gini coefficient       : {gini:.3f}")
print(f"Mean inscription length: {passport['mean_inscription_length']:.3f}")
print()
print(f"JSON report            : {JSON_OUT}")
print(f"CSV distribution       : {CSV_OUT}")
print(f"Markdown passport      : {MD_OUT}")
