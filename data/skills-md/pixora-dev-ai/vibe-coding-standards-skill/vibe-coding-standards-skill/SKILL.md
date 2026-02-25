---
name: vibe-coding-standards-skill
description: |
  A comprehensive skill for enforcing project-specific architecture, styling, security, and quality rules. 
  Use this skill when: (1) Reviewing code for compliance, (2) Generating new components or modules, 
  (3) Refactoring existing code, or (4) Setting up a new project's coding standards.
license: MIT
metadata:
  author: Pixora-dev-ai
  version: 1.0.0
---

# Coding Standards Enforcer

This skill provides a complete framework for maintaining high code quality and architectural consistency across the project.

## Core Workflows

### 1. Code Review & Auditing

Before approving any code, validte it against the Master Rules.

- **Primary Reference**: See [references/master-rules.json](references/master-rules.json) for the "Critical" checks (Architecture, Security, Performance).
- **Rule Index**: See [references/rules-index.json](references/rules-index.json) for a full list of specialized rule sets.

### 2. Mandatory Enforcement & Detection

To actively enforce these rules, use the bundled detection scripts. These MUST be run during CI or pre-commit.

- **Architecture Audit**: Run `scripts/audit/audit_engine.py .`
  - Scans for forbidden patterns (e.g., hardcoded secrets, relative imports, bad dependencies).
  - Configured via `scripts/audit/detectors_config.json`.
- **Linter Config**: Run `scripts/audit/generate_eslint.sh`
  - Generates a strict `.eslintrc.js` that enforces clean code, accessibility, and hooks rules at the IDE level.

### 3. Feature Implementation

When building new features, consult the relevant domain-specific rules:

- **UI/UX & Components**: See [references/ui-ux-engineering.rules.json](references/ui-ux-engineering.rules.json) and [references/component-modularity.rules.json](references/component-modularity.rules.json).
- **State & Data Flow**: See [references/dependency-architecture.rules.json](references/dependency-architecture.rules.json).
- **Styling**: See [references/styling-tokens.rules.json](references/styling-tokens.rules.json).
- **Assets**: See [references/assets-handling.rules.json](references/assets-handling.rules.json).

### 4. Project Setup

To initialize these rules in a new repository:

1. Run `scripts/init_project_rules.sh` to configure the project name and tokens.
2. Use `assets/project-config.template.json` to customize the strictness and tech stack.

## Advanced References

- **AI & Intelligence Architecture**: See [references/ai-core-architecture.md](references/ai-core-architecture.md) for integrating AI modules.
- **Security & Privacy**: See [references/security-privacy.rules.json](references/security-privacy.rules.json).
- **Performance**: See [references/performance.rules.json](references/performance.rules.json).
- **Testing**: See [references/testing.rules.json](references/testing.rules.json).

> [!NOTE]
> Always prefer the "Single Source of Truth" defined in `master-rules.json` if there is a conflict.
