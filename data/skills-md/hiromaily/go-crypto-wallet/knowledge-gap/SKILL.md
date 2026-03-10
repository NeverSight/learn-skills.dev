---
name: knowledge-gap
description: Post-task knowledge gap review and proposals for improving skills/rules
---

# Knowledge Gap Review

Run this after completing a task to identify issues in information retrieval and propose candidates for improving skills/rules.

## Purpose

A skill for AI-assisted development that helps verbalize project-specific tacit knowledge and continuously improve the knowledge base.

## When to Use

- During self-review after completing a task
- When you felt unsure during implementation
- When you had to repeatedly refer to existing code

## Review Process

### Step 1: Reflection Perspectives

Review the most recent task from the following perspectives:

1. **Items that took time to research**
   - Information that required three or more tool calls to find
   - Implicit patterns understood by referencing multiple parts of existing code
   - Areas where you had to proceed by guessing because documentation was not found

2. **Items where decisions were difficult**
   - Cases with multiple possible implementation approaches
   - Situations where you checked existing patterns for error codes or naming conventions
   - Parts where you were not confident whether your choice was correct

3. **Information missing from existing skills/rules**
   - Cases where you referenced a skill but the required information was missing
   - Mistakes or rework that could have been avoided if a rule had existed

### Step 2: Classify the Issues

Classify the identified issues based on the following criteria:

| Difficulty | Criteria                                               |
| ---------- | ------------------------------------------------------ |
| High       | Took more than 10 minutes / required multiple files    |
| Medium     | Took 5–10 minutes / referenced 1–2 existing files      |
| Low        | Less than 5 minutes / easy to find but worth recording |

### Step 3: Propose Where to Maintain Them

Propose the appropriate destination based on the nature of each issue:

| Destination          | Suitable Cases                                                  |
| -------------------- | --------------------------------------------------------------- |
| `.claude/skills/`    | Knowledge referenced during specific tasks (invoked by command) |
| `.claude/rules/`     | Rules that should always be applied (auto-loaded)               |
| `CLAUDE.md`          | Project-wide principles and architecture                        |
| Update existing file | Can be handled by extending an existing skill/rule              |

## Output Format

Output the results using the following format:

```markdown
## Knowledge Gap Review Results

### Identified Issues

| Item         | Difficulty   | Recommended Location           | Summary             |
| ------------ | ------------ | ------------------------------ | ------------------- |
| (Issue name) | High/Med/Low | .claude/rules/go/repository.md | (Brief description) |

### Details

#### 1. (Issue name)

**Current Problem**:
(What made it difficult)

**Required Information**:

- (Specific information that was needed 1)
- (Specific information that was needed 2)

**Recommended Action**:
(File name and a summary of what should be added)

---

### Next Steps

- [ ] Create a GitHub issue (label: `ai-knowledge-gap`)
- [ ] Create or update skill/rule files
```

---

## Example

```
/knowledge-gap
```

After execution, the AI reviews the most recent task and outputs the identified issues and proposals in the format above.

---

## Related

- Existing skills: `.claude/skills/`
- Existing rules: `.claude/rules/`
- CLAUDE.md: `CLAUDE.md`
- GitHub label: `ai-knowledge-gap` (for tracking issues)
