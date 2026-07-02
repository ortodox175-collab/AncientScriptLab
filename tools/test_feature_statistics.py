"""
AncientScriptLab

Feature Statistics Integration Test
"""

from pathlib import Path

from core.io.image_loader import load_image
from core.context.feature_context import FeatureContext

from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine

from core.packs.geometry_pack import GeometryPack

from core.vector.feature_vector import FeatureVector
from core.statistics.feature_statistics import FeatureStatistics


REFERENCE = Path("tests/data/reference")


def main():

    registry = RuntimeRegistry()
    GeometryPack.register_all(registry)

    engine = ExecutionEngine(registry)

    algorithms = [
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

    vectors = []

    for image_path in sorted(REFERENCE.glob("*.png")):

        image = load_image(image_path)
        context = FeatureContext(image)

        vector = FeatureVector()

        for code, algorithm in algorithms:
            vector.add(code, engine.compute(algorithm, context))

        vectors.append(vector)

    stats = FeatureStatistics.build(vectors)

    print("=" * 70)
    print("Feature Statistics")
    print("=" * 70)

    for feature in sorted(stats):

        s = stats[feature]

        print(
            f"{feature:<6}"
            f" count={s['count']:<2}"
            f" min={s['min']:.6f}"
            f" max={s['max']:.6f}"
            f" mean={s['mean']:.6f}"
        )


if __name__ == "__main__":
    main()

