---
name: chrisai-knowledge
description: Install, repair, or update a project-root `.agents` operating surface with lossless document workflows and validation, optionally installing MCP publishing when the user requests access from other projects.
license: MIT
---

# ChrisAI Knowledge

## Purpose

Use this skill to install, repair, or update the local operating surface for a project root `.agents/` folder. This skill maintains the rule files, workflows, references used by those workflows, and deterministic helper scripts; it does not directly author Accepted Reusable Truth in `.agents/context/` or project resources in `.agents/resources/`.

This is the ChrisAI distribution of the Agent Workspace Rules surface. The installed `.agents` files intentionally keep `agent-workspace-rules` managed markers and reference filenames so repeated installs can refresh those managed sections safely.

## Installed Surface

The installer manages these target files:

- `.agents/AGENTS.md`: compact local operating contract.
- `.agents/TERMS.md`: managed glossary section plus room for project-specific terms.
- `.agents/workflows/agent-file-creation.md`: workflow for completing new Agent Documents before splitting and linking them.
- `.agents/workflows/agent-file-update.md`: workflow for loading, revising, and repartitioning existing Agent Documents without losing unaffected information.
- `.agents/workflows/agent-file-ingestion.md`: workflow for importing Source Material into complete Agent Documents while archiving vulnerable sources and referencing durable project sources in place.
- `.agents/workflows/context-initialization.md`: workflow for bootstrapping or substantially rebuilding `.agents/context/` from mixed project inputs.
- `.agents/workflows/spec-driven-development.md`: workflow for creating, researching, resolving gaps for, promoting context from, and freezing Spec Files.
- `.agents/workflows/spec-task-implementation.md`: workflow for planning and implementing tasks from Frozen Spec Files.
- `.agents/workflows/spec-task-acceptance.md`: workflow for planning, executing, evidencing, and reporting explicitly delegated acceptance of implemented spec tasks.
- `.agents/workflows/spec-grill-session.md`: optional workflow for resumable, lossless spec clarification sessions.
- `.agents/workflows/spec-user-journeys.md`: optional workflow for auditing human actors, actor states, features, applicable Use Cases, journey scenarios, and journey-driven Gaps before Freeze.
- `.agents/workflows/repair-zombie-reference-files.md`: workflow for repairing unowned Reference Files.
- `.agents/references/00001-agent-workspace-rules.md`: detailed rule reference used by AGENTS and workflows.
- `.agents/references/00002-intersection-points.md`: detailed scan points used by the ingestion workflow.
- `.agents/references/00003-reference-recovery-points.md`: detailed owner selection points used by the zombie Reference File repair workflow.
- `.agents/scripts/validate-agent-workspace.py`: deterministic validator for managed-surface completeness, line caps, reference naming, links, context-index routing, and zombie Reference Files.

The installer plans every target file before writing. If any conflict is found, it reports the conflict and writes nothing. It refreshes managed sections when markers already exist. It appends managed sections to existing `.agents/AGENTS.md` and `.agents/TERMS.md` when those files exist without markers, so user-authored content can remain outside the managed block.

## Install, Repair, Or Update

1. Identify the target project root. The Agent Workspace is `<project-root>/.agents`.
2. Run the installer in dry-run mode first:

```bash
python scripts/install_agent_workspace_rules.py --target /path/to/project
```

3. Apply the installer when the planned changes are correct:

```bash
python scripts/install_agent_workspace_rules.py --target /path/to/project --apply
```

4. If the installer reports conflicts, inspect the existing target files and merge the managed rule content manually instead of overwriting user-authored project content.
5. Run validation after installation or repair:

```bash
python scripts/validate_agent_workspace.py --target /path/to/project
```

After installation, the target project can also run:

```bash
python .agents/scripts/validate-agent-workspace.py
```

Use `python3` instead of `python` on systems where that is the Python 3 executable.

## Optional MCP Publishing

When the user explicitly requests serving this project's knowledge to other
projects through MCP, add `--with-mcp` to the installer dry run and apply:

```sh
python scripts/install_agent_workspace_rules.py --target /path/to/project --with-mcp
python scripts/install_agent_workspace_rules.py --target /path/to/project --with-mcp --apply
```

This installs `.agents/workflows/serve-kb.md` and the self-contained runtime
under `.agents/scripts/mcp/`. It records opt-in in `.agents/.knowledge-mcp.json`
so ordinary later repairs restore the enabled capability. Projects that have
not opted in receive no MCP workflow, runtime, or dependency installation.
Project configuration is preserved; modified runtime assets cause a conflict
instead of being overwritten. Deleting the runtime folder alone is not an
opt-out because the recorded feature remains repairable.

Read [Serve KB Workflow](assets/dot-agents/workflows/serve-kb.md) when configuring
or operating the publisher. It covers stdio and authenticated HTTP consumers,
exact JSONL snapshots, keyword/semantic/hybrid retrieval, embedding choices,
truth/proposal provenance, and recovery. The installed copy is the target
project's operational entrypoint. Dependencies, models, and generated data
are isolated inside the runtime folder; they are not Agent Documents.
New publisher configurations default to local `Xenova/all-MiniLM-L6-v2`
embeddings, with the pinned model downloaded on first indexing and cached for
reuse. Remote embeddings and keyword-only indexing remain explicit choices.
Search includes linked reference sections and owning passages by default,
preserving exact citations and authority in a deduplicated response. Resolved
links distinguish included, omitted, and unavailable context with callable
follow-ups. Compact responses are the default; full diagnostics are optional.
Embedding inputs include bounded title/heading context while source text stays
exact. Evidence tools share token budgets and explicit pagination. The bundled
evaluation helper measures retrieval and consumer answers against project-owned
fixtures; prose correctness still requires review.

Installing the capability does not automatically start a service or edit
consuming clients. If the user requests serving now, continue through the
installed workflow within that request. Preserve Markdown as authoritative;
indexing never accepts proposals or writes project knowledge.

## After Setup, Repair, Or Update

After installing, repairing, or updating a target `.agents/` workspace, tell the user what
changed, where to start, the validation result, and the recommended next step.
When several routes are plausible, include up to two useful alternatives. Do
not continue into context initialization, ingestion, spec work, or implementation
unless the user asks for that next step.

## Scope Rules

- Do not install `.agents/context/` content. Installed rules may describe how context should be used, but Accepted Reusable Truth must come from the target project and user-approved sources.
- Do not install `.agents/resources/` content. Installed rules may describe Resource Links and Raw Source preservation, but resource files are project-owned.
- Do not install or manage `.agents/skills/` content. Independently installed skill packages are tooling rather than project Agent Files, and the Agent Workspace validator excludes them from line-count and local-link checks.
- Treat fenced markdown in checked Agent Files as examples rather than live links. The Agent Workspace validator also excludes `.agents/workflows/` from local-link errors and warnings while allowing valid workflow links to establish Reference File ownership.
- Do not treat `.agents/resources/` as a mirror of the repository. Source code stays in its authoritative location and receives precise Source Provenance. Copy source code into `.agents/resources/` only when the user explicitly requests a source-code archive; never infer that permission from source location, durability, or deletion risk.
- Keep `.agents/TERMS.md` managed by section so future project-specific terms can be added outside the managed block.
- Keep references flat under `.agents/references/`; this skill installs only references used by `.agents/AGENTS.md` or `.agents/workflows/*`.

## Deterministic Validation

Run `scripts/validate_agent_workspace.py` for deterministic checks. It reports errors for hard-rule violations and warnings for preference-level or review-required issues. Read [Validator Checks](references/validator-checks.md) when interpreting output or deciding whether a rule can be checked mechanically.

The validator does not decide whether context content is truly Accepted Reusable Truth or whether an Agent Document retained all information through creation, ingestion, update, or splitting. Those require human review of the Source Material, the complete draft, and the final routed files.

## Bundled Resources

- `assets/dot-agents/`: templates installed into the target `.agents/` folder.
- `scripts/install_agent_workspace_rules.py`: dry-run or apply installer for managed rule files.
- `scripts/validate_agent_workspace.py`: deterministic checker installed into target `.agents/scripts/`.
- `references/validator-checks.md`: details of what the validator can and cannot prove.
