"""
AncientScriptLab

Normalization

Center by Mass

Level A (Safe)

Moves the symbol so that its centroid
is located at the image center.
"""

from __future__ import annotations

import cv2
import numpy as np


def center_of_mass(image: np.ndarray) -> np.ndarray:

    moments = cv2.moments(image, binaryImage=True)

    if moments["m00"] == 0:
        return image.copy()

    cx = moments["m10"] / moments["m00"]
    cy = moments["m01"] / moments["m00"]

    height, width = image.shape

    target_x = (width - 1) / 2.0
    target_y = (height - 1) / 2.0

    dx = target_x - cx
    dy = target_y - cy

    matrix = np.float32([
        [1, 0, dx],
        [0, 1, dy],
    ])

    return cv2.warpAffine(
        image,
        matrix,
        (width, height),
        flags=cv2.INTER_NEAREST,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )

