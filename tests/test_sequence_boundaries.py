from core.corpus.corpus_sequence import CorpusSequence, Inscription
from core.sequence.bigrams import corpus_bigrams, inscription_bigrams


a = Inscription(
    id="A",
    signs=["X", "Y", "Z"],
)

b = Inscription(
    id="B",
    signs=["P", "Q"],
)

corpus = CorpusSequence(
    corpus="test",
    inscriptions=[a, b],
)

assert corpus_bigrams(corpus) == [
    ("X", "Y"),
    ("Y", "Z"),
    ("P", "Q"),
]

# Must NOT create ("Z", "P")
assert ("Z", "P") not in corpus_bigrams(corpus)

damaged = Inscription(
    id="C",
    signs=["A", "B", "C", "D"],
    damaged_positions=[1],
)

# Damage at B breaks A-B and B-C,
# but C-D remains valid.
assert inscription_bigrams(damaged) == [
    ("C", "D"),
]

print("SEQUENCE BOUNDARY POLICY: PASS")
