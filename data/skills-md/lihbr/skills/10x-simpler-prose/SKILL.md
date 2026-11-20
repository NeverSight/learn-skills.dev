---
name: 10x-simpler-prose
description: Use on every draft before posting it to GitHub, including PR titles and bodies (gh pr create, gh pr edit), issues, and review comment replies (gh pr comment, gh pr review, gh api .../comments). Also use when the user says "10x simpler prose", "distill this writing", "tighten this draft", or asks to make a document radically shorter without losing substance.
argument-hint: "[path]"
---

# 10x simpler, for prose

Rewrite the target so it is as short and as clear as it can honestly be. This is not a copyedit. Question whether each section, paragraph, and sentence needs to exist at all.

This skill works at the structural level. Run a sentence-level pass (like unslop) on whatever survives.

## What "simple" means

Fewer ideas the reader must hold, not fewer characters. Word count is the score; comprehension is the constraint. A reader must understand the piece in one pass. Never compress into telegraphic fragments, stacked clauses, or abbreviations. That is the prose version of code golf.

The real score depends on the reader. For a portfolio or proposal, it is claims the reader remembers per minute of reading. A piece can be too short to do its job; a piece where every sentence is load-bearing cannot.

## The five reduction moves

In rough order of impact:

1. **Delete before rewriting.** Cut sentences and paragraphs that exist for structure rather than content: throat-clearing openers, transitions that restate the previous section, significance statements ("This is what makes it matter"), any point made twice. If a sentence can't be restated as a concrete fact, instruction, or number, cut it.
2. **Collapse layers.** Inline single-use framing. A sentence that only introduces the next sentence gets merged into it. A subsection with one paragraph loses its header. A term defined and used once is an abstraction with one caller: just say the thing.
3. **Use the platform.** Rely on what the reader already knows. Don't explain standard concepts to an expert audience. Let a table, code block, or link carry meaning instead of prose describing it.
4. **Flatten.** State each claim once, directly. Replace hedged branching ("in some cases X, though sometimes Y") with the honest single claim. Lead with the conclusion, then support it.
5. **Condense style.** Direct sentences, no intermediate phrases that add nothing, consistent with the author's voice. This move is last because it saves the least; do not start here.

## Guardrails

- **Meaning preservation is non-negotiable.** Every fact, number, attribution, and caveat survives. Compress the telling, never the record.
- If a big cut would change or weaken a claim, do not make it. Report it as a suggested follow-up.
- Preserve the author's voice. Reduction is not homogenization; keep their phrasings when they carry the point.
- Stay inside the target. If related documents beg for the same treatment, suggest it, don't do it.

## Process

1. Read the full piece before cutting anything. Know what job each section does.
2. Do a deep reduction pass using the five moves.
3. Re-read and ask "what is still removable?" Repeat until a pass changes nothing, max 3 passes. The second pass finds cuts the first one created: a sentence often becomes removable only after its neighbor dies.
4. Re-read once more for flow. Cuts leave seams; smooth only where a seam breaks comprehension.
5. Close with a short report: word count before and after, what was cut and why (grouped by move, not sentence by sentence), and any suggested cuts you deliberately did not make.

## Drafts about to be posted

When the target is your own draft for GitHub, run the passes, then post the result. Skip the report. Don't mention this skill in the posted text.
