---
name: create-lore
description: >-
  Initialise a new Lore Work at refs/lore/<work-id> with an independent Git
  history and initial plan.md. Use when starting new work, when the user asks
  to create lore, start lore, initialise lore, or begin a new lore work.
---

# create-lore

Create a new Lore Work: an independent, versioned context store at
`refs/lore/<work-id>`. Lore lives in Git objects only — nothing is written
to the repository working tree.

Protocol reference: [references/protocol.md](references/protocol.md) and Lore Work
`refs/lore/git-lore` (`git show refs/lore/git-lore:spec.md`) for full
specification.

## When to use

- Starting a new piece of work that needs durable context
- User asks to "create lore", "start lore", or "initialise a lore work"
- No `refs/lore/<work-id>` exists yet for this work

Do **not** use when a Lore Work already exists for this task — use read-lore
or edit-lore instead.

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Resolve work-id
- [ ] Step 2: Guard — ref must not exist
- [ ] Step 3: Draft plan.md content
- [ ] Step 4: Create lore commit via Git plumbing
- [ ] Step 5: Associate branch
- [ ] Step 6: Verify and report
```

### Step 1: Resolve work-id

Choose a lowercase slug: letters, digits, hyphens. Maps to `refs/lore/<work-id>`.

If the user provides a work-id, use it. Otherwise:

1. Derive a default from the current branch name:
   - Lowercase
   - Replace `/` and other non-alphanumeric characters with `-`
   - Collapse consecutive hyphens; strip leading/trailing hyphens
2. If the branch name is nested or long (e.g. `skills/create-lore` →
   `skills-create-lore`), prefer a shorter **semantic** id when scope is clear
   (e.g. `create-lore`). Confirm with the user if ambiguous.

### Step 2: Guard — ref must not exist

```bash
WORK_ID=<work-id>
git rev-parse "refs/lore/${WORK_ID}" 2>/dev/null
```

If this succeeds, the Work already exists. Stop and ask whether to read it
(read-lore) or choose a different work-id.

### Step 3: Draft plan.md content

Create **only** `plan.md`. Do not preemptively create decisions.md, spec.md,
or other artefacts — edit-lore adds those when durable conclusions emerge.

The plan should be concise and durable, not a conversation transcript.

Required sections:

```markdown
# Plan

## Objective

[What this work is trying to achieve — 1–3 sentences]

## Scope

[What is in scope and explicitly out of scope]

## Next steps

[Immediate actionable items]
```

Apply the curation heuristic from [references/protocol.md](references/protocol.md):

> Would a future developer or agent otherwise have to rediscover this?

### Step 4: Create lore commit via Git plumbing

Do not write lore files to the working tree. Build Git objects directly:

```bash
WORK_ID=<work-id>
PLAN_CONTENT='<content from step 3>'

PLAN_BLOB=$(printf '%s' "$PLAN_CONTENT" | git hash-object -w --stdin)
TREE=$(printf '100644 blob %s\tplan.md' "$PLAN_BLOB" | git mktree)
COMMIT=$(git commit-tree "$TREE" -m "lore: initialise Work ${WORK_ID}")
git update-ref "refs/lore/${WORK_ID}" "$COMMIT"
```

Notes:

- The initial commit is an **orphan** — no `-p` parent. This keeps lore
  history independent of source-branch rebases and squashes.
- `git mktree` requires a tab between the object descriptor and filename.
- To add multiple files (not the default), pipe multiple lines to `git mktree`.

### Step 5: Associate branch

Link the current branch to this Work for discovery by other skills:

```bash
BRANCH=$(git branch --show-current)
git config "branch.${BRANCH}.lore" "${WORK_ID}"
```

This is local metadata only — it is not committed.

### Step 6: Verify and report

```bash
git for-each-ref refs/lore --format='%(refname:short)'
git log --oneline refs/lore/${WORK_ID}
git ls-tree -r --name-only refs/lore/${WORK_ID}
git show "refs/lore/${WORK_ID}:plan.md"
git config --get "branch.$(git branch --show-current).lore"
git status
```

Confirm:

- Lore ref exists with a single commit
- Only `plan.md` is in the tree (unless user explicitly requested more)
- `git status` is clean — no lore files in the working tree
- Lore commit is unrelated to source history (`git merge-base refs/lore/${WORK_ID} HEAD` returns nothing)

Report to the user:

- Work id and ref (`refs/lore/<work-id>`)
- Commit hash and message
- Branch association set
- Manual inspect commands (`git show refs/lore/<work-id>:plan.md`)

Suggest read-lore if the user wants to review the result.

## Examples

### New feature branch

Branch: `feature/oauth2`
Work-id: `oauth2` (semantic, confirmed with user)
Creates: `refs/lore/oauth2` with plan.md describing the OAuth2 integration work.

### Nested branch name

Branch: `skills/create-lore`
Sanitized default: `skills-create-lore`
Preferred: `create-lore` when scope matches the skill name — confirm with user.

### Work already exists

```bash
$ git rev-parse refs/lore/git-lore
15a064273c79e1fee420cae7b959a83d995a3ffa
```

Stop. Ask whether to read the existing Work or choose a different id.

## Non-goals

- No working-tree files for lore content
- No manifest or metadata files
- No lore transport (sync-lore handles push/fetch)
- No executable or helper scripts
- No automatic creation of artefacts beyond plan.md
