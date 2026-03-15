---
name: mkt-technical-writer
description: This skill should be used when the user asks to "document this project", "create a user guide", "write documentation", "explain this app", "create README", "write technical docs", "document the codebase", or mentions product documentation, user guides, technical writing, or translating code to documentation. Scans project structure and generates clear, user-facing documentation.
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
---

# Technical Writer

Generate product documentation by analyzing codebases and translating technical implementation into clear, structured user guides.

## Before Starting

### Step 0: Product Context
Check for `.agents/mkt/product-context.md`. If available, read for product context to inform documentation.

### Required Artifacts
None — scans project structure directly.

### Optional Artifacts
| Artifact | Source | Benefit |
|----------|--------|---------|
| `product-context.md` | mkt-copywriting | Product context for documentation |

---

## Workflow

1. **Scan project structure** to understand architecture
2. **Identify key files** for analysis
3. **Extract core concepts** from implementation
4. **Generate documentation** following the output template

## Step 1: Scan Project Structure

Run a directory scan to map the project:

```bash
find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.tsx" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.swift" -o -name "*.kt" \) | head -100
```

Also check for:
- `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod` for dependencies
- `README.md` for existing context
- Config files like `.env.example`, `config/`, `settings/`

## Step 2: Identify Key Files

Priority files to analyze:

| File Type | What It Reveals |
|-----------|-----------------|
| Entry points (`main.*`, `index.*`, `app.*`) | Core app initialization and structure |
| Route definitions | Available features and user flows |
| Components/Views | UI structure and user interactions |
| Models/Types | Core data entities and relationships |
| API handlers | Backend capabilities |
| Config/env | Environment requirements and settings |

Read 5-10 most important files. Skip generated files, node_modules, vendor directories, and test files unless specifically relevant.

## Step 3: Extract Core Concepts

While reading code, identify:

**Product Identity**
- What problem does this solve?
- Who is the target user?
- What's the core value proposition?

**Features & Capabilities**
- Main user-facing features
- Key workflows and user journeys
- Input/output patterns

**Architecture Decisions**
- Why was this tech stack chosen?
- What design patterns are used?
- What are the dependencies?

**UX Intent**
- How should users navigate?
- What's the intended user experience?
- What states and feedback exist?

## Step 4: Generate Documentation

Output documentation following the structure in `references/doc-template.md`.

Key principles:
- Write for users who have never seen the code
- Explain the "why" before the "how"
- Use concrete examples over abstract descriptions
- Include screenshots or diagrams when describing UI flows
- Keep technical jargon to a minimum

## Output Format

When saving documentation artifacts, use this frontmatter:

```yaml
---
skill: mkt-technical-writer
version: 1
date: [today's date]
status: draft
---
```

> On re-run: rename existing artifact to `[name].v[N].md` and create new with incremented version.

Generate a single markdown file with all documentation. See `references/doc-template.md` for the full structure.

If the project is large, suggest breaking into multiple focused guides:
- Getting Started Guide
- Feature Reference
- User Workflows
- Configuration Guide
