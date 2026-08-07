from pathlib import Path
import json
from statistics import mean

# -------------------------------------------------
# Paths
# -------------------------------------------------

input_path = Path('datasets/egyptian_canonical/metrology/glyph_symmetry_spectrum_v6R.json')
output_path = Path('datasets/egyptian_canonical/metrology/glyph_structural_signature_v8_1.json')

# -------------------------------------------------
# Helpers
# -------------------------------------------------

LEVELS = ['S16', 'S32', 'S64', 'S128', 'S256']

def spectral_stability(block):
    values = [float(block.get(k, 0.0)) for k in LEVELS]
    if len(values) < 2:
        return 0.0
    diffs = [abs(values[i+1] - values[i]) for i in range(len(values)-1)]
    variation = sum(diffs) / len(diffs)
    return max(0.0, 1.0 - variation)

def profile_type(block):
    values = [float(block.get(k, 0.0)) for k in LEVELS]
    if len(values) < 5:
        return 'Mixed'

    d1 = values[1] - values[0]
    d2 = values[2] - values[1]
    d3 = values[3] - values[2]
    d4 = values[4] - values[3]

    eps = 0.01

    if all(x <= eps for x in [d1, d2, d3, d4]):
        return 'Decay'

    if all(x >= -eps for x in [d1, d2, d3, d4]):
        return 'Growth'

    if d1 < 0 and d4 > 0:
        return 'U'

    if d1 > 0 and d4 < 0:
        return 'Inverse-U'

    if max(values) - min(values) < 0.03:
        return 'Flat'

    return 'Mixed'

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

    v_sym = float(v.get('S256', 0.0))
    h_sym = float(h.get('S256', 0.0))

    symmetry = (v_sym + h_sym) / 2.0
    hierarchy = (float(v.get('SHI', 0.0)) + float(h.get('SHI', 0.0))) / 2.0
    branching = (abs(float(v.get('lambda', 0.0))) + abs(float(h.get('lambda', 0.0)))) / 2.0
    stability = (spectral_stability(v) + spectral_stability(h)) / 2.0

    orientation = float(v.get('SHI', 0.0)) - float(h.get('SHI', 0.0))

    pv = profile_type(v)
    ph = profile_type(h)

    profile = pv if pv == ph else 'Mixed'

    signature = {
        'Symmetry': symmetry,
        'Hierarchy': hierarchy,
        'Branching': branching,
        'Stability': stability,
        'Orientation': orientation,
        'Profile': profile
    }

    vector = [
        symmetry,
        hierarchy,
        branching,
        stability
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
        'version': 'V8.1',
        'feature_order': [
            'Symmetry',
            'Hierarchy',
            'Branching',
            'Stability'
        ],
        'results': results
    }, f, ensure_ascii=False, indent=2)

print('Glyph Structural Signature V8.1 completed')
print('Output:', output_path)
print('Glyphs:', len(results))
print('Average symmetry :', round(mean(r['signature']['Symmetry'] for r in results), 4))
print('Average hierarchy:', round(mean(r['signature']['Hierarchy'] for r in results), 4))
print('Average branching:', round(mean(r['signature']['Branching'] for r in results), 5))
print('Average stability:', round(mean(r['signature']['Stability'] for r in results), 4))
print('STATUS: PASS')
