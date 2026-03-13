---
name: validation
description: 'Full validation phase orchestrator. Vibe + post-mortem + retro + forge. Reviews implementation quality, extracts learnings, feeds the knowledge flywheel. Triggers: "validation", "validate", "validate work", "review and learn", "validation phase", "post-implementation review".'
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
metadata:
  tier: meta
  dependencies:
    - vibe        # required - code quality review
    - post-mortem # required - retrospective analysis
    - retro       # optional - quick learning capture
    - forge       # optional - transcript mining
    - shared      # optional - CLI fallback table
---

# /validation — Full Validation Phase Orchestrator

> **Quick Ref:** Vibe → post-mortem → retro → forge. Reviews implementation quality, extracts learnings, and feeds the knowledge flywheel.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Quick Start

```bash
/validation ag-5k2                        # validate epic with full close-out
/validation                               # validate recent work (no epic)
/validation --complexity=full ag-5k2      # force full council ceremony
/validation --no-retro ag-5k2             # skip retro + forge
/validation --no-forge ag-5k2             # skip forge only
```

## Architecture

```
/validation [<epic-id>] [--complexity=<fast|standard|full>] [--no-retro] [--no-forge]
  │
  ├── Step 1: Vibe (gate)
  │   └── /vibe recent — code quality + council review
  │       PASS/WARN → proceed to learning capture
  │       FAIL → signal re-implementation needed
  │
  ├── Step 2: Post-mortem
  │   └── /post-mortem <epic-id> — retrospective analysis
  │
  ├── Step 3: Retro (optional)
  │   └── /retro — quick-capture session learnings
  │
  └── Step 4: Forge (optional)
      └── /forge — mine transcripts for patterns + decisions
```

## Execution Steps

### Step 0: Setup

```bash
mkdir -p .agents/rpi
```

Initialize state:

```
validation_state = {
  epic_id: "<epic-id or null>",
  complexity: <fast|standard|full or null for auto-detect>,
  no_retro: <true if --no-retro>,
  no_forge: <true if --no-forge>,
  vibe_verdict: null,
  post_mortem_verdict: null,
  attempt: 1
}
```

**Load execution packet** (if available):

```bash
if [[ -f .agents/rpi/execution-packet.json ]]; then
  # Read contract surfaces, done_criteria, complexity from packet
  # Use for scoping vibe and post-mortem
fi
```

**Auto-detect complexity** (if not overridden and execution-packet exists):
- Read `complexity` field from execution-packet
- If no packet: default to `standard`

**CLI dependency detection:**

```bash
if command -v ao &>/dev/null; then AO_AVAILABLE=true; else AO_AVAILABLE=false; fi
```

### Step 1: Vibe (gate)

Invoke `/vibe` for code quality review:

```
Skill(skill="vibe", args="recent [--quick]")
```

Use `--quick` for fast/standard complexity. Use full council (no `--quick`) for full complexity.

**If no epic-id provided:** `/vibe recent` reviews the most recent changes.

**Gate logic:**

- **PASS:** Log `"Vibe: PASS"`. Store verdict. Proceed to Step 2.
- **WARN:** Log `"Vibe: WARN -- see report for concerns"`. Store verdict. Proceed to Step 2.
- **FAIL:** Do NOT retry internally. Signal failure to caller:
  1. Read vibe report: `ls -t .agents/council/*vibe*.md | head -1`
  2. Extract structured findings (description, fix, ref)
  3. Write phase summary with FAIL status
  4. Output: `<promise>FAIL</promise>` with findings attached
  5. Suggest: `"Vibe FAIL. Fix findings, then re-run /validation [epic-id]"`

**Why no internal retry:** Validation cannot fix code. Retries require re-implementation (`/crank`). The caller (`/rpi` or human) decides whether to loop back.

### Step 2: Post-mortem

**Skip if:** No epic-id provided (standalone vibe-only mode).

Invoke `/post-mortem` for retrospective analysis:

```
Skill(skill="post-mortem", args="<epic-id> [--quick]")
```

Use `--quick` for fast/standard complexity. Full council for full complexity.

Store post-mortem verdict in `validation_state.post_mortem_verdict`.

### Step 3: Retro (optional)

**Skip if:** `--no-retro` flag.

Invoke `/retro` for quick learning capture:

```
Skill(skill="retro")
```

Retro captures session-specific learnings to `.agents/learnings/`.

### Step 4: Forge (optional)

**Skip if:** `--no-forge` flag, OR `ao` CLI is not available.

Mine the current session for patterns, decisions, and failures:

```bash
ao forge transcript --last-session --queue --quiet 2>/dev/null || true
```

Note: `/forge` is an internal skill (`user-invocable: false`) — invoke via CLI, not via `Skill()`. Forge extracts structured knowledge to `.agents/learnings/`. Scoped to the current session only — full corpus mining is `/athena`'s job.

### Step 5: Output

1. **Write phase summary** to `.agents/rpi/phase-3-summary-YYYY-MM-DD-<slug>.md`:

```markdown
# Phase 3 Summary: Validation

- **Epic:** <epic-id or "standalone">
- **Vibe verdict:** <PASS|WARN|FAIL>
- **Post-mortem verdict:** <verdict or "skipped">
- **Retro:** <captured|skipped>
- **Forge:** <mined|skipped>
- **Complexity:** <fast|standard|full>
- **Status:** <DONE|FAIL>
- **Timestamp:** <ISO-8601>
```

2. **Record ratchet and telemetry:**

```bash
ao ratchet record vibe 2>/dev/null || true
bash scripts/checkpoint-commit.sh rpi "phase-3" "validation complete" 2>/dev/null || true
bash scripts/log-telemetry.sh rpi phase-complete phase=3 phase_name=validation 2>/dev/null || true
```

3. **Output completion marker:**

```
<promise>DONE</promise>    # Vibe PASS/WARN, learnings captured
<promise>FAIL</promise>    # Vibe FAIL, re-implementation needed
```

If DONE: report verdicts and suggest next steps.
If FAIL: report findings and suggest `/crank <epic-id> --context '<findings>'`.

## Phase Budgets

| Sub-step | `fast` | `standard` | `full` |
|----------|--------|------------|--------|
| Vibe | 2 min | 3 min | 5 min |
| Post-mortem | 2 min | 3 min | 5 min |
| Retro | 1 min | 1 min | 2 min |
| Forge | skip | 2 min | 3 min |

On budget expiry: allow in-flight calls to complete, write `[TIME-BOXED]` marker, proceed with whatever artifacts exist.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--complexity=<level>` | auto | Force complexity level (fast/standard/full) |
| `--no-retro` | off | Skip retro + forge steps |
| `--no-forge` | off | Skip forge step only |
| `--no-budget` | off | Disable phase time budgets |

## Completion Markers

```
<promise>DONE</promise>    # Validation passed, learnings captured
<promise>FAIL</promise>    # Vibe failed, re-implementation needed (findings attached)
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Vibe FAIL on first run | Implementation has quality issues | Fix findings via `/crank`, then re-run `/validation` |
| Post-mortem skipped unexpectedly | No epic-id provided | Pass epic-id: `/validation ag-5k2` |
| Forge produces no output | No ao CLI or no transcript content | Install ao CLI or run `/retro` manually |
| Stale execution-packet | Packet from a previous RPI cycle | Delete `.agents/rpi/execution-packet.json` and pass `--complexity` explicitly |

## Reference Documents

- [references/forge-scope.md](references/forge-scope.md) — forge session scoping and deduplication
- [references/idempotency-and-resume.md](references/idempotency-and-resume.md) — re-run behavior and standalone mode

## See Also

- [skills/vibe/SKILL.md](../vibe/SKILL.md) — code quality review
- [skills/post-mortem/SKILL.md](../post-mortem/SKILL.md) — retrospective analysis
- [skills/retro/SKILL.md](../retro/SKILL.md) — quick learning capture
- [skills/forge/SKILL.md](../forge/SKILL.md) — transcript mining
- [skills/crank/SKILL.md](../crank/SKILL.md) — previous phase (implementation)
- [skills/discovery/SKILL.md](../discovery/SKILL.md) — first phase (discovery)
- [skills/rpi/SKILL.md](../rpi/SKILL.md) — full lifecycle orchestrator
