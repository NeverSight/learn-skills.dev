---
name: joe
description: Re-say the last answer simple and straight, aimed at the "oh, I get it" click — short, direct, no hedging, no padding, no tech-legalese. Goes for understanding over detail, so it leads with what is going on and why, keeps only the specifics the reader needs to act, and grounds tool-specific terms in a few words for a programmer who may not be deep in this stack. Use when the user types /joe or asks for the short version, the straight version, "what did you just say", or "TL;DR that".
---

# joe

Someone just got a wall of text. Say the same thing again — short and straight.

**Rewrite only. Do no new work.** No tool calls, no file reads, no re-checking, no fresh
analysis, no new recommendations. The source is what was already written in this
conversation (normally your immediately preceding message; if an argument is given, the part
of it the argument names). If there is nothing to condense, say so in one line and stop.

## Understanding, not details

The point is that they *get it* — the shape of what's going on, why it happened, what it
means for them. Specifics are how you'd prove it; they're not the answer.

- **Lead with the idea.** "The install silently skipped the skill because the frontmatter
  didn't parse" — not a list of what you ran.
- **Details earn their place.** A command, path, flag, number, or error string goes in only
  when they need it to act right now, or when the idea makes no sense without it. Otherwise
  leave it out — the long version above still has it if they want it.
- **Never fake a detail you do keep.** Exact or gone. No rounding, no approximate paths, no
  paraphrased error text.
- **No process narration.** What you tried, in what order, how many attempts — cut all of it
  unless the sequence *is* the insight.

Reading level: a competent programmer who may not be deep in *this particular* stack.

- General programming words stay — race condition, symlink, stderr, cache, rebase. Never
  define them.
- Terms specific to this tool, library, or domain get grounded the first time in three or
  four words, inline: "a worktree (second checkout of the same repo)". Better still, just say
  what it does and skip the name.
- Don't explain the obvious, and don't re-teach their own code.

## Output shape

- **Bottom line first.** One sentence: what's going on, or the actual answer.
- **Then at most 3–4 short lines** of anything that changes what they'd think or do. Bullets
  or prose, whichever is more natural. Often the bottom line is enough — ship just that.
- **Hard ceiling: ~120 words.** Under 60 is better. No heading, no table, no nested bullet,
  no closing "let me know if…".

## Voice

Flat and direct. Contractions fine. "It broke because X" — not "the failure mode originates
in X".

Kill on sight:
- **Hedging** — "it appears that", "generally speaking", "you may want to consider". Say the
  thing. If you're genuinely unsure, one short "not sure:" clause.
- **Tech-legalese** — "leverage", "utilize", "facilitate", "as such", "note that", "it is
  worth noting", "in order to", "robust", "seamless", "comprehensive".
- **Throat-clearing** — restating the question, "great question", recapping the steps you
  took before getting to what they mean.
- **Caveats nobody asked for.** Keep only a risk that would actually bite them.
- **Praise, apology, and enthusiasm.** Not part of the answer.

## Rules that keep it honest

- Shorter, not softer. Don't turn "this is broken" into "there are some considerations". If
  the long version said something failed, is uncertain, or needs their decision, the short
  version says it too — first.
- Don't add facts, confidence, or promises that weren't in the original.
- If the original ended with a question or a choice for them, end with that same question,
  in one line.
