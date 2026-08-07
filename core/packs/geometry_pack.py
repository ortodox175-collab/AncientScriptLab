"""
AncientScriptLab

Geometry Feature Pack

M7 compatibility layer
"""

from __future__ import annotations

from typing import Dict

from core.execution.algorithm import Algorithm


class GeometryPack:
    """
    Geometry pack using legacy Algorithm interface.
    """

    def __init__(self) -> None:

        self._features: Dict[str, Algorithm] = {}

        self._features["aspect_ratio"] = Algorithm(
            name="aspect_ratio",
            title="Aspect Ratio",
            version="1.0",
            author="AncientScriptLab",
            features=("G-006",),
            implementation=self._aspect_ratio,
        )

    # ---------------------------------------------
    # Feature implementation
    # ---------------------------------------------

    def _aspect_ratio(self, context) -> float:

        bbox = context.bounding_box

        if bbox.height == 0:
            return 0.0

        return float(bbox.width / bbox.height)

    # ---------------------------------------------
    # API
    # ---------------------------------------------

    def get(self, name: str):

        if name not in self._features:
            raise KeyError(f"Geometry feature not found: {name}")

        return self._features[name]

    def list_features(self):

        return list(self._features.keys())