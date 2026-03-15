---
name: repo-elegance-review
description: Audit software repositories for elegance/cleanliness/organization and explain why they feel messy or polished. Use when a user asks if a repo is pretty/elegant/clean, wants a codebase aesthetics review, or needs actionable steps to improve structure, naming, cohesion, repo hygiene, or documentation.
---

# Repo Elegance Review

## Overview

Evaluate a codebase for elegance by scanning structure, naming, boundaries, and repo hygiene, then deliver a concise verdict with evidence and prioritized improvements.

## Workflow

### 1) Calibrate

- Ask 1-2 quick questions if “pretty/elegant” is undefined: what they value (structure vs. velocity vs. readability), scope (whole repo vs. area), and constraints (stage/team size).
- Proceed with the default rubric if the user does not respond.

### 2) Quick Scan (lightweight)

- Map the top-level layout with `ls`, `rg --files`, and `find . -maxdepth 2 -type d`.
- Read `README.md`, primary config (`package.json`, `pyproject.toml`, etc.), and `.gitignore`.
- Sample a few key directories; avoid full-depth reads unless asked.
- If it is a git repo, check `git status -s` for untracked noise.

### 3) Assess Against the Rubric

Evaluate each category; collect 1-3 concrete examples per issue with file paths.

- Repo hygiene and clutter (root noise, generated artifacts, ignores not matching reality)
- Information architecture (clear domains, predictable placement, shallow navigation)
- Boundaries and layering (separation of concerns, minimal cross-coupling)
- Naming consistency (directories, modules, types, config alignment)
- Duplication and drift (parallel folders, overlapping responsibilities)
- Dependency and config coherence (single source of truth, minimal duplicative tooling)
- Tests and tooling (test discipline, coverage expectations, docs match behavior)
- Docs and onboarding (README accuracy, quick start reliability, minimal tribal knowledge)

### 4) Synthesize and Prioritize

- Summarize the top reasons the repo feels elegant or messy.
- Order actions by impact on cognitive load and maintainability.
- Tie each action to its rationale and the evidence that motivated it.

## Output Format

Use this structure:

- Verdict: `Pretty` / `Mixed` / `Not pretty`
- Why: 2-3 bullets with the main reasons
- Strengths: 2-5 bullets
- Issues: bullets formatted as `[Severity] Issue — Evidence (file paths) — Impact`
- Actions: numbered list; each item includes the change, why it helps, and where to start (file paths)
- Questions: only if critical uncertainty blocks a confident recommendation

## Heuristics

- Favor clarity and predictability over cleverness.
- Minimize cognitive load: fewer places to look, fewer naming variants.
- Prefer cohesive modules and explicit boundaries.
- Keep the root clean; move artifacts to `work/`, `tmp/`, or `out/` and align `.gitignore`.
- Keep docs synchronized with reality; stale docs are anti-elegant.

## Pitfalls to Avoid

- Do not nitpick formatting if it does not affect comprehension.
- Do not claim issues without evidence from the repo.
- Do not run heavy commands or full test suites unless the user asks.
