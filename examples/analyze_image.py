"""
AncientScriptLab

Geometry Pack Demo
"""

from core.io.image_loader import load_image
from core.context.feature_context import FeatureContext
from core.execution.runtime_registry import RuntimeRegistry
from core.execution.engine import ExecutionEngine
from core.packs.geometry_pack import GeometryPack


def main():

    image = load_image("tests/data/test.png")

    context = FeatureContext(image)

    registry = RuntimeRegistry()

    GeometryPack.register_all(registry)

    engine = ExecutionEngine(registry)

    algorithms = [

        ("Width", "geometry.bounding_box.width"),
        ("Height", "geometry.bounding_box.height"),
        ("Bounding Box Area", "geometry.bounding_box.area"),
        ("Foreground Area", "geometry.foreground.area"),
        ("Perimeter", "geometry.perimeter"),
        ("Aspect Ratio", "geometry.aspect_ratio"),
        ("Extent", "geometry.extent"),
        ("Centroid X", "geometry.centroid_x"),
        ("Centroid Y", "geometry.centroid_y"),
        ("Compactness", "geometry.compactness"),

    ]

    print()
    print("========================================")
    print(" AncientScriptLab")
    print(" Geometry Pack M5")
    print("========================================")
    print()

    for title, algorithm in algorithms:

        value = engine.compute(algorithm, context)

        print(f"{title:<18}: {value}")

    print()
    print("M5 COMPLETE")


if __name__ == "__main__":
    main()

