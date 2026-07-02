"""
AncientScriptLab

M6 Similarity Test

First complete comparison pipeline.
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

    vectors = []

    names = []

    for image_path in sorted(REFERENCE.glob("*.png")):

        image = load_image(image_path)

        vectors.append(build_vector(engine, image))

        names.append(image_path.name)

    statistics = FeatureStatistics.build(vectors)

    normalized = [
        FeatureNormalizer.from_statistics(v, statistics)
        for v in vectors
    ]

    print("=" * 72)
    print("AncientScriptLab")
    print("First Similarity Experiment")
    print("=" * 72)
    print()

    base = normalized[0]

    print("Reference :", names[0])
    print()

    for name, vector in zip(names, normalized):

        d = FeatureDistance.euclidean(base, vector)

        print(f"{name:<20} distance = {d:.6f}")


if __name__ == "__main__":
    main()

