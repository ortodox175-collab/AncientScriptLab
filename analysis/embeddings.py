from collections import defaultdict
import math


# =========================
# v5 — CO-OCCURRENCE MATRIX
# =========================

def build_cooccurrence(sequence, window=2):
    """
    матрица совместных появлений символов
    """
    matrix = defaultdict(lambda: defaultdict(int))

    for i in range(len(sequence)):
        for j in range(1, window + 1):
            if i + j < len(sequence):
                a = sequence[i]
                b = sequence[i + j]
                matrix[a][b] += 1
                matrix[b][a] += 1

    return matrix


# =========================
# PMI (упрощённый)
# =========================

def compute_pmi(matrix):
    total = 0
    freq = defaultdict(int)

    for a in matrix:
        for b in matrix[a]:
            freq[a] += matrix[a][b]
            total += matrix[a][b]

    pmi = defaultdict(dict)

    for a in matrix:
        for b in matrix[a]:
            p_a = freq[a] / total
            p_b = freq[b] / total
            p_ab = matrix[a][b] / total

            if p_ab == 0:
                continue

            pmi[a][b] = math.log(p_ab / (p_a * p_b) + 1e-9)

    return pmi


# =========================
# SIMPLE EMBEDDINGS (vector)
# =========================

def build_embeddings(pmi):
    """
    превращаем PMI в вектора
    """
    symbols = list(pmi.keys())
    vectors = {}

    for s in symbols:
        vec = []
        for t in symbols:
            vec.append(pmi.get(s, {}).get(t, 0.0))
        vectors[s] = vec

    return vectors


# =========================
# cosine similarity
# =========================

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))

    if na == 0 or nb == 0:
        return 0.0

    return dot / (na * nb)
