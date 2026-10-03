---
name: setup-software-engineering-skills
description: "Configure a repository's engineering-skill integration: issue tracker, triage labels, domain documentation, and model routing when available. Use when installing these skills into a repository or when another skill reports that docs/agents/ configuration is missing."
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Setup software engineering skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** - where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels** - the strings used for the seven canonical triage roles
- **Domain docs** - where `CONTEXT.md` and ADRs live, and the consumer rules for reading them
- **Model routing** - a session-start pointer to `model-routing` when that skill is available

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write. When `model-routing` is available in the current session, load it and route the setup deliverables before starting.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` - is this a GitHub repo? Which one?
- When Azure DevOps organization/project scope is supplied or discovered, run authenticated project and work-item-type queries from [issue-tracker-azure-devops.md](references/issue-tracker-azure-devops.md). Inventory the available types and inspect their workflow states, required fields, and process/team hierarchy where exposed. Record the evidence and verification status for types, states, and Parent/Child relationships separately. Some CLI versions have no `az boards work-item type list`; use the documented WIT REST resource through `az devops invoke` or an authenticated REST client.
- `AGENTS.md` and `CLAUDE.md` at the repo root - does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/` - does this skill's prior output already exist?
- `.scratch/` - sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Is the `wayfinder` skill installed? Check its availability in the current agent's skills or installed skill directories. This decides whether Azure DevOps setup asks the user to choose a map type.
- Is `model-routing` available to the agent in the target project? Check the current skill catalog and the target project's applicable project or user skill locations. A source copy in a distribution repository alone does not establish availability. Include the model-routing pointer only when the target agent can load the skill.
- Monorepo signals - a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

**Complete when:** the tracker evidence, existing agent configuration, triage, Wayfinder and model-routing availability, and context-layout signals are recorded or explicitly absent.

For a failed or unauthenticated Azure DevOps query, explicitly report which types, states, and relationships remain unverified. Ask for missing organization/project data or authentication, then repeat discovery. General Agile templates and other repository files cannot verify the project's current configuration. A user-supplied mapping remains a proposed convention until supported by project evidence; record any explicitly accepted verification gap using the Azure DevOps reference's failure procedure.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order - one section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A - Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills that create, triage, or plan work need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow another workflow. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **Azure DevOps** - issues live in the repo's Azure DevOps project (uses the `az devops` CLI)
- **GitHub** - issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab** - issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown** - issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.) - ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off** - leave it off and don't raise it; a user who wants external PRs in the triage queue can flip the flag in the file later.

For Azure DevOps, confirm the discovered organization/project and present the type inventory, state categories, hierarchy evidence, and outstanding verification gaps. Repeat authenticated discovery after resolving scope or access problems. Ask which available types should represent approved specifications and implementation tickets. When `wayfinder` is installed, ask for the map type and confirm the decision-ticket type separately. Custom types such as `Specification` and `Wayfinder` are choices, not presumed requirements. If a requested type is unavailable, ask the user to choose an available type or resolve the process configuration before using it.

**Section B - Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you) - an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are seven canonical roles, each label string equal to its name: categories `bug` and `enhancement`; states `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. On **yes**, write them as-is. Only if the user says no - usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`) - collect the overrides so `triage` applies existing labels instead of creating duplicates.

**Section C - Domain docs.** Default to **single-context** - one `CONTEXT.md` + `docs/adr/` at the repo root. This fits almost every repo; write it without asking.

Offer **multi-context** - a root `CONTEXT-MAP.md` pointing to per-context `CONTEXT.md` files - only when exploration found monorepo signals. Then confirm which layout they want.

**Complete when:** every unresolved configuration branch has one user answer.

### 3. Confirm target and draft

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) - always edit the file that already exists.

Show the user a draft of:

- The `## Agent skills` block for the selected file
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)

For Azure DevOps, show the complete tracker draft, including confirmed scope/process, available types, workflow type roles, required inputs, hierarchy and relation direction, state mappings, triage tags when applicable, completion rules, and all verification gaps. State whether each finding is verified, user-selected, or explicitly accepted as unverified. Use those mappings in the proposed Wayfinding, specification, and ticket operations. Agent instruction pointers must direct consuming skills to this contract before publication, hierarchy changes, triage, or completion; keep the mappings authoritative in the tracker document.

Let them edit before writing.

**Complete when:** the user has approved the selected instruction file and the complete contents of every generated document. For Azure DevOps, configuration values are confirmed or explicitly accepted as unverified, and operations depending on unverified values are documented as blocked until discovery succeeds. Unknown values are labelled unverified rather than inserted into executable commands.

### 4. Write

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Model routing

At the start of every session, before starting or delegating any task, load and apply the `model-routing` skill when available. Follow its model selection, harness fallback, and session-reuse rules.

### Issue tracker

[one-line summary of where issues are tracked]. Before creating or reading tickets, publishing specifications, changing hierarchy, triaging, wayfinding, or completing work, use the type roles, state mappings, and verification status in `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. Before applying triage roles, use `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout - "single-context" or "multi-context"]. Before exploring domain behavior or naming domain concepts, use `docs/agents/domain.md`.
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

Include `### Model routing` as the first sub-block only when exploration confirmed that the target agent can load `model-routing`. Keep the routing rules in the skill itself; the project instruction file carries only the pointer above. Preserve an existing equivalent instruction instead of adding a duplicate, and reconcile conflicting routing instructions with the user in the draft. Once the selected instruction file is loaded in a new session, its pointer requires routing before work begins.

For Azure DevOps, generate work-item templates from the process findings gathered in Section A, using the output structure in [issue-tracker-azure-devops.md](references/issue-tracker-azure-devops.md). The assigned process determines the types, fields, rules, and states.

Include the Wayfinding operations for every tracker. They establish stable tracker mechanics so the `wayfinder` skill can be used later without rerunning setup.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-azure-devops.md](references/issue-tracker-azure-devops.md) - Azure DevOps issue tracker
- [issue-tracker-github.md](references/issue-tracker-github.md) - GitHub issue tracker
- [issue-tracker-gitlab.md](references/issue-tracker-gitlab.md) - GitLab issue tracker
- [issue-tracker-local.md](references/issue-tracker-local.md) - local-markdown issue tracker
- [triage-labels.md](references/triage-labels.md) - label mapping (only if `triage` is installed)
- [domain.md](references/domain.md) - domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

**Complete when:** the selected agent file and generated documents match the approved draft, their required pointers resolve, executable tracker commands contain no unresolved configuration placeholders, explicitly accepted verification gaps and blocked operations are documented, and the model-routing pointer is present exactly once when the skill is available to the target agent.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later - re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.

**Complete when:** the user knows which skills consume the configuration and when to rerun setup.
