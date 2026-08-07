from pathlib import Path
import json
import csv
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering

GRAPH_PATH = Path("datasets/egyptian/primitive_graphs/primitive_graphs.json")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "hierarchical_archetypes.json"
CSV_OUT = OUT_DIR / "hierarchical_archetype_assignments.csv"
MD_OUT = OUT_DIR / "hierarchical_archetype_report_v1.md"

data = json.loads(GRAPH_PATH.read_text())
graphs = data["graphs"]

X = []
image_ids = []

for g in graphs:
    s = g["graph_signature"]
    X.append([
        float(s["node_count"]),
        float(s["edge_count"]),
        float(s["endpoint_count"]),
        float(s["junction_count"]),
        float(s["average_degree"]),
    ])
    image_ids.append(g["image_id"])

X = np.array(X)
X = StandardScaler().fit_transform(X)

macro = AgglomerativeClustering(n_clusters=3)
macro_labels = macro.fit_predict(X)

meso_labels = np.zeros(len(X), dtype=int)
micro_labels = np.zeros(len(X), dtype=int)

meso_offset = 0
micro_offset = 0

for m in sorted(set(macro_labels)):
    idx = np.where(macro_labels == m)[0]
    if len(idx) < 6:
        meso_labels[idx] = meso_offset
        micro_labels[idx] = micro_offset
        meso_offset += 1
        micro_offset += 1
        continue

    k_meso = min(4, max(2, len(idx)//40))
    meso = AgglomerativeClustering(n_clusters=k_meso)
    local_meso = meso.fit_predict(X[idx])

    for local_id in sorted(set(local_meso)):
        sub = idx[np.where(local_meso == local_id)[0]]
        meso_labels[sub] = meso_offset

        if len(sub) < 4:
            micro_labels[sub] = micro_offset
            micro_offset += 1
        else:
            k_micro = min(3, max(2, len(sub)//20))
            micro = AgglomerativeClustering(n_clusters=k_micro)
            local_micro = micro.fit_predict(X[sub])

            for lm in sorted(set(local_micro)):
                final = sub[np.where(local_micro == lm)[0]]
                micro_labels[final] = micro_offset
                micro_offset += 1

        meso_offset += 1

hierarchy = []

for m in sorted(set(macro_labels)):
    idx = np.where(macro_labels == m)[0]
    meso_ids = sorted(set(meso_labels[idx]))

    hierarchy.append({
        "macro_archetype": int(m),
        "sign_count": int(len(idx)),
        "meso_archetypes": [
            {
                "meso_archetype": int(me),
                "sign_count": int(np.sum(meso_labels[idx] == me)),
                "micro_archetypes": [
                    {
                        "micro_archetype": int(mi),
                        "sign_count": int(np.sum(micro_labels[idx] == mi)),
                        "sample_signs": [
                            image_ids[j]
                            for j in idx[np.where(micro_labels[idx] == mi)[0]][:8]
                        ],
                    }
                    for mi in sorted(set(micro_labels[idx][meso_labels[idx] == me]))
                ],
            }
            for me in meso_ids
        ],
    })

JSON_OUT.write_text(json.dumps({
    "module": "M10.1J Hierarchical Archetype Extraction",
    "macro_count": int(len(set(macro_labels))),
    "meso_count": int(len(set(meso_labels))),
    "micro_count": int(len(set(micro_labels))),
    "hierarchy": hierarchy,
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["image_id", "macro_archetype", "meso_archetype", "micro_archetype"])
    for img, ma, me, mi in zip(image_ids, macro_labels, meso_labels, micro_labels):
        w.writerow([img, int(ma), int(me), int(mi)])

with open(MD_OUT, "w") as f:
    f.write("# Hierarchical archetype report v1.0\n\n")
    f.write(f"Signs analyzed: {len(X)}\n\n")
    f.write(f"Macro archetypes: {len(set(macro_labels))}\n")
    f.write(f"Meso archetypes: {len(set(meso_labels))}\n")
    f.write(f"Micro archetypes: {len(set(micro_labels))}\n\n")
    for h in hierarchy:
        f.write(f"## Macro archetype {h['macro_archetype']}\n")
        f.write(f"Signs: {h['sign_count']}\n\n")
        for me in h["meso_archetypes"]:
            f.write(f"### Meso {me['meso_archetype']} ({me['sign_count']} signs)\n")
            for mi in me["micro_archetypes"]:
                f.write(f"- Micro {mi['micro_archetype']}: {mi['sign_count']} signs\n")
            f.write("\n")

print("M10.1J Hierarchical Archetype Extraction")
print("=======================================")
print(f"Signs analyzed   : {len(X)}")
print(f"Macro archetypes : {len(set(macro_labels))}")
print(f"Meso archetypes  : {len(set(meso_labels))}")
print(f"Micro archetypes : {len(set(micro_labels))}")
print()
print(f"JSON report      : {JSON_OUT}")
print(f"CSV assignments  : {CSV_OUT}")
print(f"Markdown report  : {MD_OUT}")
