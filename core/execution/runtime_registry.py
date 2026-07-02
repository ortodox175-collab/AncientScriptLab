"""
AncientScriptLab

Runtime Registry

Stores runtime Algorithm objects.
"""

from __future__ import annotations

from typing import Dict, Iterable

from core.execution.algorithm import Algorithm


class RuntimeRegistry:

    def __init__(self):

        self._algorithms: Dict[str, Algorithm] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        algorithm: Algorithm,
    ) -> None:

        if algorithm.name in self._algorithms:

            raise ValueError(
                f"Algorithm already registered: {algorithm.name}"
            )

        self._algorithms[algorithm.name] = algorithm

    # --------------------------------------------------
    # Lookup
    # --------------------------------------------------

    def exists(
        self,
        algorithm_name: str,
    ) -> bool:

        return algorithm_name in self._algorithms

    def get(
        self,
        algorithm_name: str,
    ) -> Algorithm:

        if algorithm_name not in self._algorithms:

            raise KeyError(
                f"Unknown algorithm: {algorithm_name}"
            )

        return self._algorithms[algorithm_name]

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    @property
    def algorithms(self):

        return tuple(
            sorted(self._algorithms.keys())
        )

    def count(self):

        return len(self._algorithms)

    def clear(self):

        self._algorithms.clear()

    def __contains__(
        self,
        algorithm_name: str,
    ):

        return algorithm_name in self._algorithms

    def __len__(self):

        return len(self._algorithms)

    def __iter__(self) -> Iterable[Algorithm]:

        for name in sorted(self._algorithms.keys()):
            yield self._algorithms[name]
