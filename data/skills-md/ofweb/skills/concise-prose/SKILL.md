---
name: concise-prose
description: Write and review concise prose across documentation, source comments, and commit messages. Use STE100 for all authored prose and run prose-check after writing.
---

# Concise prose

Use this skill when writing or substantially editing prose, including Markdown
documentation, design documents, specifications, README and AGENTS files,
source documentation comments, and commit messages. Document-specific skills
decide what information belongs in each artifact.

Before writing, read and follow [ste100/SKILL.md](ste100/SKILL.md). All authored
prose uses STE100. Preserve verbatim material as-is: code, command output,
protocol strings, identifiers, quoted external text, and exact product or API
names where rewriting would be incorrect.

Optimize for information density.
Prefer deleting redundant or unnecessary text over rewriting it. Preserve useful
technical information and its intended meaning.
Avoid repeating information already stated in nearby prose.
State behavior directly.
Avoid introductory prose, summaries of the immediately preceding text, and conversational filler.

After writing or substantially editing prose, run `prose-check` on edited Markdown files.
Pass other authored prose on standard input. The command checks STE100 first.
When STE100 passes, it runs Vale. Treat findings as work to fix and rerun the
checker. Stop when the checked prose passes. Ask for the vocabulary review
below. Ask about other findings only when a semantic decision prevents a safe fix.

For project files, `prose-check` combines three vocabulary sources:

- `shared-terms.json`: common software engineering and workflow language that
  is broadly reusable across projects.
- `.workflow/ste-glossary.json`: intentional project or domain language without
  a special canonical project meaning.
- `.workflow/context.md`: project concepts whose meaning must remain stable
  and explicit across contexts.

`shared-terms.json` belongs to the `ofweb/skills` repository. When developing
this skill there, add reviewed, broadly reusable engineering and workflow terms
directly to that file. In a consuming project, treat the installed file as read-only.
Use the project's glossary for intentional local vocabulary and Context for
canonical project concepts. Do not edit the installed skill copy from a
consuming project. Suggest repeated local terms for promotion to shared
vocabulary when they could help many projects. Make and review that change in
`ofweb/skills` before it enters the common language profile.

Put reviewed terms in an `approved_terms` list. Each entry has a `word` and
only the `inflections` that the prose needs. Add `part_of_speech` only when it
helps distinguish a verb or adjective. The pinned checker still needs its
native noun and verb lists; `prose-check` builds those lists at run time.
Existing project glossaries with `technical_nouns` and `technical_verbs` still
work. Do not use a glossary term to change the approved meaning of an ordinary
STE100 word. Keep meanings and feature behavior out of the project glossary.
Use `--project-root` for standard input or files outside the project tree.

Keep exact product names, mod names, API names, commands, and identifiers
verbatim. Do not approve their fragments as vocabulary. Inline code is already
excluded from STE100 input. For plain-text exact names, add the complete name
to `exact_names` in `.workflow/ste-glossary.json`. This only filters vocabulary
findings within that name. Use the exact capitalized spelling. Put lowercase
identifiers in inline code. Sentence checks still see the full text.

Use Context only for a project concept with a stable canonical meaning. Prefer
a multi-word concept when its special meaning belongs to the phrase. A generic
word does not need Context merely because STE100 does not know it. For example,
`reservation` can be a shared term while `Job reservation` can be a Context
concept. The checker approves unknown words only inside the complete Context
phrase, so the individual words do not gain general approval.

When STE100 reports unknown words, first ask if simpler approved language can
preserve useful meaning. Prefer that rewrite over a vocabulary exception.
Collect all distinct unknown words with
`prose-check --vocabulary-report '.workflow/**/*.md'`. The report groups observed forms and counts their total
use. Search existing vocabulary, Context, and project documents when usage
helps classification. Classify every remaining term as one of these:

- `rewrite`: simpler STE100 wording preserves the meaning.
- `shared`: necessary software or workflow language useful across projects.
- `project`: necessary local or domain language without a special meaning.
- `context`: a project concept whose exact meaning must remain stable.
- `checker`: an exact name, identifier, false positive, or extraction problem.

Rewrite safe `rewrite` cases without asking the user. Investigate `checker`
cases and fix the tool or exact-name list where appropriate. Rerun
`prose-check` after each pass. Do not stop with raw checker output.

Add vocabulary only if replacement would reduce precision, clarity, or
consistency, or make the prose awkward. Repeated use suggests intent, but it
does not approve a term by itself. Be especially conservative with ordinary
adjectives, abstract nouns, jargon, rare words, and words that approved STE100
language can express clearly. Vocabulary supports necessary terminology; it
must not recreate unrestricted English.

Before adding vocabulary, present one compact review group of real decisions.
Group trivial noun and verb forms under one canonical candidate. For each
candidate, show its source (`shared`, `project`, or `context`), observed forms,
and a short reason an approved replacement does not work. Include one short
project example when the classification is unclear. Do not show raw lint output
unless requested. Wait for the user's review before adding vocabulary.

Apply accepted project terms to `.workflow/ste-glossary.json`. Add a Context
concept only after its canonical meaning is agreed. Change shared vocabulary
only in `ofweb/skills`, after review. Do not edit the installed copy from a
consuming project. Rerun `prose-check` after each accepted vocabulary pass.
Continue rewriting avoidable words until STE100 passes. Then fix Vale findings
and rerun the checker. Do not soften sentence structure, verb usage, approved
meaning, sentence length, ambiguity, or complexity rules to approve a term.
The pinned checker does not enforce part of speech for technical terms. Review
their verb use and intended meaning directly.
