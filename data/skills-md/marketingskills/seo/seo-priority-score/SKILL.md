---
name: seo-priority-score
description: Rank SEO tasks by expected impact, confidence, effort, authority feasibility, and revenue proximity. Use when Codex needs to decide which of many identified issues to work on first.
---

# SEO Priority Score

## Overview

Given a list of potential SEO tasks (from any Diagnose skill), score each one on a standardized framework and produce a ranked priority list.

## Inputs

- List of SEO tasks or opportunities with supporting data
- Optional: business context (revenue per visitor, conversion rates, margins)

## Workflow

1. For each task, collect or estimate:
   - **Impact**: traffic, conversion, or revenue potential (scale 1-10)
   - **Confidence**: how reliable the signal is (scale 1-5)
   - **Effort**: hours or cost to implement (scale 1-5, inverted)
   - **Authority feasibility**: can the site realistically compete (scale 1-5)
   - **Revenue proximity**: how directly this affects pipeline (scale 1-5)
2. Calculate a composite priority score: `(Impact × Confidence) / (Effort × Authority gap)` with revenue proximity as a multiplier.
3. Group tasks by effort band: quick wins (< 4 hours), medium projects (4-20 hours), strategic initiatives (20+ hours).
4. Output a sorted priority list with the score breakdown.

## Output

Ranked task list with priority score, breakdown, and effort band.
