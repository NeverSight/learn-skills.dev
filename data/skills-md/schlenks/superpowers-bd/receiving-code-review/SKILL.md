---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Code Review Reception

Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## Response Pattern

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each

## Response Task Enforcement

Create native tasks for each step (each blocked by previous via addBlockedBy):

1. **"READ: Complete feedback without reacting"** -- Read all items completely first
2. **"UNDERSTAND: Restate requirements"** -- Restate each in own words. Ask if unclear
3. **"VERIFY: Check against codebase"** -- Check suggestions against reality. Does current code exist for a reason?
4. **"EVALUATE: Technical soundness"** -- Sound for THIS codebase? Violates YAGNI? Conflicts with architecture?
5. **"IMPLEMENT: Apply changes"** -- One at a time. Test each. Verify no regressions

See `references/task-enforcement-blocks.md` for full TaskCreate blocks.

**ENFORCEMENT:** VERIFY cannot be skipped (blocked until UNDERSTAND completes). IMPLEMENT blocked until EVALUATE completes. TaskList exposes skipped steps.

## Forbidden Responses

**NEVER:** "You're absolutely right!" / "Great point!" / "Excellent feedback!" / "Let me implement that now" (before verification)

**INSTEAD:** Restate technical requirement, ask clarifying questions, push back with reasoning if wrong, just start working.

## Handling Unclear Feedback

If ANY item unclear: STOP, do not implement anything, ASK for clarification. Items may be related -- partial understanding = wrong implementation.

Example: "Fix 1-6" but unclear on 4,5. Do NOT implement 1,2,3,6 now. Ask about 4,5 first.

## Source-Specific Handling

**From human partner:** Trusted -- implement after understanding. Still ask if scope unclear. No performative agreement. Skip to action.

**From external reviewers:** Before implementing, check: technically correct for THIS codebase? Breaks existing functionality? Reason for current implementation? Works on all platforms? Reviewer understands full context? If wrong: push back. If can't verify: say so. If conflicts with partner's decisions: stop and discuss first. See `references/external-reviewer-protocol.md`.

## When To Push Back

Push back when: breaks existing functionality, reviewer lacks context, violates YAGNI, technically incorrect, legacy/compatibility reasons, conflicts with architectural decisions.

**How:** Technical reasoning, specific questions, reference working tests/code. See `references/pushback-guide.md`.

**Signal if uncomfortable:** "Strange things are afoot at the Circle K"

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Performative agreement | State requirement or just act |
| Blind implementation | Verify against codebase first |
| Batch without testing | One at a time, test each |
| Assuming reviewer is right | Check if breaks things |
| Avoiding pushback | Technical correctness > comfort |
| Partial implementation | Clarify all items first |
| Can't verify, proceed anyway | State limitation, ask for direction |

## The Bottom Line

External feedback = suggestions to evaluate, not orders to follow. Verify. Question. Then implement.

## Reference Files

- `references/task-enforcement-blocks.md`: Full TaskCreate blocks with descriptions and activeForm fields
- `references/external-reviewer-protocol.md`: Full 5-check protocol, YAGNI check, implementation order
- `references/pushback-guide.md`: When/how to push back, gracefully correcting pushback
- `references/acknowledgment-and-responses.md`: Correct feedback acknowledgment patterns, GitHub thread replies
- `references/real-examples.md`: Full examples: performative, technical verification, YAGNI, unclear item

<!-- compressed: 2026-02-11, original: 722 words, compressed: 467 words -->
