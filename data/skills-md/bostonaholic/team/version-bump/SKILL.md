---
name: version-bump
description: 'Use for version bumps on explicit request or as the pre-merge step of a PR land. Never infer from finished, reviewed, green, or draft-ready work. Assigns SemVer.'
---

# Version Bump — version a project at land time

This repository's own versioning procedure. `AGENTS.md` declares it as the
pre-merge step, so the land command runs it before merging. Tagging and the
GitHub release are **not** part of it; `release-on-merge.yml` does that on
merge. When invoked directly, run this skill **before** the land command,
against the version of `main` you intend to land onto. When a land command
invokes this skill, return to it after step 8.

## Precondition — explicit land intent

**Why:** the bump is computed against the base branch's tip at this moment; a
bump made before the land goes stale when another PR merges, and the pre-merge
guard then denies the merge.

**This skill fires only on explicit land intent**, meaning one of:

- The user asked to land: "ship it", "land the PR", "land this".
- The user asked for the bump itself: "bump the version", "version this PR".
- A land command is already in flight and reached the project's pre-merge steps.

**Never infer land intent.** None of the following is a cue to bump:

- The work is finished, the review passed, or CI is green.
- A draft PR is about to be opened, or was just opened. A drafted PR carries
  **no** version: the bullet goes under `## [Unreleased]` and nothing else moves.
- The invariant script exited 1. That exit states a precondition for *merging*,
  expected for a runtime PR's whole review lifetime, never a request to bump now.

With no land intent, **stop and say so.** Report that the branch will need a
bump before it can merge, and wait for the user. Do not bump "to be helpful".

## Steps

### 0. Runtime-vs-dev gate — does this PR warrant a bump at all?

**Run this before everything else. Most steps below only apply if it says yes.**

The quick look is orientation only — it never decides the exit:
`git diff "origin/<default>...HEAD" --name-only`. The decision comes from **the
invariant run**, the same invocation contract the pre-merge guard enforces:

1. Resolve the default branch by asking GitHub (`gh repo view`), falling back
   to the local `origin/HEAD` ref. Never a guessed `main`. If both fail, stop:
   no verdict.
2. `git fetch origin <default>` must succeed. Never degrade to a stale base for
   a verdict.
3. The fetched `origin/<default>` tip must be an ancestor of the branch tip. If
   the branch is behind, **stop**: rebase onto `origin/<default>` and re-enter
   step 0.
4. Run the script with `HEAD_SHA` = the local branch tip and `BASE_SHA` = the
   fetched `origin/<default>` **tip** — never a pre-computed merge-base, and
   never a hand-rolled two-dot diff.

```bash
DEFAULT=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null)
DEFAULT=${DEFAULT:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|^refs/remotes/origin/||')}
[ -n "$DEFAULT" ] || { echo "cannot resolve the default branch — no verdict"; exit 1; }
git fetch origin "$DEFAULT" || { echo "fetch failed — no verdict"; exit 1; }
git merge-base --is-ancestor "refs/remotes/origin/$DEFAULT" HEAD \
  || { echo "behind base — rebase onto origin/$DEFAULT, re-enter step 0"; exit 1; }
HEAD_SHA=$(git rev-parse HEAD) BASE_SHA=$(git rev-parse "refs/remotes/origin/$DEFAULT") \
  .claude/scripts/version-bump-required.sh
```

**Read the outcome by exact output match — the signal rule, default-deny:**

- Exit 0, stdout starting `OK: runtime_changed=false bumped=false` → dev-only
  and final. **DO NOT BUMP.** Skip every step below. Leave the version
  untouched, do **not** cut the changelog, and land with the plain
  conventional title (`<type>: <subject>`). On a re-entry whose PR title
  still carries a stale `vX.Y.Z` prefix from an earlier bump, strip it now
  (`gh pr edit --title`) — the title backstop never strips a stale prefix,
  and this is the one step-8 action a no-bump exit still owes. Then go
  straight to the land command. This exit **requires** that OK line — the quick look
  alone never authorizes it.
- Exit 0, stdout starting `OK: runtime_changed=true bumped=true` → already
  bumped (a recovery re-entry). Never re-bump — proceed to the land command.
- Exit 1, verdict containing `cannot merge until version-bump runs at land time`
  → bump warranted. It is actionable here only because the land-intent
  precondition already passed; read outside a land it states a merge
  precondition and nothing more.
  - On a branch with **no** `chore(version)` commit: **continue to step 1**.
    Every other exit-1 verdict in this list stops.
  - On a branch **already carrying** a `chore(version)` commit: the bump went
    stale (a rebase moved the fork point). Stop — drop the bump commit, undo
    the changelog cut, reset the title, and re-enter step 0.
- Exit 1, verdict containing `must land with no bump` → wrongful bump. Stop —
  drop the commit, undo the cut, and re-run step 0.
- **Anything else** — a non-semver version, a merge-base or diff failure, or
  unrecognized output — stops in both directions. Surface the message
  verbatim. A hard script error never means "keep going".

This is a hard gate, not a judgment call.

### 1. Decide the bump level

Reached **only when step 0 said a bump is warranted**; the only question is how
big the bump is.

```bash
# Re-derive the base: shell variables do not persist from step 0's call.
DEFAULT=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null)
DEFAULT=${DEFAULT:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|^refs/remotes/origin/||')}
: "${DEFAULT:?cannot resolve the default branch}"
git log "origin/$DEFAULT..HEAD" --oneline
git diff "origin/$DEFAULT...HEAD" --stat
```

[SemVer 2.0.0](https://semver.org/spec/v2.0.0.html), quoted verbatim. Items 6,
7, and 8 each carry an `x > 0` precondition:

| Item | Normative rule | Scope |
|------|----------------|-------|
| 6 | PATCH "MUST be incremented if only backward compatible bug fixes are introduced. A bug fix is defined as an internal change that fixes incorrect behavior." | `x.y.Z \| x > 0` |
| 7 | MINOR "MUST be incremented if new, backward compatible functionality is introduced to the public API." | `x.Y.z \| x > 0` |
| 8 | MAJOR "MUST be incremented if any backward incompatible changes are introduced to the public API." | `X.y.z \| X > 0` |

If the version starts `0.`, none of those three binds. Item 4 governs: "Major
version zero (`0.y.z`) is for initial development. Anything MAY change at any
time. The public API SHOULD NOT be considered stable." Item 5: "Version 1.0.0
defines the public API." The spec assigns no level pre-1.0, so the decision
below uses the same observable-change rule before and after 1.0.0.

Ask these in order. **The first yes wins.** Judge the *change*, never the
commit subject:

1. **Can a plugin user observe the difference?** → **minor**. Anything that
   changes what they type, what they get back, or what the project does on
   their behalf is observable: a command's name or arguments
   (`argument-hint`), documented behavior, whether a step prompts them, an
   artifact's format or frontmatter schema, an agent's model, or tool access.
   New and changed capability both land here.
2. **Otherwise** → **patch**: internal-only *and* backward compatible — prose
   that clarifies without changing an instruction, a comment, restructuring
   that preserves behavior. Item 6 requires both qualifiers, not just a `fix:`
   subject. Expect patch to be rare for projects that ship instructions a
   model reads. Do not widen patch to make the cadence feel familiar.

**`major` is unreachable while the version starts `0.`** A breaking change
pre-1.0 is a **minor**, not a major. If a change looks like it warrants major,
that is a signal to **ask whether it is time to declare 1.0.0** — a deliberate
decision, never a side effect of this skill.

State the chosen level and which question decided it. A level that needed a
judgment call means the observability question was not actually answered —
answer it rather than asking the user.

### 2. Compute the next version

```bash
bash .claude/scripts/next-version.sh <level>
```

### 3. Bump every version string

The version lives in **every file below**:

| File | Occurrences |
|------|-------------|
| `.claude-plugin/plugin.json` | 1 (`version`) |
| `.claude-plugin/marketplace.json` | 2 (`metadata.version` **and** `plugins[0].version`) |
| `.codex-plugin/plugin.json` | 1 (`version`) |
| `.cursor-plugin/plugin.json` | 1 (`version`): what Cursor reports |
| `package.json` | 1 (`version`) |
| `plugin.json` (repo root) | 1 (`version`): what Antigravity reports |

Each host shows the version in its own manifest: Codex reads
`.codex-plugin/plugin.json` in preference to the Claude manifest; Antigravity
reads the root `plugin.json`, which sits at the root rather than in a directory
of its own because that host resolves `skills/` and `agents/` as siblings of
its manifest. A stale one makes the same release look like two different
versions depending on the host.

Edit every file, then prove it:

```bash
grep -rn '"version"' package.json plugin.json .claude-plugin/plugin.json \
  .claude-plugin/marketplace.json .codex-plugin/plugin.json .cursor-plugin/plugin.json
```

Every line must show the **new** version. None may still show the old one.

### 4. Cut the changelog section

In `CHANGELOG.md` (Keep a Changelog format, entry style per
`skills/team-pr/references/changelog.md`):

- Move the entire `[Unreleased]` body into a new `## [X.Y.Z] - YYYY-MM-DD`
  (today's date) section inserted directly **below** `## [Unreleased]`. Leave
  `## [Unreleased]` in place, now empty again.
- Re-point the link-reference footer:
  - `[Unreleased]` compare base → `vX.Y.Z...HEAD`
  - Add `[X.Y.Z]: https://github.com/<owner>/<repo>/compare/v<prev>...vX.Y.Z`

This section becomes the GitHub release notes verbatim — write it for a reader
deciding if the upgrade is worth it. Any links must be **absolute URLs**:
relative paths (e.g. `docs/versioning.md`) render as dead links on the release
page.

**Empty `[Unreleased]`.** A PR that reached this step changed runtime files; an
empty `[Unreleased]` on it means nobody wrote the user-facing bullet. **Derive
at least one bullet from the PR's runtime commits**
(`feat:`/`fix:`/`perf:`/`security:`, in that entry style). Never write an empty
section (`release-on-merge.yml` errors on empty release notes).

Empty `[Unreleased]` **and** no runtime change is not this case: that PR must
have stopped at **step 0**, with no bump and no changelog cut. Do not invent a
bullet to justify a bump that step 0 already declined. Go back and land plain.

### 5. Land-time consistency assertion

Run it after the changelog cut (so the dated section exists) and **before
committing**:

```bash
bash .claude/scripts/check-version-consistency.sh
node -e "['.claude-plugin/plugin.json','.claude-plugin/marketplace.json','.codex-plugin/plugin.json','.cursor-plugin/plugin.json','.agents/plugins/marketplace.json','plugin.json','package.json'].forEach(f=>JSON.parse(require('fs').readFileSync(f)));console.log('JSON OK')"
```

The released-section and footer-compare-link invariants hold only after the
cut, so assert them inline here:

```bash
V=$(jq -r .version .claude-plugin/plugin.json)
OWNER_REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
ESC=$(sed 's/\./\\./g' <<<"$V")
grep -qE "^## \[$ESC\] - [0-9]{4}-[0-9]{2}-[0-9]{2}$" CHANGELOG.md \
  || { echo "::error::no '## [$V] - YYYY-MM-DD' section — the cut did not land"; exit 1; }
grep -qE "^\[$ESC\]: https://" CHANGELOG.md \
  || { echo "::error::no footer compare link for $V"; exit 1; }
grep -q "\[Unreleased\]: https://github.com/$OWNER_REPO/compare/v$V...HEAD" CHANGELOG.md \
  || { echo "::error::[Unreleased] footer does not compare from v$V"; exit 1; }
echo "OK: land-time consistency holds"
```

If any check fails, **stop before committing** and fix the cut.

### 6. Commit

Commit the bump as its own commit in the PR branch:

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json \
  .codex-plugin/plugin.json .cursor-plugin/plugin.json plugin.json package.json \
  CHANGELOG.md
git commit -m "chore(version): X.Y.Z"
```

### 7. Assert the bump invariant

Re-run the invariant run from step 0 — the head is now the branch tip carrying
the `chore(version)` commit. Require exit 0 with stdout starting
`OK: runtime_changed=true bumped=true`.

This runs **before any remote change** (the title edit in step 8 is remote).
On any other outcome, stop: drop the `chore(version)` commit, undo the
changelog cut, and land plain — nothing has left the machine, so the recovery
is purely local.

### 8. Title the PR

`vX.Y.Z <type>: <subject>` — e.g. `v1.4.0 feat: add a design review gate`. Set
it on the existing PR (`gh pr edit --title`). The `PR title sync` workflow is a
backstop — do not rely on it.

A re-entry path that runs after a title already exists must reset it: the
stale-bump recovery re-titles with the recomputed version, and a re-entry that
ends at "no bump" strips the `vX.Y.Z` prefix explicitly — the title backstop
never strips a stale prefix.

Return to the land command to push, wait for CI, and squash-merge.
