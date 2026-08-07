"""
AncientScriptLab

M7

Topology Pipeline Integration Test

Purpose
-------
Verifies the complete execution pipeline:

FeatureContext
    ↓
ExecutionEngine
    ↓
RuntimeRegistry
    ↓
TopologyPack
    ↓
Connected Components
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry


EXPECTED_COMPONENTS = 2.0
EPSILON = 1e-9


def main() -> None:

    print("=" * 72)
    print("Topology Pipeline Integration Test")
    print("=" * 72)
    print()

    image = np.zeros((10, 10), dtype=np.uint8)

    # First component
    image[1:4, 1:4] = 255

    # Second component
    image[6:9, 6:9] = 255

    context = FeatureContext(image)

    registry = RuntimeRegistry()

    engine = ExecutionEngine(registry)

    value = engine.compute(
        "topology.connected_components",
        context,
    )

    print(f"Computed connected components : {value:.6f}")
    print(f"Expected connected components : {EXPECTED_COMPONENTS:.6f}")
    print()

    assert abs(value - EXPECTED_COMPONENTS) < EPSILON, (
        f"Expected {EXPECTED_COMPONENTS}, got {value}"
    )

    print("Pipeline status : PASSED")


if __name__ == "__main__":
    main()