"""
AncientScriptLab

Algorithm

geometry.foreground.area

Feature

G-004 Foreground Area
"""

from __future__ import annotations

import numpy as np

from core.execution.algorithm import Algorithm


def execute(context):

    image = context.image

    return float(np.count_nonzero(image))


ALGORITHM = Algorithm(
    name="geometry.foreground.area",
    title="Foreground Area",
    version="1.0",
    author="AncientScriptLab",
    features=("G-004",),
    implementation=execute,
    dependencies=(),
    complexity="O(n)",
    deterministic=True,
    reference="Pixel Count",
)

