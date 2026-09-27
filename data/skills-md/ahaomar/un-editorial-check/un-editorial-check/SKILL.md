---
name: un-editorial-check
description: Reads user-visible copy the way a United Nations editor would — language, wording, tone, grammar, hate speech, spelling, terminology, dates, numbers, claims and register — and reports what fails. Use when reviewing web pages, dashboards, blog posts, page titles, meta descriptions or copy baked into JavaScript by a coding agent. Checks HTML, Markdown, plain text and rendered JavaScript string literals only; it is not a code-quality, accessibility, security or SEO linter (those run only as explicit opt-in audits) and it does not judge whether a claim is true.
license: MIT
compatibility: Requires Node.js 18 or later and a host that can load the portable Agent Skills SKILL.md format.
metadata:
  version: "0.8.0"
  source-date: "2026-09-27"
---

# UN editorial check

Run the bundled Node.js CLI before offering editorial judgement. The CLI checks documented rules over extracted copy; it does not prove that prose is clear, neutral, accurate or adequately sourced.

Resolve `<skill-base>` from the directory containing this `SKILL.md`. All paths below are relative to that directory.

## Workflow

1. Run `node <skill-base>/bin/check.mjs <paths>`. Add `--report <path.pdf>` to write a current-to-should-be PDF of the same findings for the user.
2. Address error-severity findings (exit code `1`). Review warnings; do not suppress them merely to obtain exit code `0`.
3. Read the applicable files under [rules/](rules/): [spelling](rules/spelling.md), [terminology](rules/terminology.md), [numerals](rules/numerals.md), [register](rules/register.md), [diplomacy](rules/diplomacy.md), [hate speech](rules/hate-speech.md) and [grammar](rules/grammar.md). Do not restate or reinterpret them from memory.
4. Work through `AGENT REVIEW REQUIRED` findings: whether claims match evidence, figures are sourced and dated, citations are complete, comparisons use aligned years, and labels say what was counted.
5. Report deterministic findings separately from editorial judgement.

## What is checked, and what is not

Only classified user-visible copy is checked: prose in HTML text nodes and attributes that carry copy, Markdown, plain text, and JavaScript string literals that have render evidence (an assignment to a render target, a template or concatenation used as copy, a sentence-like literal). Comments, code, identifiers, URLs, quoted material and cited titles are masked before any rule runs.

Code quality, accessibility, security and SEO findings are **audits**, not editorial rules. They run only when asked for with `--profile publishing`, `--profile accessibility` or `--profile security`, they are reported in their own section, and they never change the exit code.

## Boundaries

Never use `--fix` without showing the user the target files first. `--fix` prints a `(proposed)` diff and writes nothing; `--fix --apply` writes and labels results `(applied)`. It is limited to deterministic replacements (British spelling, `per cent`, en-dash ranges, `the United States`, a doubled word, a space before punctuation and a missing space between sentences) in `.md`, `.markdown` and `.txt` files, and it refuses symbolic links, hard-linked files and anything that is not a regular file. Review every resulting diff. It does not rewrite dates, terminology, claims or exclamation marks.

Exit codes: `0` no error-severity editorial findings, `1` error-severity editorial findings, `2` usage, configuration, scan or write failure. Audits never move the exit code.

Configuration comes from [config/default.json](config/default.json) plus an optional project `.un-editorial.json`, or `--config <file>`. A `--profile` value is either a built-in audit name (`publishing`, `accessibility`, `security`) or a path to an organisation profile JSON file merged over the bundled baseline in [config/profiles/un-v1.json](config/profiles/un-v1.json). Do not invent undocumented configuration keys; the maintained index of rule IDs is [rules/catalogue.json](rules/catalogue.json).

Suppress a single known-good case inside the copy span it belongs to, and record the reason in version control: `<!-- ue:ignore UE-SP001 -->`, `<!-- ue:ignore UE-SP* -->` or `<!-- ue:ignore all -->`. A suppression applies to its own paragraph only.

When `baseOrigin` is configured, canonical URLs are checked against its scheme, hostname and effective port. SRI results certify declaration syntax and required attributes, not whether a digest matches downloaded content.
