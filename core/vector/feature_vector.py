"""
AncientScriptLab

Feature Vector
"""

from __future__ import annotations


class FeatureVector:

    def __init__(self):

        self._values = {}

    # --------------------------------------------

    def add(
        self,
        feature: str,
        value,
    ):

        self._values[feature] = value

    # --------------------------------------------

    def get(
        self,
        feature: str,
    ):

        return self._values[feature]

    # --------------------------------------------

    def as_dict(self):

        return dict(self._values)

    # --------------------------------------------

    def to_dict(self):

        return self.as_dict()

    # --------------------------------------------

    def items(self):

        return self._values.items()

    # --------------------------------------------

    def keys(self):

        return self._values.keys()

    # --------------------------------------------

    def values(self):

        return self._values.values()

    # --------------------------------------------

    def __len__(self):

        return len(self._values)

    # --------------------------------------------

    def __contains__(self, key):

        return key in self._values

    # --------------------------------------------

    def __iter__(self):

        return iter(sorted(self._values.items()))

    # --------------------------------------------

    def __repr__(self):

        return f"FeatureVector({self._values})"

