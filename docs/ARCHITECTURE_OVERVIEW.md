# AncientScriptLab

# ARCHITECTURE OVERVIEW

Version: 1.0

Status: Active

---

# Purpose

This document describes the high-level architecture of AncientScriptLab.

Its purpose is to define:

- module responsibilities;
- allowed dependencies;
- data flow;
- execution flow;
- architectural boundaries.

The architecture is intended to remain stable over the long term.

---

# Architectural Philosophy

AncientScriptLab is built as a collection of small, independent scientific components.

Each component has exactly one clearly defined responsibility.

Modules communicate through well-defined interfaces.

Scientific algorithms remain independent from execution infrastructure.

---

# Core Architecture

```
                    Images
                       │
                       ▼
                Image Loading
                       │
                       ▼
                 Feature Context
                       │
                       ▼
              Execution Engine
                       │
                       ▼
             Registered Algorithms
                       │
                       ▼
                Feature Packs
                       │
                       ▼
                Feature Vector
                       │
                       ▼
               Normalization
                       │
                       ▼
             Distance Metrics
                       │
                       ▼
                 Statistics
                       │
                       ▼
                 Experiments
                       │
                       ▼
             Experiment Results
                       │
                       ▼
          Scientific Interpretation
```

---

# Module Responsibilities

## core/context

Caches expensive computations.

Examples:

- Bounding Box
- Contours
- Skeleton (future)
- Moments (future)

---

## core/execution

Responsible for executing algorithms.

Contains:

- Execution Engine
- Runtime Registry

---

## core/algorithms

Contains independent scientific algorithms.

Each algorithm computes one measurable property.

Algorithms never know about other algorithms.

---

## core/features

Provides interfaces between algorithms and Feature Packs.

---

## core/packs

Groups algorithms into reusable scientific Feature Packs.

Examples:

- Geometry Pack
- Topology Pack (future)
- Skeleton Pack (future)

---

## core/vector

Stores computed Feature Vectors.

Contains no scientific logic.

---

## core/normalization

Implements Feature Vector normalization methods.

Methods are interchangeable.

Managed through Normalization Registry.

---

## core/comparison

Computes distances between Feature Vectors.

Distance metrics remain independent from normalization.

---

## core/statistics

Computes descriptive statistics.

No scientific interpretation is performed here.

---

## core/experiments

Runs scientific experiments.

Contains:

- Experiment
- Experiment Runner
- Experiment Registry
- Experiment Result

---

## registry

Stores scientific Feature Registry definitions.

---

# Allowed Dependencies

The dependency direction must always remain:

```
Algorithms
      ↓
Feature Packs
      ↓
Execution
      ↓
Experiments
```

Never the reverse.

Algorithms must never depend on:

- experiments;
- execution engine;
- feature packs.

---

# Import Rules

Higher-level modules may import lower-level modules.

Lower-level modules must never import higher-level modules.

Example:

Allowed:

Feature Pack
→ Algorithm

Execution Engine
→ Algorithm

Experiment
→ Normalization

Forbidden:

Algorithm
→ Experiment

Algorithm
→ Feature Pack

Algorithm
→ Execution Engine

---

# Scientific Pipeline

Every scientific experiment follows the same workflow.

```
Input Image

↓

Feature Context

↓

Algorithms

↓

Feature Pack

↓

Feature Vector

↓

Normalization

↓

Distance Metrics

↓

Statistics

↓

Experiment

↓

Result

↓

Research Interpretation
```

---

# Design Principles

The architecture follows:

- Single Responsibility Principle
- Open/Closed Principle
- Registry Pattern
- Explainable Scientific Computing
- Reproducible Experiments

---

# Long-Term Stability

Architectural changes are introduced only when they objectively improve:

- scientific correctness;
- reproducibility;
- maintainability;
- modularity;
- long-term scalability.

Architecture is never modified solely for stylistic reasons.

