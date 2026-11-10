---
name: init-project-orchestration
description: "Create or migrate project-level agents, repeatable project workflows, and planning state from one client-neutral contract, then render repository-scoped adapters for both Claude Code and Codex. Use when a research project needs role separation, project commands, formal phase tracking, or conversion from an existing Claude-only .claude/agents and .claude/commands setup."
---

# Initialize project orchestration

Create the project source once under `.ai/orchestration/`. Treat Claude Code
and Codex files as generated adapters, never as parallel authoring surfaces.

## Resulting structure

```text
.ai/orchestration/                 # canonical, client-neutral source
├── manifest.yaml
├── agents/<role>.md
└── commands/<workflow>.md

.claude/agents/project-<role>.md   # generated Claude agent
.claude/commands/project/<workflow>.md
.codex/agents/project-<role>.toml  # generated Codex agent
.agents/skills/project-<workflow>/SKILL.md
.planning/roadmap.md               # shared project state
.planning/state.md
```

Claude exposes a workflow as `/project:<workflow>`. Codex exposes the same
workflow as `$project-<workflow>`. Both adapters derive from the same neutral
command body. The namespace prevents collisions with global skills.

## Phase 1: Assess

1. Resolve the project root from the argument or current directory. Confirm it
   is the intended research project before searching elsewhere.
2. Read the active client's project guidance. Read neutral project facts from
   `AI.md`, `README.md`, `docs/`, and `.context/`; do not treat the sibling
   client's guidance file as an additional instruction set.
3. Read `.context/field-calibration.md`, project memory, and `.planning/` when
   present.
4. Classify the project:
   - experimental: data preparation and empirical estimation;
   - computational: software, algorithms, simulations, or experiments;
   - theoretical: formal models and proofs;
   - mixed: select roles and workflows from more than one preset.
5. Inventory existing neutral sources and generated adapters. Also inventory
   legacy non-generated `.claude/agents/` and `.claude/commands/` files.

Do not overwrite anything during assessment.

## Phase 2: Confirm the design

Read the applicable preset under `templates/presets/` and present:

- proposed project agents and their exact read/write boundaries;
- proposed project workflows and expected arguments;
- the initial `.planning/` phases;
- any legacy single-client Claude files that need reconciliation.

Ask for one confirmation covering additions, removals, names, and
project-specific standards. Agents implement; independent global agents review.

## Phase 3: Author neutral sources

1. Create `.ai/orchestration/manifest.yaml` from
   `templates/manifest-template.yaml`. Keep `namespace: project` unless an
   existing checked-in namespace would collide.
2. Create one neutral agent source per confirmed role using
   `templates/agent-template.md`.
3. Create one neutral command source per confirmed workflow using
   `templates/command-template.md`.
4. Always include `commands/update-state.md`, starting from
   `templates/update-state-command.md`.
5. Populate real project paths, standards, and ownership boundaries. Do not
   leave placeholders.

Canonical sources must not contain client-home paths, machine-absolute paths,
Claude/Codex adapter directories, or client-specific invocation syntax. Refer
to reusable global capabilities as “the `latex` skill”, for example.

### Agent policy

- Use `artifact_contract.mode: response-only` plus
  `write_policy.project: read-only` for an advisory agent.
- Use `artifact_contract.mode: project-write` plus
  `write_policy.project: scoped-write` for an implementation agent.
- Keep `write_policy.git: forbidden` unless the user explicitly authorizes Git
  mutation as part of that role.
- Declare behavioral `capabilities` and the minimum Claude adapter tools. Codex
  derives a read-only or workspace-write sandbox from the neutral write policy.
- Treat every `data/raw/` path as read-only.

## Phase 4: Reconcile an existing Claude project

If legacy project agents or commands exist:

1. Read every non-generated legacy file.
2. Convert its substantive behavior into the matching neutral source.
3. Replace client-bound guidance-file reads with “active client guidance” plus
   the relevant neutral project files.
4. Convert slash-skill calls to semantic skill references.
5. Preserve tool and write restrictions in neutral policy fields.
6. Compare the neutral source against the legacy file before rendering.

The renderer refuses to overwrite a non-generated target. Keep unmatched
legacy files in place and report them; never select one side silently.

## Phase 5: Render and verify

Resolve `scripts/project-orchestration.py` relative to this skill directory,
then run it through `uv`:

```bash
uv run <skill-root>/scripts/project-orchestration.py render --project <project-root>
uv run <skill-root>/scripts/project-orchestration.py check --project <project-root>
```

The renderer:

- validates the neutral schemas and portability constraints;
- writes both clients' adapters atomically;
- refuses symlinked parents and non-generated collisions;
- removes only stale files carrying its own generated marker;
- exits non-zero when `check` detects drift.

Never edit a generated adapter. Change `.ai/orchestration/` and render again.

## Phase 6: Planning and guidance pointers

Create `.planning/roadmap.md` and `.planning/state.md` from the bundled
templates only when they are absent. When they exist, merge deliberately and
preserve current decisions and progress.

Add a short pointer to each existing client guidance file without duplicating
the orchestration body:

- canonical project roles/workflows: `.ai/orchestration/`;
- shared phase state: `.planning/roadmap.md` and `.planning/state.md`;
- generated adapters for that client;
- rerender command.

Do not create or overwrite a large `CLAUDE.md` or `AGENTS.md` merely to install
orchestration. Shared project facts belong in neutral project documentation.

## Completion report

Report:

- neutral agent and workflow sources created or migrated;
- generated Claude and Codex adapter counts;
- planning files created, merged, or preserved;
- any legacy file still awaiting reconciliation;
- the exact renderer check result.

Do not commit or push unless the user separately requests it.
