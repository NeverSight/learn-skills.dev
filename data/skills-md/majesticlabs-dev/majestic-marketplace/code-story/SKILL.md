---
name: code-story
description: Narrative templates for git history documentation. Used by /git:code-story command.
disable-model-invocation: true
---

# Code Story Skill

Provides narrative templates for transforming git history into documentary-style stories.

## Templates

Read the appropriate template based on detail level:
- [references/minimal-template.md](references/minimal-template.md) - 1-2 page executive summary
- [references/standard-template.md](references/standard-template.md) - 5-10 page story with acts
- [references/comprehensive-template.md](references/comprehensive-template.md) - 20+ page deep dive

## Narrative Guidelines

### Voice and Tone
- Documentary style: informative yet engaging
- Third-person perspective
- Acknowledge the human element
- Find the drama in technical decisions
- Celebrate achievements without hyperbole

### What Makes a Good Code Story
- **Genesis moment**: First commit sets the stage
- **Character development**: Contributors evolve
- **Conflict and resolution**: Bugs, refactors, breaking changes
- **Turning points**: Direction-changing decisions
- **Present connection**: Link past to current state

### Commit Citation Format
- Short SHA in backticks: `abc1234`
- Include date and author for key commits
- Link to GitHub if remote is github.com
