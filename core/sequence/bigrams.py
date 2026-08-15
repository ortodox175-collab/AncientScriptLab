"""
AncientScriptLab

Boundary-safe bigram analysis for CorpusSequence.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Tuple

from core.corpus.corpus_sequence import CorpusSequence, Inscription


Bigram = Tuple[str, str]


def inscription_bigrams(inscription: Inscription) -> list[Bigram]:
    """
    Build bigrams inside one inscription only.

    Any damaged position breaks adjacency.
    """
    damaged = set(inscription.damaged_positions)
    result: list[Bigram] = []

    for i in range(len(inscription.signs) - 1):
        if i in damaged or (i + 1) in damaged:
            continue

        result.append(
            (inscription.signs[i], inscription.signs[i + 1])
        )

    return result


def corpus_bigrams(corpus: CorpusSequence) -> list[Bigram]:
    """
    Build bigrams without crossing inscription boundaries.
    """
    result: list[Bigram] = []

    for inscription in corpus.inscriptions:
        result.extend(inscription_bigrams(inscription))

    return result


def bigram_frequency(corpus: CorpusSequence) -> Counter:
    return Counter(corpus_bigrams(corpus))
