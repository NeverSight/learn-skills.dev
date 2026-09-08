---
name: skill-stocktake
description: >-
  Use when auditing Claude skills and commands for quality. Supports Quick Scan (changed skills only), Full Stocktake, and Overview modes with sequential subagent batch evaluation.
arguments: mode
argument-hint: |-
   "[full|quick|overview] -- audit mode (default: overview)"
disable-model-invocation: true

---
# skill-stocktake

Slash command (`/skill-stocktake`) that audits all Claude skills and commands using a quality checklist + AI holistic judgment. Supports three modes: Overview for quick stats, Quick Scan for recently changed skills, and Full Stocktake for a complete review.

## Requirements

- Python 3.11+
- `uv` — for running Python scripts

## CLI Commands

```bash
uv run $SKILL_DIR/scripts/stocktake.py <command> [options]

Commands:
  scan        Phase 1: Inventory all skills
  diff        Quick Scan: Find changed skills since last run
  overview    Quick overview with usage stats (today, 7d, 30d)
  summary     Phase 3: Display results table
  save        Merge evaluation results into results.json
  merge-chunks Merge chunked evaluation results

Global options:
  --width N   Override terminal width for rich output
  --output json|rich|markdown   Output format
```

## Overview Mode

Quick snapshot of all skills with usage statistics:

```bash
uv run $SKILL_DIR/scripts/stocktake.py overview [--width 120]
```

Displays a table with:
- Skill name
- Today's usage count
- 7-day usage count
- 30-day usage count
- Description

## Scope

The command targets the following paths **relative to the directory where it is invoked**:

| Path | Description |
|------|-------------|
| `~/.claude/skills/` | Global skills (all projects) |
| `{cwd}/.claude/skills/` | Project-level skills (if the directory exists) |

**At the start of Phase 1, the command explicitly lists which paths were found and scanned.**

### Targeting a specific project

If the project has no `.claude/skills/` directory, only global skills and commands are evaluated.

## Modes

| Mode | Trigger | Duration |
|------|---------|---------|
| Quick Scan | `results.json` exists (default) | 5–10 min |
| Full Stocktake | `results.json` absent, or `/skill-stocktake full` | 20–30 min |

**Results cache:** `~/.claude/lsz/skill-stocktake/results.json`

## Quick Scan Flow

Re-evaluate only skills that have changed since the last run (5–10 min).

1. Run: `uv run $SKILL_DIR/scripts/stocktake.py diff`
2. If output shows no changes: report "No changes since last run." and stop
3. Re-evaluate only those changed files using the same Phase 2 criteria
4. Carry forward unchanged skills from previous results
5. Output only the diff
6. Save results: `uv run $SKILL_DIR/scripts/stocktake.py save < eval.json`

## Full Stocktake Flow

### Phase 1 — Inventory

Run: `uv run $SKILL_DIR/scripts/stocktake.py scan`

The script enumerates skill files, extracts frontmatter, aggregates observations, and outputs structured JSON or rich terminal display.

Options:
- `--global-dir PATH` — Override global skills directory
- `--project-dir PATH` — Override project skills directory
- `--observations-dir PATH` — Override observations directory
- `--output json|rich|markdown` — Output format (default: rich)

Present the scan summary and inventory table from the script output.

### Phase 2 — Quality Evaluation

Launch parallel Agent tool subagents (**general-purpose agent**) with chunked inventory and checklist:

```text
Agent(
  subagent_type="general-purpose",
  prompt="
Evaluate the following skill inventory against the checklist.

[INVENTORY JSON array]

[CHECKLIST]

Return JSON array for each evaluated skill:
[{ "path": "...", "verdict": "Keep", "reason": "..." }, ...]
"
)
```

The subagent reads each skill, applies the checklist, and returns per-skill JSON array:

```json
[
  { "path": "~/.claude/skills/brainstorming/SKILL.md", "verdict": "Keep", "reason": "..." }
]
```

**Chunk guidance:** Process ~15 skills per subagent invocation. Launch chunks in parallel.

**Chunked file workflow:**
1. Save scan inventory to temp: `uv run $SKILL_DIR/scripts/stocktake.py scan --output json > ~/.claude/lsz/skill-stocktake/.tmp/inventory.json`
2. Save each chunk's evaluation output to: `~/.claude/lsz/skill-stocktake/.tmp/chunk_{N}.json`
3. After all chunks complete, merge with inventory:
   ```
   uv run $SKILL_DIR/scripts/stocktake.py merge-chunks \
     --inventory ~/.claude/lsz/skill-stocktake/.tmp/inventory.json \
     --clean
   ```
4. The `--clean` flag removes `.tmp/` directory after merge

**Usage data:** The inventory is an array of objects with `path`, `name`, `description`, `use_7d`, `use_30d`, `mtime`. The `merge-chunks` command merges evaluation results with inventory using `path` as the join key.

After all skills are evaluated: set `status: "completed"`, proceed to Phase 3.

**Resume detection:** If `status: "in_progress"` is found on startup, check for existing chunk files in `.tmp/` and resume incomplete chunks.

Each skill is evaluated against this checklist:

```
- [ ] Content overlap with other skills checked
- [ ] Overlap with MEMORY.md / CLAUDE.md checked
- [ ] Freshness of technical references verified (use WebSearch if tool names / CLI flags / APIs are present)
- [ ] Usage frequency considered
```

Verdict criteria:

| Verdict | Meaning |
|---------|---------|
| Keep | Useful and current |
| Improve | Worth keeping, but specific improvements needed |
| Update | Referenced technology is outdated (verify with WebSearch) |
| Retire | Low quality, stale, or cost-asymmetric |
| Merge into [X] | Substantial overlap with another skill; name the merge target |

Evaluation is **holistic AI judgment** — not a numeric rubric. Guiding dimensions:
- **Actionability**: code examples, commands, or steps that let you act immediately
- **Scope fit**: name, trigger, and content are aligned; not too broad or narrow
- **Uniqueness**: value not replaceable by MEMORY.md / CLAUDE.md / another skill
- **Currency**: technical references work in the current environment

**Reason quality requirements** — the `reason` field must be self-contained and decision-enabling:
- Do NOT write "unchanged" alone — always restate the core evidence
- For **Retire**: state (1) what specific defect was found, (2) what covers the same need instead
  - Bad: `"Superseded"`
  - Good: `"disable-model-invocation: true already set; superseded by continuous-learning-v2 which covers all the same patterns plus confidence scoring. No unique content remains."`
- For **Merge**: name the target and describe what content to integrate
  - Bad: `"Overlaps with X"`
  - Good: `"42-line thin content; Step 4 of chatlog-to-article already covers the same workflow. Integrate the 'article angle' tip as a note in that skill."`
- For **Improve**: describe the specific change needed (what section, what action, target size if relevant)
  - Bad: `"Too long"`
  - Good: `"276 lines; Section 'Framework Comparison' (L80–140) duplicates ai-era-architecture-principles; delete it to reach ~150 lines."`
- For **Keep** (mtime-only change in Quick Scan): restate the original verdict rationale, do not write "unchanged"
  - Bad: `"Unchanged"`
  - Good: `"mtime updated but content unchanged. Unique Python reference explicitly imported by rules/python/; no overlap found."`

### Phase 3 — Summary Table

Run: `uv run $SKILL_DIR/scripts/stocktake.py summary`

Reads results.json and outputs formatted summary table grouped by verdict.

Options:
- `--results PATH` — Path to results.json
- `--output rich|markdown|json` — Output format (default: rich)
- `--group-by verdict|skill` — Grouping (default: verdict)

### Phase 4 — Consolidation

1. **Retire / Merge**: present detailed justification per file before confirming with user:
   - What specific problem was found (overlap, staleness, broken references, etc.)
   - What alternative covers the same functionality (for Retire: which existing skill/rule; for Merge: the target file and what content to integrate)
   - Impact of removal (any dependent skills, MEMORY.md references, or workflows affected)
2. **Improve**: present specific improvement suggestions with rationale:
   - What to change and why (e.g., "trim 430→200 lines because sections X/Y duplicate python-patterns")
   - User decides whether to act
3. **Update**: present updated content with sources checked
4. Check MEMORY.md line count; propose compression if >100 lines

## Results File Schema

`~/.claude/lsz/skill-stocktake/results.json`:

**`evaluated_at`**: Must be set to the actual UTC time of evaluation completion.
Obtain via Bash: `date -u +%Y-%m-%dT%H:%M:%SZ`. Never use a date-only approximation like `T00:00:00Z`.

```json
{
  "evaluated_at": "2026-02-21T10:00:00Z",
  "mode": "full",
  "batch_progress": {
    "total": 80,
    "evaluated": 80,
    "status": "completed"
  },
  "skills": [
    {
      "path": "~/.claude/skills/brainstorming/SKILL.md",
      "name": "brainstorming",
      "verdict": "Keep",
      "reason": "Concrete, actionable, unique value for X workflow",
      "use_7d": 4,
      "use_30d": 6,
      "mtime": "2026-01-15T08:30:00Z"
    }
  ]
}
```

**Required fields per skill:** `path`, `verdict`, `reason`
**Inherited from inventory:** `name`, `use_7d`, `use_30d`, `mtime`

## Notes

- Evaluation is blind: the same checklist applies to all skills regardless of origin (LSZ, self-authored, auto-extracted)
- Archive / delete operations always require explicit user confirmation
- No verdict branching by skill origin
