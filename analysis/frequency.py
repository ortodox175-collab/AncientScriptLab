from collections import Counter
from core.utils import sign_id


def frequency(sequence):
    """
    Universal frequency counter.

    Supports:
        int
        SignReference
        future Vision objects
    """

    counter = Counter()

    for symbol in sequence:
        counter[sign_id(symbol)] += 1

    return dict(counter)


def top_symbols(sequence, n=10):
    freq = frequency(sequence)

    return sorted(
        freq.items(),
        key=lambda x: x[1],
        reverse=True
    )[:n]
