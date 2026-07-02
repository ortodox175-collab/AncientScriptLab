"""
AncientScriptLab

Algorithm

geometry.aspect_ratio

Feature

G-006 Aspect Ratio
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm


def execute(context):

    bbox = context.bounding_box

    if bbox.height == 0:
        return 0.0

    return float(bbox.width / bbox.height)


ALGORITHM = Algorithm(
    name="geometry.aspect_ratio",
    title="Aspect Ratio",
    version="1.0",
    author="AncientScriptLab",
    features=("G-006",),
    implementation=execute,
    dependencies=(),
    complexity="O(1)",
    deterministic=True,
    reference="Bounding Box Aspect Ratio",
)

