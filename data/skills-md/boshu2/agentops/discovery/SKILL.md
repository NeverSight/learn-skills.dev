---
name: discovery
description: 'Full discovery phase orchestrator. Brainstorm + ao search + research + plan + pre-mortem gate. Produces epic-id and execution-packet for /crank. Triggers: "discovery", "discover", "explore and plan", "research and plan", "discovery phase".'
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
    - brainstorm  # optional - clarify WHAT before HOW
    - research    # required - codebase exploration
    - plan        # required - epic decomposition
    - pre-mortem  # required - validation gate
    - shared      # optional - CLI fallback table
---

# /discovery — Full Discovery Phase Orchestrator

> **Quick Ref:** Brainstorm → search history → research → plan → pre-mortem. Produces an epic-id and execution-packet ready for `/crank`.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## Quick Start

```bash
/discovery "add user authentication"              # full discovery
/discovery --interactive "refactor payment module" # human gates in research + plan
/discovery --skip-brainstorm "fix login bug"       # skip brainstorm for specific goals
/discovery --complexity=full "migrate to v2 API"   # force full council ceremony
```

## Architecture

```
/discovery <goal> [--interactive] [--complexity=<fast|standard|full>] [--skip-brainstorm]
  │
  ├── Step 1: Brainstorm (optional)
  │   └── /brainstorm <goal> — clarify WHAT before HOW
  │
  ├── Step 2: Search History
  │   └── ao search "<goal keywords>" — surface prior learnings
  │
  ├── Step 3: Research
  │   └── /research <goal> — deep codebase exploration
  │
  ├── Step 4: Plan
  │   └── /plan <goal> — decompose into epic + issues
  │
  └── Step 5: Pre-mortem (gate)
      └── /pre-mortem — council validates the plan
          PASS/WARN → output epic-id + execution-packet
          FAIL → re-plan with findings, max 3 attempts
```

## Execution Steps

### Step 0: Setup

```bash
mkdir -p .agents/rpi
```

Initialize state:

```
discovery_state = {
  goal: "<goal string>",
  interactive: <true if --interactive>,
  complexity: <fast|standard|full or null for auto-detect>,
  skip_brainstorm: <true if --skip-brainstorm or goal is >50 chars and specific>,
  epic_id: null,
  attempt: 1,
  verdict: null
}
```

**CLI dependency detection:**

```bash
# Tracking mode
if command -v bd &>/dev/null; then TRACKING_MODE="beads"; else TRACKING_MODE="tasklist"; fi

# Knowledge flywheel
if command -v ao &>/dev/null; then AO_AVAILABLE=true; else AO_AVAILABLE=false; fi
```

### Step 1: Brainstorm (optional)

**Skip if:** `--skip-brainstorm` flag, OR goal is >50 chars and contains no vague keywords (improve, better, something, somehow, maybe), OR a brainstorm artifact already exists for this goal in `.agents/brainstorm/`.

**Otherwise:** Invoke `/brainstorm` to clarify WHAT before HOW:

```
Skill(skill="brainstorm", args="<goal>")
```

If brainstorm produces a refined goal, use the refined goal for subsequent steps.

### Step 2: Search History

**Skip if:** `ao` CLI is not available.

**Otherwise:** Search for prior session learnings relevant to the goal:

```bash
ao search "<goal keywords>" 2>/dev/null || true
ao lookup --query "<goal keywords>" --limit 5 2>/dev/null || true
```

Summarize any relevant findings (prior attempts, related decisions, known constraints) and carry them forward as context for research.

**Ranked packet requirement:** Before leaving discovery, assemble a lightweight ranked packet for the current goal:
- matching compiled planning rules / pre-mortem checks
- matching active findings from `.agents/findings/*.md`
- matching unconsumed high-severity items from `.agents/rpi/next-work.jsonl`

Rank by literal goal-text overlap first, then issue-type / work-shape overlap, then file-path or module overlap when known. Discovery does not need the final file list yet, but it MUST surface the best matching high-severity next-work items so planning can incorporate them instead of rediscovering them later.

### Step 3: Research

Invoke `/research` for deep codebase exploration:

```
Skill(skill="research", args="<goal> [--auto]")
```

Pass `--auto` unless `--interactive` was specified. Research output lands in `.agents/research/`.

### Step 4: Plan

Invoke `/plan` to decompose into an epic with trackable issues:

```
Skill(skill="plan", args="<goal> [--auto]")
```

Pass `--auto` unless `--interactive` was specified. Plan output lands in `.agents/plans/` and creates issues via `bd` or TaskList.

After plan completes:
1. Extract epic ID: `bd list --type epic --status open` (beads) or identify from TaskList.
2. Store in `discovery_state.epic_id`.
3. Carry forward the ranked packet summary (applied findings, known risks, high-severity next-work matches) into the execution packet and phase summary.
3. **Auto-detect complexity** (if not overridden):
   - Count issues: `bd children <epic-id> | wc -l`
   - Low: 1-2 issues → `fast`
   - Medium: 3-6 issues → `standard`
   - High: 7+ issues or 3+ waves → `full`

### Step 5: Pre-mortem (gate)

Invoke `/pre-mortem` to validate the plan:

```
Skill(skill="pre-mortem", args="[--quick]")
```

Use `--quick` for fast/standard complexity. Use full council (no `--quick`) for full complexity or `--deep` override.

**Gate logic (max 3 attempts):**

- **PASS/WARN:** Proceed. Store verdict in `discovery_state.verdict`.
- **FAIL:** Retry loop:
  1. Read pre-mortem report: `ls -t .agents/council/*pre-mortem*.md | head -1`
  2. Extract structured findings (description, fix, ref)
  3. Log: `"Pre-mortem: FAIL (attempt N/3) -- retrying plan with feedback"`
  4. Re-invoke `/plan` with findings context:
     ```
     Skill(skill="plan", args="<goal> --auto --context 'Pre-mortem FAIL: <findings>'")
     ```
  5. Re-invoke `/pre-mortem`
  6. If still FAIL after 3 total attempts, stop:
     ```
     "Pre-mortem failed 3 times. Last report: <path>. Manual intervention needed."
     ```
     Output: `<promise>BLOCKED</promise>`

### Step 6: Output

After successful gate (PASS/WARN): write execution packet and phase summary (read `references/output-templates.md` for formats), record ratchet, output `<promise>DONE</promise>`, and report epic-id with suggested next step: `/crank <epic-id>`.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--interactive` | off | Human gates in research and plan |
| `--skip-brainstorm` | auto | Skip brainstorm step |
| `--complexity=<level>` | auto | Force complexity level (fast/standard/full) |
| `--no-budget` | off | Disable phase time budgets |

## Completion Markers

```
<promise>DONE</promise>      # Discovery complete, epic-id + execution-packet ready
<promise>BLOCKED</promise>   # Pre-mortem failed 3x, manual intervention needed
```

## Examples

```bash
/discovery "add user authentication"              # full discovery
/discovery --interactive "refactor payment module" # human gates
/discovery --skip-brainstorm "fix login bug"       # skip brainstorm
```

## Troubleshooting

Read `references/troubleshooting.md` for common problems and solutions.

## Reference Documents

- [references/complexity-auto-detect.md](references/complexity-auto-detect.md) — precedence contract for keyword vs issue-count classification
- [references/idempotency-and-resume.md](references/idempotency-and-resume.md) — re-run safety and resume behavior
- [references/phase-budgets.md](references/phase-budgets.md) — time budgets per complexity level
- [references/troubleshooting.md](references/troubleshooting.md) — common problems and solutions
- [references/output-templates.md](references/output-templates.md) — execution packet and phase summary formats

**See also:** [brainstorm](../brainstorm/SKILL.md), [research](../research/SKILL.md), [plan](../plan/SKILL.md), [pre-mortem](../pre-mortem/SKILL.md), [crank](../crank/SKILL.md), [rpi](../rpi/SKILL.md)
