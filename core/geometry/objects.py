"""
AncientScriptLab

Geometry Objects

Pure data objects.

No algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BoundingBox:
    """
    Axis-aligned bounding box.
    """

    x: int
    y: int

    width: int
    height: int


# ----------------------------------------------------
# Reserved for future objects
# ----------------------------------------------------

#
# Contour
#
# ConvexHull
#
# Skeleton
#
# Moments
#
# ConnectedComponents
#
