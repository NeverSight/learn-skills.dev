---
name: skills-creator
description: Create and manage Agent Skills following the agentskills.io specification. Use when users want to create, validate, or modify skills for AI agents.
license: MIT
metadata:
  author: restman
  version: "1.0"
---

# Skills Creator

A comprehensive skill for creating, validating, and managing Agent Skills that follow the agentskills.io specification.

## When to use this skill

Use this skill when:
- User asks to create a new agent skill
- User wants to modify or improve an existing skill
- User needs to validate a skill's structure or frontmatter
- User mentions "skill", "agent skill", or agentskills.io
- User wants to understand the Agent Skills format

## What Agent Skills are

Agent Skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge and workflows. At its core, a skill is a folder containing a `SKILL.md` file with metadata and instructions.

### Progressive disclosure principle

Skills use progressive disclosure to manage context efficiently:
1. **Discovery**: At startup, agents load only name and description
2. **Activation**: When relevant, agents read the full SKILL.md instructions
3. **Execution**: Agents load referenced files or execute code as needed

This keeps agents fast while providing access to more context on demand.

## Directory structure

```
skill-name/
├── SKILL.md          # Required: instructions + metadata
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
└── assets/           # Optional: templates, resources
```

## SKILL.md format

Every skill starts with YAML frontmatter followed by Markdown instructions.

### Required frontmatter

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

### Optional frontmatter fields

```yaml
---
name: skill-name
description: What this skill does and when to use it.
license: MIT
compatibility: Requires git, docker, jq, and internet access
metadata:
  author: example-org
  version: "1.0"
allowed-tools: Bash(git:*) Bash(jq:*) Read
---
```

## Field specifications

### name field
- **Required**: Yes
- **Constraints**: 1-64 characters, lowercase letters/numbers/hyphens only
- Must not start or end with hyphen
- Must not contain consecutive hyphens (`--`)
- Must match the parent directory name

**Valid examples:**
- `pdf-processing`
- `data-analysis`
- `code-review`

**Invalid examples:**
- `PDF-Processing` (uppercase)
- `-pdf` (starts with hyphen)
- `pdf--processing` (consecutive hyphens)

### description field
- **Required**: Yes
- **Constraints**: 1-1024 characters, non-empty
- Should describe both what the skill does AND when to use it
- Include specific keywords that help agents identify relevant tasks

**Good example:**
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.
```

**Poor example:**
```yaml
description: Helps with PDFs.
```

### license field
- **Required**: No
- Keep it short (license name or reference to bundled file)

Example:
```yaml
license: Apache-2.0
```

### compatibility field
- **Required**: No
- **Constraints**: 1-500 characters if provided
- Only include if skill has specific environment requirements
- Can indicate intended product, required packages, network access, etc.

Examples:
```yaml
compatibility: Designed for Claude Code (or similar products)
```
```yaml
compatibility: Requires git, docker, jq, and access to the internet
```

### metadata field
- **Required**: No
- Map from string keys to string values
- Use for additional properties not defined by spec
- Make key names reasonably unique to avoid conflicts

Example:
```yaml
metadata:
  author: example-org
  version: "1.0"
  category: development
```

### allowed-tools field
- **Required**: No
- Space-delimited list of pre-approved tools
- Experimental feature, support varies

Example:
```yaml
allowed-tools: Bash(git:*) Bash(jq:*) Read
```

## Body content guidelines

The Markdown body after frontmatter contains the skill instructions. No format restrictions, but follow these best practices:

### Recommended sections

1. **When to use this skill** - Clear triggers for when agents should activate this skill
2. **What this skill does** - Brief overview of capabilities
3. **Step-by-step instructions** - Detailed procedures
4. **Examples** - Sample inputs and expected outputs
5. **Common patterns** - Reusable approaches
6. **Best practices** - Tips and recommendations
7. **Edge cases** - How to handle unusual situations

### Content best practices

- Keep main SKILL.md under 500 lines (< 5000 tokens recommended)
- Move detailed reference material to separate files in `references/`
- Use clear, actionable language
- Include code examples where helpful
- Focus on the "why" and "how", not just "what"
- Consider the agent's perspective when writing instructions

## Optional directories

### scripts/
Contains executable code that agents can run.

**Best practices:**
- Make scripts self-contained or clearly document dependencies
- Include helpful error messages
- Handle edge cases gracefully
- Use common languages (Python, Bash, JavaScript)

Example structure:
```
scripts/
├── validate.py
├── generate.sh
└── utils/
    └── helpers.py
```

### references/
Contains additional documentation loaded on demand.

**Best practices:**
- Keep files focused on single topics
- Use descriptive filenames
- Recommended files:
  - `REFERENCE.md` - Detailed technical reference
  - `FORMS.md` - Form templates or structured data formats
  - Domain-specific files (`finance.md`, `legal.md`, etc.)

Example structure:
```
references/
├── REFERENCE.md
├── API.md
└── TROUBLESHOOTING.md
```

### assets/
Contains static resources like templates, images, and data files.

Example structure:
```
assets/
├── templates/
│   └── config.yaml
├── diagrams/
│   └── workflow.png
└── data/
    └── schema.json
```

## File references

When referencing other files in your skill, use relative paths from the skill root:

```markdown
See [the reference guide](references/REFERENCE.md) for details.

Run the extraction script:
```bash
scripts/extract.py
```
```

Keep file references one level deep from SKILL.md. Avoid deeply nested reference chains.

## Creating a new skill step-by-step

When a user asks you to create a skill, follow these steps:

### 1. Gather requirements
Ask the user:
- What should the skill do?
- When should it be activated?
- What tools or resources are needed?
- Are there specific examples or use cases?

### 2. Choose a name
- Use lowercase with hyphens
- Keep it short and descriptive
- Ensure it matches the directory name

### 3. Write a clear description
- Include what the skill does
- Include when to use it
- Add keywords for agent matching

### 4. Create directory structure
```bash
mkdir -p skill-name/scripts
mkdir -p skill-name/references
mkdir -p skill-name/assets
```

### 5. Write SKILL.md
Start with frontmatter, then add body with:
- When to use section
- What it does
- Step-by-step instructions
- Examples
- Best practices

### 6. Add supporting files (if needed)
- Scripts in `scripts/`
- Reference docs in `references/`
- Templates/assets in `assets/`

### 7. Validate
Check that:
- Name follows constraints (lowercase, no consecutive hyphens, etc.)
- Description is clear and keyword-rich (1-1024 chars)
- Frontmatter is valid YAML
- Directory name matches skill name
- Instructions are clear and actionable

## Common patterns

### Basic skill (instructions only)
```
basic-skill/
└── SKILL.md
```

### Skill with scripts
```
automation-skill/
├── SKILL.md
└── scripts/
    └── automate.py
```

### Complex skill with references
```
complex-skill/
├── SKILL.md
├── scripts/
│   └── process.py
├── references/
│   ├── REFERENCE.md
│   └── API.md
└── assets/
    └── templates/
        └── config.yaml
```

## Validation checklist

Before finalizing a skill, verify:

- [ ] Directory name matches `name` in frontmatter
- [ ] `name` is 1-64 chars, lowercase alphanumeric + hyphens only
- [ ] `name` doesn't start/end with hyphen or have consecutive hyphens
- [ ] `description` is 1-1024 chars and includes when to use
- [ ] YAML frontmatter is valid
- [ ] Main SKILL.md is under 500 lines
- [ ] File references use relative paths
- [ ] Scripts have clear error handling (if present)
- [ ] No deeply nested reference chains

## Example skill templates

### Minimal skill
```markdown
---
name: example-skill
description: Brief description of what this does and when to use it.
---

## When to use this skill
Use when...

## Instructions
1. Step one
2. Step two
3. Step three
```

### Full-featured skill
```markdown
---
name: advanced-skill
description: Comprehensive description with keywords for activation.
license: MIT
compatibility: Requires specific tools or environment
metadata:
  author: your-name
  version: "1.0"
---

## When to use this skill
Use when...

## What this skill does
Overview...

## Instructions
Detailed steps...

## Examples
Sample code and outputs...

## Best practices
Tips and recommendations...

## Common patterns
Reusable approaches...

## Troubleshooting
See [troubleshooting guide](references/TROUBLESHOOTING.md)
```

## Integration notes

Skills are designed to work with filesystem-based agents (preferred) or tool-based agents:

### Filesystem-based agents
- Skills activated via shell commands like `cat /path/to/skill/SKILL.md`
- Bundled resources accessed through shell commands

### Tool-based agents
- Implement tools for triggering skills and accessing assets
- Tool implementation is up to the developer

## Resources

For more information:
- [agentskills.io specification](https://agentskills.io/specification)
- [Integration guide](https://agentskills.io/integrate-skills)
- [Example skills on GitHub](https://github.com/anthropics/skills)
- [Authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Reference library (skills-ref)](https://github.com/agentskills/agentskills/tree/main/skills-ref)

## Validation commands

If the user has the `skills-ref` library installed:

```bash
# Validate a skill directory
skills-ref validate ./skill-name

# Generate XML for agent prompts
skills-ref to-prompt ./skill-name
```

## Best practices for writing skills

1. **Keep it focused**: One skill should do one thing well
2. **Be specific in descriptions**: Include activation keywords
3. **Use progressive disclosure**: Keep SKILL.md concise, move details to references
4. **Provide examples**: Show don't just tell
5. **Handle errors gracefully**: Anticipate edge cases
6. **Test thoroughly**: Ensure instructions are clear and complete
7. **Version your skills**: Use metadata to track changes
8. **Document dependencies**: Use compatibility field when needed
9. **Make it portable**: Skills should work across environments when possible
10. **Think like an agent**: Write instructions from the agent's perspective

## Security considerations

When creating skills with scripts:
- Warn about potentially dangerous operations
- Document all external dependencies
- Consider sandboxing requirements
- Use allowlisting for trusted scripts
- Log script executions for auditing
- Avoid hardcoded credentials or secrets
