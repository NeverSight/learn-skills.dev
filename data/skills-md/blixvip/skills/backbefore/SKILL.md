---
name: backbefore
description: Restore the version immediately before a rejected implementation, then reapply the user's latest request as a minimal compatible change. Use when the user invokes /backbefore or says they preferred the version before the latest change.
---

# /backbefore

Treat the version immediately before the rejected change as the baseline. Restore its look, behavior, and structure, then implement the latest request in a way that fits that baseline.

## Workflow

1. Identify the last good state from recent context, Git history or diffs, screenshots, or prior output.
2. Determine exactly what the rejected implementation changed or damaged.
3. Restore only the affected parts and preserve unrelated work.
4. Reapply the latest request as a minimal, compatible change.
5. Verify both that the prior behavior is restored and that the new request works.

## Rules

- Treat the previous version as the baseline and the latest request as the delta.
- Do not merely undo the new feature; integrate it better.
- Do not redesign, rewrite, or improve unrelated parts.
- Never use a destructive full reset, checkout, or revert that could erase other work.
- If several older versions exist, use the state immediately before the rejected change.
- For UI work, verify the rendered result rather than source alone.
- Use the fastest capable model when model switching is supported.
- Work immediately and return only after restoration and the new change are verified.

Return only:

```
✅ Back before: [what was restored]
✅ Still added: [how the new request now fits]
Verified: [specific check and result]
```

If genuinely blocked, return only:

```
⛔ Blocked: [exact missing history, file, or external dependency]
Needed: [single requirement to continue]
```
