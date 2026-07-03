"""
AncientScriptLab

Test

Experiment Framework
"""

from __future__ import annotations

from core.experiments.experiment import Experiment
from core.experiments.result import ExperimentResult
from core.experiments.runner import ExperimentRunner


class DummyExperiment(Experiment):

    name = "Dummy Experiment"

    def run(self) -> ExperimentResult:

        result = ExperimentResult(
            experiment=self.name,
        )

        result.set_status("PASS")

        result.add_measurement(
            "example_value",
            42.0,
        )

        result.add_metadata(
            "version",
            "1.0",
        )

        return result


runner = ExperimentRunner()

result = runner.run(
    DummyExperiment()
)

print()

print("=" * 72)
print("Experiment Framework")
print("=" * 72)

print()

for key, value in result.to_dict().items():

    print(f"{key}: {value}")

