"""
AncientScriptLab

Algorithm

geometry.compactness

Feature

G-010 Compactness
"""

from __future__ import annotations

import cv2
import math

from core.execution.algorithm import Algorithm


def execute(context):

    image = context.image

    contours, _ = cv2.findContours(
        image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE,
    )

    if len(contours) == 0:
        return 0.0

    contour = max(contours, key=cv2.contourArea)

    area = cv2.contourArea(contour)

    perimeter = cv2.arcLength(contour, True)

    if perimeter == 0:
        return 0.0

    return float(
        (4.0 * math.pi * area) /
        (perimeter * perimeter)
    )


ALGORITHM = Algorithm(
    name="geometry.compactness",
    title="Compactness",
    version="1.0",
    author="AncientScriptLab",
    features=("G-010",),
    implementation=execute,
    dependencies=(),
    complexity="O(n)",
    deterministic=True,
    reference="4πA/P²",
)

