import numpy as np

from core.context.feature_context import FeatureContext

from core.algorithms.topology.connected_components import execute as C
from core.algorithms.topology.hole_count import execute as H
from core.algorithms.topology.euler_characteristic import execute as E
from core.algorithms.topology.total_foreground_area import execute as FG
from core.algorithms.topology.largest_component_area import execute as LARGEST
from core.algorithms.topology.smallest_component_area import execute as SMALLEST
from core.algorithms.topology.mean_component_area import execute as MEAN
from core.algorithms.topology.component_area_ratio import execute as RATIO
from core.algorithms.topology.component_density import execute as CDENS
from core.algorithms.topology.foreground_density import execute as FDENS


def ctx(img):
    return FeatureContext(img)


def check(name, image, expected):
    x = ctx(image)

    actual = {
        "C": C(x),
        "H": H(x),
        "E": E(x),
        "FG": FG(x),
        "largest": LARGEST(x),
        "smallest": SMALLEST(x),
        "mean": MEAN(x),
        "ratio": RATIO(x),
        "component_density": CDENS(x),
        "foreground_density": FDENS(x),
    }

    for key, value in expected.items():
        assert abs(actual[key] - value) < 1e-12, (
            f"{name}: {key}: expected {value}, got {actual[key]}"
        )

    # Cross-algorithm consistency
    assert actual["E"] == actual["C"] - actual["H"]

    if actual["C"] > 0:
        assert actual["smallest"] <= actual["mean"] <= actual["largest"]
        assert actual["largest"] <= actual["FG"]

    print(f"PASS  {name}")


# --------------------------------------------------
# 1. Blank image
# --------------------------------------------------

img = np.full((7, 7), 255, dtype=np.uint8)

check("blank", img, {
    "C": 0,
    "H": 0,
    "E": 0,
    "FG": 0,
    "largest": 0,
    "smallest": 0,
    "mean": 0,
    "ratio": 0,
    "component_density": 0,
    "foreground_density": 0,
})


# --------------------------------------------------
# 2. Solid 3x3 component
# --------------------------------------------------

img = np.full((7, 7), 255, dtype=np.uint8)
img[2:5, 2:5] = 0

check("solid", img, {
    "C": 1,
    "H": 0,
    "E": 1,
    "FG": 9,
    "largest": 9,
    "smallest": 9,
    "mean": 9,
    "ratio": 1,
    "component_density": 1 / 49,
    "foreground_density": 9 / 49,
})


# --------------------------------------------------
# 3. Two disconnected components: areas 4 and 1
# --------------------------------------------------

img = np.full((7, 7), 255, dtype=np.uint8)
img[1:3, 1:3] = 0
img[5, 5] = 0

check("two_components", img, {
    "C": 2,
    "H": 0,
    "E": 2,
    "FG": 5,
    "largest": 4,
    "smallest": 1,
    "mean": 2.5,
    "ratio": 4 / 5,
    "component_density": 2 / 49,
    "foreground_density": 5 / 49,
})


# --------------------------------------------------
# 4. Square ring: one component, one hole
# --------------------------------------------------

img = np.full((7, 7), 255, dtype=np.uint8)
img[1:6, 1:6] = 0
img[2:5, 2:5] = 255

check("one_hole", img, {
    "C": 1,
    "H": 1,
    "E": 0,
    "FG": 16,
    "largest": 16,
    "smallest": 16,
    "mean": 16,
    "ratio": 1,
    "component_density": 1 / 49,
    "foreground_density": 16 / 49,
})


# --------------------------------------------------
# 5. Diagonal contact
# Foreground connectivity=8 => one component
# --------------------------------------------------

img = np.full((7, 7), 255, dtype=np.uint8)
img[2, 2] = 0
img[3, 3] = 0

check("diagonal_contact", img, {
    "C": 1,
    "H": 0,
    "E": 1,
    "FG": 2,
    "largest": 2,
    "smallest": 2,
    "mean": 2,
    "ratio": 1,
    "component_density": 1 / 49,
    "foreground_density": 2 / 49,
})


# --------------------------------------------------
# 6. One component containing two independent holes
# --------------------------------------------------

img = np.full((9, 11), 255, dtype=np.uint8)
img[1:8, 1:10] = 0
img[3, 3] = 255
img[3, 7] = 255

check("two_holes", img, {
    "C": 1,
    "H": 2,
    "E": -1,
    "FG": 61,
    "largest": 61,
    "smallest": 61,
    "mean": 61,
    "ratio": 1,
    "component_density": 1 / 99,
    "foreground_density": 61 / 99,
})

print()
print("TOPOLOGY SYNTHETIC GROUND TRUTH: PASS")
