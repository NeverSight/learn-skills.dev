---
name: workflow-quality-audit
description: Domain-agnostic quality audit pipeline. Enumerates items, loads standards, captures evidence, evaluates per-item, posts structured verdicts, verifies coverage, and summarizes findings. Works for UI components, code review, SDLC, icon design, animation, or any domain with items to audit against criteria.
disable-model-invocation: true
context: fork
agent: general-purpose
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task
---

# Workflow: Quality Audit

A **7-step pipeline** for auditing any collection of items against a set of standards.
Domain-agnostic by design — the caller supplies a config block that plugs in the
item source, standards document, evidence capture method, evaluation template, and
reporting target.

## When to Use

- After completing a body of work (design wave, sprint, migration) that needs QA sign-off
- Before a release to verify quality across a surface area
- For structured reviews: code, visual, accessibility, compliance, performance
- Any time you have **N items** and need a **per-item verdict** against **defined criteria**

## Config Schema

Supply a YAML config block when invoking. All fields are optional — the pipeline
will prompt for missing required fields.

```yaml
# --- Required ---
domain: <string>              # Human label (e.g., "kingly-design-system", "api-endpoints")

items:
  source: <enum>              # bd-children | file-glob | manual-list | api
  parent: <string>            # bd parent bead ID (if source=bd-children)
  glob: <string>              # File glob pattern (if source=file-glob)
  list: [<string>, ...]       # Explicit item list (if source=manual-list)
  api: <string>               # API endpoint/command (if source=api)

standards:
  doc: <path>                 # Path to standards/checklist document
  sections: [<string>, ...]   # Specific sections to evaluate (optional, default=all)
  known_gaps: <string>        # Section to skip or flag separately

# --- Optional ---
evidence:
  type: <enum>                # screenshot | test-run | recording | measurement | source-read
  capture: <string>           # Shell command template for capture
  naming: <string>            # Filename template: {id}, {slug}, {date} supported
  storage: <path>             # Output directory for evidence artifacts

evaluation:
  template: <enum>            # component-audit | visual-audit | code-review | generic | custom
  custom_path: <path>         # Path to custom checklist (if template=custom)
  agents: <int>               # Number of parallel evaluator agents (default: 2)
  parallel: <bool>            # Run evaluators in parallel (default: true)
  split_by: <string>          # How to partition work (e.g., "source-vs-visual", "by-epic")

reporting:
  target: <enum>              # bd-comments | markdown-files | stdout
  verdict_taxonomy: [<string>, ...]  # Custom verdicts (default: [PASS, NEEDS_WORK, BLOCKED])
  output_dir: <path>          # Directory for report files (default: .lev/reports/)

summary:
  format: <enum>              # scorecard | heatmap | backlog (default: scorecard)
```

## Pipeline Steps

### Step 1: INVENTORY

Enumerate all items to audit.

| Source | Method |
|--------|--------|
| `bd-children` | `bd list --parent {parent}` — collects bead IDs + titles |
| `file-glob` | `Glob({glob})` — each matching file is an item |
| `manual-list` | Literal list from config |
| `api` | Execute `{api}` command, parse JSON/lines output |

**Output:** An ordered list of `(id, title/name, metadata)` tuples.
Persist to `.lev/reports/audit-{domain}-{date}/inventory.json`.

### Step 2: STANDARDS

Load and parse the evaluation criteria.

1. Read the `standards.doc` file
2. If `sections` is specified, extract only those sections
3. If `known_gaps` is specified, flag that section as informational (not scored)
4. Parse into a checklist of `(category, criterion, weight)` triples

**Output:** Structured checklist ready for per-item evaluation.

### Step 3: EVIDENCE

Capture per-item evidence using the configured method.

| Type | Method |
|------|--------|
| `screenshot` | Execute `{capture}` command per item, save to `{storage}/{naming}` |
| `test-run` | Execute test suite, capture per-item results |
| `recording` | Capture screen/interaction recording per item |
| `measurement` | Run measurement command, capture metrics |
| `source-read` | Read source files associated with each item |

Evidence is stored at `{storage}/{naming}` with template variables expanded.
If capture fails for an item, mark it `EVIDENCE_FAILED` and continue.

**Output:** Evidence manifest mapping each item ID to its artifact paths.

### Step 4: EVALUATE

Run the evaluation checklist against each item's evidence.

**Team delegation pattern:**
- If `agents > 1` and `parallel: true`, partition items across N evaluator agents
- Each evaluator receives: item subset, standards checklist, evidence paths
- Use `split_by` to control partitioning (round-robin if not specified)

**Per-item evaluation produces:**
```markdown
## {item.title}

### {category_1}
- [ ] {criterion}: {PASS|FAIL} — {note}
- [ ] {criterion}: {PASS|FAIL} — {note}

### {category_2}
...

**Verdict:** {verdict} ({pass_count}/{total_count})
**Issues:**
1. {issue description} — severity: {P0-P3}
```

**Built-in templates** (see `templates/` directory):
- `component-audit` — Visual + Code Quality + Accessibility + Standards Compliance
- `visual-audit` — Visual Fidelity + Storybook Coverage + Code Structure
- `code-review` — Correctness + Style + Performance + Security + Tests
- `generic` — User-defined categories (bare scaffold)
- `custom` — Load from `custom_path`

### Step 5: REPORT

Post the structured verdict for each item.

| Target | Method |
|--------|--------|
| `bd-comments` | `bd comment {item.id} --body "{verdict}"` per item |
| `markdown-files` | Write `{output_dir}/{item.id}-verdict.md` per item |
| `stdout` | Print verdicts to console |

Each verdict includes: item ID, title, verdict label, pass/fail counts, issue list.

### Step 6: VERIFY

Confirm 100% coverage.

1. Load inventory from Step 1
2. Load all verdicts from Step 5
3. Check: every item has exactly one verdict
4. Check: no items are `EVIDENCE_FAILED` without a retry or exception note
5. Check: verdict taxonomy matches config (no unknown labels)

**Output:** Coverage report — `{covered}/{total}` with any gaps listed.

If gaps exist, report them and optionally re-run Steps 3-5 for missing items.

### Step 7: SUMMARIZE

Aggregate findings into a top-level summary.

**Scorecard format (default):**
```
Domain: {domain}
Date: {date}
Items: {total} | PASS: {n} | NEEDS_WORK: {n} | BLOCKED: {n}
Coverage: {covered}/{total} ({pct}%)
Issues: {total_issues} (P0: {n}, P1: {n}, P2: {n}, P3: {n})
Top systemic patterns:
  1. {pattern} — {count} items affected
  2. {pattern} — {count} items affected
```

Write full report to `{output_dir}/audit-{domain}-{date}.md`.

## Team Delegation

For audits with >5 items, delegate to parallel evaluators:

| Role | Responsibility |
|------|---------------|
| **Coordinator** (you) | Steps 1, 2, 6, 7 — inventory, standards, verify, summarize |
| **Evaluator 1..N** | Steps 3-5 — capture evidence, evaluate, post verdicts |

Evaluators receive a self-contained work packet:
- Their item subset (IDs + titles)
- The full standards checklist
- The evidence capture config
- The report template + target config

Evaluators return a manifest: `{items_evaluated, verdicts, issues_found, evidence_paths}`.

## Domain Examples

### UI Components (the original use case)
```yaml
domain: kingly-design-system
items: { source: bd-children, parent: oclaw-top.2 }
standards: { doc: packages/kingly-ui/DESIGN_STANDARDS.md }
evidence: { type: screenshot, capture: "apptestr screenshot" }
evaluation: { template: component-audit, agents: 2, parallel: true }
reporting: { target: bd-comments, verdict_taxonomy: [PASS, NEEDS_WORK] }
```

### Code Review
```yaml
domain: api-endpoints
items: { source: file-glob, glob: "src/routes/**/*.ts" }
standards: { doc: docs/API_STANDARDS.md }
evidence: { type: source-read }
evaluation: { template: code-review, agents: 2 }
reporting: { target: markdown-files, output_dir: .lev/reports/api-review/ }
```

### SDLC / Sprint Review
```yaml
domain: sprint-42
items: { source: bd-children, parent: sprint-42 }
standards: { doc: docs/DEFINITION_OF_DONE.md }
evidence: { type: test-run, capture: "pnpm test --filter {id}" }
evaluation: { template: generic }
reporting: { target: bd-comments, verdict_taxonomy: [SHIP, FIX, HOLD] }
```

### Icon Design
```yaml
domain: app-icons
items: { source: file-glob, glob: "assets/icons/**/*.svg" }
standards: { doc: docs/BRAND_GUIDE.md, sections: [Icons, Color Palette] }
evidence: { type: measurement, capture: "convert {path} -resize 16x16 /tmp/{slug}-16.png" }
evaluation: { template: visual-audit }
reporting: { target: markdown-files, verdict_taxonomy: [APPROVED, REVISE] }
```

## Validation

The audit is complete when:
- [ ] Inventory persisted with item count logged
- [ ] Standards checklist parsed and loaded
- [ ] Evidence captured for all items (or failures documented)
- [ ] Every item has exactly one verdict
- [ ] Coverage is 100% (or gaps explicitly noted)
- [ ] Summary report written to output directory
- [ ] All P0/P1 issues have corresponding tracking items (if using bd)

## Notes

- For `bd-children` source, items inherit the parent's epic/project context
- Evidence capture failures are non-fatal — the item gets `EVIDENCE_FAILED` and continues
- The `known_gaps` standards section is included in reports as informational but not scored
- Parallel evaluation scales linearly: 2 agents = ~2x throughput for >10 items
- Custom verdict taxonomies must have at least 2 labels (one positive, one negative)
- Templates are composable — `component-audit` includes visual + code + a11y categories
