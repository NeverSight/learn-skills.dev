---
name: project-memory
description: Manages the .ai/ progressive project memory layer, context window optimization, document synchronization, and live drift detection between source reality and cached memory.
---

# Project Memory Skill

Activate this skill when reading, creating, updating, or repairing `.ai/` memory files, resolving documentation drift, or managing agent context windows.

> **Operational Principle:** *Project memory is an indexed cache of project facts. Source code is the ultimate ground truth.*

---

## 1. Project Memory Hierarchy & Source of Truth

When conflicting information is detected between files:
1. **Source of Truth 1 (Highest):** Verifiable source code, database schemas (`schema.prisma`, `models.py`, `migrations/`), and package manifests (`package.json`, `Cargo.toml`, `go.mod`).
2. **Source of Truth 2:** Project Memory Files (`.ai/STACK.md`, `.ai/API.md`, `.ai/DATABASE.md`).
3. **Source of Truth 3 (Lowest):** Outdated inline comments, legacy markdown notes, or unverified chat instructions.

If memory conflicts with source code: **Trust the source code, flag the drift, and immediately update the memory document.**

---

## 2. Progressive Disclosure Rules (Token Optimization)

To minimize context token consumption and maintain maximum LLM reasoning capacity:
* **Entry Point:** Always read `.ai/CONSTITUTION.md` and `.ai/INDEX.md` first.
* **Domain Documents (Read strictly on demand):**
  - Architecture decisions: `.ai/ARCHITECTURE.md`, `.ai/DECISIONS.md`
  - UI components and design tokens: `.ai/UI.md`, `.ai/CONVENTIONS.md`
  - Endpoints, contracts, and payloads: `.ai/API.md`
  - Schemas, migrations, and ORMs: `.ai/DATABASE.md`
  - Installed packages and governance: `.ai/DEPENDENCIES.md`
  - Security policies and secret management: `.ai/SECURITY.md`
  - Verification runners and commands: `.ai/TESTING.md`

---

## 3. Drift Detection & Live Repair Workflow

When finishing any non-trivial coding task or executing `/update-project-memory`:
1. Check if dependencies were added, removed, or upgraded. If so, synchronize `.ai/DEPENDENCIES.md`.
2. Check if new database models or migrations were introduced. If so, synchronize `.ai/DATABASE.md`.
3. Check if new API endpoints or route contracts were created. If so, synchronize `.ai/API.md`.
4. Check if new architectural decisions were adopted. If so, record an ADR in `.ai/DECISIONS.md`.
5. Verify that `.ai/INDEX.md` accurately references all active domain memory files.
