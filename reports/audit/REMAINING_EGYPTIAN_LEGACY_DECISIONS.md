# AncientScriptLab — Remaining Egyptian Legacy Decisions

Status: reviewed after removal of obsolete Egyptian M10 structural pipeline.

Principle:
Preserve scientific concepts and provenance, not obsolete implementations.
No legacy script is promoted to canonical Core merely because it once produced reports.

## A. OBSOLETE DERIVED ANALYSIS — SAFE TO DELETE

### tools/analyze_egyptian_feature_informativeness.py
Decision: DELETE

Reason:
- depends on obsolete Egyptian feature-vector export;
- combines entropy, CV, unique ratio and dominant ratio using unsupported fixed weights;
- thresholds 0.60 / 0.40 are arbitrary;
- individual descriptive statistics may be reimplemented generically later.

### tools/analyze_structural_primitives.py
Decision: DELETE

Reason:
- depends on removed structural_signatures pipeline;
- uses another unsupported composite informativeness score;
- duplicates generic descriptive-statistics concepts.

### tools/audit_primitive_graphs.py
Decision: DELETE

Reason:
- depends on removed primitive_graphs output;
- descriptive summaries are generic and trivial to rebuild when graph measurement returns;
- no need to preserve Egyptian-specific orchestration.

### tools/build_archetype_sequences.py
Decision: DELETE

Reason:
- depends on obsolete hierarchical_archetypes output;
- old hierarchy implementation has already been rejected;
- therefore mapped archetype sequences have no canonical scientific basis.

### tools/map_real_corpus_to_archetypes.py
Decision: DELETE

Reason:
- depends on obsolete hierarchical_archetypes output;
- mapping coverage is useful as a generic future concept;
- current assignments originate from rejected legacy hierarchy.

## B. GARDINER / UNIKEMET PROVENANCE — PRESERVE HISTORY, THEN DELETE BUILDERS

Files:
- tools/build_gardiner_reference_corpus.py
- tools/build_gardiner_registry.py
- tools/build_canonical_gardiner_registry.py
- tools/build_unikemet_registry.py
- tools/build_unikemet_registry_v31.py
- tools/build_unikemet_registry_v32.py
- tools/build_unikemet_registry_v4.py
- tools/build_unikemet_registry_v5.py
- tools/build_unikemet_unicode_registry.py

Decision: HOLD FOR PROVENANCE RECORD, THEN DELETE

Reason:
- these scripts represent successive experimental registry-building attempts;
- different versions interpret UniKemet fields differently;
- source labels/descriptions/categories must remain external metadata and never measurement features;
- canonical Egyptian inventory now lives outside this legacy path.

Required before deletion:
- preserve source/provenance decisions;
- record which UniKemet fields were tested;
- do not silently select one experimental mapping as canonical truth.

## C. CORPUS INGESTION — HOLD / SALVAGE

### tools/import_mdc_corpus.py
Decision: SALVAGE CONCEPT / REWRITE GENERICALLY

Keep:
- inscription-level parsing;
- explicit source metadata;
- token-count statistics;
- MdC as an import format.

Reject:
- regex-only token extraction that silently ignores unresolved material;
- Egyptian-specific output path;
- automatic confidence=1.0 without provenance basis.

Requirement:
future importer must preserve unresolved tokens explicitly.

### tools/normalize_mdc_corpus.py
Decision: DO NOT MIGRATE IMPLEMENTATION

Critical defect:
- unconditionally deletes tokens beginning with Ff;
- drops every token not matching its restricted regex;
- therefore can silently alter the source corpus.

Historical significance:
this implementation documents why unresolved tokens such as Ff301 must be preserved and marked, not deleted.

### tools/build_egyptian_corpus_sequence.py
Decision: HOLD AS LEGACY IMPORT EXAMPLE

Keep concept:
- inscription boundaries;
- sequence construction;
- corpus-level counts.

Reject:
- dataset-specific path and hard-coded source/confidence assumptions.

## Final classification

SAFE DELETE NOW:
- analyze_egyptian_feature_informativeness.py
- analyze_structural_primitives.py
- audit_primitive_graphs.py
- build_archetype_sequences.py
- map_real_corpus_to_archetypes.py

HOLD FOR PROVENANCE THEN DELETE:
- build_gardiner_reference_corpus.py
- build_gardiner_registry.py
- build_canonical_gardiner_registry.py
- build_unikemet_registry.py
- build_unikemet_registry_v31.py
- build_unikemet_registry_v32.py
- build_unikemet_registry_v4.py
- build_unikemet_registry_v5.py
- build_unikemet_unicode_registry.py

HOLD / SALVAGE:
- import_mdc_corpus.py
- normalize_mdc_corpus.py
- build_egyptian_corpus_sequence.py
