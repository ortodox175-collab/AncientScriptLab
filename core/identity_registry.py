"""
AncientScriptLab

Identity registry for canonical epigraphic identities.

The registry is corpus-independent and stores only canonical
epigraphic identity objects.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from core.epigraphic_identity import (
    EpigraphicIdentity,
    Orientation,
    SignCategory,
)


class IdentityRegistry:
    """
    Registry of canonical epigraphic identities.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, EpigraphicIdentity] = {}

    # -----------------------------
    # Container protocol
    # -----------------------------

    def __len__(self) -> int:
        return len(self._registry)

    def __iter__(self):
        return iter(self._registry.values())

    def __contains__(self, asl_id: str) -> bool:
        return asl_id in self._registry

    # -----------------------------
    # Registry operations
    # -----------------------------

    def register(self, identity: EpigraphicIdentity) -> None:
        if identity.asl_id in self._registry:
            raise ValueError(f"Duplicate ASL identity: {identity.asl_id}")
        self._registry[identity.asl_id] = identity

    def get(self, asl_id: str) -> Optional[EpigraphicIdentity]:
        return self._registry.get(asl_id)

    def all(self) -> List[EpigraphicIdentity]:
        return list(self._registry.values())

    # -----------------------------
    # Queries
    # -----------------------------

    def by_category(self, category: SignCategory) -> List[EpigraphicIdentity]:
        return [
            sign
            for sign in self._registry.values()
            if sign.category == category
        ]

    def by_orientation(
        self,
        orientation: Orientation,
    ) -> List[EpigraphicIdentity]:
        return [
            sign
            for sign in self._registry.values()
            if sign.orientation == orientation
        ]

    def query(
        self,
        category: Optional[SignCategory] = None,
        orientation: Optional[Orientation] = None,
        subcategory: Optional[str] = None,
    ) -> List[EpigraphicIdentity]:
        result = list(self._registry.values())

        if category is not None:
            result = [s for s in result if s.category == category]

        if orientation is not None:
            result = [s for s in result if s.orientation == orientation]

        if subcategory is not None:
            result = [s for s in result if s.subcategory == subcategory]

        return result

    def size(self) -> int:
        return len(self._registry)
