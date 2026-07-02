"""
AncientScriptLab

Execution Engine Integration Test
"""

import numpy as np

from core.context.feature_context import FeatureContext

from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine

from core.algorithms.geometry.bounding_box_width import ALGORITHM


def main():

    image = np.zeros((100, 100), dtype=np.uint8)

    image[30:70, 20:60] = 255

    context = FeatureContext(image)

    registry = RuntimeRegistry()

    registry.register(ALGORITHM)

    engine = ExecutionEngine(registry)

    result = engine.compute(
        "geometry.bounding_box.width",
        context,
    )

    print()

    print("===================================")
    print("Execution Engine Test")
    print("===================================")

    print()

    print("Algorithm :", ALGORITHM.name)
    print("Result    :", result)

    assert result == 40.0

    print()

    print("TEST PASSED")


if __name__ == "__main__":

    main()
