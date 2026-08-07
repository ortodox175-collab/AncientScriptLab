from pathlib import Path
from core.corpus.corpus_sequence import CorpusSequence
import json

EXAMPLE = Path("validation/examples/corpus_sequence_example.json")
REPORT = Path("reports/statistics/corpus_sequence_validation.json")

corpus = CorpusSequence.from_json(EXAMPLE)
errors = corpus.validate()

report = {
    "corpus": corpus.corpus,
    "inscriptions": len(corpus.inscriptions),
    "total_tokens": corpus.total_tokens(),
    "unique_signs": len(corpus.unique_signs()),
    "validation_errors": errors,
    "status": "PASS" if not errors else "FAIL",
}

REPORT.write_text(json.dumps(report, indent=2))

print("M9.0 CorpusSequence Foundation")
print("==============================")
print(f"Corpus             : {corpus.corpus}")
print(f"Inscriptions       : {len(corpus.inscriptions)}")
print(f"Total sign tokens  : {corpus.total_tokens()}")
print(f"Unique signs       : {len(corpus.unique_signs())}")
print(f"Validation status  : {report['status']}")
if errors:
    print("Errors:")
    for e in errors:
        print(" -", e)
print()
print(f"Validation report  : {REPORT}")
