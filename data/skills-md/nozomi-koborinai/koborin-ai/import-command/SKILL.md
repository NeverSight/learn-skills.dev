---
name: import-command
description: Convert Cursor custom commands (.cursor/commands/*.md) to Claude Code skills (.claude/skills/*/SKILL.md). Use when the user says "import command to skill", "convert command to skill", or "migrate cursor command".
---

# import-command

Convert Cursor custom commands to Claude Code skills.

## Trigger Examples

- "Import command to skill"
- "Convert command to skill"
- "Migrate cursor command to skill"
- "Turn this command into a skill"

## Format Differences

### Cursor Command Format

```markdown
# /command-name

## Overview
[Description]

## Usage
[Usage pattern]

## Prerequisites
[Prerequisites]

## Execution Flow (steps)
[Steps]

## AI considerations
[AI guidance]

## Notes
[Notes]

## Examples
[Examples]
```

### Claude Code Skill Format

```markdown
---
name: skill-name
description: [What it does and when to use it. Include trigger phrases.]
---

# skill-name

[One-line overview]

## Trigger Examples

- "Trigger phrase 1"
- "Trigger phrase 2"

## Prerequisites (optional)

- [Prerequisite]

## Execution Flow

### 1. [Step name]

- [Details]

## Notes

- [Note]
```

## Conversion Rules

### 1. Command Name → Skill Name

- Remove leading `/`
- Keep kebab-case: `/commit-push-pr` → `commit-push-pr`

### 2. Overview → Description (Frontmatter)

- Combine "Overview" and "Usage" into a concise description
- Add trigger phrases based on the command name and purpose
- This is the most important part: description determines when the skill triggers

### 3. Usage → Trigger Examples

- Convert usage patterns to natural language trigger phrases
- Example: `/check-secrets [--strict]` → "Check for secrets", "Scan for leaks"

### 4. Execution Flow (steps) → Execution Flow

- Keep the step structure
- Simplify verbose explanations
- Remove redundant context (Claude is smart)

### 5. AI considerations → Merge into Execution Flow or Notes

- If actionable: merge into Execution Flow
- If general guidance: move to Notes

### 6. Examples → Omit or Simplify

- Skills prefer concise instructions over verbose examples
- Keep only if essential for understanding

## Execution Flow

### 1. Read Source Command

Read the Cursor command file from `.cursor/commands/<command-name>.md`

### 2. Extract Key Information

- Command name
- Overview/description
- Usage patterns
- Prerequisites
- Execution steps
- Notes and caveats

### 3. Generate Skill Structure

Create skill directory and SKILL.md:

```
.claude/skills/<skill-name>/
└── SKILL.md
```

### 4. Write Frontmatter

```yaml
---
name: <skill-name>
description: <comprehensive description with trigger phrases>
---
```

### 5. Write Body

- Concise trigger examples
- Simplified execution flow
- Essential notes only

### 6. Present for Approval

Show the generated skill and ask for approval before creating.

### 7. Update CLAUDE.md

Add the new skill to the skills list in CLAUDE.md.

## Notes

- Skills should be more concise than commands
- Focus on trigger phrases in description
- Remove redundant explanations
- Deprecated commands should not be converted
