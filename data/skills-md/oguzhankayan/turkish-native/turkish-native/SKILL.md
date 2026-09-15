---
name: turkish-native
description: |
  Write and rewrite Turkish so it reads as native Turkish rather than translated English.
  Use for Turkish marketing copy, product and UI text, localization, documentation, support,
  legal or security prose, and reviews of AI-written Turkish. Detect translationese, copied
  clause structure, nominalization, wrong case and collocations, generic helper verbs, SaaS
  and sales calques, jargon leakage, forced slogans, corporate abstraction, cross-sector
  template residue, unsupported operational claims, and page-level repetition.
license: MIT
metadata:
  version: "0.5.0"
---

# Turkish Native

Write Turkish as Turkish. Do not preserve the sentence skeleton of English or another source language and merely replace its words with Turkish ones.

A sentence can be grammatically valid and still sound translated. Work from meaning, not source-language shape.

## Core test

Before keeping a sentence, ask:

> If I had received only this meaning, with no source-language wording, would I naturally build the Turkish sentence this way?

If not, rebuild it from the intended meaning.

## How to work

1. **Identify the job.** Determine audience, medium, register, sector, and intended action. A landing-page hero, button label, legal notice, clinic page, and API document need different Turkish.
2. **Extract the meaning.** Separate facts and required terminology from wording. Preserve names, numbers, claims, dates, links, commands, legal terms, identifiers, and product behavior.
3. **Fix structure before vocabulary.** Check clause structure, word order, case, references, verb choice, and collocations first.
4. **Check domain fit.** Make sure fields, CTAs, process steps, labels, and examples belong to the actual sector and task rather than a neighboring template.
5. **Rebuild instead of patching.** If the sentence is structurally foreign or domain-wrong, rewrite it around its main meaning. Do not repair translationese one word at a time.
6. **Read it as Turkish.** A native reader should not need to reconstruct another language mentally.
7. **Check fidelity.** Do not invent, remove, strengthen, weaken, or generalize factual claims, operational promises, source labels, or regulated-domain outcomes.
8. **Check restraint.** Do not rewrite natural Turkish merely because another phrasing is possible.

## Voice and register

Match a supplied writing sample or existing product voice. Preserve deliberate short sentences, colloquial expressions, terminology, humor, or formality when they fit the audience.

Do not turn natural Turkish into corporate Turkish. `Sen satışa bak.` can be better than a longer formal alternative. Do not force every English loanword into Turkish: `link`, `demo`, `dashboard`, `API`, `MCP`, and `commit` may be natural in technical or product contexts.

## What to return

- **Write mode:** return the finished Turkish text. Explain rules only when asked.
- **Review mode:** briefly identify important problems and give a revised version. For page reviews, `Bölüm | Mevcut | Önerilen` is often useful.
- **File mode:** change prose only unless instructed otherwise. Preserve code, commands, URLs, route names, placeholders, translation keys, variable names, frontmatter, and machine-readable structure.
- **Embedded mode:** when another agent invokes the skill, return only the requested final copy unless analysis is requested.

## Translation and localization

Preserve meaning, scope, and product terminology, but do not preserve source-language word order, clause boundaries, or part of speech unless Turkish naturally uses the same structure. A good translation may split or merge sentences, drop an explicit pronoun, turn a noun into a verb, or replace a source-language metaphor with a direct statement.

If the user asks for a literal, legal, or line-by-line translation, honor that fidelity while still using grammatical Turkish.

## Pattern references

This skill contains **57 Turkish-specific patterns**. Read the relevant bundled reference before rewriting; for broad copy review or translation, read all six.

- **1–10 Sentence architecture:** `references/01-sentence-architecture.md`
- **11–20 Verb choice and lexical fit:** `references/02-verb-and-lexical-fit.md`
- **21–30 Product, UI, and localization:** `references/03-product-ui-localization.md`
- **31–40 Marketing and model-written copy:** `references/04-marketing-model-copy.md`
- **41–51 Register, fidelity, and final checks:** `references/05-register-fidelity.md`
- **52–57 Domain and page integrity:** `references/06-domain-page-integrity.md`

These are diagnostic rules, not search-and-replace rules. Context always wins.

## Non-negotiable checks

Before returning the text, verify that:

- meaning and factual scope are preserved,
- clause structure is Turkish rather than copied from another language,
- verbs fit their nouns and real actions,
- case suffixes and references are clear,
- product copy uses user language rather than database language,
- every field, CTA, process step, and example belongs to the actual sector and task,
- marketing copy does not repeat or inflate ordinary claims,
- operational promises, medical or other high-stakes claims, privacy statements, ratings, and source labels are supported,
- synthetic examples are not presented as sourced customer evidence,
- process sections describe a real process rather than narrating obvious buttons or navigation,
- legal, security, and technical text preserves precision,
- natural colloquial Turkish has not been “improved” into corporate prose,
- one repaired shape has not been copied onto every sentence, and no line repeats what another line on the same page already said,
- the result sounds native when read without the source.
