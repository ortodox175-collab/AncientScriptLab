"""
AncientScriptLab

Geometry Pack Validation

Runs all geometry algorithms
on the complete reference dataset.
"""

from pathlib import Path

from core.io.image_loader import load_image
from core.context.feature_context import FeatureContext
from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine
from core.packs.geometry_pack import GeometryPack


REFERENCE = Path("tests/data/reference")


def main():

    registry = RuntimeRegistry()
    GeometryPack.register_all(registry)

    engine = ExecutionEngine(registry)

    algorithms = [

        ("Width", "geometry.bounding_box.width"),
        ("Height", "geometry.bounding_box.height"),
        ("BBoxArea", "geometry.bounding_box.area"),
        ("Foreground", "geometry.foreground.area"),
        ("Perimeter", "geometry.perimeter"),
        ("Aspect", "geometry.aspect_ratio"),
        ("Extent", "geometry.extent"),
        ("CentroidX", "geometry.centroid_x"),
        ("CentroidY", "geometry.centroid_y"),
        ("Compactness", "geometry.compactness"),

    ]

    print("=" * 110)
    print("AncientScriptLab Geometry Validation")
    print("=" * 110)
    print()

    for image_path in sorted(REFERENCE.glob("*.png")):

        image = load_image(image_path)

        context = FeatureContext(image)

        print(image_path.name)

        for title, algorithm in algorithms:

            value = engine.compute(algorithm, context)

            print(f"  {title:<12}: {value}")

        print()


if __name__ == "__main__":
    main()

