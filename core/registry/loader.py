"""
AncientScriptLab

Registry Loader
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .models import (
    Feature,
    FeatureRegistry,
    RegistryMetadata,
)


class RegistryLoader:
    """Loads a Feature Registry from YAML."""

    @staticmethod
    def load(path: str | Path) -> FeatureRegistry:

        path = Path(path)

        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        metadata = RegistryMetadata(
            version=data["version"],
            project=data["metadata"]["project"],
            registry=data["metadata"]["registry"],
            status=data["metadata"]["status"],
            description=data["metadata"]["description"],
        )

        features = []

        for item in data["features"]:

            features.append(
                Feature(
                    id=item["id"],
                    internal_name=item["internal_name"],
                    name=item["name"],
                    short_name=item["short_name"],
                    category=item["category"],
                    origin=item["origin"],
                    computation_level=item["computation_level"],
                    algorithm=item["algorithm"],
                    input=item["input"],
                    output=item["output"],
                    units=item["units"],
                    normalization=item["normalization"],
                    deterministic=item["deterministic"],
                    dependencies=item.get("dependencies", []),
                    invariance=item.get("invariance", {}),
                    complexity=item.get("complexity", ""),
                    scientific_status=item.get(
                        "scientific_status",
                        ""
                    ),
                    maturity=item.get(
                        "maturity",
                        "Draft"
                    ),
                )
            )

        return FeatureRegistry(
            metadata=metadata,
            categories=data["categories"],
            features=features,
        )
