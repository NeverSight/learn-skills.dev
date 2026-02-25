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
npx skills add david-marstree/anysystem

# or

bunx skills add david-marstree/anysystem
```

Then configure in your AI assistant:

```json
{
  "skills": {
    "anysystem-design": {
      "path": "node_modules/anysystem-design"
    }
  }
}
```

### Option 2: Direct Clone

Clone this repository directly:

```bash
git clone git@github.com:david-marstree/anysystem.git
```

### Option 3: Claude Code Skills

For Claude Code CLI, copy to your project's `.claude/skills/` directory:

```bash
cp SKILL.md .claude/skills/anysystem-design.md
cp skills/skill-definition.json .claude/skills/
```

## Documentation Structure

This skill includes comprehensive documentation:

### Quick Reference
- **skills/quick-reference.md** - Fast lookup guide for all components
- **skills/api-reference.md** - Complete API documentation

### Guides & Examples
- **skills/examples/formcontrol-guide.md** - ⭐ FormControl 完整指南（推薦閱讀）
- **skills/examples/form-validation.md** - Form validation with Formik

### Full Documentation
- **docs/README.md** - Documentation overview
- **docs/GETTING_STARTED.md** - Getting started guide
- **docs/COMPONENT_CATALOG.md** - Complete component catalog

### Component Docs
- **docs/components/** - Individual component documentation (20 files)
- **docs/layouts/** - Layout documentation (2 files)

### Troubleshooting
- **skills/troubleshooting.md** - Common issues and solutions

## Contents

```
/
├── SKILL.md                         # This file
├── skills/
│   ├── quick-reference.md           # Quick lookup guide
│   ├── api-reference.md             # Complete API docs
│   ├── skill-definition.json        # Structured component data
│   ├── troubleshooting.md           # Common issues
│   └── examples/
│       ├── formcontrol-guide.md     # FormControl 完整指南 ⭐
│       └── form-validation.md       # Form validation example
├── docs/
│   ├── README.md                    # Documentation overview
│   ├── GETTING_STARTED.md           # Getting started
│   ├── COMPONENT_CATALOG.md         # Component catalog
│   ├── DOCUMENTATION_SUMMARY.md     # Docs summary
│   ├── INDEX.md                     # Index
│   ├── components/                  # Component docs (20 files)
│   │   ├── AutoComplete.md
│   │   ├── Button.md
│   │   ├── Checkbox.md
│   │   ├── Column.md
│   │   ├── Container.md
│   │   ├── DataTable.md
│   │   ├── DatePicker.md
│   │   ├── FormControl.md
│   │   ├── Input.md
│   │   ├── Label.md
│   │   ├── Modal.md
│   │   ├── Navbar.md
│   │   ├── NavList.md
│   │   ├── PasswordInput.md
│   │   ├── RadioGroup.md
│   │   ├── Row.md
│   │   ├── Selectbox.md
│   │   ├── Switch.md
│   │   ├── TelephoneInput.md
│   │   └── Text.md
│   └── layouts/                     # Layout docs
│       ├── EmptyLayout.md
│       └── SideMenuLayout.md
└── lib/                             # Source code
    └── components/                  # Component implementations
```

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

## Component Quick Reference

### Forms (11 components)
- **FormControl** ⭐ - Unified form control API (covers 12 input types)
- Button, Input, PasswordInput, TelephoneInput
- Selectbox, AutoComplete, RadioGroup, DatePicker
- Checkbox, Switch, Label

### Layout (5 components)
- Container, Row, Column
- EmptyLayout, SideMenuLayout

### Navigation (2 components)
- Navbar, NavList

### Data Display (2 components)
- DataTable, Text

### Interactive (1 component)
- Modal

## Key Recommendations

### ⭐ Use FormControl First

**FormControl** is the recommended high-level component that covers **12 input types**:

| Type | Description |
|------|-------------|
| `text`, `email`, `number`, `password` | Basic inputs |
| `tel`, `date`, `datetime` | Specialized inputs |
| `select`, `autocomplete` | Selection controls |
| `radio`, `switch`, `confirm` | Choice controls |

**Benefits**:
- Unified API for all input types
- Automatic Label management
- Consistent variant (sm/md) handling
- Simplified onChange handling
- 50% less code than manual composition

**Example**:
```tsx
<FormControl
  type="email"
  name="email"
  value={email}
  onChange={setEmail}
  labelProps={{ label: "Email" }}
/>
```

See **skills/examples/formcontrol-guide.md** for complete documentation.

### Quick Start Pattern

```tsx
import { AppProvider, FormControl, Button } from 'anysystem-design';

function App() {
  return (
    <AppProvider appName="My App">
      <form className="space-y-4">
        <FormControl
          type="text"
          name="username"
          value={username}
          onChange={setUsername}
          labelProps={{ label: "Username" }}
        />
        <FormControl
          type="password"
          name="password"
          value={password}
          onChange={setPassword}
          labelProps={{ label: "Password" }}
        />
        <Button type="submit" variant="primary">Submit</Button>
      </form>
    </AppProvider>
  );
}
```

## Usage with Different AI Assistants

### Claude Code

1. Copy skill to `.claude/skills/`:
```bash
mkdir -p .claude/skills
cp SKILL.md .claude/skills/anysystem-design.md
cp skills/skill-definition.json .claude/skills/
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
    "customSkills": ["./skills/skill-definition.json"]
  }
}
```

### Custom GPT (ChatGPT)

1. Upload `skills/skill-definition.json` as knowledge
2. Use this SKILL.md as instructions

### LangChain / LlamaIndex

```python
from langchain.tools import Tool

anysystem_skill = Tool(
    name="anysystem-design",
    description="Help with AnySystem Design React components",
    func=load_skill("path/to/skills")
)
```

## Example Queries

The skill can handle queries like:

- "How do I create a form with validation?"
- "Show me a complete login page example"
- "How to use DataTable with selection?"
- "Create a sidebar layout with navigation"
- "What props does the Modal component accept?"
- "How to integrate with Formik?"
- "DatePicker value format explanation"
- "What is FormControl and when should I use it?"

## Documentation Lookup Order

For AI assistants, lookup in this order:

1. **skills/quick-reference.md** - Fast component lookup
2. **skills/examples/formcontrol-guide.md** - FormControl usage ⭐
3. **docs/components/[Component].md** - Detailed component docs
4. **skills/examples/form-validation.md** - Validation patterns
5. **skills/troubleshooting.md** - Common issues

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
1. **Recommended**: FormControl approach
2. Formik + Yup setup
3. FormControl usage with labelProps
4. Error handling
5. Submit button
6. Complete working example
7. Best practices

## Must Remember

1. ✅ Always wrap with `<AppProvider>`
2. ✅ Use `Form*` variants with Formik (FormInput, not Input)
3. ✅ DatePicker value = Unix timestamp (seconds) as string
4. ✅ Modal uses imperative API (ref.current.show/hide)
5. ✅ **FormControl is the preferred way** for form inputs
6. ✅ All components support TypeScript

## Contributing

To update or improve this skill:

1. Make your changes to the skill files
2. Test with your AI assistant
3. Submit a pull request

## Version

Current version: 0.0.48

## Repository

- [Main Component Library](https://github.com/david-marstree/anysystem)
- [Component Library NPM](https://www.npmjs.com/package/anysystem-design)

## Support

For issues or questions:
- GitHub Issues: https://github.com/david-marstree/anysystem/issues
- Examples: See `skills/examples/` directory
- Documentation: See `docs/` directory for complete component docs

---

**Made for AI Assistants 🤖**

This skill enables AI to help developers build better React applications with AnySystem Design.
