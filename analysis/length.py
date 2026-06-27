def record_lengths(records):
    """
    Возвращает список длин всех записей корпуса.
    """
    return [len(record.sequence) for record in records]


def average_length(records):
    """
    Средняя длина записи.
    """
    lengths = record_lengths(records)

    if not lengths:
        return 0.0

    return sum(lengths) / len(lengths)


def min_length(records):
    """
    Минимальная длина записи.
    """
    lengths = record_lengths(records)

    if not lengths:
        return 0

    return min(lengths)


def max_length(records):
    """
    Максимальная длина записи.
    """
    lengths = record_lengths(records)

    if not lengths:
        return 0

    return max(lengths)
