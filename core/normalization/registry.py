"""
AncientScriptLab

Normalization Registry

Central registry for all normalization methods.
"""

from __future__ import annotations

from core.normalization.base import NormalizationMethod
from core.normalization.min_max import MinMaxNormalization


class NormalizationRegistry:

    def __init__(self):

        self._methods = {}

        self.register(MinMaxNormalization())

    # --------------------------------------------------

    def register(
        self,
        method: NormalizationMethod,
    ):

        self._methods[method.name.lower()] = method

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> NormalizationMethod:

        try:

            return self._methods[name.lower()]

        except KeyError as e:

            raise ValueError(
                f"Unknown normalization method: {name}"
            ) from e

    # --------------------------------------------------

    def names(self):

        return sorted(self._methods.keys())

    # --------------------------------------------------

    def methods(self):

        return list(self._methods.values())

