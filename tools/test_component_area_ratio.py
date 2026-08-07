"""
AncientScriptLab

Unit Test

Component Area Ratio

T-005
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.component_area_ratio import ALGORITHM


def main() -> None:

    print("=" * 72)
    print("Component Area Ratio Unit Test")
    print("=" * 72)
    print()

    #
    # Two connected components:
    #
    # Component A : 4×4 = 16 pixels
    # Component B : 8×8 = 64 pixels
    #
    # Total foreground = 80 pixels
    #
    # Expected ratio:
    #
    # 64 / 80 = 0.8
    #

    image = np.zeros((30, 30), dtype=np.uint8)

    # Small component
    image[2:6, 2:6] = 255

    # Large component
    image[12:20, 12:20] = 255

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)

    expected = 0.8

    print(f"Computed ratio : {value:.6f}")
    print(f"Expected ratio : {expected:.6f}")
    print()

    if abs(value - expected) < 1e-9:
        print("Unit test : PASSED")
    else:
        print("Unit test : FAILED")


if __name__ == "__main__":
    main()