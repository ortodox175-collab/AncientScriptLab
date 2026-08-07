from pathlib import Path
import json
from statistics import median, mean

FP = Path('datasets/egyptian_canonical/archetypes/category_fingerprint_v8_6.json')
OUT = Path('datasets/egyptian_canonical/validation/statistical_architecture_baseline_v8_10A.json')

if not FP.exists():
    raise SystemExit(f'Missing file: {FP}')

data = json.loads(FP.read_text(encoding='utf-8'))
fingerprints = data.get('fingerprints', {})

if not fingerprints:
    raise SystemExit('No fingerprints found')

FEATURES = ['Symmetry','Hierarchy','Complexity','Balance']

# -------------------------------------------------
# Collect distributions
# -------------------------------------------------

compactness = []
distance = []
feature_values = {f: [] for f in FEATURES}

for fp in fingerprints.values():
    compactness.append(float(fp['compactness']))
    distance.append(float(fp['nearest_category']['distance']))
    centroid = fp['centroid']
    for f in FEATURES:
        feature_values[f].append(float(centroid[f]))

# -------------------------------------------------
# Robust statistics
# -------------------------------------------------

def mad(values):
    m = median(values)
    return median([abs(v - m) for v in values])

def ecdf_probability(values, x):
    n = len(values)
    if n == 0:
        return 0.0
    rank = sum(1 for v in values if v <= x)
    p = rank / n
    return 2 * min(p, 1 - p)

baseline = {
    'compactness': {
        'median': median(compactness),
        'mad': mad(compactness),
        'min': min(compactness),
        'max': max(compactness)
    },
    'distance': {
        'median': median(distance),
        'mad': mad(distance),
        'min': min(distance),
        'max': max(distance)
    },
    'features': {}
}

for f in FEATURES:
    baseline['features'][f] = {
        'median': median(feature_values[f]),
        'mad': mad(feature_values[f]),
        'min': min(feature_values[f]),
        'max': max(feature_values[f])
    }

# -------------------------------------------------
# Category empirical probabilities
# -------------------------------------------------

category_scores = []

for cat in sorted(fingerprints):
    fp = fingerprints[cat]
    centroid = fp['centroid']

    p_comp = ecdf_probability(compactness, float(fp['compactness']))
    p_dist = ecdf_probability(distance, float(fp['nearest_category']['distance']))

    p_features = {}
    for f in FEATURES:
        p_features[f] = ecdf_probability(feature_values[f], float(centroid[f]))

    architecture_probability = mean(
        [p_comp, p_dist] + list(p_features.values())
    )

    category_scores.append({
        'Category': cat,
        'N': fp['count'],
        'Compactness': float(fp['compactness']),
        'Distance': float(fp['nearest_category']['distance']),
        'P_compactness': p_comp,
        'P_distance': p_dist,
        'P_features': p_features,
        'ArchitectureProbability': architecture_probability
    })

# -------------------------------------------------
# Weighted AII v3.0
# -------------------------------------------------

weighted_sum = sum(x['ArchitectureProbability'] * x['N'] for x in category_scores)
total_signs = sum(x['N'] for x in category_scores)
AII = weighted_sum / total_signs

# -------------------------------------------------
# Save
# -------------------------------------------------

OUT.parent.mkdir(parents=True, exist_ok=True)

OUT.write_text(
    json.dumps({
        'version': 'V8.10A',
        'baseline': baseline,
        'categories': category_scores,
        'AII_v3': AII
    }, ensure_ascii=False, indent=2),
    encoding='utf-8'
)

# -------------------------------------------------
# Report
# -------------------------------------------------

print('STATISTICAL ARCHITECTURE BASELINE V8.10A')
print('=' * 120)
print()

print(f'{"Cat":4s} {"N":4s} {"P_arch":8s} {"P_comp":8s} {"P_dist":8s}')
print('-' * 120)

for x in category_scores:
    print(
        f'{x["Category"]:4s} '
        f'{x["N"]:4d} '
        f'{x["ArchitectureProbability"]:8.3f} '
        f'{x["P_compactness"]:8.3f} '
        f'{x["P_distance"]:8.3f}'
    )

print()
print('=' * 120)
print('EMPIRICAL BASELINE')
print('=' * 120)

print(
    f'Compactness median = {baseline["compactness"]["median"]:.4f} '
    f'MAD = {baseline["compactness"]["mad"]:.4f}'
)

print(
    f'Distance median    = {baseline["distance"]["median"]:.4f} '
    f'MAD = {baseline["distance"]["mad"]:.4f}'
)

print()
print('=' * 120)
print('EMPIRICAL ARCHITECTURE INTEGRITY INDEX')
print('=' * 120)
print(f'AII v3.0 = {AII:.4f}')
print()
print(f'Output: {OUT}')
print('STATUS: PASS')
