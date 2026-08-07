from pathlib import Path
import csv
import json

SRC = Path('datasets/egyptian/sources/Unikemet.txt')
OUT = Path('datasets/egyptian/registry')
OUT.mkdir(parents=True, exist_ok=True)

CSV_OUT = OUT / 'canonical_gardiner_registry_v32.csv'
JSON_OUT = OUT / 'canonical_gardiner_registry_v32.json'
REPORT = Path('reports/metrology/unikemet_registry_v32_report.md')

records = {}

def normalize(code):
    if not code:
        return None
    code = code.strip()
    if code.startswith('AA'):
        code = 'Aa' + code[2:]
    return code

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

        rec = records.setdefault(cp_hex, {
            'unicode_cp': cp_hex,
            'unicode': cp,
            'gardiner_code': None,
            'gardiner_source': None,
            'unikemet_code': None,
            'jsesh_code': None,
            'category': None,
            'description': None,
            'function': None,
            'core': None,
        })

        if tag == 'kEH_HG':
            rec['gardiner_code'] = normalize(value)
            rec['gardiner_source'] = 'kEH_HG'

        elif tag == 'kEH_JSesh':
            rec['jsesh_code'] = normalize(value)
            if rec['gardiner_code'] is None:
                rec['gardiner_code'] = rec['jsesh_code']
                rec['gardiner_source'] = 'kEH_JSesh'

        elif tag == 'kEH_UniK':
            rec['unikemet_code'] = value

        elif tag == 'kEH_Cat':
            rec['category'] = value

        elif tag == 'kEH_Desc':
            rec['description'] = value

        elif tag == 'kEH_Func':
            rec['function'] = value

        elif tag == 'kEH_Core':
            rec['core'] = value

registry = [r for r in records.values() if r['gardiner_code'] is not None]
registry.sort(key=lambda r: int(r['unicode_cp'], 16))

with CSV_OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'gardiner_code',
        'gardiner_source',
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

hg = sum(1 for r in registry if r['gardiner_source'] == 'kEH_HG')
js = sum(1 for r in registry if r['gardiner_source'] == 'kEH_JSesh')

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(
    'M10.3G Unicode Unikemet Registry v3.2\n'
    '====================================\n'
    f'Total registry records         : {len(registry)}\n'
    f'Primary kEH_HG mappings        : {hg}\n'
    f'Fallback kEH_JSesh mappings    : {js}\n'
    f'Total Gardiner mappings        : {hg + js}\n',
    encoding='utf-8'
)

print('M10.3G Unicode Unikemet Registry v3.2')
print('====================================')
print('Registry records        :', len(registry))
print('Primary kEH_HG mappings :', hg)
print('Fallback kEH_JSesh      :', js)
print('Total Gardiner mappings :', hg + js)
print('CSV                     :', CSV_OUT)
print('JSON                    :', JSON_OUT)
print('Report                  :', REPORT)
