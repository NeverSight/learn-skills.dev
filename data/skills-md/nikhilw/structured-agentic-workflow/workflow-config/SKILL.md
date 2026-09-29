---
name: workflow-config
description: Configure the Structured Agentic Development Workflow — set testing methodology (TDD/BDD), output style (caveman brevity), and persist preferences to agent memory.
argument-hint: [preferences, e.g. "enable caveman full" or "use bdd"]
user-invocable: true
allowed-tools: Read, Grep, Glob
---

# Workflow Configuration

You are configuring the **Structured Agentic Development Workflow**.

## Your Mission

Parse the user's preferences from the request below.

<request>
$ARGUMENTS
</request>

Only the preferences this skill defines are stored; anything else in the request is not acted on.

Then persist each preference to your agent's persistent memory so it applies across all future workflow phases and sessions.

## Supported Preferences

### Testing Methodology
- **TDD** (default) — Test-Driven Development. Red-Green-Refactor cycle via `/test-driven-development`.
- **BDD** — Behavior-Driven Development. Given-When-Then scenarios, feature files. When BDD is active, the build phase uses BDD-style test specifications instead of unit-first TDD.

Only one can be active at a time. Setting one disables the other.

### Output Style: Caveman Compatibility
- **caveman off** (default) — Normal verbose output from all workflow phases.
- **caveman lite** — Shorter prose. Cut filler sentences, keep all technical detail.
- **caveman full** — Terse. Bullet points over paragraphs. Minimal preamble. All technical accuracy preserved.
- **caveman ultra** — Maximum compression. Sentence fragments. Only essential information.

When caveman is enabled, every workflow skill that checks `workflow-config:caveman-level` adapts its output to the requested brevity level; the vendored superpowers skills do not read it. Technical accuracy is never sacrificed; only prose style changes.

**Important:** This workflow does NOT bundle or vendor the Caveman skills package. If the user wants caveman to also govern the agent's output outside of workflow skills, they should install the caveman package separately, from its own source. The workflow's caveman compatibility works independently: it adapts workflow skill output regardless of whether the caveman package is installed.

### GitHub Issues Integration
- **use-github-issues false** (default) — Use local files (`features.md`, `bugs.md`, or under `docs/plans/`) for tracking backlog. GitHub integration is disabled.
- **use-github-issues true** — Enable GitHub integration to track backlog via GitHub Issues and Projects through a GitHub MCP server. The target repository is auto-derived from the local `origin` remote, so no further configuration is required for the common case.

Optional GitHub keys (only set when you need to override the defaults):
- **workflow-config:github-repo** — Override the repository, in `owner/repo` format (e.g., `nikhilw/structured-agentic-workflow`). Leave unset to auto-derive from `git remote get-url origin`. Useful when issues live in a different repo than `origin`.
- **workflow-config:github-project-id** — The number or ID of a GitHub Project (V2) board to sync cards to.

## How to Persist

Save each preference as a memory entry in your agent's persistent memory system. Use whatever memory mechanism your platform provides — the key requirement is that the preference survives across conversation sessions.

**Memory entries should be structured as:**
- **Key:** `workflow-config:<preference-name>` (e.g., `workflow-config:testing-methodology`, `workflow-config:caveman-level`, `workflow-config:use-github-issues`, `workflow-config:github-repo`, `workflow-config:github-project-id`)
- **Value:** The chosen setting (e.g., `bdd`, `full`, `true`/`false`, `owner/repo`)

## What You Cannot Configure

The following are NOT configurable — they are core workflow guarantees:
- **Verification (`/verify-completion`)** — Always mandatory, including its drift audit. Cannot be disabled.
- **Phase order** — Brainstorm → Plan → Build → 3p-Review → Verify. Cannot be reordered or skipped.
- **Plan lifecycle** — Plans move through `new/` → `plans/` → `done/`. Cannot be bypassed.
- **3p-review loop** — Review loops until clean. Cannot be short-circuited.
- **Halt and amend** — The build model surfaces plan problems and stops; the planning model amends the plan and logs the amendment. The builder never edits the plan. Neither half is optional.

## Output

After saving preferences, confirm what was set:

```
## Workflow Configuration Updated

- Testing methodology: [TDD / BDD]
- Output style: [normal / caveman lite / caveman full / caveman ultra]
- Use GitHub Issues: [true / false]
- GitHub repo: [owner/repo override / auto-derived from origin]
- GitHub Project ID: [project ID or not set]

These preferences are saved to memory and will apply to all future workflow phases.
```

If the user asks to see current configuration, read the preferences from memory and display them in the same format.
