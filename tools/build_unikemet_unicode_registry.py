from pathlib import Path
import csv
import json

SRC = Path('datasets/egyptian/sources/Unikemet.txt')
OUT = Path('datasets/egyptian/registry')
OUT.mkdir(parents=True, exist_ok=True)

CSV_OUT = OUT / 'unicode_immutable_registry.csv'
JSON_OUT = OUT / 'unicode_immutable_registry.json'
REPORT = Path('reports/metrology/unicode_immutable_registry_report.md')

RANGES = [
    (0x13000, 0x1345F),  # Egyptian Hieroglyphs + Format Controls
    (0x13460, 0x143FF),  # Egyptian Hieroglyphs Extended-A
]

def is_egyptian(cp_hex):
    cp = int(cp_hex, 16)
    return any(a <= cp <= b for a, b in RANGES)

records = {}

with SRC.open('r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue

        parts = line.rstrip('\n').split('\t')
        if len(parts) != 3:
            continue

        cp, tag, value = parts

        if not cp.startswith('U+'):
            continue

        cp_hex = cp[2:]

        if not is_egyptian(cp_hex):
            continue

        rec = records.setdefault(cp_hex, {
            'unicode_cp': cp_hex,
            'unicode': cp,
        })

        rec[tag] = value

registry = sorted(
    records.values(),
    key=lambda r: int(r['unicode_cp'], 16)
)

fieldnames = set()
for r in registry:
    fieldnames.update(r.keys())

fieldnames = ['unicode_cp', 'unicode'] + sorted(
    x for x in fieldnames
    if x not in ('unicode_cp', 'unicode')
)

with CSV_OUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(registry)

with JSON_OUT.open('w', encoding='utf-8') as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(
    'M10.3I Immutable Unicode Registry\n'
    '================================\n'
    f'Unicode Egyptian records : {len(registry)}\n',
    encoding='utf-8'
)

print('M10.3I Immutable Unicode Registry')
print('================================')
print('Unicode Egyptian records :', len(registry))
print('CSV                      :', CSV_OUT)
print('JSON                     :', JSON_OUT)
print('Report                   :', REPORT)
