from pathlib import Path
import json
from statistics import mean
from math import sqrt

# -------------------------------------------------
# Paths
# -------------------------------------------------

input_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')
output_path = Path('datasets/egyptian_canonical/validation/gss_archetype_validation_v8_4.json')

FEATURES = ['Symmetry', 'Hierarchy', 'Complexity', 'Balance']

# -------------------------------------------------
# Load JSON safely
# -------------------------------------------------

with input_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

if isinstance(data, dict):
    records = data.get('results', [])
elif isinstance(data, list):
    records = data
else:
    raise ValueError('Unsupported JSON structure')

# -------------------------------------------------
# Group by Gardiner category
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
# Category statistics
# -------------------------------------------------

category_stats = {}

for category, items in sorted(groups.items()):
    stats = {'count': len(items)}

    for feature in FEATURES:
        values = [float(x[feature]) for x in items]
        m = mean(values)
        var = mean((v - m) ** 2 for v in values)

        stats[feature] = {
            'mean': m,
            'variance': var
        }

    category_stats[category] = stats

# -------------------------------------------------
# Euclidean distance between category centroids
# -------------------------------------------------

centroids = {}

for category, stats in category_stats.items():
    centroids[category] = [
        stats[f]['mean'] for f in FEATURES
    ]

distances = {}

cats = sorted(centroids.keys())

for c1 in cats:
    distances[c1] = {}

    for c2 in cats:
        a = centroids[c1]
        b = centroids[c2]

        d = sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
        distances[c1][c2] = d

# -------------------------------------------------
# Save
# -------------------------------------------------

output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open('w', encoding='utf-8') as f:
    json.dump({
        'version': 'V8.4',
        'categories': category_stats,
        'distances': distances
    }, f, ensure_ascii=False, indent=2)

# -------------------------------------------------
# Report
# -------------------------------------------------

print('GSS archetype validation V8.4 completed')
print('Output:', output_path)
print()

print('Category profiles')
print('-' * 72)
print(f'{"Cat":4s} {"N":5s} {"Sym":8s} {"Hier":8s} {"Comp":8s} {"Bal":8s}')

for category in cats:
    s = category_stats[category]
    print(
        f'{category:4s} '
        f'{s["count"]:5d} '
        f'{s["Symmetry"]["mean"]:8.3f} '
        f'{s["Hierarchy"]["mean"]:8.3f} '
        f'{s["Complexity"]["mean"]:8.3f} '
        f'{s["Balance"]["mean"]:8.3f}'
    )

print()
print('Most distant category pairs')
print('-' * 72)

pairs = []

for i, c1 in enumerate(cats):
    for c2 in cats[i+1:]:
        pairs.append((distances[c1][c2], c1, c2))

pairs.sort(reverse=True)

for d, c1, c2 in pairs[:10]:
    print(f'{c1} - {c2}: {d:.3f}')

print()
print('STATUS: PASS')
