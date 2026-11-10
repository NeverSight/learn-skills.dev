---
name: project-deck
description: "Create a concise presentation deck that communicates a project's current state, decisions, evidence, risks, and next steps. Use when preparing a project update for collaborators, supervisors, or stakeholders. Not for a research talk centered on one paper; use $talk-deck."
allowed-tools: Bash(latexmk*), Bash(xelatex*), Bash(pdflatex*), Bash(mkdir*), Read, Write, Edit
argument-hint: "[project-name-or-path]"
---

# Project Deck Skill

> Create beautiful presentation decks to communicate project status to your future self and collaborators.

## Purpose

Based on Scott Cunningham's Part 7: "Making Beautiful Decks For My Future Self" - using decks not for public speaking but to efficiently communicate work status across time and to coauthors.

## The Philosophy

"I use decks to help me keep track of the work I was doing so that I can communicate it to my coauthors and myself later in the week when we meet to go over our projects."

Claude has absorbed the "rhetoric of decks" - the tacit knowledge about what makes presentations effective:
- One idea per slide
- Titles are assertions, not labels
- Lead with conclusions
- Visual hierarchy signals importance
- Repeat for retention
- Transition explicitly

## When to Use

- Before a supervisor meeting
- At the end of a research sprint
- When handing off to a coauthor
- When returning to a dormant project
- Weekly project status updates

## Workflow

1. **Read project context** - Progress logs, current focus, recent work
2. **Design deck structure**:
   - Research question
   - What's been done (with figures/tables)
   - Key findings so far
   - Current blockers
   - Next steps
3. **Create beautiful output** - Clean design, good typography, optimal cognitive density
4. **Include visuals** - Figures, tables, diagrams that capture the work

## Deck Rhetoric Principles

```markdown
## Principles for Effective Decks

1. **One idea per slide** - Don't overload
2. **Titles are assertions** - "Distance increases abortion rates" not "Results"
3. **Lead with conclusions** - Don't bury the lede
4. **Visual hierarchy** - Most important things stand out
5. **Optimal cognitive density** - Smooth delivery, not overloaded
6. **Beautiful figures and tables** - Data visualisation matters
7. **Explicit transitions** - Guide the reader through the narrative
```

## Extended Rhetoric Principles

### For Research Decks
- **Motivation slides**: Why should anyone care? What's the gap?
- **Methods slides**: Identification strategy in plain English, visualize variation
- **Results slides**: Lead with main coefficient, visualize where possible
- **Figures**: Clear titles, labeled axes, no chartjunk

### For "Decks as Thinking Tools"
When making decks for yourself/coauthors:
1. **Document decisions** — Why did we choose this approach?
2. **Visualize data** — Patterns you've discovered
3. **Track progress** — What's done, what's next
4. **Summarize code** — What scripts do what
5. **Capture context** — So future-you remembers

### Beamer Tips
- Custom themes > recognizable templates
- Metropolis or Madrid themes as starting points
- Sans-serif fonts for readability
- Generous margins and whitespace
- Compile without warnings (fix overfull hboxes)

## Example Prompt

"Create a project deck for my Indifference Adjustments paper. Read my progress logs and the current state of the project, then make a 10-slide deck that I can use in my supervisor meeting next week. Include the key figures and a clear 'what's next' section."
