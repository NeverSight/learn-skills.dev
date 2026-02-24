---
name: rebuttal-writing
description: Write point-by-point rebuttals to reviewer comments. Extract concerns from reviews, generate evidence-based responses, and format as a structured rebuttal document. Use after receiving peer review feedback.
argument-hint: [reviews-file]
---

# Rebuttal Writing

Generate structured, evidence-based rebuttals to peer review comments.

## Input

- `$0` — Reviewer comments (text file, or pasted directly)
- Optional: current paper draft for reference

## References

- Rebuttal prompts and format templates: `~/.claude/skills/rebuttal-writing/references/rebuttal-prompts.md`

## Workflow

### Step 1: Parse Review Comments
For each reviewer:
1. Extract individual concerns/questions/weaknesses
2. Categorize each: major concern, minor concern, question, suggestion
3. Identify the core issue behind each concern

### Step 2: Generate Responses
For each concern:
1. **Acknowledge** the reviewer's point
2. **Respond with evidence** — cite specific sections, equations, experiments, or results from the paper
3. **Describe what was done** (not what will be done) — "We have added...", "Our experiments show..."
4. If additional experiments are needed, describe the new results concretely

### Step 3: Format Rebuttal
Use the standard rebuttal format:

```
# Response to Reviewers

We thank all reviewers for their constructive feedback. We address each concern below.

## Reviewer #1

**Concern #1:** [extracted concern]
**Author Response:** [detailed response with evidence]

**Concern #2:** [extracted concern]
**Author Response:** [detailed response with evidence]

## Reviewer #2
...
```

### Step 4: Summary of Changes
Add a brief summary at the top listing all major changes made to the paper:
- New experiments added
- Sections revised
- Clarifications made

## Rules

- **Reply with what was done, not what will be done** — "We have conducted additional experiments" not "We will conduct..."
- **Be specific** — Reference exact sections, table numbers, equation numbers
- **Be respectful** — Thank reviewers, acknowledge valid concerns
- **Address every concern** — Do not skip any reviewer point
- **Provide evidence** — Every response should include concrete data, citations, or reasoning
- **Keep responses concise** — Detailed enough to address the concern, but not padded
- **Highlight changes** — When referring to modified text, use blue text or clearly mark revisions

## Related Skills
- Upstream: [self-review](../self-review/), [paper-revision](../paper-revision/)
- Downstream: [paper-compilation](../paper-compilation/)
- See also: [data-analysis](../data-analysis/)
