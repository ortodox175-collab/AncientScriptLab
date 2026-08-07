"""
AncientScriptLab

Topology Algorithm

Total Foreground Area

Topology Refactor v2.0
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import foreground_area


def execute(context) -> float:
    """
    Total foreground area in pixels.
    """

    return float(foreground_area(context))


ALGORITHM = Algorithm(
    name="topology.total_foreground_area",
    title="Total Foreground Area",
    version="2.0",
    author="AncientScriptLab",
    features=("T-006",),
    implementation=execute,
    dependencies=(),
    complexity="O(N)",
    deterministic=True,
    reference="Total number of foreground pixels",
)
