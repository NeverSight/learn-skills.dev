---
name: skill-creator
description: >-
  Guide for creating and managing Claude Code skills. Use when creating a new skill,
  updating an existing skill, or validating skill structure. Enforces ABOUTME headers,
  proper frontmatter format, and progressive disclosure patterns. Triggers on "create skill",
  "new skill", "skill template", "init skill", "validate skill", "skill structure",
  "update skill", "modify skill", "edit skill", "add to skill", "change skill",
  "SKILL.md", "skill frontmatter", "skill description", "skill triggers", "allowed-tools",
  "skill file", "claude code skill", "custom skill", "personal skill", "project skill".
allowed-tools: Read, Write, Edit, Bash, Glob
---

# ABOUTME: Skill for creating well-structured Claude Code skills
# ABOUTME: Enforces conventions from CLAUDE.md and provides init/validate tooling

# Skill Creator

Create effective Claude Code skills following established conventions.

## Quick Reference

| Script | Purpose |
|--------|---------|
| `init_skill.py` | Create new skill with proper structure |
| `validate_skill.py` | Validate skill frontmatter and structure |

Run with `--help` for full options:
```bash
uv run ~/.claude/skills/skill-creator/scripts/init_skill.py --help
```

## Skill Anatomy

Every skill consists of:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, allowed-tools)
│   ├── ABOUTME headers (after closing ---)
│   └── Markdown body (instructions)
└── Optional resources/
    ├── scripts/      - Executable code (Python/Bash)
    ├── references/   - Documentation loaded on demand
    └── assets/       - Files used in output (templates, etc.)
```

## SKILL.md Structure

### Frontmatter (Required)

```yaml
---
name: skill-name
description: >-
  What the skill does and WHEN to use it. Include trigger phrases.
  Triggers on "keyword1", "keyword2", "keyword3".
allowed-tools: Read, Write, Edit, Bash
---
```

**Allowed frontmatter keys:** `name`, `description`, `allowed-tools`, `license`, `metadata`

### ABOUTME Headers (Required)

MUST appear immediately after the closing `---`:

```markdown
---
name: my-skill
description: What it does. Triggers on "x", "y".
allowed-tools: Read, Write
---

# ABOUTME: [Brief description of file purpose]
# ABOUTME: [Key context or dependencies]

# Skill Title
```

### Body (Required)

Write instructions Claude needs to execute the skill effectively.

## 🔄 RESUMED SESSION CHECKPOINT

**When a session is resumed from context compaction, verify skill creation state:**

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - SKILL CREATION VERIFICATION              │
│                                                             │
│  Before continuing skill creation/update work:              │
│                                                             │
│  1. Was I in the middle of creating/updating a skill?       │
│     → Check summary for skill names being worked on         │
│     → Check ~/.claude/skills/ for partial skills            │
│                                                             │
│  2. Did the skill pass validation?                          │
│     → Run: uv run validate_skill.py <skill-path>            │
│                                                             │
│  3. Are ABOUTME headers correct?                            │
│     → Must appear AFTER closing --- of frontmatter          │
│     → Must have 2 lines describing purpose and context      │
│                                                             │
│  If skill creation was in progress:                         │
│  → Re-validate the skill structure                          │
│  → Check description is under 1024 chars                    │
│  → Ensure trigger phrases are included                      │
└─────────────────────────────────────────────────────────────┘
```

## Workflow: Create New Skill

### Step 1: Initialize

```bash
uv run ~/.claude/skills/skill-creator/scripts/init_skill.py \
    my-new-skill \
    --path ~/.claude/skills
```

### Step 2: Edit SKILL.md

1. Update the description with clear trigger phrases
2. Write ABOUTME headers describing the skill purpose
3. Add workflow instructions or decision trees
4. Reference any scripts/references you'll create

### Step 3: Add Resources (Optional)

- **scripts/**: Add helper scripts for repeatable operations
- **references/**: Add detailed docs that load only when needed
- **assets/**: Add templates or files used in output

**🚨 IMPORTANT: When creating scripts, invoke the appropriate language skill FIRST:**
- `.sh` files → `/bash`
- `.py` files → `/python`
- `.go` files → `/golang`

### Step 4: Validate

```bash
uv run ~/.claude/skills/skill-creator/scripts/validate_skill.py \
    ~/.claude/skills/my-new-skill
```

### Step 5: Test

Test the skill by invoking it in a Claude Code session with trigger phrases.

## Workflow: Update Existing Skill

When modifying an existing skill (adding features, fixing issues, improving documentation):

### Step 1: Understand Current Structure

Read the existing SKILL.md to understand:
- Current sections and their organization
- Where new content fits logically
- Existing patterns and style to follow

```bash
# Check current structure
head -50 ~/.claude/skills/<skill-name>/SKILL.md
```

### Step 2: Plan Changes

Before editing, identify:
- **Where** the new content belongs (which section)
- **How** it relates to existing content (new section vs. addition to existing)
- **Style** consistency (follow existing formatting patterns)

### Step 3: Make Changes

Follow these rules when editing:
- **Preserve ABOUTME headers** - never remove or modify unless intentional
- **Maintain consistent formatting** - match existing heading levels, list styles
- **Add to existing sections** when content is related
- **Create new sections** only when content is distinct
- **Update trigger phrases** if adding new use cases

### Step 4: Validate

```bash
uv run ~/.claude/skills/skill-creator/scripts/validate_skill.py \
    ~/.claude/skills/<skill-name>
```

### Step 5: Test

Verify the skill triggers correctly with both old and new trigger phrases.

## Design Principles

### Conciseness

Context window is shared. Only include what Claude does NOT already know.
Prefer examples over verbose explanations.

### Progressive Disclosure

| Level | When Loaded | Size Target |
|-------|-------------|-------------|
| Frontmatter | Always | ~100 words |
| SKILL.md body | When triggered | <500 lines |
| References | On demand | Unlimited |

### Degrees of Freedom

Match specificity to task fragility:

- **High freedom** (text instructions): Multiple valid approaches
- **Medium freedom** (pseudocode/params): Preferred pattern with variation
- **Low freedom** (specific scripts): Fragile operations requiring consistency

## Patterns

See `references/patterns.md` for:
- Sequential workflow patterns
- Conditional workflow patterns
- Output template patterns
- Domain-specific organization

## Validation Rules

The validate script checks:

1. **Frontmatter**: Valid YAML, required fields present
2. **Name**: Hyphen-case, max 64 chars, matches directory name
3. **Description**: No angle brackets, max 1024 chars, includes triggers
4. **Structure**: ABOUTME headers present after frontmatter

## Common Issues

| Issue | Solution |
|-------|----------|
| Skill not triggering | Add trigger phrases to description |
| Skill not triggering on updates | Add "update skill", "modify skill" to triggers |
| ABOUTME before frontmatter | Move ABOUTME after closing `---` |
| Description too long | Move details to SKILL.md body |
| Missing allowed-tools | Add tools the skill needs |
| Style inconsistency after edit | Read existing skill first; match patterns |
