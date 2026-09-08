---
name: setup
description: Configure a repo for the giljabi skills in one run — issue tracker, VCS conventions, test commands, the gitignored working directory, and the docs/domain knowledge scaffold. Run once per repo before first use.
disable-model-invocation: true
---

# Setup

Scaffold the per-repo configuration the giljabi skills read:

- **Issue tracker** — where specs and tickets live → `docs/agents/issue-tracker.md`
- **VCS** — host, integration branch, languages, reviewers → `docs/agents/vcs.md`
- **Testing** — how suites run here, and what breaks when run wrong → `docs/agents/testing.md`
- **Data access** — the read-only path to production data, when the repo provides one → `docs/agents/data.md`
- **Working directory** — `.scratch/` gitignored → `.gitignore`
- **Knowledge layer** — `docs/domain/`, `docs/platform/`, `docs/conventions/` scaffolds → see `/knowledge` for the layer table and contract
- **Agent doc** — pointer blocks in `CLAUDE.md` / `AGENTS.md`

Prompt-driven, not a script: explore, present what you found, confirm, write.

## The repo answers *where*; the skill carries the obligation

These files record facts about **this repo** — the host, the language, the commands. Never the
process itself: `/commit` knows it must screen for secrets; `vcs.md` only says which language the
message is written in. The test for every line: *could this be different in another repo?* If no, it
belongs in a skill, not here.

## 1. Explore — infer before asking

Every answer you can read out of the repo is one the user does not have to type:

- `git remote -v` — the PR host. `github.com` → GitHub; `dev.azure.com`/`visualstudio.com` → Azure
  DevOps; `gitlab.com` or self-hosted → GitLab. No remote → ask.
- `git log --no-merges --format=%s -30` — three answers at once: prose language, whether
  Conventional Commit prefixes are used, and whether they carry scopes (which scopes, if so).
  **`--no-merges` is load-bearing** — a host's merge commits follow no convention and can be a third
  of the sample. An empty history settles nothing; default to English and say so.
- `git log --no-merges -30 --format=%B | grep -ci 'co-authored-by'` — attribution, read as a
  **proportion in a recent window**, never a whole-history grep: a repo that changed policy partway
  returns hits across all time and near-zero recently. A genuine split → ask.
- `git branch -a --sort=-committerdate | head -20` — branch naming. Record the prefixes actually in
  use; skills strip `<type>/` to recover the feature slug.
- Recent merged PR titles (`gh pr list --state merged --limit 10 --json title`, or the `az` form) —
  repos routinely use Conventional Commits on commits and a plain phrase on PR titles; infer each
  from its own evidence. No CLI access → "same as the commit subject", and say so.
- `.gitignore` — whether `.scratch/` is ignored. **A precondition, not a preference**: without it,
  `/commit`'s `git add -A` commits the working directory permanently, and nothing flags it because
  it is not a secret.
- Test-runner config: `package.json` scripts, `Makefile`, `pyproject.toml`, `Cargo.toml`,
  `jest.*.config.*` / `vitest.config.*` / `pytest.ini` — plus a sample of the test files themselves
  (`**/*.spec.*`, `**/*.test.*`, `**/test_*.py`) to read the layout off the paths.
- `scripts/` and the harness's command allow-list — a wrapper that queries a replica read-only, and
  whether the harness already permits it. A wrapper that exists and is not on record is the one an
  agent bypasses with a raw connection string.
- `find . -maxdepth 3 -iname 'pull_request_template*'` — whether the repo ships a PR template, and
  where; `vcs.md` records the path and the template stays there.
- `CLAUDE.md` / `AGENTS.md` — an existing `## Agent skills` block, and any rules already in prose.
- `docs/agents/`, `docs/domain/`, `docs/platform/`, `docs/conventions/` — this skill's own prior output.
- Legacy docs — `docs/adr/`, `CONTEXT.md`, a known-issues file. Their presence means a migration to
  the knowledge layer is owed; note it, name `/migrate-docs` as the follow-up, and do not delete anything.

**Infer the PR host and the issue tracker separately.** They usually coincide and legitimately
differ — local-markdown issues with Azure DevOps PRs is a real configuration. Deriving one from the
other silently misconfigures exactly the repos that most need configuring.

## 2. Present inferences, then ask what is left

Lead with the inferences as statements to correct, not questions to answer. When `.scratch/` is not
in `.gitignore`, state that you will add it — the alternative is not a configuration.

Then ask only these; "none" is a valid answer to each:

- **Tracker** — where should specs and tickets live? Recommend what the remote implies: GitHub
  issues, GitLab issues, or local markdown under `.scratch/` (solo repos, no remote). Anything else
  (Jira, Linear): have the user describe the workflow in a paragraph and record it as prose.
- **Reviewers** — who goes on a PR by default, and do PRs open as drafts? Nothing in the repo
  reveals intent; on a solo project recommend none + draft.
- **Attribution** — does agent-authored work carry a `Co-Authored-By` trailer? Ask even when history
  answered it, unless unambiguous — the harness appends one by default, so an unstated preference is
  the tool deciding for the repo.
- **Test gotchas** — what does someone need to know that `package.json` does not say? A heap size,
  suites that must run serially, an integration DB, a suite too expensive to run locally. Record it
  verbatim; a thin accurate `testing.md` beats a padded guess.
- **Data access** — is there a repo-provided read-only path to production data — a wrapper script, a
  proxy, a replica URL? Record the exact command and what it may not do. `/grill` and `/knowledge-tend`
  read production through it; with none on record they write the SQL and ask.

## 3. Confirm

Show the full drafted contents of every file and the `.gitignore` line. Let the user edit before
anything is written.

## 4. Write

Seed templates in this folder — start from them rather than composing:
[issue-tracker-github.md](./issue-tracker-github.md) ·
[issue-tracker-gitlab.md](./issue-tracker-gitlab.md) ·
[issue-tracker-local.md](./issue-tracker-local.md) ·
[vcs-github.md](./vcs-github.md) · [vcs-azure-devops.md](./vcs-azure-devops.md) ·
[testing.md](./testing.md) · [data.md](./data.md). For a host with no seed, keep the same headings so `/pr` and `/commit`
find what they expect, and say `/pr` will need the commands spelled out.

Generate `docs/domain/README.md` and `docs/platform/README.md` with `/knowledge`'s `index.sh` (empty
directories yield the preamble alone — pages are created lazily), and write
`docs/conventions/README.md` as a hand-kept index with no entries; it points at conventions wherever
they live, so it is the one index not generated.

**Append `.scratch/` to `.gitignore`** if missing; do not reorder or tidy the file around it.

Then add to the `## Agent skills` block in whichever of `CLAUDE.md` / `AGENTS.md` exists — edit the
one that is there; if neither exists, ask which to create. Update sub-blocks in place; leave every
other section alone:

```markdown
## Agent skills

### Issue tracker
[one line]. See `docs/agents/issue-tracker.md`.

### VCS conventions
[host], [language] commits and PR bodies. See `docs/agents/vcs.md`.

### Testing
[one line on how suites run]. See `docs/agents/testing.md`.
[A guardrail line only if a gotcha's violation causes damage, worded to self-trigger:
"Never run the whole suite locally; it can take the machine down."]

### Data access
[one line: the read-only query command]. See `docs/agents/data.md`.

### Knowledge layer
Current-state pages: business entities in `docs/domain/`, stack behaviour in `docs/platform/`, coding
conventions indexed in `docs/conventions/`. Read the pages for anything you touch and change them in
the same diff as the code; the `README.md` indexes are generated, never edited.

### Findings log
Defects and gotchas found mid-feature land in `.scratch/<feature-slug>/findings.md` as they surface.

### Feature state
A `.scratch/<feature-slug>/STATE.md` means that feature is mid-flight. Read it before touching that
feature's code — it names the workflow in progress and the command that resumes it.
```

The last three blocks are **pointers whose full rules live in the skills** — a repo doc restating
them would be a photocopy that never re-syncs. **Feature state** carries a second job: it is the only
line that can bootstrap a resumed workflow — a session resuming cold has not loaded `/giljabi` and
never sees its instruction to read `STATE.md`; this pointer breaks the circle.

## 5. Done

Name every file written and the skills that read each. Editing `docs/agents/*.md` directly is the
normal way to change an answer later; re-running this skill is for starting over.
