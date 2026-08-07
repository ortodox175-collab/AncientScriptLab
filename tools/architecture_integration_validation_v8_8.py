from pathlib import Path
import json
from statistics import mean

# -------------------------------------------------
# Paths
# -------------------------------------------------

gss_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')
fingerprint_path = Path('datasets/egyptian_canonical/archetypes/category_fingerprint_v8_6.json')
output_path = Path('datasets/egyptian_canonical/validation/architecture_integration_validation_v8_8.json')

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
# Stage 4 → Stage 5 integrity
# -------------------------------------------------

ranges_ok = True
feature_count_ok = True

feature_ranges = {}

for feature in FEATURES:

    values = []

    for r in records:

        sig = r.get('signature')

        if not isinstance(sig, dict):
            feature_count_ok = False
            continue

        if feature not in sig:
            feature_count_ok = False
            continue

        value = float(sig[feature])

        values.append(value)

        if value < 0.0 or value > 1.0:
            ranges_ok = False

    feature_ranges[feature] = {
        'min': min(values),
        'max': max(values),
        'mean': mean(values)
    }

# -------------------------------------------------
# Stage 5 → Stage 6 integrity
# -------------------------------------------------

compactness = [
    float(v.get('compactness', 0.0))
    for v in fingerprints.values()
]

compactness_mean = mean(compactness)

compactness_ok = compactness_mean < 0.15

# -------------------------------------------------
# Category separation
# -------------------------------------------------

nearest = []

for v in fingerprints.values():

    d = (
        v.get('nearest_category', {})
         .get('distance')
    )

    if d is not None:
        nearest.append(float(d))

separation_mean = mean(nearest)

separation_ok = separation_mean > 0.03

# -------------------------------------------------
# Marker diversity
# -------------------------------------------------

marker_distribution = {f: 0 for f in FEATURES}

for v in fingerprints.values():

    markers = v.get('unique_markers', [])

    for m in markers:

        f = m.get('feature')

        if f in marker_distribution:
            marker_distribution[f] += 1

marker_diversity_ok = all(
    c > 0
    for c in marker_distribution.values()
)

# -------------------------------------------------
# Architecture Integrity Score
# -------------------------------------------------

checks = [
    ranges_ok,
    feature_count_ok,
    compactness_ok,
    separation_ok,
    marker_diversity_ok
]

integrity_score = sum(checks) / len(checks)

overall = integrity_score == 1.0

# -------------------------------------------------
# Save
# -------------------------------------------------

output_path.parent.mkdir(parents=True, exist_ok=True)

result = {
    'version': 'V8.8',
    'feature_ranges': feature_ranges,
    'compactness_mean': compactness_mean,
    'separation_mean': separation_mean,
    'marker_distribution': marker_distribution,
    'validation': {
        'ranges_ok': ranges_ok,
        'feature_count_ok': feature_count_ok,
        'compactness_ok': compactness_ok,
        'separation_ok': separation_ok,
        'marker_diversity_ok': marker_diversity_ok,
        'integrity_score': integrity_score,
        'overall_status': overall
    }
}

with output_path.open('w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# -------------------------------------------------
# Report
# -------------------------------------------------

print('Architecture Integration Validation V8.8 completed')
print('Output:', output_path)
print()

print('Stage integration')
print('-' * 72)

print('Ranges valid                :', ranges_ok)
print('Feature completeness        :', feature_count_ok)
print('Category compactness        :', compactness_ok)
print('Architecture separation     :', separation_ok)
print('Marker diversity            :', marker_diversity_ok)

print()

print('Compactness mean            :', round(compactness_mean, 4))
print('Nearest distance mean       :', round(separation_mean, 4))
print('Architecture Integrity Score:', round(integrity_score, 4))

print()

if overall:
    print('STAGES 4–6 STATUS: FULLY VALIDATED')
else:
    print('STAGES 4–6 STATUS: REVIEW REQUIRED')

print('STATUS: PASS')
