---
name: learn-add
description: Add a lesson to a skill LEARN.md file, routing feedback to skill, template, or context learning. Use when capturing workflow lessons.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/**), Bash(git add:*), Bash(git commit:*), Edit(jaan-to/config/settings.yaml)
argument-hint: "[target] [lesson]"
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# learn-add

> Route feedback to the appropriate LEARN.md file.

## Context Files

- `$JAAN_LEARN_DIR/*.learn.md` - Skill lessons
- `$JAAN_CONTEXT_DIR/*.md` - Context files and lessons
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

## Input

**Arguments**: $ARGUMENTS

Expected format: `"target" "lesson"`
- Target: skill name, `$JAAN_TEMPLATES_DIR/name`, or `$JAAN_CONTEXT_DIR/name`
- Lesson: the feedback to add

Examples:
- `/jaan-to:learn-add "pm-prd-write" "Always ask about rollback strategy"`
- `/jaan-to:learn-add "$JAAN_CONTEXT_DIR/tech" "All new tables need soft delete"`

If no input provided, ask for target and lesson.

---

## Pre-Execution Protocol

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_learn-add`

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Parse Input

Extract target and lesson from arguments.

If format is unclear:
1. "Which skill/context should this lesson apply to?"
2. "What is the lesson to add?"

## Step 2: Determine Target File

Route based on target:

| Target Pattern | LEARN.md Location |
|----------------|-------------------|
| Skill name (e.g., `pm-prd-write`) | `$JAAN_LEARN_DIR/jaan-to-{skill}.learn.md` |
| System skill (e.g., `skill-create`) | `$JAAN_LEARN_DIR/jaan-to-{skill}.learn.md` |
| `$JAAN_TEMPLATES_DIR/{name}` | `$JAAN_TEMPLATES_DIR/LEARN.md` |
| `$JAAN_CONTEXT_DIR/{name}` | `$JAAN_CONTEXT_DIR/LEARN.md` |
| `$JAAN_CONTEXT_DIR/tech` | `$JAAN_CONTEXT_DIR/tech.md` (constraints section) |
| `$JAAN_CONTEXT_DIR/team` | `$JAAN_CONTEXT_DIR/team.md` (norms section) |

## Step 3: Auto-Categorize Lesson

Detect category from lesson keywords:

| Category | Trigger Keywords |
|----------|------------------|
| Better Questions | ask, question, clarify, confirm, "should ask" |
| Edge Cases | edge, special, case, handle, check, "need to handle" |
| Workflow | workflow, process, step, order, "before/after" |
| Common Mistakes | avoid, mistake, wrong, don't, never, "should not" |

If unclear, ask: "Which category? [questions/edge-cases/workflow/mistakes]"

## Step 4: Read Current LEARN.md

Read the target LEARN.md file if it exists at `$JAAN_LEARN_DIR/jaan-to-{name}.learn.md`.
If not found, check legacy path `$JAAN_LEARN_DIR/jaan-to:{name}.learn.md` — if legacy found, rename it to the dash-prefixed path first.
If neither exists, prepare to create with template.

---

# HARD STOP - Human Review Check

Show preview:
```markdown
Ready to Add Lesson

**File:** {file path}
**Category:** {category}
**Lesson:** {lesson text}

Preview:
## {Category}
- {existing lessons...}
- {new lesson}  <-- NEW

Confirm? [y/n/edit]
```

**Do NOT proceed without explicit approval.**

---

# PHASE 2: Write

## Step 5: Update LEARN.md

If file exists:
1. Read current content
2. Find the category section (e.g., `## Better Questions`)
3. Append new lesson as bullet point
4. Update "Last updated" date
5. Write file

If file doesn't exist:
1. Check if plugin has seed data: `${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/LEARN.md`
2. If seed exists and has meaningful content (contains `- ` bullet points), use it as starting point
3. If no seed exists, create from the template below
4. Add the new lesson to the appropriate category
5. Write file to: `$JAAN_LEARN_DIR/jaan-to-{skill-name}.learn.md`

### LEARN.md Template

```markdown
# Lessons: {skill-name}

> Last updated: {date}

## Better Questions
- {lesson if category matches}

## Edge Cases
- {lesson if category matches}

## Workflow
- {lesson if category matches}

## Common Mistakes
- {lesson if category matches}
```

## Step 6: Confirm Write

```markdown
Lesson Added

**File:** {path}
**Category:** {category}
**Lesson:** {lesson}
```

## Step 7: Offer to Commit

Ask user:
```
Commit this lesson? [y/n]
```

**If confirmed:**
1. Stage: `git add {file_path}`
2. Commit: `git commit -m "learn({skill}): {short lesson summary}"`
3. Show: "Lesson committed: `{commit hash}`"

**If declined:**
- Skip commit, lesson is saved locally
- Show: "Lesson saved (not committed)"

---

## Error Handling

### No Target
> "No target specified. Which skill or context should this lesson apply to?"

### Target Not Found
> "Skill '{target}' not found. Available skills: {list}"

### Empty Lesson
> "No lesson provided. What feedback should be remembered?"

### LEARN.md Create Fail
> "Could not create LEARN.md. Check file permissions."

---

## Trust Rules

1. **NEVER** modify without user confirmation
2. **ALWAYS** show preview before writing
3. **PRESERVE** existing lessons
4. **ASK** when category is unclear

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Single source of truth (no duplication)
- Plugin-internal automation
- Maintains human control over changes

## Definition of Done

- [ ] Target skill/context identified and validated
- [ ] Lesson categorized (questions/edge-cases/workflow/mistakes)
- [ ] Preview shown and user approved
- [ ] LEARN.md file updated with new lesson
- [ ] Commit offered to user
