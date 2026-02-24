---
name: codebase-study-guide
description: "Generate a pedagogically-grounded study guide for learning an unfamiliar codebase. Use when the user wants to onboard onto a codebase, understand a project's architecture, create learning materials for a team, or asks things like \"help me learn this codebase\", \"create an onboarding guide\", \"I'm new to this project\", \"how does this system work\", \"study guide for this repo\", or \"explain this codebase to me\". Produces a structured document that builds understanding from purpose to systems to patterns, using evidence-based learning techniques (elaborative interrogation, concept mapping, threshold concepts, worked examples, progressive disclosure)."
---

# Codebase Study Guide

Generate a study guide that builds durable understanding of a codebase using evidence-based learning techniques. The guide helps readers grasp not just what the code does, but why it exists and how its parts relate.

## Guiding Pedagogy

These principles shape every section of the guide. See [references/pedagogy.md](references/pedagogy.md) for the full research basis.

- **Purpose before structure.** Start with the problem being solved, not the file tree. Readers who understand the "why" form stronger schemas for the "how" (Ausubel's meaningful learning).
- **Threshold concepts first.** Identify the 2-3 ideas that, once grasped, make everything else click. Front-load these (Meyer & Land).
- **Progressive disclosure.** Layer complexity: overview -> systems -> interfaces -> internals. Never introduce more than one unfamiliar subsystem at a time (Cognitive Load Theory).
- **Active over passive.** Include prediction prompts, elaborative interrogation questions, and exploration tasks — not just descriptions. Active techniques outperform passive reading by d = 0.5-0.7 (Dunlosky et al.).
- **Dual coding.** Pair every textual explanation with a visual (diagram, map, flow). Dual-channel encoding roughly doubles recall (Paivio).
- **Name the patterns.** Explicitly identify architectural patterns and link to resources. Pattern recognition is the mechanism of expert code comprehension (Brooks, Soloway).

## Workflow

### Step 1: Scope the Guide

Use AskUserQuestion to understand the audience and focus:

```
question: "Who is the primary audience for this study guide?"
header: "Audience"
options:
  - label: "New team member"
    description: "Developer joining this team, needs full onboarding"
  - label: "Experienced dev, new codebase"
    description: "Senior engineer who knows the stack but not this project"
  - label: "Cross-team collaborator"
    description: "Someone who needs to interface with this system, not own it"
  - label: "Future me"
    description: "Personal reference for a codebase I'm exploring now"
```

Then clarify depth:

```
question: "What depth should the guide cover?"
header: "Depth"
options:
  - label: "Full guide (Recommended)"
    description: "Purpose, architecture, systems, patterns, interfaces, and exploration tasks"
  - label: "Architecture overview"
    description: "Purpose and high-level systems only, no deep dives"
  - label: "Specific subsystem"
    description: "Deep dive into one area of the codebase"
```

### Step 2: Explore the Codebase

Conduct systematic exploration using the Explore agent or direct tools. Investigate in this order:

1. **Entry points** — Where does execution begin? (`main`, route handlers, CLI entry, event listeners)
2. **Configuration** — What shapes behavior? (env vars, config files, feature flags)
3. **Domain model** — What are the core entities and their relationships?
4. **Primary flows** — Trace 2-3 representative operations end-to-end
5. **System boundaries** — Where does this code interact with external systems?
6. **Test structure** — What do tests reveal about intended behavior and edge cases?
7. **Existing docs** — README, CLAUDE.md, architecture docs, ADRs, inline comments

Also look for:
- Naming conventions and code organization patterns
- Error handling philosophy
- Key dependencies and what role they play

### Step 3: Identify Threshold Concepts

From the exploration, identify 2-3 codebase-specific threshold concepts — ideas that are:

- **Transformative**: Understanding them changes how you see the whole system
- **Integrative**: They connect previously unrelated parts
- **Non-obvious**: A newcomer wouldn't discover them from casual reading

Examples: "Everything is an event," "ownership determines lifecycle," "the config is the source of truth," "reads and writes are separate models."

### Step 4: Build the Concept Map

Before writing, create a mental model of the system as a concept map:

- **Nodes**: The 5-8 primary systems/modules
- **Edges**: How they communicate (function calls, events, shared state, HTTP, queues)
- **Direction**: Which way data/control flows

This becomes the "System Map" section of the guide and informs the sequencing of everything else.

### Step 5: Write the Guide

Follow the template structure in [references/guide-template.md](references/guide-template.md). Key principles while writing:

**For each system/module section:**
- Open with purpose ("why does this exist?") before mechanics ("how does it work?")
- Include an elaborative interrogation prompt — a "why" question that forces the reader to think about design tradeoffs
- Name any architectural pattern being used and link to a canonical resource
- Show a representative code snippet as a worked example — annotated with reasoning, not just syntax
- End with an exploration task the reader can do independently

**For the Mermaid diagrams:**
- Use `graph TD` for system architecture and data flow
- Use `sequenceDiagram` for request flows and interactions
- Use `classDiagram` for domain models with relationships
- Keep diagrams focused — one concept per diagram, not everything at once

**For the exploration tasks:**
- Follow the PRIMM progression: Predict -> Run -> Investigate -> Modify
- Start with prediction ("before looking at the code, what do you think happens when...?")
- Include specific file paths and function names to examine
- Graduate from guided exploration to independent investigation

### Step 6: Review and Deliver

Before delivering the guide:

1. **Check the "forest for the trees"** — Does a reader who finishes the guide understand *why this thing exists* and *what problem it solves for its users*? If the purpose section doesn't answer this compellingly, revise it.
2. **Check progressive disclosure** — Could a reader stop after Section 2 and still have useful understanding? After Section 3? Each section should be independently valuable.
3. **Check active elements** — Does every major section include at least one question or task? Remove any section that's purely passive description without an active learning prompt.
4. **Check pattern links** — Is every named pattern linked to a learning resource?

Write the guide as a single Markdown file placed at a sensible location (`.claude/docs/study-guide.md` or as specified by the user). The guide should be self-contained — a reader with access to the codebase and the guide should need nothing else.
