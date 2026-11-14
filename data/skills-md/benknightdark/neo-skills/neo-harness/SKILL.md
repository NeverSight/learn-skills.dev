---
name: neo-harness
description: >
  Use this skill when you need to inspect a target project codebase and generate or improve a tailored,
  comprehensive AGENTS.md file (Harness Workflow Specification) that enforces strict AI agent
  harness rules, feedback sensors, execution SOP, orchestration topologies, and safety redlines.
  Supports non-interactive script execution via scripts/generate-agents-md.py.
  The generated AGENTS.md MUST NOT exceed 32 KiB in size.
license: MIT
metadata:
  version: "1.0.0"
  type: "unified-harness-generator"
---

# Unified Agent Harness Architect & Workflow Generator

This skill integrates three core Agent engineering domains (**Harness Assessment**, **Execution Protocol**, and **Orchestration Architecture**) to analyze a target project and generate a tailored, strict `AGENTS.md` file (Harness Workflow Specification).

## Core Principle

```text
Agent = Model (Reasoning & Generation) + Harness (Guides + Sensors + Gates + Topologies)
```

The generated `AGENTS.md` acts as the single source of truth governing all AI Agents operating in the project.

> [!IMPORTANT]
> **Template Compliance & Size Constraint**:
> Any created or modified `AGENTS.md` MUST strictly adhere to the design specification of [`assets/AGENTS.md.template`](assets/AGENTS.md.template) (containing 4 mandatory sections: Project Overview, Commands Table, 9-stage Workflow Mermaid loop, and Forbidden Antipattern Redlines Table) and MUST NOT exceed 32 KiB (32,768 bytes).

---

## Quick Automation (Non-Interactive Generator Script)

To quickly analyze a repository and generate or preview an `AGENTS.md` file, run the non-interactive script:

```bash
# Preview generated content (dry-run)
python3 skills/neo-harness/scripts/generate-agents-md.py --target-dir /path/to/repo --dry-run

# Generate AGENTS.md directly in target repository
python3 skills/neo-harness/scripts/generate-agents-md.py --target-dir /path/to/repo --force

# Validate existing AGENTS.md against assets/AGENTS.md.template design specification
python3 skills/neo-harness/scripts/generate-agents-md.py --target-dir /path/to/repo --validate
```

---

## Workflow SOP

### Step 1 — Perceive Target Repository
1. Inspect project root and structure manually or via `scripts/generate-agents-md.py`:
   - Configuration files: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, etc.
   - Build, lint, and test toolchains.
   - Existing guidelines: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, README.
   - CI workflows: `.github/workflows/`, GitLab CI, etc.
2. Identify primary languages, test suites, and fast local feedback sensors.

### Step 2 — Reason & Synthesize Harness Rules
Load detailed reference knowledge as needed:
* **Harness Assessment & Sensors**: Read [references/harness-assessment.md](references/harness-assessment.md) to rate harnessability and define computational vs. inferential sensors.
* **Execution Protocol & SOP**: Read [references/execution-protocol.md](references/execution-protocol.md) to enforce the 5 Harness Laws, dual-loop SOP, zero-fake pass, and antipattern rules.
* **Orchestration Topologies**: Read [references/orchestration-patterns.md](references/orchestration-patterns.md) to select appropriate routing, chaining, or human-in-the-loop (HITL) gates.

### Step 3 — Generate & Format `AGENTS.md`
Use `scripts/generate-agents-md.py` with [assets/AGENTS.md.template](assets/AGENTS.md.template) as the strict baseline template.
All created or modified `AGENTS.md` files MUST strictly contain the following 4 structural sections in order:
1. **`## 1. Project Overview`**: Primary tech stack, modular architecture, and coding conventions.
2. **`## 2. Commands`**: Standard markdown table (`Command Type`, `Exact Command Line`, `Purpose / Scope`) listing test, typecheck, lint, build, or syntax check commands.
3. **`## 3. Workflow`**: The mandatory 9-stage closed loop Mermaid diagram (`graph TD` from Step1 to Step9) followed by the 9 numbered step definitions.
4. **`## 4. Forbidden Antipattern Redlines`**: Standard markdown table (`Forbidden Action`, `Why It Is Prohibited`, `Required Behavior`) specifying non-negotiable redlines.

### Step 4 — Verify Template Compliance & Quality Gate
1. Validate structural compliance against `assets/AGENTS.md.template`:
   - Run `python3 skills/neo-harness/scripts/generate-agents-md.py --target-dir /path/to/repo --validate`.
2. Check the file size of the generated `AGENTS.md`:
   - Must be `<= 32,768 bytes`.
   - If over 32 KiB, prune redundant descriptions or move extended reference docs to separate files under `.agents/` or `docs/`.
3. Validate syntax and markdown formatting.
