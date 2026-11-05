---
name: setup-matt-pocock-skills
description: "Configure the repo's issue tracker, ownership, optional GitHub Project, final PR policy, triage vocabulary, and domain docs."
disable-model-invocation: true
---

# Setup Matt Pocock's Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live, who owns them, and which branch receives final PRs
- **Work tracking**: the existing GitHub Project and its Status mapping, or explicit issue-only tracking
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present the concrete configuration, then write within the user's authorization. Reuse choices already agreed in the session; ask only for unresolved choices.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root, and the legacy `CONTEXT.md` / `CONTEXT-MAP.md`. If a legacy file exists, offer to `git mv` it to its `GLOSSARY` name and rewrite those names in `docs/agents/domain.md`.
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- For GitHub: the repository's actual default branch, intended final PR base, active developer identity, and any existing Project configuration. Discover repository-linked Projects and check owner-level candidates with `gh project list --owner <owner> --format json`; a candidate is not selected until its repository relevance is verified. Read the selected Project's fields, options, items, and views where available. Preserve existing mappings and unrelated configuration.
- Check Project access with `gh project view <number> --owner <owner> --format json` and `gh project field-list <number> --owner <owner> --format json`. Missing read access requires `read:project`; writing requires `project`. Tell the user to run `gh auth refresh --hostname <host> --scopes project` in their terminal when needed. Report missing scopes or organization permissions explicitly; an inaccessible Project is not evidence that none exists.
- Are `triage`, `to-spec`, or `to-tickets` installed? Check sibling skill folders or the available skills. These consumers determine whether Section B runs; publishing still needs a readiness label when `triage` is absent.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order. One section, one answer, then the next.

Lead each unresolved section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip Section B when no installed skill consumes its labels, and write the single-context layout without asking when there is no monorepo.

**Section A: Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it. They need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

A GitHub or GitLab tracker needs a reachable repo. When the user picks one and no `git remote` points at that host, get the repo URL from them and wire it up (`git init` if needed, `git remote add origin <url>`) before going further. Done when `gh repo view` / `glab repo view` prints the project from inside this directory; if it can't, stop and tell the user what's missing.

**Section A.1: Ownership and work tracking.** For GitHub, configure the lifecycle in the GitHub seed template.

- Recommend the verified existing Project. If several are relevant, ask which is authoritative; create a Project only when requested. Map existing equivalent Status options before proposing additions.
- Record the Project owner, number, URL, Status field name, and actual option names for `todo`, `in-progress`, `waiting-validation`, `blocked`, `paused`, and `done`. Record `Project: disabled` only when the user chooses issue-only tracking. An access failure remains pending configuration.
- Ownership defaults: new PRDs belong to the developer driving the session; new children inherit the parent's assignees, falling back to the driving developer when the parent is unassigned. Preserve existing assignments unless reassignment was requested.
- Status belongs in the Project. Keep labels for triage and scope; when adopting a Project, discuss existing lifecycle labels before changing them.
- Record the intended final PR base separately from the actual default branch. Recommend making the integration branch the default only when that matches the team's flow; changing the default branch requires an explicit instruction. Native closing references work for final PRs targeting the actual default branch. For another base, record a separately authorized post-merge reconciliation procedure.
- Recommend native Project workflows: add matching issues from the selected repository, initialize new items as Todo, and reflect completed issue closure as Done. Keep issue closure driven by verified final delivery rather than moving a card. These workflows require no GitHub Actions runner.
- Preserve shared Project settings for other repos. If workflow/view configuration requires the web UI, give the exact remaining steps and record them as pending until confirmed. Auto-add does not backfill existing issues: enumerate the intended existing scope and add it explicitly only when authorized.

For GitLab, local markdown, or another tracker, preserve its native ownership and status conventions. GitHub Projects are optional.

**Section B: Triage label vocabulary.** Run this section when `triage`, `to-spec`, or `to-tickets` is installed. Reuse an existing mapping. Publishing requires `ready-for-agent` even without the triage skill.

If the mapping is unresolved, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no, usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`), collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root). This fits almost every repo; write it without asking.

Offer **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found monorepo signals. Then confirm which layout they want.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last when Section B runs)

Apply decisions already approved in the session. Present unresolved choices before changing them. Replace seed placeholders with verified values; preserve unrelated repository-specific conventions.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create; don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa); always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

Before publishing, implementing, resuming, or delivering tracked work, read `docs/agents/issue-tracker.md` for tracker operations, ownership, Project status, and final PR policy.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the `### Triage labels` sub-block and write `docs/agents/triage-labels.md` when Section B ran. Otherwise omit both.

When Section B ran on GitHub or GitLab, create missing labels used by installed skills (`gh label create` / `glab label create`): all five roles for `triage`, or just `ready-for-agent` when only the publishing skills consume labels. Preserve the canonical role mapping without adding Project lifecycle labels.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping (when Section B runs)
- [domain.md](./domain.md): domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Verify and report

Read back the written tracker policy and the selected Project's fields and mappings. Verify only the remote changes actually made; report any pending auth, workflow, or UI steps separately. Setup is complete only when the selected configuration is written and the required remote configuration is verified. Issue-only tracking needs no Project verification.

Tell the user which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later; re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
