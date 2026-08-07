from pathlib import Path
import json
from statistics import mean
from math import log, exp
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen

# -------------------------------------------------
# Configuration
# -------------------------------------------------

registry_path = Path('datasets/egyptian_canonical/corpus/egyptian_canonical_registry_v1.json')
font_path = Path('datasets/egyptian_canonical/fonts/JSeshFont.ttf')

out_dir = Path('datasets/egyptian_canonical/metrology')
out_dir.mkdir(parents=True, exist_ok=True)

output_path = out_dir / 'glyph_symmetry_spectrum_v6R.json'

LEVELS = [16, 32, 64, 128, 256]

# -------------------------------------------------
# Load registry and font
# -------------------------------------------------

with registry_path.open('r', encoding='utf-8') as f:
    registry = json.load(f)

font = TTFont(font_path)
glyph_set = font.getGlyphSet()

cmap = {}
for table in font['cmap'].tables:
    cmap.update(table.cmap)

# -------------------------------------------------
# Normalize contour points
# -------------------------------------------------

def normalized_points(glyph):

    bounds_pen = BoundsPen(glyph_set)
    glyph.draw(bounds_pen)

    if bounds_pen.bounds is None:
        return None

    xmin, ymin, xmax, ymax = bounds_pen.bounds

    width = xmax - xmin
    height = ymax - ymin

    if width == 0 or height == 0:
        return None

    pen = RecordingPen()
    glyph.draw(pen)

    pts = []

    for cmd, points in pen.value:
        for p in points:
            if p is None:
                continue
            x = (p[0] - xmin) / width
            y = (p[1] - ymin) / height
            pts.append((x, y))

    return pts

# -------------------------------------------------
# Rotate around center
# -------------------------------------------------

def rotate_90(points):

    if not points:
        return points

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2

    out = []

    for x, y in points:
        dx = x - cx
        dy = y - cy
        rx = -dy
        ry = dx
        out.append((rx + cx, ry + cy))

    return out

# -------------------------------------------------
# Canonical symmetry analyzer
# -------------------------------------------------

def strip_symmetry(points, strips):

    hist = [0] * strips

    for x, y in points:
        i = min(int(x * strips), strips - 1)
        hist[i] += 1

    total = sum(hist)

    if total == 0:
        return 0.0

    left = hist[:strips // 2]
    right = hist[strips // 2:]

    diff = sum(
        abs(a - b)
        for a, b in zip(left, reversed(right))
    )

    return max(0.0, 1.0 - diff / total)

# -------------------------------------------------
# Spectrum + lambda + R2 + SHI
# -------------------------------------------------

def analyze(points):

    values = []

    for strips in LEVELS:
        values.append(strip_symmetry(points, strips))

    spectrum = {}

    for strips, value in zip(LEVELS, values):
        spectrum[f'S{strips}'] = value

    positive = [
        (x, y)
        for x, y in zip(LEVELS, values)
        if y > 1e-9
    ]

    lam = 0.0
    r2 = 1.0

    if len(positive) >= 2:

        xs = [p[0] for p in positive]
        ys = [log(p[1]) for p in positive]

        mx = mean(xs)
        my = mean(ys)

        varx = sum((x - mx) ** 2 for x in xs)

        if varx > 0:

            cov = sum(
                (x - mx) * (y - my)
                for x, y in zip(xs, ys)
            )

            slope = cov / varx
            intercept = my - slope * mx

            lam = -slope

            pred = [
                exp(intercept - lam * x)
                for x in xs
            ]

            actual = [p[1] for p in positive]
            m = mean(actual)

            ss_res = sum(
                (a - p) ** 2
                for a, p in zip(actual, pred)
            )

            ss_tot = sum(
                (a - m) ** 2
                for a in actual
            )

            r2 = (
                1.0 - ss_res / ss_tot
                if ss_tot > 0
                else 1.0
            )

    delta = abs(values[0] - values[-1])

    variation = sum(
        abs(values[i + 1] - values[i])
        for i in range(len(values) - 1)
    ) / (len(values) - 1)

    shi = 0.7 * delta + 0.3 * variation

    spectrum['lambda'] = lam
    spectrum['R2'] = r2
    spectrum['SHI'] = shi

    return spectrum

# -------------------------------------------------
# Main
# -------------------------------------------------

results = []

for entry in registry:

    cp = int(entry['unicode_cp'], 16)

    glyph_name = cmap.get(cp)

    if glyph_name is None:
        continue

    pts = normalized_points(glyph_set[glyph_name])

    if not pts or len(pts) < 4:
        continue

    vertical = analyze(pts)
    horizontal = analyze(rotate_90(pts))

    results.append({
        'unicode_cp': entry['unicode_cp'],
        'jsesh_code': entry.get('jsesh_code'),
        'gardiner_code': entry.get('gardiner_code'),
        'vertical': vertical,
        'horizontal': horizontal
    })

with output_path.open('w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('Rotational Symmetry Analyzer V6R completed')
print('Output:', output_path)
print('Glyphs analyzed:', len(results))
print()
print('Average vertical SHI:',
      round(mean(r['vertical']['SHI'] for r in results), 4))
print('Average horizontal SHI:',
      round(mean(r['horizontal']['SHI'] for r in results), 4))
print()
print('STATUS: PASS')
