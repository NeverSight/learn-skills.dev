---
name: better-skill-creator
description: "Create new agent skills with best-practice templates. Guides through skill level selection (L0 pure prompt, L0+ with helper scripts, L1 with business scripts), environment strategy (stdlib/uv/venv), and generates ready-to-edit project files following runtime UX best practices. This skill should be used when creating a new skill, scaffolding a skill project, initializing skill templates, or when the user says 'help me build a skill', 'create a skill', '创建技能', '新建 skill'."
---

# Skill Creator

## Language

**Match user's language**: Respond in the same language the user uses.

## Overview

Create new agent skills by guiding the user through a series of choices, then generating a ready-to-edit project structure with best practices baked in.

## How It Works

1. Collect requirements through dialogue (AskUserQuestion)
2. Call `scaffold.py` with the collected parameters (non-interactive)
3. Report what was generated and guide next steps

## Dialogue Flow

Progress:
- [ ] Step 1: Understand intent
- [ ] Step 2: Skill name
- [ ] Step 3: Skill level (auto-recommended)
- [ ] Step 4: Environment strategy (L1 only)
- [ ] Step 5: Output directory
- [ ] Generate, validate, and report

Follow these steps in order. Use AskUserQuestion for steps 1–5.

### Step 1: Understand Intent

**Before any structural decisions, understand what the skill will do.** Ask the user:

1. What does this skill do? (one sentence)
2. Give 2–3 example user prompts that should trigger it
3. What does the output/result look like?

This step is critical — it determines the level recommendation and produces a better `description` field.

### Step 2: Skill Name

Ask the user for a skill name. Validate it meets these rules:
- Lowercase letters, digits, and hyphens only
- Must start with a letter, end with a letter or digit
- No consecutive hyphens
- Maximum 64 characters

If invalid, explain the constraint and ask again.

### Step 3: Skill Level (Auto-Recommended)

Based on the examples gathered in Step 1, **recommend a level** before asking:

- If all examples can be handled with Claude's built-in tools, MCP servers, or domain knowledge → recommend **L0**
- If examples need environment detection, status caching, or lightweight shell checks → recommend **L0+**
- If examples involve API calls, data processing, or operations benefiting from deterministic code → recommend **L1**

Present the recommendation with rationale, then let the user confirm or override:

**L0 — Pure Prompt**: Only a SKILL.md file. All capabilities come from Claude's built-in tools, MCP servers, or general knowledge. Best for workflow guides, domain knowledge, configuration wizards. No scripts needed.

**L0+ — Prompt + Helper Scripts**: SKILL.md plus lightweight helper scripts for environment detection, status caching, or other auxiliary tasks. Core logic stays in the prompt. Best when Claude needs a preflight check or a small utility but handles business logic itself.

**L1 — Prompt + Business Scripts**: SKILL.md orchestrates CLI scripts that handle core business logic. Scripts accept parameters, return structured JSON, and follow MCP tool design principles. Best for skills that interact with APIs, process data, or perform operations that benefit from deterministic code.

### Step 4: Environment Strategy (L1 only)

If the user chose L1, ask which environment strategy to use:

**stdlib** — Python standard library only. Zero dependencies, zero environment issues. Choose this when `urllib`, `json`, `argparse`, `pathlib` are sufficient. This is the recommended default.

**uv** — Dependencies declared inline via PEP 723, executed with `uv run`. No persistent venv, global cache, version-isolated. Choose this when external packages are needed but a full venv is overkill.

**venv** — Traditional per-skill virtual environment with `run.sh` wrapper. Choose this only when dependencies require C extensions, or the skill runs long-lived processes.

### Step 5: Output Directory

Ask where to generate the skill. Default: current working directory. The script creates `skills/<name>/` under this directory.

## Generate

After collecting all parameters, run:

```bash
python3 {SKILL_DIR}/scripts/scaffold.py scaffold \
    --name <name> \
    --level <level> \
    [--env <strategy>] \
    --output <dir>
```

Where `{SKILL_DIR}` is the directory containing this SKILL.md file. Resolve it at runtime.

The script outputs JSON to stdout:
```json
{
  "status": "ok",
  "level": "l1",
  "env": "uv",
  "created": ["skills/my-skill/SKILL.md", "skills/my-skill/scripts/main.py", ...],
  "hint": "..."
}
```

If it fails, stderr contains JSON with `error`, `hint`, and `recoverable` fields.

## Post-Generate Validation

Immediately after scaffolding, run the built-in structural validator:

```bash
python3 {SKILL_DIR}/scripts/scaffold.py validate --path <generated-skill-dir>
```

This checks:
- Frontmatter has `name` and `description` fields
- No unreplaced `{{PLACEHOLDER}}` tokens remain
- Referenced files (scripts, references) actually exist
- SKILL.md is under 200 lines (context budget warning)

Report any warnings in the completion output. This catches structural issues before the user invests time editing.

## Completion Report

After successful generation, present:

```
[Skill Creator] Complete!

Skill: <name> (Level: <level>[, Env: <env>])
Output: <directory>

Files created:
• <list from JSON "created" field>

Next Steps:
→ Edit SKILL.md — replace TODO markers, write description with trigger phrases
→ Customize scripts/ (L0+/L1)
→ Test preflight (L0+/L1)
→ Publish with skill-publish when ready
```

Then provide detailed guidance:

1. **Edit SKILL.md** — Replace all placeholder markers. The `description` field in frontmatter is critical — it determines when Claude activates the skill. Be specific and include trigger phrases.

2. **Customize scripts/** (L0+/L1) — The generated scripts are functional frameworks with placeholder markers. Add your business logic.

3. **Test preflight** (L0+/L1) — Run the preflight command to verify the JSON output structure works:
   - L0+: `bash scripts/helper.sh preflight`
   - L1 stdlib: `python3 scripts/main.py preflight`
   - L1 uv: `uv run scripts/main.py preflight`
   - L1 venv: `bash scripts/run.sh preflight` (after setup)

4. **Add references/** — Put detailed reference documents here and reference them from SKILL.md with file read instructions. Keep SKILL.md lean (under 200 lines — the context window is shared with conversation history and other skills).

5. **Use assets/ for non-context files** (L0+/L1) — If your skill produces documents, templates, or uses images/fonts in output, put them in `assets/`. Unlike `references/` (which are loaded into context), `assets/` files are only used by scripts and never consume context window budget.

6. **Do NOT add auxiliary docs** — Do not create README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or other documentation files inside the skill directory. The skill should only contain files needed by the AI agent. READMEs belong at the repo level (handled by `better-skill-publish`).

7. **Ready to publish?** — If the `better-skill-publish` skill is installed, use it to wrap this into a complete GitHub repo with README, LICENSE, plugin.json, and marketplace.json.
   If not installed: `npx skills add psylch/better-skills@better-skill-publish -g -y`

## Design Principles

### Context Budget

The context window is a shared resource. Every line of SKILL.md competes with conversation history, other skills, and tool results. Keep SKILL.md under 200 lines. Move detailed documentation to `references/`.

### Degrees of Freedom

Match instruction specificity to task fragility:
- **Low freedom** (exact commands, strict sequence): For operations where mistakes are costly or hard to reverse — setup flows, credential configuration, destructive operations.
- **Medium freedom** (guidelines + examples): For business logic where the approach is clear but details vary — API interactions, data processing.
- **High freedom** (goals + constraints): For creative or analytical tasks where Claude should adapt — research, analysis, content generation.

## References

For skill design conventions — output formats, error handling, environment strategies, preflight conventions — read `references/best_practices.md`.

For common quality issues and how to avoid them, read `references/improvement_patterns.md`.

For what automated validation checks will be run (by better-skill-review), read `references/validation_rules.md`.
