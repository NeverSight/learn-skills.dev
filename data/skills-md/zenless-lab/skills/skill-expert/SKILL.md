---
name: skill-expert
description: Comprehensive master guide for designing, creating, editing, updating, and refactoring Agent Skills according to the official agentskills.io specification. Use this when you need to build or modify capabilities for an AI agent.
---
# Agent Skill Manager & Creator

Welcome to the Agent Skill Manager. This skill outlines the core philosophy and comprehensive guiding principles for building, editing, and maintaining high-quality, efficient, and modular Agent Skills.

## 🧠 Core Philosophy: Simplicity & Progressive Disclosure

When creating or refactoring a skill, you must first assess its complexity. 
* **For simple skills:** A single `SKILL.md` file is entirely sufficient. Do not create unnecessary folders or files if the core logic and instructions are brief, straightforward, and easily fit within the agent's context window.
* **For complex skills:** Your critical responsibility is designing for **Progressive Disclosure**. You must proactively split complex content into multiple files to manage the target agent's context window efficiently. Do not overload the main skill file.

### Progressive Disclosure Workflow (For Complex Skills)
1. **Discovery**: Only the `name` and `description` (YAML frontmatter) are loaded at the target agent's startup. Keep them keyword-rich and highly descriptive so the agent knows exactly when to use the skill.
2. **Activation**: The newly created `SKILL.md` file is read in its entirety upon task activation. It must remain strictly under 500 lines. Focus this file only on *what* the skill does, high-level rules, and providing a map to auxiliary files.
3. **Execution (Optional File Splitting)**: When a skill requires complex logic, long text, or templates, structurally split them into optional subdirectories so the target agent loads them *only on demand*:
   * **`references/`**: Extract detailed technical docs, step-by-step workflows, API references, or long-form domain instructions into highly focused, small markdown files here.
   * **`assets/`**: Isolate static resources like document templates, config templates, or data schemas here.
   * **`scripts/`**: Move executable code (e.g., Python or Bash) here. Scripts must be self-contained, provide clear error messages, and handle edge cases gracefully.

## 🏗️ Structural Principles

Every Agent Skill you create or refactor must adhere to these architectural standards:

* **Self-Contained Folder**: The skill lives in a directory matching the `name` in the frontmatter.
* **Mandatory SKILL.md**: This is the heart of the skill. It MUST contain compliant YAML frontmatter (`name`, `description`), followed by Markdown instructions.
* **Optional Auxiliary Folders**: `references/`, `assets/`, and `scripts/` are completely situational and should only be created when the skill's complexity necessitates them.
* **Relative Referencing**: All internal links to auxiliary files MUST use relative paths from the skill root (e.g., `[Format Guide](references/format-guide.md)`).

## 📜 Formatting and Syntax Rules

* **Naming Constraints**: `name` must be 1-64 characters, restricted to lowercase alphanumeric and hyphens (`a-z`, `0-9`, `-`). Cannot start/end with a hyphen, nor contain consecutive hyphens.
* **Description Constraints**: `description` (1-1024 characters) must explicitly state what the skill does and *when* the agent should trigger it.
* **Script Standards & Execution Preference** (If scripts are used):
  * Any Python scripts placed in the `scripts/` directory MUST follow the PEP 723 inline script metadata standard.
  * **CRITICAL**: If you generate a new skill that contains executable scripts, you MUST explicitly state in the generated `SKILL.md` that the agent should prefer using `uv run scripts/your_script.py` (or `uvx`) to ensure dependencies are automatically handled.

## 🌐 Official Specifications

If you need to consult the raw official definitions and specs during creation or validation, access the following links:
* [Home](https://agentskills.io/home.md)
* [What are skills?](https://agentskills.io/what-are-skills.md)
* [Specification](https://agentskills.io/specification.md)
* [Integrate skills](https://agentskills.io/integrate-skills.md)

## 📚 Detailed Workflows & Guidelines

*(Note: The following references are examples of progressive disclosure for complex tasks. Read them only when performing a specific task that requires deep context.)*

* [For the Standard Operating Procedure on creating/editing skills](references/step-by-step-workflow.md)
* [For YAML specifications](references/frontmatter-spec.md)
* For coding and documentation rules: 
  * [Script best practices](references/script-best-practices.md)
  * [Reference file best practices](references/reference-best-practices.md)
