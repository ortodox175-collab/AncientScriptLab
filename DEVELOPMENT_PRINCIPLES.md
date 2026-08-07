# AncientScriptLab

# DEVELOPMENT PRINCIPLES

Version: 1.0

---

## Purpose

This document defines the engineering principles used during the development of AncientScriptLab.

These principles are mandatory.

Every architectural decision, algorithm and implementation must comply with them.

---

## 1. Scientific First

Scientific correctness always has priority over implementation speed.

---

## 2. Roadmap Driven Development

ROADMAP.md is the primary planning document.

Every implementation must directly contribute to the current Milestone.

Ideas unrelated to the current Milestone are moved to BACKLOG.md.

---

## 3. No Premature Infrastructure

Infrastructure is created only when required.

Never build systems "for the future."

---

## 4. Stable Architecture

Architecture is modified only when there is objective evidence that the modification improves the project.

Never refactor simply because another solution looks cleaner.

---

## 5. Complete Deliverables

Whenever possible, code is delivered as complete files.

Preferred format:

cat > filename <<'EOF'

...
## Principle 14 — Reuse Validated Scientific Algorithms

Scientific features should be built hierarchically.

If a scientific quantity can be derived from already validated lower-level
algorithms, those algorithms must be reused instead of reimplementing the
same mathematical logic.

This principle provides several important benefits:

- Single source of scientific truth
- Reduced code duplication
- Improved reproducibility
- Easier maintenance
- Lower probability of mathematical inconsistencies

Example:

Connected Components (T-001)
            │
            ▼
Hole Count (T-002)
            │
            ▼
Euler Characteristic (T-003)

where

Euler Characteristic = Connected Components − Hole Count

Higher-level scientific features should compose validated lower-level
features whenever possible.

---

# AP-07 — automatic archetype discovery principle

## Status

Mandatory architectural principle.

## Formulation

AncientScriptLab **must never assume a fixed number of structural archetypes** for any writing system.

The number of archetypes is treated as a **measurable property of a corpus**, not as a system parameter.

For every corpus the system must:

1. automatically estimate the possible number of structural archetypes;
2. evaluate clustering quality;
3. validate clustering stability;
4. compare multiple independent clustering methods;
5. build a hierarchical archetype spectrum.

## Scientific rationale

Different writing systems may possess different structural complexity.

For example:

- one writing system may contain 3 fundamental archetypes;
- another may contain 12;
- another may contain 47.

Fixing the number of clusters in advance introduces an artificial limitation and may distort the internal structural organization of the corpus.

Therefore the system must **discover archetypes rather than impose them**.

## Mandatory validation procedures

For every corpus the system must evaluate:

- K-means clustering;
- hierarchical clustering;
- Gaussian Mixture Models;
- DBSCAN;
- repeated random initializations;
- bootstrap stability analysis.

An archetype is considered validated only if it remains stable under:

- changes of clustering algorithm;
- changes of the number of clusters;
- random initialization;
- resampling of the corpus.

## Hierarchical model

The system stores not a single value of K, but a **hierarchical spectrum of archetypes**.

For example:

- macro-archetypes;
- meso-archetypes;
- micro-archetypes.

This allows a writing system to be described simultaneously at multiple levels of structural organization.

## Consequence

All AncientScriptLab modules must be designed to operate with a **dynamically determined number of archetypes**.

No module may assume a fixed number of structural classes.

An archetype is **the result of analysis**, not an input parameter.

