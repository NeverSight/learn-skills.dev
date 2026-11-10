---
name: latex-cleanup
user_invocable: true
description: Review LaTeX documents for common issues, style consistency, typography, cross-references, draft artifacts, and debugging code. Use after editing LaTeX documents or before submission.
---

# Review LaTeX documents

Review technical correctness by default. Do not rewrite prose or modify files unless the user asks.

## Scope

Use a user-provided manuscript path when available. Otherwise, identify the build entrypoint from the project configuration and TeX structure. Follow `\input` and `\include` dependencies rather than reviewing only the main file.

Build with the project's normal entrypoint when possible. Inspect both the compilation log and rendered PDF; do not infer page-layout problems from source alone.

## Compilation and submission checks

- Compilation errors and missing source, bibliography, or figure files.
- Undefined references and citations, duplicate labels, and visible `??` markers.
- Overfull and underfull boxes, including their visible effect in the PDF.
- `draft` document-class or package options, `showkeys`, `lineno`, `\overfullrule`, and other debugging aids that should not ship.
- Document-class options, margins, and required front matter when venue requirements are available. Do not guess venue rules.

## Cross-references and floats

- Flag undefined, duplicate, unused, and broken cross-file labels.
- Verify that every figure and table is referenced in the text and that placement specifiers are reasonable.
- For each float family separately, compare float source order with the order in which labels are first referenced in manuscript reading order. Flag figures, tables, algorithms, or other floats first referenced out of sequence; do not impose one global order across float types.
- Inspect rendered pages for widows, orphans, awkward float placement, and obvious whitespace problems. Treat manual page breaks as a last resort rather than the default fix.

## LaTeX consistency

- Use non-breaking spaces before citations and references, between quantities and units, and after titles such as `Dr.~Smith`. Do not insert `~` before `\footnote{}`.
- Keep citation commands and grouping consistent with the project's citation style.
- Keep heading and caption capitalization, list punctuation, and forms such as `Figure` versus `Fig.` consistent. Spell out abbreviations at first use.
- Keep mathematical notation and variable names consistent. Use `\text{}` for words in subscripts, standard operators such as `\log` and `\Pr`, and `\operatorname{}` for custom operators.
- Typeset negative numbers in math mode. Keep reference forms such as `Section~\ref{}` versus `Sec.~\ref{}` consistent.

## Draft artifacts

- Flag `TODO`, `FIXME`, `XXX`, `HACK`, `TBD`, `PLACEHOLDER`, literal `Lorem ipsum`, `\lipsum`, `\todo`, `\note`, `\marginpar`, and similar draft material.
- Flag long commented-out sections and comments that are clearly stale or submission-facing. Do not treat ordinary explanatory comments as defects.
- Verify that URLs are valid and correctly escaped when link checking is in scope.
- Report unused packages or bibliography entries only when there is evidence they are unused; do not recommend speculative deletion.

## Typography and source formatting

- Use TeX opening and closing quotation marks for double and single quotes rather than straight quotes:

```latex
``double quoted text''
`single quoted text'
```

- Distinguish hyphens, en dashes, and em dashes. Do not put spaces around em dashes.
- Use `\ldots` or `\dots` for ellipses and escape `%`, `&`, `#`, `$`, and `_` where required.
- Keep one sentence per source line unless the project specifies another convention.

## Prose review when requested

Preserve the author's voice. Correct demonstrable errors in subject-verb agreement, articles, tense, modifiers, parallel structure, fragments, and run-on sentences. Check `which` versus `that`, `less` versus `fewer`, `between` versus `among`, and `compared to` versus `compared with` in context. Treat phrases such as `in order to`, `a total of`, and `the fact that` as compression candidates, not automatic substitutions.

## Report

Prioritize compilation failures, missing content, unresolved references, and submission blockers. Give a file and line for each source finding, cite log or rendered-page evidence when relevant, and propose a concrete fix. Separate demonstrated problems from preferences or venue-dependent judgments. Do not enumerate checks that passed unless the user requests a checklist.
