"""
AncientScriptLab

Topology Algorithm

Foreground Density

M7

Computes the foreground-area density relative to
the image area.
"""

from __future__ import annotations

import numpy as np

from core.execution.algorithm import Algorithm


def execute(context) -> float:
    """
    Compute foreground density.

    Density = foreground_area / image_area

    Foreground convention:
    black sign = foreground
    white background = background

    Returns 0.0 for an empty image.
    """

    image = context.image

    if image.ndim != 2:
        raise ValueError("Grayscale image expected.")

    height, width = image.shape

    image_area = height * width

    if image_area == 0:
        return 0.0

    foreground_area = int(np.count_nonzero(image < 128))

    density = foreground_area / image_area

    return float(density)


ALGORITHM = Algorithm(
    name="topology.foreground_density",
    title="Foreground Density",
    version="2.0",
    author="AncientScriptLab",
    features=("T-022",),
    implementation=execute,
    dependencies=(),
    complexity="O(N)",
    deterministic=True,
    reference="Foreground-area density relative to image area",
)
