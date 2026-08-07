from pathlib import Path
import json
from statistics import mean
from math import sqrt

# -------------------------------------------------
# Paths
# -------------------------------------------------

input_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')
output_path = Path('datasets/egyptian_canonical/validation/gss_correlation_v8_3.json')

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
# Extract valid records
# -------------------------------------------------

valid_records = []

for r in records:
    sig = r.get('signature')
    if not isinstance(sig, dict):
        continue

    if all(k in sig for k in FEATURES):
        valid_records.append(sig)

if not valid_records:
    raise ValueError('No valid GSS records found')

# -------------------------------------------------
# Build feature columns
# -------------------------------------------------

columns = {}

for feature in FEATURES:
    columns[feature] = [float(sig[feature]) for sig in valid_records]

# -------------------------------------------------
# Statistics
# -------------------------------------------------

def variance(values):
    m = mean(values)
    return mean((x - m) ** 2 for x in values)

def pearson(x, y):
    if len(x) != len(y) or len(x) == 0:
        return 0.0

    mx = mean(x)
    my = mean(y)

    sx = sqrt(sum((v - mx) ** 2 for v in x))
    sy = sqrt(sum((v - my) ** 2 for v in y))

    if sx == 0 or sy == 0:
        return 0.0

    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / (sx * sy)

summary = {}

for feature in FEATURES:
    values = columns[feature]
    summary[feature] = {
        'mean': mean(values),
        'min': min(values),
        'max': max(values),
        'variance': variance(values)
    }

# -------------------------------------------------
# Correlation matrix
# -------------------------------------------------

correlation = {}

for f1 in FEATURES:
    correlation[f1] = {}
    for f2 in FEATURES:
        correlation[f1][f2] = pearson(columns[f1], columns[f2])

# -------------------------------------------------
# Save results
# -------------------------------------------------

output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open('w', encoding='utf-8') as f:
    json.dump({
        'version': 'V8.3',
        'glyphs': len(valid_records),
        'summary': summary,
        'correlation': correlation
    }, f, ensure_ascii=False, indent=2)

# -------------------------------------------------
# Console report
# -------------------------------------------------

print('GSS correlation analysis V8.3 completed')
print('Output:', output_path)
print('Glyphs analyzed:', len(valid_records))
print()

print('Feature statistics')
print('-' * 64)

for feature in FEATURES:
    s = summary[feature]
    print(
        f'{feature:12s}',
        'mean =', round(s['mean'], 4),
        'var =', round(s['variance'], 5),
        'range =', round(s['min'], 4), '-', round(s['max'], 4)
    )

print()
print('Correlation matrix')
print('-' * 64)

header = ' ' * 12 + ''.join(f'{f:12s}' for f in FEATURES)
print(header)

for f1 in FEATURES:
    row = f'{f1:12s}'
    for f2 in FEATURES:
        row += f'{correlation[f1][f2]:12.3f}'
    print(row)

print()
print('STATUS: PASS')
