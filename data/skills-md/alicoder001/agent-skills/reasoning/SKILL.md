---
name: reasoning
description: Chain-of-thought reasoning, self-reflection, and systematic problem-solving patterns for AI agents. Use before any complex task to ensure logical and accurate solutions.
---

# Reasoning Patterns

> Systematic thinking for accurate problem solving.

## Instructions

### 1. Chain-of-Thought (CoT)

Break complex problems into explicit reasoning steps:

```
PROBLEM → ANALYZE → DECOMPOSE → SOLVE STEPS → VERIFY → SYNTHESIZE
```

```markdown
## Thinking Process

1. **Understand**: What is being asked?
2. **Identify**: What information do I have?
3. **Plan**: What steps will solve this?
4. **Execute**: Work through each step
5. **Verify**: Is the solution correct?
```

### 2. Self-Reflection Protocol

Before finalizing any output:

```markdown
## Reflection Checklist

- [ ] Does this answer the actual question?
- [ ] Are there any logical errors?
- [ ] Did I miss edge cases?
- [ ] Is this the simplest solution?
- [ ] Would a senior developer approve this?
```

### 3. Problem Decomposition

```typescript
// ❌ Bad: Trying to solve everything at once
function solveComplexProblem() {
  // 500 lines of tangled logic
}

// ✅ Good: Decomposed into clear steps
function solveComplexProblem() {
  const parsed = parseInput();
  const validated = validateData(parsed);
  const processed = processData(validated);
  return formatOutput(processed);
}
```

### 4. Verification Strategies

| Strategy | When to Use |
|----------|-------------|
| **Trace Through** | Algorithm logic |
| **Edge Cases** | Input validation |
| **Type Check** | TypeScript code |
| **Unit Test** | Critical functions |
| **Dry Run** | Complex flows |

### 5. Error Detection

```markdown
## Common Reasoning Errors

1. **Assumption Error**: Assuming facts not stated
2. **Logic Gap**: Missing intermediate steps
3. **Scope Creep**: Solving wrong problem
4. **Premature Optimization**: Overcomplicating
5. **Confirmation Bias**: Ignoring alternatives
```

### 6. Reasoning Template

Use this template for complex tasks:

```markdown
## Task: [Description]

### Understanding
- Goal: [What we need to achieve]
- Constraints: [Limitations]
- Inputs: [Available data]

### Approach
1. Step 1: [Description]
2. Step 2: [Description]
3. Step 3: [Description]

### Execution
[Work through each step]

### Verification
- [ ] Goal achieved
- [ ] Constraints satisfied
- [ ] No side effects

### Reflection
- What worked: [...]
- What could improve: [...]
```

## References

- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- [Self-Consistency Improves CoT](https://arxiv.org/abs/2203.11171)
