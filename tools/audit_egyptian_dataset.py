from pathlib import Path
import json
import hashlib
from collections import Counter
from PIL import Image

IMG_DIR = Path("datasets/egyptian/images")
OUT_DIR = Path("reports/audit/egyptian")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT = OUT_DIR / "dataset_audit.json"
MARKDOWN = OUT_DIR / "DATASET_AUDIT.md"

files = sorted(IMG_DIR.glob("*.png"))

sizes = Counter()
prefixes = Counter()
duplicates = {}
hashes = {}
empty_images = []
corrupted_images = []

first_files = [f.name for f in files[:10]]
last_files = [f.name for f in files[-10:]]

for f in files:
    stem = f.stem
    prefix = ""
    for ch in stem:
        if ch.isalpha():
            prefix += ch
        else:
            break
    prefixes[prefix or "UNKNOWN"] += 1

    try:
        img = Image.open(f)
        img.load()
        sizes[f"{img.width}x{img.height}"] += 1

        if img.getbbox() is None:
            empty_images.append(f.name)

        h = hashlib.sha256(f.read_bytes()).hexdigest()
        if h in hashes:
            duplicates.setdefault(hashes[h], []).append(f.name)
        else:
            hashes[h] = f.name

    except Exception:
        corrupted_images.append(f.name)

metadata_files = []
for ext in ("*.json", "*.csv", "*.txt", "*.xml"):
    metadata_files.extend([str(p) for p in IMG_DIR.parent.glob(ext)])

report = {
    "dataset": "Egyptian",
    "image_directory": str(IMG_DIR),
    "total_images": len(files),
    "file_format": "PNG",
    "size_distribution": dict(sizes),
    "prefix_distribution": dict(prefixes),
    "first_files": first_files,
    "last_files": last_files,
    "metadata_files": metadata_files,
    "duplicate_groups": duplicates,
    "duplicate_image_count": sum(len(v) for v in duplicates.values()),
    "empty_images": empty_images,
    "corrupted_images": corrupted_images,
    "preliminary_gardiner_assessment": (
        "Prefix structure does not yet demonstrate verified Gardiner mapping."
    ),
    "audit_status": "COMPLETED",
}

REPORT.write_text(json.dumps(report, indent=2))

with open(MARKDOWN, "w") as f:
    f.write("# Egyptian dataset audit\\n\\n")
    f.write("## Summary\\n\\n")
    f.write(f"- Total images: {len(files)}\\n")
    f.write(f"- File format: PNG\\n")
    f.write(f"- Duplicate images: {report['duplicate_image_count']}\\n")
    f.write(f"- Empty images: {len(empty_images)}\\n")
    f.write(f"- Corrupted images: {len(corrupted_images)}\\n\\n")

    f.write("## Prefix distribution\\n\\n")
    for k, v in sorted(prefixes.items()):
        f.write(f"- {k}: {v}\\n")

    f.write("\\n## Image size distribution\\n\\n")
    for k, v in sorted(sizes.items()):
        f.write(f"- {k}: {v}\\n")

    f.write("\\n## Metadata files\\n\\n")
    if metadata_files:
        for m in metadata_files:
            f.write(f"- {m}\\n")
    else:
        f.write("- none detected\\n")

print("M9.0B Egyptian Dataset Audit")
print("============================")
print(f"Total images        : {len(files)}")
print(f"Unique size formats : {len(sizes)}")
print(f"Prefix groups       : {len(prefixes)}")
print(f"Duplicate images    : {report['duplicate_image_count']}")
print(f"Empty images        : {len(empty_images)}")
print(f"Corrupted images    : {len(corrupted_images)}")
print()
print(f"JSON report         : {REPORT}")
print(f"Markdown report     : {MARKDOWN}")
