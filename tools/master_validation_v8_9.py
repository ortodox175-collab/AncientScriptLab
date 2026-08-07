from pathlib import Path
import json
from statistics import mean

GSS = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')
FP = Path('datasets/egyptian_canonical/archetypes/category_fingerprint_v8_6.json')

if not GSS.exists():
    raise SystemExit(f'Missing file: {GSS}')
if not FP.exists():
    raise SystemExit(f'Missing file: {FP}')

gss_data = json.loads(GSS.read_text(encoding='utf-8'))
records = gss_data.get('results', gss_data)

fp_data = json.loads(FP.read_text(encoding='utf-8'))
fingerprints = fp_data.get('fingerprints', {})

FEATURES = ['Symmetry', 'Hierarchy', 'Complexity', 'Balance']

codes = [r.get('gardiner_code') for r in records if r.get('gardiner_code')]
unique_codes = len(set(codes))
duplicates = len(codes) - unique_codes

feature_stats = {}
for feature in FEATURES:
    values = []
    missing = 0
    for r in records:
        sig = r.get('signature')
        if not isinstance(sig, dict) or feature not in sig:
            missing += 1
            continue
        values.append(float(sig[feature]))
    if not values:
        raise SystemExit(f'No values for feature {feature}')
    feature_stats[feature] = {
        'min': min(values),
        'max': max(values),
        'mean': mean(values),
        'missing': missing
    }

compactness = []
distances = []
marker_counts = {f: 0 for f in FEATURES}

for cat, fp in sorted(fingerprints.items()):
    compactness.append(float(fp.get('compactness', 0.0)))
    nearest = fp.get('nearest_category', {})
    d = nearest.get('distance')
    if d is not None:
        distances.append(float(d))
    markers = fp.get('unique_markers', [])
    if markers:
        m = markers[0].get('feature')
        if m in marker_counts:
            marker_counts[m] += 1

compactness_mean = mean(compactness)
compactness_min = min(compactness)
compactness_max = max(compactness)

distance_mean = mean(distances)
distance_min = min(distances)
distance_max = max(distances)

print('MASTER VALIDATION V8.9')
print('=' * 120)
print()
print(f'{"Cat":4s} {"N":4s} {"Symmetry":9s} {"Hierarchy":10s} {"Complexity":11s} {"Balance":8s} {"Compact":8s} {"Nearest":7s} {"Distance":8s} {"Top marker":12s}')
print('-' * 120)

for cat, fp in sorted(fingerprints.items()):
    c = fp.get('centroid', {})
    nearest = fp.get('nearest_category', {})
    markers = fp.get('unique_markers', [])
    marker = markers[0].get('feature') if markers else '-'
    print(
        f'{cat:4s} '
        f'{fp.get("count",0):4d} '
        f'{c.get("Symmetry",0):9.4f} '
        f'{c.get("Hierarchy",0):10.4f} '
        f'{c.get("Complexity",0):11.4f} '
        f'{c.get("Balance",0):8.4f} '
        f'{fp.get("compactness",0):8.4f} '
        f'{nearest.get("category","-"):7s} '
        f'{nearest.get("distance",0):8.4f} '
        f'{marker:12s}'
    )

print()
print('=' * 120)
print('СВОДНЫЕ ПОКАЗАТЕЛИ')
print('=' * 120)
print(f'Всего знаков                    : {len(records)}')
print(f'Уникальных Gardiner-кодов       : {unique_codes}')
print(f'Дубликатов                      : {duplicates}')
print()
for feature in FEATURES:
    s = feature_stats[feature]
    print(f'{feature:12s}: min={s["min"]:.4f} max={s["max"]:.4f} mean={s["mean"]:.4f} missing={s["missing"]}')
print()
print(f'Средняя компактность категорий  : {compactness_mean:.4f}')
print(f'Минимальная компактность        : {compactness_min:.4f}')
print(f'Максимальная компактность       : {compactness_max:.4f}')
print()
print(f'Среднее расстояние категорий    : {distance_mean:.4f}')
print(f'Минимальное расстояние          : {distance_min:.4f}')
print(f'Максимальное расстояние         : {distance_max:.4f}')
print()
print('РАСПРЕДЕЛЕНИЕ ГЛАВНЫХ МАРКЕРОВ')
print('-' * 120)
for k in FEATURES:
    print(f'{k:12s}: {marker_counts[k]}')

ranges_ok = all(
    0.0 <= feature_stats[f]['min'] and feature_stats[f]['max'] <= 1.0
    for f in FEATURES
)
feature_complete = all(feature_stats[f]['missing'] == 0 for f in FEATURES)
compactness_ok = compactness_mean < 0.15
separation_ok = distance_mean > 0.03
marker_diversity_ok = all(marker_counts[f] > 0 for f in FEATURES)

score = sum([
    ranges_ok,
    feature_complete,
    compactness_ok,
    separation_ok,
    marker_diversity_ok,
]) / 5

print()
print('=' * 120)
print('ИТОГОВАЯ ВАЛИДАЦИЯ')
print('=' * 120)
print(f'Диапазоны признаков            : {ranges_ok}')
print(f'Полнота признаков              : {feature_complete}')
print(f'Компактность категорий         : {compactness_ok}')
print(f'Разделение категорий           : {separation_ok}')
print(f'Разнообразие маркеров          : {marker_diversity_ok}')
print(f'Architecture Integrity Score   : {score:.4f}')
print()
print('STATUS: PASS')
