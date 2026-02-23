---
name: architecture-validation
description: Dynamically validate that the implemented codebase matches architectural decisions documented in plan files. Use when validating implementation matches planning documents, checking for architecture drift, or preparing for architecture reviews.
---

# Architecture Validation Skill

Dynamically validate that the implemented codebase matches architectural decisions documented in plan files.

## Quick Reference

- **[Dimensions](dimensions.md)** - What gets validated (components, dependencies, APIs, etc.)
- **[Workflow](workflow.md)** - Step-by-step validation process
- **[Extraction Patterns](extraction.md)** - How to extract architectural elements from plans
- **[Compliance](compliance.md)** - Compliance levels and report format
- **[Self-Learning](self-learning.md)** - Continuous improvement framework

## Purpose

**Generic, adaptive framework** that:
- Discovers all plan files in `plans/` directory
- Extracts architectural requirements dynamically
- Validates implementation compliance
- Reports gaps, drift, and violations

**Key Principle**: Be architecture-agnostic. Work with ANY project structure.

## When to Use

- Validating implementation matches planning documents
- Checking for architecture drift after development
- Ensuring design decisions are followed
- Identifying missing implementations
- Preparing for architecture reviews
- Verifying refactoring didn't break boundaries

## Validation Workflow

1. **Discover** - Find all plan files
2. **Extract** - Pull architectural elements
3. **Analyze** - Compare vs codebase
4. **Validate** - Check compliance
5. **Gap Analysis** - Identify missing/drift/extra
6. **Report** - Generate comprehensive report

See **[workflow.md](workflow.md)** for detailed phases and **[dimensions.md](dimensions.md)** for validation categories.
