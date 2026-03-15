---
name: Skill Creator
slug: skill-creator
description: Create new Claude Code skills with proper structure and documentation
category: meta
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "create a skill"
  - "new skill"
  - "build a skill"
  - "skill creator"
  - "design a skill"
tags:
  - skill-development
  - meta-programming
  - automation
---

# Skill Creator

The Skill Creator skill helps you design, build, and document new Claude Code skills following ID8Labs standards. It guides you through the complete skill creation process, from concept to implementation, ensuring your skills are well-structured, properly documented, and integrate seamlessly with the Claude Code ecosystem.

This skill automates the boilerplate work of skill creation while enforcing best practices around naming conventions, file structure, workflow design, and documentation. It helps you think through skill design decisions, identify the right complexity level, define clear triggers, and create comprehensive documentation that makes your skills easy to use and maintain.

Use this skill whenever you want to extend Claude Code's capabilities with new, reusable workflows that solve recurring problems or automate complex tasks.

## Core Workflows

### Workflow 1: Design New Skill from Concept
1. **Clarify** the skill purpose:
   - What problem does it solve?
   - Who will use it?
   - What are the key workflows?
2. **Define** skill metadata:
   - Name (clear, descriptive)
   - Slug (kebab-case)
   - Category (development, operations, meta, etc.)
   - Complexity (simple, complex, multi-agent)
   - Triggers (natural language phrases)
   - Tags (for discovery)
3. **Design** core workflows:
   - Identify 2-4 primary workflows
   - Map step-by-step processes
   - Define inputs and outputs
   - Identify dependencies (tools, MCPs, other skills)
4. **Structure** documentation:
   - Overview and use cases
   - Workflow details
   - Quick reference table
   - Best practices
   - Examples
5. **Create** skill file with full documentation
6. **Test** skill integration
7. **Iterate** based on usage

### Workflow 2: Scaffold Skill from Template
1. **Gather** basic requirements:
   - Skill name and purpose
   - Category
   - Primary workflow
2. **Generate** SKILL.md from template:
   - Frontmatter with metadata
   - Description section
   - Core Workflows section
   - Quick Reference table
   - Best Practices list
3. **Create** directory structure:
   - `/skills/[slug]/SKILL.md`
   - Additional files if needed (examples, templates)
4. **Populate** with placeholder content
5. **Guide** user to fill in specifics

### Workflow 3: Refactor Existing Workflow into Skill
1. **Analyze** the existing workflow:
   - What steps are repeated?
   - What knowledge is required?
   - What could be automated?
2. **Extract** reusable patterns
3. **Generalize** for broader use cases
4. **Document** as formal skill
5. **Parameterize** variable elements
6. **Test** with original use case and variations
7. **Deploy** to skills directory

### Workflow 4: Skill Quality Review
1. **Check** metadata completeness:
   - All required frontmatter fields present
   - Triggers are natural and discoverable
   - Tags are relevant and consistent
2. **Review** documentation:
   - Clear description of purpose
   - Well-defined workflows
   - Actionable best practices
   - Useful examples
3. **Validate** structure:
   - Follows standard SKILL.md format
   - Proper markdown formatting
   - Logical organization
4. **Test** functionality:
   - Triggers work as expected
   - Workflows are executable
   - Dependencies are available
5. **Suggest** improvements
6. **Approve** or request revisions

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create new skill | "Create a skill for [purpose]" |
| Scaffold from template | "Scaffold a skill called [name]" |
| Review existing skill | "Review this skill: [path or content]" |
| Convert workflow to skill | "Turn this workflow into a skill: [workflow]" |
| Generate skill metadata | "Generate metadata for [skill concept]" |
| Design skill workflows | "Design workflows for [skill purpose]" |
| Validate skill structure | "Validate this skill file: [path]" |

## Best Practices

- **Name Clearly**: Skill names should be instantly understandable
  - Good: "Database Designer", "API Tester", "Deployment Automation"
  - Bad: "Helper", "Tool", "Manager"

- **Choose Right Complexity**:
  - **Simple**: Single workflow, minimal dependencies, straightforward execution
  - **Complex**: Multiple workflows, external tools, conditional logic
  - **Multi-agent**: Coordinates other skills/agents, orchestration layer

- **Define Natural Triggers**: Use phrases users would actually say
  - Include variations: "review code", "code review", "review this code"
  - Avoid overly formal language
  - Test with real users if possible

- **Document Workflows Step-by-Step**: Each workflow should be executable
  - Number the steps
  - Use action verbs
  - Be specific about inputs/outputs
  - Include decision points

- **Provide Quick Reference**: Users shouldn't need to read full docs
  - Table format for common actions
  - Copy-pasteable commands
  - Clear, concise descriptions

- **Include Examples**: Show real usage
  - Before/after scenarios
  - Common use cases
  - Edge cases if relevant

- **Tag Thoughtfully**: Help users discover your skill
  - Use existing category tags when possible
  - Add 3-5 specific tags
  - Consider search terms users might use

- **Version Properly**: Follow semantic versioning
  - Start at 1.0.0 for initial release
  - Increment patch for bug fixes
  - Increment minor for new workflows
  - Increment major for breaking changes

## Skill Metadata Reference

### Required Frontmatter Fields
```yaml
name: Human-Readable Name
slug: kebab-case-identifier
description: One-line description (under 100 chars)
category: development | operations | meta | design | data | testing
complexity: simple | complex | multi-agent
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "natural language trigger 1"
  - "natural language trigger 2"
tags:
  - relevant-tag-1
  - relevant-tag-2
```

### Optional Frontmatter Fields
```yaml
dependencies:
  tools:
    - playwright
    - supabase
  mcps:
    - firecrawl
    - github
  skills:
    - other-skill-slug
requires_config:
  - ENV_VAR_NAME: "Description of what this is for"
examples_dir: "./examples"
```

## Skill Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **development** | Building and coding | Code review, scaffolding, refactoring |
| **operations** | Deployment and infrastructure | CI/CD, monitoring, deployment |
| **meta** | Skills about AI/skills | Prompt engineering, workflow design |
| **design** | UI/UX and creative work | Component design, design systems |
| **data** | Database and data workflows | Schema design, migrations, queries |
| **testing** | Quality assurance | Test generation, E2E testing |
| **content** | Writing and documentation | Technical writing, marketing copy |

## Common Skill Patterns

### Simple Pattern: Single Action
```markdown
## Core Workflows

### Workflow 1: Execute [Action]
1. Receive input
2. Process input
3. Return output
```

### Complex Pattern: Multi-Step with Branching
```markdown
## Core Workflows

### Workflow 1: [Primary Action]
1. Analyze input
2. **If** [condition]:
   - Path A
3. **Else**:
   - Path B
4. Synthesize results
5. Validate output
```

### Multi-Agent Pattern: Orchestration
```markdown
## Core Workflows

### Workflow 1: Coordinate [Task]
1. Assess requirements
2. **Delegate** to Skill A for [subtask]
3. **Delegate** to Skill B for [subtask]
4. **Monitor** progress
5. **Integrate** results
6. Validate final output
```

## Testing Your Skill

Before considering a skill complete:

1. **Test triggers**: Verify phrases activate the skill
2. **Execute workflows**: Run through each workflow completely
3. **Check dependencies**: Ensure all required tools are available
4. **Validate documentation**: Have someone else read and use it
5. **Edge cases**: Test with unusual or complex inputs
6. **Integration**: Verify it works with related skills
7. **Performance**: Ensure it doesn't create bottlenecks

## Skill Maintenance

Skills should evolve with usage:

- **Track issues**: Note when workflows fail or confuse users
- **Gather feedback**: Ask users what's missing or unclear
- **Update docs**: Keep examples and best practices current
- **Deprecate carefully**: If replacing, provide migration guide
- **Version clearly**: Document breaking changes
