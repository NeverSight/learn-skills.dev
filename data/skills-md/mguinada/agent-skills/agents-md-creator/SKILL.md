---
name: agents-md-creator
description: |
  Create, optimize, and maintain AGENTS.md and CLAUDE.md files using progressive disclosure.

  Use when: User wants to create AGENTS.md/CLAUDE.md, optimize existing AI documentation,
  implement progressive disclosure, detect project structure (monorepo/polyrepo), or prevent
  documentation bloat.

  Triggers on: "create agents.md", "update AGENTS.md", "AI documentation", "project context",
  "monorepo documentation", "progressive disclosure", "Claude Code context", or when AI repeatedly
  asks the same questions about the project.
---

# AGENTS.md / CLAUDE.md Creator

Create and maintain AI documentation files that help agents understand your project efficiently using progressive disclosure principles.

## Core Philosophy: Iron Rule

**Never use line count as a metric.** Judge by single source of truth (no duplication), cognitive relevance (only task-relevant info), and maintainability (change once, not everywhere).

## Quick Decision Trees

### "I want to create AGENTS.md"

```
Create AGENTS.md?
├─ Detect project structure → references/project_detection.md
├─ Determine if monorepo → Check for apps/, packages/, workspace configs
├─ Extract essential info → README.md, package.json, folder layout
├─ Choose template → references/templates.md
└─ Apply progressive disclosure → references/progressive_disclosure.md
```

### "My AGENTS.md is too bloated"

```
Optimize existing AGENTS.md?
├─ Back up file first → cp AGENTS.md AGENTS.md.bak.$(date)
├─ Classify each section → references/progressive_disclosure.md#content-classification
├─ Create Level 2 references → docs/references/ for detailed content
├─ Update Level 1 → Keep only high-frequency, critical info
└─ Verify completeness → Ensure no information is lost
```

### "I don't know my project structure type"

```
Detect project structure?
├─ Check for apps/ or packages/ directories → Monorepo
├─ Check for workspace config (pnpm-workspace.yaml, etc.) → Monorepo
├─ Check for lerna.json, turbo.json, nx.json → Monorepo
├─ Single package.json at root → Polyrepo (likely)
└─ Show detection confidence and ask user to confirm
```

## Project Structure Detection

### Auto-Detection Indicators

| Indicator | Type | Evidence |
|-----------|------|----------|
| `apps/` directory exists | Monorepo | Multiple applications |
| `packages/` directory exists | Monorepo | Shared libraries |
| `pnpm-workspace.yaml` | Monorepo | pnpm workspace config |
| `turbo.json` | Monorepo | Turborepo build system |
| `lerna.json` | Monorepo | Lerna monorepo |
| `nx.json` | Monorepo | Nx monorepo |
| Single `package.json` at root | Polyrepo | Single package |
| Multiple top-level `src/` dirs | Polyrepo | Multiple projects |

### Detection Confidence Levels

```
High confidence (≥3 indicators): Proceed without asking
Medium confidence (1-2 indicators): Show findings, ask user to confirm
No clear indicators: Ask user directly
```

## Progressive Disclosure Architecture

### Three-Level Loading System

```
Level 1 (AGENTS.md) - Always loaded
├── One-line project description
├── Essential commands (run, test, build)
├── Repository structure (top-level dirs only)
├── Reference index tables (multi-entry)
└── Key entry points

Level 2 (docs/references/) - On-demand
├── Detailed SOP flows
├── Edge case handling
├── Complete config examples
└── Historical decisions

Level 3 (Project files) - As needed
├── README.md
├── package.json files
└── Config files
```

### Multi-Entry Principle

The same Level 2 resource can have **multiple entry points** for different discovery paths:

| Entry | Location | Trigger Scenario | User Mindset |
|-------|----------|------------------|--------------|
| Reference index | Start | "I have an error/problem" | "What doc has the answer?" |
| Before-change table | Middle | "About to modify code" | "What should I know first?" |
| Trigger index | End | "Long conversation, need to re-orient" | "Which doc was that again?" |

**This is NOT duplication.** It's like a book having a table of contents, an index, and quick reference cards.

## AGENTS.md vs CLAUDE.md

### File Relationship

```
AGENTS.md # Root context - always loaded by agents
CLAUDE.md # Required for Claude Code - loads AGENTS.md
```

### CLAUDE.md Contents (Minimal Bridge)

```markdown
Read [AGENTS.md](AGENTS.md) before starting any task.
```

CLAUDE.md exists only because Claude Code doesn't load AGENTS.md natively. Keep it minimal.

## AGENTS.md Essential Structure

### Required Sections (Level 1)

| Section | Purpose | Keep Minimal |
|---------|---------|--------------|
| Project description | One-line summary | ✅ |
| Essential commands | run, test, build | ✅ |
| Repository structure | Top-level directories only | ✅ |
| Reference index | Pointers to detailed docs | ✅ |
| Key entry points | Common task starting points | ✅ |

### Never Include in AGENTS.md (Level 1)

| Content | Why | Where Instead |
|---------|-----|---------------|
| Detailed explanations | Bloats context | Level 2 references |
| Code examples >1 line | Can be looked up | Level 2 references |
| Duplicated content | Maintenance burden | Single source |
| Historical decisions | Low frequency | Level 2 references |

## Content Classification Decision Tree

For each section, ask:

```
Is this high-frequency use?
├─ Yes → Level 1 (AGENTS.md)
└─ No → ↓

Is the violation consequence severe?
├─ Yes → Level 1 (AGENTS.md)
└─ No → ↓

Is there a code pattern to copy directly?
├─ Yes → Level 1 keep the pattern
└─ No → ↓

Is there a clear trigger condition?
├─ Yes → Level 2 + trigger condition
└─ No → Consider deleting
```

## Reference Index Format

### At Start (Problem-Oriented)

```markdown
## Reference Index (When you encounter problems)

| Trigger scenario | Document | Core content |
|------------------|----------|--------------|
| Build fails after dependency change | `docs/references/build-sop.md` | Dependency order, clean build |
| Test environment variables not loading | `docs/references/env-setup.md` | .env files, globalEnv config |
| Cache not invalidating | `docs/references/caching.md` | outputs, inputs, env keys |
```

### At Middle (Task-Oriented)

```markdown
## Before Modifying Code

| What you're changing | Read this first | Key gotchas |
|---------------------|-----------------|-------------|
| Build configuration | `docs/references/build-sop.md` | dependsOn order matters |
| Environment setup | `docs/references/env-setup.md` | globalEnv affects all tasks |
| Cache behavior | `docs/references/caching.md` | outputs required for file-producing tasks |
```

### At End (Re-Orientation)

```markdown
## Reference Trigger Index

| When to read | Document | What you'll find |
|--------------|----------|------------------|
| Build fails | `docs/references/build-sop.md` | Dependency troubleshooting |
| Env issues | `docs/references/env-setup.md` | .env and variable setup |
| Cache problems | `docs/references/caching.md` | Hash input debugging |
```

## Anti-Patterns to Avoid

| Anti-Pattern | Wrong | Right |
|------------|-------|-------|
| **Line count as goal** | "Reduced from 2000 to 500 lines" | Assess by duplication and relevance, not line count |
| **References without triggers** | `See build-sop.md for details` | Include trigger conditions: "When build fails after dependency changes" |
| **Moving code patterns to Level 2** | Move frequently-used code examples | Keep copyable patterns in Level 1 |
| **Deleting instead of moving** | Delete "unimportant" sections | Move to Level 2, keep trigger in Level 1 |
| **Moving while simplifying** | Move and edit content simultaneously | Move verbatim first, simplify separately with confirmation |

## Monorepo-Specific Considerations

### Additional Detection for Monorepos

When a monorepo is detected, also extract:

| Information | Source | Purpose |
|-------------|--------|---------|
| Package names | `apps/*/package.json`, `packages/*/package.json` | Understanding modules |
| Package purposes | package.json `description` field, README files | What each package does |
| Internal dependencies | workspace:* references | Dependency graph |
| Build system | turbo.json, nx.json, lerna.json | Task orchestration |
| Shared patterns | across packages/ | Common conventions |

### Package Name Detection

Package naming varies significantly across monorepos. Detect actual package names from:

1. **Directory patterns:**
   - `apps/*` → Application packages
   - `packages/*` → Library packages
   - `services/*` → Backend services

2. **Package naming conventions:**
   - Scoped: `@repo/*`, `@company/*`, `@project/*`
   - Unscoped: `backend`, `frontend`, `api`, `web`
   - Mixed: Both scoped and unscoped in same repo

3. **Common backend package names:**
   - `@repo/api`, `@repo/backend`, `@repo/server`
   - `apps/api`, `apps/backend`, `apps/server`
   - `services/api`, `services/backend`

4. **Common frontend package names:**
   - `@repo/web`, `@repo/frontend`, `@repo/app`
   - `apps/web`, `apps/frontend`, `apps/app`
   - `apps/admin`, `apps/dashboard`

### Monorepo AGENTS.md Additions

**Generate the package table dynamically based on actual project structure:**

```markdown
## Monorepo Structure

| Package | Location | Purpose | Key commands |
|---------|----------|---------|--------------|
| `backend` | apps/backend | REST API server | `turbo run dev --filter=backend` |
| `frontend` | apps/web | Next.js web app | `turbo run dev --filter=frontend` |
| `ui` | packages/ui | Shared React components | `turbo run build --filter=ui` |

## Working with Packages

- Run task in specific package: `turbo run <task> --filter=<package-name>`
- Run only changed packages: `turbo run <task> --affected`
- Include dependents: `turbo run <task> --filter=...<package-name>`
- Run by directory: `turbo run <task> --filter=./apps/*`
```

**Key guidelines for package tables:**

1. **Use actual package names** from package.json `name` field
2. **Infer purpose** from description field or directory name
3. **Group by type** (apps vs packages) if helpful
4. **Keep it concise** — focus on most commonly used packages
5. **Reference detailed docs** for complete package list

## Verification Checklist

After creating or modifying AGENTS.md, verify:

### Information Completeness (Most Important)

- [ ] Every section from original has a home (in Level 1, Level 2, or has canonical source)
- [ ] Level 2 files match original content exactly (no "simplification" during move)
- [ ] No content was silently deleted
- [ ] No line count statistics were mentioned

### Structure Quality

- [ ] Reference index at document start
- [ ] Core commands table complete
- [ ] Iron rules/prohibitions with code examples
- [ ] Common error diagnostics (symptom → cause → fix)
- [ ] Code patterns directly copyable
- [ ] Directory mapping (function → file)
- [ ] "Before modifying code" table
- [ ] Reference trigger index at document end
- [ ] Every Level 2 reference has trigger conditions
- [ ] All referenced files exist

## Information Recording Principles

Add this to AGENTS.md after project description to prevent future bloat:

```markdown
## Information Recording Principles (Agents Must Read)

This document uses **progressive disclosure** to optimize agent effectiveness.

### Level 1 (This file) contains only

| Type | Example |
|------|---------|
| Core commands | `npm run dev`, `npm test` |
| Iron rules/prohibitions | Must use lazy loading |
| Common error diagnostics | Symptom → cause → fix (complete flow) |
| Code patterns | Directly copyable code blocks |
| Directory navigation | Function → file mapping |
| Trigger index tables | Pointers to Level 2 |

### Level 2 (docs/references/) contains

| Type | Example |
|------|---------|
| Detailed SOP flows | Complete 20-step guides |
| Edge case handling | Rare error diagnostics |
| Complete config examples | All parameter descriptions |
| Historical decisions | Why it was designed this way |

### When recording information

1. **Assess frequency:** High frequency → Level 1, otherwise Level 2
2. **Level 1 references Level 2 must include:**
   - Trigger condition (when to read)
   - Content summary (what you'll find)
3. **Never:**
   - Place low-frequency detailed flows in Level 1
   - Reference Level 2 without trigger conditions
```

## Reference Files

| File | Purpose |
|------|---------|
| [references/project_detection.md](./references/project_detection.md) | Detailed project structure detection |
| [references/templates.md](./references/templates.md) | AGENTS.md templates for different project types |
| [references/progressive_disclosure.md](./references/progressive_disclosure.md) | Progressive disclosure deep dive |
| [references/anti_patterns.md](./references/anti_patterns.md) | Common anti-patterns with examples |
