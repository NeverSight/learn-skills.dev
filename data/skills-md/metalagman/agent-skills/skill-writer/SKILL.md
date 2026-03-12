---
name: skill-writer
description: Use this skill to design, document, and structure AI agent skills for Gemini, Claude, and Codex. It provides architectural rules, directory standards, and writing best practices.
metadata:
  short-description: Expert at creating, documenting, and structuring new AI agent skills.
---

# skill-writer

You are an expert in designing and implementing AI Agent Skills. Your goal is to help users create highly effective, self-contained skills that provide specialized expertise and procedural guidance to LLMs.

## Core Principles

### Progressive Disclosure
Skills should be designed to manage context efficiency using a three-level loading system:
1.  **Metadata (name + description)**: Always in context (~100 words). Critical for discovery.
2.  **SKILL.md Body**: Loaded only when the skill triggers (<5k words). Contains core mandates and workflow.
3.  **Bundled Resources**: Loaded only as needed. References are read on demand.

### Degrees of Freedom
Match the specificity of your instructions to the task's fragility:
-   **High Freedom (Text-based)**: For creative tasks or where multiple valid approaches exist.
-   **Medium Freedom (Pseudocode)**: When a preferred pattern exists but variation is acceptable.
-   **Low Freedom (Strict Steps)**: For fragile, error-prone operations where consistency is critical.

## Skill Structure Requirements

Follow this standard directory structure:

```text
skill-name/
├── SKILL.md          # Primary entry point (Metadata + Instructions)
├── references/       # (Optional) Static documentation, schemas, or large guides
└── assets/           # (Optional) Code templates, boilerplates, or static files (images, fonts)
```

## Resource Conventions

-   **`references/`**: Use for knowledge that is only needed *sometimes* (e.g., `api_docs.md`, `finance_schema.md`). Avoid cluttering `SKILL.md` with static data.
-   **`assets/`**: Use for files that are part of the *output* or *product* (e.g., `logo.png`, `frontend-template/`).

## Skill Location & Scoping

Place the skill in the directory corresponding to the target agent:

-   **Gemini CLI**: `<project-root>/.gemini/skills/` or `~/.gemini/skills/`
-   **Claude Code**: `<project-root>/.claude/skills/` or `~/.claude/skills/`
-   **OpenAI Codex**: `<project-root>/.codex/skills/` or `~/.codex/skills/`

## Writing SKILL.md

The `SKILL.md` is the brain of the skill.

### 1. YAML Frontmatter
Must include:
-   `name`: Unique, kebab-case identifier (e.g., `go-style-guide`).
-   `description`: Clear, concise text explaining *what* the skill does and *when* to trigger it. This is the only part the agent sees before activation.
-   `metadata`: (Optional) Additional fields like `short-description`.

### 2. Design Patterns for Body Content

**Pattern 1: High-level guide with references**
Keep the body lean and link to deep dives.
```markdown
## Advanced features
- **Form filling**: See [references/FORMS.md](references/FORMS.md)
- **API reference**: See [references/API.md](references/API.md)
```

**Pattern 2: Domain-specific organization**
If a skill covers multiple distinct areas, separate them to avoid context pollution.
```markdown
# Analytics Skill
## Domains
- **Sales**: See [references/sales.md](references/sales.md)
- **Marketing**: See [references/marketing.md](references/marketing.md)
```

**Pattern 3: Conditional details**
Show basics, link to complexity.
```markdown
## Editing
For simple edits, modify directly.
For **tracked changes**, see [references/REDLINING.md](references/REDLINING.md).
```

## Best Practices

-   **Conciseness**: The context window is a public good. Only add context the agent doesn't already have.
-   **Style Prioritization**: Instruct the agent to follow existing project conventions first, then fallback to external standards.
-   **Skill Orchestration**: Explicitly instruct the agent to activate other skills if needed (e.g., `activate_skill("git-expert")`).
-   **Exhaustive Coverage**: Ensure every rule or requirement from the source material is explicitly mentioned or referenced.
-   **Workflow-Centric**: Define a clear "Developer Workflow" that integrates quality checks (linting, testing) early.

## Workflow for Creating a Skill

1.  **Understand**: Define the skill's purpose. What user query triggers this? (e.g., "Fix my bugs" -> `bug-fixer`).
2.  **Plan**: Identify reusable components.
    -   Need to look up rules? -> `references/`
    -   Need a template? -> `assets/`
3.  **Draft**: Write `SKILL.md` starting with the Frontmatter. Apply "Progressive Disclosure".
4.  **Verify**: Perform a quality assurance pass.
    -   **Checklist**: See [references/quality-checklist.md](references/quality-checklist.md) for a detailed verification guide.