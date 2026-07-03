# AncientScriptLab

# DEPENDENCY RULES

Version: 1.0

Status: Active

---

# Purpose

This document defines the allowed dependency directions between all major modules.

Dependencies must always point downward.

Circular dependencies are prohibited.

---

# Dependency Graph

```
Applications

↓

Experiments

↓

Execution

↓

Feature Packs

↓

Algorithms

↓

Context

↓

Geometry

↓

Vector

↓

Utilities
```

---

# Allowed Imports

## Applications

May import any project module.

---

## Experiments

May import:

- execution
- comparison
- normalization
- statistics
- vector
- packs

Must never be imported by lower layers.

---

## Execution

May import:

- algorithms
- context
- registry

Must never import experiments.

---

## Feature Packs

May import:

- algorithms
- vector
- context

Must never import execution.

---

## Algorithms

May import:

- geometry
- context
- utils

Must never import:

- experiments
- execution
- packs
- statistics

---

## Context

May import:

- geometry
- utils

Must never import algorithms.

---

## Geometry

Independent.

Contains only mathematical objects and geometry algorithms.

---

## Statistics

May import:

- vector

Must never import experiments.

---

## Comparison

May import:

- vector

- normalization

Must never import execution.

---

## Normalization

May import:

- vector

- statistics

Must never import experiments.

---

# General Rules

Algorithms never know:

- who executes them;

- who requested them;

- how results will be used.

Algorithms compute only mathematics.

---

# Architectural Principle

Control flows downward.

Scientific knowledge flows upward.

