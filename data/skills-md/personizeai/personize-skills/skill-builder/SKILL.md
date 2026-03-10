---
name: skill-builder
description: "How to create, structure, and install skills for this codebase. Use this skill whenever the user wants to create a new skill, add agent capabilities, write a SKILL.md, structure a skill folder, or follow the skills framework. Also trigger when they mention 'new skill', 'add a skill', 'skill template', or 'extend agent capabilities'."
metadata:
  short-description: Create and manage skills for agent capabilities
---

# Skill Builder

> **Skill Name**: Skill-Builder  
> **Description**: Guide for creating new skills to extend agent capabilities, following the OpenAI Codex CLI skills standard.

---

## Overview

Skills are modular, reusable packages of instructions that help AI agents perform specific tasks reliably. This skill documents how to create, structure, and add new skills to the `Skills/` folder.

---

## Skill Folder Structure

Based on [OpenAI's Codex CLI skills framework](https://github.com/openai/codex):

```
Skills/
├── README.md                    # Skill catalog + routing guide
├── my-skill/                    # Skill folder (use kebab-case)
│   ├── SKILL.md                 # Required: Main instructions + metadata
│   ├── scripts/                 # Optional: Executable code/automation
│   ├── reference/               # Optional: Additional documentation
│   └── assets/                  # Optional: Templates, images, resources
│
├── skill-builder/SKILL.md       # This skill — how to create new skills
└── _internal/                   # Platform dev docs (not discoverable skills)
```

---

## Creating a New Skill

### Option 1: Single-File Skill (Simple)

For straightforward skills, create a single `.md` file:

```markdown
---
name: My Skill Name
description: Brief description of what this skill does
metadata:
  short-description: One-line summary
---

# My Skill Name

> **Skill Name**: My-Skill-Name  
> **Description**: Detailed description of the skill's purpose.

---

## Overview
[What this skill does and when to use it]

## Instructions
[Step-by-step guide]

## Examples
[Code samples or usage examples]

## References
[Links to relevant documentation]
```

### Option 2: Folder-Based Skill (Complex)

For skills with scripts, assets, or extensive documentation:

```
Skills/
└── My-Complex-Skill/
    ├── SKILL.md           # Main skill file (required)
    ├── scripts/
    │   └── setup.sh       # Automation scripts
    ├── references/
    │   └── api-docs.md    # Supporting documentation
    └── assets/
        └── template.json  # Templates or resources
```

---

## SKILL.md Template

```markdown
---
name: [Skill Name]
description: [What this skill helps accomplish - used for skill selection]
metadata:
  short-description: [One-line summary for UI display]
  version: 1.0.0
  author: [Your name or team]
  tags: [api, database, frontend, etc.]
---

# [Skill Name]

## Overview
[Comprehensive description of the skill's purpose and use cases]

## Prerequisites
- [Required knowledge or setup]
- [Dependencies]

## Instructions

### Step 1: [First Action]
[Detailed instructions]

### Step 2: [Second Action]
[Detailed instructions]

## Verification
- [ ] [How to verify the skill worked correctly]

## Troubleshooting
| Issue | Solution |
|-------|----------|
| [Common problem] | [How to fix it] |

## References
- [Link to relevant documentation]
- [Related skills or resources]
```

---

## Skill Naming Conventions

| Convention | Example | Usage |
|------------|---------|-------|
| Kebab-case | `Add-Data-Type-CRUD.md` | File names |
| Title Case | `Add Data Type CRUD` | Skill display name |
| Descriptive | `How to add new data type...` | Description field |

---

## Best Practices

1. **RFC 2119 Constraints**: Use MUST/SHOULD/MAY with rationale clauses in all enforcement sections (see Writing Standard below)
2. **Progressive Disclosure**: Put the most important info first; details later
3. **Actionable Steps**: Use numbered lists for procedures
4. **Code Examples**: Include working code snippets
5. **Verification**: Always include a way to verify success
6. **Links**: Reference source files with relative paths

---

## Writing Standard: RFC 2119 Constraints

All skills use [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) keywords to express enforcement levels. This replaces informal patterns like "always", "never", "important", and "prefer" in rule sections.

> Inspired by [Amazon's Agent SOPs](https://github.com/strands-agents/agent-sop) from the Strands SDK — natural language markdown with formal requirement keywords creates a middle ground between rigid code and freeform prompting.

### Keywords

| Keyword | Meaning | Agent Behavior | When to Use |
|---------|---------|----------------|-------------|
| **MUST** / **MUST NOT** | Absolute requirement | Agent fails the task if violated | Data integrity, security, user trust, API correctness |
| **SHOULD** / **SHOULD NOT** | Strong default | Follow unless you state explicit reasoning to deviate | Best practices, performance, quality patterns |
| **MAY** | Agent discretion | Choose either way without justification | Optimization hints, convenience, stylistic choices |

### Rationale Clauses

Every constraint gets a "because" rationale after an em dash. This gives the agent context to make good decisions in edge cases rather than blindly following rules.

**Format:**
```
- **MUST** [do X] -- because [consequence of not doing it].
- **SHOULD** [do Y] -- because [benefit, with acceptable override conditions].
- **MAY** [do Z] -- because [benefit when applicable].
```

**Before/After examples:**
```
Before: "ALWAYS show the admin what you're about to change before calling the API."
After:  "MUST show the admin the proposed change before calling any mutating API
         -- because silent modifications erode trust and prevent catching errors
         before they reach production."

Before: "Prefer section-level updates over full replace."
After:  "SHOULD use section-level updates over full replace -- because scoped edits
         reduce blast radius and allow concurrent editing; override only when
         structural reorganization requires full rewrite."

Before: "Optionally add an IF node to check success."
After:  "MAY add an IF node after the API call to check success -- because explicit
         success checks simplify debugging in complex workflows."
```

### Section Naming

Use `## Constraints` (H2) for top-level enforcement sections. Use `### Constraints` (H3) for per-action constraints within a dispatch skill.

Do NOT use: "Critical Rules", "Key Rules", "Important Rules", "Guardrails". The three-tier MUST/SHOULD/MAY gradient replaces severity signaling.

### Balance Check

Not everything should be MUST. A skill with zero SHOULD or MAY rules is probably over-constraining. The gradient exists so agents can exercise judgment on best practices while never violating safety-critical requirements.

---

## SOP Files (.sop.md)

For procedural workflows (multi-step processes with sequenced actions, branching, and explicit success criteria), create a `.sop.md` file alongside or instead of a SKILL.md.

### When to Use `.sop.md` vs `SKILL.md`

| Signal | Use `SKILL.md` | Use `.sop.md` |
|--------|----------------|---------------|
| Multiple independent actions | Yes | No |
| Dispatch table ("jump to action") | Yes | No |
| Linear procedure with ordered steps | No | Yes |
| Steps have pre/post-conditions | No | Yes |
| Branching decision points | Either | Yes (preferred) |
| Measurable success criteria | Either | Yes (preferred) |

Both formats use the same RFC 2119 keywords and rationale clauses.

### SOP Template

```markdown
---
name: [procedure-name]
description: [what this SOP accomplishes]
type: sop
metadata:
  version: 1.0.0
  author: [your name or team]
---

# SOP: [Procedure Name]

## Overview
[What this procedure does, when to use it, expected duration]

## Parameters
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| [param]   | yes/no   | [value] | [what it controls] |

## Pre-conditions
- [What MUST be true before starting]

## Steps

### Step 1: [Action Name]
[Instructions]

**Constraints:**
- **MUST** [requirement] -- because [rationale].
- **SHOULD** [recommendation] -- because [rationale].

### Step 2: [Action Name]
[Instructions]

**Constraints:**
- **MUST** [requirement] -- because [rationale].
- **MAY** [option] -- because [rationale].

## Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

## Artifacts
| Artifact | Location | Description |
|----------|----------|-------------|
| [output] | [path]   | [what it is] |
```

---

## Skills Catalog & Routing

For the full skill catalog and routing guide, see the [Skills README](../README.md).

---

## References

- [OpenAI Codex CLI - Skills Documentation](https://github.com/openai/codex/blob/main/docs/skills.md)
- [OpenAI Skills Repository](https://github.com/openai/skills)
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
