from pathlib import Path
import json
import csv
import re

IMG_DIR = Path('datasets/egyptian/images')
REG_DIR = Path('datasets/egyptian/registry')
REG_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = REG_DIR / 'franken_gardiner_mapping.csv'
JSON_OUT = REG_DIR / 'gardiner_sign_registry_v2.json'
MD_OUT = Path('reports/metrology/gardiner_registry_v2_report.md')

CODE_RE = re.compile(r'^(Aa|[A-Z])[0-9]+[A-Z]?$')

if not CSV_PATH.exists():
    rows = []
    for p in sorted(IMG_DIR.iterdir()):
        if p.is_file():
            rows.append({
                'image_id': p.stem,
                'gardiner_code': '',
                'filename': p.name
            })

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['image_id','gardiner_code','filename'])
        w.writeheader()
        w.writerows(rows)

    print('M10.3B Franken Registry Integration')
    print('===================================')
    print('Template mapping created:')
    print(CSV_PATH)
    print()
    print('Next step: populate gardiner_code from Franken Dataset.')
    raise SystemExit(0)

registry = []
mapped = 0
unmapped = 0

with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        code = row['gardiner_code'].strip()
        if code and CODE_RE.match(code):
            mapped += 1
        else:
            code = None
            unmapped += 1

        registry.append({
            'image_id': row['image_id'],
            'gardiner_code': code,
            'filename': row['filename']
        })

JSON_OUT.write_text(json.dumps({
    'module': 'M10.3B Franken Registry Integration',
    'registry': registry
}, indent=2))

with open(MD_OUT, 'w', encoding='utf-8') as f:
    f.write('# Gardiner registry v2 report\\n\\n')
    f.write(f'Total entries: {len(registry)}\\n')
    f.write(f'Mapped Gardiner codes: {mapped}\\n')
    f.write(f'Unmapped entries: {unmapped}\\n')

print('M10.3B Franken Registry Integration')
print('===================================')
print(f'Total entries : {len(registry)}')
print(f'Mapped codes  : {mapped}')
print(f'Unmapped      : {unmapped}')
print()
print(f'JSON registry : {JSON_OUT}')
print(f'Report        : {MD_OUT}')
