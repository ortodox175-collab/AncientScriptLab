from pathlib import Path
import json
import csv
import cv2
import numpy as np

IMG_DIR = Path("datasets/egyptian/images")
OUT_DIR = Path("datasets/egyptian/primitive_graphs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "primitive_graphs.json"
CSV_OUT = OUT_DIR / "primitive_graph_summary.csv"
REPORT_OUT = Path("reports/metrology/primitive_graph_report.json")

def skeletonize(binary):
    if hasattr(cv2, "ximgproc") and hasattr(cv2.ximgproc, "thinning"):
        return cv2.ximgproc.thinning(binary)
    skel = np.zeros_like(binary)
    img = binary.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    while True:
        eroded = cv2.erode(img, kernel)
        temp = cv2.dilate(eroded, kernel)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded
        if cv2.countNonZero(img) == 0:
            break
    return skel

def neighbors(s, x, y):
    h, w = s.shape
    pts = []
    for yy in range(max(0, y-1), min(h, y+2)):
        for xx in range(max(0, x-1), min(w, x+2)):
            if xx == x and yy == y:
                continue
            if s[yy, xx]:
                pts.append((xx, yy))
    return pts

def build_graph(skel):
    s = (skel > 0).astype(np.uint8)
    h, w = s.shape

    nodes = []
    node_map = {}

    for y in range(h):
        for x in range(w):
            if not s[y, x]:
                continue
            deg = len(neighbors(s, x, y))
            if deg == 1:
                t = "endpoint"
            elif deg >= 3:
                t = "junction"
            else:
                continue
            node_id = f"N{len(nodes)}"
            nodes.append({
                "id": node_id,
                "type": t,
                "x": x,
                "y": y
            })
            node_map[(x, y)] = node_id

    visited = set()
    edge_set = set()
    edges = []

    for (sx, sy), sid in node_map.items():
        for nx, ny in neighbors(s, sx, sy):
            if ((sx, sy), (nx, ny)) in visited:
                continue

            prev = (sx, sy)
            cur = (nx, ny)
            length = 1

            while True:
                visited.add((prev, cur))
                visited.add((cur, prev))

                if cur in node_map:
                    tid = node_map[cur]
                    if tid != sid:
                        key = tuple(sorted((sid, tid)))
                        if key not in edge_set:
                            edge_set.add(key)
                            edges.append({
                                "from": sid,
                                "to": tid,
                                "length": length
                            })
                    break

                nbrs = [p for p in neighbors(s, cur[0], cur[1]) if p != prev]

                if len(nbrs) == 0:
                    break
                if len(nbrs) > 1:
                    break

                prev = cur
                cur = nbrs[0]
                length += 1

    node_count = len(nodes)
    edge_count = len(edges)
    endpoint_count = sum(1 for n in nodes if n["type"] == "endpoint")
    junction_count = sum(1 for n in nodes if n["type"] == "junction")
    avg_degree = (2 * edge_count / node_count) if node_count else 0.0

    signature = {
        "node_count": node_count,
        "edge_count": edge_count,
        "endpoint_count": endpoint_count,
        "junction_count": junction_count,
        "average_degree": round(avg_degree, 6)
    }

    return nodes, edges, signature

graphs = []
csv_rows = []

for img_path in sorted(IMG_DIR.glob("*.png")):
    gray = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    skel = skeletonize(binary)
    nodes, edges, sig = build_graph(skel)

    graphs.append({
        "image_id": img_path.stem,
        "nodes": nodes,
        "edges": edges,
        "graph_signature": sig
    })

    row = {"image_id": img_path.stem}
    row.update(sig)
    csv_rows.append(row)

JSON_OUT.write_text(json.dumps({
    "primitive_graph_version": "2.0",
    "graphs": graphs
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
    writer.writeheader()
    writer.writerows(csv_rows)

REPORT_OUT.write_text(json.dumps({
    "module": "M10.1E Primitive Graph Extraction",
    "primitive_graph_version": "2.0",
    "graphs_processed": len(graphs),
    "status": "PASS"
}, indent=2))

print("M10.1E Primitive Graph Extraction v2.0")
print("======================================")
print(f"Signs processed : {len(graphs)}")
print(f"JSON graphs     : {JSON_OUT}")
print(f"CSV summary     : {CSV_OUT}")
print(f"Metrology report: {REPORT_OUT}")
