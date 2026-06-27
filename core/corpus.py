from typing import List
from core.record import TextRecord
from core.import_rongorongo import load_rongorongo_file

class Corpus:
    def __init__(self):
        self.records: List[TextRecord] = []

    def add(self, record: TextRecord):
        self.records.append(record)

    def load_rongorongo(self, path: str):
        records = load_rongorongo_file(path)
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
