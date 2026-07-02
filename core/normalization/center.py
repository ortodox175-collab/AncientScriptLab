"""
AncientScriptLab

Normalization

Center Image

Level A (Safe)
"""

from __future__ import annotations

import cv2
import numpy as np


def center_image(image: np.ndarray) -> np.ndarray:

    points = cv2.findNonZero(image)

    if points is None:
        return image.copy()

    x, y, w, h = cv2.boundingRect(points)

    cropped = image[y:y+h, x:x+w]

    canvas = np.zeros_like(image)

    H, W = canvas.shape

    start_x = (W - w) // 2
    start_y = (H - h) // 2

    canvas[
        start_y:start_y+h,
        start_x:start_x+w,
    ] = cropped

    return canvas

