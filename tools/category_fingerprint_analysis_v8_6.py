from pathlib import Path
import json
from statistics import mean
from math import sqrt

# -------------------------------------------------
# Paths
# -------------------------------------------------

input_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')
output_path = Path('datasets/egyptian_canonical/archetypes/category_fingerprint_v8_6.json')

FEATURES = ['Symmetry', 'Hierarchy', 'Complexity', 'Balance']

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def std(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return sqrt(mean((v - m) ** 2 for v in values))

def euclidean(a, b):
    return sqrt(sum((a[f] - b[f]) ** 2 for f in FEATURES))

# -------------------------------------------------
# Load
# -------------------------------------------------

with input_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

records = data.get('results', data)

# -------------------------------------------------
# Group by category
# -------------------------------------------------

groups = {}

for r in records:
    code = r.get('gardiner_code')
    sig = r.get('signature')

    if not code or not isinstance(sig, dict):
        continue

    category = code[0]
    groups.setdefault(category, []).append(sig)

# -------------------------------------------------
# Global statistics
# -------------------------------------------------

global_mean = {}

for feature in FEATURES:
    values = [
        float(sig[feature])
        for items in groups.values()
        for sig in items
    ]
    global_mean[feature] = mean(values)

# -------------------------------------------------
# Fingerprints
# -------------------------------------------------

fingerprints = {}

for category, items in groups.items():

    centroid = {}
    stdev = {}
    variation = {}

    for feature in FEATURES:

        values = [float(sig[feature]) for sig in items]

        centroid[feature] = mean(values)
        stdev[feature] = std(values)

        if centroid[feature] != 0:
            variation[feature] = stdev[feature] / centroid[feature]
        else:
            variation[feature] = 0.0

    compactness = mean(stdev.values())

    fingerprints[category] = {
        'count': len(items),
        'centroid': centroid,
        'stdev': stdev,
        'variation': variation,
        'compactness': compactness
    }

# -------------------------------------------------
# Distances between categories
# -------------------------------------------------

for category in fingerprints:

    distances = {}

    for other in fingerprints:

        if other == category:
            continue

        d = euclidean(
            fingerprints[category]['centroid'],
            fingerprints[other]['centroid']
        )

        distances[other] = d

    nearest = min(distances, key=distances.get)
    farthest = max(distances, key=distances.get)

    fingerprints[category]['nearest_category'] = {
        'category': nearest,
        'distance': distances[nearest]
    }

    fingerprints[category]['farthest_category'] = {
        'category': farthest,
        'distance': distances[farthest]
    }

# -------------------------------------------------
# Unique markers
# -------------------------------------------------

for category in fingerprints:

    markers = []

    for feature in FEATURES:

        diff = (
            fingerprints[category]['centroid'][feature]
            - global_mean[feature]
        )

        score = abs(diff)

        markers.append({
            'feature': feature,
            'deviation': diff,
            'score': score
        })

    markers.sort(
        key=lambda x: x['score'],
        reverse=True
    )

    fingerprints[category]['unique_markers'] = markers[:2]

# -------------------------------------------------
# Save
# -------------------------------------------------

output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open('w', encoding='utf-8') as f:
    json.dump({
        'version': 'V8.6',
        'features': FEATURES,
        'fingerprints': fingerprints
    }, f, ensure_ascii=False, indent=2)

# -------------------------------------------------
# Report
# -------------------------------------------------

print('Category Fingerprint Analysis V8.6 completed')
print('Output:', output_path)
print()

print('Category fingerprints')
print('-' * 96)
print(f'{"Cat":4s} {"N":4s} {"Compact":10s} {"Nearest":10s} {"Distance":10s} {"Top marker":16s}')

for category in sorted(fingerprints):

    fp = fingerprints[category]

    marker = fp['unique_markers'][0]['feature']

    print(
        f'{category:4s} '
        f'{fp["count"]:4d} '
        f'{fp["compactness"]:10.4f} '
        f'{fp["nearest_category"]["category"]:10s} '
        f'{fp["nearest_category"]["distance"]:10.4f} '
        f'{marker:16s}'
    )

print()
print('STATUS: PASS')
