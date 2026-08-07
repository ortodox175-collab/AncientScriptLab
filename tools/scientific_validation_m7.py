"""
AncientScriptLab

M7.1 Scientific validation protocol
"""

from __future__ import annotations

import random
import time
import tracemalloc

import cv2
import numpy as np

from core.context.feature_context import FeatureContext
from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry

FEATURES = [
    "topology.connected_components",
    "topology.hole_count",
    "topology.euler_characteristic",
    "topology.largest_component_area",
    "topology.smallest_component_area",
    "topology.mean_component_area",
    "topology.component_area_ratio",
    "topology.total_foreground_area",
    "topology.component_density",
    "topology.foreground_density",
]


def generate_random_symbol(size: int = 64) -> np.ndarray:
    image = np.zeros((size, size), dtype=np.uint8)

    for _ in range(random.randint(1, 6)):
        x = random.randint(0, size - 10)
        y = random.randint(0, size - 10)
        w = random.randint(3, 15)
        h = random.randint(3, 15)

        cv2.rectangle(
            image,
            (x, y),
            (min(size - 1, x + w), min(size - 1, y + h)),
            255,
            -1,
        )

    return image


def validate(results: dict) -> list[str]:
    errors = []

    cc = results["topology.connected_components"]
    holes = results["topology.hole_count"]
    euler = results["topology.euler_characteristic"]

    largest = results["topology.largest_component_area"]
    smallest = results["topology.smallest_component_area"]
    mean = results["topology.mean_component_area"]
    total = results["topology.total_foreground_area"]

    ratio = results["topology.component_area_ratio"]
    comp_density = results["topology.component_density"]
    fg_density = results["topology.foreground_density"]

    image_area = 64 * 64

    if largest + 1e-9 < mean:
        errors.append("largest < mean")

    if mean + 1e-9 < smallest:
        errors.append("mean < smallest")

    if abs(euler - (cc - holes)) > 1e-9:
        errors.append("Euler inconsistency")

    if total > 0:
        if abs(ratio - largest / total) > 1e-9:
            errors.append("component_area_ratio inconsistency")

    if abs(fg_density - total / image_area) > 1e-9:
        errors.append("foreground_density inconsistency")

    if abs(comp_density - cc / image_area) > 1e-9:
        errors.append("component_density inconsistency")

    return errors


def main() -> None:
    print("=" * 72)
    print("AncientScriptLab M7.1 Scientific Validation Protocol")
    print("=" * 72)
    print()

    registry = RuntimeRegistry()
    engine = ExecutionEngine(registry)

    tracemalloc.start()
    start = time.perf_counter()

    failures = 0
    consistency = 0
    shown = 0

    images = 1000

    for _ in range(images):
        image = generate_random_symbol()
        context = FeatureContext(image)

        results = {}

        for feature in FEATURES:
            try:
                results[feature] = engine.compute(feature, context)
            except Exception:
                failures += 1

        errs = validate(results)

        if errs:
            consistency += len(errs)

            if shown < 5:
                shown += 1
                print("CONSISTENCY ERROR:", errs)
                print(results)
                print("-" * 72)

    end = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print()
    print("Images processed              :", images)
    print("Algorithms executed           :", len(FEATURES))
    print("Total computations            :", images * len(FEATURES))
    print()
    print("Execution failures            :", failures)
    print("Scientific consistency errors :", consistency)
    print()
    print(f"Total execution time          : {end-start:.3f} s")
    print(f"Mean time per image           : {(end-start)/images*1000:.3f} ms")
    print(f"Peak memory usage             : {peak/(1024*1024):.2f} MB")
    print()

    if failures == 0 and consistency == 0:
        print("SCIENTIFIC VALIDATION : PASSED")
    else:
        print("SCIENTIFIC VALIDATION : FAILED")


if __name__ == "__main__":
    main()
