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
    def __init__(self):
        self.records: Dict[str, SignRecord] = {}

    def add(self, record: SignRecord):
        self.records[record.sign_id] = record

    def get(self, sign_id: str) -> Optional[SignRecord]:
        return self.records.get(sign_id)

    def category(self, sign_id: str) -> Optional[str]:
        rec = self.get(sign_id)
        return rec.category if rec else None

    def to_json(self, path: str | Path):
        data = {
            "registry_version": "1.0",
            "records": [asdict(r) for r in self.records.values()]
        }
        Path(path).write_text(json.dumps(data, indent=2))

    @classmethod
    def from_json(cls, path: str | Path):
        data = json.loads(Path(path).read_text())
        reg = cls()
        for r in data["records"]:
            reg.add(SignRecord(**r))
        return reg
