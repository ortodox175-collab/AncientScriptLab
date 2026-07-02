"""
AncientScriptLab

Algorithm

geometry.bounding_box.area
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.features.geometry.bounding_box import BoundingBoxFeatures


def execute(context):

    width = BoundingBoxFeatures.feature_g001(context)
    height = BoundingBoxFeatures.feature_g002(context)

    return width * height


ALGORITHM = Algorithm(
    name="geometry.bounding_box.area",
    title="Bounding Box Area",
    version="1.0",
    author="AncientScriptLab",
    features=("G-003",),
    implementation=execute,
    dependencies=(
        "geometry.bounding_box.width",
        "geometry.bounding_box.height",
    ),
    complexity="O(1)",
    deterministic=True,
    reference="AncientScriptLab Geometry",
)
