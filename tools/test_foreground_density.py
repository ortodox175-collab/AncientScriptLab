"""
AncientScriptLab

Unit Test

Foreground Density

T-022
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.foreground_density import ALGORITHM


def main() -> None:

    print("=" * 72)
    print("Foreground Density Unit Test")
    print("=" * 72)
    print()

    #
    # Image size:
    # 20 × 20 = 400 pixels
    #
    # Foreground pixels:
    # 4 + 16 = 20 pixels
    #
    # Density = 20 / 400 = 0.05
    #

    image = np.zeros((20, 20), dtype=np.uint8)

    image[2:4, 2:4] = 255
    image[10:14, 10:14] = 255

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)

    expected = 20.0 / 400.0

    print(f"Computed density : {value:.6f}")
    print(f"Expected density : {expected:.6f}")
    print()

    if abs(value - expected) < 1e-9:
        print("Unit test : PASSED")
    else:
        print("Unit test : FAILED")


if __name__ == "__main__":
    main()