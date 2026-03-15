---
name: agent-creator
description: Guide for creating, configuring, and refining AI Agents. Use this skill when users want to define a new agent persona, generate a system prompt, or assemble a specific set of skills/workflows for a specialized agent (e.g., "Create a QA Agent" or "Design a Security Auditor Agent").
---

# Agent Creator

This skill provides a structured process for designing and configuring specialized AI Agents.

## When to Use

Use this skill when you need to:
1.  **Create a New Agent**: Define a purpose-built agent with specific expertise (e.g., "Make a Frontend Specialist Agent").
2.  **Generate System Prompts**: Create robust, effective system instructions for an agent.
3.  **Assemble Capabilities**: Select the right combination of Skills, Workflows, and Rules for a specific domain.
4.  **Refine Agent Behavior**: specialized tuning of an existing agent's operational guidelines.

## Agent Architecture

An Agent in the Antigravity system is defined by a markdown file in `.agent/agents/{name}.md` containing:

### 1. Frontmatter (Metadata)
-   `name`: Kebab-case identifier (e.g., `backend-specialist`).
-   `description`: Short summary and trigger keywords.
-   `tools`: List of tools the agent has access to (e.g., `Read, Write, Bash`).
-   `model`: The model usage strategy (usually `inherit`).
-   `skills`: Comma-separated list of skills from `.agent/skills/` this agent needs.

### 2. Identity & Charter
-   **Role**: Who the agent is.
-   **Philosophy**: Core beliefs driving decisions.
-   **Mindset**: Operational mode and priorities.

### 3. Critical Guidelines (The "Stop & Ask" Protocol)
-   **CRITICAL: CLARIFY BEFORE CODING**: A mandatory section forcing the agent to ask clarifying questions before making assumptions about stack, runtime, or tools.

### 4. Decision Frameworks
-   Tables and logic guides to help the agent make technical decisions (e.g., "Node vs Python", "SQL vs NoSQL").

### 5. Capabilities & specialized Lists
-   **Expertise Areas**: Deep dive into specific techs.
-   **Quality Control Loop**: Mandatory steps to run after every edit.

## Workflow: Creating an Agent

Follow these steps to create a new Agent.

### Step 1: Define the Goal
Ask the user for the Agent's primary purpose.
*   *Prompt*: "What is the primary goal of this agent? What domain does it specialize in?"

### Step 2: Select Capabilities (Skills)
Analyze the available Skills in `.agent/skills/` to recommend the best set to include in the `skills` frontmatter.
-   *Example*: A Backend Agent needs `nodejs-best-practices`, `database-design`.

### Step 3: Draft the Agent Definition
Use the **Agent Template** in `assets/agent_template.md` as the mandatory base.
1.  **Frontmatter**: Fill in name, tools, and required skills.
2.  **Philosophy & Mindset**: Define *how* the agent thinks, not just what it does.
3.  **Critical Clarifications**: Define what the agent MUST ask users before starting (e.g., "Which framework?", "Which DB?").
4.  **Decision Frameworks**: Populate tables with current best practices for the domain.

### Step 4: Save the Artifact
Save the file to `.agent/agents/{name}.md`.
-   Ensure the filename matches the `name` in frontmatter.

## Tools & Resources

### Agent Template
Use `assets/agent_template.md` to structure the agent definition. **Strictly follow this structure.**

### Best Practices for specialized Agents
-   **Opinionated Defaults**: Agents should have strong opinions (Philosophy) but flexible execution (Clarification).
-   **Mandatory Checks**: Include a "Quality Control Loop" that forces the agent to validate its own work (Lint, Test, Security).
-   **Anti-Patterns**: Explicitly list what the agent should AVOID.
