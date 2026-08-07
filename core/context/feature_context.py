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

    _binary: Optional[np.ndarray] = field(
        default=None,
        init=False,
        repr=False,
    )

    _bounding_box: Optional[BoundingBox] = field(
        default=None,
        init=False,
        repr=False,
    )

    @property
    def binary(self) -> np.ndarray:
        """
        Binary foreground mask.

        Convention:
        foreground (sign) = 255
        background = 0
        """

        if self._binary is None:

            if self.image.ndim != 2:
                raise ValueError(
                    "Grayscale image expected."
                )

            _, binary = cv2.threshold(
                self.image,
                127,
                255,
                cv2.THRESH_BINARY_INV,
            )

            self._binary = binary

        return self._binary

    @property
    def bounding_box(self) -> BoundingBox:
        """
        Lazily compute Bounding Box.
        """

        if self._bounding_box is None:

            points = cv2.findNonZero(self.binary)

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
