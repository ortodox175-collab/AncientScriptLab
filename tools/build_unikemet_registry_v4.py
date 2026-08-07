from pathlib import Path
import csv
import json

SRC = Path('datasets/egyptian/sources/Unikemet.txt')
OUT = Path('datasets/egyptian/registry')
OUT.mkdir(parents=True, exist_ok=True)

CSV_OUT = OUT / 'canonical_gardiner_registry_v4.csv'
JSON_OUT = OUT / 'canonical_gardiner_registry_v4.json'
REPORT = Path('reports/metrology/unikemet_registry_v4_report.md')

# Сначала собираем свойства по Unicode-кодовой точке
by_cp = {}

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

        rec = by_cp.setdefault(cp_hex, {
            'unicode_cp': cp_hex,
            'unicode': cp,
            'kEH_HG': None,
            'kEH_JSesh': None,
            'kEH_UniK': None,
            'kEH_Cat': None,
            'kEH_Desc': None,
            'kEH_Func': None,
            'kEH_Core': None,
        })

        rec[tag] = value

# Теперь строим реестр по уникальным Gardiner-кодам
registry = {}

for rec in by_cp.values():
    code = normalize(rec.get('kEH_HG'))
    source = 'kEH_HG'

    if code is None:
        code = normalize(rec.get('kEH_JSesh'))
        source = 'kEH_JSesh'

    if code is None:
        continue

    existing = registry.get(code)

    if existing is None or source == 'kEH_HG':
        registry[code] = {
            'gardiner_code': code,
            'gardiner_source': source,
            'unicode_cp': rec['unicode_cp'],
            'unicode': rec['unicode'],
            'unikemet_code': rec.get('kEH_UniK'),
            'jsesh_code': normalize(rec.get('kEH_JSesh')),
            'category': rec.get('kEH_Cat'),
            'description': rec.get('kEH_Desc'),
            'function': rec.get('kEH_Func'),
            'core': rec.get('kEH_Core'),
        }

records = sorted(
    registry.values(),
    key=lambda r: (
        r['gardiner_code'].replace('Aa', 'ZZ'),
        int(r['unicode_cp'], 16),
    ),
)

with CSV_OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
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
        ],
    )
    writer.writeheader()
    writer.writerows(records)

with JSON_OUT.open('w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

hg = sum(1 for r in records if r['gardiner_source'] == 'kEH_HG')
js = sum(1 for r in records if r['gardiner_source'] == 'kEH_JSesh')

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(
    'M10.3G Unicode Unikemet Registry v4\n'
    '==================================\n'
    f'Unique Gardiner codes        : {len(records)}\n'
    f'Primary kEH_HG mappings      : {hg}\n'
    f'Fallback kEH_JSesh mappings  : {js}\n',
    encoding='utf-8'
)

print('M10.3G Unicode Unikemet Registry v4')
print('==================================')
print('Unique Gardiner codes       :', len(records))
print('Primary kEH_HG mappings     :', hg)
print('Fallback kEH_JSesh mappings :', js)
print('CSV                         :', CSV_OUT)
print('JSON                        :', JSON_OUT)
print('Report                      :', REPORT)
