---
name: natural-writing
description: Use when asked to humanize text, remove AI tells, check whether text reads as AI-generated, or draft prose that must not sound AI-written.
license: SEE LICENSE IN LICENSE.md
disable-model-invocation: true
metadata:
  author: Vivswan
---

# Natural writing

Produce prose that avoids the documented signs of AI writing, based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). That page is a field guide for *detecting* AI text. This skill inverts it into rules for *not producing* those patterns.

One pattern alone can be fine. The goal is prose where the patterns don't cluster and nothing reads generated.

Scope: this skill is a guideline, not law. Skimmability for the reader outranks any style rule in it (short front-loaded paragraphs, no text blobs, examples first). Accuracy and reference-integrity rules always bind.

Under that house standard, bold-label bullets and sparing keyword bolds are sanctioned formatting. The bold and bullet cautions in this skill apply to prose written for external readers, not to this repo's own skill docs.

## When to apply

- "humanize this text" / "make this sound less like AI" / "remove the AI tells"
- "does this read as AI-generated?"
- Drafting or rewriting prose for readers outside the repository: articles, blog posts, reports, emails, announcements, PR descriptions
- Not repository documentation (READMEs, guides, reference pages): those are programmer-register pages of the `/docs-discipline` skill
- Any writing task where the user cares about tone, voice, or naturalness

## Source of truth

The catalog of signs changes over time (models change, and the community adds new tells). Prefer the live page, fall back to the bundled snapshot:

1. Live: fetch <https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing> (raw wikitext: `https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&action=raw`). Do this when auditing text for AI tells, when the user asks for a thorough pass, or when the bundled snapshot looks stale for the topic at hand.
2. Snapshot: [references/signs-catalog.md](references/signs-catalog.md) is a distilled copy of the full page, reorganized as writing rules. Use it as the working checklist for every invocation. It is enough when offline or for routine drafting.

Snapshot last synced: 2026-08-26, from page revision 1371415133 (2026-08-26T08:17:42Z). See "Maintaining the snapshot" below for how to update it.

[references/words-to-avoid.md](references/words-to-avoid.md) lists the words and phrases the page flags, organized for scanning, plus ready-made grep commands for the mechanical checks.

## Workflow

### 1. Load the rules

Read `references/signs-catalog.md` in full. For audits or thorough requests, also fetch the live page and note any signs not yet in the snapshot.

### 2. Pick the mode

- **Draft**: writing new text.
- **Rewrite**: revising existing text. Preserve the author's facts and voice, and the structure where sound. Strip only the tells and do not inject new claims.
- **Audit**: the user wants an assessment, not edits, so do not edit unless asked. Report which signs appear, where, with brief quotes. Mind the false-positive caveats in the catalog (section 9): formal prose or perfect grammar alone proves nothing.

### 3. Write or edit

Apply the full catalog. The highest-value rules:

1. **State facts plainly**, with *is/are/has/was*. Not "serves as", "stands as", "boasts", "features", "marks", "represents", or "refers to" openings.
2. **Cut inflated significance**: "pivotal moment", "testament to", "underscores its importance", "reflects broader trends", "rich cultural heritage", "evolving landscape". Replace generic importance-claims with a specific, checkable fact. Specificity is the whole game.
3. **Kill trailing participle analysis.** No sentence-final "-ing" clauses that editorialize: "…, highlighting the significance of X", "…, ensuring Y".
4. **Avoid AI-vocabulary clusters**: delve, crucial, pivotal, tapestry, landscape (abstract), showcase, underscore, intricate, fostering, garner, meticulous, vibrant, robust, boasts, align with, testament. One may be fine, but clusters are the tell. See the word list.
5. **Break the templates.** No "not just X, but Y" or "It's not X, it's Y" parallelisms, and no rule-of-three triads everywhere. No "Despite these challenges…" conclusions, no "In summary / In conclusion / Overall" wrap-ups, and no "It's important to note".
6. **Attribute precisely or not at all.** No "experts argue", "observers have noted", "industry reports suggest". Name the source or drop the claim, and never imply many sources when there is one.
7. **Never use a dash as punctuation.** No em dashes (—), and no sneaking the same construction back in with an en dash (–) or a spaced hyphen ( - ), which swaps the character while keeping the tell. Restructure instead: a comma, a colon, parentheses, or two sentences. Hyphens stay only inside compound words, and en dashes only in numeric ranges.
8. **Format like a human.** Prose first, and lists only when the content is genuinely enumerable. Sentence case headings, and bold almost nothing. No bullet lists where every item is a bold label plus a colon, no emoji decoration, no needless small tables, no horizontal rules before headings, no skipped heading levels.
9. **No chat artifacts.** No "I hope this helps", "Certainly!", "Would you like…", "Here is a…" framing, and no knowledge-cutoff disclaimers. No speculation dressed as fact ("details are not widely documented, but likely…"). No unfilled placeholders like `[Your Name]` or `2025-XX-XX`.
10. **Use the target medium's markup**, never Markdown headed for a non-Markdown destination. Never invent citations, links, DOIs, ISBNs, or page numbers. Verify every reference you emit, and strip tool residue (`utm_source=`, `turn0search0`, `oaicite`, `[cite: 1]`).
11. **Vary rhythm, and repeat words when natural.** Reusing the same noun beats cycling synonyms. Mix sentence lengths. Commit to definite statements ("was the first") and use plain verbs (wrote, used, moved, tried, died).

The dash rule (7) is a house rule. It is stricter than the Wikipedia page, which only flags overuse.

### 4. Self-review pass

Before delivering, reread the output against the checklist above. Scan it against the term lists in `references/words-to-avoid.md` (they are written for reading, not for `grep -f`). Two checks are mechanical, so run them on the draft file:

```bash
# Dash punctuation and machine artifacts: any hit outside quoted material is a bug.
# (Unspaced en dashes in numeric ranges like 2024–2025 are allowed and not flagged.)
grep -nE '—| – | - |turn0|oaicite|oai_citation|contentReference|attributableIndex|attached_file|grok[_-]|(start|end)_span|ppl-ai-file-upload|【|\[cite:|\[web:[0-9]|:::writing|utm_source=(chatgpt\.com|openai|copilot\.com)|referrer=grok\.com|↩|XX-XX|INSERT_|PASTE_' draft.md

# High-signal AI vocabulary: hits are prompts to reread the sentence, not automatic errors
grep -inE 'delve|deep dive|tapestry|testament|pivotal|crucial|underscor|showcas|foster(ing|s)|garner|meticulous|vibrant|intrica|boasts|bolster|interplay|stands as|serves as|not just|not only' draft.md
```

Fix a hit by rewriting the sentence, never by thesaurus-swapping the flagged word. The underlying pattern (vagueness, puffery, formula) is the problem, not the word itself.

### 5. Report

- **Draft/Rewrite**: deliver the text. If rewriting, summarize which signs you removed in one or two sentences.
- **Audit**: list the signs found with locations and quotes, state an overall read, and note the base-rate caveat: these are statistical signs, not proof.

## Fallback without network

Everything works offline from `references/signs-catalog.md` and `references/words-to-avoid.md`. Only the live-refresh step is skipped.

## Maintaining the snapshot

When asked to update this skill from Wikipedia (or when the snapshot looks stale), reconcile semantically. The catalog is a reorganized distillation, so a textual diff against the wikitext is noise.

1. Check whether the page changed since the pinned revision:

   ```bash
   curl -fsSL 'https://en.wikipedia.org/w/api.php?action=query&titles=Wikipedia:Signs_of_AI_writing&prop=revisions&rvprop=ids|timestamp&format=json'
   ```

   If `revid` equals the revision pinned under "Source of truth" above, nothing to do.

2. Otherwise fetch and read the full current wikitext:

   ```bash
   curl -fsSL 'https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&action=raw' -o /tmp/signs.txt
   ```

3. Compare it section by section against `references/signs-catalog.md`. Fold in new signs, drop removed ones, and update `references/words-to-avoid.md` to match.

4. Update the pinned revision ID, timestamp, and sync date in both places: under "Source of truth" in this file and in the header of `references/signs-catalog.md`. The two pins must match.
