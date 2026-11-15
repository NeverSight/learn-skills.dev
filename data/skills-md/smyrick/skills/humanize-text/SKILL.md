---
name: "humanize-text"
description: "Remove generic AI-writing patterns from prose while preserving facts, meaning, and the writer’s voice."
---

# Humanize Text

Rewrite supplied prose so it reads like a deliberate human draft. Preserve the source; do not turn the task into fact-checking, summarization, or new writing.

## Establish the Contract

Identify:

- the exact text to rewrite;
- the target genre and audience, when stated;
- any voice sample or explicit style direction;
- protected spans that must remain byte-for-byte unchanged.

Treat code blocks, inline code, URLs, quoted passages, headings, proper nouns, numbers, dates, citations, identifiers, and user-marked text as protected unless the user explicitly includes them in scope. Protection includes spelling, capitalization, whitespace, and punctuation. A style preference, including em-dash avoidance, never overrides a protected span.

If the target text is ambiguous, ask which text to process. Otherwise, infer the register and proceed without a discovery interview.

## Preserve Fidelity

Before rewriting, make a private inventory of factual claims and protected spans. During the rewrite:

- Preserve every claim, qualification, relationship, number, name, date, citation, and URL.
- Preserve the author's stance, certainty, and intent.
- Do not add examples, facts, metrics, anecdotes, praise, caveats, or opinions.
- Do not silently correct a suspected factual error. Keep it or ask the user whether they want a separate fact-check.
- Do not shorten, expand, or restructure beyond what is needed to improve the prose.

After rewriting, compare the result against the inventory. Restore anything changed, omitted, or invented.

## Match the Writer

Use the strongest available voice evidence in this order:

1. same-genre samples supplied by the user;
2. other published or finished writing by the user;
3. transcripts containing the user's actual words;
4. repeated choices in the current conversation;
5. explicit style directions;
6. genre conventions.

Infer a compact voice brief from stable traits: density, stance, rhythm, formatting, and diction. Do not imitate typos, one-off jokes, accidental grammar, or artificial casualness.

## Rewrite

Remove patterns that are generic rather than characteristic of the writer:

- assistant boilerplate, praise-padding, and trailing offers;
- hollow openings, canned transitions, and conclusion summaries;
- repeated antithesis, impact-label, and rule-of-three constructions;
- clustered hype, vague abstractions, and fashionable AI vocabulary;
- forced bulletization, uniform cadence, excessive hedging, and empty repetition.

Read past the lead-in, especially when it ends in a colon. If the next sentence or list makes the same point on its own, delete the whole lead-in. If the lead-in supplies context the reader needs, keep it or fold it into the sentence. Apply the same test when the setup ends in a period or dash.

Prefer plain, precise phrasing and varied sentence rhythm. Do not replace one tell with another: avoid fake typos, forced lowercase, conspicuous slang, uniform fragments, or contorted em-dash avoidance.

Read [PATTERNS.md](./PATTERNS.md) only when the text presents an edge case or needs a detailed pattern checklist. The fidelity and protection rules in this file take precedence over any heuristic in that reference.

## Output

Return only the final rewritten copy, ready to paste. Do not include findings, counts, explanations, before/after examples, or a follow-up offer unless the user explicitly requests analysis.

When the source is a file, do not overwrite it unless the user explicitly asks for an in-place edit. For an authorized file edit, preserve the file's unrelated content and formatting.
