"""
AncientScriptLab

Algorithm

geometry.bounding_box.width
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.features.geometry.bounding_box import BoundingBoxFeatures


def execute(context):

    return BoundingBoxFeatures.feature_g001(
        context
    )


ALGORITHM = Algorithm(
    name="geometry.bounding_box.width",

    title="Bounding Box Width",

    version="1.0",

    author="AncientScriptLab",

    features=("G-001",),

    dependencies=(),

    complexity="O(n)",

    deterministic=True,

    reference="AncientScriptLab Geometry",

    implementation=execute,
)
