"""
AncientScriptLab

Execution Engine Integration Test

Tests canonical pack-based RuntimeRegistry.
"""

import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine


def main():
    # Canonical image convention:
    # background = white
    # foreground sign = black
    image = np.full((100, 100), 255, dtype=np.uint8)
    image[30:70, 20:60] = 0

    context = FeatureContext(image)

    registry = RuntimeRegistry()
    engine = ExecutionEngine(registry)

    result = engine.compute(
        "geometry.bounding_box.width",
        context,
    )

    assert result == 40.0

    assert "geometry" in registry.list_packs()
    assert "bounding_box.width" in registry.list_features("geometry")

    print("EXECUTION ENGINE PACK REGISTRY: PASS")


if __name__ == "__main__":
    main()
