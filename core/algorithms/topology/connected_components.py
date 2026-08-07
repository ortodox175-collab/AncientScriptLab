"""
AncientScriptLab

Topology Algorithm

Connected Components

Topology Refactor v2.0
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import connected_component_areas


def execute(context) -> float:
    """
    Number of connected foreground components.
    """

    return float(len(connected_component_areas(context)))


ALGORITHM = Algorithm(
    name="topology.connected_components",
    title="Connected Components",
    version="2.0",
    author="AncientScriptLab",
    features=("T-001",),
    implementation=execute,
    dependencies=(),
    complexity="O(N)",
    deterministic=True,
    reference="Connected-component count of binary foreground",
)
