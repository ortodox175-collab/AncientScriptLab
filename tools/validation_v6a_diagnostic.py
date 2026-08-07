import cv2

from core.context.feature_context import FeatureContext
from core.algorithms.topology.connected_components import execute as cc
from core.algorithms.topology.hole_count import execute as hc
from core.algorithms.topology.euler_characteristic import execute as ec
from core.algorithms.topology.total_foreground_area import execute as ta

img = cv2.imread(
    "validation/synthetic/images/single_square.png",
    cv2.IMREAD_GRAYSCALE,
)

def report(title, image):
    ctx = FeatureContext(image)
    print(title)
    print(f"  size: {image.shape[1]}x{image.shape[0]}")
    print(f"  components: {cc(ctx)}")
    print(f"  holes:      {hc(ctx)}")
    print(f"  euler:      {ec(ctx)}")
    print(f"  area:       {ta(ctx)}")
    print()

report("Original", img)

resized = cv2.resize(
    img,
    None,
    fx=0.9,
    fy=0.9,
    interpolation=cv2.INTER_NEAREST,
)

canvas = 255 * cv2.UMat(64,64,cv2.CV_8UC1).get()
h, w = resized.shape
x = (64 - w) // 2
y = (64 - h) // 2
canvas[y:y+h, x:x+w] = resized

report("Scaled 90%", canvas)
