"""
AncientScriptLab

Feature Contribution Validation

M6.2
"""

from pathlib import Path
from math import sqrt

from core.io.image_loader import load_image
from core.context.feature_context import FeatureContext

from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine
from core.packs.geometry_pack import GeometryPack

from core.vector.feature_vector import FeatureVector
from core.statistics.feature_statistics import FeatureStatistics
from core.comparison.feature_normalizer import FeatureNormalizer


REFERENCE = Path("tests/data/reference")

ALGORITHMS = [
    ("G-001", "geometry.bounding_box.width"),
    ("G-002", "geometry.bounding_box.height"),
    ("G-003", "geometry.bounding_box.area"),
    ("G-004", "geometry.foreground.area"),
    ("G-005", "geometry.perimeter"),
    ("G-006", "geometry.aspect_ratio"),
    ("G-007", "geometry.extent"),
    ("G-008", "geometry.centroid_x"),
    ("G-009", "geometry.centroid_y"),
    ("G-010", "geometry.compactness"),
]


def build_vector(engine, image):

    context = FeatureContext(image)

    vector = FeatureVector()

    for code, algorithm in ALGORITHMS:
        vector.add(code, engine.compute(algorithm, context))

    return vector


def main():

    registry = RuntimeRegistry()
    # RuntimeRegistry loads canonical packs automatically

    engine = ExecutionEngine(registry)

    names = []
    vectors = []

    for image_path in sorted(REFERENCE.glob("*.png")):

        names.append(image_path.stem)
        vectors.append(build_vector(engine, load_image(image_path)))

    statistics = FeatureStatistics.build(vectors)

    vectors = [
        FeatureNormalizer.from_statistics(v, statistics)
        for v in vectors
    ]

    left = vectors[0]      # square
    right = vectors[2]     # circle

    print("=" * 72)
    print("AncientScriptLab")
    print("Feature Contribution")
    print("=" * 72)
    print()

    print("Reference :", names[0])
    print("Compared  :", names[2])
    print()

    total = 0.0

    for feature, left_value in left:

        right_value = right.get(feature)

        contribution = (left_value - right_value) ** 2

        total += contribution

        print(
            f"{feature:<8}"
            f"{contribution:>12.6f}"
        )

    print()
    print(f"Squared Sum : {total:.6f}")
    print(f"Distance    : {sqrt(total):.6f}")


if __name__ == "__main__":
    main()

