#!/usr/bin/env python3
"""
AncientScriptLab

Registry Validation Tool
"""

from pathlib import Path
import sys

from core.registry.loader import RegistryLoader
from core.registry.validator import RegistryValidator


def main():

    registry_path = Path("registry/feature_registry.yaml")

    if not registry_path.exists():
        print("FATAL: registry/feature_registry.yaml not found")
        sys.exit(1)

    registry = RegistryLoader.load(registry_path)

    errors = RegistryValidator.validate(registry)

    print("=" * 45)
    print("AncientScriptLab Registry Validator")
    print("=" * 45)
    print()

    print(f"Project   : {registry.metadata.project}")
    print(f"Registry  : {registry.metadata.registry}")
    print(f"Version   : {registry.metadata.version}")
    print(f"Features  : {registry.count()}")
    print()

    if errors:
        print("Status    : INVALID")
        print()

        for error in errors:
            print(error)

        sys.exit(1)

    print("Status    : VALID")
    print("Errors    : 0")
    print()


if __name__ == "__main__":
    main()
