---
name: skill-craft
description: Create and edit agent skills with enforced conventions. Use when creating a new skill, modifying an existing skill, or harmonizing skill structure. Also use when the user mentions "skill conventions", "clean up skills", "standardize skills", or wants to ensure skills follow best practices for token efficiency and triggering accuracy.
argument-hint: "[skill-name or 'new']"
---

# Skill Craft

Create, edit, and harmonize agent skills.

## When to Use

- Creating a new skill from scratch
- Modifying an existing skill's SKILL.md or phases
- Adding/removing phases to a skill
- User asks to "harmonize", "clean up", or "standardize" skills

## Why This Exists

Without conventions, skills drift: inconsistent frontmatter breaks skill discovery, monolithic files waste tokens on every load, and missing sections (like Gotchas) mean the agent repeats the same mistakes. This skill encodes the patterns that prevent skill rot.

## Gotchas

- **Description is discovery**: The agent uses the `description` field to decide whether to load a skill. A vague description means the skill never triggers. Always follow the description formula.
- **Undertriggering is the default**: Agents tend to NOT trigger skills when they should. Descriptions should be slightly "pushy" — explicitly list contexts and adjacent phrases that should activate the skill, even if they seem obvious.
- **Loaded ≠ used**: SKILL.md is loaded into context every time the skill triggers. Every token in it competes with conversation history. A 500-line SKILL.md burns context even for simple tasks.
- **Phases are free until loaded**: Phase files only consume tokens when a `> Load:` directive is followed. Put detailed instructions in phases, not in SKILL.md.
- **Family rules deduplication**: When a skill belongs to a family, rules in both the skill AND the family rules get loaded. Duplicated rules waste tokens twice.
- **`Critical Rules` is an anti-pattern**: Agents tend to over-weight Critical Rules sections and under-weight everything else. Pre-flight checklists distribute enforcement to the right moment.
- **Conditional steps get skipped**: Steps phrased as "mandatory if X" or split into many sub-steps (5a, 5b, 5c) are treated as optional by agents. If a step must happen, use a `(CHECKPOINT)` marker and an imperative "Do NOT skip" instruction — not conditional language.
- **Skill vs agent config**: Skills are for task-specific workflows loaded on-demand. The agent's config file (e.g., `CLAUDE.md`, `.cursorrules`) is for always-on project rules. If the knowledge applies to every conversation (coding standards, naming conventions), put it in the config file. If it's a complex workflow activated contextually, make it a skill.

## Core Principles

### Token Efficiency

Every token in a skill competes with conversation history. Assume the agent is competent — before writing any instruction, ask: "Would the agent do this badly without it?" If no, skip it. Only document what it doesn't inherently know: project-specific conventions, domain knowledge, non-obvious workflows, gotchas.

❌ Don't: "Use git to commit your changes" (the agent knows git)
✅ Do: "Commit with `feat(scope):` format, scope = feature name not issue number"

### Progressive Disclosure

SKILL.md is a hub, not a monolith. Put detailed instructions in phase files or reference files that the agent loads on-demand. One level deep maximum — never chain reference → sub-reference → sub-sub-reference.

**Sizing guidelines:**

- Frontmatter description: ~100 words max (always in context)
- SKILL.md body: <500 lines (loaded when skill triggers)
- Reference files >300 lines: add a table of contents

### Single Category

Every skill should fit cleanly into one category. Skills that straddle multiple categories become hard to maintain and confusing to trigger. If a skill does two things, split it into two skills.

### Degrees of Freedom

Match instruction specificity to task fragility:

| Freedom | When | Example |
|---|---|---|
| **High** | Multiple valid approaches | Code review guidelines |
| **Medium** | Preferred pattern, some variation OK | Report templates |
| **Low** | Fragile, error-prone, consistency critical | DB migration commands |

High freedom = state the goal. Low freedom = specify exact steps. Most skills mix both — reserve low freedom for the parts that break silently.

## Conventions

### 1. Directory Layout

```
{skill-name}/
├── SKILL.md              # Always required — the hub
├── phases/               # For multi-step workflows (3+ steps)
│   ├── 01-{name}.md
│   ├── 02-{name}.md
│   └── ...
├── references/           # Deep knowledge, loaded on-demand
├── scripts/              # Executable code (shell, Python)
└── templates/            # Content generation templates
```

- Phase files: zero-padded, kebab-case (`01-context-gathering.md`)
- Single-file skills (no phases) are valid for simple commands or background knowledge
- Never nest skills inside other skills
- Scripts: distinguish "execute" vs "read as reference" in SKILL.md (`Run scripts/validate.py` vs `See scripts/validate.py for the algorithm`)

### 2. Language

All skill files MUST be in English. Only content examples (e.g., sample posts, article excerpts) may be in the target language.

### 3. Frontmatter (mandatory)

Every SKILL.md MUST have YAML frontmatter with at least `name` and `description`.

```yaml
---
name: skill-name # kebab-case, matches directory name
description: "[What it does]. Use when [trigger conditions]."
---
```

**Naming strategy:** Prefer action-oriented names that describe what the skill does.

❌ Don't: `helper`, `utils`, `tools`, `data` (vague, never triggers)
✅ Do: `processing-pdfs`, `reviewing-code`, `deploying-api` (specific action)

**Description formula:** Third-person, action-focused. State what the skill does, then when to invoke it. The description is how the agent decides whether to load this skill — it uses LLM reasoning, not keyword matching. Err on the side of "pushy": include adjacent phrases and contexts that should trigger the skill.

❌ Don't: "Helper for reviews"
✅ Do: "Run a 5-phase security audit on changed files. Use when the user asks to review code for vulnerabilities, before merging a PR, or when security-related files are modified."

**Optional fields:**

| Field                      | When to use                             | Example                   |
| -------------------------- | --------------------------------------- | ------------------------- |
| `argument-hint`            | Skill takes arguments                   | `"[issue-number]"`        |
| `disable-model-invocation` | Manual only (side effects, destructive) | `true`                    |
| `user-invocable`           | Background knowledge, not a command     | `false`                   |
| `allowed-tools`            | Pre-approve tools the workflow runs     | `Bash(gh issue view:*), Read, Grep` |

**Decision guide:**

- User runs it directly → leave defaults (user-invocable: true)
- Loaded by other skills only → `user-invocable: false`
- Has side effects (push, publish, delete) → `disable-model-invocation: true`
- Pure knowledge (voice profile, rules) → `user-invocable: false`

**`allowed-tools` pre-approves, it does not restrict.** A listed pattern can run without a new permission prompt while the skill is active; the user's matching `ask` and `deny` rules still apply, and unlisted tools follow the current permission settings. Never list a blanket network or VCS pattern (`Bash(curl:*)`, `Bash(git:*)`, `Bash(gh:*)`): they let through uploads to any host, force pushes or `gh auth token` while the agent reads untrusted content (API responses, issue bodies). A command-group prefix is blanket too: `Bash(gh issue:*)` also approves `gh issue delete` and `gh issue transfer`. List the exact read subcommands the workflow runs (`Bash(gh issue view:*)`, `Bash(gh label list:*)`) and let writes prompt.

### 4. Recommended Sections

Every SKILL.md should contain:

| Section | Required? | Purpose |
|---|---|---|
| `## When to Use` | Yes | Trigger conditions — when the agent should load this skill |
| `## Why This Exists` | Recommended | Motivation — helps the agent understand when NOT to use it |
| `## Gotchas` | Recommended | Non-obvious pitfalls, edge cases, things that break silently |
| `## Phase N: Name` | If multi-step | Overview + load directive for each phase |

The "Gotchas" section is high-value: it documents what the agent would get wrong without the skill. This is the core of token efficiency — skip what the agent knows, focus on what it doesn't.

### 5. Example Formatting

Do/don't examples MUST use this format:

```
❌ Don't: "example of what not to do"
✅ Do: "example of what to do"
```

### 6. Load Directives

Reference phases or other skills with `> Load:` syntax:

```markdown
> Load: [Phase Name](phases/01-phase-name.md)
> Load: [Shared Rules](../other-skill/SKILL.md)
```

- Always use relative paths from the SKILL.md location
- Load directives must be on their own line

### 7. Skill Families

Related skills sharing a common prefix (e.g., `blog-*`, `email-*`) should share a `{prefix}-rules` skill (`user-invocable: false`) for common config. Never duplicate rules between a skill and its family rules — both get loaded into context.

### 8. Behavior Rules

- **User input**: Never print questions as plain text — use an interactive tool that blocks execution until the user responds (Claude Code: `AskUserQuestion`)
- **Checkpoints**: Any step where the agent MUST wait for user input before proceeding should be marked with `(CHECKPOINT)` in the step title and include an explicit "Do NOT skip this step. Do NOT proceed to the next phase without completing it." instruction. Without this, agents tend to skip interactive steps that feel optional — especially when nested in sub-steps or wrapped in conditional language like "if enabled".
- **Task tracking**: Use task tracking in phases with 3+ sub-steps, for AI self-tracking not user-facing (Claude Code: `TodoWrite`)
- **Sequential execution**: For multi-phase workflows (4+ phases), enforce sequential execution with plan mode + TodoWrite instead of text-based pre-conditions. Start in plan mode so the user sees and approves the full pipeline. Initialize TodoWrite with all phases as pending. Mark each `in_progress` when starting, `completed` when done. Only one phase `in_progress` at a time. This is more robust than "Pre-condition: phase N must be complete" text in each phase file, because TodoWrite provides visual tracking and plan mode forces user approval.
- **No time estimates in phase titles**: Duration estimates ("~30 min", "~1h") are noise. They're always wrong, they vary by tool complexity, and they clutter the pipeline. State what the phase does, not how long it takes.
- **Pre-flight checklist**: Replace `## Critical Rules` with a verifiable checklist in the last phase before publishing. Each item must be testable (not vague).
- **Writes to shared content**: Before creating or editing anything others read (issues, PRs, docs, messages), show the exact result — the full body or a diff — at a `(CHECKPOINT)`, and write only what was approved. A change made after the approval, including a pre-flight fix, is presented again. Pass bodies as files (`--body-file`), never as inline shell strings, whose backticks and `$` the shell expands.
- **Load-bearing output**: Output the user approves or a check relies on (a diff, a log, a list) must reach the agent whole. Command proxies and output-compacting hooks (e.g. rtk) rewrite `diff`, `git diff`/`log`/`show`/`status`/`branch`, `gh pr diff`, `cat`, `head` or `tail` into truncated summaries or reads that drop lines, and a `curl` response into its JSON schema (`id: int`, no values) or a cut HTML page, still exit 0, and may refuse `find` actions (`-delete`, `-exec`) — a limitation, not a guard: the action silently doesn't happen. Read a file with the Read tool, and run a load-bearing command with the hook's explicit bypass (`RTK_DISABLED=1 git --no-pager diff --no-index -- a b`, `RTK_DISABLED=1 git --no-pager log`, `RTK_DISABLED=1 curl -s <url>` for any response body the agent reads, POST responses included; a `find` that must delete, scoped to one directory and one name pattern: `RTK_DISABLED=1 command find "<dir>" -maxdepth 1 -name '*.tmp' -delete`): a form that merely goes unrecognised today, such as `git --no-pager …`, can be rewritten by the next version of the hook. The variable is harmless where no hook is installed, and a prefixed command is no longer auto-allowed by the hook nor matched by `allowed-tools` prefixes, so it prompts. Check a command against the hook when the environment has one (`rtk rewrite '<command>'`). The rule covers commands the agent runs: a `` !`…` `` preload runs outside the hook, is not rewritten, and stays unprefixed so it keeps matching `allowed-tools`.

```markdown
### N. Pre-flight checklist

**Verify every item below.** Display pass/fail status. Fix failures before proceeding.

[ ] Item 1 — what to verify
[ ] Item 2 — what to verify
```

## Creating a New Skill

### Step 1: Determine the skill category

Classify by what the skill DOES, not what it's about. Every skill should fit one category:

| Category | What it does | Characteristics | Example |
|---|---|---|---|
| **Library / API Reference** | Encodes how to use a tool, SDK, or internal library correctly | `user-invocable: false`, loaded on demand | brand-voice, writing-style |
| **Product Verification** | Tests or verifies that output is correct | Paired with scripts, explicit pass/fail | content-audit, security-review |
| **Data Fetching & Analysis** | Connects to data sources, runs queries | Uses MCP servers or APIs, returns structured data | analytics-report, metrics-check |
| **Business Process** | Automates repetitive workflows | Multi-step, checkpoint-driven | standup-post, release-notes |
| **Code Scaffolding** | Generates boilerplate for project patterns | Templates, conventions-aware | new-feature, add-connector |
| **Code Quality** | Enforces standards, reviews code | Spawns sub-agents, iterates until clean | code-review, lint-check |
| **CI/CD & Deployment** | Builds, tests, deploys | Has side effects → `disable-model-invocation: true` | deploy, publish |
| **Runbook** | Diagnoses and resolves known issues | Decision tree, symptom-matching | debug, incident-response |
| **Shared Config** | Provides conventions and settings | `user-invocable: false`, loaded by family | family-rules, shared-config |

If a skill straddles two categories, split it.

### Step 2: Scaffold the directory and write the SKILL.md

1. Frontmatter with `name`, `description` (using the description formula)
2. One-line description block
3. `## When to Use` section (trigger conditions)
4. `## Why This Exists` section (motivation, what goes wrong without it)
5. `## Gotchas` section (non-obvious pitfalls)
6. Load directives for phases and dependencies

### Step 3: Write phase files (if multi-step)

Each phase file starts with a `#` heading and contains actionable instructions. In SKILL.md, reference each phase with a load directive and a brief description of what it produces.

### Step 4: Validate with realistic prompts

Test the skill with 2-3 realistic user prompts — the kind of thing someone would actually type, with natural phrasing and context. Verify the skill triggers correctly and produces the expected behavior. If triggering is unreliable, make the description more "pushy".

## Editing an Existing Skill

1. Read the current SKILL.md and all phases before making changes
2. Check frontmatter is valid and up-to-date
3. Verify load directives still point to correct paths
4. Run the conventions check below after editing

## Anti-Patterns

Avoid these common mistakes when writing skills:

| Anti-pattern | Why it's bad | Fix |
|---|---|---|
| Restating what the agent already knows | Wastes tokens, competes with conversation context | Only document project-specific or non-obvious knowledge |
| Hardcoded file paths | Breaks when project structure changes | Use `{baseDir}` placeholders or describe patterns |
| Deeply nested references | Agent loses context traversing chains | One level deep max from SKILL.md |
| Time-sensitive information | Becomes stale, causes wrong behavior | Put dates in the agent's config file, not skills |
| Multiple options without defaults | Agent has to guess which to pick | Always specify a default, note alternatives |
| Rigid ALWAYS/NEVER commands | Agent checks boxes instead of thinking | Explain the *why* behind the rule — agents respond better to reasoning than rigid commands |
| Inconsistent terminology | Confuses the agent across sections | Pick one term per concept, use it throughout (e.g., always "endpoint" not sometimes "route", "URL", "path") |
| Monolithic SKILL.md (500+ lines) | Loaded every time, wastes tokens | Split into phases/ and references/ |
| Text-based pre-conditions ("Pre-condition: phase N must be complete") | Agent reads it but doesn't enforce it — easy to skip under context pressure | Use plan mode + TodoWrite for sequential enforcement |
| Time estimates in phase titles ("~30 min") | Always wrong, varies by complexity, clutters the pipeline | Remove — state what the phase does, not how long |
| Orchestrator skills that rewrite sub-skill rules | Duplicates rules, drifts from source, wastes tokens | Reference the sub-skill by name ("Run `/humanizer`"), don't copy its instructions |
| Sub-skill call next to a manual checklist | Agent does the checklist manually and skips the skill. "Run `/seo-auditor`" + 5 checklist items below = agent checks the 5 items itself, never invokes the skill | Sub-skill invocations must be numbered steps BEFORE manual checks, with CHECKPOINT. Manual checks come after, only for things the sub-skill doesn't cover |

## Conventions Check (run after create/edit)

- [ ] Frontmatter has `name` + `description` (both non-empty)
- [ ] `description` follows the formula: "[What it does]. Use when [trigger]."
- [ ] `description` is "pushy" enough to combat undertriggering
- [ ] `name` matches directory name (kebab-case)
- [ ] Skill fits cleanly into one category (not straddling)
- [ ] Has `## When to Use` section
- [ ] Only documents what the agent doesn't inherently know (token efficiency)
- [ ] SKILL.md body is under 500 lines
- [ ] Phase files are numbered (`01-`, `02-`, etc.) if phases/ exists
- [ ] Load directives use relative paths and point to existing files
- [ ] No duplicate rules between skill and its family rules
- [ ] References are one level deep max from SKILL.md
- [ ] No hardcoded absolute paths — uses relative or pattern-based paths
- [ ] Interactive question tool used for user input (workflow/content skills)
- [ ] `disable-model-invocation: true` set if skill has side effects
- [ ] `user-invocable: false` set if skill is background knowledge
- [ ] All content in English (only examples may be in target language)
- [ ] Examples use `❌ Don't:` / `✅ Do:` format
- [ ] No `## Critical Rules` section — rules enforced via pre-flight checklist
- [ ] Workflow skills with side effects have a pre-flight checklist
- [ ] Steps requiring user input are marked `(CHECKPOINT)` with "Do NOT skip" instruction
- [ ] No conditional language ("mandatory if...") on blocking steps — use imperative
- [ ] Consistent terminology throughout (one term per concept)
- [ ] `name` is action-oriented (not vague like `helper` or `utils`)
- [ ] Validated with 2-3 realistic prompts
- [ ] Multi-phase workflows use plan mode + TodoWrite (not text pre-conditions)
- [ ] No time estimates in phase titles
- [ ] Orchestrator skills reference sub-skills by name, don't duplicate their rules
- [ ] Sub-skill invocations are numbered steps with CHECKPOINT, not annotations inside manual checklists
- [ ] `allowed-tools` lists no blanket network or VCS pattern (`curl:*`, `git:*`, `gh:*`) and no command-group prefix (`gh issue:*`): exact read subcommands only
- [ ] Output shown for approval or used as a check (diffs, logs, status, files read back) comes from the Read tool or a command with the hook's explicit bypass (`RTK_DISABLED=1 …`), `curl` bodies included; `` !`…` `` preloads stay unprefixed
- [ ] Every write to shared content follows a CHECKPOINT that shows the exact result; bodies passed as files
