---
name: octivi-bash-boilerplate
description: Create, refactor, and migrate Bash scripts with Octivi Bash Boilerplate (OBB) using marker blocks (`# >>> OBB:BEGIN ...` / `# <<< OBB:END`). Use when selecting `header` vs `full` integration, copying ready templates, updating marker blocks, and validating script quality with deterministic checks.
---

# Octivi Bash Boilerplate

Use this skill for any Bash script task that should follow OBB conventions.

## Inputs Required

- Script intent and lifecycle (throwaway helper vs maintained CLI).
- CLI contract: required/optional flags, positional args, env vars.
- Output contract: stdout/stderr format, exit codes.
- Side effects: files, network, permissions, cleanup requirements.

If any of these are missing, infer minimally and state assumptions.

## Decision Table

Choose exactly one mode per script:

| Mode            | Use when                                                        | Tradeoff                                  |
| --------------- | --------------------------------------------------------------- | ----------------------------------------- |
| `header`        | Small scripts; strict mode + basic constants are enough         | Few helpers, more manual utilities        |
| `full-source`   | Medium/large scripts; you can rely on external OBB library path | Cleaner file, external runtime dependency |
| `full-embedded` | Medium/large scripts; self-contained delivery required          | Bigger file, embedded generated block     |

## Execution Steps

1. Read `references/workflow.md` and apply the flow for new/refactor/migration.
2. Copy one ready template to destination:
   `cp skills/octivi-bash-boilerplate/assets/templates/<header-only-script|full-obb-script-source|full-obb-script-embedded> ./script.sh`.
3. Implement business logic outside OBB marker blocks.
4. If a marker block is unpopulated or stale, run:
   `octivi-bash-boilerplate-update <script>`.
5. Run quality gates from `references/checklist.md` and resolve all required failures.

## Output Contract

The final response must include:

- Selected mode and short rationale.
- What changed (CLI, behavior, compatibility expectations).
- Commands executed for validation.
- Residual risks and follow-up actions, if any.

## Template Source Of Truth

- Canonical OBB scripts live at repository root:
  - `octivi-bash-boilerplate`
  - `octivi-bash-boilerplate-header`
  - `octivi-bash-boilerplate-update`
- Do not edit `assets/templates/*` marker payloads manually; regenerate with:
  `scripts/generate-skill-templates`.

## Reference Loading Strategy

- Primary workflow: `references/workflow.md`.
- Final gate and pass/fail rules: `references/checklist.md`.

## Non-negotiable rules

- Keep marker syntax exact:
  `# >>> OBB:BEGIN variant=header|full` and `# <<< OBB:END`.
- Keep all business logic outside OBB marker blocks.
- For full embedded mode, keep `variant=full` marker block at end of script.
- Never source `octivi-bash-boilerplate-header` as a library file.
- Use one template variant per script and avoid mixing integration styles.
