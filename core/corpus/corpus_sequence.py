from dataclasses import dataclass, field
from typing import List, Literal
import json
from pathlib import Path


IdentityLevel = Literal["observation", "canonical"]


@dataclass
class Inscription:
    id: str
    signs: List[str]
    source: str = ""
    confidence: float = 1.0
    damaged_positions: List[int] = field(default_factory=list)


@dataclass
class CorpusSequence:
    corpus: str
    inscriptions: List[Inscription]
    identity_level: IdentityLevel = "canonical"

    @classmethod
    def from_json(cls, path: str | Path):
        data = json.loads(
            Path(path).read_text(encoding="utf-8")
        )

        inscriptions = [
            Inscription(
                id=i["id"],
                signs=i["signs"],
                source=i.get("source", ""),
                confidence=i.get("confidence", 1.0),
                damaged_positions=i.get("damaged_positions", []),
            )
            for i in data["inscriptions"]
        ]

        return cls(
            corpus=data["corpus"],
            inscriptions=inscriptions,
            identity_level=data.get("identity_level", "canonical"),
        )

    def to_json(self, path: str | Path):
        data = {
            "corpus": self.corpus,
            "identity_level": self.identity_level,
            "inscriptions": [
                {
                    "id": i.id,
                    "signs": i.signs,
                    "source": i.source,
                    "confidence": i.confidence,
                    "damaged_positions": i.damaged_positions,
                }
                for i in self.inscriptions
            ],
        }

        Path(path).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

    def total_tokens(self) -> int:
        return sum(len(i.signs) for i in self.inscriptions)

    def unique_signs(self):
        result = set()

        for inscription in self.inscriptions:
            result.update(inscription.signs)

        return result

    def validate(self):
        errors = []

        if self.identity_level not in ("observation", "canonical"):
            errors.append(
                f"Invalid identity_level: {self.identity_level}"
            )

        for ins in self.inscriptions:
            if not ins.id:
                errors.append("Inscription without id")

            if not isinstance(ins.signs, list):
                errors.append(f"{ins.id}: signs must be a list")
                continue

            if not all(isinstance(x, str) for x in ins.signs):
                errors.append(
                    f"{ins.id}: sign identifiers must be strings"
                )

            if not (0.0 <= ins.confidence <= 1.0):
                errors.append(
                    f"{ins.id}: confidence out of range"
                )

            for p in ins.damaged_positions:
                if p < 0 or p >= len(ins.signs):
                    errors.append(
                        f"{ins.id}: damaged position {p} out of range"
                    )

        return errors
