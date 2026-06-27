from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TextRecord:
    script: str
    text_id: str
    sequence: List[int]
    metadata: Dict[str, Any]
