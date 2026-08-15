"""
AncientScriptLab

Pipeline Integration Test

Total Foreground Area

T-006
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry


def main() -> None:

    print("=" * 72)
    print("Total Foreground Area Pipeline Integration Test")
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

    image = np.full((30, 30), 255, dtype=np.uint8)

    # Small component
    image[2:6, 2:6] = 0

    # Large component
    image[12:20, 12:20] = 0

    context = FeatureContext(image)

    registry = RuntimeRegistry()

    engine = ExecutionEngine(registry)

    value = engine.compute(
        "topology.total_foreground_area",
        context,
    )

    expected = 80.0

    print(f"Computed area : {value:.6f}")
    print(f"Expected area : {expected:.6f}")
    print()

    assert abs(value - expected) < 1e-9, (
        f"Expected {expected}, got {value}"
    )
    print("Pipeline test : PASSED")


if __name__ == "__main__":
    main()
