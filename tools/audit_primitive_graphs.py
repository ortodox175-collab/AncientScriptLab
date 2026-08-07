from pathlib import Path
import json
import csv
import math
from collections import Counter
from statistics import mean, median, pstdev

GRAPH_PATH = Path("datasets/egyptian/primitive_graphs/primitive_graphs.json")
OUT_DIR = Path("reports/statistics/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "primitive_graph_audit.json"
CSV_OUT = OUT_DIR / "primitive_graph_signature_ranking.csv"
MD_OUT = OUT_DIR / "primitive_graph_audit_v1.md"

data = json.loads(GRAPH_PATH.read_text())
graphs = data["graphs"]

node_counts = []
edge_counts = []
endpoint_counts = []
junction_counts = []
avg_degrees = []
signatures = []

for g in graphs:
    sig = g["graph_signature"]
    node_counts.append(sig["node_count"])
    edge_counts.append(sig["edge_count"])
    endpoint_counts.append(sig["endpoint_count"])
    junction_counts.append(sig["junction_count"])
    avg_degrees.append(sig["average_degree"])

    signatures.append(
        (
            sig["node_count"],
            sig["edge_count"],
            sig["endpoint_count"],
            sig["junction_count"],
            round(sig["average_degree"], 3),
        )
    )

def entropy(values):
    cnt = Counter(values)
    e = 0.0
    for c in cnt.values():
        p = c / len(values)
        e -= p * math.log2(p)
    return e

def summary(values):
    return {
        "min": min(values),
        "max": max(values),
        "mean": round(mean(values), 6),
        "median": round(median(values), 6),
        "std": round(pstdev(values), 6),
        "entropy": round(entropy(values), 6),
        "unique_values": len(set(values)),
    }

signature_counter = Counter(signatures)
top_signatures = signature_counter.most_common(20)

report = {
    "graphs_analyzed": len(graphs),
    "node_count": summary(node_counts),
    "edge_count": summary(edge_counts),
    "endpoint_count": summary(endpoint_counts),
    "junction_count": summary(junction_counts),
    "average_degree": summary(avg_degrees),
    "top_signatures": [
        {
            "signature": {
                "node_count": s[0],
                "edge_count": s[1],
                "endpoint_count": s[2],
                "junction_count": s[3],
                "average_degree": s[4],
            },
            "count": c,
            "frequency": round(c / len(graphs), 6),
        }
        for s, c in top_signatures
    ],
}

JSON_OUT.write_text(json.dumps(report, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(
        [
            "rank",
            "node_count",
            "edge_count",
            "endpoint_count",
            "junction_count",
            "average_degree",
            "count",
            "frequency",
        ]
    )
    for i, (s, c) in enumerate(top_signatures, 1):
        writer.writerow(
            [
                i,
                s[0],
                s[1],
                s[2],
                s[3],
                s[4],
                c,
                round(c / len(graphs), 6),
            ]
        )

with open(MD_OUT, "w") as f:
    f.write("# Primitive graph audit v1.0\\n\\n")
    f.write(f"Graphs analyzed: {len(graphs)}\\n\\n")
    f.write("## Summary\\n\\n")
    for key in [
        "node_count",
        "edge_count",
        "endpoint_count",
        "junction_count",
        "average_degree",
    ]:
        s = report[key]
        f.write(
            f"### {key}\\n"
            f"- mean: {s['mean']}\\n"
            f"- median: {s['median']}\\n"
            f"- entropy: {s['entropy']}\\n"
            f"- unique values: {s['unique_values']}\\n\\n"
        )

print("M10.1F Primitive Graph Audit")
print("============================")
print(f"Graphs analyzed : {len(graphs)}")
print()
print("Entropy summary:")
print(f"Node count      : {report['node_count']['entropy']}")
print(f"Edge count      : {report['edge_count']['entropy']}")
print(f"Endpoint count  : {report['endpoint_count']['entropy']}")
print(f"Junction count  : {report['junction_count']['entropy']}")
print(f"Average degree  : {report['average_degree']['entropy']}")
print()
print(f"Top signatures  : {len(top_signatures)} reported")
print(f"JSON report     : {JSON_OUT}")
print(f"CSV ranking     : {CSV_OUT}")
print(f"Markdown report : {MD_OUT}")
