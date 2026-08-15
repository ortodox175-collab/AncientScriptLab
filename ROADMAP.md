# AncientScriptLab

# ROADMAP

Version: 2.0

Status: Active

---

# Development Strategy

ROADMAP is the primary planning document of the project.

All development must follow the current Milestone.

Features outside the current Milestone are not implemented immediately and must be moved to BACKLOG.md.

---

# Completed Milestones

## M1 — Core Architecture

Status: Completed

Objectives:

✓ Project structure

✓ Core data model

✓ Basic architecture

---

## M2 — Image Processing

Status: Completed

Objectives:

✓ Image loading

✓ Binary preprocessing

✓ Basic normalization

---

## M3 — Geometry Foundation

Status: Completed

Objectives:

✓ Geometry primitives

✓ Bounding Box

✓ Center normalization

✓ Geometry algorithms

---

## M4 — Feature Extraction

Status: Completed

Objectives:

✓ Feature extraction framework

✓ Geometry Feature Pack

✓ Feature Registry integration

---

## M5 — Validation Framework

Status: Completed

Objectives:

✓ Reference datasets

✓ Validation tools

✓ Regression testing

✓ Scientific reproducibility

---

## M6 — Scientific Core

Status: In Progress

Objectives:

✓ Execution Engine

✓ Runtime Registry

✓ Feature Context

✓ Feature Vector

✓ Feature Statistics

✓ Feature Distance

✓ Feature Normalization

✓ Contribution Analysis

Current focus:

Scientific validation of the mathematical model.

---

## M6.4 — Validation of Normalization Methods

Status: Planned

Purpose:

Determine which feature normalization method produces the most stable, reproducible and scientifically interpretable feature space.

Candidate methods:

• Min-Max Scaling

• Z-Score Standardization

• Robust Scaling (Median / IQR)

• Percentile Scaling

• Log Scaling (if required)

• No Normalization (control experiment)

Validation criteria:

• Distance stability

• Sensitivity to outliers

• Feature dominance

• Behaviour on small datasets

• Behaviour on large datasets

• Numerical stability

• Scientific interpretability

• Reproducibility

Scientific rules:

• Every method uses identical validation datasets.

• Every method undergoes Feature Contribution Analysis.

• No method becomes the project standard after a single experiment.

Expected result:

One normalization method becomes the AncientScriptLab scientific standard.

Alternative methods remain available only for research.

---

## M7 — Scientific Expansion

Status: Planned

Objectives:

• Extend Feature Registry

• Introduce additional validated feature packs

• Expand statistical analysis

• Improve corpus analysis capabilities

---

## M8 — Script Analysis

Status: Planned

Objectives:

• Symbol clustering

• Variant detection

• Structural analysis

• Writing system modelling

---

## M9 — Decipherment Support

Status: Planned

Objectives:

• Statistical hypothesis generation

• Comparison with known writing systems

• Explainable similarity analysis

• Research assistance tools

---

# Development Rules

Development always follows this sequence:

1. Planning

2. Implementation

3. Experimental validation

4. Architectural audit

5. Documentation update

Only after successful validation may the next Milestone begin.

---

# Long-Term Vision

AncientScriptLab aims to become a universal scientific laboratory for objective, reproducible and explainable measurement and analysis of known and unknown writing systems.

The project prioritizes scientific correctness, reproducibility and explainable mathematical models over implementation speed or feature quantity.

