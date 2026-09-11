---
name: agent-watchdog
description: Audit another agent against the original request and live evidence. Use for sessions, PRs, branches, comparisons, authorized fixes, or taking over stuck work.
---

Read `references/builder-upstream.md` for complex/ambiguous audits.

## Modes

- **Watch:** monitor session/PR/branch/CI/transcript to terminal; no edits.
- **Audit:** compare request, transcript, diff, tests, CI, comments, visuals, claims; no edits.
- **Audit and fix:** audit, then narrow authorized fixes.
- **Compare:** judge agents/sessions against one request.
- **Takeover:** explicit request to own stuck work; follow [references/takeover.md](references/takeover.md), then execute to the requested endpoint. This is not limited to patching the previous approach.

Default audit-only when edit authority is unclear.

## Workflow

For takeover, use its reference instead of the narrow audit-and-fix steps below.

1. Resolve target: session/transcript/thread/PR/branch/commit/CI/issue/link/summary.
2. Reconstruct original ask, scope changes, constraints, implied criteria, claims, caveats.
3. Inspect files, surrounding code, command output, CI, screenshots, comments, deploy logs.
4. Classify `Gap|Bug|Verification miss|Scope drift|No issue`.
5. If authorized, fix only clear gaps; never revert unrelated work or move branches unasked.
6. Report exact evidence, unresolved risks, next action.

```md
## Agent watchdog
Target/Mode/Contract:
Evidence checked:
Findings: <class, evidence, action>
Fixes made:
Still open:
```
