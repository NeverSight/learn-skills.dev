---
name: commit-documentor
description: After committing, check whether the change needs documentation, draft the doc updates for approval, and on approval publish them — to a separate documentation repository (branch + PR by default), or to a docs tree in this repo for projects that have no separate docs repo. Uses a committed config for the doc location, a committed doc index to keep queries cheap and in sync, and user-defined rules for what does and does not warrant a doc update. Use when the user runs commit-documentor, or asks to document, sync, or check docs for their recent commits.
---

# Commit Documentor

Reviews the commits the user just made, decides whether they change anything the
documentation claims to describe, drafts the doc edits, and — only after the user
approves — publishes them.

See also: [USE_CASES.md](USE_CASES.md) for trigger phrases and a worked example,
[references/rules.md](references/rules.md) for how the applicability rules are
evaluated, and the [top-level skills index](../USE_CASES.md).

**Every write here is outward-facing** — a push to a separate docs repository, or a
commit to the user's own branch. Never commit or push without an explicit approval
in this conversation for the specific diff you are about to publish.

## Two modes

Set by `mode` in the config, chosen once during first-run setup:

- **`repo`** (default) — docs live in a **separate repository**. Publishing means
  branch → commit → push → PR against that repo.
- **`local`** — the project has no separate docs repo, so this skill creates and
  maintains docs **inside this repo** under `local_docs.docs_root`. Publishing means
  a commit on the current branch, scoped to the docs paths only. **It never pushes**
  in local mode — the user pushes docs along with the rest of their work.

Everything else — the doc index, the rules, the classification logic, the approval
gate — is identical in both modes. `scripts/doc-repo.sh` handles the difference;
run `scripts/doc-repo.sh mode` if you need to know which one is active.

## First run: setup

If `scripts/doc-repo.sh config` exits 3, nothing is configured yet. Do the whole
setup **before** touching any commits, and **write the config file exactly once**
at the end of it — do not create a partial config and amend it.

**Do not guess a documentation location.** Ask the user in one grouped question
(a single `AskUserQuestion` with multiple questions, not a sequence of separate
turns):

1. **Where do the docs live?** Options: a separate docs repo (ask for the local
   clone path, the remote URL, the base branch, and the docs root within it) —
   or *"no separate docs repo"*, in which case **offer local mode**: this skill
   will create and manage a `docs/` tree in this repo instead. Do not treat
   "no docs repo" as a reason to stop; local mode is a first-class answer.
2. **What should never trigger a doc update?** e.g. chore commits, dependency
   bumps, test-only changes → `rules.exclude_commit_types`, `rules.exclude_paths`.
3. **What must always trigger one?** e.g. anything under the API or config
   surface → `rules.always_document_paths`.
4. **Anything else to always or never do** when editing docs →
   `rules.instructions`.

Only if the user declines to answer at all — they don't want docs managed either
way — stop cleanly: say the skill needs a documentation target and leave the repo
untouched. Never invent a docs repo, never write docs to a path the user didn't
agree to.

Then write `.agents/commit-documentor.json` from
[templates/config-template.json](templates/config-template.json), keeping only the
block for the chosen mode (`doc_repo` or `local_docs`) and dropping every
`_comment_*` key. Show it to the user and offer to commit it to the project repo.

Requires `jq`. `gh` is only needed for the PR step in `repo` mode.

## Prerequisite: the doc index

The index lives in the project repo at the config's `doc_index` path (default
`.agents/commit-documentor/doc-index.md`) and is **committed** — it is the local,
reviewable map of code area → doc page, and it is what keeps doc querying cheap
and in sync.

If the index is missing, or its recorded doc SHA is behind the current one, run the
scan before anything else:

```bash
scripts/doc-repo.sh sync     # repo mode: clone or fast-forward. local mode: no-op
scripts/doc-repo.sh list     # every doc file under docs_root
```

Then, for each significant top-level code area in the project (directories under
the source root, the CLI, the API surface, config), search the docs for it:

```bash
scripts/doc-repo.sh search "<module name>" "<command name>" "<env var>"
```

Fill in [templates/doc-index-template.md](templates/doc-index-template.md) from the
results, including the two negative sections — undocumented code areas, and doc
pages with no code owner. Both are load-bearing later: the first tells you when to
propose a *new* page, the second tells you what to leave alone. Record the docs'
current SHA in the header so drift is detectable next run.

In local mode on a project with no `docs/` tree yet, the scan is legitimately
empty: every code area lands under "Undocumented areas", and the first real run
will propose new pages rather than edits. Say that plainly rather than reporting
an empty index as a failure.

Show the index to the user before committing it — a wrong mapping silently
mis-targets every future run.

## Rules

Rules live under `rules` in the config, gathered during first-run setup:
`exclude_commit_types`, `exclude_paths`, `always_document_paths`, and free-form
`instructions`. See [references/rules.md](references/rules.md) for precedence.

Any instruction the user gives when invoking the skill applies to this run only and
**overrides** the config; if it looks durable ("stop documenting CLI flag changes"),
offer to add it to the config.

## Workflow

Track each step as a task.

### 0. Check preconditions — before reading any commits

Do not start reviewing commits until both of these pass:

```bash
scripts/doc-repo.sh config >/dev/null   # exit 3 → run "First run: setup" above
```

- **Config missing (exit 3)?** Run [First run: setup](#first-run-setup) and finish
  it before continuing.
- **Doc index missing or stale?** Run the [doc index](#prerequisite-the-doc-index)
  scan and get it approved before continuing.

Hitting either of these halfway through a run wastes the review and forces the user
to answer setup questions mid-flow. Check first.

### 1. Establish the commit range

Default: everything on the branch not yet on origin.

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1 \
  && range="@{u}..HEAD" || range="HEAD~1..HEAD"
git log --format='%h %s' $range
git diff --stat $range
```

If the user passed a range or a SHA as an argument, use that instead. If the range
is empty (nothing unpushed), say so and stop — there is nothing to document.

### 2. Review the commits

For each commit, read the actual diff, not just the subject:

```bash
git show --stat <sha>
git show <sha> -- <paths of interest>
```

Fold in whatever extra instruction the user gave when invoking the skill. Judge
each commit on what the diff *does*, not what its message claims — a commit typed
`chore:` that changes a default config value is a behavior change and the message
is wrong.

### 3. Decide applicability

Apply the rules from [references/rules.md](references/rules.md) to each commit and
classify it: **needs docs**, **excluded by rule** (name the rule), or **no
user-visible change**. Then, for the commits that need docs, use the doc index to
find the target pages, and confirm against the live doc repo:

```bash
scripts/doc-repo.sh sync
scripts/doc-repo.sh search "<symbol>" "<flag>" "<endpoint>"
```

Read the target pages in full before editing them. If a needed page does not exist
and the area is listed under "Undocumented areas", propose a new page — but say
plainly that it is new, and where it would sit.

If nothing needs docs, report the classification per commit and stop. That is a
successful run, not a failure.

### 4. Draft the updates

Edit the doc files directly — the doc repo clone in `repo` mode, `docs_root` in
this repo in `local` mode; `scripts/doc-repo.sh path` and `... root` resolve both.
Match the surrounding page's structure, voice, and heading depth — read neighbors
before writing. In local mode with no docs yet, you are creating the first pages:
establish a simple, obvious structure (a page per user-facing surface) rather than
scaffolding an elaborate tree the project can't sustain. Keep edits minimal and
scoped to what the commits actually changed; do not opportunistically rewrite
unrelated prose.

Present for approval:

```bash
scripts/doc-repo.sh diff
```

This shows tracked edits *and* the full content of any new pages, scoped to
`docs_root` so the user's unrelated working-tree changes never appear. Show the
user the full diff, plus a short per-file rationale tying each edit to a specific
commit, and the list of commits you excluded and why.

### 5a. Approved → publish

Write the commit message to a file first (subject line + body referencing the
source commit SHAs and, in `repo` mode, the project repo). Then:

```bash
scripts/doc-repo.sh publish "<branch_prefix>/<short-slug>" <msg-file> <body-file>
```

- **`repo` mode**, default `push_mode: pr`: branches, pushes, and opens a PR
  against `doc_repo.branch` — use [templates/doc-pr-body.md](templates/doc-pr-body.md)
  for the body. If `push_mode` is `direct`, commit and push to `doc_repo.branch`
  instead — still only after approval. Report the PR URL (or pushed branch).
- **`local` mode**: commits on the **current branch**, staging only paths under
  `docs_root`, and does **not** push. The `<branch>` argument is ignored, and no PR
  body is used. Tell the user the docs are committed locally and will go out with
  their next push — never push the project repo yourself.

Then update the doc index's recorded SHA and any changed mappings, and mention that
the index file now has an uncommitted change.

### 5b. Declined → regenerate

Ask what was wrong, take the added instruction, and redo step 4 against the same
commit set — discard the previous draft first so drafts don't stack:

```bash
scripts/doc-repo.sh revert
```

This reverts only paths under `docs_root`, so in local mode the user's own
in-progress work is untouched. Regenerate as many times as the user wants. If the
correction is durable, offer to write it into the config's `rules.instructions`. If
the user declines entirely, revert and stop — never publish a partial draft.

## Hard rules

- Never publish docs without approval of the specific diff in this session.
- Never guess a documentation location. If none is configured, run first-run setup;
  if the user has no docs repo, offer local mode rather than inventing a target.
- In local mode, never push the project repo and never stage anything outside
  `docs_root` — the user's other work is not yours to commit.
- Never edit paths the config or index marks as hand-maintained / no code owner.
- Never invent doc content that the commits do not support — if the code's behavior
  is ambiguous, ask rather than documenting a guess.
- Never rewrite the project repo's own commits; this skill only writes docs and the
  index.
- Leave the working tree clean on exit: either published, or reverted.
