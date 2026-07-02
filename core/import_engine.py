from pathlib import Path

from core.record import TextRecord


class ImportEngine:
    """
    Universal Import Engine
    AncientScriptLab v8
    """

    @staticmethod
    def load_unicode_file(
        path,
        script="Unknown",
        text_id=None,
        metadata=None,
        encoding="utf-8"
    ):

        path = Path(path)

        if text_id is None:
            text_id = path.stem

        if metadata is None:
            metadata = {}

        text = path.read_text(
            encoding=encoding
        )

        sequence = [ord(ch) for ch in text]

        return TextRecord(
            script=script,
            text_id=text_id,
            sequence=sequence,
            metadata=metadata,
            source=str(path),
            corpus=script,
            version="v8",
            encoding="unicode",
        )

    @staticmethod
    def load_numeric_file(
        path,
        script="Unknown",
        separator=" "
    ):

        path = Path(path)

        data = path.read_text(
            encoding="utf-8"
        ).split(separator)

        sequence = []

        for x in data:

            x = x.strip()

            if x == "":
                continue

            sequence.append(int(x))

        return TextRecord(
            script=script,
            text_id=path.stem,
            sequence=sequence,
            source=str(path),
            corpus=script,
            version="v8",
            encoding="numeric",
        )
