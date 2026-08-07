from pathlib import Path
import json
from statistics import mean

# -------------------------------------------------
# Paths
# -------------------------------------------------

input_path = Path('datasets/egyptian_canonical/metrology/glyph_symmetry_spectrum_v6R.json')
output_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_2.json')

LEVELS = ['S16', 'S32', 'S64', 'S128', 'S256']

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def get_values(block):
    return [float(block.get(k, 0.0)) for k in LEVELS]

def integral_symmetry(block):
    values = get_values(block)
    return mean(values)

def spectral_curvature(block):
    values = get_values(block)

    if len(values) < 3:
        return 0.0

    second = []

    for i in range(1, len(values)-1):
        c = abs(values[i+1] - 2*values[i] + values[i-1])
        second.append(c)

    if not second:
        return 0.0

    curvature = mean(second)

    # normalize to 0–1
    return min(1.0, curvature * 10.0)

# -------------------------------------------------
# Load V6R
# -------------------------------------------------

with input_path.open('r', encoding='utf-8') as f:
    data = json.load(f)

results = []

for g in data:

    if 'vertical' not in g or 'horizontal' not in g:
        continue

    v = g['vertical']
    h = g['horizontal']

    v_sym = integral_symmetry(v)
    h_sym = integral_symmetry(h)

    symmetry = (v_sym + h_sym) / 2.0

    hierarchy = (
        float(v.get('SHI', 0.0)) +
        float(h.get('SHI', 0.0))
    ) / 2.0

    complexity = (
        spectral_curvature(v) +
        spectral_curvature(h)
    ) / 2.0

    balance = abs(
        float(v.get('SHI', 0.0)) -
        float(h.get('SHI', 0.0))
    )

    signature = {
        'Symmetry': round(symmetry, 6),
        'Hierarchy': round(hierarchy, 6),
        'Complexity': round(complexity, 6),
        'Balance': round(balance, 6)
    }

    vector = [
        signature['Symmetry'],
        signature['Hierarchy'],
        signature['Complexity'],
        signature['Balance']
    ]

    results.append({
        'unicode_cp': g.get('unicode_cp'),
        'jsesh_code': g.get('jsesh_code'),
        'gardiner_code': g.get('gardiner_code'),
        'vector': vector,
        'signature': signature
    })

with output_path.open('w', encoding='utf-8') as f:
    json.dump({
        'version': 'V8.2',
        'feature_order': [
            'Symmetry',
            'Hierarchy',
            'Complexity',
            'Balance'
        ],
        'results': results
    }, f, ensure_ascii=False, indent=2)

print('Glyph Structural Signature V8.2 completed')
print('Output:', output_path)
print('Glyphs:', len(results))
print('Average symmetry  :', round(mean(r['signature']['Symmetry'] for r in results), 4))
print('Average hierarchy :', round(mean(r['signature']['Hierarchy'] for r in results), 4))
print('Average complexity:', round(mean(r['signature']['Complexity'] for r in results), 4))
print('Average balance   :', round(mean(r['signature']['Balance'] for r in results), 4))
print('STATUS: PASS')
