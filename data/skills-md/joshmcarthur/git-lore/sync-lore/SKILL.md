---
name: sync-lore
description: >-
  Transport Lore Works between local repository and Git remotes via fetch and
  push on refs/lore/*. Use when the user asks to sync lore, push lore, fetch
  lore, pull lore, share lore, or check lore status against a remote.
---

# sync-lore

Transport Lore Works between the local repository and Git remotes using
ordinary `git fetch` and `git push` on `refs/lore/*`. sync-lore configures
fetch refspecs (not set by default), runs transport operations, compares
local vs remote refs, and reports divergence.

Nothing is written to the working tree — lore refs and git config only.

Protocol reference: [references/protocol.md](references/protocol.md) and Lore Work
`refs/lore/git-lore` (`git show refs/lore/git-lore:spec.md`) for full
specification. This skill's Lore Work: `refs/lore/sync-lore`.

## When to use

- Sharing Lore Works with teammates via the same Git remote as source code
- User asks to "sync lore", "push lore", "fetch lore", "pull lore", or
  "share lore"
- read-lore or edit-lore suggest sync-lore (Work not found locally, lore
  should be shared, remote may have the Work)
- Post-clone setup to obtain lore refs from remote
- Checking whether local and remote lore refs match

Do **not** use when:

- No Git remote exists → lore is local-only; explain and stop
- User wants to **read** Lore → read-lore (after fetch if needed)
- User wants to **change** Lore → edit-lore
- No Lore Work exists yet → create-lore
- Diverged histories need reconciliation → detect with sync-lore, reconcile
  with edit-lore

## Sync modes

Determine mode from the user's request:

| Mode | Trigger | Behaviour |
|------|---------|-----------|
| sync | Default, "sync lore" | Configure refspec if needed, fetch, then push |
| fetch | "fetch lore", "pull lore" | Fetch lore refs only |
| push | "push lore" | Push lore refs only |
| status | "lore status", "lore remote" | Compare local vs remote refs |

When the user specifies a `work-id`, scope fetch, push, and status to that
Work only. Default remote is `origin` unless the user names another.

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Resolve remote and mode
- [ ] Step 2: Guard — remote must exist
- [ ] Step 3: Ensure fetch refspec is configured
- [ ] Step 4: Execute mode (fetch / push / sync / status)
- [ ] Step 5: Report transport results
- [ ] Step 6: Handle divergence if push rejected or status shows diverged
- [ ] Step 7: Verify and suggest next skill if appropriate
```

### Step 1: Resolve remote and mode

- **Remote:** default `origin`; use user-specified remote if given
- **Mode:** infer from request (see table above); default is **sync**
- **Work id:** optional; scopes operations to `refs/lore/<work-id>` only

List local lore refs when helpful:

```bash
git for-each-ref refs/lore --format='%(refname:short) %(objectname:short)'
```

### Step 2: Guard — remote must exist

```bash
REMOTE=origin
git remote get-url "$REMOTE" 2>/dev/null
```

If this fails:

- No remotes configured → lore is **local-only**. Explain that lore refs
  exist only in this clone until a remote is added and sync-lore is run.
- Stop. Do not attempt fetch or push.

### Step 3: Ensure fetch refspec is configured

Lore refs are **not** fetched by default. Check:

```bash
REMOTE=origin
git config --get-all "remote.${REMOTE}.fetch" | grep -F 'refs/lore/'
```

If missing, configure once per remote (local `.git/config`, not committed):

```bash
git config --add "remote.${REMOTE}.fetch" 'refs/lore/*:refs/lore/*'
```

Properties:

- **No `+` prefix** — avoids force-overwriting local lore refs with unpushed
  commits on fetch
- Repeat for each remote that should transport lore
- After configuration, `git fetch <remote>` includes lore refs

Report whether refspec was already configured or newly added.

### Step 4: Execute mode

#### Fetch mode

All lore refs:

```bash
REMOTE=origin
git fetch "$REMOTE" 'refs/lore/*:refs/lore/*'
```

Single Work:

```bash
WORK_ID=<work-id>
git fetch "$REMOTE" "refs/lore/${WORK_ID}:refs/lore/${WORK_ID}"
```

Fetch without `+` will:

- Fast-forward local ref if remote is ahead
- Leave local ref unchanged if local is ahead
- Not overwrite on divergence

#### Push mode

All lore refs:

```bash
REMOTE=origin
git push "$REMOTE" 'refs/lore/*'
```

Single Work:

```bash
WORK_ID=<work-id>
git push "$REMOTE" "refs/lore/${WORK_ID}"
```

If push is rejected (non-fast-forward), proceed to Step 6.

#### Sync mode

Default — fetch then push:

```bash
REMOTE=origin
git fetch "$REMOTE" 'refs/lore/*:refs/lore/*'
git push "$REMOTE" 'refs/lore/*'
```

Report each step separately. If push fails after fetch, proceed to Step 6.

#### Status mode

Compare local and remote lore refs:

```bash
REMOTE=origin

# Local
git for-each-ref refs/lore --format='%(refname:short) %(objectname:short)'

# Remote
git ls-remote "$REMOTE" 'refs/lore/*'
```

For each work-id on either side, classify:

| State | How to detect |
|-------|---------------|
| synced | Same commit SHA |
| local-only | Local ref exists; absent from `git ls-remote` |
| remote-only | On remote; `git rev-parse refs/lore/<id>` fails locally |
| ahead | Local is strict descendant of remote (`merge-base` == remote SHA) |
| behind | Remote is strict descendant of local (`merge-base` == local SHA) |
| diverged | Both exist, different SHAs, neither is ancestor of the other |

Classification helpers:

```bash
WORK_ID=<work-id>
LOCAL=$(git rev-parse "refs/lore/${WORK_ID}" 2>/dev/null)
REMOTE=$(git ls-remote "$REMOTE" "refs/lore/${WORK_ID}" | awk '{print $1}')
```

Skip side refs matching `*-remote` in default listings unless inspecting
divergence.

### Step 5: Report transport results

Report clearly:

- Remote name and mode executed
- Refspec status (configured or newly added)
- Per-ref outcome: fetched, pushed, up to date, skipped, or failed
- For status mode: classification table per work-id

Post-clone note when relevant:

```bash
git clone <url> <dir>
cd <dir>
git config --add remote.origin.fetch 'refs/lore/*:refs/lore/*'
git fetch origin
git for-each-ref refs/lore
```

`git pull` updates the current branch only. Lore requires explicit
`git fetch` (sync-lore fetch mode) even after refspec is configured.

### Step 6: Handle divergence

sync-lore does **not** automatically merge lore histories. Lore documents
are curated Markdown — automatic merge produces conflict markers.

When push is rejected or status shows **diverged**:

1. Fetch remote to a side ref without overwriting local:

```bash
WORK_ID=<work-id>
REMOTE=origin
git fetch "$REMOTE" "refs/lore/${WORK_ID}:refs/lore/${WORK_ID}-remote"
```

2. Show both histories:

```bash
git log --oneline "refs/lore/${WORK_ID}"
git log --oneline "refs/lore/${WORK_ID}-remote"
```

3. Suggest manual reconciliation:
   - read-lore for local version
   - `git show "refs/lore/${WORK_ID}-remote:plan.md"` (and other files) for remote
   - edit-lore to curate a reconciled version
   - sync-lore push after reconciliation

4. After reconciliation, clean up side ref:

```bash
git update-ref -d "refs/lore/${WORK_ID}-remote"
```

Do **not** force-push lore refs by default. If the user explicitly requests
force-push, warn about destroying remote lore history and require confirmation.

Record persistent friction via edit-lore on the relevant Lore Work if the
workflow is painful.

### Step 7: Verify and suggest next skill

```bash
git status
git for-each-ref refs/lore --format='%(refname:short) %(objectname:short)'
```

Confirm working tree is clean — sync-lore never checks out lore files.

| Situation | Suggest |
|-----------|---------|
| New lore fetched from remote | read-lore |
| Diverged histories need merge | edit-lore (after comparing side ref) |
| User wants to review local lore | read-lore |
| No lore refs exist anywhere | create-lore |
| Lore should be updated before push | edit-lore, then sync-lore push |

sync-lore does not call other skills — it only suggests them.

## Examples

### Default sync

User: "sync lore"

1. Verify `origin` exists
2. Add fetch refspec if missing
3. `git fetch origin 'refs/lore/*:refs/lore/*'`
4. `git push origin 'refs/lore/*'`
5. Report: 5 refs pushed, working tree clean

### Push single Work

User: "push lore for git-lore"

```bash
git push origin refs/lore/git-lore
```

### Fetch after clone

New clone with no lore refs locally:

```bash
git config --add remote.origin.fetch 'refs/lore/*:refs/lore/*'
git fetch origin 'refs/lore/*:refs/lore/*'
git for-each-ref refs/lore
```

Suggest read-lore to onboard.

### Status check

User: "lore status"

```bash
git for-each-ref refs/lore --format='%(refname:short) %(objectname:short)'
git ls-remote origin 'refs/lore/*'
```

Report per-ref classification (synced / ahead / behind / diverged / local-only
/ remote-only).

### Push rejected — divergence

```bash
$ git push origin refs/lore/git-lore
 ! [rejected] refs/lore/git-lore -> refs/lore/git-lore (non-fast-forward)
```

1. Fetch to side ref: `git fetch origin refs/lore/git-lore:refs/lore/git-lore-remote`
2. Show both logs
3. Suggest read-lore + inspect remote files + edit-lore to reconcile
4. Push again after reconciliation
5. Delete side ref when done

### No remote

```bash
$ git remote get-url origin
fatal: No such remote 'origin'
```

Explain lore is local-only. List local refs with `git for-each-ref refs/lore`.
Stop.

### Local-only Work

Status shows `create-lore` as local-only (not on remote). Push mode uploads
it; sync mode fetches then pushes it.

## Verification

After any sync operation:

```bash
git status
git for-each-ref refs/lore --format='%(refname:short) %(objectname:short)'
```

Working tree must remain clean.

## Non-goals

- No force-push of lore refs (default)
- No automatic lore history merge
- No working-tree checkout of lore files
- No lore ref deletion or archival
- No GitHub-specific ref handling
- No transport of source branches (ordinary git push/pull handles those)
- No executable or helper scripts
