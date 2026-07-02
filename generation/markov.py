import random
from collections import defaultdict


# =========================
# v3 CONTROL GENERATION
# =========================

def sample_next(prob_dict, temperature=1.0):
    """
    Temperature-controlled sampling
    """
    items = list(prob_dict.items())

    # temperature adjustment (softmax-like)
    adjusted = [(k, v ** (1.0 / max(temperature, 0.1))) for k, v in items]
    total = sum(v for _, v in adjusted)

    r = random.random()
    acc = 0.0

    for symbol, weight in adjusted:
        acc += weight / total
        if r <= acc:
            return symbol

    return items[-1][0]


def choose_start(sequence, freq):
    """
    stable start (top frequent tokens)
    """
    top = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:20]
    return random.choice([t[0] for t in top])


def generate_v3(prob_graph, start, length=30, temperature=0.8, max_repeat=3):
    """
    Controlled generation (anti-loop)
    """
    result = [start]
    current = start
    repeat = 0

    for _ in range(length - 1):

        if current not in prob_graph:
            break

        nxt = sample_next(prob_graph[current], temperature)

        if len(result) > 1 and nxt == result[-1]:
            repeat += 1
        else:
            repeat = 0

        if repeat >= max_repeat:
            break

        result.append(nxt)
        current = nxt

    return result


# =========================
# v3.1 MULTI-ORDER MODEL
# =========================

def build_context_model(sequence, order=2):
    """
    P(next | previous n tokens)
    """
    model = defaultdict(lambda: defaultdict(int))

    for i in range(len(sequence) - order):
        context = tuple(sequence[i:i+order])
        nxt = sequence[i+order]
        model[context][nxt] += 1

    # normalize
    prob_model = {}

    for ctx, targets in model.items():
        total = sum(targets.values())
        prob_model[ctx] = {
            k: v / total for k, v in targets.items()
        }

    return prob_model


def generate_v31(context_model, start_seq, length=30, temperature=0.8):
    """
    Multi-order generation (more language-like)
    """
    if len(start_seq) < 2:
        return start_seq

    order = len(next(iter(context_model.keys())))

    result = list(start_seq[:order])
    ctx = tuple(result[-order:])

    for _ in range(length - order):

        if ctx not in context_model:
            break

        nxt = sample_next(context_model[ctx], temperature)

        result.append(nxt)
        ctx = tuple(result[-order:])

    return result


# =========================
# v4 STRUCTURE SCORE
# =========================

def structure_score(sequence):
    """
    Heuristic "language-like structure"
    """
    if len(sequence) < 3:
        return 0.0

    transitions = len(set(zip(sequence[:-1], sequence[1:])))
    total = len(sequence)

    repetition = sum(
        1 for i in range(1, len(sequence))
        if sequence[i] == sequence[i-1]
    )

    diversity = transitions / total
    stability = 1 - (repetition / total)

    return (diversity * 0.6) + (stability * 0.4)
