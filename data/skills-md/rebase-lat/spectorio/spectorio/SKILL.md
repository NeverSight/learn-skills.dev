---
name: spectorio
description: Trap-aware spec-driven development workflow (OpenSpec fork) — use when planning, specifying, or implementing a multi-step change with proposal/specs/design/tasks artifacts, or when the user mentions spectorio, change proposal, delta specs, or spec-driven development.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  workflow: proposal → specs/design → tasks → apply, with optional explore, verify, sync, archive
---

# Spectorio

Spec-driven development fork of OpenSpec with metacognitive-trap guardrails baked in.
The workflow lives in these skill files; read project files directly. A small CLI
delivers setup only (commands + workspace bootstrap) — it never plans or codes.

## Behavior

Act as the expert developer/product owner defined in `references/persona.md`
(workspace `spectorio/references/persona.md` once it exists): precise,
scope-disciplined, evidence-backed, concise. Persona governs voice and judgment;
workflow rules govern procedure.

## When to Use

- User asks to plan, spec, or implement a non-trivial change (feature, refactor, migration).
- User mentions `spectorio`, change proposal, delta specs, EARS requirements, or spec-driven development.
- Do NOT activate for trivia, single-line fixes, or pure Q&A — just do the work.

## Core Loop

```
onboard (once, then amend as the stack evolves) → propose → apply → archive
                  optional: explore first · verify before archive · sync before archive
```

0. **Bootstrap** (first run in a project — skip if `spectorio/` exists): the
    project is missing its workspace, so set it up before anything else.
    Execute this from the project root instead of quoting it:

    ```bash
    npx -y @rebase-lat/spectorio@latest init --tools <this-agent>
    ```

    `<this-agent>` is `opencode`, `claude`, or `cursor` for the agent you are
    running in (default to all three when unsure). If shell access is denied, quote
    the command and stop — tell the user to run it in a terminal and re-invoke
    afterwards. Otherwise confirm `spectorio/onboarding.md` exists. If npx/registry is unavailable, fall back to materializing
    the workspace from this bundle (see `references/new.md` §0), and if command
    wrappers are missing, copy them from the `spectorio-new` skill payload.
    Newly installed slash-commands need an IDE restart to appear — say so, then
    continue with onboarding (step 1) in this session regardless.
1. **Onboard**: run a live Q&A session (`references/onboard.md` Flow A) to fill `spectorio/onboarding.md` — one topic at a time, versions pinned, vague answers challenged, gate boxes closed by explicit YES. It stays living: stack changes go through the amend flow (`references/onboard.md` Flow B), never silent edits. Every spec re-uses these rules instead of re-litigating them.
2. **Propose**: scaffold `spectorio/changes/<kebab-name>/` (see `references/new.md`), then draft planning artifacts in dependency order (see `references/workflow.md`). Vague/risky request? Explore first via the `motion` artifact (3-agent synthesis, human picks direction). New dep mid-planning? Amend onboarding first (`references/onboard.md` flow B), then resume.
3. **Apply**: implement `tasks.md` top-to-bottom with pause-and-ask guardrails (see `references/apply.md`).
4. **Archive**: validate → sync deltas → changelog → move folder (see `references/archive.md`).

## Rules That Are Always On

- **Planning only means planning only** — never edit project code while drafting proposal/specs/design/tasks/update. Wait for an explicit apply request.
- **Requires are enablers, not gates** — `proposal → specs/design (either order) → tasks`. Skipped steps are recorded with reason, never silently.
- **Never silently narrow scope** — unclear task, design issue, scope creep, or urge to simplify specified behavior → surface and ask. Queue out-of-scope ideas to `verification.md`.
- **Specs describe behavior, not implementation** (see `references/conventions.md` §2).
- **Design is stack-bound** — only libraries pinned in `onboarding.md`; new dep → update onboarding FIRST.
- **Default is warn-and-confirm**; per-change `.spectorio.yaml` flags opt into strictness (see `references/conventions.md` §6).

## References (progressive disclosure — load as needed)

This router skill carries the full workflow reference. Each step is also an
installable skill with slash-command wrappers (single-source `commands/` via `npx @rebase-lat/spectorio init`):

| Skill | Command (opencode/cursor) | Command (claude) | Contents |
| ----- | ------------------------- | ---------------- | -------- |
| `spectorio-new` | `/spectorio-new` | `/spectorio:new` | Workspace bootstrap + scaffolding a change + `.spectorio.yaml` flags |
| `spectorio-discover` | `/spectorio-discover` | `/spectorio:discover` | Chart a module's behavior into living specs + interview, then offer motion/propose |
| `spectorio-status` | `/spectorio-status` | `/spectorio:status` | Answer "now what?" — scan changes, report state/staleness, recommend next step |
| `spectorio-onboard` | `/spectorio-onboard` | `/spectorio:onboard` | Onboarding init + amend flows |
| `spectorio-motion` | `/spectorio-motion` | `/spectorio:motion` | Optional explore (3-agent synthesis, human picks direction) |
| `spectorio-propose` | `/spectorio-propose` | `/spectorio:propose` | Artifact DAG, status checklist, how to create the next artifact |
| `spectorio-validate` | `/spectorio-validate` | `/spectorio:validate` | Structural checks (block apply/archive on error) |
| `spectorio-apply` | `/spectorio-apply` | `/spectorio:apply` | Implementation guardrails |
| `spectorio-verify` | `/spectorio-verify` | `/spectorio:verify` | Spec-match + Clean Code audit + refactor-vs-patch + learning check |
| `spectorio-update` | `/spectorio-update` | `/spectorio:update` | Revising planning artifacts, any direction |
| `spectorio-sync` | `/spectorio-sync` | `/spectorio:sync` | Merging deltas into living specs |
| `spectorio-archive` | `/spectorio-archive` | `/spectorio:archive` | Changelog + archive move |

Detail files (this bundle only — verb skills read the workspace copies post-bootstrap):

| File                       | Contents                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------ |
| `references/conventions.md`| Central base: naming, requirements/scenarios, delta ops, tasks, checklist, flags, paths         |
| `references/persona.md`    | Voice: expert developer/product owner — engineering, ownership, communication                    |
| `references/workflow.md`   | Artifact DAG, status checklist, how to create the next artifact                                  |
| `references/onboard.md`    | Onboarding init + amend flows                                                                    |
| `references/motion.md`     | Optional explore (3-agent synthesis, human picks direction)                                      |
| `references/propose.md`    | Artifact creation order, per-artifact essentials                                                 |
| `references/new.md`        | Workspace bootstrap + scaffolding a change + `.spectorio.yaml` flags                            |
| `references/validate.md`   | Structural checks (block apply/archive on error)                                                 |
| `references/apply.md`      | Implementation guardrails                                                                        |
| `references/update.md`     | Revising planning artifacts, any direction                                                       |
| `references/sync.md`       | Merging deltas into living specs                                                                 |
| `references/archive.md`    | Changelog + archive move                                                                         |
| `references/verify.md`     | Spec-match + Clean Code audit + refactor-vs-patch                                                |
| `references/discover.md`   | Chart a module into living specs + interview, then offer motion/propose                          |
| `references/status.md`     | Workspace scan, staleness signals, recommended next step                                         |
| `references/templates/`    | Artifact templates (proposal, delta spec, design, tasks, motion, verification, learning, update, changelog) |
| `references/schema/`       | `spectorio-workflow.yaml` (DAG + instructions) — copied to `spectorio/schemas/` at bootstrap    |
| `references/onboarding.md` | Project constitution template                                                                    |
| `references/principles/`   | `clean-code-principles.md`, `spec-driven-development.md`, `metacognitive-traps.md`               |
| `references/examples/`     | `main-spec.md` — what a merged living spec looks like                                             |

After bootstrap, `spectorio/` paths in this skill resolve against the project workspace
(`spectorio/schemas/`, `spectorio/changes/_template/`, `spectorio/onboarding.md`,
`spectorio/references/` — the user-editable guidelines copy); the `references/`
copies are the portable seeds — prefer the workspace copies once they exist.
