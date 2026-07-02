"""
AncientScriptLab

Algorithm

geometry.centroid_y

Feature

G-009 Centroid Y
"""

from __future__ import annotations

import cv2

from core.execution.algorithm import Algorithm


def execute(context):

    moments = cv2.moments(context.image, binaryImage=True)

    if moments["m00"] == 0:
        return 0.0

    return float(moments["m01"] / moments["m00"])


ALGORITHM = Algorithm(
    name="geometry.centroid_y",
    title="Centroid Y",
    version="1.0",
    author="AncientScriptLab",
    features=("G-009",),
    implementation=execute,
    dependencies=(),
    complexity="O(n)",
    deterministic=True,
    reference="Image Moments",
)

