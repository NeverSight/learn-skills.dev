---
name: prompt-master
description: WHEN refining or structuring prompts; NOT executing tasks; outputs XML-tagged instructions with roles, tasks, constraints, and examples.
---

# Prompt Master

Transform simple prompts into comprehensive, context-rich instruction sets following Claude's XML tagging best practices.

## Workflow

### 1. Intake & Clarification

Understand the objective, desired outcome, and success criteria.

Ask for missing inputs when unclear:

- Audience (who will use the output)
- Format (structure, length, style)
- Constraints (boundaries, requirements)
- Tools/integrations (APIs, schemas, functions)
- Tone/style (professional, casual, technical)

Wrap user-provided details in descriptive XML tags (e.g., `<user_prompt>`, `<context>`, `<audience>`, `<tone>`, `<constraints>`). Keep directives outside user-data tags.

### 2. Refinement

Expand the prompt into detailed, ordered instructions with explicit actions:

1. Add edge cases, success criteria, data sources, goals, and constraints
2. Include examples inside `<example>` tags (mark as illustrative)
3. Add domain-specific guidance and pitfalls where applicable
4. If tools/schemas are relevant, scope them via `<tools>`, `<function_call>`, `<api_schema>`

### 3. XML Structuring

Use descriptive, properly nested tags; close all tags.

**Helpful tags:**

- `<role>` - Define the AI's persona and objective
- `<key_responsibilities>` - List core duties
- `<approach>` - Break down the workflow
- `<step number="">` - Sequential actions
- `<tasks>` - Specific actionable items
- `<additional_considerations>` - Edge cases, safety, compliance
- `<reasoning visibility="hidden">` - Internal thought process guidance

### 4. Output Format

Structure the response as:

````
[One-line introduction]

​```markdown
[Enhanced prompt with XML tags]
​```

**Key Improvements Made:**
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]
````

**Wrap the enhanced prompt in a markdown code fence** (`markdown ... `) for clear presentation.

## Template Structure

```markdown
<role>You are an AI-powered [role description]. [Concise persona and objective]</role>

<user_input>
<user_prompt>[Original prompt]</user_prompt>
<context>[Background or constraints]</context>
<audience>[Intended audience]</audience>
<tone>[Desired tone]</tone>
</user_input>

<key_responsibilities>

- [Responsibility 1]
- [Responsibility 2]
  </key_responsibilities>

<approach>
  <step number="1" title="[Step title]">
    - [Actions or questions]
  </step>
  <step number="2" title="[Step title]">
    - [How to add detail and structure]
  </step>
  <step number="3" title="[Step title]">
    - [Formatting, checks, validation]
  </step>
</approach>

<tasks>
  - [Specific actionable tasks]
  - [Edge cases or validations]
</tasks>

<additional_considerations>

- [Safety, compliance, or scope boundaries]
- [Note assumptions; invite clarifications]
  </additional_considerations>

<example>
  [Optional illustrative refined prompt]
</example>
```

## Guidelines

- Keep tone professional and authoritative
- Note assumptions and request missing inputs when needed
- Ensure directives are actionable, testable, and unambiguous
- Use nested tags appropriately for complex structures
- Always close all XML tags properly
