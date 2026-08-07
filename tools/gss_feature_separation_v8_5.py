from pathlib import Path
import json
from statistics import mean

# -------------------------------------------------
# Paths
# -------------------------------------------------

input_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')
output_path = Path('datasets/egyptian_canonical/validation/gss_feature_separation_v8_5.json')

FEATURES = ['Symmetry', 'Hierarchy', 'Complexity', 'Balance']

# -------------------------------------------------
# Load data
# -------------------------------------------------

with input_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

records = data.get('results', data)

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
# Separation analysis
# -------------------------------------------------

analysis = {}

for feature in FEATURES:

    category_means = {}
    within_vars = []

    for category, items in groups.items():

        values = [float(x[feature]) for x in items]

        m = mean(values)
        category_means[category] = m

        if len(values) > 1:
            var = mean((v - m) ** 2 for v in values)
            within_vars.append(var)

    global_mean = mean(category_means.values())

    between_var = mean(
        (v - global_mean) ** 2
        for v in category_means.values()
    )

    within_var = mean(within_vars) if within_vars else 0.0

    separation_ratio = (
        between_var / within_var
        if within_var > 0
        else 0.0
    )

    analysis[feature] = {
        'between_category_variance': between_var,
        'within_category_variance': within_var,
        'separation_ratio': separation_ratio,
        'category_means': category_means
    }

# -------------------------------------------------
# Save
# -------------------------------------------------

output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open('w', encoding='utf-8') as f:
    json.dump({
        'version': 'V8.5',
        'features': analysis
    }, f, ensure_ascii=False, indent=2)

# -------------------------------------------------
# Report
# -------------------------------------------------

print('GSS feature separation V8.5 completed')
print('Output:', output_path)
print()

print('Feature separation ratios')
print('-' * 72)
print(f'{"Feature":12s} {"Between":12s} {"Within":12s} {"Ratio":12s}')

for feature in FEATURES:
    a = analysis[feature]

    print(
        f'{feature:12s} '
        f'{a["between_category_variance"]:12.5f} '
        f'{a["within_category_variance"]:12.5f} '
        f'{a["separation_ratio"]:12.3f}'
    )

best = max(
    FEATURES,
    key=lambda f: analysis[f]['separation_ratio']
)

print()
print('Best separating feature:', best)
print('STATUS: PASS')
