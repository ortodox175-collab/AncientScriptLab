"""
AncientScriptLab

Experiment Result

Stores the result of a scientific experiment.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ExperimentResult:

    experiment: str

    status: str = "UNKNOWN"

    measurements: dict[str, float] = field(
        default_factory=dict
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    # --------------------------------------------------

    def add_measurement(
        self,
        name: str,
        value: float,
    ):

        self.measurements[name] = float(value)

    # --------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value,
    ):

        self.metadata[key] = str(value)

    # --------------------------------------------------

    def set_status(
        self,
        status: str,
    ):

        self.status = status

    # --------------------------------------------------

    def to_dict(self):

        return {

            "experiment": self.experiment,

            "status": self.status,

            "measurements": dict(self.measurements),

            "metadata": dict(self.metadata),

        }

