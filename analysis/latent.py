from collections import defaultdict
import math


# =========================
# entropy per symbol context
# =========================

def context_entropy(sequence, symbol):
    next_symbols = []

    for i in range(len(sequence) - 1):
        if sequence[i] == symbol:
            next_symbols.append(sequence[i + 1])

    if not next_symbols:
        return 0.0

    freq = defaultdict(int)

    for s in next_symbols:
        freq[s] += 1

    total = len(next_symbols)

    entropy = 0.0

    for count in freq.values():
        p = count / total
        entropy -= p * math.log(p + 1e-9)

    return entropy


# =========================
# latent structure map
# =========================

def latent_structure(sequence):
    symbols = set(sequence)
    scores = {}

    for s in symbols:
        scores[s] = context_entropy(sequence, s)

    return scores


def print_latent(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print("\nLatent structure (high uncertainty symbols):")
    for s, v in sorted_scores[:10]:
        print(s, ":", round(v, 4))
