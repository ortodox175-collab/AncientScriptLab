"""
AncientScriptLab

M7

Unit Test

T-002 Hole Count
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.hole_count import execute


EXPECTED = 1.0
EPSILON = 1e-9


def create_test_image() -> np.ndarray:
    """
    Create a binary image containing exactly one hole.
    """

    image = np.zeros((11, 11), dtype=np.uint8)

    # Filled square
    image[2:9, 2:9] = 255

    # Central hole
    image[4:7, 4:7] = 0

    return image


def main() -> None:

    print("=" * 72)
    print("Hole Count Unit Test")
    print("=" * 72)
    print()

    image = create_test_image()

    context = FeatureContext(image)

    value = execute(context)

    print(f"Computed holes : {value:.6f}")
    print(f"Expected holes : {EXPECTED:.6f}")
    print()

    assert abs(value - EXPECTED) < EPSILON, (
        f"Expected {EXPECTED}, got {value}"
    )

    print("Unit test : PASSED")


if __name__ == "__main__":
    main()