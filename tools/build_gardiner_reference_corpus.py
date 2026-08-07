from pathlib import Path
import json
import time
import cv2
import numpy as np
import requests

RAW = Path('datasets/egyptian/raw')
OUT = Path('datasets/egyptian/images')
META = Path('datasets/egyptian/metadata')

RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
META.mkdir(parents=True, exist_ok=True)

HEADERS = {'User-Agent': 'AncientScriptLab/1.0'}

# первые 200 Unicode Egyptian Hieroglyphs
BASE = 'https://commons.wikimedia.org/wiki/Special:FilePath/'

metadata = []
count = 0

for code in range(0x13000, 0x130C8):   # 200 знаков
    name = f'Egyptian_hieroglyph_{code:05X}.svg'
    url = BASE + name

    try:
        r = requests.get(url, headers=HEADERS, timeout=30)

        if r.status_code != 200:
            time.sleep(0.5)
            continue

        svg_path = RAW / f'{count:04d}.svg'
        svg_path.write_bytes(r.content)

        png_path = RAW / f'{count:04d}.png'

        # если rsvg-convert не установлен, пропускаем
        import subprocess
        res = subprocess.run(
            ['rsvg-convert', '-w', '256', '-h', '256',
             str(svg_path), '-o', str(png_path)],
            capture_output=True
        )

        if res.returncode != 0:
            continue

        img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        _, binary = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY_INV)

        coords = cv2.findNonZero(binary)

        if coords is None:
            continue

        x, y, w, h = cv2.boundingRect(coords)

        crop = binary[y:y+h, x:x+w]

        canvas = np.zeros((64, 64), np.uint8)

        scale = min(56 / w, 56 / h)

        nw = max(1, int(w * scale))
        nh = max(1, int(h * scale))

        resized = cv2.resize(
            crop,
            (nw, nh),
            interpolation=cv2.INTER_NEAREST,
        )

        ox = (64 - nw) // 2
        oy = (64 - nh) // 2

        canvas[oy:oy+nh, ox:ox+nw] = resized

        final = 255 - canvas

        out_path = OUT / f'hiero_{count:04d}.png'

        cv2.imwrite(str(out_path), final)

        metadata.append(
            {
                'id': count,
                'unicode': f'U+{code:05X}',
                'source': url,
            }
        )

        count += 1

        print(f'[{count}] U+{code:05X}')

        time.sleep(0.5)

    except Exception:
        time.sleep(0.5)
        continue

(META / 'gardiner_metadata.json').write_text(
    json.dumps(metadata, indent=2),
    encoding='utf-8',
)

print()
print('=' * 60)
print(f'Prepared signs: {count}')
print('=' * 60)
