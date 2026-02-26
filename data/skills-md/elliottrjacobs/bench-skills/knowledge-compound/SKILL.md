---
name: knowledge-compound
description: Document solutions, decisions, and learnings into a searchable knowledge base. Use when the user says "document this", "compound this", "save this solution", "capture this", or after completing significant work that uncovered reusable knowledge.
allowed-tools: ["Read", "Glob", "Grep", "Write", "AskUserQuestion"]
---

# /knowledge-compound — Document Solutions & Learnings

Capture solutions, decisions, and learnings into a searchable knowledge base at `docs/solutions/`. Makes every unit of work compound into future productivity.

## When to Use

- After solving a tricky bug
- After making an architectural decision
- After a session with useful discoveries
- User says "document this", "compound this", "save this"
- After completing `/engineer-work` or `/engineer-review`

## Process

### Step 1: Determine What to Document

Ask the user what they want to capture:

```
AskUserQuestion:
  question: "What would you like to document?"
  options:
    - "A problem and its solution"
    - "An architectural decision"
    - "A pattern or technique I discovered"
    - "A session summary (multiple learnings)"
```

### Step 2: Gather Context

Based on the type:

**Problem/Solution:**
- What was the problem? (symptoms, error messages)
- What caused it? (root cause)
- What fixed it? (the solution with key code)
- What didn't work? (dead ends worth documenting)
- How to prevent it? (prevention strategy)

**Architectural Decision:**
- What was the decision?
- What options were considered?
- Why was this option chosen? (rationale)
- What are the tradeoffs?
- When would you revisit this?

**Pattern/Technique:**
- What is the pattern?
- When should it be used?
- Example implementation
- Gotchas or edge cases

**Session Summary:**
- What were the key decisions made?
- What problems were encountered and solved?
- What patterns were established?
- What's left to do?

If context is available from the current conversation (recent problem-solving, code changes), extract it automatically and confirm with the user rather than asking from scratch.

### Step 3: Write the Document

Use the solution template from [references/solution-template.md](references/solution-template.md).

**YAML frontmatter is critical** — it enables future searchability:

```yaml
---
title: "Clear, searchable title"
date: YYYY-MM-DD
category: auth|database|api|ui|state|navigation|performance|testing|deployment|typescript|tooling|architecture|mobile|general
tags: [minimum 2, maximum 8 relevant tags]
difficulty: low|medium|high
applicability: specific|moderate|broad
---
```

**Category selection rules:**
- Choose the most specific matching category
- If multi-category, choose the root cause category
- Use tags for secondary categories

### Step 4: Save

Save to `docs/solutions/YYYY-MM-DD-<slug>.md` where slug is a short, descriptive kebab-case name.

If `docs/solutions/` doesn't exist, create it.

### Step 5: Confirm

Show the user the file path and a brief summary of what was captured. Suggest related skills:

- Want to create a plan from this? → `/engineer-plan`
- Want to continue building? → `/engineer-work`
- More to document? → Run `/knowledge-compound` again
