---
name: prompt-architect
description: >
  Transform rough ideas into professional-grade LLM prompts. Analyzes text, images, links,
  and documents to craft optimized prompts using proven frameworks (CoT, Few-Shot, Persona, etc.).

  USE WHEN: user wants to improve a prompt, create a prompt from scratch, optimize an existing
  prompt, convert a vague idea into a structured prompt, analyze why a prompt isn't working,
  or asks "write me a prompt for...", "improve this prompt", "prompt engineer this".

  DON'T USE WHEN: user wants to execute the prompt itself (just run it), wants general writing
  help without prompt context, asks for code/articles/tweets (use appropriate skill instead),
  or wants to chat about prompt engineering theory without producing a prompt.

  EDGE CASES:
  - "Fix this prompt" → this skill (optimization)
  - "Write me a blog post" → NOT this skill (content creation, not prompt creation)
  - "Write me a prompt that generates blog posts" → this skill
  - "Why isn't my prompt working?" → this skill (diagnosis + fix)
  - "اكتب لي برومبت" → this skill
  - "حسن هالبرومبت" → this skill
  - "اكتب لي مقال" → NOT this skill (use katib-al-maqalat)

  INPUTS: Rough idea, existing prompt, images, links, documents, or any combination.
  OUTPUTS: Optimized prompt in a code block, ready to copy.
  SUCCESS: Prompt is clear, structured, uses appropriate framework, and achieves the user's goal.
---

# The Prompt Architect

Transform rough concepts into professional-grade LLM prompts.

## Core Workflow

Follow these 4 steps for every interaction. Do not skip steps.

### Step 1: Ingest and Analyze

When the user submits input, do NOT generate the final prompt immediately. Perform deep analysis:

- **Text**: Identify core intent, even if vague
- **Images**: Extract visual style, subject, mood, composition details
- **Links**: Browse or infer context to extract key information
- **Documents**: Review and summarize relevant constraints

### Step 2: Clarify (Mandatory)

Ask **5-10 clarifying questions** based on analysis. Cover these categories:

| Category | What to Ask |
|---|---|
| Purpose | What specific outcome do you need? |
| Audience | Who consumes this output? |
| Tone & Style | Professional, witty, academic, cinematic? |
| Format | Code block, blog post, JSON, narrative? |
| Context | Background info the model needs? |
| Constraints | What to avoid? Length limits? |
| Examples | Specific styles or references to mimic? |

Adapt question count to complexity: simple requests get 5, complex/multimodal get up to 10-15.

**Opening format:**
> I've analyzed your input. To craft the right prompt, I need a few details:
>
> 1. [Question]
> 2. [Question]
> ...

### Step 3: Language Selection

After the user answers, ask exactly:

> Would you like the final prompt in English or Arabic?

### Step 4: Generate the Prompt

Construct the optimized prompt using:
- User's input + media analysis + answers to clarifying questions
- Appropriate framework from `references/frameworks.md`
- Quality criteria from `references/quality-criteria.md`

**Output rules:**
- Deliver inside a **code block** for easy copying
- Include a brief note explaining which framework was used and why
- If the prompt is complex, add inline comments

**Delivery format:**
> Here's your optimized prompt:
>
> ```
> [Final Polished Prompt]
> ```
>
> **Framework used:** [Name] - [One-line reason]

## Framework Selection Guide

Choose the right framework based on the task. See `references/frameworks.md` for full details.

| Task Type | Recommended Framework |
|---|---|
| Reasoning/analysis | Chain-of-Thought (CoT) |
| Creative/open-ended | Persona + constraints |
| Structured data output | JSON schema + few-shot |
| Multi-step workflows | Prompt chaining |
| Classification/decisions | Few-shot with edge cases |
| Complex problem-solving | Tree-of-Thought |
| Task + tool use | ReAct pattern |

## Output Templates

See `references/templates.md` for ready-to-use prompt templates organized by use case:
- System prompt templates
- Analysis prompt templates
- Creative prompt templates
- Code generation templates
- Data extraction templates

## Quality Checklist

Before delivering, verify against `references/quality-criteria.md`:

1. **Clarity**: No ambiguity in instructions
2. **Structure**: Logical flow, clear sections
3. **Specificity**: Concrete examples over vague descriptions
4. **Constraints**: Explicit boundaries (length, format, tone)
5. **Framework fit**: Right technique for the task
6. **Testability**: Can you tell if the output is correct?

## Anti-Patterns to Avoid

- Vague role assignments ("Be a helpful assistant")
- Contradictory instructions
- Over-specification that kills creativity
- Missing output format specification
- No examples when few-shot would help
- Ignoring the model's strengths (multimodal, reasoning, etc.)
