---
name: skill-create
description: Guide users through creating new jaan-to skills step-by-step. Use when building a new plugin skill.
allowed-tools: Read, Glob, Grep, Task, WebSearch, Write(skills/**), Write(docs/**), Write($JAAN_OUTPUTS_DIR/**), Edit($JAAN_TEMPLATES_DIR/**), Edit($JAAN_LEARN_DIR/**), Edit(jaan-to/config/settings.yaml), Bash(bash scripts/prepare-skill-pr.sh*), Bash(git checkout:*), Bash(git branch:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr create:*)
argument-hint: [optional-skill-idea]
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# skill-create

> Guide users through creating new jaan.to skills with web research and best practices.

## Context Files

- `docs/extending/create-skill.md` - Skill creation specification (v3.0.0)
- `$JAAN_LEARN_DIR/jaan-to-skill-create.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_TEMPLATES_DIR/jaan-to-skill-create.template.md` - Generation templates
- `$JAAN_CONTEXT_DIR/config.md` - Current skill catalog
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Skill Idea**: $ARGUMENTS

If provided, use as starting context. Otherwise, begin with identity questions.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `skill-create`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

**v3.0.0 Common Mistakes to Avoid** (regardless of LEARN.md):
- ✗ Using hardcoded `jaan-to/outputs/` instead of `$JAAN_OUTPUTS_DIR`
- ✗ Using hardcoded `jaan-to/templates/` instead of `$JAAN_TEMPLATES_DIR`
- ✗ Using hardcoded `jaan-to/learn/` instead of `$JAAN_LEARN_DIR`
- ✗ Using hardcoded `jaan-to/context/` instead of `$JAAN_CONTEXT_DIR`
- ✗ Forgetting `#anchor` syntax when importing tech.md sections
- ✗ Using too-broad permissions like `Write(jaan-to/**)`
- ✗ Not validating with `/jaan-to:skill-update` before user testing

If the file does not exist, continue without it (but still avoid mistakes above).

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_skill-create`

---

# PHASE 0: Duplicate Detection (Single Source of Truth)

Before any creation, check for existing skills:

1. **Glob** `skills/*/SKILL.md` to get all skills
2. **For each skill**, compare:
   - Role + domain match
   - Purpose description similarity
   - Calculate overlap score (0-100%)

3. **Decision tree**:
   - **Exact match exists**: "Skill '{name}' already does this. Use: `/{command}` [show example]"
   - **>70% overlap**: "'{name}' is similar ({n}% overlap). Update it instead? [update/new]"
     - If update: Invoke `/jaan-to:skill-update {name}`
     - If new: Continue with creation
   - **<70% overlap**: Continue with creation

4. **Fast-track option** for simple skills:
   > "This seems straightforward. Create minimal skill directly? [y/wizard]"

   Skip wizard for:
   - Single-purpose skills with obvious structure
   - Skills that wrap an existing command
   - Internal/utility skills with <50 lines expected

---

# PHASE 1: Analysis (Interactive + Research)

## Thinking Mode

ultrathink

Use extended reasoning for:
- Analyzing user requirements
- Planning skill structure
- Validating against specification
- Research synthesis

## Questioning Guidelines

Ask up to 7 clarifying questions across Phase 1 if needed.

**Skip questions when**:
- Information already provided in user input
- Research answered the question
- Context files contain the answer
- Question is redundant with previous answer

**Make questions smart**:
- Reference user's input: "You said '{X}' — does that mean...?"
- Build on research: "Best practices suggest Y — does that fit your case?"
- Probe specifics: "What should happen when Z?"

## Step 1: Basic Identity

Ask these questions one at a time:

| Question | Purpose | Validation |
|----------|---------|------------|
| "What role does this skill serve?" | Determine role prefix | Must be: pm, dev, qa, ux, data, growth, or custom |
| "What domain/area does it work in?" | Determine domain | 1-2 words, lowercase, hyphens allowed |
| "What action does it perform?" | Determine action verb | write, create, add, review, generate, update, analyze, etc. |

**After answers**, validate and show:
> "Skill name will be: `{role}-{domain}-{action}`"
> "Command: `/jaan-to:{role}-{domain}-{action}`"
> "Directory: `skills/{role}-{domain}-{action}/`"

## Step 1.5: Check Project Configuration (v3.0.0)

Before proceeding with design, understand the project's configuration:

1. **Check if configuration exists**:
   - Read `jaan-to/config/settings.yaml` (if exists)
   - Note any custom path configurations

2. **Path customization check**:
   - Are default paths customized?
   - If `settings.yaml` has `paths:` section, note custom locations
   - Skills should use `$JAAN_*` env vars (automatically resolve to correct paths)

3. **Learning strategy**:
   - Check `settings.yaml` for `learning.strategy: "merge"` or `"override"`
   - **merge**: Combine plugin + project lessons (default, recommended)
   - **override**: Use only project lessons (ignore plugin defaults)

4. **Template customization**:
   - Check if custom templates exist for similar skills
   - Pattern: `templates.{skill-name}.path: "./custom/path.md"`
   - If project has custom templates, new skill should follow same pattern

**Information helps generate skills that work correctly with the project's configuration.**

> "Configuration checked: [default paths / custom paths detected]"

## Step 2: Web Research (Token-Optimized)

Use **Task tool with Explore subagent** to isolate research tokens:

```
Task prompt: "Research best practices for {domain} {action}:
1. Search '{domain} best practices {year}'
2. Search '{domain} report template'
3. Search 'how to {action} {domain}'
4. Search '{domain} checklist'

Return:
- 3-5 key best practices
- Suggested questions the skill should ask
- Suggested quality checks
- Suggested output sections
- Sources used"
```

**Present research summary to user**:
> "Research findings for {domain}:
>
> **Best Practices Found:**
> 1. {practice1}
> 2. {practice2}
> ...
>
> **Suggested Questions for Skill:**
> - {question1}
> - {question2}
> ...
>
> **Suggested Quality Checks:**
> - [ ] {check1}
> - [ ] {check2}
> ...
>
> **Suggested Output Sections:**
> - {section1}
> - {section2}
> ..."

## Step 3: Purpose & Triggers

Show research-based suggestions, then ask:

1. "What does this skill do? (1-2 sentences)"
   - [Suggested from research]: "{suggested_description}"

2. "What phrases should auto-trigger this skill?"
   - [Suggested]: {action} {domain}, {domain} {action}, etc.

## Step 4: Input & Output

1. "What input does the skill need?"
   - Examples: file path, topic name, feature description
   - Will become `$ARGUMENTS` handling

2. "What files/outputs does it produce?"
   - [Suggested from templates]: {format} file with {sections}

3. "What format? (markdown/json/both)"
   - Determines template.md creation

## Step 5: Questions, Quality & Done

Present research-based suggestions, let user accept/modify/add:

1. "What questions should the skill ask users?"
   - [Pre-filled from research]:
     - {research_question1}
     - {research_question2}
   - "Add more or modify? [accept/edit]"

2. "What quality checks before writing?"
   - [Pre-filled from research]:
     - [ ] {research_check1}
     - [ ] {research_check2}
   - "Add more or modify? [accept/edit]"

3. "What defines 'done' for this skill?"
   - [Suggested]:
     - [ ] Output file written
     - [ ] Quality checks pass
     - [ ] User approved

---

# HARD STOP - Human Review Check

Present complete skill structure:

```
SKILL SUMMARY
─────────────
Name: {role}-{domain}-{action}
Command: /{role}-{domain}-{action}
Logical: {role}-{domain}-{action}
Description: {description}

RESEARCH USED
─────────────
Sources: {source_count} web sources consulted
Best practices incorporated: {practice_count}

FILES TO CREATE
───────────────
□ skills/{name}/SKILL.md
□ skills/{name}/LEARN.md
□ skills/{name}/template.md (if needed)

WILL ALSO
─────────
□ Register in scripts/seeds/config.md
□ Create docs/skills/{role}/{name}.md (via /jaan-to:docs-create)
□ Commit to branch skill/{name}
```

> "Create this skill? [y/n/edit]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation (Write Phase)

## Step 6: Create Git Branch

```bash
git checkout dev
git pull origin dev
git checkout -b skill/{role}-{domain}-{action}
```

Confirm: "Created branch `skill/{name}` from `dev`. All work on this branch."

## Step 7: Generate SKILL.md

Use template from `$JAAN_TEMPLATES_DIR/jaan-to-skill-create.template.md`:

1. Fill YAML frontmatter:
   - name: {name}
   - description: from Step 3 (must include "Use when" trigger phrase, no colons)
   - allowed-tools: based on needs from Step 5
   - argument-hint: from Step 4
   - license: MIT
   - compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
   - **DO NOT add `model:` field** (use inherited default)

2. Fill markdown body:
   - Context Files from gathered info
   - Input handling from Step 4
   - Phase 1 questions from Step 5
   - HARD STOP section
   - Phase 2 generation steps
   - Quality checks from Step 5
   - Definition of Done from Step 5

## Step 8: Generate LEARN.md (Plugin Source)

Create `skills/{name}/LEARN.md` with research insights as initial lessons. Follow the standard LEARN.md structure from `docs/extending/v3-compliance-reference.md` section 12.7 (Better Questions, Edge Cases, Workflow, Common Mistakes). Seed each section with relevant research findings.

## Step 9: Generate template.md (Plugin Source, if needed)

Based on output format from Step 4:
- Use researched report structure
- Include required metadata section
- Add placeholders for dynamic content

## Step 10: Validate Against Specification

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/skill-create-reference.md` section "Specification Validation Checklist" for the full frontmatter, body, size, trust, and budget checks.

Validate against `docs/extending/create-skill.md`. If any check fails, fix before preview.

## Step 11: Preview All Files

Show complete content of:
1. SKILL.md
2. LEARN.md
3. template.md (if created)

> "Write these files? [y/n]"

## Step 12: Write Files (v3.0.0-Compliant)

> **Reference**: See `docs/extending/v3-compliance-reference.md` section "skill-create: v3.0.0 Best Practices for Writing Skills" for full details on Steps 12.1-12.9:
> - 12.1: Frontmatter (env var permissions, anti-patterns)
> - 12.2: Context Files section (standard env var references)
> - 12.3: Pre-Execution section (learning + language settings pattern)
> - 12.4: Template references (env vars, tech imports)
> - 12.5: Output paths (ID-based folder pattern, id-generator.sh, index-updater.sh)
> - 12.6: template.md variable syntax (`{{field}}`, `{{env:VAR}}`, `{{config:key}}`, `{{import:path#section}}`)
> - 12.7: LEARN.md seed structure (plugin-side, merge strategy)
> - 12.8: v3.0.0 validation checklist (compliance, output structure, tech stack, learning, quality)
> - 12.9: Automated path scan (hardcoded path detection and auto-fix)

Write to `skills/{name}/SKILL.md`, `skills/{name}/LEARN.md`, and `skills/{name}/template.md` (if needed), following all v3.0.0 patterns from the reference.


Confirm: "Skill files written to `skills/{name}/` (v3.0.0-compliant)"

## Step 13: Tech Stack Integration (Optional)

Ask: "Should this skill reference the project's tech stack?"

> **Reference**: See `docs/extending/v3-compliance-reference.md` section "skill-create: Tech Stack Integration Reference" for full details on Steps 13.1-13.4 (identifying needs, updating SKILL.md, template imports, documentation).

**Tech-aware**: PRD generation, code generation, story writing, API docs.
**Tech-agnostic**: Research, non-technical docs, roadmap planning.

> "Tech integration: [enabled / not applicable]"

## Step 14: Update Config Catalog

Edit `scripts/seeds/config.md` to add skill to Available Skills table:

```markdown
| {role}-{domain}-{action} | `/{name}` | {short_description} |
```

## Step 14.5: Update Team Roles Registry

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/skill-create-reference.md` section "Team Roles Registry Update Procedure" for the full role-matching and registry update steps.

If skill name matches a known role prefix, update `skills/team-ship/roles.md` accordingly. If `roles.md` does not exist, skip silently.

## Step 15: Auto-Invoke Documentation

Run `/jaan-to:docs-create` to create:
- `docs/skills/{role}/{name}.md`

This ensures documentation is always created with the skill.

## Step 16: Commit to Branch

> **Reference**: See `docs/extending/git-pr-workflow.md` section "skill-create: Commit to Branch" for the full commit template.

Before staging, run:

```bash
bash scripts/prepare-skill-pr.sh
```

This regenerates + validates Codex skillpack artifacts and stages `adapters/codex/skillpack/`.

Then stage `skills/{name}/`, `jaan-to/`, and `docs/skills/{role}/{name}.md`. Commit with feat(skill) message including description and research source count.

---

# PHASE 3: Testing & PR

## Step 17: Validate v3.0.0 Compliance

Run `/jaan-to:skill-update {skill-name}` before user testing.

> **Reference**: See `docs/extending/v3-compliance-reference.md` section "skill-create: v3.0.0 Post-Creation Validation" for full validation details.

**Only proceed to user testing after validation passes.**

## Step 18: User Testing

> "Please test the skill in a new session. Here's a copy-paste ready example:"
>
> ```
> /{name} "{example_input_based_on_skill_purpose}"
> ```
>
> For example, if the skill is `pm-prd-write`:
> ```
> /jaan-to:pm-prd-write "Add user authentication with OAuth support"
> ```
>
> "Did it work correctly? [y/n]"

If issues:
1. Help debug the problem
2. Make fixes
3. Commit fixes
4. Repeat testing

## Step 19: Create Pull Request

When user confirms working:
> "Create pull request to merge to dev? [y/n]"

> **Reference**: See `docs/extending/git-pr-workflow.md` section "skill-create: Create Pull Request" for the full `gh pr create` template.

Push branch, create PR with skill summary, research used, files created, and an explicit line:

`Codex skillpack sync: ✅ generated via scripts/prepare-skill-pr.sh`

Show PR URL to user.

If no:
> "Branch `skill/{name}` is ready. Merge manually when ready."

---

## Step 20: Capture Feedback

> "Any feedback on the skill creation process? [y/n]"

If yes:
- Run `/jaan-to:learn-add skill-create "{feedback}"`

---

## Step 21: Auto-Invoke Roadmap Update

Run `/jaan-to:pm-roadmap-update` to sync the new skill with the roadmap.

This ensures the roadmap reflects the latest skill additions.

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Single source of truth (no duplication)
- Plugin-internal automation
- Maintains human control over changes

## Definition of Done

- [ ] Duplicate check completed
- [ ] Web research performed
- [ ] All skill files created (SKILL.md, LEARN.md, template.md)
- [ ] Passes specification validation
- [ ] `scripts/validate-skills.sh` passes (description budget + body line cap)
- [ ] Registered in context/config.md
- [ ] Documentation created via /jaan-to:docs-create
- [ ] User tested and confirmed working
- [ ] PR created (or branch ready for manual merge)
- [ ] Roadmap synced via /jaan-to:pm-roadmap-update
- [ ] User approved final result
