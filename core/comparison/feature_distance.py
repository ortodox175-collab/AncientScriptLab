"""
AncientScriptLab

Feature Distance

M6

Computes distances between FeatureVector objects.
"""

from __future__ import annotations

import math

from core.vector.feature_vector import FeatureVector


class FeatureDistance:

    @staticmethod
    def euclidean(
        left: FeatureVector,
        right: FeatureVector,
    ) -> float:

        left_data = left.to_dict()
        right_data = right.to_dict()

        keys = sorted(
            set(left_data.keys()) &
            set(right_data.keys())
        )

        total = 0.0

        for key in keys:

            delta = float(left_data[key]) - float(right_data[key])

            total += delta * delta

        return math.sqrt(total)

