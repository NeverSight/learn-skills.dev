---
name: prompt-optimizer
description: Transforms vague or simple user prompts into high-quality, structured, and high-performance AI instructions using systematic optimization techniques like XML tagging, few-shot examples, and Chain-of-Thought. Use this skill when you need to improve the reliability, accuracy, or formatting of an AI's output.
---

# Prompt Optimizer

This skill enables agents to systematically optimize prompts based on the "AI as a New Employee" philosophy. It applies structural, contextual, and technical enhancements to ensure AI models perform tasks with maximum clarity and precision.

## Instructions

### 1. Analysis Phase

Before generating the optimized prompt, analyze the following in a `<thinking>` block:

- **Core Objective**: What is the primary goal?
- **Target Audience**: Who will consume the output?
- **Professional Role**: What persona best fits this task?
- **Complexity**: Does it require step-by-step reasoning (Chain-of-Thought)?
- **Structure**: Which XML tags are needed to organize the components?

### 2. Construction Phase

Build the optimized prompt using these mandatory components:

- **`<role>`**: Define a specialized persona with relevant expertise.
- **`<context>`**: Provide background information and the "why" behind the task.
- **`<task>`**: State the instructions clearly and concisely.
- **`<requirements>`**: List specific success criteria and constraints.
- **`<output_format>`**: Define the expected structure (e.g., JSON, Markdown).

### 3. Enhancement Phase

- **XML Tagging**: Wrap different sections in clear XML tags for structural clarity.
- **Few-shot Examples**: Include 2-3 high-quality `<example>` blocks if the task is pattern-based.
- **Chain-of-Thought**: For complex logic, instruct the AI to reason inside `<thinking>` tags.
- **Response Prefilling**: If a strict format is required, provide the starting characters of the response.

## Examples

### Example 1: Simple to Structured

**Input**: "Write a product description for a smartwatch."
**Optimized Output**:

```markdown
<role>
Senior Marketing Copywriter specializing in wearable technology.
</role>

<context>
We are launching the 'Apex-1' smartwatch targeting fitness enthusiasts who value data accuracy and battery life.
</context>

<task>
Write a compelling 200-word product description for the Apex-1 smartwatch.
</task>

<requirements>
1. Highlight the 14-day battery life and dual-band GPS.
2. Use an energetic and professional tone.
3. Include a clear Call to Action (CTA) at the end.
</requirements>

<output_format>
Markdown with headers for 'Features', 'Benefits', and 'Specifications'.
</output_format>
```

## Reference

For deep dives into the underlying methodology, see [the systematic guide](references/GUIDE.md).
