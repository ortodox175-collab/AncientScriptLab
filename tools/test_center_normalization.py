"""
AncientScriptLab

Normalization Comparison Test
"""

from core.io.image_loader import load_image
from core.context.feature_context import FeatureContext

from core.normalization.center import center_image
from core.normalization.center_of_mass import center_of_mass

from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine
from core.packs.geometry_pack import GeometryPack


registry = RuntimeRegistry()
GeometryPack.register_all(registry)
engine = ExecutionEngine(registry)


def report(title, image):

    context = FeatureContext(image)

    print(title)
    print("-" * len(title))

    values = [
        ("Centroid X", "geometry.centroid_x"),
        ("Centroid Y", "geometry.centroid_y"),
        ("Width", "geometry.bounding_box.width"),
        ("Height", "geometry.bounding_box.height"),
    ]

    for name, algorithm in values:
        value = engine.compute(algorithm, context)
        print(f"{name:<12}: {value}")

    print()


def main():

    image = load_image("tests/data/reference/004_triangle.png")

    report("Original", image)

    report(
        "Bounding Box Center",
        center_image(image),
    )

    report(
        "Center Of Mass",
        center_of_mass(image),
    )


if __name__ == "__main__":
    main()

