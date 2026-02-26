---
name: skill-update
description: Update an existing jaan-to skill following standards. Use when modifying or improving existing skills.
allowed-tools: Read, Glob, Grep, Task, WebSearch, Write(skills/**), Write(docs/**), Write($JAAN_OUTPUTS_DIR/**), Edit(skills/**), Edit(docs/**), Bash(bash scripts/prepare-skill-pr.sh*), Bash(git checkout:*), Bash(git branch:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(gh pr create:*)
argument-hint: [skill-name]
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# skill-update

> Update existing jaan.to skills with specification compliance and documentation sync.

## Context Files

- `docs/extending/create-skill.md` - Skill specification (REQUIRED)
- `$JAAN_LEARN_DIR/jaan-to-skill-update.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_CONTEXT_DIR/config.md` - Current skill catalog
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Skill Name**: $ARGUMENTS

The name of the skill to update (e.g., `pm-prd-write` or just `prd-write`).

If not provided, list available skills and ask which to update.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `skill-update`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_skill-update`

---

# PHASE 0: Git Branch Setup

Create feature branch for updates:

```bash
git checkout dev
git pull origin dev
git checkout -b update/{skill-name}
```

Confirm: "Created branch `update/{name}` from `dev`. All updates on this branch."

---

# PHASE 1: Analysis (Read-Only)

## Thinking Mode

ultrathink

Use extended reasoning for:
- Analyzing existing skill structure
- Planning updates carefully
- Validating against specification
- Ensuring backward compatibility

## Questioning Guidelines

Ask up to 7 clarifying questions across Phase 1 if needed.

**Skip questions when**:
- Information already provided in user input
- Research answered the question
- Context files contain the answer
- Question is redundant with previous answer

**Make questions smart**:
- Reference user's input: "You said '{X}' — does that mean...?"
- Build on existing skill: "The current skill does Y — should that change?"
- Probe specifics: "What should happen when Z?"

## Step 1: Read Existing Skill

Read all files for the skill:
- `skills/{name}/SKILL.md` - Current skill definition
- `$JAAN_LEARN_DIR/{name}.learn.md` - Accumulated lessons
- `$JAAN_TEMPLATES_DIR/{name}.template.md` - Output template (if exists)

Display current structure:
```
CURRENT SKILL: {name}
────────────────────
Command: /{name}
Name: {name}
Description: {description}

FILES
─────
□ SKILL.md ({line_count} lines)
□ LEARN.md ({lesson_count} lessons)
□ template.md ({exists/missing})
```

## Step 2: Validate Against Specification

Check current skill against `docs/extending/create-skill.md`:

**Frontmatter**:
- [ ] Has `name` matching directory
- [ ] Has `description` with purpose and mapping
- [ ] Has `allowed-tools` with valid patterns
- [ ] Has `argument-hint`

**Body**:
- [ ] Has H1 title matching skill name
- [ ] Has tagline blockquote
- [ ] Has `## Context Files`
- [ ] Has `## Input`
- [ ] Has `# PHASE 1: Analysis`
- [ ] Has `## Step 0: Apply Past Lessons`
- [ ] Has `# HARD STOP`
- [ ] Has `# PHASE 2: Generation`
- [ ] Has `## Definition of Done`

**Trust**:
- [ ] Tool permissions are sandboxed

Show compliance status:
```
SPECIFICATION COMPLIANCE
────────────────────────
✓ Frontmatter: 4/4 fields
✗ Body: 8/9 sections (missing: Step 0)
✓ Trust: sandboxed
```

## Step 2.1: v3.0.0 Compliance Check

Check the skill for v3.0.0 customization system compatibility:

Read and apply V3.1–V3.10 check patterns from: `${CLAUDE_PLUGIN_ROOT}/docs/extending/v3-compliance-reference.md` (section: "skill-update: v3.0.0 Compliance Checks", subsections V3.1–V3.10)

Run each check (V3.1 through V3.10) against the skill. Then display:

### v3.0.0 Compliance Summary

Display results:
```
v3.0.0 COMPLIANCE
─────────────────
V3.1 Frontmatter env vars:     ✓ / ✗
V3.2 Context paths:             ✓ / ✗
V3.3 Learning path:             ✓ / ✗
V3.4 Template path:             ✓ / ✗ / N/A
V3.5 Output path:               ✓ / ✗ / N/A
V3.6 Template variables:        ✓ / ✗ / N/A
V3.7 Tech integration:          ✓ / N/A

OUTPUT STRUCTURE COMPLIANCE
───────────────────────────
V3.8.1 ID generation:           ✓ / ✗ / N/A
V3.8.2 Folder structure:        ✓ / ✗ / N/A
V3.8.3 Index management:        ✓ / ✗ / N/A
V3.8.4 Executive Summary:       ✓ / ✗ / N/A

DESCRIPTION BUDGET
──────────────────
V3.9 Description budget:        ✓ / ✗

DISPLAY STRINGS
───────────────
V3.10 Display paths use vars:   ✓ / ✗

VERDICT: v3.0.0 Compliant / Needs Migration / Needs Output Migration / Needs Description Fix / Needs Display Fix
```

If **any check fails (✗)**:
- Add option [8] to Step 3: "Migrate to v3.0.0"
- If V3.8 checks fail: Add option [9]: "Migrate output structure to ID-based folders"

## Step 3: Ask Update Type

> "What do you want to change?"
>
> [1] Add/modify questions (Phase 1)
> [2] Update quality checks (Phase 2)
> [3] Modify output format (template.md)
> [4] Add tool permissions
> [5] Incorporate LEARN.md lessons → SKILL.md
> [6] Fix specification compliance issues
> [7] Other (describe)
> [8] Migrate to v3.0.0 (if v3.0.0 compliance check failed)
> [9] Migrate output structure to ID-based folders (if V3.8 check failed)
> [10] Fix description budget (trim Auto-triggers/Maps-to lines, shorten description)

## Step 4: Optional Web Research

For options [1], [2], [3], or [7], offer:
> "Search for updated best practices? [y/n]"

If yes, use **Task tool with Explore subagent**:
```
Task prompt: "Research current best practices for {domain}:
1. Search '{domain} best practices {year}'
2. Search '{domain} checklist {year}'
Return: new practices, updated methodologies, changes since {skill_created_date}"
```

## Step 5: Plan Changes

Based on selected option, plan specific changes:

**Option 1 (Questions)**: Show current questions, propose additions
**Option 2 (Quality)**: Show current checks, propose updates
**Option 3 (Template)**: Show current template, propose modifications
**Option 4 (Tools)**: Show current permissions, propose additions
**Option 5 (LEARN→SKILL)**: Map lessons to skill sections:

| LEARN.md Section | Incorporate Into |
|------------------|------------------|
| Better Questions | Phase 1 Step 1 questions |
| Edge Cases | Phase 2 quality checks |
| Workflow | Process steps + Definition of Done |
| Common Mistakes | Warnings in relevant sections |

**Option 6 (Compliance)**: List missing sections, propose additions
**Option 7 (Other)**: Gather details, plan custom changes

**Option 8 (Migrate to v3.0.0)**: Read and apply migration wizard from: `${CLAUDE_PLUGIN_ROOT}/docs/extending/v3-compliance-reference.md` (section: "Migration Wizard (v2.x → v3.0.0)"). Offers 4 approaches: Auto-fix all, Interactive, Manual script, Guidance only.

---

# HARD STOP - Human Review Check

Show diff preview:

```
PROPOSED CHANGES
────────────────
File: SKILL.md
───
- old line
+ new line
───

File: template.md (if applicable)
───
- old line
+ new line
───

COMPLIANCE AFTER UPDATE
───────────────────────
✓ Frontmatter: 4/4 fields
✓ Body: 9/9 sections
✓ Trust: sandboxed
```

> "Apply these changes? [y/n/edit]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Update (Write Phase)

## Step 6: Update SKILL.md

Apply planned changes while preserving:
- Two-phase workflow structure
- HARD STOP section
- Definition of Done section
- Specification compliance

## Step 7: Update template.md (if needed)

If output format changes requested:
1. Update template structure
2. Preserve required metadata section
3. Update placeholders

## Step 8: Update LEARN.md

If Option 5 selected (lessons incorporated):
- Add workflow note: "Incorporated into SKILL.md on {date}"
- Keep original lessons for reference

Otherwise, add any new workflow learnings:
- "Updated {section} based on {reason}"

## Step 9: Validate Updated Skill

Run full specification check:

- [ ] YAML frontmatter complete
- [ ] All required sections present
- [ ] Two-phase workflow intact
- [ ] HARD STOP section exists
- [ ] Definition of Done present
- [ ] Tool permissions sandboxed

If any check fails, fix before continuing.

## Step 10: Preview All Changes

Show final versions of all modified files.

> "Write these updates? [y/n]"

## Step 10.5: Handle Output Structure Migration (If Option [9] Selected)

Read and apply output structure migration from: `${CLAUDE_PLUGIN_ROOT}/docs/extending/v3-compliance-reference.md` (section: "Output Structure Migration (Step 10.5)")

Includes: migration plan display, HARD STOP approval, Step 5.5 insertion, output writing update, template update, and validation checklist.

## Step 11: Write Updated Files

If approved:
1. Write SKILL.md to `skills/{name}/SKILL.md`
2. Write template.md to `skills/{name}/template.md` (if modified)
3. Write LEARN.md to `skills/{name}/LEARN.md`

Confirm: "Skill files updated in `skills/{name}/`"

## Step 12: Auto-Invoke Documentation Sync

Run `/jaan-to:docs-update {name}` to sync:
- `docs/skills/{role}/{name}.md`

This ensures documentation stays in sync with skill changes.

## Step 13: Commit to Branch

Stage and commit updated files:

```bash
bash scripts/prepare-skill-pr.sh
git add skills/{name}/ jaan-to/ docs/skills/{role}/{name}.md
```

`prepare-skill-pr.sh` regenerates + validates Codex skillpack artifacts and stages `adapters/codex/skillpack/`.

For full commit message template, read: `${CLAUDE_PLUGIN_ROOT}/docs/extending/git-pr-workflow.md` (section: "Step 13: Commit to Branch")
Commit message prefix: `fix(skill): Update {name} skill`

---

# PHASE 3: Testing & PR

## Step 14: User Testing

> "Please test the updated skill in a new session. Here's a copy-paste ready example:"
>
> ```
> /{name} "{example_input_based_on_skill_purpose}"
> ```
>
> "Did it work correctly? [y/n]"

If issues:
1. Help debug the problem
2. Make fixes
3. Commit fixes
4. Repeat testing

## Step 15: Create Pull Request

When user confirms working:
> "Create pull request to merge to dev? [y/n]"

If yes, push and create PR. For full PR body template, read: `${CLAUDE_PLUGIN_ROOT}/docs/extending/git-pr-workflow.md` (section: "Step 15: Create Pull Request")

```bash
git push -u origin update/{name}
gh pr create --base dev --title "fix(skill): Update {name} skill" --body "..."
```

PR summary must include:

`Codex skillpack sync: ✅ generated via scripts/prepare-skill-pr.sh`

Show PR URL to user.

If no:
> "Branch `update/{name}` is ready. Merge manually when ready."

---

## Step 16: Capture Feedback

> "Any feedback on the skill update process? [y/n]"

If yes:
- Run `/jaan-to:learn-add skill-update "{feedback}"`

### v3.0.0 Migration Feedback (if Option 8 was used)

If skill was migrated to v3.0.0, capture migration-specific learnings:

**Categories**: migration approach effectiveness, missed patterns, template variable adoption, tech stack integration.

**Auto-categorize**: patterns to compliance checks, edge cases to Step 2.1, workflow to Migration Wizard.

Example:
```
/jaan-to:learn-add skill-update "Auto-fix missed pattern: `Read(jaan-to/docs/**)` in doc-generation skills."
```

---

## Step 17: Auto-Invoke Roadmap Update

Run `/jaan-to:pm-roadmap-update` to sync the skill update with the roadmap.

This ensures the roadmap reflects the latest skill changes.

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Single source of truth (no duplication)
- Plugin-internal automation
- Maintains human control over changes

## Definition of Done

- [ ] Existing skill files read and analyzed
- [ ] Specification compliance validated
- [ ] User-selected updates applied
- [ ] Passes specification validation after update
- [ ] Documentation synced via /jaan-to:docs-update
- [ ] User tested and confirmed working
- [ ] PR created (or branch ready for manual merge)
- [ ] Roadmap synced via /jaan-to:pm-roadmap-update
- [ ] User approved final result
