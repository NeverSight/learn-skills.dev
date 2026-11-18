---
name: github-project-init
description: Stand up the GitHub project from the task breakdown, after coding standards are set. Converts every task-breakdown card into an issue (assigned to the right teammate, labelled, milestoned per sprint, placed in the board Backlog), creates the Projects v2 Kanban board, the dev/test/main branches with protection, issue and pull-request templates, CI quality and build workflows, dependabot, and a release template. Asks each role (TL, BE1, FE1, ...) for their GitHub username first. Use when the user wants to initialize a GitHub project, create issues from the task breakdown, set up the kanban board, repo templates, branches, or CI workflows.
---

# GitHub Project Init

Turn the planned work into a live GitHub project: issues, board, branches, templates, and CI. This runs **after `coding-standard`** (the PR template and CI quality gate reference the checklist) and reads the task breakdown (`docs/task-breakdown/`, or `docs/TASK_BREAKDOWN.md` in an older project) as the issue source. It is the only skill that writes CI: `tech-lead-setups` defines the aggregate check command, and this skill's workflow runs it.

**Running project (adopt mode).** If the repository already has branches, protection rules, labels, a board, or workflows, keep them. Add only what is missing, and ask before you add a branch or change a default branch or a protection rule.

This skill performs many outward-facing, hard-to-reverse actions (creating dozens of issues, branches, a board). Work in two phases: **gather and confirm the full plan, then execute.** Never bulk-create before the user has approved the plan and the issue count.

## Prerequisites

- `gh` authenticated with repo write access: `gh auth status`. If not, ask the user to run `gh auth login`.
- A GitHub repository exists for this project. If not, confirm and create it (`gh repo create`).
- The task breakdown exists (run `task-breakdown` first if not) and the coding standard and review checklist exist: `docs/coding-standard/` and `docs/code-review-checklist/`, or the single-file forms in an older project (the templates and CI reference them). Read `docs/technical-specs/` and `docs/deployment-plan/` (or `DEPLOYMENT_PLAN.md` in an older project) for the verification commands and the branch/deploy model, and `docs/business/sprint-breakdown.md` for the canonical sprint numbers and titles.
- Issues come from the **engineering** cards in the task breakdown (backend, frontend, and Tech-Lead scaffold work). Deployment, release, and ops procedures are not cards; they live in `docs/deployment-plan/`. Do not invent issues for them.

## Phase 1: Gather and confirm

1. **Resolve the repo.** `gh repo view --json nameWithOwner,defaultBranchRef`. Confirm owner/name with the user.
2. **Collect GitHub usernames per role.** From `docs/task-breakdown/team-and-process.md` the roles are placeholders (`TL`, `BE1`, `FE1`, `FE2`, ...). Ask the user for each one's GitHub username, allowing "none" so that role's issues stay unassigned. Build a `role -> @username` map; this drives issue assignees.
3. **Confirm the label vocabulary.** Propose the set in [references/labels.md](references/labels.md) and let the user adjust before creating.
4. **Confirm the board columns.** Propose `Backlog, Ready, In Progress, In Review, Done`; every issue starts in **Backlog**.
5. **Confirm the branch model.** `dev`, `test`, `main`; feature branches target `dev`, `dev` promotes to `test`, `test` releases to `main` (match `docs/deployment-plan/04-release-updates.md`). Confirm the default branch (usually `dev`) and which branches get protection.
6. **Confirm CI shape.** Propose the three gates in [references/ci-gates.md](references/ci-gates.md): a heavy PR gate, a light gate on pushes to the long-lived branches, and a heavy build gate in a build/deploy workflow that is manual (`workflow_dispatch` with an environment selector) plus on release. Ask the two questions in its "The condition" section: does any environment deploy on every merge, and does every change reach `dev` through a PR. Confirm the commands from the standard and `tech-lead-setups`: the aggregate check, `check:fast`, `test:e2e`, and `test:e2e:full`.
7. **Summarize and get the go-ahead.** State the counts (N issues across M sprints, the branches, the files to be committed) and confirm before executing. This is the gate.

## Phase 2: Execute

Run in this order so dependencies exist before they are referenced. Prefer `gh` and `gh api` (remote operations) so nothing depends on a local push. Make every step idempotent: check existence before creating, so a re-run repairs rather than duplicates.

### A. Labels

Create the agreed set (idempotent: `gh label create <name> --color <hex> --description <d> --force`). See [references/labels.md](references/labels.md).

### B. Branches and protection

- Get the base SHA: `gh api repos/{owner}/{repo}/git/refs/heads/{default} --jq .object.sha`.
- Create `dev`, `test`, `main` if missing via the refs API (this is not a `git push`, so it works even under a push-blocking hook):
  `gh api -X POST repos/{owner}/{repo}/git/refs -f ref=refs/heads/dev -f sha=<sha>`.
- Set the default branch: `gh api -X PATCH repos/{owner}/{repo} -f default_branch=dev`.
- Protect `main` and `test` (require the CI quality check and at least one review) via `gh api -X PUT repos/{owner}/{repo}/branches/{b}/protection ...`. Confirm the exact rules with the user.

### C. Repo files

Generate these from the project's real values (commands, checklist, sprints), then commit them. Open a PR into `dev` rather than committing to a protected branch. If a local push is blocked by a guardrail hook, hand the push command to the user.

- `.github/ISSUE_TEMPLATE/feature.md` and `bug.md` (and `config.yml`): fields for the linked US/AC ids, task id, description, and definition of done.
- `.github/PULL_REQUEST_TEMPLATE.md`: one `## ` section per `pr-heading` in the coding standard's `pr-hygiene` block, in that order (by default Summary, Card, Tests, Checklist). Card holds the card ID and the US and AC it covers. Checklist holds the self-review attestation that points at the review checklist (`docs/code-review-checklist/`).
- `.github/scripts/pr_hygiene.py`: copied from the `setup-pre-commit` skill in engineering-skills. It checks commits, the branch name, and the PR against the `pr-hygiene` block.
- `.github/workflows/ci.yml`: the PR gate on `pull_request` and the branch gate on push to `dev`/`test`/`main`, as [references/ci-gates.md](references/ci-gates.md) sets out, with its defaults on every workflow. Use the detected package manager and commands; do not hard-code a stack. In adopt mode, measure the existing workflows first (`gh run list --limit 100 --json name,event,conclusion,createdAt,updatedAt`) and propose the changes as a table before you edit them. Add a `pr-hygiene` job on `pull_request`: write the PR title and body from the event payload to files, list the changed paths with `git diff --name-only origin/<base>...HEAD` and write the diff with `git diff origin/<base>...HEAD`, run `pr_hygiene.py pr --title <file> --body <file> --branch <head> --changed <file> --diff <file>`, and run `pr_hygiene.py commit-msg` on every commit in the PR.
- `.github/workflows/build.yml` (or `deploy.yml`): `workflow_dispatch` with an environment input, plus a `release: published` trigger for production. Its first job is the build gate: the aggregate check and `test:e2e:full` on the exact commit. The build and deploy jobs `need` it. Mirror the deploy policy in `docs/deployment-plan/`.
- `.github/dependabot.yml`: the ecosystem(s) present in the repo, weekly, grouped where sensible.
- `.github/release.yml`: auto-generated release-notes categories mapped to the labels.

### D. Milestones

One milestone per sprint, with numbers and titles taken from `docs/business/sprint-breakdown.md` (the canonical sprint source, which the task breakdown follows):
`gh api -X POST repos/{owner}/{repo}/milestones -f title="Sprint 1: <focus>" -f description="..."`.

### E. Project board

- Create the Projects v2 board: `gh project create --owner {owner} --title "<repo> delivery"`.
- Ensure the `Status` field has the agreed columns and that `Backlog` is the default.
- Add an **`Estimate`** number field so the developer-day estimates from the task breakdown live on the board: `gh project field-create <number> --owner {owner} --name "Estimate" --data-type NUMBER`. This lets the board sum and group by effort per sprint/assignee.
- For a timeline/gantt-style view, add an `Iteration` field (one iteration per sprint, durations from the sprint cadence) and a Roadmap view; the Roadmap view renders issues as bars across iterations. Offer this; it is optional.
- Items are added in step F and set to `Backlog`.

### F. Issues from the task breakdown

Parse the card tables in each `docs/task-breakdown/sprint-N.md` (or in the single `docs/TASK_BREAKDOWN.md` of an older project). For each card create one issue:

- **Title**: `<Card ID> <PM Card Title>` (e.g. `BE-S1-08 Implement real POST /work-orders`).
- **Body**: the Task Description, the AC ids it satisfies (link to `docs/business/`), the Docs refs, and the Est. Note wiring cards explicitly.
- **Labels**: area from the card's role: the Card ID prefix (`BE`->`area:backend`, `FE`->`area:frontend`, `TL`/`DB`->`area:infra`), or the board's role column when its IDs do not encode the role, a `type:*`, the `sprint:<n>`, and `wiring` for wiring cards.
- **Assignee**: the `role -> @username` map (skip if "none").
- **Milestone**: the sprint milestone.

Then add the issue to the board, set its status to `Backlog`, and set its `Estimate` field from the card's Est as a plain number (strip the unit: `1.5d` becomes `1.5`):
`gh issue create --title "..." --body-file <tmp> --label ... --assignee ... --milestone "..."`, then `gh project item-add`, then `gh project item-edit` to set both the `Status` (Backlog) and `Estimate` fields. If the Iteration field exists, set it to the card's sprint.

Create them in a loop. For a large breakdown, confirm the count first and report progress as you go. Skip cards whose issue already exists (match by title) so a re-run is safe.

### Report

When done, report what was created: issue count per sprint, the board URL, the branches and protection, and the PR that adds the `.github` files. List anything skipped (existing issues, unassigned roles).

## Safety

- Confirm the plan and the issue count before creating anything. Bulk issue creation is tedious to undo.
- Idempotent throughout: check before create; a second run repairs gaps instead of duplicating.
- Do not commit directly to a protected branch; open a PR into `dev`.
- If a push-blocking guardrail hook is active, the remote `gh`/`gh api` operations still work; only local `git push` for the `.github` files needs to be handed to the user.

## Writing conventions (enforced in all output)

- No AI slop: no filler or hedging; every sentence informs. Use the `stop-slop` skill on prose when unsure.
- No em-dashes, no double-dashes (`--`) in prose; dashes only as Markdown syntax (list bullets, table rules) or in literal code/CLI flags (e.g. `--no-deps`).
- No emoji. Professional, declarative tone.
- If a document carries a metadata header (`**Version:**`, `**Date:**`, `**Author:**`, `**Status:**`, `**Phase:**`), each such line ends with two trailing spaces so Markdown renders them on separate lines.
