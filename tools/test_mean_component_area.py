"""
AncientScriptLab

Unit Test

Mean Component Area

T-008
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.mean_component_area import ALGORITHM


def main() -> None:

    print("=" * 72)
    print("Mean Component Area Unit Test")
    print("=" * 72)
    print()

    #
    # Two connected components:
    #
    # Component A : 4×4 = 16 pixels
    # Component B : 8×8 = 64 pixels
    #
    # Mean area = (16 + 64) / 2 = 40 pixels
    #

    image = np.full((30, 30), 255, dtype=np.uint8)

    # Small component
    image[2:6, 2:6] = 0

    # Large component
    image[12:20, 12:20] = 0

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)

    expected = 40.0

    print(f"Computed mean area : {value:.6f}")
    print(f"Expected mean area : {expected:.6f}")
    print()

    assert abs(value - expected) < 1e-9, (
        f"Expected {expected}, got {value}"
    )
    print("Unit test : PASSED")


if __name__ == "__main__":
    main()
