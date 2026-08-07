from pathlib import Path
import csv
import json
import math
import sys
from collections import Counter

if len(sys.argv) != 3:
    print("Usage: python tools/build_corpus_frequency_profile.py <csv_path> <corpus_name>")
    sys.exit(1)

CSV_PATH = Path(sys.argv[1])
CORPUS = sys.argv[2]

OUT_DIR = Path(f"reports/statistics/{CORPUS}")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "frequency_profile.json"
CSV_OUT = OUT_DIR / "sign_frequency_ranking.csv"
MD_OUT = OUT_DIR / "corpus_frequency_profile_v1.md"

signs = []
with open(CSV_PATH, newline="") as f:
    reader = csv.DictReader(f)

    id_column = None
    for candidate in ("sign_id", "image_id"):
        if candidate in reader.fieldnames:
            id_column = candidate
            break

    if id_column is None:
        raise ValueError(f"CSV must contain either 'sign_id' or 'image_id'. Found columns: {reader.fieldnames}")

    for row in reader:
        signs.append(row[id_column])

N = len(signs)
counts = Counter(signs)
unique_signs = len(counts)

frequencies = sorted(counts.items(), key=lambda x: x[1], reverse=True)

entropy = 0.0
for c in counts.values():
    p = c / N
    entropy -= p * math.log2(p)

top10 = sum(c for _, c in frequencies[:10]) / N
top20 = sum(c for _, c in frequencies[:20]) / N

rare_sign_ratio = sum(1 for c in counts.values() if c <= 3) / unique_signs
hapax_legomena = sum(1 for c in counts.values() if c == 1)

vals = sorted(counts.values())
cum = 0
for i, x in enumerate(vals, 1):
    cum += i * x
gini = (2 * cum) / (len(vals) * sum(vals)) - (len(vals) + 1) / len(vals)

profile = {
    "corpus": CORPUS,
    "identifier_column": id_column,
    "tokens": N,
    "unique_signs": unique_signs,
    "frequency_entropy": entropy,
    "top10_coverage": top10,
    "top20_coverage": top20,
    "rare_sign_ratio": rare_sign_ratio,
    "hapax_legomena": hapax_legomena,
    "gini_coefficient": gini,
}

with open(JSON_OUT, "w") as f:
    json.dump(profile, f, indent=2)

with open(CSV_OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank", id_column, "count", "frequency"])
    for i, (sid, c) in enumerate(frequencies, 1):
        w.writerow([i, sid, c, c / N])

with open(MD_OUT, "w") as f:
    f.write(f"# Corpus frequency profile v1.0 ({CORPUS})\\n\\n")
    f.write(f"Corpus: {CORPUS}\\n")
    f.write(f"Identifier column: {id_column}\\n")
    f.write(f"Total sign tokens: {N}\\n")
    f.write(f"Unique signs: {unique_signs}\\n\\n")
    f.write("## Summary\\n\\n")
    f.write(f"- Frequency entropy: {entropy:.6f}\\n")
    f.write(f"- Top-10 sign coverage: {top10:.6f}\\n")
    f.write(f"- Top-20 sign coverage: {top20:.6f}\\n")
    f.write(f"- Rare sign ratio: {rare_sign_ratio:.6f}\\n")
    f.write(f"- Hapax legomena: {hapax_legomena}\\n")
    f.write(f"- Gini coefficient: {gini:.6f}\\n\\n")
    f.write("## Top 20 most frequent signs\\n\\n")
    for sid, c in frequencies[:20]:
        f.write(f"- {sid}: {c} ({c / N:.4%})\\n")

print("M9.1 Corpus frequency profile")
print("=============================")
print(f"Corpus              : {CORPUS}")
print(f"Identifier column   : {id_column}")
print(f"Total sign tokens   : {N}")
print(f"Unique signs        : {unique_signs}")
print(f"Frequency entropy   : {entropy:.3f}")
print(f"Top-10 coverage     : {top10:.3%}")
print(f"Top-20 coverage     : {top20:.3%}")
print(f"Rare sign ratio     : {rare_sign_ratio:.3%}")
print(f"Hapax legomena      : {hapax_legomena}")
print(f"Gini coefficient    : {gini:.3f}")
print()
print(f"JSON report         : {JSON_OUT}")
print(f"CSV ranking         : {CSV_OUT}")
print(f"Markdown report     : {MD_OUT}")
