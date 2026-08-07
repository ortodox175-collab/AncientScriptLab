"""
AncientScriptLab

Pipeline Integration Test

Largest Component Area

T-004
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry


def main() -> None:

    print("=" * 72)
    print("Largest Component Area Pipeline Integration Test")
    print("=" * 72)
    print()

    #
    # Two connected components:
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

    registry = RuntimeRegistry()

    engine = ExecutionEngine(registry)

    value = engine.compute(
        "topology.largest_component_area",
        context,
    )

    expected = 64.0

    print(f"Computed largest area : {value:.6f}")
    print(f"Expected largest area : {expected:.6f}")
    print()

    if abs(value - expected) < 1e-9:
        print("Pipeline test : PASSED")
    else:
        print("Pipeline test : FAILED")


if __name__ == "__main__":
    main()