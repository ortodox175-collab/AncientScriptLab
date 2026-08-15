"""
AncientScriptLab

Geometry Feature Pack

Registers canonical geometry algorithms.
Scientific implementations live exclusively in
core.algorithms.geometry.
"""

from __future__ import annotations

from typing import Dict

from core.execution.algorithm import Algorithm

from core.algorithms.geometry.aspect_ratio import (
    ALGORITHM as ASPECT_RATIO,
)
from core.algorithms.geometry.bounding_box_width import (
    ALGORITHM as BOUNDING_BOX_WIDTH,
)
from core.algorithms.geometry.bounding_box_height import (
    ALGORITHM as BOUNDING_BOX_HEIGHT,
)
from core.algorithms.geometry.bounding_box_area import (
    ALGORITHM as BOUNDING_BOX_AREA,
)
from core.algorithms.geometry.centroid_x import (
    ALGORITHM as CENTROID_X,
)
from core.algorithms.geometry.centroid_y import (
    ALGORITHM as CENTROID_Y,
)
from core.algorithms.geometry.compactness import (
    ALGORITHM as COMPACTNESS,
)
from core.algorithms.geometry.extent import (
    ALGORITHM as EXTENT,
)
from core.algorithms.geometry.foreground_area import (
    ALGORITHM as FOREGROUND_AREA,
)
from core.algorithms.geometry.perimeter import (
    ALGORITHM as PERIMETER,
)


class GeometryPack:
    """
    Registry of geometry algorithms.

    Scientific logic lives in algorithm modules,
    not in the pack.
    """

    def __init__(self) -> None:
        self._features: Dict[str, Algorithm] = {
            "aspect_ratio": ASPECT_RATIO,
            "bounding_box.width": BOUNDING_BOX_WIDTH,
            "bounding_box.height": BOUNDING_BOX_HEIGHT,
            "bounding_box.area": BOUNDING_BOX_AREA,
            "centroid_x": CENTROID_X,
            "centroid_y": CENTROID_Y,
            "compactness": COMPACTNESS,
            "extent": EXTENT,
            "foreground.area": FOREGROUND_AREA,
            "perimeter": PERIMETER,
        }

    def get(self, name: str) -> Algorithm:
        if name not in self._features:
            raise KeyError(f"Geometry feature not found: {name}")

        return self._features[name]

    def list_features(self) -> list[str]:
        return sorted(self._features.keys())
