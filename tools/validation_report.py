"""
AncientScriptLab

Scientific Validation Report

Common reporting framework for validation experiments.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationReport:

    experiment: str

    method: str

    results: dict[str, str] = field(default_factory=dict)

    # --------------------------------------------------

    def add(
        self,
        criterion: str,
        status: str,
    ):

        self.results[criterion] = status

    # --------------------------------------------------

    def overall_status(self) -> str:

        values = set(self.results.values())

        if "FAIL" in values:
            return "FAIL"

        if "WARNING" in values:
            return "WARNING"

        if values and values == {"PASS"}:
            return "PASS"

        return "INCOMPLETE"

    # --------------------------------------------------

    def print(self):

        print()

        print("=" * 72)
        print(self.experiment)
        print("=" * 72)

        print(f"Method : {self.method}")
        print()

        width = max(len(name) for name in self.results)

        for criterion, status in self.results.items():

            print(
                f"{criterion:<{width}} : {status}"
            )

        print()

        print(
            f"Overall Status : {self.overall_status()}"
        )

