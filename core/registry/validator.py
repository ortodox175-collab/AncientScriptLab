"""
AncientScriptLab

Registry Validator
"""

from __future__ import annotations

from .models import FeatureRegistry


class RegistryValidator:

    @staticmethod
    def validate(registry: FeatureRegistry):

        errors = []

        # ---------------------------------------
        # Unique IDs
        # ---------------------------------------

        ids = registry.ids()

        if len(ids) != len(set(ids)):
            errors.append("VAL-001 Duplicate Feature ID")

        # ---------------------------------------
        # Unique Internal Names
        # ---------------------------------------

        internal = registry.internal_names()

        if len(internal) != len(set(internal)):
            errors.append("VAL-002 Duplicate Internal Name")

        # ---------------------------------------
        # Existing Dependencies
        # ---------------------------------------

        all_ids = set(ids)

        for feature in registry.features:

            for dep in feature.dependencies:

                if dep not in all_ids:

                    errors.append(
                        f"VAL-003 Unknown dependency: "
                        f"{feature.id} -> {dep}"
                    )

        return errors
