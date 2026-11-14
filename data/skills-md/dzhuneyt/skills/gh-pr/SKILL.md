---
name: gh-pr
description: Open a GitHub pull request (draft or ready for review) from the current branch using the gh CLI. Use this whenever the user wants to open, create, raise, submit, or "ship" a PR / pull request, or says things like "open a PR", "PR this branch", "put this up for review", or invokes /gh-pr — even when they don't specify the base branch, title, or description. Handles pushing the branch, writing the title and body from the actual diff, respecting the repo's PR template, linking issues, and dropping to --draft for unfinished work.
---

# gh-pr

Open a pull request from the current branch with a title and body that reflect what actually changed, not just the last commit message. The goal is a PR a reviewer can understand without reading the diff first.

Use `gh` for everything. It handles auth, the API, and returns a URL at the end. Do not script raw API calls.

## The shape of the work

Three phases, in order. The hard rule that drives the ordering: **nothing gets pushed until the work is confirmed to be on the right branch.** Phase 2 is entirely local and reversible; the first irreversible-ish action (push) is the top of Phase 3.

```
  Phase 1  Can I run?         local gates + gh auth
                              any gate fails -> stop
     |
     v
  Phase 2  Right place?       base -> assess -> branch-fit -> settle tree
                              all local, nothing pushed yet
     |
     v
  Phase 3  Open the PR        push -> compose -> gh pr create -> url
```

---

# PHASE 1 · Can I run?

## Step 0: cheap local gates

All local — no network, no push — so they fail in milliseconds before any expensive work. Order matters: cheapest and most fundamental first.

**Hard exits** — nothing downstream can recover, so bail immediately with a clear message:

1. **Not a git repo.** `git rev-parse --is-inside-work-tree`. Fastest check; run it first.
2. **`gh` not installed.** `command -v gh`. The cheap, local half of the auth check — keep it separate from `gh auth status` (network, see Preflight). "Not installed" and "not logged in" need different messages.
3. **No `origin` remote.** `git remote get-url origin` (non-zero exit = no `origin`). This skill assumes a single remote named `origin` and pushes the branch there; with no `origin` there's nowhere to push and nothing for `gh` to target, so stop here. **Fork workflows are out of scope** — pushing to a fork while basing the PR against an `upstream` repo (`--head owner:branch`) is deliberately not handled. If the only remote is named something else (e.g. `upstream`), stop and ask rather than guessing.
4. **Remote isn't GitHub.** `git remote get-url origin`, check the host. GitLab/Bitbucket/anything else → `gh` can't help, stop here.
5. **Detached HEAD or unborn branch.** `git symbolic-ref -q HEAD` (empty = detached; also catches a fresh repo with no commits). No branch means nothing to PR.

**Confirm and stop** — possible but almost always a mistake, so pause rather than refuse:

6. **On the default branch.** A PR from `main` into `main` is almost always wrong. Cheap path: if `git symbolic-ref refs/remotes/origin/HEAD` resolves locally (it only exists when the clone set `origin/HEAD`, e.g. via `git remote set-head origin -a`), compare against it here. If it's missing, skip the check here — Preflight resolves the default branch authoritatively and re-checks.
7. **Mid-operation.** Check for `MERGE_HEAD`, `.git/rebase-merge`, `.git/rebase-apply`, `.git/CHERRY_PICK_HEAD`, `.git/REVERT_HEAD`. A rebase/merge/cherry-pick/revert in flight means the tree is half-applied — a PR now is garbage.
8. **Zero commits ahead of base.** A smoke test only — base isn't resolved yet (that's Phase 2). Compare against the locally-resolved default branch (the `origin/HEAD` target from Step 0's default-branch check; skip if that ref is missing) using `git rev-list --count origin/<default>..HEAD`. **Before treating zero as a bail, check `git status --porcelain`:** a dirty tree means the work exists but is uncommitted — don't exit; carry on to Phase 2 and let "Settle uncommitted changes" commit it. Only zero commits + clean tree is a true hard exit. Phase 2 authoritatively determines the base (including any user-specified base) and supersedes this check; a non-zero count here is not a guarantee against the real base, and `origin/<default>` may be locally stale.

Once Step 0 passes, `git branch --show-current` gives the head branch for everything below.

## Preflight (network)

Costs a round trip, so it runs only after Step 0 clears.

- `gh auth status` — confirm the CLI is authenticated. If not, point the user at `gh auth login`; do not log in for them.
- **Resolve the default branch once, here.** Everything downstream (the Step 0 default-branch check, the base in Phase 2) refers back to this single value. Fallback chain — first hit wins:
  1. `git symbolic-ref --short refs/remotes/origin/HEAD` → strip the `origin/` prefix (local, no round trip).
  2. `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name` (authoritative, one round trip).

  If Step 0's local check was skipped because `origin/HEAD` was missing, re-check now that the head branch isn't this default.

---

# PHASE 2 · Is the work in the right place?

Everything in this phase is local. Resolve all of it before pushing.

## Determine the base branch

Reuse the default branch already resolved in Preflight — don't resolve it again. Use that default unless the user named a different base. Stacked PRs (a feature branch targeting another feature branch) are real but rare — the user usually says so. When in doubt, ask rather than assume `main`.

## Assess local state

Gather the facts once; they feed both the branch-fit decision and the PR body.

First resolve the upstream once, because the default first-PR path has none — the branch has never been pushed, so `origin/<branch>` doesn't exist and any `origin/<branch>..HEAD` comparison errors out:

```bash
git rev-parse --abbrev-ref @{u} 2>/dev/null               # upstream, or empty
```

- **Upstream exists** → unpushed commits are `git log --oneline @{u}..HEAD`.
- **No upstream** (first PR) → there's nothing to compare against; treat *every* commit since base as unpushed and skip the `origin/<branch>` comparisons entirely.

```bash
git status --porcelain                                    # dirty tree?
git log --reverse --format='%s%n%b' origin/<base>..HEAD   # commits since base
git diff --stat origin/<base>...HEAD                      # files + scope
gh pr list --head <branch> --state open --json number,url,title  # open PR?
```

The **local-only delta** = unpushed commits + uncommitted changes. That's the work that isn't yet captured anywhere — and it's the thing the branch-fit check reasons about. On the first-PR path every commit since base is part of that delta.

## Branch-fit decision

The failure mode: the user finished feature A (maybe already PR'd), started feature B without switching branches, and is now about to push B's work onto A.

Do **not** anchor on "does the branch name match the diff." Generic/personal names (`dev`, `wip`, `dzh/misc`) match nothing and false-positive constantly, and branches legitimately grow scope. Anchor on whether the branch already has a PR and whether there's local-only work on top of it:

```
  open PR on branch?   local-only delta?   -> action
  -----------------------------------------------------------------
  no                   either                 open a fresh PR
  yes                  none                   nothing new -> stop
  yes                  some                   STOP and ask (below)
```

Only the last row stops a routine flow. In that case summarize the **delta only** (not the whole branch), e.g. "Branch `<branch>` already has open PR #123. You have 2 unpushed commits and 4 changed files since then — do these belong on this branch, or should they move to their own branch?"

Keep this gate high-precision. If it interrupts routine PRs with "are you sure you're on the right branch?", the user learns to mash through it and it stops being useful. Only the bottom-right cell stops the flow.

## If the work needs to move

The remedy forks on committed vs uncommitted, because the mechanics and risk differ sharply:

```
  move the work off this branch:

  uncommitted  ->  git switch -c <new> origin/<base>      safe, just do it
                   (then continue — PR opens from <new>)
  committed    ->  git switch -c <new> origin/<base>      you do this
                   cherry-pick the stray commits onto <new>
                   ...then reset old branch + force-push   user's call — STOP
```

The committed path stops short of touching the old branch on purpose: cleaning the stray commits off it rewrites history, which needs a force-push — and this skill never force-pushes automatically, least of all on a branch that already has an open PR. Do steps 1–2, then hand the rewrite to the user.

The critical detail in both paths: fork from `origin/<base>`, **not** the current tip. `git switch -c <new>` from where you're standing bases the new branch on top of the old one, and its PR would then drag in all of the old branch's commits.

## Settle uncommitted changes

Now that the work is on the right branch:

```bash
git status --porcelain
```

If the tree is dirty, **surface the files and stop.** Do not commit on the user's behalf — they may be mid-thought, and a silent commit buries decisions they wanted to make. Ask: commit, stash, or leave out. If they ask you to commit, write the message as a Conventional Commit (see Phase 3) — pick the type from what changed, not a blanket `chore`.

---

# PHASE 3 · Open the PR

## Push the branch

```bash
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

- No upstream → `git push -u origin <branch>`.
- Upstream exists, local ahead → `git push`.
- Never `--force` or `--force-with-lease`. If the push is rejected, report it and let the user decide.

## Compose the title and body

**Optional: refresh the base before writing the body.**
Run `git fetch origin <base>` to update `origin/<base>` so the diff commands from Phase 2 (`git diff --stat origin/<base>...HEAD`, `git log ... origin/<base>..HEAD`) reflect the true merge-base rather than a potentially stale local copy. Do this when the base may have moved since the last fetch — merges, rebases, or a shared branch with active teammates. Skip it when speed matters or you know the base is fresh (e.g. you just pulled it). It costs one network round-trip.

Check for project conventions first:

- **PR template** — GitHub resolves templates from three root locations in priority order: `.github/`, `docs/`, and the repo root. In each location look for `pull_request_template.md`, `PULL_REQUEST_TEMPLATE.md`, or a `PULL_REQUEST_TEMPLATE/` directory. So the full set of candidates is: `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/`, `docs/pull_request_template.md`, `docs/PULL_REQUEST_TEMPLATE.md`, `docs/PULL_REQUEST_TEMPLATE/`, `pull_request_template.md`, `PULL_REQUEST_TEMPLATE.md`, `PULL_REQUEST_TEMPLATE/`. If one exists, fill its sections rather than inventing your own structure. The maintainers chose that shape for a reason.
- **Linked issues** — scan the branch name and commits:
  - GitHub issues like `#123` / `fixes #123`.
  - Linear keys like `eng-412`, often in branch names (`dzh/eng-412-token-refresh`). Linear auto-links PRs whose title or body contains the key, so make sure it lands in one.
  - If the branch clearly maps to an issue but no closing keyword is present, add one (`Closes #123` / `Fixes ENG-412`) unless the change only partially addresses it.

**Title:** one line, imperative, describing the change as a whole — if the branch has five commits, summarize all of them, not commit #5. **Conventional Commit format by default**, but match an evident repo convention when one clearly exists (e.g. a commitlint config, or consistent existing PR/commit titles) — forcing CC against a repo's settled style can clash with commitlint or squash-merge tooling. Type and scope reflect the net change.

### Conventional Commit format

Used for the PR title and for any commit this skill creates:

```
type(optional-scope): short imperative description
```

- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`. Pick the most specific that fits; don't default to `chore`.
- **Scope** is optional but useful — the package/module/area touched, e.g. `feat(auth):`.
- **Description** is lowercase, imperative, no trailing period, under ~72 chars.
- **Breaking changes:** append `!` after type/scope (`feat(api)!: ...`); for a commit, add a `BREAKING CHANGE:` footer.

If the change spans several types, pick the dominant one rather than inventing a compound type.

**Body** (when no template exists) — short and skimmable:

```markdown
## What
<one or two sentences: which files, what kind of change>

## Why
<one or two sentences: what made this necessary>

## Notes for review
<the contestable parts only>

<Closes #N / Fixes ENG-N if applicable>
```

Target under ~300 words plus at most one table. Past that, the extra is almost always
restatement.

Scale the body to the diff. ~300 words is a ceiling, not a target. A change of a few lines
gets one short paragraph, plus the warnings a reviewer must not miss. Verification steps and
background already recorded in the linked issue stay there.

"Notes for review" is the section that goes wrong. It is not a summary of the diff — the diff is
right there. It is the short list of things a reviewer could disagree with: an inference you drew,
a judgement call, a number you're asserting, something you got wrong earlier in the branch. If
none of that exists, drop the section.

Rules that keep it short:

- **One headline finding, stated first.** Open with the single thing a reviewer must not skim
  past, in bold. Everything else supports it. Three co-equal bold blocks means you haven't decided
  what matters.
- **State an implication once.** If a bullet already says what the finding means, don't add a
  paragraph explaining what that means in turn.
- **Point into the artifact, don't copy it.** When the diff already carries the full detail,
  abbreviate and say "full table in the record". The body is a reading order, not a second copy.
- **Table rows are distinct behaviours, not distinct commands you ran.** Collapse rows sharing an
  outcome and a cause. Eight verification runs producing four behaviours is a four-row table.
- **Cut negative results** unless a reviewer would otherwise assume the thing broke.
- **Scope the body to the diff.** Open questions the change surfaced but doesn't touch belong in
  an issue, not here.

Rules that keep it useful. Never cut these to save words:

- Where you were wrong earlier in the branch, and what you corrected.
- Why a superseded decision was right at the time. "X was recorded as not-Y, which was true at
  merge; Y landed afterwards" reads as drift rather than as an error to hunt for.
- Exact identifiers: policy IDs, error strings, versions, flags. They tell a reviewer where to
  look.

Don't pad it.

## Draft vs ready

Default to **ready for review**. Switch to `--draft` automatically if the branch looks unfinished — commit subjects containing `wip`, `tmp`, `fixup!`, or `squash!`. Always respect an explicit request for either (e.g. the user passes "draft" in $ARGUMENTS).

## Open

```bash
gh pr create \
  --base <base> \
  --head <branch> \
  --title "<title>" \
  --body "<body>" \
  [--draft]
```

Do **not** add reviewers, assignees, labels, or milestones unless asked — auto-assigning spams people and auto-labeling guesses at taxonomy you don't control.

If `gh pr create` says a PR already exists, don't open a second one — surface the existing URL and ask whether to update it (`gh pr edit`). (Phase 2 normally catches this first.)

## Finish

Print the PR URL on its own line. That's what the user wants. Don't summarize the diff back to them — they just wrote it.

Then, on the next line, print a one-line auto-merge hint: `enable auto-merge: gh pr merge <number> --auto --squash` (substitute the PR number; pick the merge method the repo uses — `--squash`, `--merge`, or `--rebase`). The skill never runs this — it only surfaces the option so the user can opt in explicitly. Skip the hint for draft PRs (not mergeable yet).

---

## Hard limits

- Never force-push.
- Never auto-merge or enable auto-merge.
- Never commit uncommitted changes without explicit confirmation.
- Never open a PR from the default branch into itself.
- Never add reviewers/labels/assignees unprompted.
- Never push before the branch-fit decision is resolved.
