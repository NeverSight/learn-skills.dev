---
id: SKILL
aliases: []
tags: []
description: LLM Agent Skill for AnySystem Design React component library
name: anysystem-design
---

# AnySystem Design - LLM Agent Skill

A comprehensive LLM agent skill for the AnySystem Design React component library. This skill enables AI assistants to help developers use the component library effectively.

## Overview

AnySystem Design is a React component library with 22 components covering forms, layouts, navigation, and data display. This skill provides structured knowledge and examples for LLM agents to assist developers.

## Installation

### Option 1: NPX / BUNX Package (Recommended)

```bash
npx skills add freedomw1987/anysystem-design-skill

# or 

bunx skills add freedomw1987/anysystem-design-skill
```

Then configure in your AI assistant:

```json
{
  "skills": {
    "anysystem-design": {
      "path": "node_modules/@anysystem-design-skill"
    }
  }
}
```

### Option 2: Git Submodule

Add as a submodule to your project:

```bash
git submodule add git@github.com:freedomw1987/anysystem-design-skill.git agent-skill
```

Update the submodule to latest version:

```bash
git submodule update --remote agent-skill
```

### Option 3: Direct Clone

Clone this repository directly:

```bash
git clone git@github.com:freedomw1987/anysystem-design-skill.git
```

### Option 4: Claude Code Skills

For Claude Code CLI, copy to your project's `.claude/skills/` directory:

```bash
cp -r anysystem-design-skill/* .claude/skills/
```

## Contents

This skill package includes:

- **skill-definition.json** - Structured component metadata
- **quick-reference.md** - Fast lookup guide
- **examples/** - Code examples for common patterns
- **troubleshooting.md** - Common issues and solutions
- **api-reference.md** - Complete API documentation

## Features

### Component Coverage
- ✅ All 22 components documented
- ✅ Form components with Formik integration
- ✅ Layout and navigation components
- ✅ Data display components
- ✅ TypeScript type definitions

### Capabilities
- 🔍 Component lookup and explanation
- 💻 Code example generation
- 🎯 Best practices guidance
- 🐛 Troubleshooting assistance
- 🔗 Integration examples (Formik, React Router)

## Usage with Different AI Assistants

### Claude Code

1. Copy skill to `.claude/skills/`:
```bash
mkdir -p .claude/skills
cp agent-skill/skill-definition.json .claude/skills/anysystem-design.json
```

2. Use in conversation:
```
How do I create a form with validation using AnySystem Design?
```

### GitHub Copilot

1. Add to workspace settings:
```json
{
  "github.copilot.advanced": {
    "customSkills": ["node_modules/@anysystem/design-agent-skill"]
  }
}
```

### Custom GPT (ChatGPT)

1. Upload `skill-definition.json` as knowledge
2. Add instructions from `gpt-instructions.md`

### LangChain / LlamaIndex

```python
from langchain.tools import Tool

anysystem_skill = Tool(
    name="anysystem-design",
    description="Help with AnySystem Design React components",
    func=load_skill("path/to/agent-skill")
)
```

## Component Quick Reference

### Forms (9 components)
- Button, Input, PasswordInput, TelephoneInput
- Checkbox, Switch, FormControl, Label

### Selection (4 components)
- Selectbox, AutoComplete, RadioGroup, DatePicker

### Layout (3 components)
- Container, Row, Column

### Navigation (2 components)
- Navbar, NavList

### Data Display (2 components)
- DataTable, Text

### Interactive (1 component)
- Modal

### Layouts (2 components)
- SideMenuLayout, EmptyLayout

## Example Queries

The skill can handle queries like:

- "How do I create a form with validation?"
- "Show me a complete login page example"
- "How to use DataTable with selection?"
- "Create a sidebar layout with navigation"
- "What props does the Modal component accept?"
- "How to integrate with Formik?"
- "DatePicker value format explanation"

## Sample Responses

### Query: "How do I use the Button component?"

The agent will provide:
1. Import statement
2. Basic usage example
3. Props explanation (variant, size, rounded)
4. Code examples for different variants
5. Advanced usage (with icons, styling)
6. Related components

### Query: "Create a complete form with validation"

The agent will provide:
1. Formik + Yup setup
2. FormControl + FormInput usage
3. Error handling
4. Submit button
5. Complete working example
6. Best practices

## Skill Structure

```
agent-skill/
├── README.md                 # This file
├── skill-definition.json     # Structured component data
├── quick-reference.md        # Quick lookup guide
├── api-reference.md          # Complete API docs
├── troubleshooting.md        # Common issues
├── examples/
│   ├── form-validation.md
│   ├── sidebar-layout.md
│   ├── data-table.md
│   └── modal-dialog.md
└── integrations/
    ├── formik.md
    ├── react-router.md
    └── typescript.md
```

## Contributing

To update or improve this skill:

1. Fork this repository: https://github.com/freedomw1987/anysystem-design-skill
2. Make your changes to the skill files
3. Test with your AI assistant
4. Submit a pull request

### Updating in a Parent Project

If you're using this as a submodule:

```bash
cd agent-skill
git checkout main
git pull origin main
# Make your changes
git add .
git commit -m "Your changes"
git push origin main

# Update parent project to use new version
cd ..
git add agent-skill
git commit -m "Update agent-skill submodule"
```

## Version

Current version: 0.0.1

This skill is maintained separately from the main AnySystem Design library to allow independent updates and versioning.

## Repository

This is a standalone repository that can be used as:
- A git submodule in your main project
- An NPM package (when published)
- A direct clone for local development

## License

Same as AnySystem Design library

## Links

- [Main Component Library](https://github.com/freedomw1987/anysystem-design)
- [Component Library NPM](https://www.npmjs.com/package/anysystem-design)
- [This Skill Repository](https://github.com/freedomw1987/anysystem-design-skill)

## Support

For issues or questions:
- GitHub Issues: https://github.com/freedomw1987/anysystem-design-skill/issues
- Main Library Issues: https://github.com/freedomw1987/anysystem-design/issues
- Examples: See `examples/` directory in this repository

---

**Made for AI Assistants 🤖**

This skill enables AI to help developers build better React applications with AnySystem Design.
