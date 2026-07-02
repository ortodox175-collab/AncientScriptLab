from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass(slots=True)
class IndusInscription:
    """
    Universal representation of one Indus inscription.

    No semantics.
    No translation.
    No interpretation.

    Stores only objective published data.
    """

    inscription_id: str

    signs: List[int]

    source: str

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class IndusCorpus:

    name: str

    version: str

    inscriptions: List[IndusInscription] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add(self, inscription: IndusInscription):

        self.inscriptions.append(inscription)

    def __len__(self):

        return len(self.inscriptions)

    def total_signs(self):

        return sum(len(x.signs) for x in self.inscriptions)

    def summary(self):

        return {
            "corpus": self.name,
            "version": self.version,
            "inscriptions": len(self.inscriptions),
            "total_signs": self.total_signs()
        }
