---
name: skill-stocktake
description: Audit skills and commands for quality. Supports Quick Scan (changed only) and Full Stocktake modes with batch evaluation.
---

# Skill Stocktake

Audits all installed skills and commands using a quality checklist + AI holistic judgment. Supports two modes: Quick Scan for recently changed skills, and Full Stocktake for complete review.

## Scope

The command targets skill directories relative to the invocation path:

| Path | Description |
|------|-------------|
| Global skills directory | Skills available to all projects |
| `{cwd}/skills/` | Project-level skills (if present) |

At the start of Phase 1, explicitly list which paths were found and scanned.

## Modes

| Mode | Trigger | Duration |
|------|---------|---------|
| Quick Scan | `results.json` exists (default) | 5–10 min |
| Full Stocktake | `results.json` absent, or explicit `full` flag | 20–30 min |

## Quick Scan Flow

Re-evaluate only skills that changed since the last run:

1. Read `results.json`
2. Run: `bash scripts/quick-diff.sh results.json`
3. If output is `[]`: report "No changes since last run." and stop
4. Re-evaluate only changed files using Phase 2 criteria
5. Carry forward unchanged skills from previous results
6. Output only the diff
7. Save merged results

## Full Stocktake Flow

### Phase 1 — Inventory

Run: `bash scripts/scan.sh`

The script enumerates skill files, extracts frontmatter, and collects UTC mtimes.

```
Scanning:
  ✓ global skills/         (17 files)
  ✗ {cwd}/skills/          (not found — global skills only)
```

| Skill | 7d use | 30d use | Description |
|-------|--------|---------|-------------|

### Phase 2 — Quality Evaluation

Launch a general-purpose sub-agent with the full inventory and checklist. Process ~20 skills per invocation to keep context manageable. Save intermediate results (`status: "in_progress"`) after each chunk. Resume from the first unevaluated skill if interrupted.

Each skill is evaluated against:

```
- [ ] Content overlap with other skills checked
- [ ] Overlap with project-level config checked
- [ ] Freshness of technical references verified (web search if CLI flags / APIs are present)
- [ ] Usage frequency considered
```

Verdict criteria:

| Verdict | Meaning |
|---------|---------|
| Keep | Useful and current |
| Improve | Worth keeping, specific improvements needed |
| Update | Referenced technology is outdated |
| Retire | Low quality, stale, or cost-asymmetric |
| Merge into [X] | Substantial overlap with another skill |

Evaluation is **holistic AI judgment**. Guiding dimensions:
- **Actionability**: code examples, commands, or steps that let you act immediately
- **Scope fit**: name, trigger, and content are aligned
- **Uniqueness**: value not replaceable by another skill or project config
- **Currency**: technical references work in the current environment

**Reason quality** — the `reason` field is self-contained and decision-enabling:
- For **Retire**: state what defect was found and what covers the same need
- For **Merge**: name the target and describe what content to integrate
- For **Improve**: describe the specific change (section, action, target size)
- For **Keep**: restate the verdict rationale (not just "unchanged")

### Phase 3 — Summary Table

| Skill | 7d use | Verdict | Reason |
|-------|--------|---------|--------|

### Phase 4 — Consolidation

1. **Retire / Merge**: present justification per file before confirming with user
2. **Improve**: present specific suggestions with rationale
3. **Update**: present updated content with sources checked

Archive / delete operations always require explicit user confirmation.

## Results File Schema

`results.json`:

**`evaluated_at`**: set to actual UTC time of evaluation completion (`date -u +%Y-%m-%dT%H:%M:%SZ`).

```json
{
  "evaluated_at": "2026-02-21T10:00:00Z",
  "mode": "full",
  "batch_progress": { "total": 80, "evaluated": 80, "status": "completed" },
  "skills": {
    "skill-name": {
      "path": "skills/skill-name/SKILL.md",
      "verdict": "Keep",
      "reason": "Concrete, actionable, unique value for X workflow",
      "mtime": "2026-01-15T08:30:00Z"
    }
  }
}
```

## Notes

- Evaluation is blind: same checklist applies to all skills regardless of origin
- No verdict branching by skill origin
