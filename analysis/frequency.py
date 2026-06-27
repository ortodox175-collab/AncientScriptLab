from collections import Counter


def frequency(sequence):
    """
    Возвращает частоты символов
    """
    return Counter(sequence)


def top_symbols(sequence, n=10):
    """
    Топ-N самых частых символов
    """
    freq = Counter(sequence)
    return freq.most_common(n)


def frequency_distribution(sequence):
    """
    Нормализованное распределение (0..1)
    """
    total = len(sequence)
    freq = Counter(sequence)

    return {
        symbol: count / total
        for symbol, count in freq.items()
    }
