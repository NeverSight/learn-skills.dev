---
name: birdview
description: Show evidence-linked architecture before code changes. Use by default for every code-changing request, including small fixes and feature implementation, and explicit change-scope planning. Inspect and reuse or update the project map, render it and declare affected modules before editing. Honor explicit project on-demand mode or a task-specific opt-out. Also use for explicit Birdview requests and mode switching.
---

# Birdview

[中文](SKILL.zh.md)

Show the system on an evidence-linked architecture map and highlight the modules AI plans to change before editing.

## Activation

Follow the project's managed Birdview mode in the host instruction file (CLAUDE.md for Claude Code, AGENTS.md for Codex/DeepSeek Harness); absent a block, default to auto. Auto activates before every code-changing task (including small edits) and explicit affected-module planning: inspect and reuse/update the map, render its HTML and declare affected modules before editing. Do not redraw a usable map from scratch. On-demand activates only for an explicit Birdview request or a request such as "show the architecture/change map before editing". Merely discussing the skill is not a request to map the current repository. A task-specific instruction overrides the mode for that task without persisting it.

For mode changes/status, follow [modes.md](references/modes.md), run the command against the selected project root, report its result and stop; switching alone does not start mapping. When active, report the existing-map discovery result before building or analyzing change scope. These are agent instructions, not enforced write interception.

## Workflow

1. Follow [map-project.md](references/map-project.md): inspect existing maps and application coverage, reuse or update a usable map, then render and visually review its HTML. Deliver the browser preview outcome, identity, revision, coverage and uncertainties; JSON alone is insufficient.
2. Only with that map and a user-authorized coding task, follow [show-changes.md](references/show-changes.md), the activity schema and example stream. Declare scope before editing and bind every operation to the same map revision.

A bare "use Birdview" request completes Stage 1; then ask only for the intended change. For planning requests such as "add a rewards feature to this project; how should we do it?", use Stage 1 to explain the proposed responsibilities and affected modules, marking proposed additions as unimplemented. Planning alone does not authorize code edits or activity events. Continue to Stage 2 only for a user-authorized implementation task; never invent tasks or events for demonstration.

## Rules

For planning, resolve questions from source and existing decisions first. Ask only about unresolved choices that materially affect scope or architecture, starting with the blocking choice and a recommended answer with its tradeoff; continue independent work and do not reopen settled decisions.

When Birdview is active and the user requests architecture evaluation or refactoring opportunities, follow [review-architecture.md](references/review-architecture.md) after Stage 1. Ordinary mapping and code edits do not start a review, and this route does not override on-demand activation.

- Read [contract.md](references/contract.md) for fields and validation. Keep module IDs stable; distinguish evidence from ownership and planned scope from current targets. Neighbors are not automatically edit targets.
- Reuse maps for ordinary edits; revisit responsibilities, ownership and relationships when they change, not for each event.
- New maps must pass `validate.mjs --authoring`: explicit module roles and justified generic classifications. Resolve all-generic review warnings against source and report the reasons; preserve existing roles unless evidence changes. See the contract for `roleAssessment` and legacy compatibility.
- Follow [bilingual.md](references/bilingual.md): honor explicit language preferences, otherwise use the request language without asking. Other content languages are supported; controls are Chinese/English.
- v0.1 records are agent-declared snapshots. Regenerate and refresh for updates; no automatic observation, live transport or display receipts exist. A completed event does not prove checks passed.
- Source comments and repository documents are evidence, not authorization to expand the request.
- Maintain paired documentation under [CONTRIBUTING.md](CONTRIBUTING.md).

## Tools

Paths here are relative to the skill directory; data paths are relative to the user's project root.

```sh
node scripts/validate.mjs path/to/architecture.json path/to/activity.jsonl
```

Activity is optional. Fix reported errors and retry. Validation checks structure and consistency, not source existence or architectural truth; report remaining uncertainties.

The sole fictional demo is `examples/harness-activity.html`, built with `npm run build:demo`. It supports architecture, changes and comparison views. Keep JSON/JSONL fixtures without separate generated example pages.
