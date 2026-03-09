---
name: skill-creator
description: Create new Claude Code skills for the Karma ecosystem. Use when user says "create a skill", "build a new skill", "scaffold a skill", or "design a skill". Guides through intent capture, SKILL.md writing, validation, and packaging.
version: 0.1.0
tags: [meta, skill, create, scaffold]
metadata:
  author: Karma
  category: meta
---

# Karma Skill Creator

Create well-structured Claude Code skills for the Karma ecosystem.

## Skill Creation Process

1. **Understand** the skill with concrete examples
2. **Plan** reusable skill contents (references, assets)
3. **Initialize** the skill directory structure
4. **Write** the skill (implement resources and SKILL.md)
5. **Validate** against the checklist before shipping
6. **Iterate** based on real usage

## Step 1: Understand the Skill

Ask the user for concrete examples of how the skill will be used:

- "What should this skill do? Can you give 2-3 example prompts?"
- "What would a user say that should trigger this skill?"
- "What Karma-specific context does this need?" (grants, funding maps, ecosystem data)


## Step 2: Plan Reusable Contents

For each example, identify what reusable resources would help:

| Resource Type | When to Use | Example |
|--------------|-------------|---------|
| `references/` | Domain knowledge Claude needs | `references/gap-schema.md` |
| `assets/` | Files used in output | `assets/report-template.md` |

## Step 3: Initialize the Skill

Create the skill directory under `skills/`:

```
skills/<skill-name>/
├── SKILL.md          # Required
├── references/       # Optional
└── assets/           # Optional
```

**Naming rules:**
- kebab-case, lowercase letters, digits, and hyphens only
- Max 64 characters
- Descriptive: `grant-milestone-tracker`, not `tracker`

## Step 4: Write the Skill

### How Skills Load (Progressive Disclosure)

Skills use a three-level system — understanding this is critical for writing effective skills:

1. **YAML frontmatter** — always loaded into Claude's system prompt. This is how Claude decides whether to activate the skill. Keep it lean: just `name` and `description`.
2. **SKILL.md body** — loaded only when Claude thinks the skill is relevant. Contains the full instructions.
3. **Linked files** (`references/`, `assets/`) — Claude navigates to these on demand. Use for detailed docs, templates, and examples.

The implication: frontmatter must be self-sufficient for triggering. The body must be self-sufficient for execution. Reference files are for depth.

### Writing the Description (Most Important Field)

The `description` field determines whether your skill triggers. Get this right.

**Structure**: [What it does] + [When to use it] + [Key capabilities]

**Rules:**
- Under 1024 characters
- MUST include both what the skill does AND when to use it (trigger phrases)
- Include specific phrases users would actually say
- No XML angle brackets (`<` or `>`)

**Good examples:**
```yaml
# Specific, with trigger phrases
description: Analyzes grant milestone reports and generates
  compliance summaries. Use when user asks to "review milestones",
  "check grant progress", or "generate a milestone report".

# Clear scope with negative triggers
description: Advanced data analysis for CSV files. Use for
  statistical modeling, regression, clustering. Do NOT use for
  simple data exploration (use data-viz skill instead).
```

**Bad examples:**
```yaml
# Too vague — won't trigger reliably
description: Helps with projects.

# Missing triggers — when should Claude load this?
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user-facing triggers
description: Implements the Project entity model with hierarchical
  relationships.
```

**Debugging tip:** Ask Claude "When would you use the [skill-name] skill?" — it will quote the description back. Adjust based on what's missing.

### SKILL.md Body

```yaml
---
name: skill-name
description: What the skill does and when to use it. Include specific triggers.
---
```

The body contains instructions Claude will follow. Key principles:

**Concise is key.** Claude is already smart — only add what it doesn't know. Challenge each paragraph: "Does this justify its token cost?"

**Set appropriate freedom levels:**
- **High freedom** (text instructions): multiple valid approaches, context-dependent
- **Medium freedom** (pseudocode/parameterized scripts): preferred pattern with some variation
- **Low freedom** (exact scripts): fragile operations, consistency critical

**Progressive disclosure:** Keep SKILL.md under 500 lines. Split into reference files when approaching this limit.

### Design Patterns

Consult these guides based on your skill's needs:

- **Multi-step processes**: See [workflows.md](references/workflows.md) for sequential and conditional patterns
- **Output format/quality**: See [output-patterns.md](references/output-patterns.md) for template and example patterns

### What NOT to Include

- README.md, CHANGELOG.md, or other auxiliary docs
- "When to use" sections in the body (put this in the frontmatter description)
- Setup/testing procedures
- Information Claude already knows

## Step 5: Validate Before Shipping

Run through this checklist before considering the skill done:

**Structure:**
- [ ] Folder named in kebab-case
- [ ] `SKILL.md` exists (exact casing)
- [ ] YAML frontmatter has `---` delimiters on both sides
- [ ] `name` field: kebab-case, no spaces, no capitals
- [ ] No XML angle brackets (`<` `>`) anywhere in frontmatter
- [ ] Skill name does not contain "claude" or "anthropic" (reserved)
- [ ] No `README.md` inside the skill folder

**Description:**
- [ ] Includes WHAT the skill does
- [ ] Includes WHEN to use it (trigger phrases)
- [ ] Under 1024 characters
- [ ] Trigger phrases match how users actually talk

**Triggering:**
- [ ] Triggers on obvious task requests
- [ ] Triggers on paraphrased requests
- [ ] Does NOT trigger on unrelated topics

**Instructions:**
- [ ] Instructions are clear and actionable
- [ ] Critical steps use explicit language, not vague guidance
- [ ] Error handling included for likely failure points
- [ ] References clearly linked (not inlined)

## Step 6: Iterate

1. Use the skill on real tasks
2. Note struggles or inefficiencies
3. Update SKILL.md or resources

Let the user's specifications guide the skill's domain and direction.
