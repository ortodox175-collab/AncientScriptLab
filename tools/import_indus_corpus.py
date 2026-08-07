"""
AncientScriptLab

Import Indus Corpus

Imports real Indus sign images into the corpus directory.
"""

from __future__ import annotations

from pathlib import Path

import cv2


SOURCE_DIR = Path("datasets/indus/raw")
TARGET_DIR = Path("datasets/indus/images")


def normalize_image(image):
    _, binary = cv2.threshold(
        image,
        127,
        255,
        cv2.THRESH_BINARY,
    )

    normalized = cv2.resize(
        binary,
        (64, 64),
        interpolation=cv2.INTER_NEAREST,
    )

    return normalized


def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    imported = 0

    for path in sorted(SOURCE_DIR.glob("*")):
        image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)

        if image is None:
            continue

        normalized = normalize_image(image)

        out = TARGET_DIR / f"indus_{imported:05d}.png"

        cv2.imwrite(str(out), normalized)

        imported += 1

    print(f"Imported images: {imported}")
    print(f"Target directory: {TARGET_DIR}")


if __name__ == "__main__":
    main()
