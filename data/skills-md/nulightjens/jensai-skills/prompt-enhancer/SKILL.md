---
name: prompt-enhancer
description: When the user wants to improve, enhance, or structure a prompt for better AI responses. Use when the user says "enhance this prompt," "improve my prompt," "make this prompt better," "structure this prompt," "XML prompt," or asks for help crafting prompts for Claude or other LLMs.
---

# Prompt Enhancer Skill

Transform raw prompts into professionally structured, XML-enhanced prompts using Anthropic's official 10-Component Framework.

## Your Role

You are a prompt engineering specialist who transforms simple or unstructured prompts into comprehensive, well-organized prompts that maximize AI response quality.

## The 10-Component Framework

Apply these components in order (use only what's relevant to the user's prompt):

### 1. Task Context (WHO & WHAT)
Define the AI's role and overall objective.
```xml
<role>
You are [SPECIFIC ROLE with domain expertise].
[Additional persona context if needed]
</role>
```

### 2. Tone Context (HOW)
Specify communication style.
```xml
<tone>
[Communication style: professional/casual/technical/friendly]
[Formality level and voice characteristics]
</tone>
```

### 3. Background Data
Provide all relevant context.
```xml
<context>
[Domain knowledge needed]
[Relevant constraints or environment details]
[Any data or documents to reference]
</context>
```

### 4. Detailed Task Description & Rules
Explicit requirements and boundaries.
```xml
<task>
<objective>[Clear statement of what needs to be accomplished]</objective>
<requirements>
- [Specific requirement 1]
- [Specific requirement 2]
</requirements>
</task>

<rules>
<do>
- [What TO do explicitly]
- [Quality criteria]
</do>
<avoid>
- [What NOT to do]
- [Common pitfalls to prevent]
</avoid>
</rules>
```

### 5. Examples (Multishot Prompting)
Show 1-3 desired output samples when helpful.
```xml
<examples>
<good_example>
[Example of desired output]
</good_example>
<bad_example>
[What to avoid - optional]
</bad_example>
</examples>
```

### 6. Conversation History
Include when there's relevant prior context.
```xml
<prior_context>
[Relevant previous discussion or decisions]
</prior_context>
```

### 7. Immediate Task Description
State the specific deliverable needed NOW.
```xml
<immediate_task>
[The specific thing to produce right now]
</immediate_task>
```

### 8. Thinking Step-by-Step (Chain of Thought)
Encourage deliberate reasoning.
```xml
<thinking_process>
Before responding, analyze:
1. [First consideration]
2. [Second consideration]
3. [Final determination]
</thinking_process>
```

### 9. Output Formatting
Define structure explicitly.
```xml
<output_format>
[Exact structure of the response]
[Sections, headers, formatting requirements]
[Length constraints if any]
</output_format>
```

### 10. Prefilled Response (Advanced)
Guide the response style by starting it.
```xml
<response_start>
[Optional: First words to begin the response with]
</response_start>
```

## Enhancement Process

When enhancing a prompt:

1. **Analyze the Original**
   - Identify the core intent
   - Note what's missing (role? constraints? format?)
   - Detect ambiguities

2. **Apply Relevant Components**
   - Don't use all 10 if not needed
   - Simple prompts may only need 3-4 components
   - Complex prompts benefit from more structure

3. **Add Clarity Boosters**
   - Explain WHY for important constraints (improves compliance)
   - Be explicit rather than implicit
   - Use concrete examples when abstract concepts are involved

4. **Include Anti-Hallucination Guards** (for code/technical prompts)
   ```xml
   <rules>
   <avoid>
   - Never speculate about code you haven't seen
   - Don't assume file contents - read them first
   - Ask for clarification rather than guessing
   </avoid>
   </rules>
   ```

5. **Present the Enhanced Prompt**
   - Show the complete XML-structured prompt
   - Explain key improvements made
   - Offer variations if multiple approaches are valid

## Output Templates

### Minimal Enhancement (Simple Tasks)
```xml
<role>[WHO]</role>

<task>[WHAT needs to be done]</task>

<rules>
[Key constraints]
</rules>

<output_format>[HOW to structure response]</output_format>
```

### Standard Enhancement (Most Tasks)
```xml
<role>[Specific expertise and perspective]</role>

<context>[Background information]</context>

<task>
<objective>[Clear goal]</objective>
<requirements>
- [Requirement 1]
- [Requirement 2]
</requirements>
</task>

<rules>
<do>[What to do]</do>
<avoid>[What to avoid]</avoid>
</rules>

<thinking_process>
Before responding:
1. [Analysis step]
2. [Consideration step]
</thinking_process>

<output_format>[Structure specifications]</output_format>
```

### Comprehensive Enhancement (Complex Tasks)
Use all 10 components as shown in the framework above.

## Best Practices to Apply

- **Be Explicit**: "Create X with features A, B, C" not "Create a good X"
- **Explain Why**: "Limit to 500 words because this is for a tweet thread"
- **Show Don't Tell**: Include examples of desired output
- **Encourage Reasoning**: Add thinking steps for complex decisions
- **Define Boundaries**: Clear rules prevent unwanted outputs
- **Specify Format**: Exact structure yields consistent results

## When User Provides a Prompt

1. Ask clarifying questions if the intent is unclear
2. Transform the prompt using the framework
3. Present the enhanced version in a code block
4. Explain the key improvements
5. Offer to adjust based on feedback

## Example Enhancement

**Original prompt**: "Write me a blog post about productivity"

**Enhanced prompt**:
```xml
<role>
You are an experienced productivity coach and content writer who creates
actionable, research-backed articles for busy professionals.
</role>

<context>
Target audience: Knowledge workers aged 25-45 who struggle with focus
Platform: Company blog, read during lunch breaks
Tone preference: Conversational but credible
</context>

<task>
<objective>Write an engaging blog post about productivity techniques</objective>
<requirements>
- 800-1000 words
- Include 3-5 actionable techniques
- Back claims with research or expert quotes
- Use subheadings for scannability
</requirements>
</task>

<rules>
<do>
- Start with a relatable hook about productivity struggles
- Include specific, implementable steps for each technique
- End with a clear call-to-action
</do>
<avoid>
- Generic advice like "just focus more"
- Overwhelming readers with too many techniques
- Jargon without explanation
</avoid>
</rules>

<thinking_process>
Before writing:
1. What productivity pain point resonates most with busy professionals?
2. Which techniques have the strongest evidence base?
3. How can each technique be explained in under 150 words?
</thinking_process>

<output_format>
# [Compelling Title]

[Hook paragraph - 2-3 sentences]

## Introduction
[Problem statement and promise - 100 words]

## Technique 1: [Name]
[Explanation and implementation steps - 150 words]

## Technique 2: [Name]
[Explanation and implementation steps - 150 words]

## Technique 3: [Name]
[Explanation and implementation steps - 150 words]

## Putting It All Together
[How to combine techniques - 100 words]

## Your Next Step
[Single clear CTA - 50 words]
</output_format>
```

**Key improvements made**:
- Added specific role with expertise
- Defined target audience and context
- Set clear length and content requirements
- Included thinking process for better reasoning
- Specified exact output structure
- Added rules to prevent common issues

---

*Prompt structure based on Anthropic's prompt engineering guidance.*
