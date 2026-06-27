import re
from core.record import TextRecord

LINE_RE = re.compile(r"^(A[a-zA-Z0-9]*)\s+(\d+)\s+(\d+)")

def parse_rongorongo_lines(lines):
    """
    Ожидаемый формат строки:
    Aa01 001 430-----
    """

    records = []

    current_tablet = None
    current_sequence = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split()

        if len(parts) < 3:
            continue

        tablet = parts[0]
        index = int(parts[1])
        glyph_raw = parts[2]

        # извлекаем только числовой код знака
        glyph_match = re.match(r"(\d+)", glyph_raw)
        if not glyph_match:
            continue

        glyph = int(glyph_match.group(1))

        # новый планшет
        if current_tablet is None:
            current_tablet = tablet

        if tablet != current_tablet:
            # сохраняем предыдущий блок
            if current_sequence:
                records.append(
                    TextRecord(
                        script="Rongorongo",
                        text_id=current_tablet,
                        sequence=current_sequence,
                        metadata={}
                    )
                )

            current_tablet = tablet
            current_sequence = []

        current_sequence.append(glyph)

    # последний блок
    if current_sequence:
        records.append(
            TextRecord(
                script="Rongorongo",
                text_id=current_tablet,
                sequence=current_sequence,
                metadata={}
            )
        )

    return records


def load_rongorongo_file(path):
    """
    Загружает файл корпуса ронго-ронго и возвращает список TextRecord
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    return parse_rongorongo_lines(lines)
