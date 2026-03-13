---
name: pma
description: Project development lifecycle management with a strict three-phase workflow (investigate -> proposal -> implement), file-based plan tracking in docs/plan/, task tracking in docs/task/, and claim-before-work multi-agent coordination. Use when handling feature development, bug fixes, refactors, planning, progress tracking, or multi-agent execution in an existing codebase. Supports English and Chinese project templates.
---

# PMA - Project Management Assistant

Run delivery work with clear gates, minimal diffs, and explicit task/plan tracking.

## Hard Rules

1. Use one project content language for docs, task files, and commit messages (follow user preference, otherwise follow existing project language).
2. Read before write: inspect call chains, related config/tests, and recent changelog context before editing logic.
3. Make only the minimal requested changes; do not add unrequested refactors or features.
4. Never use plan mode (`EnterPlanMode`, `mode: "plan"`). Manage plans in `docs/plan/` files only.
5. Do not implement before explicit confirmation (`proceed`).
6. Use English filenames only, even when project content is Chinese (for example: `architecture.md`, `changelog.md`).

## Three-Phase Workflow

### Phase 1: Investigation

1. Trace upstream/downstream call chains, symbol references, and types.
2. Search related code, config, tests, migrations, and docs.
3. Read the tail of `docs/changelog.md` for recent context.
4. Find or create the matching task in `docs/task/index.md` and claim it (`[-]`).

Non-trivial task rule:
- If the change touches `>=3` files or crosses modules, create `docs/plan/PLAN-NNN.md` and write findings to the context section.

### Phase 2: Proposal

Output these items, then stop for approval:
- Current state
- Proposal
- Risks
- Scope
- Alternatives (if multiple approaches exist)

For non-trivial tasks:
- Complete remaining sections in `PLAN-NNN.md`.
- Append one line to `docs/plan/index.md` with `[ ]`.
- Wait for user annotations and address all of them before implementation.

### Phase 3: Implement -> Verify -> Record

Only after approval:

1. If a plan exists, set plan index marker to `[-]` and detail `status` to `implementing`.
2. Implement step by step according to the approved proposal.
3. Run focused self-verification.
4. Set task index marker to `[x]` and task detail `status` to `completed`.
5. If a plan exists, set plan index marker to `[x]` and plan detail `status` to `completed`.
6. Update changelog as needed.

## Task and Plan Files

Use these canonical references instead of redefining formats in-place:

- Task format: [docs/task-format.md](docs/task-format.md)
- Plan format: [docs/plan-format.md](docs/plan-format.md)

Required structure:

- `docs/task/index.md`: one-line task entries
- `docs/task/PREFIX-NNN.md`: task detail files
- `docs/plan/index.md`: one-line plan entries
- `docs/plan/PLAN-NNN.md`: plan detail files

## Claim-Before-Work (Multi-Agent Safety)

Before writing any implementation code:

1. Read `docs/task/index.md`; for `[-]` items, read detail `owner`.
2. If another agent owns the in-progress task, skip it.
3. Claim atomically:
   - Update task index `[ ] -> [-]`
   - Update task detail `status -> in_progress`, set `owner`
   - Call `TaskUpdate(status: "in_progress", owner: "<agent>")` if task tools are available
4. Start implementation only after the claim is fully written.

On completion:
- Set task index `[-] -> [x]`
- Set task detail `status -> completed`
- Call `TaskUpdate(status: "completed")` if task tools are available

On close/won't do:
- Set task index to `[~]`
- Set task detail `status -> closed` and record reason
- Call `TaskUpdate(status: "deleted")` if task tools are available

## Sync Rules

Task status updates are immediate, never deferred.

- Primary source is files in `docs/task/` and `docs/plan/`.
- If `TaskCreate`/`TaskUpdate` tools are available, keep tool state in sync with file state.
- If task tools are unavailable, continue with file-only sync and state this in the progress update.

Session checklist:
1. Session start: read `docs/task/index.md`, active task details, and `docs/plan/index.md`.
2. New task: create detail file first, then append index line.
3. Before work: complete Claim-Before-Work.
4. Session end: verify statuses are written and update index header date.

## Documentation System

Canonical structure:

```text
docs/
├── task/
│   ├── index.md
│   └── PREFIX-NNN.md
├── plan/
│   ├── index.md
│   └── PLAN-NNN.md
├── architecture.md
└── changelog.md
```

- Use English sections for English-language projects.
- Use Chinese template sections for Chinese-language projects while keeping filenames in English.
- Write investigation findings into the plan context section.
- Do not create extra report files; temporary files go to `./tmp/`.

## Changelog Conventions

Entry format:

```markdown
## YYYY-MM-DD HH:MM [tag]

[content]
```

Recommended tags:
- `[progress]`, `[BUG-P0]`, `[BUG-P1]`, `[pitfall]`, `[decision]`

## Project Initialization

On first use in a project:

1. Ensure `CLAUDE.md` contains a `## Project Development` section that references `/pma` and the three-phase workflow.
2. Ensure `AGENTS.md` contains the same section.
3. Ensure `docs/task/index.md` exists (initialize from [docs/task-format.md](docs/task-format.md)).
4. Ensure `docs/plan/index.md` exists (initialize from [docs/plan-format.md](docs/plan-format.md)).
5. Ensure core docs exist (`architecture.md` + `changelog.md`), and keep content language aligned with the project.

## Tools and Security

- Prefer semantic code navigation tools for architecture understanding.
- Check official docs (e.g., Context7) before using third-party APIs.
- Use code/web search tools for examples and troubleshooting when needed.
- Verify UI behavior after UI edits.
- Keep secrets in `.env`; never hardcode or log secrets.
- Mark risky commands with an explicit warning comment.
