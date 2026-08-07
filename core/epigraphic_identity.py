"""
AncientScriptLab

Universal epigraphic identity core.

This module defines the canonical epigraphic identity object.
The module is corpus-independent and contains no references
to any specific writing system.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SignCategory(Enum):
    HUMAN = "human"
    BIRD = "bird"
    ANIMAL = "animal"
    PLANT = "plant"
    WATER = "water"
    BUILDING = "building"
    OBJECT = "object"
    GEOMETRIC = "geometric"
    UNKNOWN = "unknown"


class Orientation(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"
    DIAGONAL = "diagonal"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class EpigraphicIdentity:
    """
    Canonical epigraphic identity of a sign.
    """

    asl_id: str
    category: SignCategory
    subcategory: Optional[str] = None
    orientation: Orientation = Orientation.UNKNOWN
    configuration: Optional[str] = None
    variant: Optional[str] = None

    def same_sign(self, other: "EpigraphicIdentity") -> bool:
        return self.asl_id == other.asl_id

    def same_category(self, other: "EpigraphicIdentity") -> bool:
        return self.category == other.category

    def same_orientation(self, other: "EpigraphicIdentity") -> bool:
        return self.orientation == other.orientation

    def structural_signature(self) -> tuple:
        return (
            self.category.value,
            self.subcategory,
            self.orientation.value,
            self.configuration,
        )
