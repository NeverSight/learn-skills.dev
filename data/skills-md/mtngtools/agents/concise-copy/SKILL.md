---
name: concise-copy
description: Refine copy or documentation to ensure the text is direct and efficient.
metadata:
  type: command
  invocation: skill-callable
  applies-to: [writing, documentation, content]
---

# Concise Copy Command

Refine copy or documentation, applying the following to ensure the text is direct and efficient.

## Rules
- **Remove filler words**: Eliminate "should", "must", "the process of", "the ability to", etc.
- **Start with the action or state**: Instead of "- The system should support **X**", use "- **X**".
- **Be direct**: Use active voice and minimal phrasing.
- **Avoid verbosity**: If a concept can be stated in 3 words instead of 10, use 3.

## Approval discussion is a removal question, not a trim

Sometimes the wordiest passage in a document is a record of a conversation: who approved something, what was considered and rejected, the back-and-forth that produced a rule. **That is not a verbosity problem, and tightening it is the wrong move** — per the `approval-policy` skill, it may not belong in a committed file at all. Its home is the PR, the issue, or the resolution comment.

What it looks like: `approved by …`, `we decided …`, `we considered X but …`, `as discussed …`, a rationale paragraph that narrates a discussion rather than stating a rule, a note explaining why an earlier version was changed.

**If the human is at the keyboard — they have sent a message in the last few exchanges and this run is answering it — ask** before touching such a passage. One question, three options: remove it (it lives on the tracker), move it there first and then remove it, or keep it as it is because this file is its intended home.

**If they are not, do not ask and do not delete.** A long unattended run, a scheduled job, a sweep across many files, or a chain from another skill with no human turn since — a question nobody is there to answer stops the whole run, which is worse than a paragraph left standing. Leave the passage exactly as it is, and **list every one you found in your output** so a human can decide later.

**Either way, never cut it silently as filler.** Compressing a record until it says less is the one edit this skill must not make on its own: removing it is a decision about where the record lives, not about how tightly it is written.

## Example
**Before**:
- The import process should support **partial data states** (e.g., a "Draft" phase with sessions but no room assignments).

**After**:
- **Partial data states** (e.g., Draft sessions -> no room assignments).
