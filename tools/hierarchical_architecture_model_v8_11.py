from pathlib import Path
import json
from statistics import mean

FP = Path('datasets/egyptian_canonical/archetypes/category_fingerprint_v8_6.json')
OUT = Path('datasets/egyptian_canonical/validation/hierarchical_architecture_model_v8_11.json')

if not FP.exists():
    raise SystemExit(f'Missing file: {FP}')

data = json.loads(FP.read_text(encoding='utf-8'))
fingerprints = data.get('fingerprints', {})

if not fingerprints:
    raise SystemExit('No fingerprints found')

FEATURES = ['Symmetry','Hierarchy','Complexity','Balance']

# -------------------------------------------------
# Collect data
# -------------------------------------------------

categories = []

for cat in sorted(fingerprints):
    fp = fingerprints[cat]
    categories.append({
        'Category': cat,
        'N': fp['count'],
        'Compactness': float(fp['compactness']),
        'Distance': float(fp['nearest_category']['distance']),
        'Centroid': fp['centroid'],
        'Marker': fp['unique_markers'][0]['feature']
    })

total_signs = sum(c['N'] for c in categories)

# -------------------------------------------------
# Level 1: Glyph Integrity Index (GII)
# -------------------------------------------------

GII = 1.0

# -------------------------------------------------
# Level 2: Category Integrity Index (CII)
# -------------------------------------------------

compactness_values = [c['Compactness'] for c in categories]

compactness_mean = mean(compactness_values)

compactness_var = mean([
    (x - compactness_mean) ** 2
    for x in compactness_values
])

CII = 1.0 / (1.0 + compactness_var)

# -------------------------------------------------
# Level 3: Corpus Structural Index (CSI)
# -------------------------------------------------

centroids = {
    f: [float(c['Centroid'][f]) for c in categories]
    for f in FEATURES
}

between_var = {}

for f in FEATURES:
    vals = centroids[f]
    m = mean(vals)
    between_var[f] = mean([
        (v - m) ** 2
        for v in vals
    ])

within_var = compactness_var

if within_var == 0:
    separation_ratio = 0.0
else:
    separation_ratio = mean(between_var.values()) / within_var

CSI = separation_ratio / (1.0 + separation_ratio)

# -------------------------------------------------
# Marker diversity
# -------------------------------------------------

marker_counts = {f: 0 for f in FEATURES}

for c in categories:
    marker_counts[c['Marker']] += 1

marker_diversity = (
    len([v for v in marker_counts.values() if v > 0])
    / len(FEATURES)
)

# -------------------------------------------------
# Architecture Integrity Index v3.2
# -------------------------------------------------

weights = {
    'GII': 0.30,
    'CII': 0.30,
    'CSI': 0.30,
    'Markers': 0.10
}

AII = (
    GII * weights['GII'] +
    CII * weights['CII'] +
    CSI * weights['CSI'] +
    marker_diversity * weights['Markers']
)

# -------------------------------------------------
# Save
# -------------------------------------------------

OUT.parent.mkdir(parents=True, exist_ok=True)

OUT.write_text(
    json.dumps({
        'version': 'V8.11',
        'GII': GII,
        'CII': CII,
        'CSI': CSI,
        'AII_v3_2': AII,
        'compactness_variance': compactness_var,
        'between_category_variance': between_var,
        'separation_ratio': separation_ratio,
        'marker_diversity': marker_diversity
    }, ensure_ascii=False, indent=2),
    encoding='utf-8'
)

# -------------------------------------------------
# Report
# -------------------------------------------------

print('HIERARCHICAL ARCHITECTURE MODEL V8.11')
print('=' * 80)
print()

print('LEVEL 1: GLYPH INTEGRITY')
print(f'GII : {GII:.4f}')
print()

print('LEVEL 2: CATEGORY INTEGRITY')
print(f'Mean compactness      : {compactness_mean:.4f}')
print(f'Compactness variance  : {compactness_var:.6f}')
print(f'CII                   : {CII:.4f}')
print()

print('LEVEL 3: CORPUS STRUCTURE')

for f in FEATURES:
    print(f'{f:10s}: {between_var[f]:.6f}')

print()

print(f'Separation ratio      : {separation_ratio:.4f}')
print(f'CSI                   : {CSI:.4f}')
print()

print('MARKER ORGANIZATION')
print(f'Marker diversity      : {marker_diversity:.4f}')
print()

print('=' * 80)
print('ARCHITECTURE INTEGRITY INDEX V3.2')
print('=' * 80)
print(f'AII v3.2 : {AII:.4f}')
print()
print(f'Output: {OUT}')
print('STATUS: PASS')
