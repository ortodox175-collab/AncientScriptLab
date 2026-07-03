"""
AncientScriptLab

M6.4

Test Validation of Normalization Methods
"""

from __future__ import annotations

from core.vector.feature_vector import FeatureVector
from tools.validate_normalization_methods import (
    NormalizationValidation,
)


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

validator = NormalizationValidation(vectors)

normalized = validator.min_max()

print()

print("===== Min-Max =====")

for i, vector in enumerate(normalized, start=1):

    print(f"Vector {i}")

    for feature, value in vector:

        print(f"  {feature}: {value:.6f}")

    print()

