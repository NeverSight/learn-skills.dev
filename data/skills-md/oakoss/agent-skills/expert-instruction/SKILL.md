---
name: expert-instruction
description: |
  System prompt design and instruction crafting for AI agents. Covers persona definition, constraint specification, output formatting, tool use instructions, multi-turn behavior, and guardrail design.

  Use when writing system prompts for AI products, designing agent personas, specifying behavioral constraints, crafting tool-use instructions, or building multi-step agent workflows.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Expert Instruction Design

## Overview

Expert instruction design focuses on crafting system prompts that define how an AI agent behaves, what it can and cannot do, and how it responds across interactions. Unlike general prompt engineering (which optimizes individual queries), this skill covers the **persistent behavioral layer** that shapes an agent's identity, capabilities, and constraints.

**When to use:** Writing system prompts for AI products, defining agent personas for customer-facing tools, specifying behavioral guardrails, crafting tool-use guidance, or designing multi-step agent workflows.

**When NOT to use:** One-off prompt optimization (use the `prompt` skill), fine-tuning or training-time configuration, infrastructure-level safety (use model provider safety features), or tasks that do not involve LLM agent behavior.

## Quick Reference

| Pattern                  | Purpose                                  | Key Points                                       |
| ------------------------ | ---------------------------------------- | ------------------------------------------------ |
| Identity block           | Define who the agent is                  | Role, expertise, communication style             |
| Capability declaration   | State what the agent can do              | Explicit tool list, domain boundaries            |
| Constraint specification | Define behavioral boundaries             | Hard limits, soft preferences, escalation rules  |
| Output format rules      | Ensure consistent response structure     | Templates, progressive disclosure, length limits |
| Tool use instructions    | Guide when and how to use tools          | Selection criteria, error handling, sequencing   |
| Multi-turn behavior      | Handle conversation continuity           | Context tracking, topic switching, memory        |
| Guardrails               | Prevent harmful or out-of-scope behavior | Content boundaries, instruction hierarchy        |
| Escalation triggers      | Define when to hand off to humans        | Confidence thresholds, scope boundaries          |

## Common Mistakes

| Mistake                                  | Correct Pattern                                               |
| ---------------------------------------- | ------------------------------------------------------------- |
| System prompt over 4000 tokens           | Keep under 2000 tokens, move details to reference docs        |
| Contradictory instructions               | Audit for conflicts, establish priority order                 |
| Vague persona ("be helpful")             | Specific: expertise domain, response style, knowledge bounds  |
| No escalation path                       | Define when agent should defer to human or say "I don't know" |
| Listing every edge case                  | State principles, provide examples for ambiguous cases only   |
| Mixing identity and task instructions    | Separate: identity block first, task instructions second      |
| No output format specification           | Define structure: headings, lists, code blocks, length        |
| Tool instructions without error handling | Include fallback behavior when tools fail or return errors    |
| Testing only happy-path inputs           | Test adversarial, off-topic, and edge case inputs             |
| Deploying without versioning             | Track system prompt versions, log changes, enable rollback    |

## Delegation

- **Prompt technique exploration**: Use `Explore` agent to research patterns
- **System prompt testing**: Use `Task` agent to run adversarial test suites
- **Code review**: Delegate to `code-reviewer` agent for integration code

> If the `prompt` skill is available, delegate general prompt engineering techniques (CoT, few-shot, structured output) to it.
> Otherwise, recommend: `pnpm dlx skills add oakoss/agent-skills -s prompt -a claude-code -y`

## References

- [System prompt design: anatomy, personas, tools, and multi-turn behavior](references/system-prompt-design.md)
- [Guardrails and testing: behavioral boundaries, versioning, and production readiness](references/guardrails-and-testing.md)
