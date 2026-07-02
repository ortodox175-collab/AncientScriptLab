from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class SignReference:
    """
    Universal sign object.

    Version:
        AncientScriptLab v8.0.2

    Stores only objective information.
    No semantics.
    """

    # Universal sign identifier
    id: int

    # Optional external identifier
    label: Optional[str] = None

    # Script name
    script: Optional[str] = None

    # Source corpus
    corpus: Optional[str] = None

    # Future geometry/image reference
    image: Optional[str] = None

    # Future feature storage
    features: Dict[str, Any] = field(default_factory=dict)

    # Research tags
    tags: List[str] = field(default_factory=list)

    @property
    def value(self) -> int:
        """
        Compatibility with integer-based code.
        """
        return self.id

    def __int__(self) -> int:
        return self.id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "script": self.script,
            "corpus": self.corpus,
            "image": self.image,
            "features": self.features,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            id=data["id"],
            label=data.get("label"),
            script=data.get("script"),
            corpus=data.get("corpus"),
            image=data.get("image"),
            features=data.get("features", {}),
            tags=data.get("tags", []),
        )

    def __repr__(self):
        return f"SignReference({self.id})"
