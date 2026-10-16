---
name: five-whys
description: Five Whys root cause analysis. Iteratively asks "why" to drill past symptoms to underlying causes. Use for debugging, investigating failures, or understanding why something went wrong.
---

# Five Whys Analysis

Perform iterative root cause analysis by asking "why" repeatedly until you reach the underlying cause.

## Instructions

Start with the stated problem and ask "why" it occurred. For each answer, ask "why" again. Continue until you reach a root cause that:

- Is actionable (you can do something about it)
- Is fundamental (asking "why" further leads to abstract/unhelpful answers)
- Explains the chain of causation

Typically this takes 5 iterations, but may be fewer or more.

### Output Format

**Problem Statement**
Restate the problem clearly and specifically.

**Why Chain**

  > Why did [problem]?
  > → [Answer 1]
  >
  > Why did [Answer 1]?
  > → [Answer 2]
  >
  > Why did [Answer 2]?
  > → [Answer 3]
  >
  > Why did [Answer 3]?
  > → [Root Cause]

**Root Cause**
The fundamental issue identified. Explain why this is the root (not just another symptom).

**Branches** (if applicable)
If multiple valid answers exist at any level, show the branching analysis which maybe
represented as mermaid `flowchart TD` diagrams - aim to keep this simple in most cases.

**Corrective Actions**

- Immediate: What to do now to address the symptom
- Systemic: What to change to prevent recurrence

**Verification**
How will you confirm the root cause is correct? (Test the hypothesis)

## Guidelines

- Each answer should be factual and verifiable
- Avoid blame ("John didn't do X")—focus on systems and processes
- If you're guessing, note it as a hypothesis to verify
- Watch for circular logic
- It's okay to branch if there are multiple valid causes
- Stop when further "why" questions become philosophical or unhelpful

Answer each Why clearly and list any immediate actions which can be taken, and any systemic
risks which should be addressed. Provide source references the cause of systemic issues.
Ask useful questions if you don't believe you have access to relevant context.

## Early Exit

You may cut short the chain of reasoning if either the root cause has been found with
exhausted exploration. The skill should recommend to use appropriate tools which will
gather effective context on the problem. If these tools have not been provided, state
what context is missing and which skills would be beneficial.
