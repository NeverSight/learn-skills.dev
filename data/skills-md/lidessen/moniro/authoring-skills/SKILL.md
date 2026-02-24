---
name: authoring-skills
description: Guide for authoring effective Agent Skills using principle-based approach (Progressive Disclosure, Respect Intelligence, Enable Discovery). Covers creating, improving, refactoring, and reviewing skills. Use for skill authoring, design questions, best practices, anti-patterns, or structure decisions.
---

# Authoring Agent Skills

## The Goal: Efficient Context Usage

Every skill you create will be loaded into Claude's limited context window. The fundamental challenge is:

**Every unnecessary token wastes limited context space, slows processing, costs money, and reduces room for actual work.**

Everything else—structure, naming, content—follows from this goal. Understanding *why* these patterns matter allows you to make good decisions in novel situations, rather than mechanically following rules.

## Three Core Principles

### 1. Progressive Disclosure: Load Only What's Needed

**The Intent**: Don't force Claude to read 5000 lines when it needs 100.

**Why It Matters**: When a skill is triggered, SKILL.md loads entirely into context. If you put everything in one file, every query wastes tokens on irrelevant content. A finance query shouldn't load sales data. A basic usage shouldn't load advanced edge cases.

**How to Apply**:
- Keep SKILL.md as a navigation hub (~500 lines)
- Defer detailed content to reference files
- Link directly from SKILL.md (avoid nested references that trigger partial reads)

**The Trade-off**: More files vs. larger context. Always choose more files.

See [best-practices/progressive-disclosure.md](best-practices/progressive-disclosure.md) for patterns.

### 2. Respect Intelligence: Assume Claude Is Smart

**The Intent**: Don't explain what Claude already knows.

**Why It Matters**: Explaining "PDF stands for Portable Document Format" wastes tokens and provides zero value. Claude understands file formats, programming concepts, standard tools, and industry patterns. Token space is precious—use it for your domain-specific knowledge, not computer science 101.

**How to Apply**:
- Skip explanations of common concepts (file formats, imports, package managers)
- Provide code and commands, not tutorials
- Challenge each sentence: "Does Claude really need this?"

**The Trade-off**: Brevity vs. completeness. Trust Claude's knowledge.

See [best-practices/conciseness.md](best-practices/conciseness.md) for examples.

### 3. Enable Discovery: Make Skills Findable

**The Intent**: Help Claude choose the right skill from potentially 100+ options.

**Why It Matters**: A vague description means your skill won't trigger when needed. "Helps with documents" doesn't tell Claude when to use it. "Extract text from PDF and Word documents" with triggers like "PDF, .docx, extraction" ensures discovery.

**How to Apply**:
- Write descriptions in third person (they're injected into system prompts)
- Include specific capabilities (WHAT) and trigger scenarios (WHEN)
- Use concrete terms: file types, technology names, activity phrases

**The Trade-off**: Specificity vs. flexibility. Be specific about triggers.

See [best-practices/description.md](best-practices/description.md) for examples.

## Quick Start Workflow

When creating a skill, apply these principles:

1. **Understand the goal** - What problem does this solve? Who will use it?
2. **Draft metadata** - Name (lowercase-with-hyphens) and description (WHAT + WHEN)
3. **Design for disclosure** - What goes in SKILL.md vs. reference files?
4. **Write concisely** - Assume Claude is smart. Skip the obvious.
5. **Test with sub-agent** - Dry-run discovery, execution, and boundary tests (see [Testing](#testing-with-sub-agent))

## Essential Constraints

Some requirements exist for technical reasons:

### Name Format
- Lowercase letters, numbers, hyphens only (parsing requirement)
- Max 64 characters (system limit)
- No XML tags, no "anthropic" or "claude" (reserved terms)
- Prefer gerund form: `processing-pdfs`, `analyzing-data` (consistency)

### Description Format
- Max 1024 characters (system limit)
- Third person: "Processes files..." not "I process..." (system prompt injection)
- Include capabilities + triggers (discovery mechanism)

**Good example**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

### File Organization
- Forward slashes in paths (cross-platform compatibility)
- One-level references from SKILL.md (avoid partial reads)
- Reference files >100 lines need TOC (enables preview scanning)

## Common Patterns

These patterns emerge from the core principles:

1. **Template Pattern**: Provide output format templates when consistency matters
2. **Workflow Pattern**: Multi-step checklists for complex processes
3. **Feedback Loop**: Validate → fix → repeat for quality-critical tasks
4. **Conditional Pattern**: Decision branches for context-dependent logic

See [patterns/](patterns/) for detailed examples.

## Degrees of Freedom

Match specificity to task fragility:

- **High freedom** (instructions): Multiple valid approaches, Claude chooses based on context
- **Medium freedom** (templates): Preferred pattern, acceptable variation
- **Low freedom** (scripts): Fragile operations requiring exact execution

*Why this matters*: Over-specifying simple tasks wastes tokens. Under-specifying fragile tasks causes errors.

See [best-practices/degrees-of-freedom.md](best-practices/degrees-of-freedom.md).

## Understanding Anti-Patterns

Rather than memorizing rules, understand *why* certain patterns fail:

- **Windows paths** (`\`) → Parser must handle both styles, adds cognitive load
- **Nested references** → Triggers partial reads, loses information
- **Time-based conditions** → Becomes wrong after dates pass
- **Vague names** → Poor discoverability, unclear purpose

The pattern: They all violate efficient context usage or discoverability.

See [anti-patterns.md](anti-patterns.md) for detailed explanations.

## Quality Self-Check

Before finalizing, ask yourself:

**Core Principles**:
- Does this minimize context usage? (Progressive disclosure)
- Am I explaining things Claude knows? (Respect intelligence)
- Will Claude discover this skill correctly? (Enable discovery)

**Technical Constraints**:
- Name/description follow format requirements?
- SKILL.md under 500 lines?
- References one level deep?
- All paths use forward slashes?

**Content Quality**:
- Consistent terminology?
- Concrete examples over abstract descriptions?
- No time-sensitive information?

## Testing with Sub-Agent

Use Task tool to dry-run test your skill before finalizing.

### 1. Discovery Test

Verify the description triggers correctly:

```
Task tool → Explore agent:
"Given this user request: '[typical trigger phrase]',
which skill would you recommend and why?"
```

**Pass criteria**: Agent identifies your skill for the right scenarios.

### 2. Execution Test

Verify the skill content is actionable:

```
Task tool → General-purpose agent:
"Using the [skill-name] skill located at [path],
perform this task: [realistic task]"
```

**Pass criteria**: Agent follows the workflow without confusion or asking for clarification on skill instructions.

### 3. Boundary Test

Verify the skill doesn't over-trigger:

```
Task tool → Explore agent:
"Given this user request: '[edge case that should NOT trigger]',
which skill would you recommend?"
```

**Pass criteria**: Agent recommends a different skill or no skill.

### Quick Test Checklist

| Test | Prompt Example | Expected |
|------|----------------|----------|
| Discovery | "How do I [trigger phrase]?" | Recommends this skill |
| Execution | "[Realistic task]" | Completes using skill workflow |
| Boundary | "[Similar but different task]" | Recommends other skill |

## Storage Locations

**Determine location based on your environment:**

1. **Check existing setup** - Look for existing skill directories:
   - **Cursor**: `~/.cursor/skills/` (personal) or `.cursor/skills/` (project)
   - **Codex/Claude**: `$CODEX_HOME/skills/` (personal) or project-specific location
   - **Other tools**: Check tool-specific documentation

2. **If no existing setup**, use standard locations:
   - **Project-level**: `.agents/skills/` (standard Agent Skills format)
   - **Personal**: `~/.agents/skills/` or tool-specific home directory

3. **For project instructions** (not skills), use `AGENTS.md` in project root

**Important**:
- **Never** use `~/.cursor/skills-cursor/` (reserved for Cursor built-ins)
- Prefer project-level storage for team collaboration

## Learning Resources

**Start Here**:
- [best-practices/core-principles.md](best-practices/core-principles.md) - **Read this first**: Philosophy, trade-offs, and judgment

**Core Philosophy**:
- [best-practices/progressive-disclosure.md](best-practices/progressive-disclosure.md) - Why and how to layer information
- [best-practices/conciseness.md](best-practices/conciseness.md) - Respecting Claude's intelligence
- [best-practices/description.md](best-practices/description.md) - Making skills discoverable
- [best-practices/degrees-of-freedom.md](best-practices/degrees-of-freedom.md) - Balancing specificity

**Practical Patterns**:
- [patterns/template.md](patterns/template.md) - When consistency matters
- [patterns/workflow.md](patterns/workflow.md) - Complex multi-step processes
- [patterns/examples.md](patterns/examples.md) - Show, don't tell
- [patterns/feedback-loop.md](patterns/feedback-loop.md) - Quality-critical tasks

**Examples**:
- [examples/simple-skill.md](examples/simple-skill.md) - Basic skill with just SKILL.md
- [examples/complex-skill.md](examples/complex-skill.md) - Progressive disclosure in action
- [examples/with-scripts.md](examples/with-scripts.md) - Including utility scripts

**Reference**:
- [yaml-requirements.md](reference/yaml-requirements.md) - Technical specifications
- [file-organization.md](reference/file-organization.md) - Organizational strategies
- [anti-patterns.md](anti-patterns.md) - Understanding what to avoid and why
