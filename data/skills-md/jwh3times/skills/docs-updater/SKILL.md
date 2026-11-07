---
name: docs-updater
description: Bring the repository's documentation in line with the code — find where the docs and the code disagree, and fix the docs (or, in check mode, only report it). Use after a feature, fix, or architectural change; when the user asks to update or audit the docs; and from ship and end-session, which run it scoped to a branch's diff.
metadata:
  settings: docs workspace issue-tracker human-follow-up
---

# Docs updater

Find drift between what the docs say and what the code does, then fix the docs. The code is the
truth: never invent a feature, a command, or a capability the code does not have.

**Announce at start:** "I'm using the docs-updater skill to bring the docs in line with the code."

Run shell snippets in bash (Git Bash on Windows).

## 0. Settings

This skill reads `docs/agents/docs.md`, `docs/agents/workspace.md`,
`docs/agents/issue-tracker.md` and `docs/agents/human-follow-up.md`. Follow
`.agents/skills/docs-updater/settings/README.md` to read them and complete any that are missing; the
definitions sit beside it.

## 1. Mode and scope

Take both from the arguments or the caller's instructions:

- **Mode** — `fix` (the default) edits the docs; `check` edits nothing and reports drift.
- **Scope** — a diff range (`<base>..HEAD`), a list of changes, or none for a full audit of every
  `Doc map` item.

A caller may add constraints; follow them. From `ship`: the branch is not merged, so leave
`ship-owned` documents alone and make no claim that the work shipped — no roadmap, archive, release
or merge status, or board change. Describing what the branch implements is still in scope. From
`end-session`: the session's work, merged or not, as it says.

## 2. Find the documents in scope

For a diff range:

```bash
git diff --stat "$range"
git diff --name-status "$range"
```

Read the diff itself, not only the file list. Skip generated copies (the mirrors the
`Generated-config check` regenerates) and read their sources instead. Skip the bodies of the skills
the `Doc map` marks `frozen` too (installed, and never edited here): read only what their change
means for claims in other documents, such as a renamed setting or a new command. A repository that
installs its own skills skips the installed copy, never the authored source it was installed from.
Match each change against every `Doc map` item's **when**: the paths it names, and the kind of
change (a new endpoint, a changed command, a new setting, a removed feature). A **when** is a
signal, not a limit: a change that plainly affects a document it does not match is in scope too, and
is named in the report so the `Doc map` can be extended. A pure refactor often owes no doc edit; say
so rather than inventing one. For a list of changes, match the same way. For a full audit, every
item is in scope.

Then search for the names the diff removed or renamed (settings, commands, files, flags, counts
such as "all four"), and for names whose meaning it widened or narrowed: stale references to them
are drift that no **when** predicts. For a member the
diff adds to an enumerated set (a marker, a setting, a skill), search for its siblings instead: a
list that names them but not the new one is now incomplete. Search for a name as it is written in
the docs, usually in backticks (`` `frozen` ``), so a common word does not bury the hits. Search
wider than the `Doc map`, skipping generated copies and `frozen` documents:

- every tracked Markdown file (`git ls-files '*.md'`);
- the companion, from its own root, when its checkout exists;
- each wiki: the `Follow-up wiki`, and any `Doc map` item that lives in a wiki, when the change is
  on the default branch, in a read-only clone in a scratch location.

A hit in a document the `Doc map` lacks is fixed like any other and named in the report, so the map
can be extended. A wiki waits for the merge, so its pages never point at a file that is not there
yet: a run on an unmerged branch (every run from `ship`) skips it and reports that the wiki search
is owed after the merge. The next `end-session`, or any run on the default branch, performs it and
fixes what it finds.

## 3. Check each document against the code

Read each document in scope, then verify every claim the change could affect against its source of
truth: the `Drift probes`, and otherwise the code, manifests, configs and CI workflows themselves.
Executable config outranks prose. Count what a probe lists rather than trusting a number in a doc
(CI jobs by their top-level keys, not by every `name:`).

A scoped run reports drift it finds outside its scope (an older claim a probe contradicts) without
fixing it: that drift belongs to its own change. A full audit fixes it.

**Companion documents.** When the `Private companion` is set, require its checkout before reading
or editing them, and inspect it from its own root (`git -C private status`, `git -C private log`):
the outer repository's history is never evidence about it. When the checkout is absent, check the
public documents and report which companion checks could not run; create nothing in its place.

## 4. Fix (fix mode)

Edit each drifted document, honoring its marker:

- `frozen` — never edit. `append-only` — add, never change. `amend-only` — add a dated amendment
  note.
- `owner-only` — report the drift; the user edits it.
- `ship-owned` — leave it to `ship`. Outside `ship`, add an `Unreleased` changelog entry at most;
  never a version, date or dated section.
- `pinned` — another check fingerprints it, and any edit, even to a link, fails that check until
  the pin it names is updated. Edit it only when the change requires it; first confirm the edit
  alters nothing the pin protects (requirements, matrix rows), then update the pin in the same
  change, and name both in the report so the caller's PR says why. A `pinned` document in scope
  that needs no edit keeps its pin; still check that the pin matches it, and report it current.

Write so the next reader trusts the docs:

- **One home per fact.** Update a fact where the `Doc map` says it lives, and point to it from
  elsewhere instead of copying it. A thin entry point (`CLAUDE.md` importing `AGENTS.md`) gets no
  content of its own.
- **What is, not what is planned.** Project guides describe implemented behavior. Work state —
  status, next steps, to-dos — lives in issues, not Markdown: a doc may state the resulting contract
  ("the secret is in the vault"), never the pending action.
- **The rule that survives.** History belongs in the changelog and ADRs; a doc records the current
  rule and may cite the issue that set it. In a document that mixes the two (a survey beside the
  design built from it), update the current-state claims and leave dated findings as written.
  Remove a known limitation only when the code shows it fixed.
- **Decisions and vocabulary.** Never edit an accepted ADR to match the code; report the
  contradiction. When a glossary (`CONTEXT.md`) defines a term, point at it rather than restating
  the definition, and do not rename code to match new vocabulary.
- **Keep private things private.** Nothing on the `Doc map` **Never in public docs** list, no
  secrets, credentials, account identifiers, live resource names, or links into the companion goes
  into a public document. A security weakness follows the `Security findings` route, never a public
  page.
- **Generated files.** Edit the source, never the generated copy, then run the
  `Generated-config check` regenerate command. Leave agent and skill frontmatter alone unless asked.
- **Setup steps** change only when a prerequisite, command or port really changed.

Leave every edit uncommitted, in the public checkout and the companion alike: the caller commits,
or the user does when the skill ran on its own.

## 5. Human actions

List every required human action the change leaves (access setup, a dashboard change, credentials,
a manual check), or say that there are none. Run from `ship` or `end-session`, return the list to
the caller, which runs the follow-up procedure once for all of it. Run on its own, run the
`## Procedure` in `.agents/skills/docs-updater/settings/human-follow-up.md` yourself. Either way, a
follow-up never lives only in a doc.

## 6. Validate

- `Docs validation`, each command from its folder (the repository root when none is named).
- `Generated-config check`, when its setting says to run it.
- `git diff --check` for whitespace errors.
- Links and anchors in every edited document resolve: relative paths exist, and `#anchors` match a
  heading in their target.

A failure caused by this run's edits is fixed before reporting. Never suppress or work around a real
failure; report it.

## 7. Report

Report private-content leaks first, in either mode. Then, one line per document, labelled in plain
text:

- **current** — checked against the code, no change needed;
- **changed** — what changed (fix mode);
- **drift** — what disagrees and with which source: left unfixed in check mode, or not resolvable
  from the code alone (a feature disabled or removed?), or in an `owner-only` or `frozen` document.

Then the changes no `Doc map` item's **when** matched, the human actions found (and, run on its
own, their follow-up links or the publication blocker), validation results, companion checks that
could not run, and that the edits are uncommitted.
