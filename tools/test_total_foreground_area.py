"""
AncientScriptLab

Unit Test

Total Foreground Area

T-006
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.total_foreground_area import ALGORITHM


def main() -> None:

    print("=" * 72)
    print("Total Foreground Area Unit Test")
    print("=" * 72)
    print()

    #
    # Two connected components:
    #
    # Component A : 4×4 = 16 pixels
    # Component B : 8×8 = 64 pixels
    #
    # Total foreground area = 80 pixels
    #

    image = np.zeros((30, 30), dtype=np.uint8)

    # Small component
    image[2:6, 2:6] = 255

    # Large component
    image[12:20, 12:20] = 255

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)

    expected = 80.0

    print(f"Computed area : {value:.6f}")
    print(f"Expected area : {expected:.6f}")
    print()

    if abs(value - expected) < 1e-9:
        print("Unit test : PASSED")
    else:
        print("Unit test : FAILED")


if __name__ == "__main__":
    main()