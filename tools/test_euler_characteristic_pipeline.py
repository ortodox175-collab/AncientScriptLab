"""
AncientScriptLab

Pipeline Integration Test

Euler Characteristic

T-003
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry


def main() -> None:
    print("=" * 72)
    print("Euler Characteristic Pipeline Integration Test")
    print("=" * 72)
    print()

    # Canonical image convention:
    # background = 255
    # foreground = 0
    #
    # One component with one enclosed hole:
    # Euler = 1 - 1 = 0

    image = np.full((20, 20), 255, dtype=np.uint8)

    image[2:18, 2:18] = 0
    image[6:14, 6:14] = 255

    context = FeatureContext(image)

    registry = RuntimeRegistry()
    engine = ExecutionEngine(registry)

    value = engine.compute(
        "topology.euler_characteristic",
        context,
    )

    expected = 0.0

    print(f"Computed Euler characteristic : {value:.6f}")
    print(f"Expected Euler characteristic : {expected:.6f}")
    print()

    assert abs(value - expected) < 1e-9, (
        f"Expected {expected}, got {value}"
    )

    print("Pipeline test : PASSED")


if __name__ == "__main__":
    main()
