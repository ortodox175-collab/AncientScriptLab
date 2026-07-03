"""
AncientScriptLab

Experiment Runner

Central execution engine for scientific experiments.
"""

from __future__ import annotations

from core.experiments.experiment import Experiment
from core.experiments.result import ExperimentResult


class ExperimentRunner:

    """
    Executes scientific experiments.
    """

    # --------------------------------------------------

    def run(
        self,
        experiment: Experiment,
    ) -> ExperimentResult:

        result = experiment.run()

        if not isinstance(result, ExperimentResult):

            raise TypeError(

                "Experiment must return ExperimentResult."

            )

        return result

