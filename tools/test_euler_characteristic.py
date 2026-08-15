"""
AncientScriptLab

Unit Test

Euler Characteristic

T-003
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.euler_characteristic import ALGORITHM


def main() -> None:
    print("=" * 72)
    print("Euler Characteristic Unit Test")
    print("=" * 72)
    print()

    # Canonical image convention:
    # background = 255
    # foreground = 0
    #
    # One foreground component with one enclosed hole.
    #
    # C = 1
    # H = 1
    # Euler = C - H = 0

    image = np.full((20, 20), 255, dtype=np.uint8)

    # Foreground body
    image[2:18, 2:18] = 0

    # Enclosed background hole
    image[6:14, 6:14] = 255

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)
    expected = 0.0

    print(f"Computed Euler characteristic : {value:.6f}")
    print(f"Expected Euler characteristic : {expected:.6f}")
    print()

    assert abs(value - expected) < 1e-9, (
        f"Expected {expected}, got {value}"
    )

    print("Unit test : PASSED")


if __name__ == "__main__":
    main()
