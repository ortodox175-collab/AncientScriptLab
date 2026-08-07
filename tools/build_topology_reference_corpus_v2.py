from pathlib import Path
import json
from PIL import Image, ImageDraw

SIZE = 64
OUT = Path("validation/reference_v2/images")
OUT.mkdir(parents=True, exist_ok=True)

metadata = {}

def save(name, draw_fn, truth):
    img = Image.new("L", (SIZE, SIZE), 255)
    d = ImageDraw.Draw(img)
    draw_fn(d)
    img.save(OUT / f"{name}.png")
    metadata[name] = truth

# 1 component
save(
    "square",
    lambda d: d.rectangle([16,16,48,48], fill=0),
    {"components":1,"holes":0,"euler":1},
)

# 2 components
save(
    "two_squares",
    lambda d: (
        d.rectangle([8,16,24,32], fill=0),
        d.rectangle([40,16,56,32], fill=0),
    ),
    {"components":2,"holes":0,"euler":2},
)

# 3 components
save(
    "three_squares",
    lambda d: (
        d.rectangle([4,16,16,28], fill=0),
        d.rectangle([26,16,38,28], fill=0),
        d.rectangle([48,16,60,28], fill=0),
    ),
    {"components":3,"holes":0,"euler":3},
)

# 1 hole
save(
    "ring",
    lambda d: (
        d.ellipse([12,12,52,52], fill=0),
        d.ellipse([22,22,42,42], fill=255),
    ),
    {"components":1,"holes":1,"euler":0},
)

# square with hole
save(
    "square_hole",
    lambda d: (
        d.rectangle([8,8,56,56], fill=0),
        d.rectangle([24,24,40,40], fill=255),
    ),
    {"components":1,"holes":1,"euler":0},
)

# 3 rings
def draw_three_rings(d):
    for x in [10,26,42]:
        d.ellipse([x,18,x+12,30], fill=0)
        d.ellipse([x+3,21,x+9,27], fill=255)

save(
    "three_rings",
    draw_three_rings,
    {"components":3,"holes":3,"euler":0},
)

# bridge
save(
    "bridge",
    lambda d: (
        d.rectangle([8,20,20,36], fill=0),
        d.rectangle([44,20,56,36], fill=0),
        d.rectangle([20,26,44,30], fill=0),
    ),
    {"components":1,"holes":0,"euler":1},
)

# diagonal contact
save(
    "diagonal_contact",
    lambda d: (
        d.rectangle([16,16,31,31], fill=0),
        d.rectangle([32,32,47,47], fill=0),
    ),
    {"components":1,"holes":0,"euler":1},
)

# nested rings
save(
    "nested_rings",
    lambda d: (
        d.ellipse([8,8,56,56], fill=0),
        d.ellipse([18,18,46,46], fill=255),
        d.ellipse([24,24,40,40], fill=0),
        d.ellipse([29,29,35,35], fill=255),
    ),
    {"components":1,"holes":2,"euler":-1},
)

with open("validation/reference_v2/metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Reference corpus v2 generated: {len(metadata)} images")
