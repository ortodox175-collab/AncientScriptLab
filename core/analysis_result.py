from dataclasses import dataclass, field
from typing import Any, Dict
from datetime import datetime


@dataclass(slots=True)
class AnalysisResult:
    """
    Universal result produced by any analysis stage.

    This class contains only objective computational results.

    It never stores semantic interpretations.
    """

    name: str

    result_type: str

    data: Any

    metadata: Dict[str, Any] = field(default_factory=dict)

    created: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    version: str = "1.0"

    def summary(self):

        return {

            "name": self.name,

            "type": self.result_type,

            "version": self.version,

            "created": self.created

        }

    def __len__(self):

        try:
            return len(self.data)
        except Exception:
            return 1

    def __repr__(self):

        return (

            f"AnalysisResult("

            f"name={self.name!r}, "

            f"type={self.result_type!r}, "

            f"size={len(self)}"

            f")"

        )
