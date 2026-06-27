import math
from collections import Counter

def entropy(sequence):
    if not sequence:
        return 0.0

    c = Counter(sequence)
    n = len(sequence)

    return -sum(
        (v / n) * math.log2(v / n)
        for v in c.values()
    )
