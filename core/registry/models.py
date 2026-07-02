"""
AncientScriptLab

Feature Registry Models

Scientific Registry Layer
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional


# ----------------------------------------------------
# Feature
# ----------------------------------------------------

@dataclass(slots=True)
class Feature:

    id: str

    internal_name: str

    name: str

    short_name: str

    category: str

    origin: str

    computation_level: int

    algorithm: str

    input: List[str]

    output: Dict

    units: Dict

    normalization: Dict

    deterministic: bool

    dependencies: List[str] = field(default_factory=list)

    invariance: Dict = field(default_factory=dict)

    complexity: str = ""

    scientific_status: str = ""

    maturity: str = "Draft"


# ----------------------------------------------------
# Registry Metadata
# ----------------------------------------------------

@dataclass(slots=True)
class RegistryMetadata:

    version: str

    project: str

    registry: str

    status: str

    description: str


# ----------------------------------------------------
# Registry
# ----------------------------------------------------

@dataclass(slots=True)
class FeatureRegistry:

    metadata: RegistryMetadata

    categories: Dict

    features: List[Feature]

    def count(self) -> int:
        return len(self.features)

    def ids(self):

        return [f.id for f in self.features]

    def internal_names(self):

        return [f.internal_name for f in self.features]

    def category(self, code: str):

        return [
            f
            for f in self.features
            if f.category == code
        ]

    def get(self, feature_id: str) -> Optional[Feature]:

        for feature in self.features:

            if feature.id == feature_id:

                return feature

        return None
