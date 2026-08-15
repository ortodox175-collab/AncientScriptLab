"""
AncientScriptLab

Pipeline Integration Test

Component Density

T-021
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry


def main() -> None:

    print("=" * 72)
    print("Component Density Pipeline Integration Test")
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

    image = np.full((20, 20), 255, dtype=np.uint8)

    image[2:4, 2:4] = 0
    image[10:14, 10:14] = 0

    context = FeatureContext(image)

    registry = RuntimeRegistry()

    engine = ExecutionEngine(registry)

    value = engine.compute(
        "topology.component_density",
        context,
    )

    expected = 2.0 / 400.0

    print(f"Computed density : {value:.6f}")
    print(f"Expected density : {expected:.6f}")
    print()

    assert abs(value - expected) < 1e-9, (
        f"Expected {expected}, got {value}"
    )
    print("Pipeline test : PASSED")


if __name__ == "__main__":
    main()
