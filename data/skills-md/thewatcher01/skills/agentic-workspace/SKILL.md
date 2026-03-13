---
name: agentic-workspace
description: "Set up and maintain SOTA agentic architectures in VS Code workspaces with multiple projects. Use when: setting up agents, agentic architecture, multi-project workspace, agent hierarchy, context engineering, prompt engineering, skills ecosystem, AGENTS.md, copilot instructions, agent handoffs, orchestrator pattern, progressive disclosure, workspace agent structure. Teaches agent taxonomy design, skill ecosystems, instruction layering, handoff graphs following anthropics/skills, OpenAI Agents SDK, and GitHub Copilot custom agent standards (VS Code 1.106+)."
license: MIT
metadata:
  version: "1.0.0"
  author: TheWatcher01
  agent_support: [copilot, claude, cursor, goose]
  tags: [agents, skills, context-engineering, multi-project, agentic, workspace, sota]
  references:
    - references/agent-template.md
    - references/skill-template.md
    - references/agents-md-template.md
    - references/instruction-template.md
    - references/prompt-template.md
    - references/architecture-patterns.md
---

# Agentic Workspace Skill

Expert guide for designing and implementing SOTA agentic architectures in multi-project
VS Code workspaces. Covers the full stack: agents, skills, instructions, prompts, context
engineering, and the interplay between them.

---

## Core Principles

### 1. Progressive Disclosure (Token Efficiency)
Context is expensive. Load the minimum at startup, expand on demand:

| Tier | What | When | Token Budget |
|------|------|------|-------------|
| **Metadata** | `name` + `description` | Always (startup) | ~100 tokens/skill |
| **Instructions** | Full `SKILL.md` body | On activation | < 5 000 tokens |
| **Resources** | `references/`, `scripts/`, `assets/` | On demand | As needed |

**Rule:** Every piece of context should earn its token cost. Challenge each element: "Does this justify its presence?"

### 2. Layered Context Architecture
Context flows from general to specific. More specific layers override less specific ones.

```
Layer 1  User-level instructions     (~/.agents/skills/, VS Code userdata)
Layer 2  Repository root             AGENTS.md + .github/copilot-instructions.md
Layer 3  Project root                project/AGENTS.md (nearest-file-wins)
Layer 4  Path-specific instructions  .github/instructions/*.instructions.md (applyTo globs)
Layer 5  Skills (triggered)          ~/.agents/skills/ + .github/skills/ (on activation)
Layer 6  Agents (when invoked)       .github/agents/*.agent.md
Layer 7  Prompts (when invoked)      .github/prompts/*.prompt.md
```

**Nearest-file-wins:** The nearest `AGENTS.md` in the directory tree takes precedence.

### 3. Separation of Concerns

| Artifact | Purpose | Scope | Activation |
|----------|---------|-------|------------|
| **Skill** | Reusable capability with scripts/resources | CrossProject portable | Dynamically by task relevance |
| **Instruction** | Project-specific coding rules | Path-scoped or repo-wide | Auto by file match (`applyTo`) |
| **Prompt** | Reusable template for specific task | Workspace or user | Manually invoked |
| **Agent** | Role/persona with tools + handoffs | Workspace or user | Manually selected or via handoff |
| **AGENTS.md** | Context index and entry point for agents | Per directory tree | Always included |

---

## Protocol — Setting Up an Agentic Workspace

### Step 1 — Audit Current State
- List all existing `.agent.md`, `SKILL.md`, `.instructions.md`, `.prompt.md`, `AGENTS.md` files
- Map the project structure (monorepo? multi-root? packages?)
- Identify duplications, gaps, and context pollution risks
- Check if global skills (`~/.agents/skills/`) are in lock file

### Step 2 — Design the Agent Hierarchy
Choose the right architecture pattern (see `references/architecture-patterns.md`):
- **Linear Pipeline**: Research → Plan → Implement → Review (simple, predictable)
- **Orchestrator-Workers**: Supervisor routes to specialists (flexible, SOTA for complex tasks)
- **Swarm/Handoffs**: Lightweight specialist handoffs (good for well-defined roles)

For most workspaces: **Orchestrator at root** + **specialists per project/domain**.

### Step 3 — Define Agent Taxonomy

```
Root (shared across all projects)
├── Orchestrator  — task analysis + routing
├── Research      — web + codebase research, freshness validation
├── Plan          — read-only exploration + structured planning
└── Review        — QA, architecture compliance, testing validation

Project-specific (override or extend root agents)
├── Deploy        — deployment workflows
├── Migration     — database/API migrations
└── <domain>      — domain-specific specialist
```

**Tool scoping by agent role:**
- Research: `['search', 'fetch', 'codebase', 'problems']` — read-only
- Plan: `['search', 'codebase', 'problems']` — read-only
- Review: `['search', 'codebase', 'problems', 'diagnostics']` — read-only
- Implement: `['editFile', 'createFile', 'terminal', 'search', 'codebase']` — full access
- Orchestrator: `['search', 'codebase']` — routing only (minimal tools)

### Step 4 — Design the Skill Ecosystem

```
Global skills (~/.agents/skills/)        — cross-project, install via skills.sh or manual
Project skills (.github/skills/)         — project-specific, committed to repo
```

**Decision criteria:**
- Will this skill be useful in >1 project? → Global
- Is this tightly coupled to this project's stack? → Project-local
- Does it need scripts or data files? → Use `scripts/`, `references/`, `assets/` subdirs

### Step 5 — Write Instructions (Path-Specific Context Injection)

Instructions auto-activate based on `applyTo` glob patterns. Cover every significant directory:

```yaml
# Standard instruction set for a TypeScript project
applyTo: "src/core/**"          → domain rules (zero deps, Result pattern)
applyTo: "src/adapters/**"      → adapter rules (implement ports, DI injection)  
applyTo: "src/cli/**"           → CLI conventions (framework, one-file-per-command)
applyTo: "**/tests/**"          → test rules (Vitest, no infra deps for unit tests)
applyTo: "**/*.test.ts"         → same as above
```

### Step 6 — Write AGENTS.md Files

One per project + one at monorepo root (if applicable):
- **Root AGENTS.md**: Monorepo index (projects, shared agents, global skills, architecture)
- **Project AGENTS.md**: Project-specific details (stack, commands, build/test, local skills)

See `references/agents-md-template.md` for templates.

### Step 7 — Connect to MCP and VS Code

- Add `.vscode/mcp.json` for MCP server auto-discovery
- Add `chat.agentFilesLocations` in `settings.json` if agents live in non-standard paths
- Ensure `copilot-instructions.md` is in root `.github/` for GitHub-hosted projects

### Step 8 — Verify

Checklist before considering the agentic setup complete:
- [ ] Nearest-file-wins works (test by opening files in different subprojects)
- [ ] All agents appear in Copilot Chat agents dropdown
- [ ] Skills trigger correctly by description keyword match
- [ ] Instructions activate only for matching `applyTo` patterns
- [ ] AGENTS.md at each level is non-redundant with parent AGENTS.md
- [ ] No secrets or credentials in any agent/skill/instruction file
- [ ] Tool scoping is correct (read-only agents can't edit files)

---

## Workspace File Structure (Reference)

```
monorepo-root/
├── AGENTS.md                                 ← Monorepo index (shared context)
├── .github/
│   ├── copilot-instructions.md               ← Repo-wide Copilot context
│   ├── agents/                               ← Shared agents (all projects)
│   │   ├── Orchestrator.agent.md
│   │   ├── Research.agent.md
│   │   ├── Plan.agent.md
│   │   └── Review.agent.md
│   ├── instructions/                         ← Cross-project path rules
│   │   ├── typescript.instructions.md        ← applyTo: "**/*.ts"
│   │   └── testing.instructions.md           ← applyTo: "**/tests/**"
│   ├── prompts/                              ← Shared reusable prompts
│   │   ├── smart-commit.prompt.md
│   │   └── code-review.prompt.md
│   └── skills/                              ← Optional project-specific skills
│
├── project-a/
│   ├── AGENTS.md                            ← Project-specific index (overrides root)
│   └── .github/
│       ├── agents/                          ← Project-specific agents
│       ├── instructions/                    ← Project-specific path rules
│       └── skills/                         ← Project-specific skills
│
└── project-b/
    ├── AGENTS.md
    └── .github/
        └── instructions/
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Duplicate AGENTS.md at multiple levels with same content | Context confusion, drift risk | Root = index, project = detail, no duplication |
| Monolithic agent doing Research + Plan + Review | Violates SRP, context bloat | Split into specialized agents with handoffs |
| Hardcoded project info in global skills | Global skills become un-reusable | Keep global skills generic, project context in local skills |
| Missing `applyTo` on instructions | Instructions activate everywhere, pollute context | Always set `applyTo` to narrowest appropriate glob |
| Agent with all tools (editFile + search + terminal) | No guardrails, risky agent | Scope tools by role (read-only for Research/Plan/Review) |
| Skills > 500 lines in SKILL.md | Context overload | Move detail to `references/` subdirectory |
| Prompts tightly coupled to one agent | Reduces reusability | Use `agent: "agent"` default, or bind explicitly per use case |
| No handoff graph | Agents are isolated silos | Define explicit handoffs with clear labels and prompts |

---

## See Also

- `references/agent-template.md` — `.agent.md` format with all fields documented
- `references/skill-template.md` — `SKILL.md` format per agentskills.io spec
- `references/agents-md-template.md` — `AGENTS.md` templates (monorepo root, project, standalone)
- `references/instruction-template.md` — `.instructions.md` template with `applyTo` patterns
- `references/prompt-template.md` — `.prompt.md` template and best practices
- `references/architecture-patterns.md` — 8 SOTA agent patterns with decision matrix
