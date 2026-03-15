---
name: tech-debt-analyzer
description: >-
  Systematic tech debt inventory with complexity analysis, dead code detection,
  and remediation planning. Track debt over time. NOT for code review
  (honest-review) or refactoring.
argument-hint: "<mode> [path]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0"
---

# Tech Debt Analyzer

Systematic technical debt inventory, prioritization, and remediation planning.
Multi-pass analysis with confidence scoring and evidence-based findings.

**Scope:** Debt inventory and tracking only. NOT for code review (honest-review), refactoring execution, or dependency updates.

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **debt item** | A discrete tech debt finding with category, severity, confidence, and evidence |
| **category** | Debt classification: design, test, documentation, dependency, infrastructure |
| **severity** | Impact level: CRITICAL, HIGH, MEDIUM, LOW |
| **confidence** | Score 0.0-1.0 per item; >=0.7 report, 0.3-0.7 flag, <0.3 discard |
| **complexity** | Cyclomatic (decision paths) or cognitive (human comprehension difficulty) |
| **dead code** | Functions, classes, or imports with no references in the codebase |
| **staleness** | Days since a dependency's current version was superseded |
| **inconsistency** | Same pattern implemented differently across files |
| **remediation** | Specific fix action with effort estimate and risk level |
| **debt score** | Aggregate metric: sum of (severity_weight x confidence) across all items |
| **baseline** | Previous scan stored at ~/.claude/tech-debt/ for longitudinal comparison |
| **heatmap** | Visual density of debt items per file or directory |
| **risk x effort** | Prioritization matrix: impact vs. remediation cost |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `scan` or `scan <path>` | Full codebase debt inventory (or scoped to path) |
| `analyze <file/dir>` | Targeted deep analysis of specific file or directory |
| `prioritize` | Rank all debt items by risk x effort matrix |
| `roadmap` | Generate phased remediation plan |
| `report` | Render dashboard visualization |
| `track` | Compare current scan against previous baseline |
| Empty | Show mode menu with descriptions and examples |

## Mode: Scan

Full codebase debt inventory. Run all 4 analysis scripts, aggregate results, assign categories and severities.

### Scan Step 1: Project Profile

Run `uv run python skills/tech-debt-analyzer/scripts/complexity-scanner.py <path>` to get complexity metrics.
Parse JSON output. Flag functions with cyclomatic_complexity > 10 as HIGH, > 5 as MEDIUM.

### Scan Step 2: Dead Code Detection

Run `uv run python skills/tech-debt-analyzer/scripts/dead-code-detector.py <path>` to find unused code.
Parse JSON output. Each unused item becomes a debt item (category: design, severity by confidence).

### Scan Step 3: Dependency Staleness

Run `uv run python skills/tech-debt-analyzer/scripts/dependency-staleness-checker.py <path>` to check outdated packages.
Parse JSON output. Deprecated packages are CRITICAL. Staleness > 365 days is HIGH.

### Scan Step 4: Pattern Consistency

Run `uv run python skills/tech-debt-analyzer/scripts/pattern-consistency-checker.py <path>` to detect inconsistencies.
Parse JSON output. Each inconsistency becomes a debt item (category: design).

### Scan Step 5: AI-Augmented Analysis

After script-based detection, perform additional analysis:

1. **Documentation gaps** — scan for undocumented public APIs, missing README sections, stale comments
2. **Test coverage gaps** — Grep for untested modules, missing edge cases, test-to-code ratio
3. **Infrastructure debt** — outdated CI configs, missing linting, inconsistent tooling
4. **Design smells** — God classes, feature envy, shotgun surgery patterns

Assign confidence scores (0.0-1.0) per finding. Research-validate HIGH/CRITICAL items using Grep and codebase evidence.

### Scan Step 6: Aggregate and Classify

Merge all findings into a unified inventory:
- Deduplicate across script outputs
- Assign categories from debt taxonomy (references/debt-taxonomy.md)
- Calculate debt score: sum of (severity_weight x confidence)
- Store baseline at `~/.claude/tech-debt/<project-slug>-<date>.json`

Present findings grouped by category, sorted by severity within each group.

## Mode: Analyze

Targeted deep analysis of a specific file or directory. Run all 4 scripts scoped to the target.
Apply the same 6-step scan process but with deeper per-function analysis.
Include: function-level complexity breakdown, inline dead code, local pattern violations.

## Mode: Prioritize

Rank debt items using risk x effort matrix. Load `references/prioritization-framework.md`.

| | Low Effort | Medium Effort | High Effort |
|---|---|---|---|
| **High Risk** | P0: Fix immediately | P1: Schedule next sprint | P2: Plan for next quarter |
| **Medium Risk** | P1: Schedule next sprint | P2: Plan for next quarter | P3: Backlog |
| **Low Risk** | P2: Quick wins batch | P3: Backlog | P4: Accept or defer |

For each debt item, estimate:
- **Risk**: blast radius x severity x confidence
- **Effort**: LOC affected x complexity x dependency count

Output a ranked list with priority labels (P0-P4).

## Mode: Roadmap

Generate a phased remediation plan. Requires a prior scan (reads baseline from `~/.claude/tech-debt/`).

**Phase structure:**
1. **Quick Wins** (P0 + low-effort P1): immediate fixes, minimal risk
2. **Structural** (remaining P1 + high-risk P2): design improvements, refactoring
3. **Maintenance** (P2 + P3): documentation, test coverage, dependency updates
4. **Strategic** (P3 + P4): architecture changes, long-term improvements

Each phase includes: items, estimated effort, dependencies, success criteria.

## Mode: Report

Render dashboard visualization. Requires a prior scan.

1. Read the most recent baseline from `~/.claude/tech-debt/`
2. Copy `templates/dashboard.html` to a temporary file
3. Inject findings JSON into the `<script id="data">` tag
4. Open in browser or report the path

Dashboard sections: category pie chart, complexity heatmap, trend chart (if multiple baselines), prioritized backlog table.

## Mode: Track

Compare current scan against previous baseline for longitudinal tracking.

1. Run a fresh scan (Mode: Scan steps 1-6)
2. Load previous baseline from `~/.claude/tech-debt/<project-slug>-*.json` (most recent)
3. Compute delta: new items, resolved items, changed severities, score trend
4. Present comparison report with trend indicators

## State Management

- State directory: `~/.claude/tech-debt/`
- Create directory on first use with `mkdir -p`
- Filename: `<project-slug>-<YYYY-MM-DD>.json`
- Project slug: sanitized basename of the project root directory
- Store after every scan; track mode reads historical baselines
- Schema: `{ "project": str, "date": str, "score": float, "items": [...], "summary": {...} }`

## Reference Files

Load ONE reference at a time. Do not preload all references into context.

| File | Content | Read When |
|------|---------|-----------|
| `references/debt-taxonomy.md` | 5 debt categories with subcategories and remediation templates | Scan Step 6, classifying findings |
| `references/complexity-metrics.md` | Cyclomatic and cognitive complexity definitions, thresholds, interpretation | Interpreting complexity-scanner output |
| `references/prioritization-framework.md` | Risk x effort matrix, scoring rubric, priority definitions | Prioritize mode |
| `references/remediation-templates.md` | Fix patterns by issue type, effort estimates, risk ratings | Roadmap mode, generating fix plans |

| Script | When to Run |
|--------|-------------|
| `scripts/complexity-scanner.py` | Scan Steps 1, Analyze mode |
| `scripts/dead-code-detector.py` | Scan Step 2, Analyze mode |
| `scripts/dependency-staleness-checker.py` | Scan Step 3 |
| `scripts/pattern-consistency-checker.py` | Scan Step 4, Analyze mode |

| Template | When to Render |
|----------|----------------|
| `templates/dashboard.html` | Report mode — inject findings JSON into data tag |

## Debt Item Structure

Every debt item follows this format:

1. **Location**: `[file:line]` or `[file:start-end]` — exact source location
2. **Category**: design | test | documentation | dependency | infrastructure
3. **Severity**: CRITICAL | HIGH | MEDIUM | LOW
4. **Confidence**: 0.0-1.0 score with evidence basis
5. **Description**: What the debt is (1-2 sentences)
6. **Impact**: Why it matters (blast radius, risk)
7. **Remediation**: Recommended fix approach with effort estimate

## Critical Rules

1. Run all 4 analysis scripts before presenting findings — partial scans are labeled as such
2. Every finding must have a confidence score backed by evidence (script output or codebase grep)
3. Confidence < 0.3 = discard; 0.3-0.7 = flag as uncertain; >= 0.7 = report
4. Never execute remediation — this skill inventories and plans, not fixes
5. Store baseline after every full scan — longitudinal tracking depends on it
6. Do not report style preferences as debt — only structural, behavioral, or maintainability issues
7. Deduplicate across script outputs — same file:line should not appear twice
8. Prioritize mode requires a prior scan — prompt user to run scan first if no baseline exists
9. Always present the debt score (aggregate metric) in scan output
10. Track mode must show delta (new/resolved/changed) — raw numbers without comparison are useless
11. Dead code detection requires high confidence (>= 0.8) — false positives erode trust
12. Load ONE reference file at a time — do not preload all references
