# AncientScriptLab — Egyptian M10 Legacy Migration Decisions

Status: migration review completed before legacy deletion.

Principle:
Legacy code is not preserved merely because it exists.
Only scientifically justified formulas, concepts, provenance,
or reproducibility checks are migrated.

---

## 1. component_relation_analysis.py

Decision: SALVAGE CONCEPT / REWRITE

Keep:
- idea of measuring relations between structural components;
- quantitative component-relation representation.

Do not preserve implementation blindly:
- dataset-specific paths;
- legacy preprocessing;
- Egyptian-specific orchestration.

Target:
generic structural-relation measurement independent of writing system.

---

## 2. primitive_graph_extraction.py

Decision: SALVAGE CONCEPT / REWRITE

Keep:
- skeleton graph representation;
- node count;
- edge count;
- endpoint count;
- junction count;
- average degree.

Do not treat current implementation as validated:
- skeletonization and graph tracing require independent ground-truth tests;
- graph construction contains implementation assumptions;
- old thresholding is outside canonical FeatureContext preprocessing.

Target:
generic tested graph-measurement module.

---

## 3. primitive_extraction.py

Decision: SALVAGE FORMULAS ONLY / THEN DELETE

Keep where justified:
- endpoint count;
- junction count;
- skeleton length;
- normalized spatial quantities.

Already superseded in current Core:
- connected components;
- holes;
- Euler characteristic;
- foreground density;
- aspect ratio;
- centroid-related geometry.

Do not duplicate canonical Core algorithms.

---

## 4. export_egyptian_feature_vectors.py

Decision: REBUILD AS GENERIC EXPORTER

Keep:
- tabular feature-vector export concept;
- machine-readable CSV/JSON;
- reproducibility metadata concept.

Reject:
- Egyptian-specific paths;
- direct algorithm orchestration outside RuntimeRegistry;
- stale claims such as "CERTIFIED 10/10 PASS";
- broad "validated/certified" scientific claims.

Target:
generic corpus/sign measurement exporter using canonical execution layer.

---

## 5. estimate_archetype_number.py

Decision: SALVAGE METRICS / REPLACE IMPLEMENTATION

Keep:
- silhouette;
- Davies-Bouldin;
- Calinski-Harabasz as separate quantitative diagnostics.

Reject:
- homemade k-means as scientific baseline;
- arbitrary fixed K=2..30 without dataset-dependent constraints;
- declaring best K from silhouette alone as objective truth.

Target:
validated clustering evaluation with deterministic metadata,
separate discovery from stability.

---

## 6. validate_archetype_stability.py

Decision: REWRITE CONCEPT

Keep:
- repeated comparison of clustering outputs;
- silhouette as cluster separation diagnostic;
- ARI as partition agreement metric.

Scientific correction:
- ARI between KMeans / hierarchical / GMM = algorithm agreement,
  NOT clustering stability;
- actual stability requires repeated seeds and/or resampling/bootstrap.

Reject:
- average silhouette across different algorithms as a universal
  objective selector of K.

---

## 7. extract_hierarchical_archetypes.py

Decision: REPLACE IMPLEMENTATION

Reject current hierarchy construction as scientific baseline because it uses
unsupported hard-coded choices such as:
- macro clusters = 3;
- len < 6;
- len // 40;
- len < 4;
- len // 20;
- max/min cluster-count heuristics.

Keep only:
- concept of hierarchical structural grouping.

Any future hierarchy must be derived from explicit,
validated quantitative criteria.

---

## 8. spatial_distribution_analysis.py

Decision: SALVAGE METRICS / REWRITE GENERICALLY

Potentially useful measurements:
- normalized centroid;
- quadrant mass fractions;
- vertical-third mass fractions;
- horizontal-third mass fractions;
- core/outer mass fractions.

Requirements before migration:
- precise coordinate conventions;
- normalization definitions;
- translation/scale sensitivity tests;
- no Egyptian-specific implementation.

---

## 9. run_m10_pipeline_validation.py

Decision: SALVAGE PIPELINE-INTEGRITY CONCEPT

Keep:
- existence checks;
- JSON parse checks;
- record-count consistency checks;
- reproducibility/integrity report concept.

Reject:
- treating file existence as scientific validation;
- hard-coded expected hierarchy counts 3 / 10 / 27;
- M10-specific paths and scientific PASS claims.

Target:
generic pipeline integrity validator.

---

# Final classification

SALVAGE / REWRITE:
- component_relation_analysis.py
- primitive_graph_extraction.py
- primitive_extraction.py
- export_egyptian_feature_vectors.py
- estimate_archetype_number.py
- validate_archetype_stability.py
- extract_hierarchical_archetypes.py
- spatial_distribution_analysis.py
- run_m10_pipeline_validation.py

No legacy implementation above is accepted unchanged as canonical Core.

Migration must occur only when the corresponding functionality
is reached again in the current roadmap.

Until then this document preserves the useful concepts sufficiently
for safe removal of the obsolete Egyptian M10 implementations.
