"""
AncientScriptLab

Runtime Registry (Stable M7 Hybrid)

Pack-based execution registry.
"""

from __future__ import annotations

from typing import Dict, Any

# Core algorithm interface
from core.execution.algorithm import Algorithm

# Feature Packs
from core.packs.geometry_pack import GeometryPack
from core.packs.topology_pack import TopologyPack


class RuntimeRegistry:
    """
    Central registry for feature packs.

    Architecture: Pack-based (M7 stable hybrid)
    """

    def __init__(self) -> None:

        self._packs: Dict[str, Any] = {}

        self._register_packs()

    # ---------------------------------------------
    # Pack registration
    # ---------------------------------------------

    def _register_packs(self) -> None:

        # Geometry Pack
        self._packs["geometry"] = GeometryPack()

        # Topology Pack (M7)
        self._packs["topology"] = TopologyPack()

    # ---------------------------------------------
    # Public API
    # ---------------------------------------------

    def get(self, name: str):

        """
        Access pattern:
        - geometry.aspect_ratio
        - topology.connected_components
        - or direct pack access
        """

        if name in self._packs:
            return self._packs[name]

        if "." in name:
            pack_name, feature_name = name.split(".", 1)

            pack = self._packs.get(pack_name)
            if not pack:
                raise KeyError(f"Pack not found: {pack_name}")

            return pack.get(feature_name)

        raise KeyError(f"Feature not found: {name}")

    def list_packs(self):

        return list(self._packs.keys())

    def list_features(self, pack_name: str):

        pack = self._packs.get(pack_name)

        if not pack:
            raise KeyError(f"Pack not found: {pack_name}")

        return pack.list_features()