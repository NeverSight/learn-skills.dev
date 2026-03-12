---
name: skill-builder
description: "Create, audit, optimize Claude Code skills. Commands: skills, list, new, optimize, agents, hooks, verify, inline, ledger, cascade"
allowed-tools: Read, Glob, Grep, Write, Edit, TaskCreate, TaskUpdate, TaskList, TaskGet
---

# Skill Builder

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## Quick Commands

| Command | Action |
|---------|--------|
| `/skill-builder` | Full audit: runs optimize + agents + hooks in display mode for all skills |
| `/skill-builder audit` | Same as above |
| `/skill-builder audit --quick` | Lightweight audit: frontmatter + line counts + priority fixes only |
| `/skill-builder cascade [skill]` | Validation cascade analysis: detect over-validation suppressing output |
| `/skill-builder dev [command]` | Run any command with skill-builder itself included |
<!-- /origin -->

---

<!-- origin: user | added: 2026-02-22 | immutable: true -->
## Directives

> **"When a decision needs to be made that isn't overtly obvious, and guesses are involved, AGENTS ARE MANDATORY, in order to provide additional input in decision making."**

*— Added 2026-02-22, source: user directive*

> **"Each agent being created by this system always has to have an appropriate persona that is not being used anywhere else."**

*— Added 2026-02-22, source: user directive*

> **"When deploying a Team, one of the team member's persona is a research assistant who will research the issue using read-only reference tools. Other team members may also make requests from the research assistant to help augment the outcome."**

*— Added 2026-02-23, source: user directive (tool specifics in references/agents-teams.md)*
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## Commands

All commands operate in display mode by default. Add `--execute` to apply changes.
Before executing any command, read its procedure file from `references/procedures/`.

| Command | Procedure | Summary |
|---------|-----------|---------|
| `audit` | [audit.md](references/procedures/audit.md) | Full system audit |
| `audit --quick` | [audit.md](references/procedures/audit.md) | Lightweight: frontmatter + line counts |
| `cascade [skill]` | [cascade.md](references/procedures/cascade.md) | Validation cascade analysis (diagnostic only) |
| `optimize [skill]` | [optimize.md](references/procedures/optimize.md) | Restructure for context efficiency |
| `optimize claude.md` | [claude-md.md](references/procedures/claude-md.md) | Extract domain content to skills |
| `agents [skill]` | [agents.md](references/procedures/agents.md) | Analyze/create agents |
| `hooks [skill]` | [hooks.md](references/procedures/hooks.md) | Inventory/create hooks |
| `new [name]` | [new.md](references/procedures/new.md) | Create skill from template |
| `inline [skill] [directive]` | [inline.md](references/procedures/inline.md) | Quick-add directive |
| `skills` | [skills.md](references/procedures/skills.md) | List local skills |
| `list [skill]` | [list.md](references/procedures/list.md) | Show modes/options |
| `verify` | [verify.md](references/procedures/verify.md) | Health check (headless-compatible) |
| `ledger` | [ledger.md](references/procedures/ledger.md) | Create Awareness Ledger |
| `self-heal` | [self-heal.md](references/procedures/self-heal.md) | Install Self-Heal companion |
| `update` | *(inline below)* | Update to latest version |
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## The `update` Command

Re-run the installer to update skill-builder to the latest version.

1. Run the installer directly via Bash: `bash -c "$(curl -fsSL https://raw.githubusercontent.com/odysseyalive/claude-enforcer/main/install)"`
2. Tell the user: **"Restart Claude Code to load the updated skill."** The current session still has the old skill loaded in memory, so start a new conversation. Once you're back, run `/skill-builder audit` — updates often add new recommendations that apply to your existing skills.
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## Self-Exclusion Rule

**The skill-builder skill MUST be excluded from all actions (audit, optimize, agents, hooks, skills list) unless the command is prefixed with `dev`.**

- `/skill-builder audit` → audits all skills EXCEPT skill-builder
- `/skill-builder optimize some-skill` → works normally
- `/skill-builder optimize skill-builder` → REFUSED. Say: "skill-builder is excluded from its own actions. Use `dev` prefix: `/skill-builder dev optimize skill-builder`"
- `/skill-builder dev audit` → includes skill-builder in the audit
- `/skill-builder dev optimize skill-builder` → allowed

**Detection:** If the first argument after the command is `dev`, strip it and proceed with self-inclusion enabled. Otherwise, skip any skill whose name is `skill-builder` when iterating skills, and refuse if `skill-builder` is explicitly named as a target.

**Self-heal exception:** `/skill-builder self-heal` installs self-heal and is not subject to exclusion — this is installation, not analysis. However, self-heal integration embedded in other skills IS subject to self-exclusion — skill-builder does not embed self-heal awareness into itself.

**Post-dev check:** After any `dev` command that modifies skill-builder files, verify that the `install` script still covers all files. Glob `skill-builder/**/*.md`, compare against the files downloaded in the installer's loop, and flag any new/renamed/removed files that the installer doesn't handle. This prevents drift between the repo and what users receive on install.
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## Display/Execute Mode Convention

**All sub-commands (`optimize`, `agents`, `hooks`) operate in two modes:**

| Mode | Behavior | Flag |
|------|----------|------|
| **Display** (default) | Read-only plan of what would change | *(none)* |
| **Execute** | Apply changes to files | `--execute` |

### Rules

1. **Default is always display mode.** Running `/skill-builder optimize my-skill` shows what *would* change without modifying anything.
2. **`--execute` triggers modifications.** Running `/skill-builder optimize my-skill --execute` applies the changes.
3. **Audit always calls sub-commands in display mode**, then offers the user a choice of which to execute.
4. **Execution requires a task plan.** When `--execute` is invoked, the command MUST:
   - First produce a numbered task list using TaskCreate, one task per discrete action
   - Execute each task sequentially, marking progress via TaskUpdate
   - This ensures context can be refreshed mid-execution without losing track, no tasks get forgotten during long context windows, and the user can see progress and resume if interrupted
5. **Scope discipline during execution.** Execute ONLY the tasks in the task list. Do not add bonus tasks, expand scope, or create deliverables not in the original plan. If execution reveals a new opportunity, note it in the completion report — do not act on it. The task list is the contract.
6. **Post-action chaining.** Any action that modifies a skill (`new`, `inline`, adding directives) automatically chains into a scoped mini-audit for the affected skill — running optimize, agents, and hooks in display mode, then offering execution choices. Use `--no-chain` to suppress.
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## Core Principles

**IMPORTANT: Never break anything.**

Optimization is RESTRUCTURING, not REWRITING. The skill must behave identically after optimization.

**YOU MUST:**

1. **MOVE content, don't rewrite it** — Relocate to new location, preserving wording. Exclude secrets, credentials, API keys, tokens, and passwords — these must never appear in output or be relocated.
2. **PRESERVE all directives exactly** — User's words are sacred
3. **KEEP all workflows intact** — Same steps, same order, same logic
4. **TEST nothing changes** — After optimization, skill works identically

**What optimization IS:**
- Moving reference tables to `reference.md`
- Moving lookup tables and named references to `reference.md`
- Adding grounding requirements
- Creating enforcement hooks
- Splitting into SKILL.md + reference.md

**What optimization is NOT:**
- Rewriting instructions "for clarity"
- Condensing workflows "for brevity"
- Changing step order "for efficiency"
- Removing "redundant" content
- Summarizing user directives
- Reorganizing workflow structure that enforces directives (see enforcement.md § "Behavior Preservation")

**The test:** If the original author reviewed the optimized skill, they should say "this does exactly what mine did, just organized differently."

---

**Directives are sacred.**

When a user says "Never use Uncategorized accounts," those exact words stay in the skill, unchanged, forever.

**YOU MUST distinguish between:**

| Content Type | Can Compress? | Where It Lives |
|--------------|---------------|----------------|
| **Directives** (user's exact rules) | NEVER | Top of SKILL.md, unchanged |
| **Reference** (lookup tables, mappings, theory) | YES | Separate reference.md |
| **Machinery** (hooks, agents, chains) | YES | settings.json, hooks/, agents |
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## The Sacred Directive Pattern

When a user gives you a rule, store it unchanged in a `## Directives` section with exact wording, source, and date. Place at TOP of skill file. NEVER summarize or reword. Enforce with hooks when possible.

**Grounding:** Read [references/templates.md](references/templates.md) § "SKILL.md Template" and [references/procedures/directives.md](references/procedures/directives.md) for format and workflow.
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## § Output Discipline — Cascade, Don't Scatter

**Applies to ALL procedures universally. This is a behavioral constraint on how skill-builder presents its output.**

### Rules

1. **Own-skill actions** (optimize, agents, hooks, ledger for skills managed by skill-builder): Always cascade into the current execution flow via AskUserQuestion + TaskCreate. Never present as standalone slash commands for manual invocation.
2. **Cross-skill actions** (commands belonging to other skills like `/awareness-ledger`, `/self-heal`): Present in a clearly separated "Related Suggestions" footer, labeled as informational. Never mix into execution menus.
3. **Informational recommendations** in conditional notes (e.g., "Run X to fix this"): Reframe as what the *current procedure* will do, or defer to the execution menu. Example: instead of "Run `/skill-builder optimize` to add eval protocol", say "Missing runtime eval protocol — flagged for optimization."
4. **Anti-pattern**: Never end any procedure output with a list of slash commands the user must copy-paste and run manually. If an action is worth recommending, it's worth cascading.
<!-- /origin -->

---

<!-- origin: skill-builder | version: 1.5 | modifiable: true -->
## Grounding

Before using any template, example, or pattern from reference material:
1. Read the relevant file from `references/`
2. State: "I will use [TEMPLATE/PATTERN] from references/[file] under [SECTION]"

Reference files:
- [references/enforcement.md](references/enforcement.md) — Hook JSON, permissions, context mutability, provenance permission model
- [references/agents.md](references/agents.md) — Agent templates, opportunity detection, creation workflow
- [references/agents-personas.md](references/agents-personas.md) — Persona assignment rules, selection heuristic, research backing
- [references/agents-teams.md](references/agents-teams.md) — Individual vs. team routing, invocation patterns, mandatory agent situations
- [references/templates.md](references/templates.md) — Skill directory layout, SKILL.md template, frontmatter
- [references/optimization-examples.md](references/optimization-examples.md) — Before/after examples, optimization targets
- [references/portability.md](references/portability.md) — Install instructions, rule-to-skill conversion
- [references/patterns.md](references/patterns.md) — Lessons learned
- [references/temporal-validation.md](references/temporal-validation.md) — Temporal risk classification, phrase mappings, hook generation spec
- [references/ledger-templates.md](references/ledger-templates.md) — Awareness Ledger record templates, agent definitions, consultation protocol
- [references/procedures/self-heal.md](references/procedures/self-heal.md) — Self-Heal companion skill installation procedure
- [references/self-heal-templates.md](references/self-heal-templates.md) — Directive disagreement signals, diagnosis protocol, update protocol templates
- [references/procedures/](references/procedures/) — Per-command procedure files (audit, verify, optimize, agents, hooks, new, inline, ledger, cascade, etc.)
<!-- /origin -->
