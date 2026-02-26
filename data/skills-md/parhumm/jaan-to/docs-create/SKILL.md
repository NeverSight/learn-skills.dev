---
name: docs-create
description: Create new documentation with templates following STYLE.md. Use when adding new documentation pages.
allowed-tools: Read, Glob, Grep, Write($JAAN_DOCS_DIR/**), Write($JAAN_OUTPUTS_DIR/**), Bash(git add:*), Bash(git commit:*), Edit(jaan-to/config/settings.yaml)
argument-hint: "{type} {name}"
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# docs-create

> Create documentation with standard templates.

## Context Files

- `${CLAUDE_PLUGIN_ROOT}/docs/STYLE.md` - Documentation standards (read from plugin source)
- `$JAAN_TEMPLATES_DIR/jaan-to-docs.template.md` - Shared docs template (shared with docs-update)
- `$JAAN_LEARN_DIR/jaan-to-docs.learn.md` - Shared docs lessons (shared with docs-update, loaded in Pre-Execution)
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

**Note:** Templates are read from the project's `$JAAN_TEMPLATES_DIR` directory. Pre-execution protocol Step C offers to seed from the plugin on first use.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `docs-create`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)
**Shared resource override:** Template and learn files are shared with `docs-update`. For Steps A/B/C, resolve using `docs` as the resource name:
- Learn: `$JAAN_LEARN_DIR/jaan-to-docs.learn.md` (fallback: `${CLAUDE_PLUGIN_ROOT}/skills/docs-create/LEARN.md`)
- Template: `$JAAN_TEMPLATES_DIR/jaan-to-docs.template.md` (fallback: `${CLAUDE_PLUGIN_ROOT}/skills/docs-create/template.md`)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_docs-create`

---

# PHASE 1: Analysis (Read-Only)

## Step 1: Parse Input & Smart Type Detection

**Arguments**: $ARGUMENTS

Expected format: `{type} "{name}"`

| Type | Description |
|------|-------------|
| skill | Skill documentation |
| hook | Hook documentation |
| config | Config documentation |
| guide | How-to guide |
| concept | Concept explanation |
| index | Section README |

### Analysis First

Analyze user input to understand their actual need:

| User Intent Signal | Recommended Type | Reasoning |
|-------------------|------------------|-----------|
| Documenting a command, `/slash`, SKILL.md | **skill** | Users run it, needs usage guide |
| Documenting automatic behavior, hook, PreToolUse/PostToolUse | **hook** | Runs on events, needs trigger/behavior docs |
| Explaining settings, options, config | **config** | Reference for what can be changed |
| Teaching how to do something, steps, tutorial | **guide** | Step-by-step walkthrough |
| Explaining what something is, overview | **concept** | Understanding-focused, not action-focused |
| README, table of contents, section overview | **index** | Navigation and overview |

### Decision Logic

**If input is clear** (high confidence):
- Auto-select type
- Confirm: "I recommend **{type}** documentation for this. Here's why: {reasoning}. Proceed? [y/n/other]"

**If input is unclear** (ambiguous signals):
- Ask up to 5 smart clarifying questions tailored to the specific ambiguity
- Questions should probe the uncertainty, not be generic
- Example smart questions:
  - "You mentioned '{term}' — is this something users invoke, or does it run automatically?"
  - "Is your goal to help users DO something, or UNDERSTAND something?"
  - "Will this document a single command, or explain a broader concept?"
  - "Does this need step-by-step instructions, or is it reference material?"
  - "Who is the primary audience — end users or developers extending the system?"

### Best Practice Recommendations

Sometimes recommend a better approach:
- If user asks for "guide" but it's really a command → suggest **skill** doc
- If topic is complex → suggest **concept** first, then **guide**
- If documenting internal behavior → suggest **hook** over **config**

> "Based on your description, I'd recommend **{type}** because {reason}.
> However, you might also want a **{alt_type}** for {alt_reason}.
> Which would you like to create first?"

After determining type, ask for name if not provided:
> "What's the name/title?"

## Step 2: Determine Output Path

| Type | Path Pattern |
|------|--------------|
| skill | `$JAAN_DOCS_DIR/skills/{role}/{name}.md` |
| hook | `$JAAN_DOCS_DIR/hooks/{name}.md` |
| config | `$JAAN_DOCS_DIR/config/{name}.md` |
| guide | `$JAAN_DOCS_DIR/extending/{name}.md` |
| concept | `$JAAN_DOCS_DIR/{name}.md` |
| index | `$JAAN_DOCS_DIR/{section}/README.md` |

For skill type, ask: "Which role? [pm/dev/qa/ux/data/core]"

## Step 3: Check for Duplicates

Search for similar docs:
```
Glob: $JAAN_DOCS_DIR/**/*{name}*.md
Grep: "{name}" in $JAAN_DOCS_DIR/
```

If potential duplicate found:
> "Similar doc exists: `{path}`. Options: [proceed/update-existing/cancel]"

## Step 4: Read STYLE.md

Read `${CLAUDE_PLUGIN_ROOT}/docs/STYLE.md` for:
- Structure rules (H1, tagline, ---)
- Length limits
- Formatting patterns

## Step 5: Gather Content

Ask up to 5 clarifying questions if needed to gather sufficient content.

**Rules**:
- Skip questions when information is already in user input or context
- Tailor questions to gaps in current knowledge
- Questions should be specific, not generic

**Question Design**:
- Reference what you already know: "You mentioned X — can you elaborate on Y?"
- Probe for missing pieces: "I have the what, but need the why..."
- Confirm assumptions: "I'm assuming X applies here — correct?"

**For each doc type, focus on answering**:

| Type | Key Questions to Answer |
|------|------------------------|
| skill | What does it do? How to use it? What to expect? |
| hook | When does it run? What does it check? What happens? |
| config | What options exist? What are defaults? When to change? |
| guide | What's the goal? What are the steps? What can go wrong? |
| concept | What is it? Why does it matter? How does it relate? |
| index | What belongs here? How to organize? What's most important? |

---

# HARD STOP - Human Review Check

Show preview:
```markdown
Ready to Create Documentation

**Type:** {type}
**Path:** {output_path}
**Title:** {title}

## Content Preview:
{first 20 lines of content}

Proceed? [y/n/edit]
```

**Do NOT proceed without explicit approval.**

---

# PHASE 2: Generation

## Step 6: Load Template

Read template for doc type from `$JAAN_TEMPLATES_DIR/jaan-to-docs.template.md`

## Step 7: Fill Template

Replace placeholders with gathered content:
- `{title}` - Document title
- `{description}` - One-line tagline
- `{date}` - Current date (YYYY-MM-DD)
- `{tags}` - Relevant tags
- Other type-specific placeholders

## Step 8: Add Metadata

Ensure YAML frontmatter:
```yaml
---
title: {title}
doc_type: {type}
created_date: {today}
updated_date: {today}
tags: [{tags}]
related: []
---
```

## Step 9: Validate

Check against `${CLAUDE_PLUGIN_ROOT}/docs/STYLE.md`:
- [ ] Has H1 title
- [ ] Has tagline (`>`)
- [ ] Sections separated with `---`
- [ ] Under line limit for type
- [ ] No H4+ headings

If validation fails, fix before proceeding.

## Step 10: Preview & Write

Show full preview and ask:
> "Write to `{path}`? [y/n]"

If approved, write file.

## Step 10.5: Update Parent README

After writing the new doc file, update the parent folder's README.md to keep indexes in sync:

1. **Determine parent README path:**
   - For `$JAAN_DOCS_DIR/skills/{role}/{name}.md` → `$JAAN_DOCS_DIR/skills/{role}/README.md`
   - For `$JAAN_DOCS_DIR/hooks/{name}.md` → `$JAAN_DOCS_DIR/hooks/README.md`
   - For other types → skip this step

2. **Read the parent README.md** (if it doesn't exist, create one using the index template with frontmatter, H1, tagline, empty Available Skills table, and back-link)

3. **Find the "## Available Skills" section** (or equivalent table header)

4. **Check if the new doc is already listed:**
   - If listed → skip (no duplicate rows)
   - If not listed → add a new row to the table

5. **New row format:**
   ```
   | [/jaan-to:{skill-name}]({filename}.md) | {description from SKILL.md} |
   ```

6. **Also check `$JAAN_DOCS_DIR/skills/README.md` (root) Available Roles table:**
   - If the role folder is new → add a row for the new role with "Active" status and link to its README
   - If the role is listed as "Planned" → update to "Active" and add link

7. **Include the README changes in the commit** (Step 11 below)

## Step 11: Commit

```bash
git add {path}
git commit -m "docs({type}): Add {name} documentation

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Step 12: Follow-up

Show confirmation:
```markdown
✅ Documentation created!

**File:** {path}
**Commit:** {hash}

Run `/jaan-to:docs-update` to check related docs? [y/n]
```

If yes, suggest running `/jaan-to:docs-update --quick` for related docs.

---

## Error Handling

### Invalid Type
> "Invalid type '{type}'. Valid types: skill, hook, config, guide, concept, index"

### Path Exists
> "File already exists at `{path}`. Options: [overwrite/rename/cancel]"

### Validation Failed
> "Document doesn't meet STYLE.md standards: {issues}. Fixing..."

---

## Trust Rules

1. **NEVER** overwrite without confirmation
2. **ALWAYS** preview before writing
3. **VALIDATE** against STYLE.md
4. **CHECK** for duplicates first
5. **COMMIT** with descriptive message

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Single source of truth (no duplication)
- Plugin-internal automation
- Maintains human control over changes

## Definition of Done

- [ ] Documentation scope and target confirmed
- [ ] Content drafted following STYLE.md standards
- [ ] Document written to appropriate docs path
- [ ] User approved final document
