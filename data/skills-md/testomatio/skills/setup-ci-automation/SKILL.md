---
name: setup-ci-automation
description: Investigate a project's CI and deploy new automated QA workflows into it. Explains what the existing workflows do — with a diagram — and wires QA tasks to run on repository events, like generating test cases when a PR opens, QA-analyzing new issues, or scheduling suite cleanups. Use when the user asks what their CI does, wants a CI workflow explained or reviewed, or wants a QA task to run automatically in CI.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

# Setup CI Automation

I work with a project's CI: find out what runs there today, explain it, and add new workflows that automate QA tasks on repository events. What a new workflow *does* comes from the skill that owns the task — this skill owns getting it into CI correctly.

## Critical Constraints

- **Only touch CI config files** — never source or test files.
- **Never invent the commands a job runs** — take the payload from the skill that owns the task, or from the user.
- The finished result is CI configuration delivered through a PR — never pushed straight to the default branch.
- Secrets live in the CI's secret store, never in config files.

## Workflow

### Step 1 — Investigate the CI

- Read the repo's CI config files to identify the CI system; several or none → ask which one to target.
- Inventory the existing workflows: trigger, jobs, and purpose of each — new automation must fit in, not duplicate or break what's there.
- Note the primitives this CI offers: secret store, value passing between jobs and pipelines, cross-pipeline triggers, deploy events.

### Step 2 — Explain with a diagram

When the environment renders Mermaid, present a workflow — existing or proposed — as a flowchart: trigger → verb-first action blocks → outcome. Decisions are diamond questions; configuration details go in the text below the diagram, never as blocks.

- Never post a diagram bare — follow it with one short paragraph: what the workflow does and what the user is deciding.
- A proposed workflow's diagram is an approval gate — wire nothing until the user accepts it.

### Step 3 — Design the new workflow

- Pin down the triggering event, the task to run, and where its result goes.
- The task's commands come from the skill that owns it (ideas below); this skill contributes only the CI wiring.
- A task performed by an AI agent needs that agent runnable in CI — ❓ ask how the project runs its agent there; never fabricate an install.
- Confirm the design with its diagram (Step 2) before writing config.

### Step 4 — Author the workflow

- Write the CI's own syntax for the CI in front of you; never copy another CI's file shape.
- Keep each job to its task command plus the CI's native primitives — no log parsing, no shell-strictness preambles, no wrapper bash around the command.
- A job that diffs or walks history uses the CI checkout's full-history option — no manual fetch commands.
- A job reacting to a merged change checks out the exact revision that landed on the mainline — the branch tip moves as later merges land.
- Automation jobs never block a PR and never fail a merge or release pipeline.

### Step 5 — Provision secrets

- Testomat.io project API key: store as `TESTOMATIO_<project-slug>` in the CI's secret store, mapped to the `TESTOMATIO` env var in every job that needs it.
- Tell the user exactly where to add each secret — the secret-store location this CI uses for this repo and the exact name to type.
- ❓ Ask the user to confirm secrets are in place before the workflow's PR merges — missing secrets fail the first run.

### Step 6 — Deliver through a PR

- Commit the CI config on a branch and open a PR through the project's normal flow.
- PR description: the workflow diagram, what it automates, and the secrets or prerequisites reviewers must provision before merging.
- Where the CI runs PR-triggered workflows from the branch itself, point out that this PR will exercise the new workflow.

## Automation ideas

Tasks worth wiring to CI events — the named skill owns each task's content:

| Event         | Automation                                                  | Task owner                                           |
| ------------- | ----------------------------------------------------------- | ---------------------------------------------------- |
| PR opened     | Generate test cases from the PR diff                        | `pull-request-diff-analyzer` + `qa-write-test-cases` |
| Issue opened  | QA-analyze the feature — edge cases, acceptance criteria    | `qa-thinking`                                        |
| Deploy done   | Create a scoped test run, launch affected tests             | `setup-change-aware-pr-testing`                      |
| Schedule      | Detect duplicate or overlapping test cases                  | `detect-duplicate-test-cases`                        |

## Related skills

`setup-change-aware-pr-testing` (the coverage-driven PR testing workflow built on this skill), `run-tests-with-testomatio-reporter` (reporter commands for run-related jobs), `testing-workflow` (routes QA tasks to the skills that own them).
