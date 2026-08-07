from pathlib import Path
import csv
import json

SRC = Path('datasets/egyptian/sources/Unikemet.txt')
OUT = Path('datasets/egyptian/registry')
OUT.mkdir(parents=True, exist_ok=True)

CSV_OUT = OUT / 'canonical_gardiner_registry_v3.csv'
JSON_OUT = OUT / 'canonical_gardiner_registry_v3.json'
REPORT = Path('reports/metrology/unikemet_registry_report.md')

records = {}

with SRC.open('r', encoding='utf-8') as f:
    for line in f:
        if not line.strip() or line.startswith('#'):
            continue

        parts = line.rstrip('\n').split('\t')
        if len(parts) != 3:
            continue

        cp, tag, value = parts

        if not cp.startswith('U+'):
            continue

        cp_hex = cp[2:]
        cp_int = int(cp_hex, 16)

        if not (0x13000 <= cp_int <= 0x1345F):
            continue

        rec = records.setdefault(cp_hex, {
            'unicode_cp': cp_hex,
            'unicode': f'U+{cp_hex}',
            'gardiner_code': None,
            'unikemet_code': None,
            'jsesh_code': None,
            'category': None,
            'description': None,
            'function': None,
            'core': None,
        })

        if tag == 'kEH_HG':
            rec['gardiner_code'] = value
        elif tag == 'kEH_UniK':
            rec['unikemet_code'] = value
        elif tag == 'kEH_JSesh':
            rec['jsesh_code'] = value
        elif tag == 'kEH_Cat':
            rec['category'] = value
        elif tag == 'kEH_Desc':
            rec['description'] = value
        elif tag == 'kEH_Func':
            rec['function'] = value
        elif tag == 'kEH_Core':
            rec['core'] = value

registry = sorted(records.values(), key=lambda r: int(r['unicode_cp'], 16))

with CSV_OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'gardiner_code',
        'unicode_cp',
        'unicode',
        'unikemet_code',
        'jsesh_code',
        'category',
        'description',
        'function',
        'core',
    ])
    writer.writeheader()
    writer.writerows(registry)

with JSON_OUT.open('w', encoding='utf-8') as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)

gardiner = sum(1 for r in registry if r['gardiner_code'])
jsesh = sum(1 for r in registry if r['jsesh_code'])
descriptions = sum(1 for r in registry if r['description'])

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(
    'M10.3G Unicode Unikemet Registry\n'
    '================================\n'
    f'Total Unicode Egyptian records : {len(registry)}\n'
    f'Gardiner codes available       : {gardiner}\n'
    f'JSesh codes available          : {jsesh}\n'
    f'Descriptions available         : {descriptions}\n',
    encoding='utf-8'
)

print('M10.3G Unicode Unikemet Registry')
print('================================')
print('Unicode Egyptian records :', len(registry))
print('Gardiner codes          :', gardiner)
print('JSesh codes             :', jsesh)
print('Descriptions            :', descriptions)
print('CSV                     :', CSV_OUT)
print('JSON                    :', JSON_OUT)
print('Report                  :', REPORT)
