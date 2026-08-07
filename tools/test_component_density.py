"""
AncientScriptLab

Unit Test

Component Density

T-021
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.component_density import ALGORITHM


def main() -> None:

    print("=" * 72)
    print("Component Density Unit Test")
    print("=" * 72)
    print()

    #
    # Image size:
    # 20 × 20 = 400 pixels
    #
    # Two connected components.
    #
    # Density = 2 / 400 = 0.005
    #

    image = np.zeros((20, 20), dtype=np.uint8)

    image[2:4, 2:4] = 255
    image[10:14, 10:14] = 255

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)

    expected = 2.0 / 400.0

    print(f"Computed density : {value:.6f}")
    print(f"Expected density : {expected:.6f}")
    print()

    if abs(value - expected) < 1e-9:
        print("Unit test : PASSED")
    else:
        print("Unit test : FAILED")


if __name__ == "__main__":
    main()