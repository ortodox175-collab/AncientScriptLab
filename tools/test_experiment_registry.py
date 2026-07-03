"""
AncientScriptLab

Test

Experiment Registry
"""

from __future__ import annotations

from core.experiments.experiment import Experiment
from core.experiments.registry import ExperimentRegistry
from core.experiments.result import ExperimentResult


class DummyExperiment(Experiment):

    name = "Dummy Experiment"

    def run(self) -> ExperimentResult:

        result = ExperimentResult(
            experiment=self.name,
        )

        result.set_status("PASS")

        return result


registry = ExperimentRegistry()

registry.register(
    DummyExperiment()
)

print()

print("=" * 72)
print("Experiment Registry")
print("=" * 72)

print()

print("Registered experiments:")

for name in registry.names():

    print(f"  - {name}")

print()

experiment = registry.get(
    "Dummy Experiment"
)

print("Retrieved experiment:")

print(f"  Name : {experiment.name}")

print()

print("Registry test: PASSED")

