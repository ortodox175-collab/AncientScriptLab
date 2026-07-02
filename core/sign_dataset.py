from __future__ import annotations

from core.sign_library import SignLibrary
from core.record import TextRecord


class SignDataset:
    """
    AncientScriptLab v8

    Combines

        SignLibrary

    with

        TextRecord collection

    into one research dataset.
    """

    def __init__(self):

        self.library = SignLibrary()

        self.records = []

    # -----------------------------------------

    def add_record(self, record: TextRecord):

        self.records.append(record)

    # -----------------------------------------

    def add_sign(self, sign):

        self.library.add(sign)

    # -----------------------------------------

    def total_records(self):

        return len(self.records)

    # -----------------------------------------

    def total_signs(self):

        return len(self.library)

    # -----------------------------------------

    def summary(self):

        return {
            "records": self.total_records(),
            "registered_signs": self.total_signs()
        }

