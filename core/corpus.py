from typing import List
from core.record import TextRecord
from core.import_engine import ImportEngine


class Corpus:
    def __init__(self):
        self.records: List[TextRecord] = []

    def add(self, record: TextRecord):
        self.records.append(record)

    def load_generic(self, path: str, script_name: str):
        engine = ImportEngine()
        records = engine.load_generic_json(path, script_name)
        self.records.extend(records)

    def filter(self, script: str):
        return [r for r in self.records if r.script == script]

    def all_sequences(self, script: str):
        seq = []
        for r in self.filter(script):
            seq.extend(r.sequence)
        return seq

    def __len__(self):
        return len(self.records)
