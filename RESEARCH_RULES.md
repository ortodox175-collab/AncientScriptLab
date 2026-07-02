# AncientScriptLab

# RESEARCH RULES

Version: 1.0

---

## Purpose

This document defines the scientific methodology used throughout the AncientScriptLab project.

All research, mathematical models and experimental results must comply with these rules.

---

# 1. Scientific Objectivity

All conclusions must be supported by measurable evidence.

Subjective interpretation must never replace quantitative analysis.

---

# 2. Experiment Before Conclusion

No scientific conclusion may be accepted without experimental validation.

If an assumption has not been tested, it remains a hypothesis.

---

# 3. Reproducibility

Every experiment must be reproducible.

The same input data must always produce the same results.

---

# 4. Explainability

Every numerical result must be explainable.

The system must answer both:

• How similar are two symbols?

and

• Why are they considered similar?

---

# 5. Mathematical Distance Comes First

Mathematical distance is the primary scientific quantity.

Similarity Score is a derived representation and must never replace the underlying distance.

---

# 6. Contribution Analysis

Every new feature introduced into the mathematical model must undergo Feature Contribution Analysis.

The contribution of each feature to the total distance must be measurable and explainable.

---

# 7. Validation of Mathematical Models

Any modification of the mathematical model requires reproducible validation experiments.

No mathematical model becomes the project standard after a single experiment.

---

# 8. Established Methods First

Whenever a well-established mathematical method satisfies the scientific requirements, it should be preferred over introducing a new custom algorithm.

Novel methods are introduced only when reproducible experiments demonstrate a clear scientific advantage.

---

# 9. Model Before Code Changes

If experimental results contradict expectations:

• first verify the implementation;

• then investigate the mathematical model;

• never modify the implementation simply to obtain expected results.

---

# 10. Normalization Policy

Normalization methods are selected only after quantitative comparison.

Selection must be based on objective evaluation, including:

• distance stability;

• sensitivity to outliers;

• feature dominance;

• behaviour on small datasets;

• behaviour on large datasets;

• numerical stability;

• scientific interpretability;

• reproducibility.

Current project standard:

Min-Max Scaling

Status:

Temporary scientific standard until completion of Milestone M6.4.

---

# 11. Experimental Integrity

Experimental results must never be adjusted to support a hypothesis.

If results contradict expectations, the hypothesis must be re-evaluated.

---

# 12. Incremental Scientific Development

Scientific complexity grows gradually.

Each validated model becomes the foundation for the next stage.

Unvalidated ideas remain in BACKLOG until scheduled by ROADMAP.

---

# 13. Audit Before Research

Before introducing new mathematical models:

• verify the current implementation;

• analyse existing results;

• identify architectural constraints;

• avoid unnecessary redesign.

---

# 14. Architecture Supports Science

Software architecture exists to support scientific research.

Architectural changes are justified only when they improve:

• scientific correctness;

• reproducibility;

• maintainability;

• computational reliability.

---

# 15. Research Documentation

Every completed Milestone must update:

• PROJECT_STATE.md

• ROADMAP.md

• BACKLOG.md (if required)

Scientific knowledge must be preserved inside the repository rather than in external discussions.

---

# Fundamental Scientific Principle

AncientScriptLab is a scientific research platform.

The objective is not to produce attractive similarity scores, but to build an explainable, reproducible and scientifically validated mathematical foundation for the objective analysis and possible decipherment of unknown writing systems.

