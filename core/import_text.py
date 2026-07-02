from core.record import TextRecord

def load_text_file(path: str, script_name: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    # универсальная токенизация: символы → int
    seq = [ord(c) for c in text]

    return [
        TextRecord(
            script=script_name,
            text_id=path,
            sequence=seq
        )
    ]
