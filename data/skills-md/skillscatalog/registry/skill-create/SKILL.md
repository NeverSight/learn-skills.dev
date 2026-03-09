---
name: skill-create
description: Create new Agent Skills from templates with best-practice structure, pre-populated SKILL.md, and optional scripts/assets directories.
version: 1.0.0
license: MIT
author: "@anthropic-agent-skills"
tags:
  - creation
  - templates
  - tooling
  - development
---

## Instructions

Use this skill to create new Agent Skills from templates. It generates a properly structured skill directory with a valid SKILL.md file and optional scripts/assets folders.

### When to Use

- Starting a new skill from scratch
- Ensuring proper skill structure and naming
- Quickly prototyping new skill ideas
- Teaching others how to structure skills

### How to Use

Create a new skill with a name:

```
Create a new skill called "pdf-tools"
```

Create a skill with a specific template:

```
Create a new skill called "data-analyzer" using the with-scripts template
```

Available templates:
- **basic** - Just SKILL.md (default)
- **with-scripts** - SKILL.md + scripts directory
- **with-assets** - SKILL.md + scripts + assets directories

### Output

Creates a complete skill directory:

**Basic template:**
```
pdf-tools/
├── SKILL.md
└── README.md
```

**With-scripts template:**
```
pdf-tools/
├── SKILL.md
├── README.md
└── scripts/
    └── main.py
```

**With-assets template:**
```
pdf-tools/
├── SKILL.md
├── README.md
├── scripts/
│   └── main.py
└── assets/
    └── .gitkeep
```

## Examples

**Basic skill:**
```
User: Create a new skill called "code-formatter"
Agent: Creating skill "code-formatter" with basic template...

       Created:
       ✓ code-formatter/SKILL.md
       ✓ code-formatter/README.md

       Next steps:
       1. Edit SKILL.md with your skill's instructions
       2. Add any supporting files
       3. Run skill-validator to check compliance
```

**Interactive mode:**
```
User: Create a new skill
Agent: I'll help you create a new skill.

       Skill name: code-formatter
       Description: Format code in various languages
       Template: with-scripts
       License: MIT

       Creating...
       ✓ Created code-formatter with with-scripts template
```

**With metadata:**
```
User: Create a new skill called "api-tester" with description "Test REST APIs" and author "acme-corp"
Agent: Creating skill "api-tester"...
       ✓ Created with custom metadata:
         - Description: Test REST APIs
         - Author: acme-corp
         - License: MIT (default)
```

## Limitations

- Skill names must be lowercase with hyphens only (1-64 chars)
- Names must start with a letter
- Will not overwrite existing directories
- Templates are minimal - intended as starting points

## Dependencies

- Python 3.9+
- No external dependencies (uses Python stdlib)
