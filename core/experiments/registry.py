"""
AncientScriptLab

Experiment Registry

Central registry for scientific experiments.
"""

from __future__ import annotations

from core.experiments.experiment import Experiment


class ExperimentRegistry:

    def __init__(self):

        self._experiments = {}

    # --------------------------------------------------

    def register(
        self,
        experiment: Experiment,
    ):

        self._experiments[experiment.name] = experiment

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Experiment:

        try:

            return self._experiments[name]

        except KeyError as e:

            raise ValueError(
                f"Unknown experiment: {name}"
            ) from e

    # --------------------------------------------------

    def names(self):

        return sorted(self._experiments.keys())

    # --------------------------------------------------

    def experiments(self):

        return list(self._experiments.values())

