from pathlib import Path
from core.registry.sign_registry import SignRegistry, SignRecord

IMG_DIR = Path("datasets/egyptian/images")
OUT = Path("datasets/egyptian/registry/sign_registry.json")

registry = SignRegistry()

for img in sorted(IMG_DIR.glob("*.png")):
    sign_id = img.stem

    if sign_id and sign_id[0].isalpha():
        category = sign_id[0].upper()
    else:
        category = "UNKNOWN"

    registry.add(SignRecord(
        sign_id=sign_id,
        category=category,
        image_path=str(img),
        source="Egyptian sign catalog"
    ))

registry.to_json(OUT)

cats = {}
for r in registry.records.values():
    cats[r.category] = cats.get(r.category, 0) + 1

print("M9.0A Egyptian Sign Registry")
print("============================")
print(f"Signs registered : {len(registry.records)}")
print(f"Registry         : {OUT}")
print()
print("Categories:")
for k in sorted(cats):
    print(f"  {k}: {cats[k]}")
