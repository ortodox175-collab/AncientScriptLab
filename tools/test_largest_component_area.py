"""
AncientScriptLab

Unit Test

Largest Component Area

T-004
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.largest_component_area import ALGORITHM


def main() -> None:

    print("=" * 72)
    print("Largest Component Area Unit Test")
    print("=" * 72)
    print()

    #
    # Image contains two connected components:
    #
    # Component A : 4×4 = 16 pixels
    # Component B : 8×8 = 64 pixels
    #
    # Expected largest area = 64
    #

    image = np.zeros((30, 30), dtype=np.uint8)

    # Small component
    image[2:6, 2:6] = 255

    # Large component
    image[12:20, 12:20] = 255

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)

    expected = 64.0

    print(f"Computed largest area : {value:.6f}")
    print(f"Expected largest area : {expected:.6f}")
    print()

    if abs(value - expected) < 1e-9:
        print("Unit test : PASSED")
    else:
        print("Unit test : FAILED")


if __name__ == "__main__":
    main()