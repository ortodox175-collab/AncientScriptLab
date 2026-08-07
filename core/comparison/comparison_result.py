"""
AncientScriptLab

Comparison Result

Container for the complete result of a symbol comparison.
"""

from __future__ import annotations

from core.vector.feature_vector import FeatureVector


class ComparisonResult:

    def __init__(
        self,
        *,
        distance: float,
        contributions: dict,
        vector_a: FeatureVector,
        vector_b: FeatureVector,
        normalized_vector_a: FeatureVector,
        normalized_vector_b: FeatureVector,
    ):

        self.distance = float(distance)

        self.contributions = dict(contributions)

        self.vector_a = vector_a
        self.vector_b = vector_b

        self.normalized_vector_a = normalized_vector_a
        self.normalized_vector_b = normalized_vector_b

    # --------------------------------------------------

    def as_dict(self):

        return {

            "distance": self.distance,

            "contributions": dict(self.contributions),

            "vector_a": self.vector_a.as_dict(),

            "vector_b": self.vector_b.as_dict(),

            "normalized_vector_a":
                self.normalized_vector_a.as_dict(),

            "normalized_vector_b":
                self.normalized_vector_b.as_dict(),
        }

    # --------------------------------------------------

    def __repr__(self):

        return (
            f"ComparisonResult("
            f"distance={self.distance:.6f}, "
            f"features={len(self.vector_a)})"
        )
