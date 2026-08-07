"""
AncientScriptLab

Topology Algorithm

Euler Characteristic

M7

Euler = connected_components - hole_count

This implementation delegates both measurements to the
validated topology algorithms to guarantee scientific consistency.
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology.connected_components import execute as connected_components_execute
from core.algorithms.topology.hole_count import execute as hole_count_execute


def execute(context) -> float:
    connected_components = connected_components_execute(context)
    hole_count = hole_count_execute(context)
    return float(connected_components - hole_count)


ALGORITHM = Algorithm(
    name="topology.euler_characteristic",
    title="Euler Characteristic",
    version="1.3",
    author="AncientScriptLab",
    features=("T-003",),
    implementation=execute,
    dependencies=(
        "topology.connected_components",
        "topology.hole_count",
    ),
    complexity="O(N)",
    deterministic=True,
    reference="Euler characteristic = connected components - holes",
)
