"""
AncientScriptLab

Current Core smoke entrypoint.

AncientScriptLab measures sign material.
It does not decipher, translate, or assign meaning.
"""

from __future__ import annotations

import numpy as np

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as connected_components
from core.algorithms.topology.hole_count import execute as hole_count
from core.algorithms.topology.euler_characteristic import execute as euler_characteristic
from core.algorithms.topology.total_foreground_area import execute as foreground_area
from core.algorithms.topology.foreground_density import execute as foreground_density
from core.algorithms.geometry.aspect_ratio import execute as aspect_ratio


def main() -> None:
    image = np.full((7, 7), 255, dtype=np.uint8)
    image[2:5, 2:5] = 0

    context = FeatureContext(image)

    print("AncientScriptLab — Core Measurement Baseline")
    print("===========================================")
    print("Connected components :", connected_components(context))
    print("Holes                :", hole_count(context))
    print("Euler characteristic :", euler_characteristic(context))
    print("Foreground area      :", foreground_area(context))
    print("Foreground density   :", foreground_density(context))
    print("Aspect ratio         :", aspect_ratio(context))


if __name__ == "__main__":
    main()
