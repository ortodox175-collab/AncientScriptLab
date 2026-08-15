"""
AncientScriptLab

Topology Algorithm

Foreground Density

Computes foreground-area density relative to image area.
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import (
    foreground_area,
    image_area,
)


def execute(context) -> float:
    """
    Density = canonical_foreground_area / image_area
    """

    area = image_area(context)

    if area == 0:
        return 0.0

    return float(foreground_area(context) / area)


ALGORITHM = Algorithm(
    name="topology.foreground_density",
    title="Foreground Density",
    version="2.1",
    author="AncientScriptLab",
    features=("T-022",),
    implementation=execute,
    dependencies=(),
    complexity="O(N)",
    deterministic=True,
    reference="Canonical foreground-area density relative to image area",
)
