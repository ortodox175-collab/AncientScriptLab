"""
AncientScriptLab

Test

Min-Max Normalization
"""

from __future__ import annotations

from core.vector.feature_vector import FeatureVector
from core.statistics.feature_statistics import FeatureStatistics
from core.normalization.min_max import MinMaxNormalization


def build_vector(values):

    vector = FeatureVector()

    for feature, value in values.items():

        vector.add(feature, value)

    return vector


vectors = [

    build_vector({

        "A": 10,

        "B": 100,

    }),

    build_vector({

        "A": 20,

        "B": 200,

    }),

    build_vector({

        "A": 30,

        "B": 300,

    }),

]


statistics = FeatureStatistics.build(vectors)

method = MinMaxNormalization()

normalized = [

    method.normalize(

        vector,

        statistics,

    )

    for vector in vectors

]


print()

print("=" * 72)

print("Min-Max Normalization")

print("=" * 72)

for i, vector in enumerate(normalized, start=1):

    print()

    print(f"Vector {i}")

    for feature, value in vector:

        print(f"  {feature}: {value:.6f}")

