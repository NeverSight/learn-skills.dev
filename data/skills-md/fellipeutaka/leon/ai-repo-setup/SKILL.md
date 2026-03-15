---
name: ai-repo-setup
description: |
  Set up and optimize repositories for AI coding agents. Creates minimal AGENTS.md,
  CLAUDE.md symlink, docs/REQUIREMENTS.md, docs/BUSINESS-RULES.md, feedback loops,
  and deterministic enforcement (Claude Code hooks, OpenCode plugins). Use when user
  wants to make a repo AI-friendly, set up AGENTS.md/CLAUDE.md, document
  requirements/business rules for AI, add pre-commit hooks for AI workflows, or
  optimize codebase structure for coding agents.
---

# AI Repo Setup

Prepare a repository so AI coding agents can navigate, implement, and verify
changes with minimal friction.

**Core philosophy**: AI agents are new starters with no memory. Every session
starts fresh. The codebase itself — not documentation — is the primary context.
Only document what is undiscoverable and globally relevant.

## Inputs to gather (if missing)

- One-sentence project description (what does this project do?)
- Functional requirements (what the system should do)
- Non-functional requirements (performance, security, scalability constraints)
- Business rules (domain logic, validation rules, constraints)
- External issue tracker (Linear, Jira, GitHub Issues, ClickUp, etc.) — if used by the team
- Behavioral preferences for agents (see step 4 for what to ask)

## Workflow

### 1. Analyze existing repo

- Read `package.json`, config files, directory structure
- Identify tech stack, package manager, existing scripts
- Check for existing AGENTS.md, CLAUDE.md, docs/
- Note what's already discoverable from source (don't re-document it)

### 2. Create or convert `docs/REQUIREMENTS.md` and `docs/BUSINESS-RULES.md`

If these files already exist, ask the user whether to convert them to the
status-based format. Preserve all existing content — only restructure the format
and add status fields. If creating from scratch, interview user or extract from
existing code.

**Choose the correct template based on whether the team uses an external tracker:**

#### Solo mode (no external tracker)

Status lives in the doc. Single source of truth = docs.

```markdown
# Requirements

## Status Reference

| Status | Meaning |
|--------|---------|
| `draft` | Written but not yet reviewed — may be vague or incomplete |
| `refined` | Reviewed and clarified by user, ready to implement |
| `in-progress` | Actively being implemented by the agent |
| `implemented` | Code written by agent, awaiting user review |
| `verified` | User reviewed and approved — only the user sets this |
| `deferred` | Intentionally postponed, not abandoned |
| `cancelled` | No longer relevant, kept for historical context |

## Functional Requirements

### [Feature Area]

#### FR-001: [Requirement title]

- **Status**: `draft`
- **Description**: [What the system should do]
```

#### Team mode (external tracker: Linear, Jira, GitHub Issues, etc.)

No `**Status**:` field in docs — status lives in the tracker. Single source of
truth = tracker. The `**Issue**:` field links to the tracker item.

```markdown
# Requirements

## Functional Requirements

### [Feature Area]

#### FR-001: [Requirement title]

- **Issue**: (none yet)
- **Description**: [What the system should do]
```

When `**Issue**:` is `(none yet)`, the agent creates the issue in the tracker
and writes back the ID (e.g., `LINEAR-123`, `PROJ-42`, `#123`).

Structure for `docs/BUSINESS-RULES.md` (same pattern in both modes):

```markdown
# Business Rules

## [Domain Area]

### BR-001: [Rule name]

- **Status**: `draft`          ← solo mode
- **Issue**: (none yet)        ← team mode (use one, not both)
- **When**: [Trigger condition]
- **Then**: [Expected behavior]
- **Rationale**: [Why this rule exists]
```

Keep requirements specific, testable, and numbered for traceability.

#### Agent Workflow for Requirements & Business Rules

**Solo mode lifecycle:**

1. **Draft** — user or agent adds a new item with `status: draft`
2. **Refine** — agent clarifies until specific and testable; user confirms;
   status → `refined`
3. **Implement** — user asks agent to implement a specific ID; agent
   implements it and updates status → `implemented`
4. **Verify** — user reviews; if approved, status → `verified`; if rejected,
   status → `in-progress` with a note

The agent must never set status to `verified` — only the user does.
The agent must update status to `implemented` before closing a session.

**Team mode lifecycle (tracker integration):**

When bulk-creating issues from requirements, follow the pre-flight checklist and
patterns in [references/tracker-issue-patterns.md](references/tracker-issue-patterns.md).

When asked to implement a requirement:

1. **Check `**Issue**:` field**
   - If `(none yet)` → create an issue in the tracker via MCP (title =
     requirement title, description = requirement body), write back the ID
   - If an ID exists → query the tracker for current status before proceeding
2. **Check tracker status**
   - If `in-progress` (or equivalent) → **warn the user and stop**. Do not
     proceed silently. The user decides whether to continue, reassign, or skip.
   - Otherwise → transition to in-progress in the tracker, then implement
3. **After implementation** → transition tracker status to the equivalent of
   `implemented`/`done` (discover available statuses via MCP; infer the mapping
   — do not hardcode it)
4. **Never query all requirements at session start** — query only the specific
   item being worked on (lazy query)

### 3. Create context docs per deployment layer (if multi-layer project)

For projects with multiple independent layers (backend, frontend, mobile, etc.),
create per-layer context docs that track implementation status separately.

See [references/multi-layer-guide.md](references/multi-layer-guide.md) for the
full guide: directory structures, context doc rules, monorepo vs separate repo
layouts, and agent workflow with layered docs.

### 4. Generate minimal `AGENTS.md`

See [references/agents-md-guide.md](references/agents-md-guide.md) for full
principles.

The file must be **as small as possible**. Only include:

1. One-sentence project description
2. Pointers to docs/ with the sync rule (mandatory — without this, the status
   lifecycle is dead on arrival since agents start fresh every session)
3. Behavioral instructions (agent workflow preferences that are undiscoverable
   from source). Ask the user about **each** of these individually — do not
   collapse them into a single vague question:
   - **Plan mode**: "How should I present plans? Concise or detailed? Should I
     list unresolved questions at the end?"
   - **Communication style**: "Any preferences for brevity, formality, or
     language?"
   - **Docs lookup**: "Should I consult Context7 (or similar) for up-to-date
     library docs before writing code, instead of relying on training data?"
   - **Tracker integration**: "Does the team use an external issue tracker
     (Linear, Jira, GitHub Issues)? Should I create/sync issues automatically?"
   - **Workflow habits**: "Any recurring instructions you find yourself
     repeating across sessions? (e.g., commit style, test expectations)"

Example (single-layer project):

```markdown
# Project Name

SaaS platform for team retrospectives with real-time collaboration.

## Docs

- `docs/REQUIREMENTS.md` — functional and non-functional requirements
- `docs/BUSINESS-RULES.md` — domain rules and constraints

When implementing features or fixing bugs, update the relevant requirement/rule
status in these docs to keep them synced with the codebase.

## Docs Lookup

When implementing or fixing bugs involving external libraries, always consult
Context7 for up-to-date documentation before writing code. Never rely on
training data for library APIs.

## Plan Mode

- Make the plan extremely concise. Sacrifice grammar for the sake of concision.
- At the end of each plan, give me a list of unresolved questions to answer, if any.
```

For multi-layer projects, see the
[multi-layer guide](references/multi-layer-guide.md#agentsmd-example) for an
AGENTS.md example.

**Team mode addition** — if the team uses an external tracker, add a Tracker
section to AGENTS.md instead of a Docs sync rule:

```markdown
## Docs

- `docs/REQUIREMENTS.md` — functional and non-functional requirements
- `docs/BUSINESS-RULES.md` — domain rules and constraints

## Tracker

Issue tracker: Linear (MCP available in this session).

When implementing a requirement:
- If `**Issue**:` is `(none yet)`, create an issue and write back the ID.
- If an ID exists, query the tracker for current status before proceeding.
- If status is in-progress, warn the user and stop — do not proceed silently.
- Discover available statuses via MCP; infer the mapping — do not hardcode it.
- Never query all requirements at session start — query only what you're about to work on.

When bulk-creating issues from requirements, follow the pre-flight checklist in
`references/tracker-issue-patterns.md` before creating anything.
```

Replace `Linear` with the actual tracker. Remove the "MCP available" note if
the team doesn't use an MCP integration for that tracker.

**Do NOT include**: package manager (discoverable from lock files,
`packageManager` field in `package.json`, or enforcement hooks), commands
(discoverable from `package.json` scripts), architecture descriptions, file
listings, framework/library explanations, implementation patterns. These are all
discoverable from source.

### 5. Create `CLAUDE.md` symlink

```bash
ln -s AGENTS.md CLAUDE.md
```

This keeps Claude Code and other tools reading the same instructions.

### 6. Set up feedback loops (optional)

See [references/feedback-loops.md](references/feedback-loops.md) for details.

Ask user which feedback loops to set up:

- [ ] TypeScript `type-check` script in package.json
- [ ] Test runner (`vitest`, `jest`, `bun test`)
- [ ] E2E tests (`playwright`, `cypress`) — for frontend projects
- [ ] Pre-commit hooks: Lefthook (recommended) or Husky + lint-staged
- [ ] Code quality: Oxlint + Oxfmt (recommended), Biome, or ESLint + Prettier

Pre-commit hooks are the most powerful feedback loop for AI agents — they get
error messages on failed commits and retry automatically.

### 7. Set up deterministic enforcement (optional)

See [references/deterministic-enforcement.md](references/deterministic-enforcement.md)
for details.

Ask user which agent tools they use and set up enforcement for each:

- **Claude Code**: `PreToolUse` hooks in `.claude/settings.json` (bash scripts)
- **OpenCode**: plugins in `.opencode/plugins/` (TypeScript/JavaScript modules)

Ask about both tools — users may use one or both. Set up enforcement for every
tool the user opts into.

Common enforcement rules:

- Enforce correct package manager (block `npm`, `yarn`, `bun`, `deno` if using `pnpm`)
- Block dangerous git commands (`git push --force`, `git reset --hard`)
- Block specific CLI patterns
- Protect sensitive files (`.env`, credentials)

Enforcement saves instruction budget and is deterministic — rules cannot be
ignored by the agent. It also makes the package manager discoverable by agents
(they see the error message when blocked), which is why it doesn't need to be
in AGENTS.md.

## Deliverables

- [ ] `docs/REQUIREMENTS.md` — numbered functional + non-functional requirements (definitions only)
- [ ] `docs/BUSINESS-RULES.md` — numbered business rules with triggers/behavior (definitions only)
- [ ] `docs/[layer]/REQUIREMENTS.md` — per-layer status + implementation scope (if multi-layer)
- [ ] `docs/[layer]/BUSINESS-RULES.md` — per-layer enforcement status (if multi-layer)
- [ ] `AGENTS.md` — minimal, hand-crafted, globally relevant only
- [ ] `CLAUDE.md` — symlink to AGENTS.md
- [ ] Feedback loops configured (if opted in)
- [ ] Deterministic enforcement configured (if opted in)

## Anti-patterns to avoid

- **Bloated AGENTS.md** — every line costs tokens on every session
- **Documenting the discoverable** — agents read `package.json` scripts, lock
  files (`pnpm-lock.yaml`, `yarn.lock`, etc.), `packageManager` field, config
  files, and imports. Don't repeat what they'll find in seconds.
- **Listing package manager or commands** — discoverable from lock files,
  `packageManager` field in `package.json`, and enforcement hooks
- **File path references** — paths change; describe capabilities instead
- **Auto-generated init files** — stale immediately, actively mislead agents
- **Global rules for local concerns** — use progressive disclosure or skills instead
- **Missing docs sync rule** — without telling agents to update requirement/rule
  statuses, the entire lifecycle system is unused
- **Layer status in root docs** — when using layered docs, agents must not update
  the root doc status to reflect only their own layer's progress. Root status is
  aggregated (all layers done → root promoted). Updating it prematurely misleads
  other layers into thinking the feature is complete across the whole system.
- **Dual source of truth for status** — in team mode, never put `**Status**:`
  in docs alongside `**Issue**:`. The tracker is the single source of truth.
  Keeping both leads to divergence and confusion about which one is authoritative.
