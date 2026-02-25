---
name: improving-prompts
description: Use when optimizing CLAUDE.md, AGENTS.md, custom commands, or skill files for Claude 4.5 models - applies documented Anthropic best practices systematically instead of inventing improvements
---

# Improving Prompts

## Overview

Apply documented Claude 4.5 best practices to existing prompts. Do not invent "improvements" - use the actual guidance from Anthropic.

## When to Use

- Optimizing CLAUDE.md or AGENTS.md files
- Improving custom command prompts
- Refining skill instructions
- Migrating prompts from older Claude models to 4.5

## When NOT to Use

- Writing new prompts from scratch (just follow best practices directly)
- The prompt is working well and user hasn't identified issues

## The Core Problem

Without this skill, agents:
- Invent "best practices" from general knowledge
- Make structural changes without asking what's broken
- Add complexity assuming more structure = better
- Change things to demonstrate value rather than solve problems

## Common Rationalizations (Do Not Fall For These)

| Rationalization | Reality |
|-----------------|---------|
| "The user said it's too vague" | "Too vague" isn't actionable. What specific behavior fails? |
| "I'm the expert, trust me" | Authority doesn't bypass the need for concrete issues |
| "Time pressure - demo tomorrow" | Pressure is when agents make the worst decisions |
| "The spirit of the skill is to help" | Violating the letter IS violating the spirit |
| "I have enough context" | If you can't name the specific failure, you don't |
| "Structure is always better" | Structure solves structure problems, not all problems |
| "This is obviously an improvement" | Obvious to you ≠ solving the user's actual problem |

## Required Process

### Step 1: Understand Before Changing

Before ANY modifications:
1. Ask what specific behaviors are underperforming
2. Ask what the prompt should achieve that it currently doesn't
3. If user says "just improve it generally" - ask for at least one concrete issue

**What counts as a "concrete issue":**
- "Claude ignores my instruction to be concise" ✓
- "The examples I provide don't match the output format" ✓
- "Claude suggests changes but doesn't implement them" ✓

**What does NOT count:**
- "It's too vague" ✗ (vague about what?)
- "It doesn't follow best practices" ✗ (which practice? what fails?)
- "It's inconsistent" ✗ (inconsistent how? show examples)

Do NOT proceed with generic "improvements" based on assumptions.

### Step 2: Reference Actual Best Practices

See `references/claude-4.5-best-practices.md` for the complete reference. Key principles:

**Be explicit with instructions:**
- Claude 4.5 follows instructions precisely - vague requests get literal interpretations
- If you want "above and beyond" behavior, explicitly request it
- Example: "Create a dashboard" → "Create a dashboard. Include relevant features and interactions. Go beyond basics."

**Add context/motivation:**
- Explain WHY a rule exists, not just WHAT the rule is
- Claude generalizes from explanations
- Example: "NEVER use ellipses" → "Never use ellipses because the text-to-speech engine cannot pronounce them"

**Be vigilant with examples:**
- Examples are followed precisely - ensure they demonstrate desired behavior
- One excellent example beats many mediocre ones

**Avoid "think" without extended thinking:**
- When extended thinking is disabled, "think" triggers unwanted behavior
- Use alternatives: "consider," "evaluate," "assess," "determine"

**Control verbosity explicitly:**
- Claude 4.5 defaults to efficiency/conciseness
- If you want summaries or explanations, request them explicitly

**Tool usage patterns:**
- "Can you suggest changes" → Claude suggests but doesn't implement
- "Make these changes" → Claude implements
- Be explicit about whether to act or advise

### Step 3: Preserve What Works

- Do NOT restructure sections that aren't problematic
- Do NOT add complexity unless solving a stated problem
- Do NOT change tone/voice unless specifically requested
- Keep the user's examples if they demonstrate the right behavior

### Step 4: Propose Changes with Rationale

For each change, state:
1. What specific best practice it applies
2. What problem it solves
3. Show before/after

Do NOT make changes without connecting them to documented guidance.

## Red Flags - You're About to Fail

- "Based on general best practices..." → STOP. Use documented practices.
- "Structure is always better..." → STOP. Ask if structure is the problem.
- "I'll assume the user wants..." → STOP. Ask.
- Making 10+ changes to a short prompt → STOP. What specific problem are you solving?
- "This is how I would write it..." → STOP. You're not the user.

## Quick Reference: Claude 4.5 Improvements

| Issue | Fix |
|-------|-----|
| Claude takes things too literally | Add "Go beyond basics" or explicit scope |
| Claude doesn't explain reasoning | Add "Explain your reasoning" or "Think through this step by step" |
| Claude is too verbose | Add "Be concise" or "Respond in X sentences" |
| Claude is too terse | Add "Provide detailed explanations" |
| Claude suggests but doesn't act | Change "Can you..." to imperative "Do X" |
| Instruction isn't followed | Add context for WHY the instruction matters |
| Examples not matching output | Ensure examples show exact desired format |

## Common Mistakes

**Overengineering:** Adding categories, numbered lists, XML structure to simple prompts that were working fine.

**Changing voice:** The user's CLAUDE.md reflects their personality. Don't make it sound like documentation.

**Assuming problems:** Making changes without knowing what's actually broken.

**Inventing practices:** Claiming something is a "best practice" without reference to actual guidance.
