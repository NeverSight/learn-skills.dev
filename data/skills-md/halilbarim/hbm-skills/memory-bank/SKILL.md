---
name: memory-bank
description: "Set up and manage a Memory Bank system for cross-session context continuity across AI coding agents. Use when the user mentions 'memory bank' with any action intent — setup, install, initialize, init, update, refresh, sync, status, check, read, show, review, display, or equivalents in any language (e.g. Turkish: kur, kurulum, güncelle, durumu, oku; German: einrichten, aktualisieren; Spanish: configurar, actualizar; French: installer, mettre à jour). Supports Claude Code, Cursor, Windsurf, Cline, GitHub Copilot, Roo Code, Aider, Antigravity, and OpenAI Codex."
---

# Memory Bank Skill

## Overview

Memory Bank is a cross-session context continuity system for AI coding agents. It maintains a `memory-bank/` directory in the project root with structured markdown files that capture project knowledge, architecture decisions, progress, and active context. Every AI agent reads these files at session start, ensuring continuity across sessions and across different agents working on the same project.

This skill handles four intents: **SETUP**, **UPDATE**, **STATUS**, and **READ**. It detects user intent from natural language in any language.

## Intent Detection

Detect the user's intent from their message. The user may write in any language — use natural language understanding to map to the correct intent.

| Intent | Trigger Words (examples, not exhaustive) |
|--------|------------------------------------------|
| **SETUP** | setup, install, initialize, init, create, bootstrap, kur, kurulum, başlat, einrichten, configurar, installer, configurer, 설치, セットアップ |
| **UPDATE** | update, refresh, sync, güncelle, yenile, aktualisieren, actualizar, mettre à jour, 업데이트, 更新 |
| **STATUS** | status, check, durumu, durum, kontrol, estado, statut, 상태, ステータス |
| **READ** | read, show, review, display, present, oku, göster, lesen, anzeigen, lire, leer, mostrar, 읽기, 読む |

Route to the matching flow below. If the intent is ambiguous, ask the user which action they want.

---

## SETUP Flow

Follow these steps in order. Get user confirmation at each major step.

### Step 1: Language & Profile Preference

**1a. Language:**

Ask the user which language the memory bank files should be written in:
- **TR** (Turkish)
- **EN** (English)

Store this choice — all file headings, labels, and descriptions will be in this language. Templates in `templates/` are in English; translate headings and labels to the chosen language when filling them.

**1b. Profile:**

Ask the user which profile they want:

- **Basic** (7 files) — Suitable for small/medium projects. Includes the core files for project context, architecture, tech stack, active context, and progress tracking.
- **Extended** (7 core + optional extra files) — Suitable for enterprise/production projects. Includes the core files plus specialized files for business logic, data models, security, observability, and more.

If the user selects **Extended**, present the list of optional extended files and let them pick which ones they need:

| Extended File | Purpose |
|---------------|---------|
| `businessLogic.md` | Domain rules, business workflows, validation logic |
| `dataModel.md` | Database schema, entity relationships, data flow |
| `dependencies.md` | Detailed dependency map, version constraints, upgrade notes |
| `events.md` | Event-driven architecture, pub/sub topics, event schemas |
| `externalIntegrations.md` | 3rd party APIs, webhooks, service contracts |
| `featureToggles.md` | Feature flags, A/B tests, gradual rollout rules |
| `observability.md` | Logging, monitoring, tracing, alerting setup |
| `security.md` | Auth flows, security policies, vulnerability tracking |
| `technicalDebt.md` | Known debt items, refactoring priorities, cleanup plans |
| `contextCoverage.md` | Memory bank completeness tracking, coverage gaps |

The user can select all, some, or none. Store the selection for Steps 4 and 5.

### Step 2: Ask User Which Agent(s) They Use

**CRITICAL:** This skill can run inside any agent (Claude Code, Cursor, Windsurf, Cline, etc.). The agent running this skill is NOT necessarily the agent the user wants to configure. You MUST always ask the user which agent(s) they use for this project. NEVER assume the running agent is the target. NEVER skip this question. NEVER auto-create a rules file based on which agent you are.

**2a. Ask the user:**

Ask: "Which AI coding agent(s) do you use for this project?" and present these options:
- Claude Code → `CLAUDE.md` or `.claude/rules/*.md`
- Cursor → `.cursor/rules/*.mdc` (legacy: `.cursorrules`)
- Windsurf → `.windsurf/rules/*.md` (legacy: `.windsurfrules`)
- Cline → `.clinerules/` directory or `.clinerules` file
- GitHub Copilot → `.github/copilot-instructions.md`
- Roo Code → `.roo/rules/*.md` (legacy: `.roorules`)
- Aider → `CONVENTIONS.md` + `.aider.conf.yml`
- Antigravity → `.gemini/GEMINI.md`
- OpenAI Codex → `AGENTS.md`
- Other → ask for the rules file name/path

The user may select multiple agents. Store the selection for Step 3.

**2b. Scan for existing rules files:**

Read `reference.md` for the full agent-to-rules-file mapping table.

**IMPORTANT:** Rules files are NOT always in the project root. Search the ENTIRE project tree to find them. Use glob/find patterns to locate all known rules files regardless of their location.

Search for the rules files of the agent(s) the user selected:

| Agent | File Names to Search |
|-------|---------------------|
| Claude Code | `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/*.md` |
| Cursor | `.cursor/rules/*.mdc`, `.cursorrules` (legacy) |
| Windsurf | `.windsurf/rules/*.md`, `.windsurfrules` (legacy) |
| Cline | `.clinerules/` (directory), `.clinerules` (file) |
| GitHub Copilot | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md` |
| Roo Code | `.roo/rules/*.md`, `.roorules` (legacy) |
| Aider | `CONVENTIONS.md`, `.aider.conf.yml` |
| Antigravity | `.gemini/GEMINI.md` |
| OpenAI Codex | `AGENTS.md` |

Search strategy:
1. Use glob patterns like `**/.cursor/rules/*.mdc`, `**/.windsurf/rules/*.md`, `**/CLAUDE.md`, `**/.claude/rules/*.md`, `**/.clinerules`, `**/.github/copilot-instructions.md`, `**/.roo/rules/*.md`, `**/.aider.conf.yml`, `**/CONVENTIONS.md`, `**/AGENTS.md`, `**/.gemini/GEMINI.md`
2. Also search for legacy files: `**/.cursorrules`, `**/.windsurfrules`, `**/.roorules`
3. Exclude `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `vendor/` directories from search
4. For ambiguous names (like `CONVENTIONS.md`), verify by checking parent directory context

**2c. Report results and handle unrecognized agents:**

- If the rules file for the user's selected agent(s) already exists, report the path(s) and proceed to inject the protocol
- If the rules file does not exist, create it at the standard location for that agent
- If the user selected multiple agents, handle each one
- **If the user's agent is NOT in the supported list above**, or the agent cannot be matched to a known rules file format:
  1. Create `AGENTS.md` in the project root as a generic fallback
  2. Inject the Memory Bank protocol into `AGENTS.md`
  3. Display a clear warning to the user:
     ```
     ⚠️  Your agent ([agent name]) is not in our supported list.
     The Memory Bank protocol has been written to AGENTS.md in the project root.

     For Memory Bank to work correctly, you MUST manually add or copy
     the contents of AGENTS.md into your agent's own rules file.

     Please check your agent's documentation for the correct rules file
     location and format, then ensure the Memory Bank protocol is included.
     ```
  4. This ensures the protocol content is available even if automatic injection isn't possible

### Step 3: Inject Protocol into Rules Files

For each selected rules file:
1. Read the file
2. Check if it already contains "Memory Bank Protocol" — if yes, skip it
3. Read `templates/rules-protocol.md` for the protocol block
4. Prepend the protocol block to the top of the file (before existing content)
5. Show the user the change and get confirmation before writing

### Step 4: Create memory-bank/ Directory

Check if `memory-bank/` exists in the project root:
- If it exists, check which files are present and only create missing ones
- If it doesn't exist, create it

**Core files (always created — 7 total):**
1. `RULES.md`
2. `projectbrief.md`
3. `productContext.md`
4. `systemPatterns.md`
5. `techContext.md`
6. `activeContext.md`
7. `progress.md`

**Extended files (only if user selected Extended profile — based on their selection):**
8. `businessLogic.md`
9. `dataModel.md`
10. `dependencies.md`
11. `events.md`
12. `externalIntegrations.md`
13. `featureToggles.md`
14. `observability.md`
15. `security.md`
16. `technicalDebt.md`
17. `contextCoverage.md`

### Step 5: Fill Templates with Project Data

For each missing file:
1. Read the corresponding template from `templates/`
2. Scan the project for real data to fill the template:
   - `package.json` — project name, dependencies, scripts
   - `README.md` — project description, vision
   - `tsconfig.json` / `jsconfig.json` — import aliases, compiler options
   - Folder structure — architecture patterns
   - Git log (last 10-20 commits) — recent changes, active work
   - Existing rules files — conventions, preferences
3. Fill placeholders with discovered project data
4. Translate headings/labels to the user's chosen language
5. Show the filled content to the user
6. Get approval before writing each file

**Important:** `RULES.md` is created from `templates/RULES.md` and is **immutable** after creation — the skill must never modify it in subsequent runs.

### Step 6: .gitignore Check

Verify that `memory-bank/` is NOT listed in `.gitignore`. Memory bank files should be committed to git so all team members and agents can access them.

If `memory-bank/` is found in `.gitignore`, warn the user and offer to remove it.

### Step 7: Validation Checklist

Run the validation checklist and display results:

```
[✓/✗] Rules file found and Memory Bank protocol injected
[✓/✗] memory-bank/ directory exists

Core files:
[✓/✗] RULES.md exists
[✓/✗] projectbrief.md exists
[✓/✗] productContext.md exists
[✓/✗] systemPatterns.md exists
[✓/✗] techContext.md exists
[✓/✗] activeContext.md exists
[✓/✗] progress.md exists
```

If Extended profile was selected, also validate the selected extended files:
```
Extended files:
[✓/✗] businessLogic.md exists
[✓/✗] dataModel.md exists
[✓/✗] dependencies.md exists
... (only show files the user selected)
```

If all pass, show completion message:
```
Memory Bank setup complete!
Profile: [Basic/Extended]
Agent: [agent name]
Rules file: [file path]
Memory Bank: memory-bank/ ([N] files)

From now on, memory-bank/ files will be read at every session start.
Try: "memory bank status" or "memory bank read"
```

If any fail, explain the issue and offer to fix it.

---

## UPDATE Flow

### Step 1: Read Current Memory Bank

Read all 7 files from `memory-bank/` (skip `RULES.md` — it is immutable).

### Step 2: Scan Current Project State

Gather current project information:
- Git status, recent commits, current branch
- Package.json changes (new dependencies, scripts)
- Folder structure changes
- Any new/modified rules files

### Step 3: Detect Changes & Propose Updates

Compare current project state with memory bank contents. For each file that needs updates:
1. Show what changed (diff-style or summary)
2. Show proposed new content
3. Get user approval before writing

### Step 4: Write Approved Updates

Write only the approved changes. Add date stamps `[YYYY-MM-DD]` to entries.

### Step 5: Summary

Show a summary of what was updated and what was left unchanged.

---

## STATUS Flow

1. Read `memory-bank/activeContext.md`
2. Read `memory-bank/progress.md`
3. Present a concise summary:
   - Current focus / active work
   - Recent changes
   - What's completed
   - What's in progress
   - Known issues
   - Next steps

Respond in the same language as the existing memory bank files (auto-detect from headings).

---

## READ Flow

1. Read ALL files in `memory-bank/`
2. Present the full context in an organized format:
   - Start with project overview (from `projectbrief.md`)
   - Then product context (from `productContext.md`)
   - Then technical details (from `techContext.md` + `systemPatterns.md`)
   - Then current state (from `activeContext.md` + `progress.md`)
3. Highlight any areas that appear outdated or incomplete

Respond in the same language as the existing memory bank files (auto-detect from headings).

---

## Important Rules

- **NEVER** modify `memory-bank/RULES.md` after initial creation
- **NEVER** write secrets (API keys, tokens, passwords) to memory bank files
- **NEVER** skip user confirmation for file writes during setup
- Keep each file under 500 lines
- Use date stamps `[YYYY-MM-DD]` for temporal entries
- Don't duplicate information across files
- When updating, preserve existing content and append/modify — don't overwrite entire files unless the user approves

For detailed rules, agent mapping, and update triggers, see `reference.md`.
