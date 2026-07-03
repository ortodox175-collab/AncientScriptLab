"""
AncientScriptLab

Min-Max Normalization

Scientific standard candidate.
"""

from __future__ import annotations

from core.normalization.base import NormalizationMethod
from core.vector.feature_vector import FeatureVector


class MinMaxNormalization(NormalizationMethod):

    name = "Min-Max"

    def normalize(
        self,
        vector: FeatureVector,
        statistics: dict[str, dict[str, float]],
    ) -> FeatureVector:

        normalized = FeatureVector()

        for feature, value in vector:

            if feature not in statistics:

                normalized.add(feature, float(value))
                continue

            minimum = statistics[feature]["min"]
            maximum = statistics[feature]["max"]

            if maximum == minimum:

                normalized.add(feature, 0.0)
                continue

            normalized.add(
                feature,
                (float(value) - minimum)
                / (maximum - minimum),
            )

        return normalized

