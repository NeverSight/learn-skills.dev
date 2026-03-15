---
name: diataxis
description: Helps maintain documentation pages based on the Diataxis method. Analyzes existing docs, classifies pages into tutorials/how-to/explanation/reference categories, identifies gaps, and helps create or restructure documentation following Diataxis principles. Use when user mentions documentation structure, Diataxis, doc categories, tutorials vs how-to guides, or reorganizing docs.
---

# Maintain Documentation with the Diataxis Method

You are helping the user organize and maintain their project documentation following the Diataxis framework.

## What is Diataxis?

Diataxis is a systematic approach to technical documentation that organizes content
into four distinct categories based on user needs:

| Category          | Orientation            | Purpose                                  | Form                |
| ----------------- | ---------------------- | ---------------------------------------- | ------------------- |
| **Tutorials**     | Learning-oriented      | Help a beginner get started              | A lesson            |
| **How-to guides** | Task-oriented          | Help the user accomplish a specific goal | A series of steps   |
| **Explanation**   | Understanding-oriented | Help the user understand a concept       | A discursive essay  |
| **Reference**     | Information-oriented   | Provide precise technical descriptions   | Dry, accurate facts |

### Key Distinctions

- **Tutorials vs How-to guides**: Tutorials teach (follow me), how-to guides direct (do this).
  Tutorials are for learners, how-to guides are for practitioners.
- **Explanation vs Reference**: Explanation discusses why and context, reference states what and how
  precisely. Explanation is discursive, reference is austere.
- **Practical vs Theoretical**: Tutorials and how-to guides are practical (doing).
  Explanation and reference are theoretical (knowing).
- **Learning vs Working**: Tutorials and explanation serve learning/studying.
  How-to guides and reference serve working/coding.

## Step 1: Discover Existing Documentation

1. **Scan the project for documentation files:**
   - Look for `docs/`, `doc/`, `documentation/` directories
   - Check for markdown files at the project root: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
   - Look for other documentation formats: `.rst`, `.adoc`, `.txt`
   - Check for documentation configuration: `mkdocs.yml`, `docusaurus.config.js`, `conf.py`, `antora.yml`, `hugo.toml`

2. **Read existing documentation** to understand what is already covered.

3. **If no documentation exists:**
   - Inform the user: "No documentation found. Let's create a documentation structure from scratch."
   - Skip to [Step 3: Propose Documentation Structure](#step-3-propose-documentation-structure)

## Step 2: Classify Existing Documentation

Analyze each documentation page and classify it into one of the four Diataxis categories.

### Classification Rules

**A page is a Tutorial if it:**

- Guides a beginner through a complete learning experience
- Has a clear starting point and end goal
- Uses phrases like "In this tutorial", "you will learn", "let's start by"
- Follows a sequential, step-by-step narrative
- Focuses on learning, not on accomplishing a real-world task

**A page is a How-to guide if it:**

- Addresses a specific task or problem
- Assumes the reader already has basic knowledge
- Uses action-oriented titles like "How to...", "Setting up...", "Configuring..."
- Provides steps to achieve a concrete goal
- Can be followed by someone who knows the basics

**A page is Explanation if it:**

- Discusses concepts, background, or design decisions
- Answers "why" questions
- Provides context and reasoning
- Uses discursive, narrative prose
- Covers architecture, design choices, trade-offs
- Has titles like "Understanding...", "About...", "Why we..."

**A page is Reference if it:**

- Describes APIs, configurations, CLI flags, or data structures
- Is structured for lookup, not reading end-to-end
- Is factual and precise, with minimal narrative
- Includes function signatures, parameter tables, return values
- Has titles like "API Reference", "Configuration options", "CLI commands"

### Mixed Content

Many pages contain content from multiple categories. Flag these for the user and suggest how to split them:

- "This page mixes tutorial content (the getting started section) with reference content
  (the API table). Consider splitting into a tutorial and a reference page."

### Present Classification Results

Present results as a table:

```text
| File                     | Current Category | Suggested Category | Notes              |
|--------------------------|------------------|--------------------|--------------------------------|
| docs/getting-started.md  | -                | Tutorial           | Good tutorial structure         |
| docs/api.md              | -                | Reference          | Contains some how-to content   |
| docs/architecture.md     | -                | Explanation        | Well-structured explanation     |
```

## Step 3: Propose Documentation Structure

Based on the analysis, propose a Diataxis-aligned directory structure.

### Standard Directory Layout

```text
docs/
  tutorials/           # Learning-oriented
    getting-started.md
    first-project.md
  how-to/              # Task-oriented
    install.md
    configure.md
    deploy.md
  explanation/         # Understanding-oriented
    architecture.md
    design-decisions.md
  reference/           # Information-oriented
    api.md
    configuration.md
    cli.md
```

### Adaptation Rules

- **Adapt to existing tooling**: If the project uses mkdocs, docusaurus, antora, hugo, or similar,
  propose a structure compatible with that tool's conventions.
- **Adapt to existing structure**: If the project already has a docs structure that partially aligns
  with Diataxis, propose minimal changes to align it fully rather than a complete restructure.
- **Keep what works**: Do not propose moving content that is already well-categorized.
- **Respect the project conventions**: If the project uses a specific naming convention
  (kebab-case, snake_case, etc.), follow it.

### Identify Documentation Gaps

After classifying existing content, identify missing pieces:

- **No tutorials?** Suggest creating a getting-started tutorial.
- **No how-to guides?** Suggest guides for the most common tasks (installation, configuration, deployment).
- **No explanation?** Suggest architecture or design decision documents.
- **No reference?** Suggest API, configuration, or CLI reference pages.

Present gaps clearly:

```text
Documentation gaps identified:
- [ ] Missing: Tutorial for getting started
- [ ] Missing: How-to guide for deployment
- [ ] Missing: Reference for configuration options
- [x] Covered: Architecture explanation exists
```

## Step 4: Execute Changes

**Always ask the user before making changes.** Present the plan and wait for approval.

### When Restructuring

1. Present the proposed file moves and renames
2. Wait for user approval
3. Move files to their new locations
4. Update any internal links between documentation pages
5. Update navigation configuration (mkdocs.yml, sidebar config, etc.) if applicable
6. Verify no broken links remain

### When Creating New Pages

1. Present which pages you suggest creating
2. Wait for user approval
3. Create pages with proper structure for their category:

**Tutorial template:**

```markdown
# Tutorial: [Title]

In this tutorial, you will learn how to [goal].

## Prerequisites

- [Prerequisite 1]

## Step 1: [First step title]

[Instruction with explanation of what the learner is doing and why]

## Step 2: [Second step title]

[Continue the learning journey]

## What you've learned

- [Summary point 1]
- [Summary point 2]

## Next steps

- [Link to next tutorial or related how-to guide]
```

**How-to guide template:**

```markdown
# How to [accomplish task]

This guide shows you how to [task description].

## Prerequisites

- [Prerequisite 1]

## Steps

### 1. [First step]

[Concise instruction]

### 2. [Second step]

[Concise instruction]

## Troubleshooting

### [Common problem]

[Solution]
```

**Explanation template:**

```markdown
# [Topic]

[Opening paragraph that establishes context and scope]

## Background

[Historical context or foundational concepts]

## [Main concept]

[Discursive explanation with reasoning]

## Trade-offs

[Discussion of alternatives and why this approach was chosen]

## Further reading

- [Related resources]
```

**Reference template:**

```markdown
# [Component] Reference

## Overview

[Brief description of what this reference covers]

## [Section]

| Parameter | Type   | Default | Description |
| --------- | ------ | ------- | ----------- |
| `name`    | string | -       | Description |

## [API/Function/Command]

**Signature:** `function_name(param1, param2)`

**Parameters:**

- `param1` (type) - Description
- `param2` (type) - Description

**Returns:** Description of return value
```

1. Fill in content based on project analysis (source code, existing docs, configuration files)

### When Improving Existing Pages

If a page is already in the right category but needs improvement to better follow Diataxis principles:

1. Identify specific issues (mixed content, wrong tone, missing structure)
2. Present suggested changes to the user
3. Apply changes after approval

## Important Guidelines

- **Do not force the framework**: If the project is small and a single README covers everything
  well, say so. Diataxis is most valuable for projects with substantial documentation needs.
- **Be pragmatic**: A partially-organized documentation set is better than no documentation.
  Suggest incremental improvements rather than demanding perfection.
- **Preserve content**: When restructuring, never delete content. Move and reorganize,
  but keep all existing information.
- **Maintain links**: When moving files, update all cross-references and navigation configurations.
- **Respect the user's decisions**: If the user disagrees with a classification or restructuring
  suggestion, accept their decision and adjust accordingly.
