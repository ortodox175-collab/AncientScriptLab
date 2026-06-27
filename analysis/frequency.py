from collections import Counter


def frequency(sequence):
    return Counter(sequence)


def top_symbols(sequence, n=10):
    return Counter(sequence).most_common(n)


def frequency_distribution(sequence):
    total = len(sequence)
    freq = Counter(sequence)

    return {k: v / total for k, v in freq.items()}
