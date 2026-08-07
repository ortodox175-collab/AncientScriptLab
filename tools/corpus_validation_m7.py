from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

from core.execution.engine import ExecutionEngine
from core.execution.runtime_registry import RuntimeRegistry
from core.context.feature_context import FeatureContext


def load_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f'Cannot load image: {path}')
    return image


def compute_statistics(values):
    arr = np.asarray(values, dtype=float)
    return {
        'mean': float(np.mean(arr)),
        'std': float(np.std(arr)),
        'min': float(np.min(arr)),
        'max': float(np.max(arr)),
    }


def main():
    corpus_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("datasets/indus/images")

    registry = RuntimeRegistry()
    engine = ExecutionEngine(registry)

    feature_names = registry.list_features("topology")

    image_paths = sorted(corpus_dir.glob("*.png"))
    results = {}

    for path in image_paths:
        image = load_image(path)
        context = FeatureContext(image)

        for feature in feature_names:
            value = engine.compute(f"topology.{feature}", context)
            results.setdefault(feature, []).append(value)

    print("=" * 72)
    print("AncientScriptLab M7.2 Corpus Validation")
    print("=" * 72)
    print()
    print(f"Corpus           : {corpus_dir}")
    print(f"Images processed : {len(image_paths)}")
    print()

    report = {
        "corpus": str(corpus_dir),
        "images": len(image_paths),
        "statistics": {},
    }

    for feature in sorted(results.keys()):
        stats = compute_statistics(results[feature])
        report["statistics"][feature] = stats

        print(f"topology.{feature}")
        print(
            f"  mean={stats['mean']:.6f}  "
            f"std={stats['std']:.6f}  "
            f"min={stats['min']:.6f}  "
            f"max={stats['max']:.6f}"
        )
        print()

    out = Path("reports/corpus_validation")
    out.mkdir(parents=True, exist_ok=True)
    report_path = out / f"{corpus_dir.parent.name}_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
