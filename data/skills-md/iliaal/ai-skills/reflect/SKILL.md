---
name: reflect
description: >-
  Session retrospective and skill audit. Use when asked to reflect, do a
  retrospective, review lessons learned, audit what went well or wrong, or
  review session effectiveness.
---

# Reflect

## Success Criteria

- Every mistake/friction point cites the specific moment and its impact
- Improvements are actionable, prioritized, and <= 10 items
- Each skill audit proposes measurable changes (not vague suggestions)
- User is asked which items to persist to memory

## Process

### 1. Session Review

Scan the full conversation. For each finding, cite the specific exchange (quote or paraphrase) and its impact.

| Category | Signal |
|----------|--------|
| **Mistakes** | Wrong outputs, incorrect assumptions, hallucinated facts |
| **Friction** | Repeated clarifications, verbose responses, misread intent |
| **Wasted effort** | Work discarded, wrong approaches tried first |
| **Wins** | Approaches worth repeating, smooth interactions |

Skip one-time typos, external tool failures, and issues outside agent control.

### 2. Improvements

Numbered list of **concrete improvements**, ranked by impact. Each item: one sentence, imperative, actionable. Cap at 10.

Ask: *"Which of these should I remember for future chats?"*

Save approved items to memory files via the auto memory system.

### 3. Skill Audit (if skills were used)

For each skill invoked during the session:

**A. Self-check gate** — If the skill lacks success criteria + verification loop:
- Add `## Success Criteria` at top (3-5 measurable checks)
- Add `## Self-Check` at bottom: "Verify all success criteria are met before presenting output. If not, iterate (max 5 times)."

**B. Token efficiency** — Flag: redundant phrasing, mergeable sections, oversized examples, "Claude already knows this" content, inert frontmatter metadata.

**C. Other** — Missing edge cases, vague directives (rewrite as measurable criteria or remove), naked negations (add "do Y instead" or remove).

Present proposed changes as diffs. Ask: *"Apply these? (all / pick / skip)"*

### 4. Pattern Detection

If 2+ similar tasks appear that no existing skill covers, suggest a new skill (1-2 sentence description). Create only after confirmation.

## Proactive Trigger

When the user corrects you, clarifies the same thing twice, or shows frustration — append:

> Tip: Type `/reflect` when you're ready — I'll review what we can improve.

## Self-Check

Before presenting output, verify all success criteria are met. If any fail, revise (max 5 iterations).
