---
description: Assess documentation impact and update affected docs for a code, API, config, or operator workflow change. Use when a change affects documented behavior, when asked to update stale docs or reconcile docs with code, or when a decision or status recorded in plans or ADRs changed. Do not use for trivial changes with no documented surface, or for drafting new product copy from scratch.
name: docs-update
---

# Update Documentation

You are the agent keeping docs truthful after a change. Work in order: scope the change, find the authoritative sources, assess each documentation category separately, edit only affected sources, verify every claim, then summarize.

## 1. Scope the change and find sources

Name the behavior change (code, API, config, or operator workflow) and locate the authoritative sources that describe it: the changed code or config, its tests, and the docs that claim to cover it. Consult the environment for available tools and current help (repo scripts, `--help` output) instead of relying on remembered paths.

## 2. Assess each category separately

Assess internal docs, user-facing docs, changelog or release notes, and required changesets separately. For each category, either update it or record a concise reason it needs no update. Keep the assessment proportionate to the change.

Respect project documentation conventions, explicit docs opt-outs, and safety rules. The absence of docs is not permission to create a large new hierarchy. Do not invent ADRs for a trivial change or new requirements; update plans and ADRs only when a recorded decision or status actually changed, preserving the historical record with amendments rather than rewriting history.

## 3. Edit only affected sources

Edit only the affected authoritative sources. Generated docs are never patched by hand: edit the canonical input and regenerate through the authorized workflow when regeneration is available; when it is not, report the blocker instead of patching the output.

## 4. Verify claims with repo tools

Verify factual claims against current code and config. Check that links resolve, examples run, and operator scripts or checks produce their expected success or failure signals, using the repository's existing tools. A local docs task completes without publishing: no mandatory PR, and no tool installs without user or project authorization.

## 5. Summarize

Report the actual edits per category, the checks run with their results, and the unresolved gaps. Keep reference files alongside the main file only when a genuinely distinct branch needs them and the pointer stays reliable; one concise file is enough otherwise.
