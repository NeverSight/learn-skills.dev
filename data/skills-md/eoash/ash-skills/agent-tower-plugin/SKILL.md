---
name: agent-tower-plugin
description: Multi-agent deliberation for Claude Code - orchestrate AI coding assistants (Claude, Codex, Gemini) for council, debate, and consensus workflows
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
---

# Agent Tower Plugin

Multi-agent deliberation for Claude Code. Orchestrate multiple AI coding assistants (Claude, Codex, Gemini) to get diverse perspectives on tasks.

## Interactive Configuration

Before running any multi-agent workflow, use **AskUserQuestion** to gather configuration preferences from the user. This ensures the user has control over:
- Number of agents/rounds
- Consensus thresholds
- Agent role assignments
- Other mode-specific options

Skip questions for any options the user explicitly provided in their command.

## Available Skills

### `/tower:council`
**Multi-agent council with parallel opinions and synthesis**

First, analyze the user's question and suggest relevant perspectives via AskUserQuestion. Then run multiple agents in parallel with the selected personas. Agents anonymously rank each other's responses, and a chairman synthesizes the final answer.

Best for: Evaluations, strategy decisions, comprehensive analysis, general knowledge questions

### `/tower:debate`
**Adversarial debate with pro/con agents**

Two agents argue opposing positions on a binary decision. A judge evaluates the arguments and declares a winner with scores.

Best for: Binary decisions, trade-off analysis, technology choices

### `/tower:deliberate`
**Producer/reviewer consensus loop**

A producer generates a response, a reviewer provides structured feedback, and they iterate until reaching consensus or hitting max rounds.

Best for: Code review, document refinement, iterative improvement

### `/tower:agents`
**List available agents**

Shows which agent backends (Claude, Codex, Gemini) are currently available.

## Agent Backends

| Agent | CLI | Default Model |
|-------|-----|---------------|
| claude | `claude -p` | opus |
| codex | `codex exec` | default |
| gemini | `gemini` | gemini-3-pro-preview |

## Dynamic Personas

Analyze the user's question and suggest relevant personas. Use technical personas for code/architecture questions, generalist personas for general knowledge questions.

**Technical:** Security Analyst, Systems Architect, Code Quality Reviewer, DevOps Engineer, Data Engineer, Devil's Advocate

**Generalist:** Research Analyst, Local Expert, Critical Thinker, Practical Advisor

**Business:** Business Strategist, Product Manager, Financial Analyst, UX Designer

Custom personas can be passed via `--personas '[{"name":"Expert Name","focus":"focus area"}]'`

## Examples

```
/tower:council "Evaluate this startup idea: AI-powered meal planning"
/tower:debate "Should we use microservices or a monolith?"
/tower:deliberate "Review the security of ~/GH/myproject"
/tower:agents
```
