from pathlib import Path
import json
import csv
import re

IMG_DIR = Path('datasets/egyptian/images')
OUT_DIR = Path('datasets/egyptian/registry')
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / 'gardiner_sign_registry.json'
CSV_OUT = OUT_DIR / 'gardiner_sign_registry.csv'
MD_OUT = Path('reports/metrology/gardiner_registry_report.md')

CODE_RE = re.compile(r'^(Aa|[A-Z])[0-9]+[A-Z]?$')

registry = []
recognized = 0
unrecognized = 0

for p in sorted(IMG_DIR.iterdir()):
    if not p.is_file():
        continue

    stem = p.stem
    m = CODE_RE.match(stem)

    if m:
        code = m.group(0)
        recognized += 1
    else:
        code = None
        unrecognized += 1

    registry.append({
        'image_id': stem,
        'gardiner_code': code,
        'filename': p.name
    })

JSON_OUT.write_text(json.dumps({
    'module': 'M10.3A Gardiner Sign Registry',
    'registry': registry
}, indent=2))

with open(CSV_OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['image_id','gardiner_code','filename'])
    w.writeheader()
    w.writerows(registry)

with open(MD_OUT, 'w', encoding='utf-8') as f:
    f.write('# Gardiner sign registry report\\n\\n')
    f.write(f'Total images: {len(registry)}\\n')
    f.write(f'Recognized Gardiner codes: {recognized}\\n')
    f.write(f'Unrecognized filenames: {unrecognized}\\n')

print('M10.3A Gardiner Sign Registry')
print('=============================')
print(f'Total images          : {len(registry)}')
print(f'Recognized Gardiner   : {recognized}')
print(f'Unrecognized filenames: {unrecognized}')
print()
print(f'JSON registry         : {JSON_OUT}')
print(f'CSV registry          : {CSV_OUT}')
print(f'Report                : {MD_OUT}')
