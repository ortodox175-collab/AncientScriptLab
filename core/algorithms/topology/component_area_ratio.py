from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import (
    connected_component_areas,
    foreground_area,
)


def execute(context) -> float:
    total = foreground_area(context)

    if total == 0:
        return 0.0

    areas = connected_component_areas(context)

    if not areas:
        return 0.0

    return float(max(areas)) / float(total)


ALGORITHM = Algorithm(
    name="topology.component_area_ratio",
    title="Component Area Ratio",
    version="2.0",
    author="AncientScriptLab",
    features=("T-005",),
    implementation=execute,
    dependencies=(
        "topology.largest_component_area",
        "topology.total_foreground_area",
    ),
    complexity="O(N)",
    deterministic=True,
    reference="Largest component area divided by total foreground area",
)
