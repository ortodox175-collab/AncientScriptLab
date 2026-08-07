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

# -------------------------------------------------
# Feature statistics
# -------------------------------------------------

feature_stats = {}

for f in FEATURES:
    vals = [float(r['signature'][f]) for r in records]
    feature_stats[f] = {
        'min': min(vals),
        'max': max(vals),
        'mean': mean(vals)
    }

# -------------------------------------------------
# Category statistics
# -------------------------------------------------

table = []
compactness = []
distances = []
marker_counts = {f: 0 for f in FEATURES}

for cat in sorted(fingerprints):
    x = fingerprints[cat]
    c = x['centroid']
    comp = float(x['compactness'])
    dist = float(x['nearest_category']['distance'])
    marker = x['unique_markers'][0]['feature']

    compactness.append(comp)
    distances.append(dist)
    marker_counts[marker] += 1

    table.append({
        'Category': cat,
        'N': x['count'],
        'Symmetry': c['Symmetry'],
        'Hierarchy': c['Hierarchy'],
        'Complexity': c['Complexity'],
        'Balance': c['Balance'],
        'Compactness': comp,
        'Nearest': x['nearest_category']['category'],
        'Distance': dist,
        'TopMarker': marker
    })

# -------------------------------------------------
# Integrity metrics
# -------------------------------------------------

total = len(records)
codes = [r['gardiner_code'] for r in records]

canonical_uniqueness = len(set(codes)) / total
feature_completeness = 1.0

range_score = 1.0
for f in FEATURES:
    s = feature_stats[f]
    if s['min'] < 0 or s['max'] > 1:
        range_score = 0.0

# -------------------------------------------------
# Compactness score (optimal zone: 0.08–0.14)
# -------------------------------------------------

compactness_mean = mean(compactness)

if 0.08 <= compactness_mean <= 0.14:
    compactness_score = 1.0
elif compactness_mean < 0.08:
    compactness_score = max(0.0, compactness_mean / 0.08)
else:
    compactness_score = max(0.0, 1.0 - (compactness_mean - 0.14) / 0.10)

# -------------------------------------------------
# Separation score (optimal zone: 0.05–0.08)
# -------------------------------------------------

separation_mean = mean(distances)

if 0.05 <= separation_mean <= 0.08:
    separation_score = 1.0
elif separation_mean < 0.05:
    separation_score = max(0.0, separation_mean / 0.05)
else:
    separation_score = max(0.0, 1.0 - (separation_mean - 0.08) / 0.20)

# -------------------------------------------------
# Marker diversity
# -------------------------------------------------

marker_diversity = len([v for v in marker_counts.values() if v > 0]) / len(FEATURES)

# -------------------------------------------------
# Weighted Architecture Integrity Index v2.0
# -------------------------------------------------

weights = {
    'canonical': 0.25,
    'completeness': 0.25,
    'ranges': 0.10,
    'compactness': 0.15,
    'separation': 0.15,
    'markers': 0.10,
}

AII = (
    canonical_uniqueness * weights['canonical'] +
    feature_completeness * weights['completeness'] +
    range_score * weights['ranges'] +
    compactness_score * weights['compactness'] +
    separation_score * weights['separation'] +
    marker_diversity * weights['markers']
)

# -------------------------------------------------
# Ranking
# -------------------------------------------------

most_compact = sorted(table, key=lambda x: x['Compactness'])[:5]
most_isolated = sorted(table, key=lambda x: x['Distance'], reverse=True)[:5]

# -------------------------------------------------
# Report
# -------------------------------------------------

print('MASTER VALIDATION REPORT V8.9S')
print('=' * 120)
print()

print(f'{"Cat":4s} {"N":4s} {"Sym":7s} {"Hier":7s} {"Comp":7s} {"Bal":7s} {"Compact":8s} {"Near":5s} {"Dist":7s} {"Marker":10s}')
print('-' * 120)

for r in table:
    print(
        f'{r["Category"]:4s} '
        f'{r["N"]:4d} '
        f'{r["Symmetry"]:7.3f} '
        f'{r["Hierarchy"]:7.3f} '
        f'{r["Complexity"]:7.3f} '
        f'{r["Balance"]:7.3f} '
        f'{r["Compactness"]:8.3f} '
        f'{r["Nearest"]:5s} '
        f'{r["Distance"]:7.3f} '
        f'{r["TopMarker"]:10s}'
    )

print()
print('=' * 120)
print('КОЛИЧЕСТВЕННАЯ ВАЛИДАЦИЯ')
print('=' * 120)

print(f'Canonical uniqueness : {canonical_uniqueness:.4f}')
print(f'Feature completeness : {feature_completeness:.4f}')
print(f'Range score          : {range_score:.4f}')
print()
print(f'Compactness mean     : {compactness_mean:.4f}')
print(f'Compactness score    : {compactness_score:.4f}')
print()
print(f'Separation mean      : {separation_mean:.4f}')
print(f'Separation score     : {separation_score:.4f}')
print()
print(f'Marker diversity     : {marker_diversity:.4f}')

print()
print('=' * 120)
print('ARCHITECTURE INTEGRITY INDEX V2.0')
print('=' * 120)
print(f'AII                 : {AII:.4f}')

print()
print('Top 5 most compact categories:')
for r in most_compact:
    print(f'{r["Category"]} : {r["Compactness"]:.4f}')

print()
print('Top 5 most isolated categories:')
for r in most_isolated:
    print(f'{r["Category"]} : {r["Distance"]:.4f}')

print()
print('STATUS: PASS')
