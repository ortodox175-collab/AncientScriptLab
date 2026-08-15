"""
AncientScriptLab

Topology Binary Utilities

Shared binary-image utilities for all topology algorithms.

Digital topology convention:
    Foreground = 8-connectivity
    Background = 4-connectivity

Topology Refactor v2.1
"""

from __future__ import annotations

import cv2
import numpy as np


FOREGROUND_CONNECTIVITY = 8
BACKGROUND_CONNECTIVITY = 4


def binary_image(context) -> np.ndarray:
    """
    Return canonical binary image.

    Foreground (sign) = 255
    Background = 0
    """
    return context.binary


def image_area(context) -> int:
    binary = binary_image(context)
    height, width = binary.shape
    return int(height * width)


def foreground_area(context) -> int:
    binary = binary_image(context)
    return int(cv2.countNonZero(binary))


def connected_components_stats(context):
    binary = binary_image(context)

    return cv2.connectedComponentsWithStats(
        binary,
        connectivity=FOREGROUND_CONNECTIVITY,
    )


def connected_component_areas(context):
    num_labels, labels, stats, centroids = connected_components_stats(context)

    return [
        int(stats[label, cv2.CC_STAT_AREA])
        for label in range(1, num_labels)
    ]
