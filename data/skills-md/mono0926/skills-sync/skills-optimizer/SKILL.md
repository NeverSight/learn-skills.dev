---
name: skills-optimizer
description: Optimizes the user's skills.yaml configuration, offering tailored skill suggestions and organizing redundant or out-of-stack skills.
---

# Skills Optimizer

A dedicated skill for optimizing the `skills.yaml` file (global: `~/.config/skills_sync/skills.yaml` or project-local: `./skills.yaml`). It aims to streamline existing skills, suggest high-quality additions customized for the user's profile, and maintain a clean, secure environment.

## Context: Understanding User Setup

Prior to proposing any optimizations, you must understand the user's **primary technical stack, preferred architectures (libraries, etc.), and overall development style**.
Extract this context from provided profile information or conversation history.
**[IMPORTANT]** If your understanding of the user's setup is insufficient (e.g., core technologies are unclear), you MUST ask the user for clarification before drafting optimization suggestions.

- **Objective**: Balance beneficial skill additions with context window efficiency. While the impact of installed skills on the initial context is minimal (mostly names and descriptions), respect the user's preference for either maximum utility or minimal noise.

## Workflow

Strictly follow these steps when this skill is invoked:

### 1. Current State Analysis

Read the current `skills.yaml`. Note that project-local `./skills.yaml` takes precedence over global `~/.config/skills_sync/skills.yaml`. Analyze the installed repositories, wildcard installations (`*`), and excluded skills (`!`).

### 2. Identifying High-Quality Skills & Security Audit

Recommend top-tier skills related to the user's tech stack (e.g., official repositories for Frameworks, Cloud providers, and tools the user prefers). Focus on skills that significantly enhance code quality and architectural alignment.

**[TIP: Using find-skills]**
To discover high-quality skills across the ecosystem, you are encouraged to use the **[find-skills](https://skills.sh/vercel-labs/skills/find-skills)** skill. It can help you search for and identify well-maintained skills that match the user's requirements.

**[CRITICAL: Security and Quality Pre-Audit]**

The `skills_sync` tool downloads configuration files from target repositories and lacks an inherent mechanism for deep security verification of the skill's logic itself. Therefore, **before proposing new skills, you MUST research the target repository (reading SKILL.md and auditing files in scripts/, etc.) and verify the following:**

- **Security Check**: Ensure there are no unauthorized network communications (data leakage), destructive commands (excessive deletion permissions like `rm -rf`), or suspicious obfuscated scripts.
- **Quality Check**: Verify that the prompt instructions align with the user's high-quality, modern development standards. Assess risks of poor instructions or prompt injection flaws.
  _Do not propose new skills to the user without completing this audit._

### 3. Screening & User Verification

Identify skills that no longer fit the user's core tech stack.

- **NEVER delete skills automatically.**
- List skills as candidates for removal only if they are clearly redundant, completely irrelevant, or potentially harmful. Items kept "just in case" are generally fine to remain.

### 4. Proposing the Optimization Plan

Present your analysis and audit results to the user:

- **Proposed Additions**: List recommended new skills and explain why they suit the user's stack. **Explicitly state that you have audited the sources and found no security risks.**
- **Removal/Retention Confirmation**: List skills considered "out-of-stack" and ask the user: "Would you like to keep these for occasional use, or remove them to save context? (If removed, they can always be re-added when needed.)"
- **Improvements**: Suggest refinements for redundant skill entries or overly broad wildcard imports.

### 5. Applying Changes

Once the user provides their preference:

1. Update `skills.yaml` based on the user's choices.
2. Maintain the original structure of YAML comments and formatting.
3. **Ask for permission to apply changes**: DO NOT run `skills_sync sync` automatically. Instead, ask the user if they would like to apply the configuration changes now.
4. Execute `skills_sync sync` only after receiving explicit confirmation.

- **[TIP]** Use `skills_sync sync --no-clean` for a faster synchronization when only adding new skills or updating existing ones.

5. Confirm successful synchronization with the user.

## Best Practices

- **NEVER modify `skills.yaml` without explicit consent from the user.**
- **Prefer Project-Local Config**: If the user is working on a specific project, check if a project-local `skills.yaml` exists or should be created instead of modifying the global one.
- Keep communication helpful, concise, and professional, adhering to any user-specific language or behavioral rules.
