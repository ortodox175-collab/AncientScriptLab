"""
AncientScriptLab

Normalization Validation Experiment

First real scientific experiment.
"""

from __future__ import annotations

from core.experiments.experiment import Experiment
from core.experiments.result import ExperimentResult
from tools.validate_normalization_methods import (
    NormalizationValidation,
)


class NormalizationValidationExperiment(Experiment):

    name = "Normalization Validation"

    def __init__(

        self,

        vectors,

        method="min-max",

    ):

        self.vectors = vectors

        self.method = method

    # --------------------------------------------------

    def run(self) -> ExperimentResult:

        validator = NormalizationValidation(
            self.vectors
        )

        normalized = validator.run(
            self.method
        )

        result = ExperimentResult(
            experiment=self.name,
        )

        result.set_status("PASS")

        result.add_metadata(
            "method",
            self.method,
        )

        result.add_measurement(
            "vectors_processed",
            len(normalized),
        )

        return result

