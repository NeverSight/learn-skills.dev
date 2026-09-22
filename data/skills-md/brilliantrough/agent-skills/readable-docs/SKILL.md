---
name: readable-docs
description: Write and edit human-facing project technical text for scanning, wherever it lives — README, specs, design notes, plans, reports, runbooks, changelogs, and project memory, not only docs/ or StrictDoc. Use whenever creating or revising these records, without waiting for an explicit style request; also for 说人话、去 AI 味、精简文档、短语分点、PPT 式表达. Prefer Chinese phrases, lists, and compact comparison tables while preserving facts, conditions, evidence, and required structure. Not a detector-evasion or creative-writing skill.
---

# Readable Docs

## One job

Make project technical records easy to scan and use: **facts first, findability second, brevity third, natural wording fourth**. Write like useful slide notes, not an essay or a slogan deck. Complete information does not require complete sentences.

Apply this style when writing the original text, not only when asked to polish it. It works alongside the active task or memory skill; it does not create an extra report, approval step, or document.

## 1. Read for meaning

- Read the relevant source and its context. Identify what the reader needs to know, decide, or do.
- For an edit, stay within the requested scope. Do not bulk-rewrite archives, quoted evidence, or unrelated documents.
- Preserve facts and their relationships: actors, actions, causes, conditions, exceptions, negation, alternatives, and uncertainty. Do not turn an observation into a rule or a proposal into a decision.
- Keep exact technical names, paths, commands, configuration keys, versions, dates, numbers, units, and source references. Never invent specifics, experience, opinions, or evidence to make the text feel human.
- Preserve required sections, output paths, status fields, and instruction strength. Shortening “must” into “may” is a behavior change, not copyediting.

## 2. Structure for scanning

Put the useful conclusion, status, or next action first. Use headings that tell readers what they can find; avoid empty headings such as “综合分析” when “失败后如何恢复” names the actual content.

| Content | Default form |
|---|---|
| Independent facts, constraints, findings | Bullets; one point per item |
| Steps, priority, chronology | Numbered list; actions in order |
| Alternatives or changes on shared dimensions | Comparison table; one dimension per row |
| Parameters, states, evidence | Compact lookup table when columns help retrieval |
| Causal chain, mechanism, derivation | Short connected paragraph when splitting would hide the logic |
| Commands, config, literal errors | Code block; explanation outside it |

- Do not force everything into a list or table. A clear sentence needs no wrapper.
- Use tables for lookup or comparison, not as boxes for paragraphs. Move long rationale below the table or into the relevant subsection; keep the essential condition beside the claim.
- If a list item contains several independent points, split it. If it needs deep nesting, regroup under a concrete heading. Keep qualifications with the point they qualify.
- Avoid headings with no content, repeated introductions and conclusions, and multiple formats repeating the same information. A short overview can point to necessary detail instead of duplicating it.

## 3. Write phrases, not filler

Use the user's language, Chinese by default. Keep established technical terms stable rather than rotating synonyms.

- Prefer phrases and short clauses. Omit a subject or object already clear from the heading or context; name it when several actors could be meant. Do not require full sentences or final punctuation for every bullet or cell.
- Front-load the differentiator: “仅首次安装询问”, not “需要说明的是，在首次安装的情况下，系统会进行询问”.
- State actions and effects directly: “保留本机值”, not “通过相应机制实现对本机值的有效保留”.
- Remove empty setup, praise, and unsupported significance: “下面将详细介绍”, “值得注意的是”, “显著提升”, “奠定坚实基础”. These are editing signals, not banned words; keep wording that carries actual meaning.
- Replace vague claims with facts already supported by the source. If evidence is absent, say so or omit the claim; do not manufacture numbers or testimonials.
- Use occasional adjacent `PS:` notes for secondary rationale. Required precautions, exceptions, and failure handling belong in the main text, not an aside.
- Use emphasis sparingly. Do not bold every bullet label, add decorative icons everywhere, force three points, alternate sentence lengths mechanically, or impose word-count quotas.
- Do not add fake personality, first-person feelings, deliberate errors, or colloquial filler. Do not mechanically ban passive voice, punctuation, lists, or ordinary Chinese parallel phrasing.

Read [references/examples.md](references/examples.md) when calibrating the style or when unsure whether a shorter version loses meaning. The examples are patterns, not mandatory document templates.

## 4. Check meaning and presentation

Before returning or saving the text:

- Compare against the source: same facts, conditions, scope, uncertainty, and normative force? No new claims, missing caveats, or swapped actors?
- Scan only the headings, first words of bullets, and table headers: can a reader find the conclusion, differences, and actions?
- Read the longest bullet and table cell: split or relocate it if it contains a paragraph in disguise. Keep connected prose where it explains more clearly.
- Keep raw quotations, code, configuration, and machine-readable structure intact. In StrictDoc, edit prose fields without changing UIDs, grammar, relations, statuses, or delimiters merely for style.
- Use the document's existing format checks. After `.sdoc` or StrictDoc config changes, run `strictdoc export .` from the docs root and inspect the relevant exported content. Export success proves syntax, not writing quality.

Deliver the requested text or file change, not a writing scorecard or an unsolicited explanation of every edit. If a source gap prevents a trustworthy rewrite, name that gap briefly.
