---
name: edit-lore
description: >-
  Curate an existing Lore Work at refs/lore/<work-id> by recording durable
  decisions, plan updates, and discoveries in a new lore commit. Use when the
  user asks to update lore, edit lore, record a decision, curate lore, add to
  lore, or update plan in lore.
---

# edit-lore

Curate an existing Lore Work: export the lore tree to a temp directory,
apply curated edits, commit a new lore revision, and update
`refs/lore/<work-id>`. Lore lives in Git objects only — nothing is written
to the repository working tree.

Protocol reference: [references/protocol.md](references/protocol.md) and Lore Work
`refs/lore/git-lore` (`git show refs/lore/git-lore:spec.md`) for full
specification. This skill's Lore Work: `refs/lore/edit-lore`.

## When to use

- A durable conclusion emerged: decision made, plan changed, discovery worth
  preserving, rejected approach identified, open question surfaced
- User asks to "update lore", "edit lore", "record decision", or "curate lore"
- read-lore surfaced stale or missing context that should be recorded

Do **not** use when:

- No Lore Work exists yet → create-lore
- User wants to **read** Lore without changing it → read-lore
- Work may exist only on remote → sync-lore first, then edit-lore
- Content fails the curation gate (see below) → explain why, do not write

## Curation gate (mandatory)

**Apply this gate before every edit.** This is the primary control for Lore
quality. If content fails, do not edit Lore — tell the user why.

1. **Durable?** Apply heuristic from [references/protocol.md](references/protocol.md):

   > Would a future developer or agent otherwise have to rediscover this?

2. **Category?** Lore should preserve:
   - decisions, constraints, discoveries, rejected approaches
   - current plans, unresolved questions, handoff information

3. **Exclude?** Do not record:
   - conversation transcripts or chat summaries
   - routine activity ("fixed typo", "ran tests", "implemented step 3")
   - detail that belongs in source code, commit messages, or PR descriptions
   - content already present in Lore (duplicate)

## Edit modes

Modes are guidance, not separate code paths. Combine related changes in one
lore commit.

| Mode | Trigger | Behaviour |
|------|---------|-----------|
| Curate | Default | Apply curation gate, edit appropriate document(s) |
| Update plan | Plan or scope changed | Edit `plan.md` |
| Record decision | Choice settled | Add to or create `decisions.md` |
| Record question | Uncertainty identified | Add to or create `questions.md` |
| Add investigation | Research worth preserving | Add to or create `investigation.md` |
| Curate handoff | Durable handoff needed | Create or update `handoff.md` |
| Create artefact | New document warranted | Add file to lore tree |

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Resolve work-id
- [ ] Step 2: Verify Work exists
- [ ] Step 3: Curation gate — should this be recorded?
- [ ] Step 4: Read current lore state
- [ ] Step 5: Export to temp dir and apply edits
- [ ] Step 6: Commit lore revision
- [ ] Step 7: Verify, show diff, and report
- [ ] Step 8: Suggest read-lore or sync-lore if appropriate
```

### Step 1: Resolve work-id

Resolve in order:

1. **Explicit argument** — user provides `work-id` (e.g. "update lore for git-lore")
2. **Branch config**:

```bash
BRANCH=$(git branch --show-current)
git config --get "branch.${BRANCH}.lore"
```

3. **Disambiguation** — list Works and ask:

```bash
git for-each-ref refs/lore --format='%(refname:short)'
```

If branch config points to a Work that does not exist locally, report the
stale config and fall through to disambiguation.

If zero Works exist, suggest create-lore.

### Step 2: Verify Work exists

```bash
WORK_ID=<work-id>
git rev-parse "refs/lore/${WORK_ID}"
```

If this fails:

- Remote may have the Work → suggest sync-lore
- Work may not exist → suggest create-lore

### Step 3: Curation gate

Apply the curation gate (see above). If content does not pass, stop and
explain to the user what would be worth recording instead.

### Step 4: Read current lore state

**Never overwrite a document without reading it first.**

- Complex edits: prefer read-lore for full context
- Minimum for targeted edits:

```bash
git ls-tree -r --name-only "refs/lore/${WORK_ID}"
git show "refs/lore/${WORK_ID}:plan.md"
git show "refs/lore/${WORK_ID}:decisions.md"   # if editing decisions
```

Read every file you intend to modify.

### Step 5: Export to temp dir and apply edits

#### Document emergence rules

Do not preemptively create documents. Create a new artefact only when the
work produces content that fits:

| File | Create when |
|------|-------------|
| `decisions.md` | First settled choice needs recording |
| `questions.md` | First unresolved question needs recording |
| `investigation.md` | Research or alternatives worth preserving |
| `spec.md` | Technical specification emerges for the work |
| `architecture.md` | System design decisions need recording |
| `handoff.md` | Durable handoff context needed across sessions |

`plan.md` always exists (created by create-lore).

#### Entry formats

**decisions.md:**

```markdown
## Short title

**Decision:** [What was decided]

[Why — durable reasoning, not conversation recap]
```

**questions.md:**

```markdown
## Short title

[Question and any context needed to understand it]
```

#### Export and edit

```bash
WORK_ID=<work-id>
REF="refs/lore/${WORK_ID}"
COMMIT=$(git rev-parse "$REF")
DIR=$(mktemp -d)
GIT_DIR=$(git rev-parse --absolute-git-dir)

git archive "$COMMIT" | tar -x -C "$DIR"
```

Edit files in `$DIR`. Apply curated changes only — do not copy conversation
transcripts into Lore.

File deletion is supported but rare. Prefer recording a superseding decision
over removing old content.

### Step 6: Commit lore revision

Use an **isolated index** (`GIT_INDEX_FILE`). Without it, `git add -A` in
the temp dir pollutes the main repository index.

```bash
INDEX=$(mktemp)
export GIT_INDEX_FILE="$INDEX"
git --git-dir="$GIT_DIR" read-tree --empty
git --git-dir="$GIT_DIR" --work-tree="$DIR" add -A .
TREE=$(git --git-dir="$GIT_DIR" write-tree)
unset GIT_INDEX_FILE

NEW=$(git commit-tree "$TREE" -p "$COMMIT" -m "lore: <what changed>")
git update-ref "$REF" "$NEW"

rm -rf "$DIR" "$INDEX"
```

Commit message format: `lore: <concise description of what was curated>`

Examples:

- `lore: record decision on isolated index for edits`
- `lore: update plan status — edit-lore done`
- `lore: add open question on lore merge conflicts`

**One lore commit per meaningful curation event.** Batch related changes;
do not commit per-line edits.

Unlike create-lore (orphan), edit-lore commits parent off the current lore
HEAD. Lore commits are separate from source-code commits on the branch.

### Step 7: Verify, show diff, and report

```bash
git log --oneline -3 "refs/lore/${WORK_ID}"
git diff "${COMMIT}" "${NEW}"
git status
git ls-tree -r --name-only "refs/lore/${WORK_ID}"
```

Confirm:

- Lore ref advanced to new commit
- `git status` is clean — no lore files in the working tree
- Diff reflects intended curation only
- Main index not polluted (nothing staged at repo root)

Report to the user:

- Work id and ref
- New commit hash and message
- Summary of what was curated
- `git diff` highlights

### Step 8: Suggest read-lore or sync-lore if appropriate

| Situation | Suggest |
|-----------|---------|
| User wants to review changes | read-lore |
| Lore should be shared with remote | sync-lore |
| No Work exists | create-lore |

edit-lore does not call other skills — it only suggests them.

## Examples

### Record a decision

User settles on using isolated `GIT_INDEX_FILE` for lore edits.

1. Curation gate passes — durable protocol decision
2. Read `refs/lore/edit-lore:decisions.md` (or create file if absent)
3. Export, append decision entry, commit:

```bash
git commit-tree ... -m "lore: record isolated GIT_INDEX_FILE decision"
```

### Update plan and record decision together

read-lore done; update plan status and record a decision in one commit:

```bash
git commit-tree ... -m "lore: mark read-lore done, record handoff format decision"
```

### Curation gate rejects content

User: "add to lore that we fixed a typo in SKILL.md"

Stop. Routine implementation activity does not pass the curation gate.
Explain and offer to record a decision if the typo revealed something
durable (e.g. a naming convention mistake).

### Stale branch config

```bash
$ git config --get branch.feature-x.lore
old-work
$ git rev-parse refs/lore/old-work
fatal: Needed a single revision...
```

Report stale config. List available Works and ask which to edit.

## Verification

After editing, confirm commands work:

```bash
git rev-parse refs/lore/<work-id>
git log --oneline -3 refs/lore/<work-id>
git diff refs/lore/<work-id>~1 refs/lore/<work-id>
git status
```

## Non-goals

- No working-tree lore files
- No automatic/background lore updates without explicit intent
- No lore ref deletion or archival
- No lore history rewriting (no amend/rebase of lore commits)
- No merge of diverged lore refs (document friction; sync-lore handles transport)
- No mixing lore commits into source-branch history
- No executable or helper scripts
