from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import connected_component_areas


def execute(context) -> float:
    areas = connected_component_areas(context)
    return float(sum(areas) / len(areas)) if areas else 0.0


ALGORITHM = Algorithm(
    name="topology.mean_component_area",
    title="Mean Component Area",
    version="2.0",
    author="AncientScriptLab",
    features=("T-008",),
    implementation=execute,
    dependencies=("topology.connected_components",),
    complexity="O(N)",
    deterministic=True,
    reference="Mean area of all connected components",
)
