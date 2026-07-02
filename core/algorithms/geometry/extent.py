"""
AncientScriptLab

Algorithm

geometry.extent

Feature

G-007 Extent
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm


def execute(context):

    bbox = context.bounding_box

    bbox_area = bbox.width * bbox.height

    if bbox_area == 0:
        return 0.0

    foreground_area = float((context.image > 0).sum())

    return foreground_area / float(bbox_area)


ALGORITHM = Algorithm(
    name="geometry.extent",
    title="Extent",
    version="1.0",
    author="AncientScriptLab",
    features=("G-007",),
    implementation=execute,
    dependencies=(),
    complexity="O(n)",
    deterministic=True,
    reference="Foreground Area / Bounding Box Area",
)

