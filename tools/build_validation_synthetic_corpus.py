from pathlib import Path
import json
from PIL import Image, ImageDraw

SIZE = 64
OUT = Path("validation/synthetic/images")
OUT.mkdir(parents=True, exist_ok=True)

metadata = {}

def save(name, draw_fn, truth):
    img = Image.new("L", (SIZE, SIZE), 255)
    d = ImageDraw.Draw(img)
    draw_fn(d)
    img.save(OUT / f"{name}.png")
    metadata[name] = truth

# 1. Single square
save(
    "single_square",
    lambda d: d.rectangle((16,16,47,47), fill=0),
    {"connected_components":1,"hole_count":0,"euler_characteristic":1}
)

# 2. Two squares
save(
    "two_squares",
    lambda d: (
        d.rectangle((8,16,23,31), fill=0),
        d.rectangle((40,32,55,47), fill=0)
    ),
    {"connected_components":2,"hole_count":0,"euler_characteristic":2}
)

# 3. Three squares
save(
    "three_squares",
    lambda d: (
        d.rectangle((6,10,18,22), fill=0),
        d.rectangle((26,26,38,38), fill=0),
        d.rectangle((46,42,58,54), fill=0)
    ),
    {"connected_components":3,"hole_count":0,"euler_characteristic":3}
)

# 4. Square with hole
save(
    "square_with_hole",
    lambda d: (
        d.rectangle((12,12,51,51), fill=0),
        d.rectangle((24,24,39,39), fill=255)
    ),
    {"connected_components":1,"hole_count":1,"euler_characteristic":0}
)

# 5. Ring
save(
    "ring",
    lambda d: (
        d.ellipse((12,12,51,51), fill=0),
        d.ellipse((22,22,41,41), fill=255)
    ),
    {"connected_components":1,"hole_count":1,"euler_characteristic":0}
)

# 6. Three rings
save(
    "three_rings",
    lambda d: (
        d.ellipse((4,18,20,34), fill=0),
        d.ellipse((8,22,16,30), fill=255),
        d.ellipse((24,18,40,34), fill=0),
        d.ellipse((28,22,36,30), fill=255),
        d.ellipse((44,18,60,34), fill=0),
        d.ellipse((48,22,56,30), fill=255)
    ),
    {"connected_components":3,"hole_count":3,"euler_characteristic":0}
)

with open("validation/synthetic/metadata.json","w") as f:
    json.dump(metadata,f,indent=2)

print(f"Synthetic validation corpus generated: {len(metadata)} images")
