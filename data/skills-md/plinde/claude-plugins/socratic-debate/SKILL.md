---
name: socratic-debate
description: This skill should be used when conducting structured multi-perspective debates to stress-test ideas, evaluate tradeoffs, or reach well-reasoned decisions. Provides the Socratic debate framework with 4 subagent roles.
---

# Socratic Debate Framework

A structured approach to deliberation using multiple AI perspectives to stress-test ideas and reach well-reasoned conclusions.

## When to Use

- Evaluating whether to accept or reject a proposal (PR feedback, RFC, design decision)
- Making architectural or technology choices with significant tradeoffs
- Deciding whether something is worth the effort/complexity
- Any situation where "it depends" is the initial answer

## The Four Perspectives

### 1. Advocate FOR (Proponent)

**Role:** Make the strongest possible case in favor of the position.

**Mindset:**
- Assume the proposal has merit and find the best reasons why
- Consider benefits that may not be immediately obvious
- Think about precedent, standards, and long-term implications
- Acknowledge weaknesses only if doing so strengthens credibility

**Output format:** 250-400 word persuasive argument with a memorable closing line.

### 2. Advocate AGAINST (Devil's Advocate)

**Role:** Stress-test the idea by making the strongest counterargument.

**Mindset:**
- Look for hidden costs, complexity, or unintended consequences
- Question whether the problem being solved is overstated
- Identify alternative approaches that might be simpler
- Consider opportunity cost and what else could be done instead

**Output format:** 250-400 word counterargument with a memorable closing line.

**Important:** The goal is constructive challenge, not dismissal. A good devil's advocate helps strengthen ideas.

### 3. Neutral Analyst

**Role:** Objectively weigh both sides and identify the key tradeoffs.

**Mindset:**
- Remain impartial while still being willing to draw conclusions
- Identify where the debaters agree (often more than expected)
- Surface context or constraints that affect the decision
- Consider hybrid approaches or middle grounds

**Output format:**
1. Balanced analysis (200 words)
2. Tradeoffs table (if applicable)
3. Preliminary verdict with confidence level (low/medium/high)

### 4. Scribe/Moderator

**Role:** Synthesize all perspectives into a coherent summary and final verdict.

**Responsibilities:**
- Extract the most compelling points from each perspective
- Identify areas of agreement across all three debaters
- Resolve conflicts by weighing evidence quality
- Deliver a clear, actionable recommendation

**Output format:**
```markdown
## Socratic Debate Summary

### Topic
[Original question/topic]

### FOR (Proponent)
[Key points summarized]

### AGAINST (Devil's Advocate)
[Key points summarized]

### NEUTRAL (Analyst)
[Key tradeoffs identified]

### Points of Agreement
[What all perspectives agreed on]

### Moderator's Verdict
**Recommendation:** [accept/reject/modify/defer]
**Confidence:** [low/medium/high]
**Key Factor:** [The decisive consideration]

### Suggested Next Steps
[If applicable]
```

## Debate Principles

### Intellectual Honesty
- Debaters should make their best arguments, not strawmen
- Acknowledge strong points from other perspectives
- Distinguish between facts, interpretations, and opinions

### Steelmanning
- Each perspective should address the strongest version of opposing arguments
- Avoid attacking weak or irrelevant points
- Give credit where due

### Actionable Outcomes
- The goal is a decision, not endless deliberation
- Every debate should end with a clear recommendation
- Include confidence levels to indicate certainty

### Appropriate Scope
- Focus on the specific question at hand
- Avoid scope creep into tangential issues
- Time-box arguments to maintain focus

## Example Debate Topics

| Category | Example Topic |
|----------|---------------|
| Code Review | "Should we require this change before merging?" |
| Architecture | "Should we adopt microservices for this system?" |
| Process | "Is the added ceremony of RFCs worth it for this team?" |
| Technology | "Should we migrate from X to Y?" |
| Prioritization | "Is this bug fix more urgent than feature work?" |

## Anti-Patterns to Avoid

1. **False Balance** - Not all positions deserve equal weight; evidence matters
2. **Analysis Paralysis** - The goal is a decision, not perpetual debate
3. **Bikeshedding** - Don't let low-stakes issues consume debate resources
4. **Motivated Reasoning** - Debaters should follow evidence, not justify predetermined conclusions
5. **Ignoring Context** - Recommendations should account for real-world constraints

## Integration with Workflows

The Socratic debate format works well for:

- **PR Reviews** - Post the debate summary as a comment
- **ADRs** - Include debate summary in the "Considered Alternatives" section
- **RFCs** - Use as structured feedback before approval
- **Retrospectives** - Debate proposed process changes
- **Incident Reviews** - Evaluate proposed preventive measures
