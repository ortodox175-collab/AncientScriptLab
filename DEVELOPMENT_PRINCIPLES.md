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

