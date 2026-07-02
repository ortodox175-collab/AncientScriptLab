"""
AncientScriptLab

FeatureVector Test
"""

from core.vector.feature_vector import FeatureVector


vector = FeatureVector()

vector.add("G-001", 40.0)
vector.add("G-002", 40.0)
vector.add("G-003", 1600.0)

print()

print(vector)

print()

print(vector.as_dict())

print()

print("Length :", len(vector))

print()

print("FEATURE VECTOR READY")
