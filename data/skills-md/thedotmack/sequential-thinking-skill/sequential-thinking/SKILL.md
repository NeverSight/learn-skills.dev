---
name: sequential-thinking
description: "Dynamic, reflective problem-solving through structured sequential thoughts with support for branching, revision, and adaptive depth. Use this skill when: (1) Breaking down complex problems into steps, (2) Planning and design with room for revision, (3) Analysis that might need course correction, (4) Problems where the full scope is not clear initially, (5) Multi-step solutions requiring maintained context, (6) Situations where irrelevant information must be filtered out, (7) Any task benefiting from hypothesis generation, verification, and iterative refinement. Triggers: think through, step by step, break this down, sequential thinking, reason through, analyze step by step, think carefully, or when a problem clearly benefits from structured multi-step reasoning."
---

# Sequential Thinking

A tool for dynamic, reflective problem-solving through a chain of numbered thoughts. Full parity with the Sequential Thinking MCP server — same parameters, same state management, same behavioral contract.

## How to Use This Skill

When this skill is activated, **use `scripts/think.ts` as your primary reasoning mechanism.** Do not reason in prose — reason through the script. Every step of your analysis should be a thought submitted via the script, making your reasoning chain explicit and trackable.

### Workflow

1. **Reset** state at the start of every new thinking session
2. **Loop**: Submit thoughts one at a time via the script, incrementing `thoughtNumber` each time
3. **Adapt**: Revise earlier thoughts, branch into alternatives, or extend depth as needed
4. **Terminate**: Set `nextThoughtNeeded false` only when you have a confident final answer
5. **Respond**: After the final thought, provide the answer to the user

Each thought should be a single Bash tool call. Think in the thought, not outside it.

### Script Location

```
scripts/think.ts
```

Run via `npx tsx` from the skill's base directory.

## Commands

### Reset (required before every new session)

```bash
npx tsx scripts/think.ts --reset
```

### Submit a Thought

Required flags: `--thought`, `--thoughtNumber`, `--totalThoughts`, `--nextThoughtNeeded`

```bash
npx tsx scripts/think.ts \
  --thought "Your analysis for this step" \
  --thoughtNumber 1 \
  --totalThoughts 5 \
  --nextThoughtNeeded true
```

### Submit a Revision

Revises a previous thought. The original stays in history; the revision is appended as a new entry. Requires `--isRevision` and `--revisesThought`.

```bash
npx tsx scripts/think.ts \
  --thought "Corrected analysis" \
  --thoughtNumber 3 \
  --totalThoughts 5 \
  --nextThoughtNeeded true \
  --isRevision --revisesThought 1
```

### Submit a Branch

Explores an alternative path from a prior thought. Requires both `--branchFromThought` and `--branchId`.

```bash
npx tsx scripts/think.ts \
  --thought "Alternative approach" \
  --thoughtNumber 4 \
  --totalThoughts 7 \
  --nextThoughtNeeded true \
  --branchFromThought 2 --branchId alt-approach
```

### Extend Depth

Signal that more thoughts are needed beyond the original estimate.

```bash
npx tsx scripts/think.ts \
  --thought "Scope is larger than expected" \
  --thoughtNumber 6 \
  --totalThoughts 8 \
  --nextThoughtNeeded true \
  --needsMoreThoughts
```

### Inspect Full State

```bash
npx tsx scripts/think.ts --status
```

Returns JSON with `fullHistory` and `branchDetails`.

## Output Format

Each thought invocation prints the thought to stderr and a compact status line to stdout:

```
💭 Thought 3/7
The analysis shows that...
[3/7] history=3 next=true
```

Revision and branch thoughts use `🔄 Revision` and `🌿 Branch` headers respectively.

## Parameters (Full MCP Parity)

| Parameter | Type | Required | Description |
|---|---|---|---|
| `--thought` | string | yes | The content of this thinking step |
| `--thoughtNumber` | int >= 1 | yes | Current thought number in the sequence |
| `--totalThoughts` | int >= 1 | yes | Estimated total thoughts needed (adjustable) |
| `--nextThoughtNeeded` | bool | yes | `true` to continue, `false` to terminate |
| `--isRevision` | flag | no | Marks this thought as revising a previous one |
| `--revisesThought` | int >= 1 | no | Which thought number is being revised (required with `--isRevision`) |
| `--branchFromThought` | int >= 1 | no | Create a branch starting from this thought number |
| `--branchId` | string | no | Label for the branch (required with `--branchFromThought`) |
| `--needsMoreThoughts` | flag | no | Signal that `totalThoughts` should be expanded |

## Behavioral Rules

These match the MCP server's tool description exactly:

1. **Start** with an initial estimate of `totalThoughts`, but adjust freely as understanding deepens
2. **Auto-adjust**: If `thoughtNumber` exceeds `totalThoughts`, the script raises `totalThoughts` to match
3. **Revise** previous thoughts when you realize an earlier step was wrong or incomplete — set `--isRevision` and `--revisesThought N`. The original stays in history; the revision is appended
4. **Branch** to explore alternative reasoning paths — set both `--branchFromThought N` and `--branchId label`. This does not abandon the main line
5. **Extend** beyond the initial estimate at any time with `--needsMoreThoughts` and an increased `--totalThoughts`
6. **Express uncertainty** — not every thought needs confidence. Questioning and exploring is encouraged
7. **Filter noise** — ignore information irrelevant to the current step
8. **Generate hypotheses** when you have enough evidence, then verify them against prior thoughts in the chain
9. **Iterate** hypothesis-verification cycles until satisfied with the answer
10. **Terminate** only when you have a satisfactory answer — set `--nextThoughtNeeded false`
11. **Non-linear paths are first-class** — branching, backtracking, and revision are features, not failures

## State Management

- State is persisted to `scripts/.think_state.json` between invocations
- `thoughtHistory[]` is append-only — thoughts are never deleted
- `branches{}` maps branch IDs to their thought arrays
- `--reset` clears all state for a fresh session
- `--status` dumps the full state as JSON for inspection

## Example Session

See [references/example-session.md](references/example-session.md) for a complete worked example demonstrating normal thoughts, revisions, branches, and dynamic depth adjustment.
