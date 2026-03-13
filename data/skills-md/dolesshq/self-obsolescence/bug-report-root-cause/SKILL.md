---
name: bug-report-root-cause
description: Produce per-item root cause analysis from bug report input. Inputs source and target where source is pasted file or linear issue and target is env scope.
metadata:
  short-description: Inputs source target. Bug report to per-item cause matrix with evidence
---

# Bug Report Root Cause

## Goal

Take a bug report (pasted text, file, or Linear issue), investigate each item, and return a root-cause analysis for every item with evidence and classification.

## Invocation syntax

Preferred:

```text
$bug-report-root-cause <source> <target>
```

Examples:

```text
$bug-report-root-cause linear:AGC-278 all-envs
$bug-report-root-cause file:/Users/sawyer/Downloads/agc-278-root-case.md prod+preview
$bug-report-root-cause pasted local-only
$bug-report-root-cause
```

Normalization:

- `source`:
  - `linear:<ISSUE_KEY>` -> fetch issue + related + blocked-by items
  - `file:<ABS_PATH>` -> parse markdown/text file
  - `pasted` -> parse current prompt text
- `target`:
  - `all-envs` -> production + preview + local (when available)
  - `prod+preview` -> production + preview only
  - `local-only` -> local only
- If omitted, default to `pasted all-envs`.

## When to use

Use this skill when the user asks to:

- explain what is causing each bug report item
- investigate a Linear issue and related dependency issues
- determine which items are fixed vs still actionable
- build an interrogation plan and then produce per-item root causes

## Required tools and lanes

Use the minimal set needed, in parallel when possible:

1. `linear` lane
- fetch primary issue and linked issues (`related`, `blockedBy`, and relevant comments)
- extract item list and normalize shorthand labels

2. `browser` lane (`playwright` and/or `agent-browser`)
- reproduce user-visible behavior across selected environments
- capture route, action, observed result, and network/API outcomes

3. `database` lane (`supabase-local`, `supabase-animo`)
- run read-only probes to validate data/model causes
- compare local/preview/production where applicable

4. `synthesis` lane
- map evidence to each bug item
- classify cause and produce remediation direction

## Investigation workflow

1. Build the item inventory
- parse each bullet/item from source
- normalize aliases (for example shorthand labels like building nicknames)
- create one canonical row per item

2. Build interrogation plan per item
- define:
  - browser checks
  - SQL/data checks
  - expected vs observed behavior
- mark dependencies (which checks unblock others)

3. Execute checks in parallel
- run browser and DB probes concurrently per item class
- keep DB access read-only unless user explicitly asks for changes

4. Determine cause per item
- assign one primary classification:
  - `fixed-in-pr`
  - `still-actionable-app-bug`
  - `upstream-data-behavior`
  - `model-semantics`
  - `process-risk`
  - `environment-parity-issue`
- include secondary contributors only when evidence supports them

5. Produce output package
- interrogation plan summary
- per-item cause matrix
- recommended remediation focus (ordered)

## Evidence standards

For each item, include at least two evidence points when feasible:

- browser evidence:
  - URL/route
  - action
  - observed result or API status
- data evidence:
  - query target (table/view/function)
  - key fields proving cause
- optional:
  - issue/PR/comment references

If evidence is missing, mark the item as `insufficient-evidence` and provide next probes.

## Output format

Use this exact structure:

```markdown
Scope:
- source: <linear:KEY | file:path | pasted>
- target: <all-envs | prod+preview | local-only>
- related issues included: <yes/no + keys>

Interrogation plan:
1. <step>
1. <step>
1. <step>

Per-item cause matrix:
| Item | Cause | Evidence | Classification | State |
| --- | --- | --- | --- | --- |
| <item> | <root cause> | <key browser/db evidence> | <classification> | <fixed|wip|open|unknown> |

Open unknowns:
1. <item> — <what is missing and how to verify>

Recommended remediation focus:
1. <highest impact fix>
1. <next fix>
1. <next fix>
```

## Guardrails

- Do not claim root cause without direct evidence; state uncertainty explicitly.
- Do not conflate preview instability with production truth; call out cross-env parity issues.
- Keep any credential handling out of skill files and logs; never store secrets in repository files.
- Prefer read-only DB interrogation unless the user explicitly requests fix implementation.
- Keep item-level conclusions falsifiable with reproducible checks.

## Notes for Linear-driven runs

- If source is `linear:<KEY>`, include:
  - issue description items
  - issues in `related`
  - issues in `blockedBy`
- Exclude unrelated linked issues unless user asks for full graph traversal.

