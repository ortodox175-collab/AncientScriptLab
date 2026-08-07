from pathlib import Path
import json
from collections import Counter

SEQ_PATH = Path("validation/examples/corpus_sequence_example.json")
HIER_PATH = Path("reports/statistics/egyptian/hierarchical_archetypes.json")
OUT_DIR = Path("datasets/egyptian/sequences")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "archetype_sequences.json"
MD_OUT = Path("reports/statistics/egyptian/archetype_sequence_report_v1.md")

hier = json.loads(HIER_PATH.read_text())
mapping = {}

for macro in hier["hierarchy"]:
    ma = macro["macro_archetype"]
    for meso in macro["meso_archetypes"]:
        me = meso["meso_archetype"]
        for micro in meso["micro_archetypes"]:
            mi = micro["micro_archetype"]
            for s in micro["sample_signs"]:
                mapping[s] = {
                    "macro": ma,
                    "meso": me,
                    "micro": mi,
                }

seq = json.loads(SEQ_PATH.read_text())
out = []
macro_counter = Counter()
meso_counter = Counter()
micro_counter = Counter()

for ins in seq["inscriptions"]:
    macro_seq = []
    meso_seq = []
    micro_seq = []

    for sign in ins["signs"]:
        a = mapping.get(sign)
        if a is None:
            macro_seq.append(None)
            meso_seq.append(None)
            micro_seq.append(None)
        else:
            macro_seq.append(a["macro"])
            meso_seq.append(a["meso"])
            micro_seq.append(a["micro"])
            macro_counter[a["macro"]] += 1
            meso_counter[a["meso"]] += 1
            micro_counter[a["micro"]] += 1

    out.append({
        "id": ins["id"],
        "sign_sequence": ins["signs"],
        "macro_sequence": macro_seq,
        "meso_sequence": meso_seq,
        "micro_sequence": micro_seq,
    })

result = {
    "module": "M11.1A Archetype Sequence Mapping",
    "inscriptions": len(out),
    "macro_distribution": dict(macro_counter),
    "meso_distribution": dict(meso_counter),
    "micro_distribution": dict(micro_counter),
    "archetype_sequences": out,
}

JSON_OUT.write_text(json.dumps(result, indent=2))

with open(MD_OUT, "w") as f:
    f.write("# Archetype sequence report v1.0\\n\\n")
    f.write(f"Inscriptions: {len(out)}\\n\\n")
    f.write("## Macro distribution\\n\\n")
    for k, v in sorted(macro_counter.items()):
        f.write(f"- Macro {k}: {v}\\n")

print("M11.1A Archetype Sequence Mapping")
print("=================================")
print(f"Inscriptions mapped : {len(out)}")
print(f"JSON dataset        : {JSON_OUT}")
print(f"Markdown report     : {MD_OUT}")
