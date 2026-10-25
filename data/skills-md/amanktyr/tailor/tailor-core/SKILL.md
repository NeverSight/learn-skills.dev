---
name: tailor-core
description: Core Tailor software engineering framework. Governs Spec-Driven Development (SDD), the 7-step decision ladder, progressive project memory (.ai/), AST semantic code reuse, and zero-bloat multi-agent discipline.
---

# Tailor Core — Agent Operational Contract

You are operating under the **Tailor** software engineering framework.

> **Core Directive:** *"Make the code fit the project — with zero waste."*

---

## 1. Universal Slash Command Router

When slash commands are triggered by the user or upstream agents, route execution to the corresponding specialized skill:

| Slash Command | Primary Action | Target Skill | Key Artifact Generated / Modified |
| :--- | :--- | :--- | :--- |
| `/constitution` | Review or edit project non-negotiables & intensity | `spec-driven-dev` | `.ai/CONSTITUTION.md` |
| `/spec-new <feature>` | Scaffold user stories, scope, and edge cases | `spec-driven-dev` | `specs/<id>-<name>/spec.md` |
| `/spec-plan <id>` | Generate reuse-aware technical architecture plan | `spec-driven-dev` + `reuse-first` | `specs/<id>-<name>/plan.md` |
| `/spec-tasks <id>` | Generate ordered, complexity-classified tasks | `spec-driven-dev` | `specs/<id>-<name>/tasks.md` |
| `/spec-implement <id>` | Execute tasks sequentially with verified tests | `spec-driven-dev` + `testing` | Production Source Code |
| `/init-project` | Product discovery, stack matrix, and ADR setup | `project-init` | `.ai/` Memory Hierarchy |
| `/analyze-project` | Index frameworks, components, and symbol catalog | `tailor-core` + `reuse-first` | AST In-Memory Catalog |
| `/review` | Multi-dimensional quality, security, and reuse review | `review` | Structured Review Findings |
| `/security-audit` | Static vulnerability, credential leak, and OWASP scan | `security` | Security Findings Report |
| `/dependency-check <pkg>` | Evaluate package for bloat, redundancy, and license | `dependency-governance` + `pragmatism` | Package Governance Verdict |
| `/update-project-memory` | Synchronize `.ai/` files with active codebase reality | `project-memory` | Updated `.ai/*.md` Files |

---

## 2. The 7-Step Pragmatism Ladder (Mandatory Priority)

Before writing any new implementation or adding dependencies, navigate down this ladder and STOP at the first level that solves the requirement:

```
┌────────────────────────────────────────────────────────┐
│ 1. Does this need to exist? (YAGNI)                    │
│    -> Reject speculative complexity or future-proofing.│
├────────────────────────────────────────────────────────┤
│ 2. Already in this codebase?                           │
│    -> Search src/components/, src/lib/, src/utils/.    │
├────────────────────────────────────────────────────────┤
│ 3. Does the Standard Library do it?                    │
│    -> Use crypto.randomUUID(), structuredClone(), etc. │
├────────────────────────────────────────────────────────┤
│ 4. Does a Native Platform / Browser API cover it?      │
│    -> Use <dialog>, <input type="date">, fetch().      │
├────────────────────────────────────────────────────────┤
│ 5. Does an already-installed dependency solve it?      │
│    -> Reuse existing packages in package.json.         │
├────────────────────────────────────────────────────────┤
│ 6. Can it be written as a one-liner / inline helper?   │
│    -> Avoid creating 50-line wrappers for simple logic.│
├────────────────────────────────────────────────────────┤
│ 7. Only then: Write the minimum amount of clean code.  │
│    -> Clean domain boundaries, types, and tests.       │
└────────────────────────────────────────────────────────┘
```

---

## 3. Progressive Disclosure (Context Window Optimization)

To prevent LLM context saturation and reduce token consumption by 40-80%:
1. **Always read `.ai/CONSTITUTION.md` and `.ai/INDEX.md` first.**
2. Load domain memory files strictly on demand:
   - Modifying visual interfaces: Read `.ai/UI.md` and `.ai/CONVENTIONS.md`.
   - Modifying databases or schemas: Read `.ai/DATABASE.md`.
   - Designing backend endpoints: Read `.ai/API.md`.
   - Evaluating or proposing packages: Read `.ai/DEPENDENCIES.md`.
   - Running verification suites: Read `.ai/TESTING.md`.
3. Never read entire repositories into context when AST symbol lookup or file-filtered search is available.

---

## 4. Task Complexity Classification & Execution Workflow

| Complexity | Trigger Characteristics | Required Process |
| :--- | :--- | :--- |
| **TRIVIAL** | Typo fixes, rename local variable, format spacing | Apply localized change directly. Verify build. |
| **SMALL** | Single component edit, single route fix, local bug | Search for existing helpers, apply minimal fix, run targeted test. |
| **MEDIUM** | New feature module, database migration, API endpoint | Query AST reuse catalog, draft brief plan, run unit/integration tests. |
| **LARGE** | Subsystem refactor, state overhaul, multi-model schema | Full Spec-Driven lifecycle (`/spec-new` -> `/spec-plan` -> `/spec-tasks`). |
| **CRITICAL** | Auth, cryptography, payments, permissions, data wipe | Mandatory security scan, risk assessment, explicit confirmation. |

---

## 5. Non-Negotiable Engineering Invariants

1. **Zero Unverified Claims:** Never assert *"All tests pass"* or *"No vulnerabilities found"* without running the verification command and confirming exit code 0.
2. **Reuse Before Creation:** If a matching component or utility exists in the codebase with >=70% semantic similarity, parameterize or extend it rather than creating a duplicate.
3. **No Phantom Dependencies:** Never introduce an external package without evaluating native standard library alternatives and verifying license compatibility.
4. **Preserve Codebase Conventions:** Conform to established formatting, casing, typing rigor, and directory layouts documented in `.ai/`.
5. **Zero Unsolicited Styling:** Never invent, redesign, or alter CSS classes, colors, themes, or inline styles unless styling changes are explicitly requested. If no styling exists and none is requested, emit clean unstyled semantic HTML.
6. **Zero Speculative Bloat:** Adhere to minimal diff discipline. Never introduce mock datasets, premature abstraction wrappers, or obvious filler comments.
7. **Cold-Start Resilience:** When `.ai/` is missing, inspect workspace manifests directly, respect existing code patterns, and advise initializing Tailor (`tailor init`).

