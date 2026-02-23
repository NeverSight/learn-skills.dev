---
name: scrum
description: |
  Scrum framework for AI agent self-management. Brings Scrum practices into
  any project to drive development and continuous improvement.
  Ceremonies chain automatically. Tool-agnostic: works with any issue tracker,
  VCS, or just local markdown files.
  Triggers: "scrum", "sprint", "retrospective", "backlog", "レトロ", "計画", "振り返り"
metadata:
  short-description: Scrum framework for AI agents
  argument-hint: "[install|uninstall|update|plan|daily|review|retro|refine|status]"
  version: 1.3.2
---

# Scrum Skill

Scrum is the MEANS, not the GOAL. The goal is delivering value to users.

Arguments: $ARGUMENTS

## Version Check (on every invocation)

Before routing arguments, check for version mismatch:

1. If `docs/scrum/` exists (not first-time setup):
   - Read `metadata.version` from this SKILL.md (currently: `1.3.2`)
   - Read `docs/scrum/.scrum-version` (if exists)
   - If versions differ or `.scrum-version` is missing: display "スキル v{new} が利用可能です（現在 v{old}）。`/scrum update` で更新してください。" (If `.scrum-version` is missing, treat as `unknown`.)
   - Continue with the requested action regardless (version check is informational only)
2. If `docs/scrum/` does not exist: proceed to setup (no version check needed)

---

## Argument Routing

| Argument | Action |
|----------|--------|
| `install` | Install this skill globally (symlink to ~/.claude/skills/) |
| `uninstall` | Remove global symlink + optionally clean project Scrum files |
| (empty, first time) | Setup: introduce Scrum to this project |
| (empty, already set up) | Show status + suggest next action |
| `plan` | Sprint Planning → `references/ceremonies/sprint-planning.md` |
| `daily` | Daily Scrum → `references/ceremonies/daily-scrum.md` |
| `review` | Sprint Review → `references/ceremonies/sprint-review.md` |
| `retro` | Retrospective → `references/ceremonies/sprint-retrospective.md` |
| `refine` | Backlog Refinement → `references/ceremonies/backlog-refinement.md` |
| `update` | Update project Scrum files to match latest skill version |
| `status` | Show current sprint status |

**Detect first time**: Check if `docs/scrum/` directory exists in project root.

---

## Install / Uninstall

### `/scrum install`

Install this skill globally so `/scrum` works in any project:

1. **Detect skill location**: Find the directory containing this SKILL.md
2. **Check existing installation**: If `~/.claude/skills/scrum` already exists, report "Already installed" and show the current link target
3. **Create symlink**: `ln -s {SKILL_DIR} ~/.claude/skills/scrum`
4. **Verify**: Confirm the link was created successfully

**Example:**
```bash
ln -s /path/to/scrum_agents/skills/scrum ~/.claude/skills/scrum
```

If the link target differs from the current skill directory, ask whether to update it.

### `/scrum uninstall`

Remove the global skill symlink and optionally clean project files:

1. **Remove symlink**: `rm ~/.claude/skills/scrum`
2. **Ask about project files**: "プロジェクトのScrumファイルも削除しますか？"
   - If yes, remove:
     - `docs/scrum/` directory
     - `.claude/agents/scrum-*.md`
     - `.claude/rules/scrum-*.md`
     - Scrum section in CLAUDE.md
   - If no, keep project files (they still work as documentation)
3. **Report**: Show what was removed

---

## Tool Agnosticism

**This skill defines Scrum process, NOT specific tools.**

Scrum requires certain capabilities (backlog management, work tracking, increment review).
HOW those capabilities are fulfilled depends on the project's environment.

### Scrum Capabilities → Environment Mapping

| Scrum Capability | What is Needed | Examples |
|-----------------|----------------|----------|
| Product Backlog | A place to list and prioritize work items | Issue tracker, `docs/scrum/backlog.md` |
| Sprint Backlog | A way to mark items as "in this sprint" | Labels/tags, sprint board, `docs/scrum/sprints/current.md` |
| Sprint Work | A way to develop and track changes | Branches + PRs/MRs, local commits |
| Increment Review | A way to present work to stakeholder | PR/MR review, demo, deploy preview |
| Feedback | A way for stakeholder to respond asynchronously | Comments on PR/MR/Issue, `docs/scrum/` notes |
| Sprint Archive | A persistent record of each sprint | `docs/scrum/sprints/YYYY-MM-DD_sprint-NNN/` (always) |

### Environment Detection (at setup)

During setup, detect what's available:

1. **VCS**: git? Other?
2. **Remote platform**: Check for existing skills, MCPs, or CLIs (e.g., `gh`, `glab`, `bb`)
3. **Issue tracker**: Integrated with platform? Separate (Jira, Redmine)?
4. **User preference**: Ask stakeholder if they have a preferred workflow

### Adaptation Rules

- **Always**: Use `docs/scrum/` for local Scrum records (sprint archives, logs, DoD). This is the source of truth for the Scrum process itself.
- **If external tools are available**: Use them for backlog management, work tracking, and async communication. Map Scrum concepts to the platform's native features.
- **If no external tools**: Use `docs/scrum/backlog.md` and `docs/scrum/sprints/current.md` as the full workflow. Everything works.
- **If stakeholder specifies tools**: Adapt to their environment. Ask for guidance on how to use unfamiliar tools, or recommend they install appropriate skills/MCPs.

### Recommending Tools (not requiring them)

During setup, if no external tool is detected, suggest (not require):

"バックログ管理や非同期フィードバックのために、プロジェクト管理ツールの導入を検討できます。
例: GitHub Issues, GitLab Issues, Jira, Redmine など。
対応するスキルや MCP があれば導入をお勧めします。
なくても、マークダウンファイルで全て運用できます。"

---

## Session Continuity (CRITICAL)

AI agents lose context between sessions. This section ensures Scrum state survives session boundaries.

### Session Start Protocol

On every session start (or `/scrum` invocation after setup), agents MUST:

1. Read `docs/scrum/sprints/current.md` -- current sprint state, goal, item statuses
2. Read the **Sprint Summary** section in `current.md` for quick context
3. Read `docs/scrum/backlog.md` -- remaining work and priorities
4. Read `docs/scrum/definition-of-done.md` -- quality criteria

This gives the agent enough context to continue where the previous session left off.

### Sprint Summary Maintenance

The Developer MUST update the **Sprint Summary** section in `current.md` whenever:
- An item's status changes
- A significant decision is made
- A blocker is encountered or resolved
- The session is about to end (if known)

Sprint Summary format:
```markdown
### Sprint Summary (for session continuity)
**What**: {1-2 sentence summary}
**Progress**: {X/Y items done}
**Key decisions**: {recent important decisions, max 3}
**Next action**: {what should happen next if session resumes}
```

### CLAUDE.md Integration

The `## Scrum` section in CLAUDE.md (written by `/scrum` setup or `/scrum update`) ensures that even without explicit `/scrum` invocation, new sessions are aware of:
- Artifact locations
- Flow rules
- Anti-patterns

This section is loaded automatically on every session start.

---

## Automatic Ceremony Flow

Ceremonies chain automatically. The user does NOT invoke each one.
**Agents MUST NOT stop between ceremonies to ask for permission or confirmation.**

```
User expresses desire
  → PO: create backlog item automatically
  → Sprint Planning: auto-start if no active sprint
  → Dev: implement (branch + changes)
  → Increment ready → Sprint Review (present to stakeholder)
  → Stakeholder feedback → Retrospective auto-runs
  → SM improves org → Next sprint auto-starts (if backlog has items)
```

### Flow Rules

1. **Never stop between ceremonies.** Review → Retro → Next Planning is one continuous flow.
2. **Stakeholder feedback is async.** Present the increment, ask for feedback, but proceed to Retro immediately. Feedback received later is incorporated in the next Backlog Refinement.
3. **Backlog operations need no approval.** The Scrum Team autonomously manages the backlog. Update it, reorder it, add items -- no "is this OK?" needed.
4. **When backlog has items, start the next sprint.** After Retro completes and backlog is not empty, Sprint Planning begins immediately.
5. **When backlog is empty, self-generate work.** Verify Product Goal achievement, propose technical improvements, or discover new backlog items. Never say "what should I do next?"

The user only needs to:
- Express desires
- Review increments and give feedback (async -- does not block the flow)

---

## Anti-Patterns (NEVER DO)

These patterns caused sessions to stall. They are explicitly forbidden:

| Anti-Pattern | Why It's Wrong | Do This Instead |
|---|---|---|
| "続けますか？" between ceremonies | Breaks automatic flow | Proceed to next ceremony immediately |
| "バックログを更新してよいですか？" | Backlog is self-managed | Update it and report what changed |
| "次に何をしますか？" after completing work | Agent is self-managing | Check backlog, start next sprint, or self-generate work |
| "マージしてよいですか？" | Blocks delivery | Execute the merge (or use the project's delivery flow) |
| Waiting for user response before Retro | Review→Retro is automatic | Present increment, then start Retro immediately |
| "期待通りですか？" and then stopping | Feedback is async | Ask, but proceed to Retro without waiting |
| Declaring intent without executing | "やる" is not doing. Saying "I'll verify" is not verifying. | Execute the action in the same turn. No separate "announcement" step. |
| Skipping delivery verification | Checking file diffs is not testing. grep is not running the skill. | Merge → update installed files → reload → run the skill → confirm it works. |
| Working without an active Sprint | All work happens inside a Sprint. No exceptions for "urgent" fixes. | Start Sprint Planning first, then work. Even a 1-item sprint is a sprint. |

**Rule: If you catch yourself about to ask permission to continue Scrum flow, STOP and just do it.**
**Rule: If you catch yourself announcing what you'll do next, STOP and do it in this turn instead.**
**Rule: If there is no active Sprint and you are about to write code or make changes, STOP and start Sprint Planning first.**

---

## File Structure

Local Scrum records (always created, regardless of tools):

```
docs/scrum/
  .scrum-version                          # Installed skill version (e.g., "1.0.0")
  definition-of-done.md                   # DoD (evolves through retros)
  sprints/
    current.md                            # Current sprint state
    YYYY-MM-DD_sprint-NNN/                # Sprint archive
      plan.md                             # Sprint Goal + items
      log.md                              # Progress log
      review.md                           # Review record
      retrospective.md                    # Retro record
  logs/
    failures.md                           # Failure log
    decisions.md                          # Design decisions
    adaptations.md                        # Real-time adaptations
    role-interactions.md                  # Cross-role handoff log
```

If external issue tracker is available, `docs/scrum/backlog.md` is optional.
The external tracker IS the backlog. Local records track the Scrum process itself.

---

## Setup (First-Time `/scrum`)

When `docs/scrum/` does NOT exist:

### Step 1: Detect Environment

- Tech stack (`pyproject.toml`, `package.json`, `Cargo.toml`, etc.)
- VCS and remote platform (what tools/skills/MCPs are available?)
- Existing CLAUDE.md and `docs/`
- Ask stakeholder about preferred tools if unclear

### Step 2: Create Local Structure

Read reference files from `references/` and **adapt** them to the project:

**Scrum records** (`docs/scrum/`):
- `definition-of-done.md` ← adapt the `{Adapt to project}` placeholder in the Testing section based on Step 1 detection results:
  - **Python** (`pyproject.toml` + pytest): `"pytest passes"`, and if ruff detected: `"ruff check passes"`
  - **Node.js** (`package.json` + jest/vitest): `"npm test passes"`, and if eslint detected: `"eslint passes"`
  - **Rust** (`Cargo.toml`): `"cargo test passes"`, and if clippy detected: `"cargo clippy passes"`
  - **No test framework detected**: `"Manual verification documented in review.md"`
  - Replace the entire `{Adapt to project ...}` block with the concrete check items. Do not leave the placeholder.
- `sprints/current.md` ← empty sprint template
- `logs/failures.md` ← empty with header
- `logs/decisions.md` ← empty with header
- `logs/adaptations.md` ← empty with header
- `logs/role-interactions.md` ← cross-role handoff log (from `references/templates/role-interactions.md`)

If no external issue tracker: also create `backlog.md` from template.

**Agents** (`.claude/agents/`) -- adapt, don't just copy:
- `scrum-product-owner.md` ← adapt artifact locations to the environment
- `scrum-master.md`
- `scrum-developer.md`

Agent definitions contain artifact references (backlog location, etc.).
When the environment uses external tools, update these references so agents
know where to find and manage artifacts.

**Rules** (`.claude/rules/`):
- `scrum-principles.md`
- `scrum-values.md`
- `scrum-role-separation.md`

### Step 3: Configure Environment Mapping

Record detected tools and how Scrum concepts map to them in `docs/scrum/sprints/current.md`
or CLAUDE.md. Example:

```
## Scrum Environment
- Backlog: GitHub Issues (via `gh` CLI)
- Sprint tracking: GitHub labels
- Code review: Pull Requests
```

Or:

```
## Scrum Environment
- Backlog: docs/scrum/backlog.md
- Sprint tracking: docs/scrum/sprints/current.md
- Code review: Direct stakeholder review
```

### Step 4: Record Skill Version

Write the current skill version to `docs/scrum/.scrum-version`:
```
1.0.0
```
This file is a single line containing only the version number. It is used by the Version Check to detect when the skill has been updated.

### Step 5: Update CLAUDE.md

Append `## Scrum (v{version})` section to CLAUDE.md. This section MUST include:
- Artifact locations (backlog, sprint, DoD, logs)
- Ceremony Auto-Flow diagram
- Flow Rules (all 5)
- Anti-Patterns table (all entries)

**This is critical.** Without this section in CLAUDE.md, new sessions won't load
Scrum rules automatically. The `/scrum` skill is only invoked on demand -- CLAUDE.md
is loaded on every session start.

### Step 6: Ask for Product Goal

"Scrum を導入しました。このプロジェクトで何を実現したいですか？"

### Step 7: Auto-flow

PO agent → create backlog → Sprint Planning → Dev starts.

---

## Status (`/scrum status`)

1. Read `docs/scrum/sprints/current.md` for sprint state
2. If external tracker available: query backlog and sprint items
3. Count sprint archives in `docs/scrum/sprints/`
4. Display in Japanese using this format:

**Output format:**

```
## {Project Name} Scrum Status

**Current Sprint**: Sprint {N} -- {Goal}
**Progress**: {completed}/{total} items done

| Item | Status | What It Delivers |
|------|--------|------------------|
| {name} | {status} | {user-facing value} |

**Backlog**: {N} items remaining
**Completed Sprints**: {N} (Sprint 1-{N} archived)

{If no active sprint: "No active sprint. Ready for next Sprint Planning."}
```

Focus on what the stakeholder cares about: what's being worked on, what they'll get, and what's next.

---

## Update (`/scrum update`)

Update project Scrum files to match the latest skill version.

### When (Auto-detect)

On every `/scrum` invocation (any argument), the Version Check (above) compares versions:
1. Read skill version from this SKILL.md's `metadata.version`
2. Read project version from `docs/scrum/.scrum-version`
3. If versions differ: show message "スキルバージョンが更新されています (v{old} -> v{new})。`/scrum update` で更新できます。"

The update is NOT automatic -- the user must explicitly run `/scrum update`.

### Process

1. **Read versions**: Compare `metadata.version` with `docs/scrum/.scrum-version`
2. **Identify changes**: List files that differ between templates and project
3. **Update managed files**: For each Scrum-managed file:
   - Read the current project file
   - Read the latest template from `references/`
   - Merge: keep project-specific content, update template-managed sections
   - Files to check:
     - `.claude/agents/scrum-*.md` <-- `references/agents/`
     - `.claude/rules/scrum-*.md` <-- `references/rules/`
     - `docs/scrum/definition-of-done.md` <-- `references/templates/definition-of-done.md`
4. **Update CLAUDE.md**: Append or update the `## Scrum` section in the project's CLAUDE.md.
   This section MUST include: artifact locations, Flow Rules, and Anti-Patterns.
   Without this, new sessions won't know about Scrum rules unless `/scrum` is explicitly invoked.
   - If `## Scrum` section exists: replace it with the latest version
   - If `## Scrum` section does not exist: append it at the end
   - Never touch non-Scrum content in CLAUDE.md
5. **Update version**: Write new version to `docs/scrum/.scrum-version`
6. **Report**: Show what was updated in Japanese

### Customization Preservation

**Principle:** Never overwrite project-specific adaptations.

Strategy:
- **Agent definitions**: Update template sections (Role Boundary, Artifacts, Record Format). Preserve project-added sections (custom workflows, project-specific notes). When in doubt, show a diff to the user rather than overwriting.
- **Rules**: Replace entirely (rules are skill-defined, not project-customized). **Important**: If a project's SM or Dev adds valuable content to rules files (e.g., Scrum Guide sections, enforcement details), those improvements MUST be upstreamed into the template files in `references/rules/` BEFORE the next version bump. Otherwise, `/scrum update` will delete them. The SM should check for rule-file diffs during Retrospective and upstream any valuable additions.
- **DoD**: Update Scrum section only. Preserve Quality, Testing, Transparency sections (these are project-adapted by the team).
- **CLAUDE.md**: Append/update Scrum section only. Never touch non-Scrum content.

### Merge Strategy Details

For agent definitions and DoD, use this merge approach:

1. **Identify template-managed sections**: Sections that originate from the skill templates (e.g., "Role Boundary", "Artifacts" in agent definitions; "Scrum" section in DoD).
2. **Identify project-specific sections**: Any sections or content added by the project team that are NOT in the template.
3. **Merge**:
   - Replace template-managed sections with the latest template content
   - Keep project-specific sections intact at their current location
   - If a section exists in both template and project with different content, prefer the template version for template-managed sections
4. **Report changes**: List each file and what was updated vs. preserved

### Version File

`docs/scrum/.scrum-version` format:
```
1.0.0
```
Single line, just the version number. Created during `/scrum` setup (Step 4), updated by `/scrum update`.

---

## Sprint Archival

**Executor: SM agent** -- after Retrospective Step 4 completes.

1. **Determine sprint number**: Count existing `sprint-NNN` directories in `docs/scrum/sprints/`, add 1, zero-pad to 3 digits
2. Create `docs/scrum/sprints/YYYY-MM-DD_sprint-NNN/` (date = retrospective execution date)
3. Save: `plan.md`, `log.md`, `review.md`, `retrospective.md` (extracted from `current.md` and retrospective output)
4. Reset `docs/scrum/sprints/current.md` to: `No active sprint. Backlog has items -- ready for Sprint Planning.`
5. If external tracker: update item statuses (close completed items, etc.)
6. Commit the archive

---

## Logging

All events logged with timestamps in `docs/scrum/logs/`:

| Log | Content | Format |
|-----|---------|--------|
| `failures.md` | Things that went wrong | `## YYYY-MM-DD HH:MM - {title}` |
| `decisions.md` | Design/tech decisions | `## YYYY-MM-DD - {decision}` with Context/Decision/Rationale |
| `adaptations.md` | Mid-sprint adaptations | `## YYYY-MM-DD HH:MM - {change}` with Trigger/Change |
| `role-interactions.md` | Cross-role handoffs and reviews | `## YYYY-MM-DD HH:MM - {From} -> {To}: {Summary}` |
