"""
AncientScriptLab

Universal Image Loader
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


SUPPORTED_FORMATS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tif",
    ".tiff",
}


def load_image(path: str | Path) -> np.ndarray:
    """
    Load grayscale image.

    Returns uint8 image.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported image format: {path.suffix}"
        )

    image = cv2.imread(
        str(path),
        cv2.IMREAD_GRAYSCALE,
    )

    if image is None:
        raise RuntimeError(
            f"Cannot load image: {path}"
        )

    return image
