"""
AncientScriptLab

Algorithm

geometry.perimeter

Feature:
G-005 Perimeter
"""

from __future__ import annotations

import cv2

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

    perimeter = 0.0

    for contour in contours:
        perimeter = max(
            perimeter,
            cv2.arcLength(contour, True),
        )

    return float(perimeter)


ALGORITHM = Algorithm(
    name="geometry.perimeter",
    title="Perimeter",
    version="1.0",
    author="AncientScriptLab",
    features=("G-005",),
    implementation=execute,
    dependencies=(),
    complexity="O(n)",
    deterministic=True,
    reference="OpenCV arcLength",
)

