from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class TextRecord:
    """
    Universal text record for AncientScriptLab v8.

    This class is intentionally script-agnostic.
    It stores only objective information about a sequence.

    Compatible with the current analysis modules.
    """

    # Existing API (kept for compatibility)
    script: str
    text_id: str
    sequence: List[int]

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ---------- v8 extensions ----------

    source: Optional[str] = None
    corpus: Optional[str] = None
    version: Optional[str] = None

    encoding: str = "unicode"

    confidence: float = 1.0

    tags: List[str] = field(default_factory=list)

    properties: Dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.sequence)

    @property
    def symbols(self) -> int:
        return len(self.sequence)

    @property
    def unique_symbols(self) -> int:
        return len(set(self.sequence))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "script": self.script,
            "text_id": self.text_id,
            "sequence": self.sequence,
            "metadata": self.metadata,
            "source": self.source,
            "corpus": self.corpus,
            "version": self.version,
            "encoding": self.encoding,
            "confidence": self.confidence,
            "tags": self.tags,
            "properties": self.properties,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TextRecord":
        return cls(
            script=data["script"],
            text_id=data["text_id"],
            sequence=list(data["sequence"]),
            metadata=data.get("metadata", {}),
            source=data.get("source"),
            corpus=data.get("corpus"),
            version=data.get("version"),
            encoding=data.get("encoding", "unicode"),
            confidence=float(data.get("confidence", 1.0)),
            tags=list(data.get("tags", [])),
            properties=dict(data.get("properties", {})),
        )

    def copy(self) -> "TextRecord":
        return TextRecord.from_dict(self.to_dict())
