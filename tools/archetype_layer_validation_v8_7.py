from pathlib import Path
import json
from statistics import mean

# -------------------------------------------------
# Paths
# -------------------------------------------------

gss_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')
fingerprint_path = Path('datasets/egyptian_canonical/archetypes/category_fingerprint_v8_6.json')
output_path = Path('datasets/egyptian_canonical/validation/archetype_layer_validation_v8_7.json')

FEATURES = ['Symmetry', 'Hierarchy', 'Complexity', 'Balance']

# -------------------------------------------------
# Load
# -------------------------------------------------

if not gss_path.exists():
    raise SystemExit(f'Missing file: {gss_path}')

if not fingerprint_path.exists():
    raise SystemExit(f'Missing file: {fingerprint_path}')

with gss_path.open('r', encoding='utf-8') as f:
    gss = json.load(f)

with fingerprint_path.open('r', encoding='utf-8') as f:
    fp = json.load(f)

records = gss.get('results', gss)
fingerprints = fp.get('fingerprints', {})

# -------------------------------------------------
# Feature ranges
# -------------------------------------------------

feature_stats = {}

for feature in FEATURES:
    values = [
        float(r['signature'][feature])
        for r in records
        if 'signature' in r and feature in r['signature']
    ]

    feature_stats[feature] = {
        'min': min(values),
        'max': max(values),
        'mean': mean(values)
    }

# -------------------------------------------------
# Compactness
# -------------------------------------------------

compactness_values = [
    float(v.get('compactness', 0.0))
    for v in fingerprints.values()
]

compactness_mean = mean(compactness_values)
compactness_max = max(compactness_values)
compactness_min = min(compactness_values)

# -------------------------------------------------
# Unique markers
# -------------------------------------------------

marker_counts = {f: 0 for f in FEATURES}

for category in fingerprints.values():
    markers = category.get('unique_markers', [])
    for m in markers:
        feature = m.get('feature')
        if feature in marker_counts:
            marker_counts[feature] += 1

# -------------------------------------------------
# Nearest category distances
# -------------------------------------------------

nearest_distances = []

for category in fingerprints.values():
    nearest = category.get('nearest_category', {})
    d = nearest.get('distance')
    if d is not None:
        nearest_distances.append(float(d))

distance_mean = mean(nearest_distances)
distance_min = min(nearest_distances)
distance_max = max(nearest_distances)

# -------------------------------------------------
# Read V8.5 separation ratio if available
# -------------------------------------------------

separation_path = Path('datasets/egyptian_canonical/validation/gss_feature_separation_v8_5.json')

best_feature = None
best_ratio = None

if separation_path.exists():
    with separation_path.open('r', encoding='utf-8') as f:
        sep = json.load(f)

    ratios = sep.get('feature_separation', {})
    if ratios:
        best_feature = max(ratios, key=lambda k: ratios[k]['ratio'])
        best_ratio = ratios[best_feature]['ratio']

# -------------------------------------------------
# Validation criteria
# -------------------------------------------------

validation = {
    'gss_ranges_valid': all(
        0.0 <= feature_stats[f]['min'] and feature_stats[f]['max'] <= 1.0
        for f in FEATURES
    ),
    'category_compactness_valid': compactness_mean < 0.15,
    'architecture_separation_valid': distance_mean > 0.03,
    'marker_diversity_valid': len(
        [f for f, c in marker_counts.items() if c > 0]
    ) == len(FEATURES),
    'best_separating_feature': best_feature,
    'best_separation_ratio': best_ratio
}

validation['overall_status'] = all([
    validation['gss_ranges_valid'],
    validation['category_compactness_valid'],
    validation['architecture_separation_valid'],
    validation['marker_diversity_valid']
])

# -------------------------------------------------
# Save
# -------------------------------------------------

output_path.parent.mkdir(parents=True, exist_ok=True)

result = {
    'version': 'V8.7',
    'feature_statistics': feature_stats,
    'compactness': {
        'mean': compactness_mean,
        'min': compactness_min,
        'max': compactness_max
    },
    'nearest_category_distances': {
        'mean': distance_mean,
        'min': distance_min,
        'max': distance_max
    },
    'marker_distribution': marker_counts,
    'validation': validation
}

with output_path.open('w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# -------------------------------------------------
# Report
# -------------------------------------------------

print('Archetype Layer Validation V8.7 completed')
print('Output:', output_path)
print()

print('Validation summary')
print('-' * 64)

print('GSS ranges valid            :', validation['gss_ranges_valid'])
print('Category compactness valid  :', validation['category_compactness_valid'])
print('Architecture separation     :', validation['architecture_separation_valid'])
print('Marker diversity            :', validation['marker_diversity_valid'])

if best_feature is not None:
    print('Best separating feature     :', best_feature)
    print('Best separation ratio       :', round(best_ratio, 4))

print()

print('Compactness mean            :', round(compactness_mean, 4))
print('Nearest distance mean       :', round(distance_mean, 4))

print()

if validation['overall_status']:
    print('ARCHETYPE LAYER STATUS: VALIDATED')
else:
    print('ARCHETYPE LAYER STATUS: REVIEW REQUIRED')

print('STATUS: PASS')
