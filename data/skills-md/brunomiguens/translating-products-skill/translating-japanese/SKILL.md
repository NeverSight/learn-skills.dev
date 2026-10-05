---
name: translating-japanese
description: Use when refining Japanese translations for the requested locale and register, including politeness, honorifics, omission, counters, loanwords, punctuation, and concise UI copy.
---

# Translating Japanese

## Overview

Revise an approved `translating-core` draft into natural Japanese for the configured locale, market, audience, and product relationship. Preserve meaning, glossary decisions, placeholders, resource syntax, and protected values exactly.

This specialist covers product-focused Japanese, not every social or industry register. Do not claim native-speaker review.

## Capabilities

- `language:japanese`
- `locale:ja`

## Entry Contract

Require an explicit locale or market and a register for each content mode: UI, support/help, marketing, or another declared surface. “Japanese” or “polite” alone may not define the customer relationship. If the locale or required register is missing, return one focused question through the orchestrator and withhold target copy.

Consume the core draft, source context, audience relationship, surface, glossary, protected terms, placeholder types/examples, and length constraints. Do not create copy before project setup and approval. Never install or download another skill at runtime.

## Refine the Draft

1. Preserve facts, intent, approved terminology, placeholders, code, links, markup, names, and version strings.
2. Set a consistent politeness level and voice for the surface. Keep UI labels compact; maintain the approved `です・ます`, plain, or other documented style across long-form prose.
3. Omit subjects, pronouns, and possessives when Japanese context makes them redundant, but retain them when omission would hide the actor or change responsibility.
4. Add an honorific to a placeholder only when the placeholder is known to be a person and the product relationship requires that honorific. Never infer gender, role, status, or personhood from an opaque value.
5. Choose counters from the counted entity and context. Test representative zero, one, and larger values without renaming or splitting the placeholder.
6. Follow approved terminology for native words, loanwords, abbreviations, and script choices. Do not vary katakana and translated terms for stylistic novelty.
7. Use Japanese punctuation and spacing while keeping protected ASCII syntax exact. Check full-width/half-width requirements from the product format rather than mechanically converting Latin text or digits.

Use project context and pinned knowledge first. Research only a concrete unresolved current Japanese market term, product convention, or usage question; record the source and decision through the orchestrator. Do not browse for ordinary grammar or every string.

## Product UI

Express the action or state with the fewest words that remain unambiguous in the screen context. Avoid mechanically retaining “you,” possessives, articles, and source word order. Use labels parallel to adjacent actions and do not add brackets, quotation marks, honorifics, or explanatory nouns merely to create visual boundaries around placeholders.

For notifications, confirm who acted, what changed, and which value anchors the message. Counters belong next to their counted noun in natural order. Check truncation, wrapping, screen-reader speech, and how placeholder values join surrounding kana, kanji, and punctuation.

## Long-Form Content

Maintain the approved politeness level across instructions, conditions, warnings, and calls to action. Prefer coherent Japanese information order and explicit logical connections over sentence-by-sentence English calques. Resolve who performs each action before omitting the subject. When English makes a product the grammatical agent of a causative or continuing state (“X keeps Y ready”), express the capability through a natural Japanese state, means, or possibility construction; do not force the product into an animate-subject template. Keep headings concise while allowing explanatory prose to breathe.

## Common Literal-Translation Failures

- retaining `あなた`, pronouns, or possessives where Japanese naturally omits them
- omitting the actor when responsibility or state ownership would become unclear
- appending `さん`, `様`, or another honorific to every name-like placeholder without relationship evidence
- selecting a generic counter without checking what is counted
- copying English sentence order into awkward long-form Japanese
- preserving an English product-as-agent causative that is grammatical but unnatural in Japanese
- mixing politeness levels or honorific treatment across related content
- adding quotation marks around placeholders without semantic reason
- mechanically converting protected ASCII, digits, `API`, versions, URLs, or code to full-width forms
- inconsistent loanword, native-term, or script choices despite the glossary

## QA Handoff

Pass source, core draft, revision, locale/market, surface register, relationship assumptions, glossary, protected values, and constraints to `reviewing-translations`. Verify:

- meaning, actors, facts, names, numbers, links, placeholders, and structure remain complete
- politeness level and honorific treatment match the configured relationship consistently
- omitted subjects remain recoverable and do not alter who acts or owns a state
- counters and surrounding grammar work for representative runtime values
- approved loanwords, native terms, abbreviations, and script choices remain consistent
- punctuation, spacing, and full-width/half-width behavior fit the output format without corrupting protected syntax
- UI copy is concise and unambiguous in context; long-form prose has natural Japanese information flow

Block the affected segment on missing locale/register, unjustified honorifics, unclear actor after omission, counter mismatch, register drift, literal word order, glossary inconsistency, or protected-value corruption. Return only the smallest failing segment to the responsible specialist.
