"""
AncientScriptLab v8

Universal utilities.

All analysis modules should use sign_id()
instead of accessing integers directly.
"""

from typing import Any


def sign_id(obj: Any) -> int:
    """
    Returns integer sign id.

    Supports:

        int

        SignReference

    Future:

        VisionObject

        ObservedObject

        etc.
    """

    if isinstance(obj, int):
        return obj

    if hasattr(obj, "id"):
        return int(obj.id)

    raise TypeError(f"Unsupported sign object: {type(obj)}")
