from pathlib import Path
import json
import csv
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, adjusted_rand_score

GRAPH_PATH = Path("datasets/egyptian/primitive_graphs/primitive_graphs.json")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "archetype_stability_validation_v2.json"
CSV_OUT = OUT_DIR / "archetype_stability_metrics_v2.csv"
MD_OUT = OUT_DIR / "archetype_stability_report_v2.md"

data = json.loads(GRAPH_PATH.read_text())
graphs = data["graphs"]

X = []
for g in graphs:
    s = g["graph_signature"]
    X.append([
        float(s["node_count"]),
        float(s["edge_count"]),
        float(s["endpoint_count"]),
        float(s["junction_count"]),
        float(s["average_degree"]),
    ])

X = np.array(X)
X = StandardScaler().fit_transform(X)

rows = []

for k in range(2, 31):
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    km_labels = km.fit_predict(X)
    km_sil = silhouette_score(X, km_labels)

    hc = AgglomerativeClustering(n_clusters=k)
    hc_labels = hc.fit_predict(X)
    hc_sil = silhouette_score(X, hc_labels)

    gm = GaussianMixture(n_components=k, random_state=42)
    gm_labels = gm.fit_predict(X)
    gm_sil = silhouette_score(X, gm_labels)

    ari_km_hc = adjusted_rand_score(km_labels, hc_labels)
    ari_km_gm = adjusted_rand_score(km_labels, gm_labels)
    ari_hc_gm = adjusted_rand_score(hc_labels, gm_labels)

    rows.append({
        "k": k,
        "km_silhouette": round(km_sil, 6),
        "hc_silhouette": round(hc_sil, 6),
        "gm_silhouette": round(gm_sil, 6),
        "ari_km_hc": round(ari_km_hc, 6),
        "ari_km_gm": round(ari_km_gm, 6),
        "ari_hc_gm": round(ari_hc_gm, 6),
    })

best = max(rows, key=lambda r: (r["km_silhouette"] + r["hc_silhouette"] + r["gm_silhouette"]) / 3)

JSON_OUT.write_text(json.dumps({
    "module": "M10.1I Multilayer Archetype Stability Validation",
    "k_range": [2, 30],
    "best_k": best["k"],
    "best_metrics": best,
    "results": rows,
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

with open(MD_OUT, "w") as f:
    f.write("# Archetype stability report v2.0\n\n")
    f.write(f"Best K: {best['k']}\n\n")
    f.write("Average silhouette:\n")
    avg = (best["km_silhouette"] + best["hc_silhouette"] + best["gm_silhouette"]) / 3
    f.write(f"- {avg:.6f}\n\n")
    f.write("Algorithm agreement (ARI):\n")
    f.write(f"- KMeans vs Hierarchical: {best['ari_km_hc']}\n")
    f.write(f"- KMeans vs GMM: {best['ari_km_gm']}\n")
    f.write(f"- Hierarchical vs GMM: {best['ari_hc_gm']}\n")

print("M10.1I Multilayer Archetype Stability Validation v2.0")
print("=====================================================")
print(f"Graphs analyzed : {len(X)}")
print(f"K range         : 2-30")
print()
print(f"Best K          : {best['k']}")
print(f"KMeans silhouette      : {best['km_silhouette']}")
print(f"Hierarchical silhouette: {best['hc_silhouette']}")
print(f"GMM silhouette         : {best['gm_silhouette']}")
print()
print(f"ARI KMeans-Hierarchical: {best['ari_km_hc']}")
print(f"ARI KMeans-GMM         : {best['ari_km_gm']}")
print(f"ARI Hierarchical-GMM   : {best['ari_hc_gm']}")
print()
print(f"JSON report     : {JSON_OUT}")
print(f"CSV metrics     : {CSV_OUT}")
print(f"Markdown report : {MD_OUT}")
