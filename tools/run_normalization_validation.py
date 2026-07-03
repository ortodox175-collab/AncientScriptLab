"""
AncientScriptLab

M6.4

Normalization Validation Runner

Runs every available normalization method
through the scientific validation protocol.
"""

from __future__ import annotations

from tools.validate_normalization_methods import (
    NormalizationValidation,
)
from tools.normalization_validation_protocol import (
    ValidationProtocol,
)
from core.vector.feature_vector import FeatureVector


def build_vector(values):

    vector = FeatureVector()

    for feature, value in values.items():
        vector.add(feature, value)

    return vector


vectors = [

    build_vector({"A": 10, "B": 100}),

    build_vector({"A": 20, "B": 200}),

    build_vector({"A": 30, "B": 300}),

]


validator = NormalizationValidation(vectors)

methods = [

    ("No Normalization", validator.none),

    ("Min-Max", validator.min_max),

    ("Z-Score", validator.z_score),

    ("Robust", validator.robust),

    ("Percentile", validator.percentile),

    ("Log Scaling", validator.log_scaling),

]


print()
print("=" * 72)
print("AncientScriptLab")
print("M6.4 Scientific Validation")
print("=" * 72)

for name, method in methods:

    print()
    print("-" * 72)
    print(name)
    print("-" * 72)

    try:

        method()

        print("Status : Available")

    except NotImplementedError:

        print("Status : Planned")

    print()

    for criterion, _ in ValidationProtocol.CRITERIA:

        print(f"[ ] {criterion}")

