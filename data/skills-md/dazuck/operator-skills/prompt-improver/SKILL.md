---
name: prompt-improver
description: Transform any rough prompt, task description, or job into an optimized AI instruction prompt. Use when users ask to "improve this prompt", "make this better for an AI", "optimize this for Claude/GPT", or provide raw instructions that need refinement into a well-structured prompt following best practices.
---

# Prompt Improver

Transform rough prompts or task descriptions into optimized AI instruction prompts using proven best practices. This skill takes any starting prompt—from a single sentence to a complex job description—and returns a polished, effective prompt that leverages AI capabilities optimally.

## Core Approach

When improving a prompt, focus on:

1. **Understanding intent** - Identify what the user actually wants to accomplish
2. **Adding strategic structure** - Organize information for maximum clarity
3. **Enhancing with proven techniques** - Apply relevant best practices without over-engineering
4. **Preserving flexibility** - Avoid rigid constraints that limit AI intelligence
5. **Maintaining naturalness** - Keep language conversational and clear

## Improvement Process

### 1. Analyze the Original Prompt

Identify:

- Core task or goal
- Implicit requirements or constraints
- Missing context that would help
- Ambiguities or unclear elements
- Opportunities for enhancement

### 2. Determine Appropriate Enhancements

Based on the task, selectively apply:

**Persona/Expertise** - Add role context when relevant:

- For technical tasks: "You are an experienced [domain] engineer"
- For creative work: "You are a creative [role] with expertise in [area]"
- For analysis: "You are a thoughtful analyst skilled in [domain]"

**Structure and Clarity**:

- Clear task statement upfront
- Relevant context and background
- Specific requirements separated from general instructions
- Output format specifications

**AI-Optimized Techniques**:

- Step-by-step reasoning requests for complex tasks
- Examples (1-3) showing desired input/output patterns when helpful
- Encouragement for high-stakes tasks ("This is important" / "Take your time")
- XML tags or clear delimiters to separate sections

**Constraints and Guardrails**:

- Length or scope boundaries
- Style, tone, or audience specifications
- What to include/exclude
- Success criteria (when genuinely needed)

### 3. What NOT to Add

Avoid over-specification:

- **No rigid rubrics** - Trust the AI's judgment rather than mechanical scoring systems
- **No excessive checklists** - Unless consistency across repetitive tasks is critical
- **No redundant instructions** - State things once clearly
- **No over-explanation** - Claude is smart; provide what it doesn't already know
- **No artificial formality** - Keep language natural

### 4. Structure the Improved Prompt

Organize using this flexible template:

```
[Optional: Relevant role or expertise context]

[Core task - what you want accomplished]

[Background context - why this matters, relevant information]

[Specific requirements and constraints]

[Examples - if they genuinely help, use 1-3]

[Output format specifications]

[Success criteria - only if needed for clarity]
```

Adapt this structure to fit the task naturally. Not every prompt needs every section.

## Techniques Reference

For detailed best practices, see `references/prompting-best-practices.md` which covers:

- Core principles (clarity, structure, leveraging AI strengths)
- Effective techniques (persona, examples, reasoning, formatting)
- Quality indicators and patterns
- What to avoid

Read this reference when:

- You need deeper understanding of a specific technique
- The task requires advanced prompting strategies
- You want to verify best practices for edge cases

## Examples

**Before**: "Write something about AI safety"

**After**:

```
Write a clear, balanced explanation of AI safety challenges and approaches.

Context: This is for a general audience interested in understanding current AI safety concerns without deep technical background.

Cover:
- Key safety challenges (alignment, robustness, interpretability)
- Current approaches and research directions
- Why this matters for AI development
- Open questions and debates in the field

Aim for approximately 500-800 words. Use clear examples to illustrate abstract concepts. Maintain an informative but accessible tone—avoid both hype and excessive pessimism.
```

**Before**: "Help me analyze data"

**After**:

```
You are a data analyst skilled in exploratory analysis and insight generation.

Analyze the provided dataset to identify:
1. Key patterns and trends
2. Anomalies or outliers worth investigating
3. Relationships between variables
4. Actionable insights or recommendations

Context: This analysis will inform business strategy decisions for Q4 planning.

Process:
- First, examine the data structure and completeness
- Look for statistical patterns and correlations
- Identify what's surprising or noteworthy
- Frame findings in business terms

Provide your analysis in clear sections with visualizations described where helpful. Focus on insights that would influence decisions rather than just describing what's in the data.
```

## Output Format

Present the improved prompt clearly:

1. Show the transformed prompt ready to use
2. Briefly explain key improvements made (2-3 sentences)
3. Offer to iterate if the user wants adjustments

Keep explanations concise—the improved prompt should speak for itself.

## Resources

This skill includes:

- `references/prompting-best-practices.md` - Comprehensive guide to effective prompting techniques, principles, and patterns. Load this when you need deeper understanding of specific techniques or are working with complex prompting scenarios.
