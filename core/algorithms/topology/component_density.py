from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import (
    connected_component_areas,
    image_area,
)


def execute(context) -> float:
    area = image_area(context)

    if area == 0:
        return 0.0

    components = len(connected_component_areas(context))

    return float(components) / float(area)


ALGORITHM = Algorithm(
    name="topology.component_density",
    title="Component Density",
    version="2.0",
    author="AncientScriptLab",
    features=("T-021",),
    implementation=execute,
    dependencies=("topology.connected_components",),
    complexity="O(N)",
    deterministic=True,
    reference="Connected-component density relative to image area",
)
