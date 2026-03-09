---
name: project-docs-maintainer
description: Maintain `*-skills` README standards and checklist-style roadmap docs through one canonical maintenance entrypoint. Use when a repo needs profile-aware README maintenance, checklist roadmap validation or migration, or a bounded audit-first doc workflow with Markdown and JSON reporting.
---

# Project Docs Maintainer

Use one canonical skill entrypoint for documentation maintenance, then choose the matching mode.

## Inputs

- `mode=skills_readme_maintenance`
  - Required: `--workspace <path>`
  - Optional: `--repo-glob <glob>`, repeatable `--exclude <path>`, `--apply-fixes`
- `mode=roadmap_maintenance`
  - Required: `--project-root <path>`, `--run-mode <check-only|apply>`
  - Optional: `--roadmap-path <path>`
- Use canonical mode names in all new prompts.
- Treat `skills_readme_alignment` as compatibility-only.

## Workflow

1. Pick the canonical `mode` from the user request.
2. Run the read-only variant first:
   - `skills_readme_maintenance`: audit first
   - `roadmap_maintenance`: `--run-mode check-only` first
3. Review findings and keep the fix scope bounded to the selected mode.
4. If the user requested edits, run the corresponding bounded write path:
   - `skills_readme_maintenance`: `--apply-fixes`
   - `roadmap_maintenance`: `--run-mode apply`
5. Re-run the same mode to confirm remaining issues.
6. Return the mode-specific Markdown and JSON report shape.

### `skills_readme_maintenance`

- Script: `scripts/skills_readme_maintenance.py`
- Scope: `README.md` maintenance for `*-skills` repositories
- References:
  - `references/output-contract.md`
  - `references/section-schema.md`
  - `references/discoverability-rules.md`
  - `references/profile-model.md`

### `roadmap_maintenance`

- Script: `scripts/roadmap_alignment_maintainer.py`
- Scope: checklist-style `ROADMAP.md` validation, migration, and bounded normalization
- References:
  - `references/roadmap-customization.md`
  - `references/roadmap-config-schema.md`

## Output Contract

- `skills_readme_maintenance`
  - Return Markdown plus JSON with:
    - `run_context`
    - `repos_scanned`
    - `profile_assignments`
    - `schema_violations`
    - `command_integrity_issues`
    - `fixes_applied`
    - `post_fix_status`
    - `errors`
  - If there are no issues and no errors, output exactly `No findings.`
- `roadmap_maintenance`
  - Return Markdown plus JSON with:
    - `run_context`
    - `findings`
    - `apply_actions`
    - `errors`
  - If there are no findings, no apply actions, and no errors, output exactly `No findings.`

## Guardrails

- Never auto-commit, auto-push, or open a PR.
- Never edit source code, manifests, lockfiles, or CI files.
- In `skills_readme_maintenance`, keep edits bounded to `README.md` and explicitly approved snippet insertions into `AGENTS.md`.
- In `roadmap_maintenance`, `apply` mode may edit only the target `ROADMAP.md`.
- Keep deprecated aliases out of the main path and mention them only when handling legacy prompts.

## References

- `references/output-contract.md`
- `references/skills-readme-maintenance-automation-prompts.md`
- `references/roadmap-automation-prompts.md`
- `references/profile-model.md`
- `references/section-schema.md`
- `references/discoverability-rules.md`
- `references/fix-policies.md`
- `references/roadmap-customization.md`
- `references/roadmap-config-schema.md`
