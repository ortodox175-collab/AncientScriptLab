# AncientScriptLab

# BACKLOG

Version: 1.0

---

## Research Ideas

### BI-001 — Rich Feature Registry

**Priority:** Low

**Status:** Backlog

**Description**

В будущем реестр признаков (Feature Registry) может стать полноценной научной спецификацией каждого признака, а не только его регистрационной записью.

Каждый признак сможет содержать дополнительные метаданные:

- категория;
- алгоритм вычисления;
- единицы измерения;
- возможность нормализации;
- участие в сравнении;
- описание;
- версия появления;
- статус научной готовности;
- связанные тесты;
- ссылки на документацию.

Возможная структура записи:

```text
id: G-008
name: Centroid X
category: Geometry
algorithm: centroid_x
units: pixels
normalized: true
comparable: true
description: X-coordinate of the centroid.
validation_status: Scientific Ready
introduced_in: M3
tests:
  - test_centroid_x.py
```

**Motivation**

Такой реестр позволит автоматически:

- проверять полноту реализации признаков;
- контролировать наличие тестов;
- автоматически строить документацию;
- отслеживать историю развития признаков;
- контролировать научную готовность каждого признака.

**Important**

Не относится к текущему Milestone.

Рассматривать только после завершения базовой архитектуры проекта.

---

## Research Ideas

### BI-002 — Scientific Consistency Validation Framework

**Priority:** Medium

**Status:** Backlog

**Description**

Создать отдельный уровень научной валидации, который проверяет не отдельные алгоритмы, а математическую согласованность результатов нескольких алгоритмов одновременно.

В отличие от Unit Tests и Pipeline Tests, такие проверки должны подтверждать выполнение фундаментальных математических законов и инвариантов.

Примеры:

- Euler Characteristic = Connected Components − Hole Count;
- Largest Component Area ≤ Foreground Area;
- Foreground Area ≤ Bounding Box Area;
- количество отверстий не может превышать число компонент в невозможных конфигурациях;
- другие научные инварианты по мере развития проекта.

Возможная структура:

```text
tests/
    scientific/
        test_topology_consistency.py
        test_geometry_consistency.py
        test_cross_pack_consistency.py
```

или

```text
tools/
    scientific_validation/
```

**Motivation**

Такой уровень проверки позволит:

- подтверждать математическую корректность всей системы;
- обнаруживать ошибки взаимодействия алгоритмов;
- контролировать научную достоверность результатов;
- предотвращать внутренние противоречия между пакетами;
- повысить доверие к результатам исследований.

**Important**

Данная система должна быть реализована только после завершения базовых Feature Packs.

Scientific Consistency Tests являются дополнительным уровнем проверки и не заменяют:

- Unit Tests;
- Pipeline Integration Tests;
- научную валидацию алгоритмов на реальных данных.
---

## BI-002: Reconstruction of proto-writing systems

**Priority:** Long-term research

### Objective

Investigate whether the earliest known writing and proto-writing systems can be represented by a common mathematical structural model.

### Candidate corpora

- Jiahu symbols
- Vinča signs
- Tărtăria tablets
- Uruk pictographic signs
- Proto-Cuneiform
- Proto-Egyptian
- Proto-Elamite

### Research hypothesis

Instead of reconstructing a historical proto-language, reconstruct the **minimal universal graphical system** capable of generating the structural properties observed in the earliest writing systems.

### Possible methodology

- FeatureVector comparison
- Topological invariants
- Geometric primitive analysis
- Graph representations
- Distributional comparison
- Generative reconstruction models
- Evolutionary structural modeling

### Expected outcome

A mathematically testable model of early writing evolution and a structural proximity framework for proto-writing systems.

**Status:** Deferred until completion of the core comparative corpus framework (M8+).

