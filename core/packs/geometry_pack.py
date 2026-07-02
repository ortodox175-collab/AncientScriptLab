"""
AncientScriptLab

Geometry Pack
"""

from __future__ import annotations

from core.algorithms.geometry.bounding_box_width import ALGORITHM as WIDTH
from core.algorithms.geometry.bounding_box_height import ALGORITHM as HEIGHT
from core.algorithms.geometry.bounding_box_area import ALGORITHM as BOX_AREA
from core.algorithms.geometry.foreground_area import ALGORITHM as FG_AREA
from core.algorithms.geometry.perimeter import ALGORITHM as PERIMETER
from core.algorithms.geometry.aspect_ratio import ALGORITHM as ASPECT_RATIO
from core.algorithms.geometry.extent import ALGORITHM as EXTENT
from core.algorithms.geometry.centroid_x import ALGORITHM as CENTROID_X
from core.algorithms.geometry.centroid_y import ALGORITHM as CENTROID_Y
from core.algorithms.geometry.compactness import ALGORITHM as COMPACTNESS


class GeometryPack:

    @staticmethod
    def register_all(registry):

        registry.register(WIDTH)
        registry.register(HEIGHT)
        registry.register(BOX_AREA)
        registry.register(FG_AREA)
        registry.register(PERIMETER)
        registry.register(ASPECT_RATIO)
        registry.register(EXTENT)
        registry.register(CENTROID_X)
        registry.register(CENTROID_Y)
        registry.register(COMPACTNESS)

