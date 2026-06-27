from collections import Counter


def build_bigrams(sequence):
    """
    Строит список биграмм из последовательности
    """
    return [(sequence[i], sequence[i + 1]) for i in range(len(sequence) - 1)]


def bigram_frequency(sequence):
    """
    Частоты биграмм
    """
    return Counter(build_bigrams(sequence))


def top_bigrams(sequence, n=10):
    """
    Топ-N самых частых биграмм
    """
    return Counter(build_bigrams(sequence)).most_common(n)
