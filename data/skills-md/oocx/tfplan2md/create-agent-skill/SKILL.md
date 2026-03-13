---
name: create-agent-skill
description: Create a new Agent Skill following project standards and templates. Use this when you need to encapsulate a new capability or workflow.
---

# Create Agent Skill

## Purpose
Standardize the creation of new Agent Skills to ensure they are consistent, discoverable, and follow best practices.

## When to Create a Skill
- **Complex Tooling**: When an agent needs to run a sequence of scripts or commands that are too long for the main agent prompt.
- **Shared Capabilities**: When multiple agents need the same capability (e.g., "Run UAT" used by UAT Tester and Quality Engineer).
- **Strict Procedures**: When a process requires exact adherence to a checklist or script (e.g., Release process).

## Hard Rules
### Must
- Create the skill in `.github/skills/<skill-name>/`.
- Use `kebab-case` for the skill name.
- Ensure the skill `name` matches the parent directory name exactly.
- Ensure `name` is 1–64 characters, lowercase letters/numbers/hyphens only.
- Ensure `name` does not start or end with `-` and does not contain consecutive hyphens (`--`).
- Include a `SKILL.md` with valid YAML frontmatter.
- Include a `description` in the frontmatter (max 1024 chars).
- Create `scripts/` and `templates/` subdirectories only if needed.
- Use the provided template for `SKILL.md`.
- Update `docs/agents.md` to register the new skill in the "Available Skills" table.

### Must Not
- Create skills in the root `.github/` directory.
- Use spaces or special characters in the skill name.
- Leave the `description` empty.

## Best Practices
- **Self-Contained**: A skill should include all necessary scripts and templates within its folder.
- **Progressive Disclosure**: Copilot only loads the skill body when the description matches the user's intent. Keep descriptions specific.
- **Verification**: Test skills by asking Copilot "How do I <skill description>?" and verifying it loads the skill.
- **Approval Minimization**: Design skills to reduce the number of Maintainer approval prompts (terminal command approvals) so agents can execute workflows with minimal interruptions.
	- Prefer a small number of **stable wrapper commands** over many one-off commands.
	- Batch related operations into a single command where practical (and safe).
	- Prefer tool-based reads (editor tools) over shell commands for read-only actions when available.
	- Reuse existing repo scripts (e.g., `scripts/uat-*.sh`) instead of duplicating multi-step command sequences.
	- If a workflow is inherently risky (force-push, merge, deleting branches), keep it explicit and gated, but still consolidate the surrounding steps.

## Actions

### 1. Gather Information
Ask the user for:
- **Skill Name**: Short, descriptive, kebab-case (e.g., `run-uat`, `deploy-docs`).
- **Description**: One sentence explaining what the skill does and *when* Copilot should load it.
- **Purpose**: Detailed explanation of the skill's goal.
- **Approval Plan**: Which commands will run, and how to structure them to minimize approvals (prefer a small number of stable wrappers).

### 2. Create Directory Structure
Run the following command to create the skill directory:
```bash
mkdir -p .github/skills/<skill-name>
```

If your skill includes scripts or templates, add those directories explicitly:
```bash
mkdir -p .github/skills/<skill-name>/scripts
mkdir -p .github/skills/<skill-name>/templates
```

### 3. Create SKILL.md
Read the template from `.github/skills/create-agent-skill/templates/SKILL.md` and create the new `SKILL.md` file:

```bash
cp .github/skills/create-agent-skill/templates/SKILL.md .github/skills/<skill-name>/SKILL.md
```

Then, edit the file to replace the placeholders (`{{skill-name}}`, `{{description}}`, `{{purpose}}`) with the gathered information.

### 4. Update Documentation
Add the new skill to the "Available Skills" table in `docs/agents.md`.

### 5. Verify
Check that the file structure looks like this:
```
.github/skills/<skill-name>/
├── SKILL.md
├── scripts/
└── templates/
```

## References

### Specifications & Documentation
| Resource | What You'll Find |
|----------|------------------|
| [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills) | Official documentation: SKILL.md format, YAML frontmatter fields, progressive disclosure architecture, and complete examples. |
| [Agent Skills Standard](https://agentskills.io/) | The open specification: formal schema, interoperability with other AI tools (Claude, Cursor, OpenAI Codex), and integration guides. |
| [Agent Skills Specification](https://agentskills.io/specification) | Detailed field definitions, validation rules, and edge cases for SKILL.md files. |

### Example Repositories
| Repository | What You'll Find |
|------------|------------------|
| [anthropics/skills](https://github.com/anthropics/skills) | Reference skills from Anthropic: well-structured examples covering common patterns like debugging, documentation, and code review. |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Community collection of skills, custom agents, instructions, and prompts. Good source of real-world patterns. |

### Practical Guides
| Resource | What You'll Find |
|----------|------------------|
| [Teaching AI Your Repository Patterns](https://dev.to/qa-leaders/github-copilot-agent-skills-teaching-ai-your-repository-patterns-1oa8) | Hands-on tutorial: real-world example (Selenium testing), key components that work (Clear Rules, Golden Examples, Templates), and verification tips. |
| [GitHub Changelog Announcement](https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/) | Feature overview, availability across VS Code/CLI/coding agent, and links to community resources. |
