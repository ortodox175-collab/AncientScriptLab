from pathlib import Path
import json
import csv
import math
import random

GRAPH_PATH = Path("datasets/egyptian/primitive_graphs/primitive_graphs.json")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "graph_signature_clusters.json"
CSV_OUT = OUT_DIR / "graph_signature_cluster_assignments.csv"
MD_OUT = OUT_DIR / "graph_signature_clusters_v1.md"

data = json.loads(GRAPH_PATH.read_text())
graphs = data["graphs"]

vectors = []
image_ids = []

for g in graphs:
    s = g["graph_signature"]
    vectors.append([
        float(s["node_count"]),
        float(s["edge_count"]),
        float(s["endpoint_count"]),
        float(s["junction_count"]),
        float(s["average_degree"]),
    ])
    image_ids.append(g["image_id"])

cols = list(zip(*vectors))
means = [sum(c)/len(c) for c in cols]
stds = []
for i, c in enumerate(cols):
    var = sum((x-means[i])**2 for x in c)/len(c)
    stds.append(math.sqrt(var) if var > 1e-9 else 1.0)

X = []
for v in vectors:
    X.append([(v[i]-means[i])/stds[i] for i in range(len(v))])

K = 8
random.seed(42)
centroids = [X[i][:] for i in random.sample(range(len(X)), K)]

def dist(a, b):
    return sum((a[i]-b[i])**2 for i in range(len(a)))

for _ in range(25):
    clusters = [[] for _ in range(K)]
    assign = []
    for idx, x in enumerate(X):
        k = min(range(K), key=lambda j: dist(x, centroids[j]))
        clusters[k].append(idx)
        assign.append(k)

    new_centroids = []
    for c in clusters:
        if not c:
            new_centroids.append(X[random.randrange(len(X))][:])
            continue
        m = []
        for d in range(len(X[0])):
            m.append(sum(X[i][d] for i in c)/len(c))
        new_centroids.append(m)
    centroids = new_centroids

cluster_info = []

for k in range(K):
    idxs = [i for i, a in enumerate(assign) if a == k]
    if idxs:
        centroid = [sum(vectors[i][d] for i in idxs)/len(idxs) for d in range(len(vectors[0]))]
    else:
        centroid = [0]*len(vectors[0])
    cluster_info.append({
        "cluster_id": k,
        "size": len(idxs),
        "centroid": {
            "node_count": round(centroid[0], 3),
            "edge_count": round(centroid[1], 3),
            "endpoint_count": round(centroid[2], 3),
            "junction_count": round(centroid[3], 3),
            "average_degree": round(centroid[4], 3),
        },
        "sample_signs": [image_ids[i] for i in idxs[:10]],
    })

JSON_OUT.write_text(json.dumps({
    "module": "M10.1G Graph Signature Clustering",
    "cluster_count": K,
    "clusters": cluster_info,
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["image_id", "cluster_id"])
    for img, a in zip(image_ids, assign):
        w.writerow([img, a])

with open(MD_OUT, "w") as f:
    f.write("# Graph signature clusters v1.0\\n\\n")
    f.write(f"Graphs analyzed: {len(graphs)}\\n\\n")
    f.write(f"Clusters: {K}\\n\\n")
    for c in sorted(cluster_info, key=lambda x: x["size"], reverse=True):
        f.write(f"## Cluster {c['cluster_id']}\\n")
        f.write(f"Size: {c['size']}\\n")
        f.write(f"Centroid: {c['centroid']}\\n")
        f.write(f"Sample signs: {', '.join(c['sample_signs'])}\\n\\n")

print("M10.1G Graph Signature Clustering")
print("=================================")
print(f"Graphs analyzed : {len(graphs)}")
print(f"Clusters        : {K}")
print()
print("Cluster sizes:")
for c in sorted(cluster_info, key=lambda x: x["size"], reverse=True):
    print(f"Cluster {c['cluster_id']}: {c['size']} signs")
print()
print(f"JSON report     : {JSON_OUT}")
print(f"CSV assignments : {CSV_OUT}")
print(f"Markdown report : {MD_OUT}")
