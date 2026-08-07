# AncientScriptLab

# ARCHITECTURE

Version: 2.0

---

# Purpose

This document describes the high-level architecture of AncientScriptLab.

The architecture is designed to maximize scientific correctness, reproducibility, explainability and long-term maintainability.

---

# Architectural Philosophy

AncientScriptLab is built as a layered scientific platform.

Each layer has a clearly defined responsibility.

Scientific research drives the architecture—not the other way around.

---

# Layer 1 — Scientific Layer

Responsible for defining the scientific methodology.

Components:

- RESEARCH_RULES.md
- ROADMAP.md
- PROJECT_STATE.md
- Mathematical models
- Validation methodology
- Experimental protocols

Responsibilities:

- Define scientific standards.
- Define validation criteria.
- Approve mathematical models.
- Ensure reproducibility.

---

# Layer 2 — Architecture Layer

Responsible for coordinating computations.

Core components:

- Execution Engine
- Runtime Registry
- Feature Registry
- Feature Context
- Feature Vector
- Statistics Framework
- Comparison Framework

Responsibilities:

- Execute algorithms.
- Manage dependencies.
- Cache expensive computations.
- Build feature vectors.
- Coordinate scientific analysis.

---

# Layer 3 — Implementation Layer

Responsible for concrete algorithms.

Components include:

- Geometry algorithms
- Feature Packs
- Image normalization
- Distance computation
- Statistical calculations
- Dataset importers

Responsibilities:

- Perform computations.
- Produce deterministic results.
- Remain independent and reusable.

---

# Architectural Principles

The architecture follows these principles.

## Single Responsibility Principle

Each module has one clearly defined responsibility.

Large universal modules are avoided.

---

## Separation of Data and Computation

Data structures do not perform scientific computations.

Algorithms operate on data provided by the architecture.

---

## Declarative Configuration

Scientific definitions are stored in registries.

Implementation reads the registry rather than embedding metadata in code.

---

## Lazy Evaluation

Expensive computations are performed only when required.

Computed values are cached inside Feature Context.

---

## Stable Interfaces

Modules communicate through stable public interfaces.

Internal implementation may evolve without affecting other components.

---

## Scientific First

Architecture exists to support scientific research.

Implementation convenience never overrides scientific correctness.

---

# Development Workflow

Each Milestone follows the same sequence.

1. Planning

2. Implementation

3. Experimental Validation

4. Architectural Audit

5. Documentation Update

Only validated work becomes part of the Scientific Core.

---

# Current Status

Architecture Status:

Stable

Scientific Core:

Validated

Known Critical Architectural Debt:

None

Future development should focus on scientific validation and expansion rather than architectural redesign.\n\n---\n## Corpus Diagnostics Layer (уровень диагностики корпуса)

Назначение слоя:

оценка вероятности того, что исследуемый корпус является письменной системой.

Используемые группы признаков:

- частотное распределение;
- энтропия;
- условная энтропия;
- повторяемость последовательностей;
- позиционные ограничения;
- графовая структура;
- масштабная устойчивость;
- архитектурная согласованность знаков (GSS).

Выход слоя:

- индекс системности корпуса;
- вероятностная оценка письменной системы;
- отчёт о структурных ограничениях корпуса.\n