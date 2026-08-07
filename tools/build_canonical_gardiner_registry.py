from pathlib import Path
import json
import csv

MAP_PATH = Path('datasets/egyptian/registry/franken_gardiner_mapping.csv')
OUT_DIR = Path('datasets/egyptian/registry')
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / 'canonical_gardiner_registry.json'
CSV_OUT = OUT_DIR / 'canonical_gardiner_registry.csv'
MD_OUT = Path('reports/metrology/canonical_gardiner_registry_report.md')

if not MAP_PATH.exists():
    print('Franken mapping not found:')
    print(MAP_PATH)
    raise SystemExit(1)

registry = {}

with open(MAP_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row['gardiner_code'].strip()
        if not code:
            continue
        if code not in registry:
            registry[code] = {
                'gardiner_code': code,
                'image_path': row['franken_image'],
                'feature_vector': None,
                'macro_archetype': None,
                'meso_archetype': None,
                'micro_archetype': None,
                'source': 'Franken/GlyphReader'
            }

records = sorted(registry.values(), key=lambda x: x['gardiner_code'])

JSON_OUT.write_text(json.dumps({
    'module': 'M10.3D Canonical Egyptian Sign Registry',
    'registry': records
}, indent=2))

with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=[
        'gardiner_code',
        'image_path',
        'feature_vector',
        'macro_archetype',
        'meso_archetype',
        'micro_archetype',
        'source'
    ])
    w.writeheader()
    w.writerows(records)

with open(MD_OUT, 'w', encoding='utf-8') as f:
    f.write('# Canonical Gardiner Registry\\n\\n')
    f.write(f'Total canonical signs: {len(records)}\\n')
    f.write('Primary identifier: gardiner_code\\n')
    f.write('Image is treated as an attribute, not identity.\\n')

print('M10.3D Canonical Egyptian Sign Registry')
print('=======================================')
print(f'Canonical signs : {len(records)}')
print()
print(f'JSON registry   : {JSON_OUT}')
print(f'CSV registry    : {CSV_OUT}')
print(f'Report          : {MD_OUT}')
