---
name: reviewing-technical-prose
description: Use when reviewing, rewriting, or editing someone else's technical text, when writing a review report on a document, or as the final check before delivering any document. Encodes the severity mapping, the findings format, the what-not-to-flag list, and the delivery checklist. Use before any document ships, even when it looks fine.
---

# Reviewing technical prose

**REQUIRED BACKGROUND:** the `technical-writing` skill, including `references/style.md` (banned constructions) and `references/truth.md` (claim rules).

## Overview

Editing is diagnosis. Every edit names the concrete defect it fixes; the smallest edit that fixes it wins. Rewriting natural or approved language without a named defect is itself a defect.

Review the full document, never a summary of it.

## When to invoke, and not

Invoke when reviewing or rewriting someone else's technical text, when producing a findings report on a document, and as the final pass before delivering anything you wrote yourself. Do NOT invoke for code review (only the prose in it), and do not use a review pass to relitigate settled decisions, expand scope, or restyle a document onto your own preferences.

## Severity mapping

- **BLOCKER**: hard-rule violations (banned dashes, changelog sections, delivery history in prose) and any claim the cited source does not support or that traces to nothing.
- **WARNING**: banned constructions, structural defects (question headings, buried conclusions, rearrangeable paragraphs), and claims supported only loosely.
- **OBS**: ambiguity, missing polish, and anything an attentive author would likely catch.

## Rewriting someone else's text

One requirement above all rules: **the content stays identical.** Work in this order:

1. Read the source. Mark every banned construction and word-choice violation.
2. Write a version. Read it aloud.
3. Ask three control questions:
   - Which sentence still sounds like a language model?
   - Did the rewrite add or drop a fact, number, date, name, source, or claim?
   - Does the rewrite recreate a removed pattern in a new rhetorical form?

   Re-scan the rewritten paragraph as if it were source text.

4. Repair what the control questions surface. An addition and a loss both count as errors, even when the text reads better for it.

Never add a fact to finish a sentence: ask the author or pick a simpler sentence. If a sentence stays wooden after two attempts, rewrite the whole paragraph around its main point. Change only running prose: code blocks, frontmatter, table data, and link targets stay as they are.

- **The rewrite keeps the document's language.** A Dutch document comes back in Dutch, with the structural and truth rules applied as always; the English-specific vocabulary checks are replaced by that language's own list where one exists.
- **When the author is reachable, the diff is the proposal.** Show the rewrite before overwriting their text. Unattended in a repository, the commit is the proposal and review does the same job.

When the source text asserts nothing recoverable (setups, glosses, meaning-sentences), the correct rewrite is deletion plus a marked gap (`**[input wanted: <the claim the sentence should make>]**`, the claim-level sibling of the core skill's `**[source wanted: ...]**`) where a real claim should stand. A rewrite full of marked gaps is the intended outcome for claim-free source text, not a failure.

## Findings to leave alone

The banned-constructions list proves nothing by itself; every pattern also occurs in good human writing. Flag only when several signs coincide in the same paragraph.

- Polished grammar and consistent formatting.
- One repeated sentence opening: fix only when the repetition adds nothing.
- One short sentence for emphasis: only a row of fragments is a problem.
- Formal words in general: the list names specific words; not every formal word needs simplifying.
- A factual contrast: "the pipeline sets the tag, the developer does not" is a statement, not antithesis.
- A serious alternative the reader would genuinely weigh: it belongs in the document.
- Qualifiers that bound something: scope, assumptions, and safety or legal notes stay. Only the stacking goes.
- A reference to the previous situation in a migration doc or release note: there the change IS the subject.
- A quoted word: never rewrite inside a citation, a title, or an example that discusses the word.
- Metaphor that explains: only the decoration around it goes.
- Deliberate awkwardness: a clear fragment or lopsided sentence is not a defect merely because it could be polished.

## Review reports

- Verdict in the first line, findings ordered most severe first.
- Severity vocabulary defined in the report that uses it: **BLOCKER** (cannot proceed), **WARNING** (likely rework; fix but not blocking), **OBS** (worth noting).
- Every finding: one sentence stating the defect, a location (`file:line`, section, task ID), a proposed fix, and a confidence level.
- A named empty case ("FINDINGS: none").
- A document claim contradicted by the code is a defect in the document; report it with the conflicting source. An unrelated bug noticed in passing is not your finding.
- Re-reviews list only what remains.
- Acknowledge what is good.

## Delivery checklist

Before any document goes out:

- [ ] **Matched** to the existing documents in the same directory, and added to the `README.md` index if one exists
- [ ] **No em dashes, en dashes, or ` -- `**; no changelog section or "last updated" field; no ticket keys, phases, or SHAs in prose
- [ ] **No banned constructions** (the `technical-writing` skill's `references/style.md`); check at least the summary and the closing paragraphs
- [ ] **Headings name the content**: no question forms, no "What X means", no heading repeated in its first sentence
- [ ] **Conclusion first** at document, chapter, and paragraph level
- [ ] **Procedures**: one action per sentence, with an actor
- [ ] **Where the document proposes or decides**: every non-trivial choice has its reasoning and a serious alternative recorded, and the costs are in, not only the benefits
- [ ] **Fact and proposal are distinguishable**; estimates labeled; unknowns explicitly unknown
- [ ] **Every claim with a number** traces to a source named in the document
- [ ] **References checked by following them**: chapter numbers, relative links, and file names actually exist
- [ ] **Terms consistent** and defined at first use; one term per concept
- [ ] **Read aloud**: at least the summary; no row of fragments, no three sentences with the same opening
- [ ] **Remove-the-name test** on the opening and summary: with the product name deleted, a stranger can still tell what the text is about
- [ ] **Reads cold, reads whole**: natural to someone who never saw the conversation or feedback rounds that produced it; one voice throughout, no patchwork seams, no sentence explaining why the document was written this way
- [ ] **On a rewrite**: no fact, number, date, or source added or lost
