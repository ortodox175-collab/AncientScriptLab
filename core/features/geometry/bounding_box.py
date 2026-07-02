"""
AncientScriptLab

Geometry Features

Bounding Box Feature Group

Implements

G-001 Bounding Box Width
G-002 Bounding Box Height
"""

from __future__ import annotations

from core.context.feature_context import FeatureContext


class BoundingBoxFeatures:
    """
    Feature implementations using FeatureContext.

    No OpenCV calls.
    No computations.
    Only reads cached geometry.
    """

    @staticmethod
    def feature_g001(ctx: FeatureContext) -> float:
        """
        G-001
        Bounding Box Width
        """
        return float(ctx.bounding_box.width)

    @staticmethod
    def feature_g002(ctx: FeatureContext) -> float:
        """
        G-002
        Bounding Box Height
        """
        return float(ctx.bounding_box.height)

    @staticmethod
    def x(ctx: FeatureContext) -> int:
        return ctx.bounding_box.x

    @staticmethod
    def y(ctx: FeatureContext) -> int:
        return ctx.bounding_box.y
