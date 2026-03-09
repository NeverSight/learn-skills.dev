---
name: capture-learning
description: "Capture comprehensive problem-solving narratives from work sessions, documenting the journey of discovery"
---

# Capture Learning

Capture comprehensive problem-solving narratives from our work sessions, documenting not just the solution but the entire journey of discovery.

## Purpose

This command captures the full narrative of problem-solving: what we thought was true, what we discovered was actually true, the troubleshooting journey, and the lessons learned. This narrative format makes it easy to harvest insights for updating documentation, commands, or pipelines.

## Usage

```bash
# Interactive mode - guides you through the narrative
bun ~/.claude/skills/capture-learning/scripts/capture-learning.ts

# Direct mode with full narrative (all 6 arguments)
bun ~/.claude/skills/capture-learning/scripts/capture-learning.ts "problem" "initial assumption" "actual reality" "troubleshooting steps" "solution" "key takeaway"
```

## Trigger Phrases

When you say any of these, I'll capture our learning:
- "Great job, log this"
- "Nice work, make a record"
- "Document this"
- "Capture this learning"
- "Save this for later"
- "That worked!"

## The Narrative Structure

The command captures a complete story with these elements:

1. **The Problem** - What issue did we encounter?
2. **Initial Assumption** - "We thought this was true..."
3. **Actual Reality** - "What we realized was actually true..."
4. **Troubleshooting Journey** - Steps we took to discover the truth
5. **The Solution** - What finally worked
6. **The Takeaway** - "So now we know..." or "So now we do it this way..."
7. **Promote to Global?** - Optionally write to `~/.claude/learnings/global-patterns.md` for cross-project knowledge

## Why This Format?

This narrative approach helps us:
- Remember the journey, not just the destination
- Understand WHY the solution works
- Recognize similar patterns in future problems
- Update our mental models and documentation
- Share knowledge effectively with others

## Output

Files are saved to: `<project-root>/.claude/learnings/YYYY-MM-DD-problem-description.md`

If not inside a git repository, falls back to `~/.claude/learnings/`.

Each file contains:
- Full narrative story
- Before/after comparison
- Technical details and commands used
- Actionable takeaways for future reference

### Making learnings active

Claude Code doesn't automatically read the learnings directory. Add this to your project's `CLAUDE.md` so Claude checks them each session:

```markdown
## Learnings
Before starting work, check `.claude/learnings/` for relevant past
problem-solving narratives. Apply those lessons instead of repeating
mistakes.

**IMPORTANT:** After solving any non-trivial debugging session or
discovering something that contradicts an initial assumption, invoke
`/capture-learning` before moving on. Do not skip this step.
```

## Implementation

The TypeScript implementation is in `scripts/capture-learning.ts`.

The command:
- Prompts for all 6 narrative elements if not provided
- Detects the git root and saves to `<project>/.claude/learnings/`
- Names files with date and problem description
- Generates a comprehensive learning narrative
