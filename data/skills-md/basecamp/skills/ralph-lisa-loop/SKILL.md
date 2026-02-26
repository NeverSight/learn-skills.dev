---
name: ralph-lisa-loop
description: |
  Automated plan-implement loop with expert review. Claude implements, Codex reviews,
  the human steers. A single rope-length knob (0-5) controls interruption frequency.
  Closure requires zero open findings and zero unresolved disputes at any rope level.
  Use for any planning, development, or implementation task that benefits from
  structured review. The default workflow for building anything non-trivial.
triggers:
  # Direct invocations
  - /ralph-lisa-loop
  - /ralph-lisa
  - /ralph
  - ralph-lisa loop
  - ralph loop
  - ralph lisa
  # Planning
  - plan this
  - let's plan
  - make a plan
  - plan with expert
  - plan and build
  - plan-implement cycle
  - plan then implement
  - plan then build
  # Plan-only
  - plan only
  - just plan
  - design review
  - RFC review
  # Development / implementation
  - build this
  - implement this
  - implement with expert
  - build with expert review
  # Implement-only
  - just implement
  - just build
  - skip planning
  # Codex review
  - codex review
  - get codex to review
  - have codex review
  - review with codex
  - expert review loop
  # Automation emphasis
  - automated review loop
  - autonomous review loop
---

# ralph-lisa-loop

## Preflight

Do not enter the round loop until all preflight checks pass.

### Step 1: Stop hook check

Read `~/.claude/settings.json` and look for a `Stop` hook entry pointing to this
skill's `scripts/stop-hook.sh`.

If the hook is NOT installed, tell the user:

> The ralph-lisa loop works best with the stop hook installed — it keeps the loop
> running automatically so you don't have to type "continue" each round. The hook
> is dormant when no loop session is active (it checks for a session file and
> exits immediately if none exists).
>
> Want me to add it to your settings?

If the user agrees, add this entry to `~/.claude/settings.json` under `hooks.Stop`
(create the key path if it doesn't exist):

```json
{
  "matcher": "",
  "hooks": [{
    "type": "command",
    "command": "SKILL_SCRIPTS_DIR/stop-hook.sh",
    "timeout": 10000
  }]
}
```

Replace `SKILL_SCRIPTS_DIR` with the absolute path to this skill's `scripts/`
directory (resolve from the skill installation location).

If the user declines the hook, proceed in Manual tier (the user will type
"continue" between rounds). Note the tier in the session's first round summary.

If the hook IS already installed, proceed without mentioning it.

### Step 2: Codex reviewer channel check

Probe whether the Codex MCP tools are callable (search available tools for
`mcp__codex__codex`, or attempt a lightweight call). Don't inspect how it's
configured — it could be project `.mcp.json`, user-wide MCP settings, or
another harness entirely.

- If `mcp__codex__codex` is available → record `reviewer_backend: mcp` and `review_channel_status: mcp_ready` in session, proceed.
- If unavailable → check `which codex` for CLI fallback.
  - If codex CLI exists → offer to configure MCP:
    > Codex MCP isn't available in this session. I can add it for you:
    >
    > 1. **User-level** — available in all projects
    > 2. **Project-level** — scoped to this repo
    > 3. **Skip** — use `codex exec` CLI fallback (slower, session-based persistence)
    >
    > Which do you prefer?

    For options 1 or 2, run the appropriate command, then stop — do not enter
    the round loop. Tell the user to restart Claude Code and re-invoke the skill.
    Preflight will re-run and find MCP available.
    ```bash
    # User-level
    claude mcp add --scope user --transport stdio codex -- codex mcp-server

    # Project-level
    claude mcp add --scope project --transport stdio codex -- codex mcp-server
    ```

    If the user chooses "skip" (option 3), record `reviewer_backend: exec` and
    `review_channel_status: exec_opt_in`, proceed with the downgrade logged.
  - If no codex CLI at all → hard stop:
    > The ralph-lisa loop requires Codex as reviewer. Install: `npm i -g @openai/codex`
    > Then either restart (I'll offer to configure MCP) or ensure the CLI is in your PATH.

### Step 3: Reasoning policy initialization

Confirm rope length and inform the user of the reasoning policy (no action
needed from them):

> Reasoning policy: xhigh for all rounds, with detailed reasoning summaries.

## Protocol

Open `@references/guide.md` and follow it. Do not proceed without it.

Automated plan-implement loop with Codex as reviewer. Use when you want:
- Plans stress-tested through parallel ideation then iterative convergence
- Implementation reviewed each round with zero-finding close gate
- Adjustable autonomy via rope-length (0 = approve everything, 5 = full auto)
- Walk-away execution with all decisions tracked in a session file

The guide contains:
- Core protocol: single workflow, two modes (plan/implement)
- Rope-length semantics and salience scoring
- Round mechanics: self-review, external review, reconciliation, synthesis
- Finding and dispute tracking with stable IDs
- Close gate derivation and anti-gaming constraints
- Phase transition (plan -> implement) with decisions ledger
- Parallel ideation protocol (Round 1 independence)
- Session file format and continuation block structure
- Stop hook integration for loop enforcement
- Prompt pack reference (`@references/prompts.md`)
- Session template (`@references/session-template.md`)
- Eval checks and failure modes
