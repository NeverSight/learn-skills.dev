---
name: agent-task-mapping
version: "2.0"
last_updated: 2026-09-08
tags: [task, mapping, agents, delegation, workflow]
description: "Map tasks to specialist agents. Use when choosing which agent for a job, comparing agent capabilities, or routing to React/Next.js/Playwright/docs/code-quality experts. Keywords: which agent, best agent for this, delegate to expert, agent capability mapping."
---
# Agent Task Mapping

- Leverage native parallel subagent dispatch and 200k+ context windows where available.


## Activation Conditions

Use symptom -> action triggers: when one matches, apply this skill and verify with the protocol below.

Use this skill when:
- Determining which specialized agent to delegate a task to
- Reviewing agent capabilities and expertise areas
- Trying to match a specific task to an appropriate specialist
- Needing quick reference for available agents and their purposes

## Available Agents

See [Agent Details](./references/agent-details.md) for comprehensive information about each agent:
- Description and specialization areas
- When to use each agent
- Typical tasks handled by each

<!-- MCP:START -->

<!-- PORTABILITY:START -->
## Cross-Client Portability

This skill is written to stay usable across GitHub Copilot, Claude Code, and Codex.

- GitHub Copilot: keep the folder in a Copilot-visible skill path or wrap the
  workflow in project instructions when folder discovery is unavailable.
- Claude Code: keep the folder in a local skills directory or a compatible plugin source.
- Codex: install or sync the folder into
  `$CODEX_HOME/skills/agent-task-mapping` and restart Codex after major changes.

<!-- PORTABILITY:END -->

## MCP Availability And Fallback

Preferred MCP Server: None required

- Fallback prompt: "Use the Agent Task Mapping skill without MCP. Rely on its local instructions, bundled resources, standard shell or editor tools, and direct verification. Show the evidence used before concluding."
- Do not claim an MCP operation was used when the active host does not expose it.
- Treat local files, tests, rendered outputs, logs, or screenshots as the fallback evidence path.

<!-- MCP:END -->

## Anti-Patterns

- Delegating or evaluating without a scoped success condition: The output becomes hard to review and easy to overbuild.
- Skipping the evidence step: A workflow that cannot be re-checked quickly is not ready for handoff.
- Bundling unrelated subtasks together: It creates noisy prompts, weaker ownership, and avoidable integration risk.

## Verification Protocol

Before claiming "skill applied successfully":

1. Pass/fail: The Agent Task Mapping workflow names the agent boundary, delegated scope, and expected return artifact.
2. Pass/fail: Context passed to helpers is minimal, task-local, and free of hidden expected answers.
3. Pass/fail: Results are integrated only after evidence, diffs, or citations are checked by the controller.
4. Pressure-test scenario: Run the workflow on two similar tasks that must not share assumptions or leaked context.
5. Success metric: Zero context leakage; every delegated output is independently reviewable.

## Examples & Scripts

- [Delegation Examples](./examples/delegation-example.md) — Code examples for delegating to different agents
- [Agent Discovery Script](./scripts/agent-discovery.js) — Node.js script to discover available agents

## Quick Reference

| Agent Name | Best For |
|------------|-----------|
| Code Explainer | Analyzing and documenting existing code |
| UI Designer | UI/UX improvements and design implementations |
| Universal Janitor | Code cleanup, simplification, and tech debt removal |
| Critical Thinking | Challenging assumptions and exploring alternatives |
| Next.js Expert | Next.js 15/16+ architecture and optimizations |
| Expert React Frontend Engineer | React 19+ patterns and best practices |
| Playwright Tester Mode | Comprehensive testing with exploratory testing |
| Tech Writer | Creating formal developer documentation |
| Create PRD Chat Mode | Generating Product Requirements Documents |
| Specification | Generating or updating specification documents |
| Plan | Research and outlining multi-step plans |

## Decision Framework

When choosing an agent for delegation:

1. **Identify task type**: Is it documentation, testing, two-stage review (spec compliance first, then code quality), or development?
2. **Match to specialization**: Find agent whose description aligns with task
3. **Check availability**: Verify agent exists and has proper frontmatter configuration
4. **Use specific agentName**: Delegate using exact name from agent's frontmatter

## Task Categories

### Code Analysis & Documentation
- Use **Code Explainer** for analyzing existing code patterns
- Use **Tech Writer** for formal developer documentation
- Use **Specification** for generating feature specifications

### Code Quality & Maintenance
- Use **Universal Janitor** for cleanup and tech debt remediation
- Use **Critical Thinking** for challenging assumptions

### Development Work
- Use **Next.js Expert** for Next.js 15/16+ architecture and optimizations
- Use **Expert React Frontend Engineer** for React 19+ patterns

### Testing
- Use **Playwright Tester Mode** for comprehensive web application testing

### Planning & Requirements
- Use **Plan** for research and outlining multi-step plans
- Use **Create PRD Chat Mode** for generating Product Requirements Documents

### Design
- Use **UI Designer** for UI/UX improvements and design implementations


---

## Related Skills

- [custom-agent-usage](../custom-agent-usage/SKILL.md): Use it when the workflow also needs loading and invoking custom agent definitions safely.
- [subagent-delegation](../subagent-delegation/SKILL.md): Use it when the workflow also needs safe, scoped delegation to helper agents.
- [subagent-driven-development](../subagent-driven-development/SKILL.md): Use it when the workflow also needs plan-driven implementation with reviewer loops.
- [agentic-eval](../agentic-eval/SKILL.md): Use it when the workflow also needs rubric-driven evaluation loops.
