"""
AncientScriptLab

Algorithm Object

Represents one executable scientific algorithm.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(slots=True, frozen=True)
class Algorithm:
    """
    Runtime representation of one scientific algorithm.
    """

    # --------------------------------------------------
    # Required fields
    # --------------------------------------------------

    name: str

    title: str

    version: str

    author: str

    features: tuple[str, ...]

    implementation: Callable = field(
        repr=False,
        compare=False,
    )

    # --------------------------------------------------
    # Optional fields
    # --------------------------------------------------

    dependencies: tuple[str, ...] = ()

    complexity: str = "Unknown"

    deterministic: bool = True

    reference: str = ""

    # --------------------------------------------------

    def execute(self, context):

        return self.implementation(context)

    # --------------------------------------------------

    def metadata(self) -> dict:

        return {
            "name": self.name,
            "title": self.title,
            "version": self.version,
            "author": self.author,
            "features": list(self.features),
            "dependencies": list(self.dependencies),
            "complexity": self.complexity,
            "deterministic": self.deterministic,
            "reference": self.reference,
        }
