"""
AncientScriptLab

Test

Normalization Validation Experiment
"""

from __future__ import annotations

from core.vector.feature_vector import FeatureVector
from core.experiments.runner import ExperimentRunner
from core.experiments.registry import ExperimentRegistry
from core.experiments.normalization_validation import (
    NormalizationValidationExperiment,
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


registry = ExperimentRegistry()

registry.register(

    NormalizationValidationExperiment(

        vectors,

        method="min-max",

    )

)


experiment = registry.get(

    "Normalization Validation"

)

runner = ExperimentRunner()

result = runner.run(

    experiment

)


print()

print("=" * 72)

print("Normalization Validation Experiment")

print("=" * 72)

print()

for key, value in result.to_dict().items():

    print(f"{key}: {value}")

