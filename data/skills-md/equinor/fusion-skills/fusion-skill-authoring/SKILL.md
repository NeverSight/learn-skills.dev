---
name: fusion-skill-authoring
description: Create or scaffold a new skill in a repository with valid metadata, clear activation cues, standard resource folders, safety boundaries, and validation evidence.
license: MIT
metadata:
   version: "0.2.1"
   tags:
      - skill-authoring
      - scaffolding
   mcp:
      suggested:
         - github
---

# Create Skill

## When to use

Use this skill when you need to create a new skill under `skills/` and want a valid, maintainable `SKILL.md`.

Typical triggers:
- "Create a skill for ..."
- "Scaffold `skills/<name>/SKILL.md`"
- "Add a new skill with proper metadata and guardrails"
- "Help me create a skill that helps create other skills"

## When not to use

Do not use this skill for:
- Editing product/application code outside `skills/`
- Large refactors of existing skills unless explicitly requested
- Running destructive commands or making unrelated repository changes

## Required inputs

Collect before writing files:
- Base skill name in kebab-case (`<skill-name>`, without prefix)
- Prefix choice (ask explicitly; suggest `custom-` by default unless the repository has its own convention)
- Final skill name (`custom-<skill-name>` unless the user chooses a different prefix or none)
- Target path (`skills/<final-skill-name>/`, `skills/.experimental/<final-skill-name>/`, or `skills/.curated/<final-skill-name>/`)
- Initial semantic version for frontmatter metadata (`MAJOR.MINOR.PATCH`, default `0.0.0` for skills created in this repository)
- License for frontmatter (`MIT` by default, or repository-specific choice)
- One-sentence purpose for frontmatter `description`
- Expected output (files, commands, summary)
- Safety boundaries

Validate metadata constraints:
- `name`: <= 64 chars, lowercase letters/numbers/hyphens only, no XML tags, and no platform-reserved words
- `description`: non-empty, <= 1024 chars, no XML tags, includes both what it does and when to use it
- `metadata.version`: semantic version string (`MAJOR.MINOR.PATCH`) in quoted YAML format
- `metadata`: primarily string key/value map; arrays allowed for explicit relationship fields, avoid nested objects
  - `metadata.role`: `"orchestrator"` or `"subordinate"` (subordinates cannot run without their orchestrator)
  - `metadata.orchestrator`: required orchestrator skill name (subordinates only)
  - `metadata.skills`: list of subordinate skill names (orchestrators only)
  - `metadata.tags`: optional list of lowercase kebab-case strings for discoverability
   - `metadata.mcp`: optional map for MCP server needs (`required` and `suggested` lists)
- `license` and `compatibility`: optional top-level frontmatter fields (not inside `metadata`)

If required inputs are missing, ask concise targeted questions first.
Use `assets/follow-up-questions.md` as the default question bank.

## Instructions

1. Check whether an existing skill already covers the request:
   - Run `npx -y skills add . --list`
   - If an existing skill matches, recommend using/updating that skill instead of creating a duplicate
   - If a skill almost matches, open/recommend a repository issue to request tweaks to that existing skill instead of creating a new custom skill
   - Prioritize reuse of repository skills to avoid proliferation of one-off custom skills
2. Confirm scope, base skill name, prefix choice, and target path.
3. Derive `<final-skill-name>` from prefix choice.
4. Create `<target>/<final-skill-name>/SKILL.md`.
5. Create resource directories as needed:
   - `references/` for longer guidance and detailed docs
   - `assets/` for templates/checklists/static resources
   - `scripts/` only when deterministic automation is required
6. Write frontmatter (`name`, `description`) that satisfies constraints.
7. Add the core sections:
   - When to use
   - When not to use
   - Required inputs
   - Instructions
   - Expected output
   - Safety & constraints
8. Keep `SKILL.md` concise; move long guidance/examples to `references/`.
9. Use `assets/` for templates, sample files, and static resources used by the skill.
10. Add `scripts/` only when deterministic automation is required.
11. When inputs are missing, ask from `assets/follow-up-questions.md` and proceed once answered.

## Expected output

Return:
- Created/updated file paths
- Validation command(s) run
- Pass/fail result with interpretation
- Any required follow-up actions
- Any unresolved follow-up questions (if user input was still missing)
- Whether an existing skill was reused, and if an issue was created/recommended for an almost-match

For a newly scaffolded skill, the default structure should be:

```text
skills/<final-skill-name>/
├── SKILL.md
├── references/
└── assets/
```

Use this baseline for generated `SKILL.md` files:

```markdown
---
name: <final-skill-name>
description: <what it does + when to use it>
license: MIT
metadata:
   version: "<initial-version>"
---

# <Skill Title>

## When to use

## When not to use

## Required inputs

## Instructions

## Expected output

## Safety & constraints
```

## Validation

Run from repo root:

```bash
npx -y skills add . --list
```

Pass criteria:
- Exit code is `0`
- New skill appears discoverable/valid
- No metadata/path errors

If validation fails:
- Fix frontmatter (`name`, `description`)
- Verify path and `SKILL.md` existence
- Re-run and report final status

## Ready-to-merge checklist

Use `assets/ready-to-merge-checklist.md` as a lightweight PR gate.

## Safety & constraints

Never:
- Request or expose secrets/credentials
- Run destructive commands without explicit user confirmation
- Invent validation results
- Modify unrelated files outside requested scope
- Add hidden network-fetch or unsafe script guidance without explicit request
