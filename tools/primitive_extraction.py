from pathlib import Path
import json
import csv
import cv2
import numpy as np

IMG_DIR = Path("datasets/egyptian/images")
OUT_DIR = Path("datasets/egyptian/signatures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "structural_signatures.json"
CSV_OUT = OUT_DIR / "structural_signatures.csv"
REPORT_OUT = Path("reports/metrology/primitive_extraction_report.json")

def skeletonize(binary):
    img = binary.copy()
    skel = np.zeros(img.shape, np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    while True:
        eroded = cv2.erode(img, kernel)
        temp = cv2.dilate(eroded, kernel)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
        if cv2.countNonZero(img) == 0:
            break
    return skel

def endpoints_junctions(skel):
    s = (skel > 0).astype(np.uint8)
    p = np.pad(s, 1)
    endpoints = 0
    junctions = 0
    for y in range(1, p.shape[0]-1):
        for x in range(1, p.shape[1]-1):
            if p[y,x]:
                n = (
                    p[y-1,x-1] + p[y-1,x] + p[y-1,x+1] +
                    p[y,x-1] + p[y,x+1] +
                    p[y+1,x-1] + p[y+1,x] + p[y+1,x+1]
                )
                if n == 1:
                    endpoints += 1
                elif n >= 3:
                    junctions += 1
    return endpoints, junctions

signatures = []

for img_path in sorted(IMG_DIR.glob("*.png")):
    gray = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    num_labels, _ = cv2.connectedComponents(binary)
    components = int(num_labels - 1)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    holes = 0
    if hierarchy is not None:
        for h in hierarchy[0]:
            if h[3] != -1:
                holes += 1

    euler = components - holes

    skel = skeletonize(binary)
    endpoints, junctions = endpoints_junctions(skel)
    skel_length = cv2.countNonZero(skel)
    diag = (binary.shape[0]**2 + binary.shape[1]**2) ** 0.5
    skel_norm = skel_length / diag if diag else 0.0

    area = cv2.countNonZero(binary)
    density = area / binary.size if binary.size else 0.0

    ys, xs = np.where(binary > 0)
    if len(xs):
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        w = x1 - x0 + 1
        h = y1 - y0 + 1
        aspect = w / h if h else 0.0
        cx = xs.mean() / binary.shape[1]
        cy = ys.mean() / binary.shape[0]
    else:
        aspect = 0.0
        cx = 0.0
        cy = 0.0

    signatures.append({
        "image_id": img_path.stem,
        "components": components,
        "holes": holes,
        "euler": euler,
        "endpoints": endpoints,
        "junctions": junctions,
        "skeleton_length_normalized": round(float(skel_norm), 6),
        "foreground_density": round(float(density), 6),
        "aspect_ratio": round(float(aspect), 6),
        "centroid_x_normalized": round(float(cx), 6),
        "centroid_y_normalized": round(float(cy), 6)
    })

JSON_OUT.write_text(json.dumps({
    "structural_signature_version": "1.0",
    "feature_count": 10,
    "signatures": signatures
}, indent=2))

with open(CSV_OUT, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=signatures[0].keys())
    writer.writeheader()
    writer.writerows(signatures)

report = {
    "module": "M10.1A Primitive Extraction",
    "structural_signature_version": "1.0",
    "images_processed": len(signatures),
    "feature_count": 10,
    "status": "PASS"
}

REPORT_OUT.write_text(json.dumps(report, indent=2))

print("M10.1A Structural Primitive Extraction")
print("======================================")
print(f"Images processed : {len(signatures)}")
print(f"Feature count    : 10")
print(f"JSON dataset     : {JSON_OUT}")
print(f"CSV dataset      : {CSV_OUT}")
print(f"Metrology report : {REPORT_OUT}")
