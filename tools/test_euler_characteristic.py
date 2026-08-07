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

    # Binary image:
    #
    # ############
    # #          #
    # #          #
    # #          #
    # ############
    #
    # One connected component
    # One hole
    #
    # Euler characteristic = 1 − 1 = 0

    image = np.zeros((20, 20), dtype=np.uint8)

    image[2:18, 2:18] = 255
    image[6:14, 6:14] = 0

    context = FeatureContext(image)

    value = ALGORITHM.execute(context)

    expected = 0.0

    print(f"Computed Euler characteristic : {value:.6f}")
    print(f"Expected Euler characteristic : {expected:.6f}")
    print()

    if abs(value - expected) < 1e-9:
        print("Unit test : PASSED")
    else:
        print("Unit test : FAILED")


if __name__ == "__main__":
    main()