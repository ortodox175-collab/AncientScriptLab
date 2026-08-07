from pathlib import Path
import json
import csv
from collections import Counter

CSV_PATH = Path("datasets/egyptian/raw/gardiner_sequences.csv")
OUT_DIR = Path("datasets/egyptian/corpus")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "egyptian_corpus_sequence.json"
MD_OUT = Path("reports/statistics/egyptian/egyptian_corpus_sequence_report_v1.md")

if not CSV_PATH.exists():
    print("M11.1B Egyptian CorpusSequence Construction")
    print("===========================================")
    print("Source file not found:")
    print(CSV_PATH)
    print()
    print("Expected CSV format:")
    print("inscription_id,sequence")
    print("E001,A12 D36 G17 N5")
    print("E002,G1 Z1 D21")
    raise SystemExit(1)

inscriptions = []
total_tokens = 0
lengths = []
sign_counter = Counter()

with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        seq = [s.strip() for s in row["sequence"].split() if s.strip()]
        inscriptions.append({
            "id": row["inscription_id"],
            "signs": seq,
            "source": "Gardiner",
            "confidence": 1.0
        })
        total_tokens += len(seq)
        lengths.append(len(seq))
        sign_counter.update(seq)

corpus = {
    "corpus": "Egyptian",
    "version": "1.0",
    "inscriptions": inscriptions,
    "statistics": {
        "inscription_count": len(inscriptions),
        "total_sign_tokens": total_tokens,
        "unique_signs": len(sign_counter),
        "mean_length": round(sum(lengths)/len(lengths), 3) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "min_length": min(lengths) if lengths else 0,
    }
}

JSON_OUT.write_text(json.dumps(corpus, indent=2))

with open(MD_OUT, "w", encoding="utf-8") as f:
    f.write("# Egyptian CorpusSequence Report v1.0\\n\\n")
    f.write(f"Inscriptions: {len(inscriptions)}\\n")
    f.write(f"Total sign tokens: {total_tokens}\\n")
    f.write(f"Unique signs: {len(sign_counter)}\\n")
    if lengths:
        f.write(f"Mean length: {sum(lengths)/len(lengths):.3f}\\n")

print("M11.1B Egyptian CorpusSequence Construction")
print("===========================================")
print(f"Inscriptions      : {len(inscriptions)}")
print(f"Total sign tokens : {total_tokens}")
print(f"Unique signs      : {len(sign_counter)}")
print()
print(f"JSON corpus       : {JSON_OUT}")
print(f"Markdown report   : {MD_OUT}")
