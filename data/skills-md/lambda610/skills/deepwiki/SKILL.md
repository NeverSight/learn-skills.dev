---
name: deepwiki
description: "AI-powered local codebase documentation generator. Use for: (1) Deep code analysis with business logic extraction, (2) Comprehensive API documentation with signatures, (3) Architecture diagrams and data flow mapping, (4) Code patterns identification and design decisions. Not for: Simple file listings or code comments only."
metadata: {"openclaw": {"emoji": "📚"}}
---

# DeepWiki — Professional Codebase Documentation Generator

Generate comprehensive, professional documentation that explains **why** and **how**, not just **what**.

## What DeepWiki Generates

DeepWiki goes beyond file listings to create documentation that tells the story of your codebase:

### 📖 Documentation Types

- **Architecture Docs** — System design, components, data flow
- **API References** — Complete function signatures with examples
- **Module Guides** — How to use and extend each part
- **Data Schemas** — Type definitions and validation rules
- **Cookbooks** — Common tasks and solutions

### 🎯 Deep Analysis Features

- **Business Logic Extraction** — Understand what the code actually does
- **Pattern Recognition** — Identify architectural and design patterns
- **Data Flow Mapping** — Trace how data moves through the system
- **Decision Records** — Document why architectural choices were made
- **Code Examples** — Working examples for every API

## Claude Code Usage

Simply describe what documentation you need:

```bash
"Analyze this codebase and generate architecture documentation"
"Document all APIs with TypeScript signatures"
"Create a module guide for the auth system"
"Generate a data schema reference"
"Scan the code and create a cookbook for common tasks"
```

DeepWiki will read your actual code, not just filenames, to create comprehensive documentation.

## When to Use

- User wants to document a new codebase
- Need to understand legacy or complex code
- Onboarding new team members
- Preparing context for AI tools
- Creating public API documentation

## Prerequisites

- Claude Code or OpenClaw with read access to the codebase
- (Optional) `tree` command for directory structure visualization

## OpenClaw Usage

### Commands

```
/deepwiki-scan [project-path]     # Deep code analysis
/deepwiki-generate                # Full documentation
/deepwiki-api                     # API reference only
/deepwiki-architecture            # Architecture docs only
/deepwiki-modules                 # Module guides only
/deepwiki-data                    # Data schemas only
```

## Claude Code Usage

Simply describe what you need (no commands needed):

```bash
"Scan this codebase structure and extract business logic"
"Generate complete documentation with API reference"
"Document the architecture and design patterns"
"Create module guides with usage examples"
"Analyze data types and validation rules"
```

The skill triggers on keywords from the description above.

## For Detailed Guidance

See [SCAN_GUIDE.md](references/SCAN_GUIDE.md) for deep analysis methodology.
See [GENERATE_GUIDE.md](references/GENERATE_GUIDE.md) for documentation templates.

## What Makes DeepWiki Different

| Aspect | Basic Docs | DeepWiki |
|--------|-----------|----------|
| Code understanding | "Has auth module" | "Auth flow: login → validate → token → session" |
| API docs | "Has login function" | Full signature + params + errors + examples |
| Architecture | "Uses React" | Component hierarchy + data flow + state management |
| Patterns | None identified | "Uses Compound Component pattern in BentoGrid" |
| Decisions | Not documented | "Chose this approach because..." |

## Output Structure

```
docs/deepwiki/
├── README.md              # Project overview + quick start
├── ARCHITECTURE.md        # System design + components
├── API.md                 # Complete API reference
├── MODULES.md             # Module guides + recipes
├── DATA.md                # Type schemas + validation
└── reference/
    ├── ADR.md            # Architecture decisions
    └── glossary.md       # Term definitions
```

## Best For

- 📚 Onboarding new team members
- 🔄 Understanding legacy codebases
- 📝 Preparing for AI context injection
- 🎓 Teaching others about your codebase
- 📦 Creating user-facing documentation

## Tips

1. **Be specific** — "Document the payment flow" vs "Document everything"
2. **Iterate** — Generate, review, then ask for refinements
3. **Focus** — Use `--focus=api` for API-only docs
4. **Examples matter** — DeepWiki includes runnable examples

## Integration

DeepWiki works great with:
- **Claude Code** — Context injection and code understanding
- **GitHub** — Documentation on push to main/PR
- **Onboarding** — New team member documentation
- **API Docs** — Public-facing API reference
