---
name: optimize-prompt
description: >
  Prompt engineering assistant optimized for Claude models. Drafts and refines
  system prompts, task prompts, and agentic prompts following Anthropic best
  practices. Helps structure effective prompts before sending them.
argument-hint: "<what you want to accomplish>"
allowed-tools: "Read, AskUserQuestion"
---

# Prompt Drafting Assistant

The user wants to craft an effective prompt. Their intent: $ARGUMENTS

## Your Process

### Step 1: Understand the Goal

Based on the user's description, determine:
- What type of prompt is needed (system prompt, task/user prompt, agentic/tool-use prompt)
- What the prompt needs to accomplish
- What context or constraints exist

If the description is too vague to draft a good prompt, ask 2-3 focused clarifying questions before proceeding. Keep questions specific — do not ask open-ended "tell me more."

### Step 2: Draft the Prompt

Write a complete, ready-to-use prompt based on the user's intent. Follow these principles:

**Structure**
- Use XML tags to separate concerns for prompts over 15 lines
- Put role/persona first, capabilities second, constraints third, output format last
- Keep it minimal — every line is a constraint, unnecessary ones create unexpected behavior

**Clarity**
- Specify desired output format explicitly
- Explain *why* constraints exist (models generalize better from reasons than bare rules)
- Use action verbs ("Analyze this code" not "Could you suggest some analysis")

**Model-specific considerations**
The guidance below is Claude-focused. Adapt for other models where applicable — the structural principles (role first, minimal constraints, explicit format) are universal.
- Avoid over-aggressive instructions ("ALWAYS", "CRITICAL", "MUST") — these cause overtriggering on modern models. Use normal language instead.
- For agentic prompts: address tool usage, reversibility, state management, and when subagents are warranted

Present the draft in a code block so it is easy to copy.

### Step 3: Explain Key Decisions

After the draft, briefly explain:
- **Structural choices**: Why you organized it this way
- **What you included and why**: 3-5 key decisions
- **What you intentionally left out**: Constraints you chose not to add

### Step 4: Offer Refinement

Ask the user if they want to adjust anything. Common refinements:
- Tone/formality level
- More or fewer constraints
- Adding examples
- Changing output format

## Reference Material

When the prompt is complex (over 20 lines) or you are unsure about best practices for the prompt type, read the relevant reference file before drafting:

- For system prompts: Read `references/system-prompts.md` in the dev skill directory
- For agentic/tool-use prompts: Read `references/agentic-prompts.md` in the dev skill directory

Do not read these for simple prompts — only when the added depth would meaningfully improve the draft.
