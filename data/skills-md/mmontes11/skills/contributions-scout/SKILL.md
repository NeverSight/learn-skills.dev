---
name: contributions-scout
description: >
  Scout a single open-source project for contributions likely to be merged. Investigate candidate
  contributions (open good-first-issue / help-wanted issues, low-risk docs / test / small-feature work,
  areas with a precedent of merged AI-authored PRs), prepare a high-level plan for the top candidate(s),
  evaluate feasibility (merge likelihood, effort, prerequisites, maintainer norms / CI expectations), and
  post the result as a comment on the Multica sub-issue that scopes the project. Use whenever a sub-issue
  asks to "investigate potential contributions" in one project, or to "scout <owner/repo> for
  contributions". Investigation and planning only — never fork the repo, make code changes, or open a PR.
license: Apache-2.0
metadata:
  author: mmontes11
  version: "1.0"
compatibility: Requires the multica CLI and read access to the scoping sub-issue, plus GitHub access (GitHub MCP tools and the authenticated gh CLI) to the target repository. Investigation only — no forks, no code changes, no PRs.
allowed-tools: Read, Grep, Bash(multica:*), Bash(gh:*)
---

# Scout a project for contributions

One project per run. The run's **Multica sub-issue** names the project (owner/repo) and scopes the work.
The deliverable is a single comment on that sub-issue.

## Scope

- **In:** investigate candidate contributions likely to be merged; prepare a high-level plan for the top
  candidate(s); evaluate feasibility.
- **Out (hard):** forking the repo, making the actual code changes, submitting the PR. Those happen
  afterwards, after the contribution has been confirmed.

## Tooling

**MCP-first, `gh` as fallback.** Use the GitHub MCP tools for what they cover (repo metadata, issue and
pull-request search, file contents, issue comment threads). Use `gh` for what MCP does not offer. Keep
responses bounded — read only the fields and threads the analysis needs; never JSON-dump whole API
responses into the conversation.

## Procedure

1. **Resolve the repo.** Confirm the project's current location — it may have been renamed or moved.
   Read its basic metadata (stars, language, `pushed_at`, `archived`). An archived repo has no viable
   contribution; say so and stop.
2. **Gather the signals.**
   - **Agent-facing docs** — `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md` at the root; any AI-PR policy in
     them or in the issue tracker, including a *no-fully-AI-generated-PR* policy (that makes the repo a
     near-zero for unattended agent work — record it, do not push on).
   - **Open `good first issue` / `help wanted` issues** — with labels, age, assignees, in-thread
     maintainer intent, and any competing PR.
   - **Low-risk surface candidates** — docs gaps, test-only work, small self-contained fixes surfaced in
     the tracker.
   - **Precedent** — merged AI-authored PRs (AI co-author: Claude, Codex, Copilot) in that repo.
   - **Friction** — DCO vs CLA, CI expectations, review norms, merge cadence.
3. **Shortlist candidates.** Prefer, in order: maintainer-endorsed (GFI / help-wanted / explicit
   in-thread ask or pre-approval); low-risk surface (docs / test-only / small self-contained fix);
   specificity (names files/behavior, reproducible); no competing PR or assignee.
4. **Plan the top candidate(s).** For each: approach, files/area touched, size (XS/S/M), effort
   estimate.
5. **Evaluate feasibility.** Likelihood of being merged, prerequisites, maintainer norms / CI
   expectations, and any blocker (CLA, strict AI-contribution policy, already claimed). Cross-check the
   evidence against the `#contribution-scoring` rubric of the
   [mmontes11/contributions](https://github.com/mmontes11/contributions) README so a later ranking pass
   can score the pick directly.
6. **Post the deliverable comment** on the sub-issue (`multica issue comment add <sub-issue-id>
   --content-file <path>`). It must carry:
   - The shortlisted candidates, each linked (issue/PR URL) with one line of why.
   - The **top pick** with its high-level plan (approach, files/area, size, effort).
   - The **feasibility read**: merge likelihood, prerequisites, maintainer norms / CI, blockers — and
     the evidence mapped to the `#contribution-scoring` signals.
   - A closing line: **no fork or PR was opened in this pass — investigation and planning only.**
7. **Close out.** Set the sub-issue status per the platform workflow once the deliverable is posted.
