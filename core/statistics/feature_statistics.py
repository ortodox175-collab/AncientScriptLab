"""
AncientScriptLab

Feature Statistics

M6

Computes descriptive statistics
for FeatureVector collections.
"""

from __future__ import annotations

from collections import defaultdict

from core.vector.feature_vector import FeatureVector


class FeatureStatistics:

    @staticmethod
    def build(
        vectors: list[FeatureVector],
    ) -> dict[str, dict[str, float]]:

        values = defaultdict(list)

        for vector in vectors:

            for feature, value in vector.to_dict().items():

                values[feature].append(float(value))

        statistics = {}

        for feature, numbers in values.items():

            statistics[feature] = {

                "count": len(numbers),

                "min": min(numbers),

                "max": max(numbers),

                "mean": sum(numbers) / len(numbers),

            }

        return statistics

