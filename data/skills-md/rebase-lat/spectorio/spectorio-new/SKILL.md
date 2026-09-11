---
name: spectorio-new
description: Bootstrap the spectorio workspace and scaffold a new change. Use when starting work in a project with no spectorio/ folder, or when the user says new change, scaffold, bootstrap, or init spectorio.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  part-of: spectorio workflow (step 1 of propose → apply → archive)
---

# Spectorio New — Bootstrap + Scaffold

Scaffold-only. Planning only — never edit project code.

## 0. Workspace init (first run in a project — skip if `spectorio/` exists)

Preferred: run the published CLI from the project root. Execute it now
instead of quoting it:

```bash
npx -y @rebase-lat/spectorio@latest init --tools <this-agent>
```

`<this-agent>` is the agent you are running in (`opencode`, `claude`, or `cursor`).
If shell access is denied, quote the command and stop — tell the user to run it
in a terminal and re-invoke this skill afterwards. Otherwise verify the workspace
files exist before continuing.

Fallback when npx/registry is unavailable — bootstrap from this bundle
(`SKILL_DIR` = this installed `spectorio-new/` skill directory):

```bash
mkdir -p spectorio/schemas spectorio/specs spectorio/archive spectorio/changes/_template/specs/_example-domain
cp SKILL_DIR/onboarding.md spectorio/onboarding.md
cp SKILL_DIR/schema/spectorio-workflow.yaml spectorio/schemas/
cp SKILL_DIR/templates/motion.md spectorio/changes/_template/motion.md
cp SKILL_DIR/templates/proposal.md spectorio/changes/_template/proposal.md
cp SKILL_DIR/templates/design.md spectorio/changes/_template/design.md
cp SKILL_DIR/templates/tasks.md spectorio/changes/_template/tasks.md
cp SKILL_DIR/templates/verification.md spectorio/changes/_template/verification.md
cp SKILL_DIR/templates/learning.md spectorio/changes/_template/learning.md
cp SKILL_DIR/templates/update.md spectorio/changes/_template/update.md
cp SKILL_DIR/templates/delta-spec.md spectorio/changes/_template/specs/_example-domain/spec.md
cp SKILL_DIR/templates/changelog.md spectorio/archive/changelog.md
```

If this skill was installed without its `templates/` payload (single-skill
install), fall back to the `spectorio` router skill's `references/templates/`
copies, or ask the user to install all skills:
`npx skills add rebase-lat/spectorio --skill 'spectorio-*'`.

Guidelines base (user-editable): copy the router skill's `references/` guides
(`conventions.md`, `workflow.md`, phase guides, `principles/`, `examples/`) to
`spectorio/references/` — `SKILL_DIR/../spectorio/references/` when installed
side by side. Copy missing files only (`cp -n`); never overwrite workspace edits.

Root instruction files (`AGENTS.md`, `CLAUDE.md`): append the router skill's
`references/agent-instructions.md` when its marker block is absent; never
overwrite or duplicate (see the exact loop in `new.md` §0).

Then run onboarding (`spectorio-onboard`) before any change. From here on, every
`spectorio/...` path resolves against the project workspace.

## 1. Scaffold the change

Metadata only — artifacts are created on demand, never pre-copied.

```bash
mkdir -p spectorio/changes/<kebab-name>/specs
cat > spectorio/changes/<kebab-name>/.spectorio.yaml <<'EOF'
schema: spectorio
created: YYYY-MM-DD  # today
skip_specs: false
strict_design: false
strict_archive: false
retire_capabilities: false
EOF
```

If the name exists → stop (continue it or pick a new name). Derive kebab-case from the request; ask when empty.

## Flags (`.spectorio.yaml` — semantics: `conventions.md` §6 in the `spectorio` router skill)

- `skip_specs`
- `strict_design`
- `strict_archive`
- `retire_capabilities`

Next: status checklist → first artifact (`spectorio-motion` when vague/risky, else `spectorio-propose`).

Voice throughout: act as the expert developer/product owner in the `spectorio` router skill's `references/persona.md`.
