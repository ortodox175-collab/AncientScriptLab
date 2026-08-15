from __future__ import annotations

from core.execution.algorithm import Algorithm


def execute(context) -> float:
    """
    Bounding-box aspect ratio.

    aspect_ratio = width / height
    """

    bbox = context.bounding_box

    if bbox.height == 0:
        return 0.0

    return float(bbox.width / bbox.height)


ALGORITHM = Algorithm(
    name="geometry.aspect_ratio",
    title="Aspect Ratio",
    version="2.0",
    author="AncientScriptLab",
    features=("G-006",),
    implementation=execute,
    dependencies=(),
    complexity="O(1)",
    deterministic=True,
    reference="Foreground bounding-box width divided by height",
)
