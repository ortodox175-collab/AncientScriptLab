from core.record import TextRecord
from core.import_engine import ImportEngine


class Corpus:
    """
    Universal corpus container.

    AncientScriptLab v8
    """

    def __init__(self):

        self.records = []

    # ---------------------------------------------

    def add(self, record: TextRecord):

        self.records.append(record)

    # ---------------------------------------------

    def extend(self, records):

        self.records.extend(records)

    # ---------------------------------------------

    def clear(self):

        self.records.clear()

    # ---------------------------------------------

    def load_unicode(
        self,
        path,
        script="Unknown"
    ):

        record = ImportEngine.load_unicode_file(
            path=path,
            script=script
        )

        self.add(record)

        return record

    # ---------------------------------------------

    def load_numeric(
        self,
        path,
        script="Unknown",
        separator=" "
    ):

        record = ImportEngine.load_numeric_file(
            path=path,
            script=script,
            separator=separator
        )

        self.add(record)

        return record

    # ---------------------------------------------

    def summary(self):

        return {
            "records": len(self.records),
            "symbols": sum(len(r) for r in self.records)
        }

    # ---------------------------------------------

    def __len__(self):

        return len(self.records)

