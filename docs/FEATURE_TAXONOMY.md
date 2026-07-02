# FEATURE TAXONOMY

Version: 0.1 Draft

Status: Scientific Specification

Project: AncientScriptLab

---

# 1. Purpose

This document defines the complete system of measurable features used by
AncientScriptLab.

A feature is an objectively measurable property of a sign, image,
sequence or corpus.

Feature Taxonomy is the only official source of feature definitions used
throughout the project.

No feature may be implemented unless it is first registered here.

---

# 2. Scope

The taxonomy applies to every symbolic system including but not limited to:

- Indus Script
- Rongorongo
- Linear A
- Proto-Elamite
- Voynich Manuscript
- Unknown symbol systems
- Artificial symbol systems
- Any future corpus

The taxonomy is intentionally independent from language,
chronology, writing system and semantic interpretation.

---

# 3. Scientific Principles

P1. Features describe measurable properties only.

P2. Features never contain semantic interpretation.

P3. Every feature must be reproducible.

P4. Every feature must be computable.

P5. Every feature must have an explicit mathematical definition.

P6. Every feature belongs to exactly one primary category.

P7. Every feature has a unique permanent identifier.

---

# 4. Feature Categories

G  Geometry

T  Topology

S  Skeleton

C  Contour

Y  Symmetry

V  Vision

X  Context

P  Statistical

E  Experimental

---

# 5. Feature Card Standard

Every feature is described using one standard card.

Fields:

- Feature ID
- Name
- Category
- Definition
- Mathematical Definition
- Algorithm
- Input
- Output
- Units
- Dependencies
- Objective
- Scale Invariant
- Rotation Invariant
- Mirror Invariant
- Translation Invariant
- Noise Sensitivity
- Reliability
- Computational Cost
- Scientific Status
- Validation Tests
- References
- Notes

---

# 6. Feature Lifecycle

Proposed

↓

Under Review

↓

Approved

↓

Implemented

↓

Validated

↓

Scientific Ready

Deprecated (optional)

---

# 7. Feature Naming Rules

Feature IDs are permanent.

Examples:

G-001

G-002

T-001

S-001

C-001

X-001

IDs are never reused.

---

# 8. Feature Approval Rules

Before implementation every feature must:

- have mathematical definition
- have algorithm
- define invariance
- define dependencies
- define validation method
- define references

Otherwise implementation is prohibited.
