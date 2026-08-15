"""
AncientScriptLab

Observation Registry

Stores individual observed sign instances before
canonical epigraphic identity is established.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ObservationRecord:
    observation_id: str
    inscription_id: str
    position: int
    source: str = ""
    image_path: str = ""
    damaged: bool = False


class ObservationRegistry:
    """
    Registry of individual sign observations.

    Observation identity is not canonical sign identity.
    Multiple observations may later be assigned to one
    EpigraphicIdentity.
    """

    def __init__(self) -> None:
        self._records: Dict[str, ObservationRecord] = {}

    def register(self, record: ObservationRecord) -> None:
        if record.observation_id in self._records:
            raise ValueError(
                f"Duplicate observation: {record.observation_id}"
            )

        if record.position < 0:
            raise ValueError("Observation position cannot be negative")

        self._records[record.observation_id] = record

    def get(self, observation_id: str) -> Optional[ObservationRecord]:
        return self._records.get(observation_id)

    def all(self) -> List[ObservationRecord]:
        return list(self._records.values())

    def __len__(self) -> int:
        return len(self._records)
