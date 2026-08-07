"""
AncientScriptLab

M7

Topology Pipeline Integration Test

T-002 Hole Count
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry


EXPECTED = 1.0
EPSILON = 1e-9


def create_test_image() -> np.ndarray:

    image = np.zeros((11, 11), dtype=np.uint8)

    image[2:9, 2:9] = 255
    image[4:7, 4:7] = 0

    return image


def main() -> None:

    print("=" * 72)
    print("Hole Count Pipeline Integration Test")
    print("=" * 72)
    print()

    image = create_test_image()

    context = FeatureContext(image)

    registry = RuntimeRegistry()
    engine = ExecutionEngine(registry)

    value = engine.compute(
        "topology.hole_count",
        context,
    )

    print(f"Computed holes : {value:.6f}")
    print(f"Expected holes : {EXPECTED:.6f}")
    print()

    assert abs(value - EXPECTED) < EPSILON, (
        f"Expected {EXPECTED}, got {value}"
    )

    print("Pipeline test : PASSED")


if __name__ == "__main__":
    main()