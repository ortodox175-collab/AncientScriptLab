"""
AncientScriptLab

Distance Matrix Validation

M6.1
"""

from pathlib import Path

from core.io.image_loader import load_image
from core.context.feature_context import FeatureContext

from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine
from core.packs.geometry_pack import GeometryPack

from core.vector.feature_vector import FeatureVector

from core.statistics.feature_statistics import FeatureStatistics
from core.comparison.feature_normalizer import FeatureNormalizer
from core.comparison.feature_distance import FeatureDistance


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
    GeometryPack.register_all(registry)

    engine = ExecutionEngine(registry)

    names = []
    vectors = []

    for image_path in sorted(REFERENCE.glob("*.png")):

        image = load_image(image_path)

        vectors.append(build_vector(engine, image))
        names.append(image_path.stem)

    statistics = FeatureStatistics.build(vectors)

    vectors = [
        FeatureNormalizer.from_statistics(v, statistics)
        for v in vectors
    ]

    print("=" * 90)
    print("AncientScriptLab")
    print("Distance Matrix")
    print("=" * 90)
    print()

    print(f"{'':15}", end="")

    for name in names:
        print(f"{name:>15}", end="")

    print()

    for i, left in enumerate(vectors):

        print(f"{names[i]:15}", end="")

        for right in vectors:

            d = FeatureDistance.euclidean(left, right)

            print(f"{d:15.4f}", end="")

        print()


if __name__ == "__main__":
    main()

