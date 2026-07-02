"""
AncientScriptLab

Execution Engine

Executes registered algorithms.
"""

from __future__ import annotations

from typing import Iterable

from core.context.feature_context import FeatureContext
from core.execution.runtime_registry import RuntimeRegistry


class ExecutionEngine:

    def __init__(
        self,
        registry: RuntimeRegistry,
    ):

        self.registry = registry

    # --------------------------------------------------
    # Execute one algorithm
    # --------------------------------------------------

    def compute(
        self,
        algorithm_name: str,
        context: FeatureContext,
    ):

        algorithm = self.registry.get(
            algorithm_name
        )

        return algorithm.execute(
            context
        )

    # --------------------------------------------------
    # Execute many algorithms
    # --------------------------------------------------

    def compute_many(
        self,
        algorithm_names: Iterable[str],
        context: FeatureContext,
    ):

        result = {}

        for name in algorithm_names:

            result[name] = self.compute(
                name,
                context,
            )

        return result
