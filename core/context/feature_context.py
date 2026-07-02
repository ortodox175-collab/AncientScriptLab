"""
AncientScriptLab

Feature Context

Central cache for all expensive computations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import cv2
import numpy as np

from core.geometry.objects import BoundingBox


@dataclass(slots=True)
class FeatureContext:
    """
    Central computation context.

    Every expensive operation is computed once and cached.
    """

    image: np.ndarray

    _bounding_box: Optional[BoundingBox] = field(
        default=None,
        init=False,
        repr=False,
    )

    @property
    def bounding_box(self) -> BoundingBox:
        """
        Lazily compute Bounding Box.
        """

        if self._bounding_box is None:

            if self.image.ndim != 2:
                raise ValueError(
                    "Binary image expected."
                )

            points = cv2.findNonZero(self.image)

            if points is None:
                raise ValueError(
                    "Image contains no foreground pixels."
                )

            x, y, w, h = cv2.boundingRect(points)

            self._bounding_box = BoundingBox(
                x=x,
                y=y,
                width=w,
                height=h,
            )

        return self._bounding_box
