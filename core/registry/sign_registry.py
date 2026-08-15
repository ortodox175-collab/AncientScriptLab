"""
AncientScriptLab

Sign Data Registry

Stores dataset/resource records associated with sign identifiers.

This registry does NOT define canonical epigraphic identity.
Canonical identities are managed by IdentityRegistry.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Optional
import json


@dataclass
class SignRecord:
    sign_id: str
    category: str
    image_path: str = ""
    feature_vector_path: str = ""
    source: str = ""
    description: str = ""
    confidence: float = 1.0


class SignRegistry:
    """
    Registry of sign-associated data/resources.

    Duplicate identifiers are forbidden.
    Replacement must always be explicit.
    """

    def __init__(self):
        self.records: Dict[str, SignRecord] = {}

    def add(self, record: SignRecord) -> None:
        if record.sign_id in self.records:
            raise ValueError(
                f"Duplicate sign record: {record.sign_id}"
            )

        self.records[record.sign_id] = record

    def replace(self, record: SignRecord) -> None:
        if record.sign_id not in self.records:
            raise KeyError(
                f"Sign record not found: {record.sign_id}"
            )

        self.records[record.sign_id] = record

    def get(self, sign_id: str) -> Optional[SignRecord]:
        return self.records.get(sign_id)

    def category(self, sign_id: str) -> Optional[str]:
        rec = self.get(sign_id)
        return rec.category if rec else None

    def to_json(self, path: str | Path) -> None:
        data = {
            "registry_version": "1.1",
            "records": [asdict(r) for r in self.records.values()],
        }

        Path(path).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_json(cls, path: str | Path):
        data = json.loads(
            Path(path).read_text(encoding="utf-8")
        )

        reg = cls()

        for raw in data["records"]:
            reg.add(SignRecord(**raw))

        return reg
