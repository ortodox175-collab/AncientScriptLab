from core.record import TextRecord
from core.import_rongorongo import load_rongorongo_file


class Corpus:
    def __init__(self):
        self.records = []

    def add(self, record: TextRecord):
        self.records.append(record)

    # текущий рабочий загрузчик ронго-ронго
    def load_rongorongo(self, path: str):
        self.records.extend(load_rongorongo_file(path))

    def load_generic(self, path: str, script_name: str):
        if script_name == "Rongorongo":
            return self.load_rongorongo(path)
        raise ValueError(f"Unsupported script: {script_name}")

    # временный универсальный интерфейс (без ломки системы)
    def load_generic(self, path: str, script_name: str):
        if script_name.lower() == "rongorongo":
            self.load_rongorongo(path)
        else:
            raise NotImplementedError(
                f"Script '{script_name}' not supported yet in current pipeline"
            )

    def filter(self, script: str):
        return [r for r in self.records if getattr(r, "script", script) == script]

    def all_sequences(self, script: str):
        seq = []
        for r in self.records:
            if getattr(r, "script", script) == script:
                seq.extend(r.sequence)
        return seq

    def __len__(self):
        return len(self.records)
