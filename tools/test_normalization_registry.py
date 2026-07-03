"""
AncientScriptLab

Test

Normalization Registry
"""

from __future__ import annotations

from core.normalization.registry import NormalizationRegistry


registry = NormalizationRegistry()

print()

print("=" * 72)
print("Normalization Registry")
print("=" * 72)

print()

print("Registered methods:")

for name in registry.names():

    print(f"  - {name}")

print()

method = registry.get("min-max")

print("Retrieved method:")

print(f"  Name : {method.name}")

print()

print("Registry test: PASSED")

