---
name: memory
description: Working memory management, context prioritization, and knowledge retention patterns for AI agents. Use when you need to maintain relevant context and avoid information loss during long tasks.
---

# Memory Management

> Efficient context and knowledge management.

## Instructions

### 1. Working Memory Model

```
┌─────────────────────────────────────────┐
│           WORKING MEMORY                │
├─────────────────────────────────────────┤
│ • Current task goal                     │
│ • Relevant file contents                │
│ • Recent decisions                      │
│ • Active constraints                    │
└─────────────────────────────────────────┘
          ↑ Load        ↓ Store
┌─────────────────────────────────────────┐
│          LONG-TERM MEMORY               │
├─────────────────────────────────────────┤
│ • Project structure                     │
│ • User preferences                      │
│ • Past solutions                        │
│ • Domain knowledge                      │
└─────────────────────────────────────────┘
```

### 2. Context Prioritization

Order of importance for context:

| Priority | Content | Action |
|----------|---------|--------|
| 🔴 Critical | Current task, active file | Always keep |
| 🟠 High | Related files, types | Keep if relevant |
| 🟡 Medium | Project structure | Summarize |
| 🟢 Low | History, logs | Forget if needed |

### 3. Information Retention

```markdown
## What to Remember

✅ Keep in context:
- Current task objective
- File being modified
- Type definitions in use
- Recent error messages
- User preferences

❌ Safe to forget:
- Already processed files
- Resolved errors
- Intermediate calculations
- Verbose logs
```

### 4. Context Summarization

When context grows too large:

```markdown
## Summarization Rules

1. **Files**: Keep imports, types, key functions
2. **Errors**: Keep message, remove stack trace
3. **Logs**: Keep last 10 lines
4. **History**: Keep decisions, remove process

### Example

Before (verbose):
"I looked at file A, then file B, noticed pattern X,
then explored file C, found issue Y, traced it to..."

After (summarized):
"Analyzed A, B, C. Found: pattern X, issue Y in C."
```

### 5. Session State Pattern

```typescript
// Conceptual session state
interface SessionMemory {
  // Always retain
  task: {
    goal: string;
    status: 'planning' | 'executing' | 'verifying';
    progress: number;
  };
  
  // Retain while relevant
  context: {
    activeFiles: string[];
    recentDecisions: string[];
    constraints: string[];
  };
  
  // Summarize or forget
  history: {
    summary: string;
    keyInsights: string[];
  };
}
```

### 6. Knowledge Retrieval

```markdown
## Before Starting New Task

1. Check: Have I seen this before?
2. Recall: What approach worked?
3. Apply: Use proven patterns
4. Adapt: Modify for current context
```

### 7. Memory Hygiene

```markdown
## Per-Turn Cleanup

After completing a step:

1. ✅ Task still relevant? Keep
2. ❓ Might need later? Summarize
3. ❌ No longer needed? Forget

## End of Task

1. Extract learnings
2. Update knowledge base
3. Clear working memory
```

### 8. Context Window Management

```markdown
## Token Budget Allocation

| Category | Budget |
|----------|--------|
| System prompt | 10% |
| Task context | 30% |
| Active code | 40% |
| Conversation | 20% |

## When Near Limit

1. Summarize conversation history
2. Remove resolved issues
3. Keep only relevant code sections
4. Preserve critical context
```

## References

- [Working Memory in LLMs](https://arxiv.org/abs/2309.02427)
- [Context Compression](https://arxiv.org/abs/2310.06839)
