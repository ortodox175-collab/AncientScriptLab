from core.observation_registry import (
    ObservationRecord,
    ObservationRegistry,
)
from core.corpus.corpus_sequence import (
    CorpusSequence,
    Inscription,
)


registry = ObservationRegistry()

registry.register(
    ObservationRecord(
        observation_id="OBS-0001",
        inscription_id="INS-001",
        position=0,
    )
)

registry.register(
    ObservationRecord(
        observation_id="OBS-0002",
        inscription_id="INS-001",
        position=1,
    )
)

assert len(registry) == 2

sequence = CorpusSequence(
    corpus="unknown-test",
    identity_level="observation",
    inscriptions=[
        Inscription(
            id="INS-001",
            signs=["OBS-0001", "OBS-0002"],
        )
    ],
)

assert sequence.validate() == []
assert sequence.identity_level == "observation"
assert sequence.total_tokens() == 2

try:
    registry.register(
        ObservationRecord(
            observation_id="OBS-0001",
            inscription_id="INS-002",
            position=0,
        )
    )
    raise AssertionError("Duplicate observation accepted")
except ValueError:
    pass

print("OBSERVATION / CANONICAL IDENTITY LAYERS: PASS")
