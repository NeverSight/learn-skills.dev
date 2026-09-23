---
name: agent-docs
description: Writes and audits a repository's AGENTS.md, CLAUDE.md, READMEs, ADRs, docs/refs, and glossary. Use before editing any of them, or to audit, shrink, or dedupe them.
license: MIT
compatibility: The audit script requires Node.js 18 or newer and git, run inside a git repository.
---

# Agent docs

Apply these rules to every doc below, plus the doc rules the repo's root
`AGENTS.md` adds. Where the two disagree, the repo's rule wins.

## Which file holds what

- `AGENTS.md`: conventions for agents. The `CLAUDE.md` beside it holds only
  `@AGENTS.md`.
- `README.md`: a short runbook for people, at the root and in every app and
  package. It covers setup, how to run, test and ship, and the context a new
  developer needs first. Leave out how things work: the code shows it.
- `GLOSSARY.md`: one meaning for each word the docs use two ways.
- `docs/adrs/`: the reasons behind architecture decisions.
- `docs/refs/`: excerpts of outside docs.
- A code comment: a reason tied to one file.

## AGENTS.md

- The root `AGENTS.md` loads in every session. A folder's `AGENTS.md` loads
  later, and not in every agent. (Claude Code loads a folder's `CLAUDE.md`
  once the agent reads a file there with its file-read tool, not through a
  shell. Codex loads each `AGENTS.md` from the repo root down to its working
  directory.) Put a rule that must hold before any file is read in the root.
- Pair a folder's `AGENTS.md` with a `CLAUDE.md` only when the folder has
  conventions of its own. One pair may cover packages whose conventions are
  about how they relate.
- Put a rule in the deepest folder covering every place it applies: two
  sibling folders mean their parent. Never repeat a parent's rule or point
  back to it.
- Keep only what an agent can get wrong with nothing else to stop it: where
  code goes, a boundary, a gotcha that fails silently or only on a real
  deployment, a step no check or hook runs.
- Leave out how things work, file inventories and what a header comment
  says. Leave out anything lint, types, tests or a hook reject with a clear
  message. Keep a tree only when it says where new files go.
- Put the rule that outranks the others first.
- Write terse imperative bullets of at most 25 words per sentence. Keep short
  parallel items inline, separated by commas. Make a list only of ordered
  steps, or of items that are clauses.
- Give a short reason inline when it stops a wrong shortcut. Cite an ADR for
  a long one, as in `(ADR 0003)`.
- Name the exact command for every step. Write "ask the user to" before a
  step the agent cannot take alone, like approving in a browser.
- Keep the rules for writing docs out of `AGENTS.md`: they live here. In the
  root `AGENTS.md`, one line sends the agent here before it edits a doc.

## ADRs

- Add an ADR only for a decision that spans packages or is costly to
  reverse. Add it only when no other place shows its reason, rejected
  alternative or coupling: code, a code comment, an `AGENTS.md`, a README or
  `docs/refs/`.
- Write in it only what those places do not show. Never write in it the
  convention, the code, or what a README says. Applying a convention needs
  no ADR.
- When the decision changes, edit the ADR to match it. Git keeps the
  history.
- When its reason no longer holds, or one of those places now shows it,
  delete the ADR and its citations.
- Read `references/adr-template.md` before writing or editing an ADR: it
  holds the file name, the sections, and the steps to amend or retire one.

## Reference docs

- Fill each `docs/refs/<folder>/` with excerpts of one outside source: one
  file per section of that source, cut to what the repo uses.
- End each file with a footer: `---`, a blank line, then `Reference:` and
  the URLs of the pages it was taken from.
- Keep an inline link's URL only when the link text does not name the
  target. Never pad a table for alignment.
- Make each folder's `README.md` an index: one line per file saying what the
  file answers, with no introduction.
- Index each folder in the `AGENTS.md` it serves, in one line saying when to
  open it. Open a reference doc only when the task touches its topic and the
  conventions leave a question open.

## Glossary

- Use each word with the meaning `GLOSSARY.md` gives it.
- When a change gives a word a second meaning and no other word fits, add an
  entry: one terse bullet with the meaning that holds. When the agent has a
  skill named `glossary`, invoke it for the entry instead.

## After editing

Run from the repo root, with `<skill-dir>` the folder holding this
`SKILL.md` (in Claude Code, `${CLAUDE_SKILL_DIR}` expands to it). Fix what it
reports until it exits 0:

```bash
node <skill-dir>/scripts/audit.mjs
```

## Audit

When the user asks to audit, shrink, tidy or dedupe the docs, follow
`references/audit.md`.
