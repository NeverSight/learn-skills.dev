---
name: project-health-check
description: Audits the project for modern and Waterfall standards (SDLC, CI/CD, Tests, Quality Metrics) and provides a health score with improvement suggestions.
status: implemented
category: Governance & Security
last_updated: '2026-02-13'
tags:
  - compliance
  - gemini-skill
  - qa
related_skills:
  - html-reporter
  - security-scanner
---

# Project Health Check

## Overview

This skill evaluates a project's adherence to both modern engineering practices and traditional quality standards.

### 1. Structural & SDLC Audit

- **Waterfall Compliance**: Checks for phase-gate deliverables (RD, Design, Test Plans) defined in `knowledge/sdlc/waterfall_standard.md`.
- **Modern Standards**: Audits CI/CD, Testing frameworks, Linting, IaC, and Docs.

### 2. Quantitative Quality Audit

- **Metrics Evaluation**: Compares test and bug densities against IPA benchmarks in `knowledge/quality-management/metrics_standards.md`.
- **Health Scoring**: Provides a cumulative score (0-100) with prioritized improvement suggestions.

## Usage

Run the audit script from the root of the project you want to check.

```bash
node project-health-check/scripts/audit.cjs
```

## Interpretation

- **PASS**: The criterion is met.
- **WARN**: Partial compliance (e.g., bug density too low compared to test count).
- **FAIL**: Critical standard or required SDLC deliverable missing.

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
