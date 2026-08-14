# AncientScriptLab — Egyptian Corpus Legacy Provenance

Status: historical/salvage record before removal of the final
datasets/egyptian/ corpus implementations.

## Scientific principle

Corpus ingestion must preserve source information.

No importer or normalizer may silently:

- discard unresolved tokens;
- merge inscriptions;
- cross inscription boundaries;
- assign unsupported confidence values;
- reinterpret uncertain source material as canonical identity.

Unknown or unresolved material must remain explicit data.

---

## 1. tools/import_mdc_corpus.py

Historical role:

- imported text encoded in Manuel de Codage style;
- preserved inscription-level records;
- extracted sign-like tokens;
- calculated corpus counts and inscription lengths;
- produced an Egyptian corpus sequence JSON.

Useful concepts to preserve:

- inscription boundaries;
- explicit source format;
- source-level token sequence;
- corpus token counts;
- unique-token counts;
- inscription-length statistics.

Implementation defects / limitations:

1. Token extraction is regex-based.

   TOKEN_RE accepts only a restricted family of sign-like strings.

2. Material not matching the regex is silently ignored.

   Therefore unresolved or unexpected source tokens can disappear
   without being represented in the output.

3. Every inscription receives:

   confidence = 1.0

   without a documented provenance basis.

4. The implementation is bound to:

   datasets/egyptian/

   and therefore belongs to the obsolete dataset-specific pipeline.

Decision:

SALVAGE CONCEPT / REWRITE GENERICALLY.

Future importer requirements:

- preserve all source tokens;
- explicitly classify parsed / unresolved / damaged material;
- retain source provenance;
- retain inscription boundaries;
- never silently discard input;
- do not manufacture certainty.

---

## 2. tools/normalize_mdc_corpus.py

Historical role:

- attempted to normalize Gardiner-like token spelling;
- rebuilt basic corpus statistics;
- produced a cleaned corpus file.

Critical scientific defect:

The implementation explicitly deletes every token beginning with:

Ff

It also deletes every token that fails its restricted regular expression.

Therefore normalization is destructive.

Historical observed consequence:

Ff301 occurred repeatedly in the imported MdC source and was removed
by this normalizer.

This token was not independently established as meaningless technical
noise.

Therefore its removal was scientifically unjustified.

Scientific rule derived from this failure:

UNRESOLVED != INVALID.

An unresolved source token must be preserved and marked.

It must not be deleted merely because the current parser does not
understand it.

Decision:

DO NOT MIGRATE IMPLEMENTATION.

Preserve only the lesson:

normalization must be lossless with respect to source observations.

---

## 3. tools/build_egyptian_corpus_sequence.py

Historical role:

- read inscription_id + sequence rows from CSV;
- preserved inscription boundaries;
- constructed per-inscription sign sequences;
- calculated corpus statistics.

Useful concepts:

- explicit inscription identifier;
- sequence contained inside inscription boundary;
- corpus-level token statistics;
- sequence-length statistics.

Limitations:

- dataset-specific paths;
- hard-coded source = "Gardiner";
- hard-coded confidence = 1.0;
- no explicit unresolved/damaged-token representation;
- no generalized ingestion contract.

Decision:

HISTORICAL IMPORT EXAMPLE / DO NOT KEEP AS ACTIVE IMPLEMENTATION.

Useful concepts are already represented by the current architecture:

Corpus
→ inscription records
→ explicit sequences
→ boundary-safe sequence analysis.

---

# Final migration decision

The three legacy corpus scripts do not belong in the active
AncientScriptLab implementation.

Their useful scientific content is now preserved in this record.

Future corpus ingestion must follow:

Source
→ inscription segmentation
→ token/sign observation
→ unresolved/damage preservation
→ identity assignment where justified
→ corpus sequence representation
→ measurement
→ sequence analysis

No stage may silently discard source evidence.

## Final status

tools/import_mdc_corpus.py
    SALVAGE CONCEPT — DELETE LEGACY IMPLEMENTATION

tools/normalize_mdc_corpus.py
    REJECT IMPLEMENTATION — DELETE

tools/build_egyptian_corpus_sequence.py
    PRESERVE CONCEPT — DELETE LEGACY IMPLEMENTATION

After removal, active Python code should contain zero references to:

datasets/egyptian/

The historical Egyptian source remains isolated under the legacy
dataset area and is not promoted to canonical scientific evidence.
