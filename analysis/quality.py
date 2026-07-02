from analysis.bigrams import build_bigrams
from collections import Counter


def bigram_overlap(real_seq, gen_seq):
    real = set(build_bigrams(real_seq))
    gen = set(build_bigrams(gen_seq))

    if not gen:
        return 0.0

    return len(real & gen) / len(gen)


def transition_validity(gen_seq, graph):
    valid = 0
    total = 0

    for a, b in build_bigrams(gen_seq):
        total += 1
        if a in graph and b in graph[a]:
            valid += 1

    if total == 0:
        return 0.0

    return valid / total


def repetition_penalty(seq):
    if len(seq) < 2:
        return 1.0

    repeats = sum(
        1 for i in range(1, len(seq))
        if seq[i] == seq[i - 1]
    )

    return 1 - repeats / len(seq)


def overall_score(real_seq, gen_seq, graph):
    b = bigram_overlap(real_seq, gen_seq)
    t = transition_validity(gen_seq, graph)
    r = repetition_penalty(gen_seq)

    return (b * 0.4) + (t * 0.4) + (r * 0.2)
