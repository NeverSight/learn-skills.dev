---
name: oss-writing
description: "Write clear technical prose for anything that lives in a repository or on a forge: commit messages, PR titles and descriptions, PR and code review comments, issue text, READMEs, documentation, CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, changelogs, ADRs. Use it when someone says commit this, open a PR, reply to a review comment, or file an issue. Use this whenever you are about to write or edit any of them, including short ones. A one-line commit message or a two-sentence review comment looks too small to need a skill, and that is exactly where the tells show up. Not for prose that needs a personal voice, such as blog posts, essays, or launch announcements."
license: MIT
---

# Repo prose

Write with clarity and force for a reader whose first language is not English. Be terse.

This skill owns how the sentence reads, which is one rule: R-DOC-05 documentation prose. The skill that owns the artifact owns what goes in it, and where a caller states an exception, the caller wins.

When `oss-audit-report.md` exists at the repository root, read the group addressed to this skill and work from that. Each failing rule there carries the audit's evidence and that rule's `Check:` text verbatim, so reading `STANDARD.md` as well adds nothing. Where the file is absent, work from the request as usual.

## Read the local contract first

Before drafting, read the repository's instructions, contribution guide, templates, and the most recent accepted examples of the same artifact. They decide the commit convention, the required sections, the terminology, and the audience. Follow the convention the repository declares rather than inventing one, and keep required template sections and legally mandated wording. Past examples show a convention's shape. They do not lift a limit this skill sets: only a stated rule does.

Verify every claim against the diff, the source, or command output. Prose that reads well and says something untrue is the one failure no rule below catches.

## Core rules (all artifacts)

- State things in positive form. Keep a negative where prohibition is the point.
- Use specific, concrete, definite words: `fails on files over 2 MB`, not `fails on large inputs`.
- Omit needless words. Never drop a word that carries a fact, condition, or scope.
- Avoid succession of loose sentences.
- Keep related words together.
- Keep to one tense in summaries.
- Write one instruction per sentence.
- Keep an instruction to 20 words. Keep any other sentence to 25.
- Write one topic per paragraph. Use at most six sentences per paragraph.
- Do not stack more than three nouns in a row.
- Use parallel form for parallel ideas.
- Put the most important word at the end of the sentence.
- Use serial commas.
- Put conditions before instructions: "to reset the cache, run `make clean`".
- Use vertical lists for complex or sequential content.

### One instruction per sentence

- Bad: Install the package and then set the token before you run the build.
- Good: Install the package. Set the token. Run the build.

### Noun cluster

- Bad: network access cost optimization proposal
- Good: a proposal to optimize the cost of network access

## Triggers (read the reference before writing)

- Before naming a branch, or writing a commit message or change request description, read [references/commits-and-change-requests.md](references/commits-and-change-requests.md).
- Before writing or replying to a review comment, read [references/code-review.md](references/code-review.md).
- Before writing a README or documentation, read [references/docs-and-readme.md](references/docs-and-readme.md).
- Before writing agent-facing text (AGENTS.md, skills, prompts), hold every sentence to 20 words and keep one meaning per word.

Ship the revision, not the draft.

## Check before returning

Read the draft against this list and fix what it catches.

- Find the longest sentence and count its words. Over 25, or over 20 for an instruction, and it splits. Two clauses joined by `and` or `so` are usually two sentences; a relative clause opening with `which` is usually the second half of one.
- Count the characters in a commit subject or change request title, plus any ` (#123)` the forge appends on squash. Over 72, and it moves detail into the body. A subject that lists several changes means the commit should be split.
- No em dashes, en dashes, or ` -- `. In short technical prose they are a reliable machine-written tell. A period, comma, colon, or pair of parentheses carries the same break.
- No emoji anywhere, including headings and bullets. Their width and glyph vary by terminal and font, so they break alignment in fixed-width contexts.
- Headings in sentence case, not Title Case. The Google style guide prescribes it. Mixing the two inside one document reads as text assembled from two sources.
- Straight ASCII quotes. Curly quotes break a copy-paste into a shell or a config file, and the reader cannot tell by eye which they got.
- Never inflect a code element or use one as a verb: `send a POST request`, not `POST the data`; `the --force flag`, not `force it`.
- No promotional adjective describing the project: `robust`, `powerful`, `seamless`, `comprehensive`, `blazing`, `effortless`. Name the property instead: `retries 3 times`, `no config file`.
- No recap section restating what the text just said. The reader just read it.
- No boilerplate caveats. State a precondition, limitation, or risk when it changes what the reader should do. A caveat that changes nothing trains the reader to skip the one that matters.
- No contrast with an invented alternative. In `X rather than Y` or `X instead of Y`, keep Y only when Y exists outside the draft. A prior behavior, a real endpoint, or a default the reader would hit qualifies. `Instead of returning a deck nobody asked for` names code nobody wrote. Delete that clause and let X stand.
- No clause telling the reader how to weigh a fact just stated. Delete the clause and see what is lost. If no fact goes with it, it was defending the sentence. A constraint or a consequence is a fact and stays. An alternative stays only when the contrast check above keeps it.

Fix what the list catches, then read the revision against the list again, because a rewritten sentence can break a rule the original passed. Return the draft only when a full pass catches nothing.

If the draft still reads padded, generic, or promotional after that pass, the remaining fault is lexical. Check it against [references/tells.md](references/tells.md), which names each pattern and what to write instead.

Run `scripts/prose.mjs` in this skill's own directory over the files you touched, before returning them. It reports the part of the list above that a regex can decide, with a file and a line for each hit. It needs Node 22 or later, or Bun, and nothing installed:

```sh
node <this skill's directory>/scripts/prose.mjs README.md docs/
```

By default it reports what R-DOC-05 names: em and en dashes, ` -- `, emoji, Title Case headings, and the six promotional words that rule lists. `--house` adds the rest of the house style, where every hit needs your judgement rather than a fix. `--length` adds sentences over 25 words and is noisy on purpose. It exits 1 when it reports anything.

The script skips fenced blocks and inline code, so a quoted dash in sample output is not a finding, and a rule may name inside backticks the pattern it forbids. It cannot tell a heading's proper noun from an ordinary capitalized word, so a wrongly flagged heading means passing `--proper` with a file of terms rather than rewriting the heading. A heading that a required template sets stays as the template writes it: its hit is expected, so leave it.

An install that brings in this skill alone still has the script, because it sits inside this directory. Anything calling it from another skill checks that it is there and reads the files itself when it is not.

To enforce the same rules in CI rather than at the end of a draft, see [references/linting.md](references/linting.md). It maps each checkable rule onto a checker, and names the rules no checker can decide.

## Do not touch

- Existing quoted code, error strings, log output, stack traces, and config samples: reproduce verbatim, including their dashes. This exception does not protect newly authored strings from review.
- Another person's words in a quote or a review thread reply.
- Identifier names, CLI flags, and file paths.
- Required legal, license, and externally mandated security-advisory wording.
- When editing prose a human wrote, fix only what is broken. Their voice is not a defect.
