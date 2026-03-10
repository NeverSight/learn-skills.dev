---
name: agent-model-selection
description: Guidelines for selecting appropriate language models for agents based on task-specific benchmarks, availability, and cost efficiency.
---

# Agent Model Selection Skill

## Purpose
Provides data-driven guidance for selecting the most appropriate language model when creating or modifying agent definitions.

## When to Use
- When creating a new agent and need to assign a model
- When modifying an existing agent's model assignment
- When troubleshooting agent performance issues related to model capabilities
- When optimizing costs across the agent ecosystem

## Reference Data

**Always consult [docs/ai-model-reference.md](../../docs/ai-model-reference.md)** for:
- Current performance benchmarks by category (Coding, Reasoning, Language, Instruction Following, etc.)
- Model availability in GitHub Copilot Pro
- Premium request multipliers (cost)
- Recommended model assignments by agent type
- **Task-based guidance and tutorials** (via external links with descriptions)

This reference is updated periodically with latest benchmark data.

## Critical Learnings

1. **Use task-specific benchmarks, not overall scores**
   - Different models excel at different tasks
   - Example: GPT-5.2-Codex excels in Coding while Claude Sonnet 4.5 is better for Language (76.00)

2. **Claude Sonnet 4.5 has poor Instruction Following** (score: 23.52)
   - Unsuitable for agents that follow templates (Task Planner, Quality Engineer)
   - Use Gemini models instead for structured output (scores: 65-75)

3. **Gemini 3 Flash offers best value for many tasks**
   - 0.33x premium multiplier (cost-effective)
   - Strong Instruction Following (74.86)
   - Good Language performance (84.56)
   - Ideal for: Task Planner, Release Manager, high-frequency agents

4. **GPT-5.2-Codex is the latest coding model**
   - Latest generation Codex model (improved over 5.1 Codex Max)
   - Specialized for agentic coding tasks
   - Primary choice for Developer agent
   - Also solid for Code Reviewer

5. **Always verify model availability**
   - Check against official GitHub Copilot documentation
   - Model names must match exactly (case-sensitive)
   - Include "(Preview)" suffix for preview models (e.g., "Gemini 3 Pro (Preview)")

6. **⚠️ Coding agents must NOT have `model:` in frontmatter**
   - The `model:` property is only valid for VS Code agents (files without `-coding-agent` suffix)
   - On GitHub.com, the `model:` property in `*-coding-agent.agent.md` files causes a hard
     `CAPIError: 400 The requested model is not supported` error (confirmed by experiment)
   - The GitHub docs say this property is "ignored" but in practice it prevents the agent from running
   - Apply model selection only to the corresponding VS Code agent file (e.g., `developer.agent.md`)

## Model Selection Process

When selecting or changing a model:

1. **Identify the agent's primary task categories** (from ai-model-reference.md)
   - Coding, Reasoning, Language, Instruction Following, etc.

2. **Check category-specific performance**
   - Look up relevant benchmarks in ai-model-reference.md
   - Compare top 3-5 performers in that category

3. **Consider cost vs frequency**
   - High-frequency agents → favor lower multipliers (0.33x, 0x)
   - Critical accuracy agents → favor best performer regardless of cost

4. **Verify availability**
   - Confirm model is listed in "Available Models" section
   - Check it's available for VS Code (required)

5. **Document your reasoning**
   - Include benchmark scores in proposal
   - Explain trade-offs made

## Example Model Selection

**Scenario**: Selecting model for Quality Engineer agent

1. **Primary tasks**: Define test plans following specific template format
2. **Key categories**: Instruction Following (critical), Reasoning (important)
3. **Benchmark lookup** (from ai-model-reference.md):
   - Gemini 3 Flash: Instruction Following 74.86, 0.33x cost ✅
   - Gemini 3 Pro: Instruction Following 65.85, 1x cost ✅
   - Claude Sonnet 4.5: Instruction Following 23.52 ❌ (disqualified)
4. **Decision**: Gemini 3 Pro (balance of performance and cost)
5. **Rationale**: Strong instruction following (65.85), reasonable cost (1x), good for template-based work

## When to Update Model Assignments

Reassess models when:
- New benchmark data shows significant performance changes
- Agent is underperforming its tasks consistently
- New models are released with better performance
- Cost optimization is needed
- ai-model-reference.md is updated with new data

## Key Principles

- **Task-specific benchmarks matter more than overall scores**
- **Balance cost with performance** based on agent frequency and criticality
- **Always verify availability** against official documentation
- **Document your rationale** for model selection decisions
