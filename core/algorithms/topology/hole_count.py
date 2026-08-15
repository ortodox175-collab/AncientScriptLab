"""
AncientScriptLab

Topology Algorithm

Hole Count

Digital topology convention:
    Foreground = 8-connectivity
    Background = 4-connectivity

Topology Refactor v2.1
"""

from __future__ import annotations

import cv2
import numpy as np

from core.execution.algorithm import Algorithm
from core.algorithms.topology._binary_utils import (
    binary_image,
    BACKGROUND_CONNECTIVITY,
)


def execute(context) -> float:
    """
    Number of enclosed background components (holes).

    Background components touching the image border are exterior
    background and therefore are not counted as holes.
    """

    binary = binary_image(context)
    background = cv2.bitwise_not(binary)

    num_labels, labels = cv2.connectedComponents(
        background,
        connectivity=BACKGROUND_CONNECTIVITY,
    )

    border_labels = set()
    border_labels.update(np.unique(labels[0, :]))
    border_labels.update(np.unique(labels[-1, :]))
    border_labels.update(np.unique(labels[:, 0]))
    border_labels.update(np.unique(labels[:, -1]))

    holes = sum(
        1
        for label in range(1, num_labels)
        if label not in border_labels
    )

    return float(holes)


ALGORITHM = Algorithm(
    name="topology.hole_count",
    title="Hole Count",
    version="2.1",
    author="AncientScriptLab",
    features=("T-002",),
    implementation=execute,
    dependencies=("topology.connected_components",),
    complexity="O(N)",
    deterministic=True,
    reference="Background connected-component analysis using complementary 4-connectivity",
)
