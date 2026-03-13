---
name: skill-system-foundry
description: >
  Designs, builds, validates, and evolves AI-agnostic skill systems composed of
  skills (with optional capabilities) and roles. Activates when the user wants
  to: create a new skill or capability, define or refine a role, restructure
  their skill/role hierarchy, migrate from flat skills to a router+capabilities
  pattern, audit skill system consistency, or reason about token efficiency and
  maintainability trade-offs. Also triggers when the user mentions "skill
  system", "canonical skill", "orchestrator", or discusses organizing
  AI-agnostic automation across multiple tools like Claude Code, Cursor, or
  Codex.
allowed-tools: Bash Read Write Edit Glob Grep
compatibility: Requires Python 3.12+ (stdlib only) for validation, scaffolding, and bundling scripts.
license: MIT
metadata:
  author: Milan Horvatovič
  version: 1.0.0
  spec: agentskills.io/1.0
---

# Skill System Foundry

A meta-skill for constructing and evolving AI-agnostic skill systems.

This skill governs the creation and maintenance of a two-layer architecture: **skills** (with optional capabilities) and **roles**. All skills produced by this system follow the [Agent Skills specification](references/agentskills-spec.md). They incorporate [authoring best practices](references/authoring-principles.md) from official vendor guides. Role contracts align with [tool integration guidance](references/tool-integration.md#convention-coexistence) for seamless deployment across platforms.

**Important:** Capabilities are optional, granular sub-skills within a parent skill. Do not create capabilities by default. Only introduce them when the integrator explicitly asks for them or when the domain clearly demands decomposition (3+ distinct operations with different trigger contexts). Start with a standalone skill; evolve to router+capabilities only when justified.

## Architecture Overview

The skill system follows a strict two-layer architecture — **skills** and **roles**. Dependencies flow strictly downward — never the reverse. A capability must never know it's being orchestrated. A role references skills but never other roles.

The dependency direction governs **references between layers**, not where orchestration begins. Two valid orchestration paths exist:

```
Path 1:  orchestration skill → roles → skills (with optional capabilities)
Path 2:  skill (standalone or router) → role(s) → skill's capabilities
```

- **Path 1 — Coordination-only skill.** A lean standalone skill sequences roles across domains. Contains no domain logic.
- **Path 2 — Self-contained skill.** A domain skill loads one or more roles for interactive workflow logic. The skill owns capabilities; roles provide responsibility, authority, and constraints, plus handoff rules, sequencing, and interaction patterns.

See [`references/architecture-patterns.md`](references/architecture-patterns.md#orchestration-skills) for decision checklists and constraints per path.

Each layer has a clear responsibility:

- **Skills** — Canonical, AI-agnostic knowledge and logic. Conform to the Agent Skills specification. A skill handles a task directly (standalone) or optionally routes to capabilities for complex domains that warrant decomposition.
- **Roles** — Canonical, AI-agnostic orchestration contracts. A role defines responsibility, authority, and constraints, plus handoff rules and workflow sequencing while composing multiple skills/capabilities.

## Bundled Resources

### references/ — Read when you need guidance

- [`references/authoring-principles.md`](references/authoring-principles.md) — Shared skill authoring principles (cross-platform consensus)
- [`references/architecture-patterns.md`](references/architecture-patterns.md) — Standalone vs router decisions and architecture patterns
- [`references/tool-integration.md`](references/tool-integration.md) — Tool-specific paths, discovery, and deployment
- [`references/agentskills-spec.md`](references/agentskills-spec.md) — Agent Skills specification compliance guide
- [`references/claude-code-extensions.md`](references/claude-code-extensions.md) — Claude Code-specific frontmatter and features
- [`references/codex-extensions.md`](references/codex-extensions.md) — Codex agents/openai.yaml and discovery hierarchy
- [`references/cursor-extensions.md`](references/cursor-extensions.md) — Cursor cross-vendor discovery and rules migration
- [`references/anti-patterns.md`](references/anti-patterns.md) — Common mistakes and how to avoid them
- [`references/directory-structure.md`](references/directory-structure.md) — Full directory layout and conventions
- [`references/workflows.md`](references/workflows.md) — Step-by-step workflows for creation, migration, deployment, and auditing

### assets/ — Copy and fill in when creating components

- `assets/skill-standalone.md` — Template for standalone skills
- `assets/skill-router.md` — Template for router skills with capabilities
- `assets/capability.md` — Template for capabilities under a router
- `assets/role.md` — Template for roles
- `assets/manifest.yaml` — Manifest schema template

### scripts/ — Run for validation and auditing

- `scripts/audit_skill_system.py` — Audit skill system structure and consistency
- `scripts/validate_skill.py` — Validate a single skill against the spec
- `scripts/scaffold.py` — Scaffold new skills or roles from templates
- `scripts/bundle.py` — Bundle a skill into a self-contained zip bundle for distribution
- `scripts/lib/validation.py` — Shared name validation logic
- `scripts/lib/references.py` — Reference scanning, resolution, and graph traversal
- `scripts/lib/constants.py` — Centralized constants and configuration

## Core Principles

### 1. Agent Skills Specification Compliance

All skills must conform to the Agent Skills specification (agentskills.io). Every registered skill directory contains a `SKILL.md` with valid YAML frontmatter. The `name` field matches the parent directory name, lowercase + hyphens only, max 64 chars. The `description` field is max 1024 chars, third-person, and describes both what the skill does and when to trigger it.

Note: capabilities are discovery-internal sub-skills. Their entry point is `capability.md`. Capability frontmatter is optional (use it when portability/promotion to standalone is likely).

Progressive disclosure is respected at all levels:
- **Level 1: Metadata** (~100 tokens) — name + description, always in context
- **Level 2: Instructions** (<5000 tokens / recommended max 500 lines) — loaded when triggered
- **Level 3: Resources** (unlimited) — scripts, references, assets, on demand

### 2. Token Economy

Discovery tokens are always present and expensive. Execution tokens are only paid when activated. Register one skill per domain, not one per capability. Keep router SKILL.md files lean. Push detail into capabilities or references. Prefer a standalone skill until the domain justifies capabilities.

### 3. Conciseness

The model is already smart. Only add context it doesn't already have. Challenge each piece of information: "Does the model really need this explanation?" See [`references/authoring-principles.md`](references/authoring-principles.md) for detailed guidance.

### 4. Degrees of Freedom

Match specificity to the task's fragility. High freedom for flexible tasks, low freedom for fragile operations. See [`references/authoring-principles.md`](references/authoring-principles.md).

### 5. Write Once, Adapt Everywhere

Domain knowledge is authored exactly once in the canonical layer (skills and roles). When domain knowledge changes, one file changes. Tool-specific deployment pointers, if needed, are optional user-managed customizations — implemented as wrapper files or symlinks. When deploying, always ask the user which mechanism to use. See [`references/tool-integration.md`](references/tool-integration.md#symlink-based-deployment-pointers) for the decision guide.

---

## Quick Reference: When to Read What

| Task | Resource |
|---|---|
| Understand the concept and goals | Architecture Overview and Core Principles (this file) |
| Create a new skill | [`assets/skill-standalone.md`](assets/skill-standalone.md) or [`assets/skill-router.md`](assets/skill-router.md) |
| Create a new capability | [`assets/capability.md`](assets/capability.md) + [`references/workflows.md`](references/workflows.md#adding-a-capability-to-an-existing-router-optional) |
| Create a new role | [`assets/role.md`](assets/role.md) |
| Deploy to a specific tool (wrapper or symlink) | [`references/tool-integration.md`](references/tool-integration.md) + [`references/workflows.md`](references/workflows.md#setting-up-symlink-based-pointers) |
| Set up the manifest | [`assets/manifest.yaml`](assets/manifest.yaml) |
| Write effective descriptions | [`references/authoring-principles.md`](references/authoring-principles.md) |
| Decide skill architecture (standalone vs router) | [`references/architecture-patterns.md`](references/architecture-patterns.md#standalone-vs-router-when-to-split) |
| Deploy to Claude Code, Cursor, Kiro (wrapper or symlink; Codex, Gemini CLI, Warp, OpenCode, Windsurf scan natively) | [`references/tool-integration.md`](references/tool-integration.md) |
| Migrate flat skills to router | [`references/workflows.md`](references/workflows.md#migrating-flat-skills-to-router-pattern) |
| Audit skill system | `scripts/audit_skill_system.py` + [`references/workflows.md`](references/workflows.md#auditing-system-consistency) |
| Validate a skill | `scripts/validate_skill.py` |
| Scaffold a new component | `scripts/scaffold.py` |
| Check spec compliance | [`references/agentskills-spec.md`](references/agentskills-spec.md) |
| Understand directory layout | [`references/directory-structure.md`](references/directory-structure.md) |
| Use Claude Code extensions | [`references/claude-code-extensions.md`](references/claude-code-extensions.md) |
| Use Codex extensions | [`references/codex-extensions.md`](references/codex-extensions.md) |
| Use Cursor features | [`references/cursor-extensions.md`](references/cursor-extensions.md) |
| Package a skill as a zip bundle | `scripts/bundle.py` + [`references/workflows.md`](references/workflows.md#packaging-a-skill-as-a-zip-bundle) |
| Review common mistakes | [`references/anti-patterns.md`](references/anti-patterns.md) |
