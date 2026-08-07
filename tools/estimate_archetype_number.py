from pathlib import Path
import json
import csv
import random
import math

GRAPH_PATH = Path("datasets/egyptian/primitive_graphs/primitive_graphs.json")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "archetype_number_estimation.json"
CSV_OUT = OUT_DIR / "archetype_number_metrics.csv"
MD_OUT = OUT_DIR / "archetype_number_estimation_v1.md"

data = json.loads(GRAPH_PATH.read_text())
graphs = data["graphs"]

vectors = []
for g in graphs:
    s = g["graph_signature"]
    vectors.append([
        float(s["node_count"]),
        float(s["edge_count"]),
        float(s["endpoint_count"]),
        float(s["junction_count"]),
        float(s["average_degree"]),
    ])

cols = list(zip(*vectors))
means = [sum(c)/len(c) for c in cols]
stds = []
for i, c in enumerate(cols):
    var = sum((x-means[i])**2 for x in c)/len(c)
    stds.append(math.sqrt(var) if var > 1e-9 else 1.0)

X = []
for v in vectors:
    X.append([(v[i]-means[i])/stds[i] for i in range(len(v))])

def dist2(a, b):
    return sum((a[i]-b[i])**2 for i in range(len(a)))

def kmeans(X, k, iterations=30):
    random.seed(42 + k)
    centroids = [X[i][:] for i in random.sample(range(len(X)), k)]
    assign = [0]*len(X)
    for _ in range(iterations):
        for i, x in enumerate(X):
            assign[i] = min(range(k), key=lambda j: dist2(x, centroids[j]))
        new = [[0.0]*len(X[0]) for _ in range(k)]
        counts = [0]*k
        for idx, a in enumerate(assign):
            counts[a] += 1
            for d in range(len(X[0])):
                new[a][d] += X[idx][d]
        for j in range(k):
            if counts[j] == 0:
                new[j] = X[random.randrange(len(X))][:]
            else:
                new[j] = [v/counts[j] for v in new[j]]
        centroids = new
    return assign, centroids

def silhouette(X, assign, centroids):
    n = len(X)
    k = len(centroids)
    clusters = [[] for _ in range(k)]
    for i, a in enumerate(assign):
        clusters[a].append(i)
    scores = []
    for i, x in enumerate(X):
        a = assign[i]
        own = clusters[a]
        if len(own) <= 1:
            scores.append(0.0)
            continue
        ai = sum(math.sqrt(dist2(x, X[j])) for j in own if j != i)/(len(own)-1)
        bi = float("inf")
        for c in range(k):
            if c == a or not clusters[c]:
                continue
            d = sum(math.sqrt(dist2(x, X[j])) for j in clusters[c])/len(clusters[c])
            bi = min(bi, d)
        scores.append((bi-ai)/max(ai, bi))
    return sum(scores)/len(scores)

def davies_bouldin(X, assign, centroids):
    k = len(centroids)
    clusters = [[] for _ in range(k)]
    for i, a in enumerate(assign):
        clusters[a].append(i)
    scat = []
    for c in range(k):
        if not clusters[c]:
            scat.append(0.0)
        else:
            scat.append(sum(math.sqrt(dist2(X[i], centroids[c])) for i in clusters[c])/len(clusters[c]))
    vals = []
    for i in range(k):
        worst = 0.0
        for j in range(k):
            if i == j:
                continue
            d = math.sqrt(dist2(centroids[i], centroids[j]))
            if d == 0:
                continue
            worst = max(worst, (scat[i]+scat[j])/d)
        vals.append(worst)
    return sum(vals)/len(vals)

def calinski_harabasz(X, assign, centroids):
    n = len(X)
    k = len(centroids)
    overall = [sum(x[d] for x in X)/n for d in range(len(X[0]))]
    clusters = [[] for _ in range(k)]
    for i, a in enumerate(assign):
        clusters[a].append(i)
    between = 0.0
    within = 0.0
    for c in range(k):
        if not clusters[c]:
            continue
        nc = len(clusters[c])
        between += nc * dist2(centroids[c], overall)
        for i in clusters[c]:
            within += dist2(X[i], centroids[c])
    if within == 0 or k == 1:
        return 0.0
    return (between/(k-1))/(within/(n-k))

rows = []
best = None

for k in range(2, 31):
    assign, centroids = kmeans(X, k)
    sil = silhouette(X, assign, centroids)
    db = davies_bouldin(X, assign, centroids)
    ch = calinski_harabasz(X, assign, centroids)
    row = {
        "k": k,
        "silhouette": round(sil, 6),
        "davies_bouldin": round(db, 6),
        "calinski_harabasz": round(ch, 6),
    }
    rows.append(row)
    if best is None or sil > best["silhouette"]:
        best = row

JSON_OUT.write_text(json.dumps({
    "module": "M10.1H Automatic Archetype Number Estimation",
    "k_range": [2,30],
    "best_k": best["k"],
    "best_metrics": best,
    "results": rows,
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

with open(MD_OUT, "w") as f:
    f.write("# Archetype number estimation v1.0\n\n")
    f.write(f"Best K: {best['k']}\n\n")
    f.write(f"Silhouette: {best['silhouette']}\n")
    f.write(f"Davies-Bouldin: {best['davies_bouldin']}\n")
    f.write(f"Calinski-Harabasz: {best['calinski_harabasz']}\n")

print("M10.1H Automatic Archetype Number Estimation")
print("============================================")
print(f"Graphs analyzed : {len(X)}")
print(f"K range         : 2-30")
print()
print(f"Best K          : {best['k']}")
print(f"Silhouette      : {best['silhouette']}")
print(f"Davies-Bouldin  : {best['davies_bouldin']}")
print(f"Calinski-Harabasz: {best['calinski_harabasz']}")
print()
print(f"JSON report     : {JSON_OUT}")
print(f"CSV metrics     : {CSV_OUT}")
print(f"Markdown report : {MD_OUT}")
