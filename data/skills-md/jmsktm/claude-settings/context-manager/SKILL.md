---
name: Context Manager
slug: context-manager
description: Manage conversation context and memory for optimal AI performance
category: meta
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "manage context"
  - "clear context"
  - "summarize context"
  - "context window"
  - "optimize context"
tags:
  - context-management
  - memory
  - optimization
---

# Context Manager

The Context Manager skill helps you optimize conversation context to maintain Claude's effectiveness throughout long sessions. It tracks context window usage, identifies when to summarize or prune context, and helps you structure conversations to keep relevant information accessible while staying within token limits.

This skill is essential for complex, multi-day projects where conversation history grows large. It helps you decide what to preserve, what to summarize, and what to discard, ensuring Claude maintains awareness of important decisions and project state without hitting context limits.

Use this skill proactively during long development sessions, before starting new major features, or when you notice performance degradation due to context bloat.

## Core Workflows

### Workflow 1: Monitor Context Health
1. **Check** current context usage:
   - Token count
   - Percentage of limit
   - Recent growth rate
2. **Analyze** context composition:
   - How much is code?
   - How much is conversation?
   - How much is documentation?
3. **Identify** problematic areas:
   - Redundant information
   - Outdated references
   - Irrelevant tangents
4. **Assess** risk level:
   - Green: <50% usage, healthy
   - Yellow: 50-75% usage, monitor
   - Red: >75% usage, take action
5. **Recommend** actions if needed
6. **Report** status to user

### Workflow 2: Summarize Long Conversation
1. **Review** conversation history
2. **Extract** key information:
   - Decisions made
   - Problems solved
   - Current project state
   - Open questions
   - Next steps
3. **Organize** by topic/timeline
4. **Create** concise summary
5. **Validate** with user
6. **Suggest** starting new thread with summary

### Workflow 3: Prune Irrelevant Context
1. **Identify** candidates for removal:
   - Resolved issues
   - Abandoned approaches
   - Temporary debugging
   - Superseded information
2. **Categorize** by importance:
   - Safe to remove
   - Could summarize
   - Must preserve
3. **Propose** pruning plan to user
4. **Execute** approved removals
5. **Preserve** critical context
6. **Verify** coherence after pruning

### Workflow 4: Optimize Context Structure
1. **Analyze** current context organization
2. **Identify** inefficiencies:
   - Information scattered across conversation
   - Redundant explanations
   - Lack of structure
3. **Restructure** for efficiency:
   - Group related information
   - Create reference sections
   - Use concise formats
4. **Suggest** external documentation for:
   - Architecture decisions
   - API specifications
   - Configuration details
5. **Link** to external docs instead of inlining
6. **Validate** improved efficiency

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Check context status | "Check context window" or "How's our context?" |
| Summarize conversation | "Summarize this conversation" |
| Start fresh with summary | "Start new thread with summary" |
| Prune old context | "Clear old context" or "Prune conversation" |
| Optimize context structure | "Optimize our context" |
| Preserve key decisions | "Document key decisions" |
| Estimate context usage | "How much context are we using?" |

## Best Practices

- **Monitor Proactively**: Don't wait for performance issues
  - Check context before starting major features
  - Monitor after long debugging sessions
  - Review weekly on long-running projects

- **Summarize Regularly**: Compress history at natural breakpoints
  - End of feature development
  - After resolving major issues
  - Before switching contexts (dev → deployment)

- **Externalize Static Info**: Move unchanging content to files
  - Architecture docs
  - API specifications
  - Code style guides
  - Reference materials

- **Use Structured Formats**: Make information dense and scannable
  - Tables instead of prose
  - Bullet points instead of paragraphs
  - Code blocks instead of descriptions

- **Preserve Decisions**: Always keep the "why"
  - Why this approach was chosen
  - Why alternatives were rejected
  - What constraints influenced decisions

- **Discard Aggressively**: Be ruthless with temporary content
  - Debugging exploration
  - Failed experiments
  - Resolved issues
  - Superseded plans

- **Start Fresh Strategically**: Know when to begin new conversation
  - After major milestones
  - When switching to unrelated work
  - When context is >75% full
  - When performance degrades

- **Document Externally**: Use files for persistent knowledge
  - PIPELINE_STATUS.md for project state
  - DECISIONS.md for architecture choices
  - TODO.md for task lists
  - README.md for onboarding

## Context Optimization Strategies

### Strategy 1: Hierarchical Summarization
```
Long conversation →
  Detailed summary (50% reduction) →
    Executive summary (80% reduction) →
      Key decisions (95% reduction)
```

### Strategy 2: Time-Based Windowing
```
Keep in context:
- Last 1 hour: Full detail
- Last 4 hours: Summarized
- Last day: Key decisions only
- Older: Link to external docs
```

### Strategy 3: Topic-Based Partitioning
```
Separate threads for:
- Feature development
- Bug investigation
- Deployment/ops
- Architecture discussion

Link between threads as needed
```

### Strategy 4: Progressive Disclosure
```
Start with:
- Current task context only

Add on demand:
- Related decisions
- Relevant code
- Background information

Remove when done
```

## Context Health Checklist

Before starting a major task, verify:

- [ ] Context usage < 75%
- [ ] Recent decisions documented
- [ ] Obsolete information removed
- [ ] Current project state clear
- [ ] Next steps identified
- [ ] Relevant files/docs linked
- [ ] Debugging traces cleaned up

## Warning Signs of Context Issues

Watch for these indicators:

- **Responses get slower**: Processing large context
- **Information ignored**: AI misses recent context
- **Repetition**: AI re-explains known information
- **Loss of coherence**: AI forgets earlier decisions
- **Token limit warnings**: Approaching hard limits
- **Degraded accuracy**: Mistakes in previously solid areas

## External Memory Strategies

Move these to files, not context:

| Information Type | Best Storage |
|------------------|--------------|
| Project overview | README.md |
| Architecture decisions | ARCHITECTURE.md or ADRs |
| API contracts | OpenAPI spec or schema files |
| Current project state | PIPELINE_STATUS.md or TODO.md |
| Configuration | .env, config files |
| Code style rules | .eslintrc, prettier.config.js |
| Deployment process | DEPLOYMENT.md or CI/CD config |
| Team decisions | DECISIONS.md or meeting notes |

## Context Templates

### Project State Summary Template
```markdown
## Project: [Name]
- **Status**: [Current pipeline stage]
- **Current focus**: [What we're working on]
- **Last completed**: [Recent achievement]
- **Next steps**: [Immediate tasks]
- **Blockers**: [What's preventing progress]
- **Key decisions**: [Recent important choices]
```

### Decision Log Template
```markdown
## Decision: [Topic]
- **Date**: [When]
- **Context**: [Why we needed to decide]
- **Options considered**: [Alternatives]
- **Choice**: [What we decided]
- **Rationale**: [Why this choice]
- **Consequences**: [Trade-offs accepted]
```

### Session Summary Template
```markdown
## Session Summary: [Date]
- **Duration**: [How long]
- **Accomplished**: [What we built/fixed]
- **Decisions**: [Choices made]
- **Issues found**: [Problems discovered]
- **Next session**: [Where to continue]
```

## Advanced: Context Compression Techniques

For power users:

1. **Use references**: Link to code instead of pasting
   - "See function `processData` in `/src/utils/data.ts`"
   - Instead of: [pasting entire function]

2. **Leverage AI memory**: Store in knowledge graph
   - Key relationships between entities
   - Project-specific terminology
   - Team member roles and expertise

3. **Create abbreviations**: Define once, use everywhere
   - "FE" = Frontend, "BE" = Backend
   - "MR" = Merge Request, "PR" = Pull Request
   - Project-specific acronyms

4. **Use diff format**: Show changes, not entire files
   - Especially for code reviews
   - Before/after comparisons

5. **Batch similar information**: Group related items
   - All env vars in one block
   - All API endpoints in table
   - All dependencies in list
