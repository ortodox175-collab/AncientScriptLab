from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

OUT = Path('datasets/egyptian/images')
META = Path('datasets/egyptian/metadata')

OUT.mkdir(parents=True, exist_ok=True)
META.mkdir(parents=True, exist_ok=True)

FONT_NAME = 'NotoSansEgyptianHieroglyphs-Regular.ttf'
SIZE = 56

font = ImageFont.truetype(FONT_NAME, SIZE)

metadata = []
count = 0

for code in range(0x13000, 0x1342F + 1):
    ch = chr(code)

    img = Image.new('L', (64, 64), 255)
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0, 0), ch, font=font)

    if bbox is None:
        continue

    x0, y0, x1, y1 = bbox
    w = x1 - x0
    h = y1 - y0

    if w == 0 or h == 0:
        continue

    x = (64 - w) // 2 - x0
    y = (64 - h) // 2 - y0

    draw.text((x, y), ch, font=font, fill=0)

    img.save(OUT / f'hiero_{count:04d}.png')

    metadata.append(
        {
            'id': count,
            'unicode': f'U+{code:05X}',
            'character': ch,
        }
    )

    count += 1

(META / 'gardiner_metadata.json').write_text(
    json.dumps(metadata, indent=2, ensure_ascii=False),
    encoding='utf-8',
)

print(f'Generated signs: {count}')
