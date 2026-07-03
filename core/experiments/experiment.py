"""
AncientScriptLab

Scientific Experiment

Base class for every scientific experiment.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Experiment(ABC):
    """
    Base class for all scientific experiments.
    """

    name = "Unnamed Experiment"

    # --------------------------------------------------

    @abstractmethod
    def run(self):
        """
        Execute the experiment.
        """
        raise NotImplementedError

