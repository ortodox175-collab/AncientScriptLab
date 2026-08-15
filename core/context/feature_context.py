"""
AncientScriptLab

Feature Context

Central immutable computation context.
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

    Contract:
    - image must be a 2D grayscale numpy array
    - dtype must be uint8
    - image values therefore lie in [0, 255]
    - input is copied on construction and made read-only
    - foreground mask convention:
        foreground = 255
        background = 0
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

    def __post_init__(self) -> None:
        if not isinstance(self.image, np.ndarray):
            raise TypeError("image must be a numpy.ndarray")

        if self.image.ndim != 2:
            raise ValueError("FeatureContext requires a 2D grayscale image.")

        if self.image.dtype != np.uint8:
            raise TypeError(
                f"FeatureContext requires dtype uint8, got {self.image.dtype}."
            )

        image = np.array(self.image, dtype=np.uint8, copy=True)
        image.flags.writeable = False
        self.image = image

    @property
    def binary(self) -> np.ndarray:
        """
        Canonical binary foreground mask.

        Threshold contract:
        source <= 127 -> foreground 255
        source > 127  -> background 0
        """

        if self._binary is None:
            _, binary = cv2.threshold(
                self.image,
                127,
                255,
                cv2.THRESH_BINARY_INV,
            )

            binary.flags.writeable = False
            self._binary = binary

        return self._binary

    @property
    def bounding_box(self) -> BoundingBox:
        """
        Lazily compute foreground bounding box.

        Coordinates follow OpenCV boundingRect:
        x, y = top-left pixel
        width, height = inclusive pixel extent expressed as dimensions
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
