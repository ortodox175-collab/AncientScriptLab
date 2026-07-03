"""
AncientScriptLab

Normalization Base

Abstract interface for all normalization methods.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.vector.feature_vector import FeatureVector


class NormalizationMethod(ABC):
    """
    Base class for all normalization methods.
    """

    name = "Unknown"

    @abstractmethod
    def normalize(
        self,
        vector: FeatureVector,
        statistics: dict[str, dict[str, float]],
    ) -> FeatureVector:
        """
        Normalize a FeatureVector.
        """
        raise NotImplementedError

