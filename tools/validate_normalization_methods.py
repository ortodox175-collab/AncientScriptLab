"""
AncientScriptLab

M6.4

Validation of Normalization Methods
"""

from __future__ import annotations

from core.statistics.feature_statistics import FeatureStatistics
from core.normalization.registry import NormalizationRegistry


class NormalizationValidation:

    def __init__(self, vectors):

        self.vectors = vectors

        self.registry = NormalizationRegistry()

    # --------------------------------------------------

    def run(
        self,
        method_name: str,
    ):

        statistics = FeatureStatistics.build(
            self.vectors
        )

        method = self.registry.get(method_name)

        return [

            method.normalize(
                vector,
                statistics,
            )

            for vector in self.vectors

        ]

    # --------------------------------------------------

    def min_max(self):

        return self.run("min-max")

    # --------------------------------------------------

    def z_score(self):

        raise NotImplementedError(
            "Planned for M6.4."
        )

    # --------------------------------------------------

    def robust(self):

        raise NotImplementedError(
            "Planned for M6.4."
        )

    # --------------------------------------------------

    def percentile(self):

        raise NotImplementedError(
            "Planned for M6.4."
        )

    # --------------------------------------------------

    def log_scaling(self):

        raise NotImplementedError(
            "Planned for M6.4."
        )

    # --------------------------------------------------

    def none(self):

        return self.vectors

