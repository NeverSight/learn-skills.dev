---
name: onboard
description: Generates a concise project summary by reading all .context/ files. Use when starting a new session, onboarding a team member, or needing a quick project overview.
version: 1.0.0
---

# Onboard

Produces an instant project dashboard by reading all `.context/` files. Designed for fast orientation at the start of any AI session or for team onboarding.

## When to Use This Skill

- Starting a new development session
- Onboarding a new team member
- Getting a quick status check
- After a long break from the project

## Execution Flow

### Step 1: Read All Context Files
Read these files in order (fail gracefully if any are missing):
1. `.context/project.md` — product context
2. `.context/stack.md` — technology stack
3. `.context/architecture.md` — directory structure
4. `.context/conventions.md` — coding standards
5. `.agents/skills/skills.json` — installed skills

### Step 2: Scan Active Specs
Read file names in `.context/specs/` (exclude `.archive/` and `_template.md`):
- Count by status: `[ ]`, `[/]`, `[x]`, `[!]`
- Identify the highest-priority active spec

### Step 3: Generate Dashboard

Output format:

```
╔══════════════════════════════════════════════════════╗
║                 PROJECT DASHBOARD                    ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  📋 Project:  {name}                                 ║
║  📝 Phase:    {phase}                                ║
║  🎯 Summary:  {one-line description}                 ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  🔧 STACK                                            ║
║  ├── Language:   {language} {version}                ║
║  ├── Framework:  {framework} {version}               ║
║  ├── Database:   {db} {version}                      ║
║  └── Testing:    {test framework}                    ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  📐 ARCHITECTURE                                     ║
║  ├── {module_count} modules defined                  ║
║  └── Key modules: {top 3 modules}                    ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  📝 ACTIVE SPECS                                     ║
║  ├── In Progress: {count}                            ║
║  ├── Not Started: {count}                            ║
║  ├── Blocked:     {count}                            ║
║  └── Archived:    {count}                            ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  🧩 INSTALLED SKILLS ({count})                       ║
║  └── {comma-separated skill names}                   ║
║                                                      ║
╠══════════════════════════════════════════════════════╣
║  ⚠️  NOTICES                                         ║
║  {any warnings from context-sync validation}         ║
║  {any stale specs from spec-lifecycle}               ║
╚══════════════════════════════════════════════════════╝
```

### Step 4: Suggest Next Action

Based on the dashboard, suggest one of:
- **"Start work on..."** — if there are `[ ] Not Started` specs
- **"Continue work on..."** — if there are `[/] In Progress` specs
- **"Unblock..."** — if there are `[!] Blocked` specs
- **"Archive completed specs"** — if there are `[x] Completed` specs still in active directory
- **"Run context-sync validation"** — if context files may be stale

## Lightweight Mode

For quick status without the full dashboard:

```
📋 {PROJECT_NAME} ({phase}) | 🔧 {language}+{framework} | 📝 {active_spec_count} active specs | 🧩 {skill_count} skills
```

## Missing Context Handling

If a `.context/` file is missing, report it clearly:

```
⚠️ MISSING CONTEXT FILES:
- .context/stack.md — Technology stack not defined
- .context/architecture.md — No architecture documentation

Run: Create these files to improve AI assistance quality.
```

## Integration
- Runs `context-sync` validation as part of the notices section
- Reads `spec-lifecycle` status for the active specs section
- Non-destructive: this skill only reads, never writes
