"""
AncientScriptLab

Topology Feature Pack

M7

Registers topology algorithms.
Scientific implementations are located exclusively in
core.algorithms.topology.
"""

from __future__ import annotations

from typing import Dict

from core.execution.algorithm import Algorithm

from core.algorithms.topology.connected_components import (
    ALGORITHM as CONNECTED_COMPONENTS,
)
from core.algorithms.topology.hole_count import (
    ALGORITHM as HOLE_COUNT,
)
from core.algorithms.topology.euler_characteristic import (
    ALGORITHM as EULER_CHARACTERISTIC,
)
from core.algorithms.topology.largest_component_area import (
    ALGORITHM as LARGEST_COMPONENT_AREA,
)
from core.algorithms.topology.smallest_component_area import (
    ALGORITHM as SMALLEST_COMPONENT_AREA,
)
from core.algorithms.topology.mean_component_area import (
    ALGORITHM as MEAN_COMPONENT_AREA,
)
from core.algorithms.topology.component_area_ratio import (
    ALGORITHM as COMPONENT_AREA_RATIO,
)
from core.algorithms.topology.total_foreground_area import (
    ALGORITHM as TOTAL_FOREGROUND_AREA,
)
from core.algorithms.topology.component_density import (
    ALGORITHM as COMPONENT_DENSITY,
)
from core.algorithms.topology.foreground_density import (
    ALGORITHM as FOREGROUND_DENSITY,
)


class TopologyPack:
    """
    Registry of topology algorithms.
    """

    def __init__(self) -> None:

        self._features: Dict[str, Algorithm] = {
            "connected_components": CONNECTED_COMPONENTS,
            "hole_count": HOLE_COUNT,
            "euler_characteristic": EULER_CHARACTERISTIC,
            "largest_component_area": LARGEST_COMPONENT_AREA,
            "smallest_component_area": SMALLEST_COMPONENT_AREA,
            "mean_component_area": MEAN_COMPONENT_AREA,
            "component_area_ratio": COMPONENT_AREA_RATIO,
            "total_foreground_area": TOTAL_FOREGROUND_AREA,
            "component_density": COMPONENT_DENSITY,
            "foreground_density": FOREGROUND_DENSITY,
        }

    def get(self, name: str) -> Algorithm:

        if name not in self._features:
            raise KeyError(f"Topology feature not found: {name}")

        return self._features[name]

    def list_features(self) -> list[str]:

        return sorted(self._features.keys())