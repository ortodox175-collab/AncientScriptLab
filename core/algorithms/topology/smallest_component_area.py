from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import connected_component_areas


def execute(context) -> float:
    areas = connected_component_areas(context)
    return float(min(areas)) if areas else 0.0


ALGORITHM = Algorithm(
    name="topology.smallest_component_area",
    title="Smallest Component Area",
    version="2.0",
    author="AncientScriptLab",
    features=("T-007",),
    implementation=execute,
    dependencies=("topology.connected_components",),
    complexity="O(N)",
    deterministic=True,
    reference="Area of the smallest connected component",
)
