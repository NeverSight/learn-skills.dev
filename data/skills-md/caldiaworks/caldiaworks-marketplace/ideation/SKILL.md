---
name: ideation
version: 0.1.0
description: >-
  Turn rough ideas into structured, validated idea documents through collaborative dialogue.
  Explores context, asks clarifying questions one at a time, proposes alternative approaches
  with feasibility evaluation, and produces documents ready for requirements definition.
  Use when: "ideation", "brainstorm", "new idea", "explore an idea", "I want to build",
  "what if we", "let's think about", "propose approaches", "evaluate this idea",
  "idea document", "アイデア出し", "案出し", "ブレスト", "アイデアを整理", "検討したい".
---

# Ideation: Ideas Into Structured Documents

Help turn rough ideas into structured, validated idea documents through natural collaborative dialogue. Start by understanding the current project context, then ask questions one at a time to refine the idea. Once the idea is clear, present approaches with feasibility evaluation and get user approval.

Do NOT skip to implementation. The purpose of this skill is to produce a well-thought-out idea document that can feed into requirements definition (e.g., USDM) or be tracked as a task. Even if the idea seems simple, unexamined assumptions cause the most wasted work.

## Process

Complete these steps in order:

### Step 1: Explore Context

Review the current project to understand what already exists:

- Check project files, documentation, and recent commits
- Identify existing solutions, patterns, and conventions
- Note constraints, dependencies, and technical boundaries

This grounds the ideation in reality rather than starting from a blank slate.

### Step 2: Ask Clarifying Questions

Understand the idea through focused dialogue:

- Ask **one question at a time** — do not overwhelm with multiple questions
- Prefer **multiple choice questions** when feasible — easier to answer than open-ended
- Focus on understanding: purpose, target users, constraints, success criteria
- Be ready to revisit earlier questions if new information changes the picture

Continue until you have a clear understanding of what the user wants and why.

### Step 3: Propose Approaches

Present 2-3 different approaches with trade-offs:

- Lead with your recommended approach and explain why
- Present options conversationally with reasoning
- Each approach must include a feasibility evaluation:
  - **Differentiation**: How does this differ from existing solutions?
  - **Technical risks and constraints**: What could go wrong technically?
  - **Pre-mortem**: "If this idea fails, what would be the cause?"
- Apply YAGNI — remove unnecessary features from all approaches

### Step 4: Present and Validate

Once the user selects an approach (or a combination):

- Present the idea in sections, scaled to complexity
- Ask after each section whether it looks right so far
- Be ready to go back and revise if something does not make sense

### Step 5: Write Idea Document

After the user approves the idea, generate the document.

Save to: `.docs/ideas/YYYY-MM-DD-<topic>.md`

The document must contain these sections:

| Section | Content |
|---------|---------|
| **What** | What it does, the problem it solves |
| **Why** | Rationale, user benefit, business value |
| **Scope** | In scope / out of scope boundaries |
| **Stakeholders** | Target users, affected systems |
| **Approaches** | The explored alternatives with trade-offs and feasibility evaluation |
| **Decision** | The selected approach and rationale |

See `templates/idea-document.md` for the output template.

These sections are structured to serve as input for requirements definition tools (e.g., USDM):

- **What** maps to Requirements
- **Why** maps to Reasons
- **Scope** maps to Descriptions (context, constraints)
- **Stakeholders** informs scope confirmation

### Step 6: Output Selection

After writing the idea document, ask the user which output they want:

| Option | Action |
|--------|--------|
| **A: Markdown only** (default) | Save the idea document to `.docs/ideas/` — done |
| **B: Markdown + GitHub Issue** | Save the document and create a GitHub Issue with the content |
| **C: Markdown + requirements** | Save the document and invoke a requirements definition skill (e.g., `usdm`) |

## Key Principles

- **One question at a time** — do not bundle multiple questions in one message
- **Multiple choice preferred** — easier to answer than open-ended when feasible
- **YAGNI ruthlessly** — remove unnecessary features from all approaches
- **Explore alternatives** — always propose 2-3 approaches before settling
- **Incremental validation** — present sections, get approval, then move on
- **Be flexible** — go back and clarify when something does not make sense
- **Feasibility over optimism** — every approach needs honest risk assessment

## Credits

This skill is based on the brainstorming skill from [obra/superpowers](https://github.com/obra/superpowers) (MIT License).
