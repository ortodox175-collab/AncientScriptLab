"""
AncientScriptLab

Reference Dataset Generator
"""

from pathlib import Path

import cv2
import numpy as np


OUT = Path("tests/data/reference")
OUT.mkdir(parents=True, exist_ok=True)


SIZE = 100


def save(name, img):

    cv2.imwrite(str(OUT / name), img)


# --------------------------------------------------

# Square

img = np.zeros((SIZE, SIZE), np.uint8)

img[30:70, 30:70] = 255

save("001_square.png", img)

# --------------------------------------------------

# Rectangle

img = np.zeros((SIZE, SIZE), np.uint8)

img[25:75, 20:80] = 255

save("002_rectangle.png", img)

# --------------------------------------------------

# Circle

img = np.zeros((SIZE, SIZE), np.uint8)

cv2.circle(img, (50, 50), 20, 255, -1)

save("003_circle.png", img)

# --------------------------------------------------

# Triangle

img = np.zeros((SIZE, SIZE), np.uint8)

pts = np.array([[50,20],[20,80],[80,80]], np.int32)

cv2.fillPoly(img,[pts],255)

save("004_triangle.png", img)

# --------------------------------------------------

# Cross

img = np.zeros((SIZE, SIZE), np.uint8)

img[20:80,45:55]=255

img[45:55,20:80]=255

save("005_cross.png", img)

print()

print("Reference dataset created")

print(OUT)

