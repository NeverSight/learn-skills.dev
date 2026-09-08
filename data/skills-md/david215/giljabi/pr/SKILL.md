---
name: pr
description: Push the current branch and open or update a real pull request — computing scope from the merge base, filling the repo's own PR template, and posting long-running content as a comment rather than the description. Works on Azure DevOps and GitHub. Use whenever a PR is wanted for the current branch.
---

# PR

Derive a PR body from the branch's **committed** work not yet on the integration branch, fill the
repo's own PR template with it, push, and actually create or update the pull request — rather than
printing text to copy-paste.

## Read the repo's conventions first

`docs/agents/vcs.md` supplies **Host**, **Integration branch**, **Language**, **PR title**,
**Reviewers**, draft state, and **linking**. Read it before anything else, then read the matching
host module for the commands:

- [hosts/azure-devops.md](./hosts/azure-devops.md) — `az repos`, and a hard description limit
- [hosts/github.md](./hosts/github.md) — `gh pr`

No `vcs.md`? Infer the host from `git remote get-url origin` and the integration branch from
`git symbolic-ref refs/remotes/origin/HEAD`, say so in one line, and open the PR without reviewers
rather than guessing at people.

**This skill runs no tests and computes no test scope.** What the body may claim about tests is
decided by evidence alone — a CI run visible on the branch, or a run the user reported. It never
claims a run it cannot point at.

## Step 1 — Compute the scope

Every commit reachable from `HEAD` that is not on the integration branch.

```bash
git branch --show-current
git fetch origin <integration-branch> --prune
git merge-base HEAD origin/<integration-branch>
git log --reverse --no-merges --format='%H%x09%s' <merge_base>..HEAD
git diff --stat <merge_base>..HEAD
git diff <merge_base>..HEAD -- <relevant paths>
```

Read **both** the commit messages and the actual diff. Commit messages describe intent; only the
diff shows what shipped.

**Then grep the added lines for new error paths.** This is a required command, not something to
keep in mind while reading:

```bash
git diff <merge_base>..HEAD | grep -nE '^\+.*(throw |raise |panic!|return .*Err\()'
```

Match the pattern to the repo's language — `throw new …Exception` in TypeScript and Java, `raise`
in Python, `return …, err` or `panic!` in Go and Rust. A large diff makes it easy to read straight
past a new `throw` in a private helper with no route name attached, and that buried throw is
routinely the most caller-visible change in the branch. For each hit: confirm it is new rather than
moved (check for the paired `-` removal), trace it to the routes that reach it, and note whether it
carries a payload or message a caller must now branch on.

If the range is empty, stop and say so. Do not open an empty PR.

## Step 2 — Compute the title

Follow `vcs.md`'s **PR title** convention, which is frequently *not* the commit convention — many
repos use Conventional Commit prefixes on commits and a plain descriptive phrase on PR titles.
Where `vcs.md` is silent, match the style of recent merged PRs rather than the commit log.

The title is passed as its own argument, never embedded in the description.

## Step 3 — Find the repo's PR template

The body structure belongs to the repo, not to this skill. Look for a template the host already
recognises:

```bash
find . -maxdepth 3 -iname 'pull_request_template*' -not -path './.git/*' -not -path '*/node_modules/*'
```

Azure DevOps reads `pull_request_template.md` from the repo root, `.azuredevops/`, or `docs/`.
GitHub reads it from `.github/`, the root, or `docs/`, in any casing. Either host may hold a
directory of named templates; pick the one matching the change, or the default, and say which. The
template lives where its host reads it — `docs/agents/` is a place no host scans, so `vcs.md` may
point at the template but never house it.

**Found one? It is the contract. Fill it; do not redesign it.**

- Preserve every label, its order, the checkbox syntax, and the blockquote markers exactly. A team
  reads these by shape, and a renamed label is a silent divergence from the template the repo ships.
- A **hint** is the placeholder text itself — `(as detailed as possible)`, `> (가능한 자세히)` — and it
  is not structure: under a heading you fill, the answer replaces the hint, keeping the marker it sat
  in. A hint the diff cannot answer (did local tests run?) stays intact, its box unchecked — you did
  not run them.
- Check a box only on evidence in the diff. Leave the rest unchecked with their placeholders intact.
  An unchecked box is information; a box checked on assumption is a false claim to a reviewer.

**No template? Use [default-template.md](./default-template.md)** and mention in one line that the
repo has none, so the user can add one if they want the structure fixed.

## Step 4 — Write the body

The template says *what sections exist*. These rules say *how to write inside them*, and apply to
whichever section asks what changed.

### Change-groups, and the label → detail shape

One top-level bullet per **change-group** — something a reviewer would consider as one decision: a
flow, a module boundary, a schema change, a background job. If two candidates describe the same flow
or would be reviewed together, merge them.

- **Label** (top level, bold, *no content of its own*) — names the group. `**Blocked access to
  deleted organizations**`, not a sentence about what changed.
- **Detail** (second level, plain) — the actual facts: what changed, where, why it matters. All real
  content lives here.
- **Sub-detail** (third level) — an escape hatch for one sub-point under a single detail. Not a
  place to enumerate files; those are detail bullets of their own.

Every label carries **at least one** child, however small the group. The uniformity is the point:
a reader skims the bold labels alone and gets the shape of the whole PR.

**Grain size is the whole game.** One label per genuine reviewable change-group — never one per file
touched or per implementation step. A body that feels too long is almost always mis-grained rather
than over-full: merge a label carrying one tiny fact into a coarser neighbour. Do not pad toward a
count either; a one-concern branch gets one label.

Order labels by blast radius: caller-visible behaviour first, then data integrity and security, then
internal refactors, renames, and docs.

### API changes get a reserved group, first position

For **every route the diff touches**, check all three contract dimensions. Do not stop at the first
that applies:

- **Request** — new, changed, or removed fields, params, or validation rules.
- **Response** — new, changed, or removed fields, or a status-code change on the success path.
- **Errors** — new or changed thrown errors, a new payload, or a message a caller must branch on
  differently. This is the dimension that hides inside a large diff, which is why Step 1 greps for
  it mechanically. **An error path alone qualifies a route**, with no request or response change.

A route also qualifies when its **side effects or authorization outcome** changed enough to surprise
a caller relying on the old behaviour — even with all three dimensions literally untouched. This is
very often the most important change in the PR, and a narrow "did the schema change" reading is
exactly what drops it.

When any route qualifies, this group comes **first** and is labelled in the repo's prose language,
matching the surrounding text — `API 변경 사항` in a Korean body, not `API changes`. The English form
in this file and in `default-template.md` is the name of the concept, not a string to copy: a body
whose every other label is Korean and whose most important label is English reads as a template that
was filled in without being read. Each child is a route written as `` `METHOD /path` `` followed by
exactly one tag:

| Tag | Meaning |
| --- | --- |
| `(BREAKING)` | the contract shape or status code itself moved — a new required field or param, a removed or renamed response field, a narrowed type, a changed success status |
| `(new)` | a brand-new route; no prior callers to break |
| `(changed)` | everything else that qualifies — additive fields, a new error or validation path, a side-effect or authorization change |
| `(global)` | a cross-cutting change not scoped to one route, e.g. `` `error response format` (global) `` |

A new blocking error path is `(changed)`, **never** `(BREAKING)`, even when it turns a
previously-succeeding caller into a failure. `(BREAKING)` is reserved for the contract shape moving,
not for "this can now fail."

A route qualifying under more than one category takes its single most severe tag, by
`(BREAKING)` > `(new)` > `(changed)` > `(global)` — one bullet per route, never split. Order routes
by that same category sequence, with impact as the secondary sort. A category with no qualifying
route contributes nothing; no empty markers.

Under each route sit the **caller-facing facts**, one per dimension that actually changed, as
sub-bullets rather than inline text after a colon. Implementation detail already stated elsewhere in
the body does not belong here.

If no route has caller-visible change, omit the group. Do not manufacture one.

#### Which section it goes in, when the repo's template has several

It goes in the section that asks **what changed** — first position inside it. Not the section that
asks what effects are expected, even though a contract change is arguably the most effect-laden thing
in the branch.

The effects section then has a real job rather than a redundant one: the *consequences* of those
route changes. `PATCH /organizations` accepting a new field is a change; every pre-existing
organization silently switching email language because of it is an effect.

**Only when a template has no what-changed section at all** does the group move under effects. Say so
in one line when that happens, since it departs from the shape above.

### Prose

- Base every claim on the committed diff, not on commit titles.
- Write in `vcs.md`'s **Language**. Keep it short and PR-ready; in Korean, avoid the polite report
  register (`~습니다`).
- Name the specific change. `improved the logic`, `structural cleanup`, and `handling refined` say
  nothing on their own.
- Claim no effect the diff does not show, and no test run the user did not report.
- State an assumption in one line where the branch reads more than one way.
- **Name nothing ephemeral.** Describe what the branch does, not which ticket asked for it or where
  the spec lives — a description outlives the branch and those do not. If the repo's `vcs.md` says to
  link the spec path because the tracker has no linkable ID, that instruction predates this rule and
  is wrong: a
  path into a deleted directory links to nothing.

### Test items are filled on evidence, never on assumption

A template's test items are part of the contract — they cannot be deleted, and leaving them blank
reads as unconsidered. What licenses each one is evidence you can point at:

- **Which spec files changed** — the diff proves this; fill it from the diff.
- **Whether tests ran and passed** — known only from a CI run visible on the branch or a run the
  user reported. Cite the source in the item (`CI 통과 — <check name>`, in the repo's prose
  language). Neither exists → leave the item unchecked with its placeholder intact and say so in one
  line; an unchecked box is information, a box checked on assumption is a false claim to a reviewer.

Never restate a full suite listing in the body when CI already carries it — the body copy is the one
nobody updates on the next push.

### User overrides

Natural-language instructions in the same message constrain **what to describe**, never git history.
Exclusions ("leave out the lockfile"), focus ("just the auth work"), language, audience. There is no
`@` syntax; read the phrasing literally.

Compute the full range for context regardless, then base the body on the remaining diff
(`git diff <merge_base>..HEAD -- . ':!path'`). **If excluded work is still on the branch, say so in
one line** inside the body — a reviewer who reads the description as the whole branch is being
misled otherwise.

## Step 5 — Check the length, then push

Host modules carry the limits; Azure DevOps has a hard description cap that will silently truncate.
Measure with `LC_ALL=en_US.UTF-8 wc -m`, never `wc -c` — multi-byte prose runs three bytes per
character and a byte count will make you cut a body that fits. **The locale prefix is the measurement:**
under `LC_ALL=C` or `POSIX` — the default in Docker, cron, and most CI — `wc -m` counts bytes too, so
the bare command fails in the same direction as `wc -c` while looking like the fix.

Over budget means a label is mis-grained. Go back to Step 4 and merge, rather than abbreviating
prose into shorthand.

Then grep the body for hints that survived under a heading you filled:

```bash
grep -nE '^\s*>?\s*\(.*\)\s*$' <body-file>
```

Every hit is either under an unanswerable item, left intact on purpose, or a fill failure — fix the
second kind before pushing.

```bash
git push -u origin <branch>    # or plain `git push` when upstream is set
```

The branch must exist on the remote with the current commits, or the host rejects the PR. No
confirmation gate: the PR opens as a draft, so a human reviews before anyone is notified in earnest.

## Step 6 — Create or update

Check for an **active** PR on this source → target pair first and update it in place rather than
opening a duplicate. A completed or abandoned PR from earlier history does not count as existing.
Commands are in the host module.

Open as a draft when `vcs.md` says draft. Never pass auto-complete, policy bypass, squash, or
delete-source-branch flags — those are merge-time decisions for the human who publishes the PR.

## Step 7 — Long-running content goes in a comment

When the user asks for point-in-time content to ride along — a benchmark table, a migration log, a
survey — post it as a **comment**, never in the body: a single further push invalidates it, and the
body is the copy nobody updates. Update the existing comment rather than posting another, unless
reviewers should be re-notified — comments notify, description edits do not. Write every path in
full, one per line — full paths are greppable and clickable, and comments have no practical length
limit. **Where the host has a resolved state for comments, post in it**: the content asks nothing of
a reviewer, and an open thread misfiles it in the unresolved count people clear before approving.
This is host-specific — Azure DevOps threads carry a status, plain GitHub PR comments do not.
Commands are in the host module. Nothing to post → skip this step.

## Step 8 — Report back

Print the PR URL, say plainly whether it was created or updated, and say it is a draft — the user
still publishes it and confirms reviewers before anyone is notified.

---

See [examples.md](./examples.md) for a filled body showing the label → detail shape and a populated
`API changes` group.
