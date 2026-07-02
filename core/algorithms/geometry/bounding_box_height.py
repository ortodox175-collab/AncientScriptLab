"""
AncientScriptLab

Algorithm

geometry.bounding_box.height

Feature

G-002 Bounding Box Height
"""

from __future__ import annotations

from core.execution.algorithm import Algorithm
from core.features.geometry.bounding_box import BoundingBoxFeatures


def execute(context):

    return BoundingBoxFeatures.feature_g002(context)


ALGORITHM = Algorithm(
    name="geometry.bounding_box.height",
    title="Bounding Box Height",
    version="1.0",
    author="AncientScriptLab",
    features=("G-002",),
    implementation=execute,
    dependencies=(),
    complexity="O(1)",
    deterministic=True,
    reference="Bounding Box Height",
)

