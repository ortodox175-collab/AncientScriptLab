"""
AncientScriptLab

M6.4

Scientific Validation Protocol

Every normalization method must be evaluated
using exactly the same scientific criteria.

This module defines the evaluation protocol only.
It does not implement the normalization methods.
"""

from __future__ import annotations


class ValidationProtocol:

    """
    Scientific protocol for evaluating
    normalization methods.
    """

    CRITERIA = [

        (
            "Distance Stability",
            "Are pairwise distances stable?"
        ),

        (
            "Feature Contribution",
            "Does one feature dominate the distance?"
        ),

        (
            "Outlier Sensitivity",
            "How strongly do outliers affect normalization?"
        ),

        (
            "Small Corpus Behaviour",
            "How does the method behave on very small datasets?"
        ),

        (
            "Large Corpus Behaviour",
            "How does the method behave on large datasets?"
        ),

        (
            "Numerical Stability",
            "Does the method remain numerically stable?"
        ),

        (
            "Scientific Interpretability",
            "Are the results scientifically explainable?"
        ),

        (
            "Reproducibility",
            "Does repeated execution produce identical results?"
        ),

    ]

    @classmethod
    def show(cls):

        print()

        print("=" * 72)
        print("AncientScriptLab")
        print("Normalization Validation Protocol")
        print("=" * 72)

        for i, (name, description) in enumerate(
            cls.CRITERIA,
            start=1,
        ):

            print()

            print(f"{i}. {name}")

            print(f"   {description}")

