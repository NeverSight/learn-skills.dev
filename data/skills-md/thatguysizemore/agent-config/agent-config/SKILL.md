---
name: agent-config
description: Intelligently modify agent core context files (AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md). Use when conversation involves changing agent behavior, updating rules, tweaking personality, modifying instructions, adjusting operational procedures, updating memory architecture, changing delegation patterns, adding safety rules, refining prompt patterns, or any other modification to agent workspace configuration files. Triggers on intent to configure, tune, improve, fix, or evolve agent behavior through context file changes.
---

# Agent Config Skill

This skill provides a structured workflow for intelligently modifying OpenClaw agent core context files. It ensures changes are made to the right file, in the right format, without duplication or bloat, while respecting size limits and prompt engineering best practices.

## Core Workflow

When modifying agent context files, follow this process:

### 1. Identify Target File

Read `references/file-map.md` to determine which file the change belongs in.

**Quick decision tree:**
- Operational procedures, memory workflows, delegation rules → `AGENTS.md`
- Personality, tone, boundaries, ethical rules → `SOUL.md`
- Agent name, emoji, core vibe → `IDENTITY.md`
- User profile, preferences, family info → `USER.md`
- Local tool notes, command examples, API locations → `TOOLS.md`
- Curated long-term facts (main session only) → `MEMORY.md`
- Heartbeat checklist (keep tiny) → `HEARTBEAT.md`

**Critical:** Subagents only see `AGENTS.md` + `TOOLS.md`. Operational rules must go in `AGENTS.md`, not `SOUL.md`.

### 2. Check Current State

Before making changes:

```bash
# Check file size (20K char limit per file)
wc -c ~/clawd/AGENTS.md ~/clawd/SOUL.md ~/clawd/IDENTITY.md \
      ~/clawd/USER.md ~/clawd/TOOLS.md ~/clawd/MEMORY.md ~/clawd/HEARTBEAT.md

# Read the target file section to check for duplication
# Use grep to search for existing similar content
grep -i "keyword" ~/clawd/TARGETFILE.md
```

**Size warnings:**
- If file is > 18,000 chars, warn before adding (approaching truncation limit)
- If file is already > 20,000 chars, it's being truncated - refactor before adding more
- Agent can still read full file with `read` tool, but startup context is truncated

**Duplication check:**
- Is this instruction already present in different words?
- Is there a similar rule that should be updated instead of adding new?
- Does this belong in multiple files? (Usually no - pick ONE location)

### 3. Draft the Change

Read `references/claude-patterns.md` for instruction formats that work.

**Format guidelines by file:**

**AGENTS.md** (structured, imperative):
- Use numbered processes for multi-step workflows
- Use tables for decision trees, model selection, routing rules
- Include examples for complex patterns
- Explain WHY rules exist (motivation > bare commands)
- Use headers and sub-sections for organization
- Reference other files/skills, don't duplicate content

**SOUL.md** (first-person OK, narrative):
- Can use personal voice ("I'm Gus" vs "You are Gus")
- Anti-pattern lists work well (forbidden phrases, hedging examples)
- Include before/after examples for tone guidance
- Keep tattoos/anchors at top for immediate context
- Use contrasts (good vs bad examples side-by-side)

**IDENTITY.md** (minimal):
- Punchy bullets
- Keep under 500 chars if possible
- Core vibe only, details go in SOUL.md

**USER.md** (factual, third-person):
- Bullet lists by category
- Dates for time-sensitive info
- Clear section headers
- Cross-reference vault files for detailed project context

**TOOLS.md** (reference guide):
- Tables for comparison (when to use X vs Y)
- Code blocks for command examples
- Clear headings for quick lookup
- Include paths, env var names, exact syntax

**MEMORY.md** (wiki-style, topic-based):
- Section by topic, not chronologically
- Cross-reference entity files in vault
- Dates for context, but organize by subject
- Main session only - privacy-sensitive

**HEARTBEAT.md** (action list):
- Extremely concise
- Bullet list of checks
- No explanations (that's AGENTS.md)
- Fast to parse

### 4. Validate Before Applying

Ask yourself:

**Fit:**
- Does this actually belong in this file based on file-map.md?
- Is it operational (AGENTS.md) or personality (SOUL.md)?
- Will subagents need this? (If yes, must be AGENTS.md or TOOLS.md)

**Format:**
- Does this match the file's existing style?
- Is it the right structure (numbered, table, bullets, prose)?
- Are examples included where needed?

**Size:**
- How many chars is this adding?
- Is the file approaching 20K limit?
- Could this be a reference file instead?

**Duplication:**
- Is this already present somewhere else?
- Should existing content be updated instead?
- Could this consolidate multiple scattered rules?

**Quality:**
- Is motivation explained (WHY this rule exists)?
- Are examples concrete and real (not generic)?
- Is it precise enough for an AI to follow?
- Does it avoid vague instructions like "be helpful"?

### 5. Apply the Change

Use the `edit` tool with exact text matching:

```python
# Read the section first to get exact text
read(path="~/clawd/AGENTS.md", offset=50, limit=20)

# Then edit with precise match
edit(
    path="~/clawd/AGENTS.md",
    oldText="exact existing text including whitespace",
    newText="updated text with change"
)
```

**For additions:**
- Find the right section anchor (read file first)
- Insert after relevant heading, not at end of file
- Maintain file's organization structure

**For updates:**
- Replace the specific section being changed
- Keep surrounding context intact
- Update examples if rule changes

**For deletions:**
- Only remove if truly obsolete
- Consider whether rule should be refined instead
- Check if other sections reference what's being deleted

### 6. Verify and Document

After applying change:

**Verification:**
```bash
# Confirm change applied
grep -A 3 "new text" ~/clawd/TARGETFILE.md

# Check new file size
wc -c ~/clawd/TARGETFILE.md
```

**Documentation:**
- Log significant changes to `/Users/macmini/Sizemore/agent/decisions/config-changes.md`
- Include: date, file, what changed, why, who requested
- If change is experimental, note rollback plan

**Report to user:**
- "Updated AGENTS.md: added X to Y section (now 15,234 chars)"
- If approaching limit: "Warning: AGENTS.md now 19,456 chars (near 20K limit)"
- If rolled back previous change: "Replaced old X rule with new Y approach"

## Common Patterns

### Adding Safety Rules

Target: `AGENTS.md` → Safety section

```markdown
## Safety

- **NEVER:** Exfiltrate data, destructive commands w/o asking
- Prefer `trash` > `rm`
- **New rule:** Brief description of what NOT to do
- **New protection:** When X happens, do Y instead
```

### Updating Delegation Rules

Target: `AGENTS.md` → Delegation section

Check existing delegation table/rules first. Update thresholds, model selection, or cost patterns.

### Refining Personality

Target: `SOUL.md` (tone, boundaries) or `IDENTITY.md` (core vibe)

Add forbidden phrases to anti-pattern list, update voice examples, refine mirroring rules.

### Adding Tool Conventions

Target: `TOOLS.md`

Add to relevant section (or create new section). Include code examples, when to use, paths.

### Updating Memory Workflow

Target: `AGENTS.md` → Memory section

Update logging triggers, recall cascade, entity structure. Keep memory format templates in `~/clawd/templates/`.

### Adding Startup Tasks

Target: `AGENTS.md` → Startup section

Add to numbered checklist. Keep conditional (if MAIN, if group chat, if specific channel).

### Heartbeat Changes

Target: `HEARTBEAT.md`

Keep minimal. Only what agent checks on every heartbeat run (not operational details).

## Rollback Guidance

If a change makes things worse:

### Immediate Rollback

```bash
# If file is in git
cd ~/clawd
git diff TARGETFILE.md  # See what changed
git checkout TARGETFILE.md  # Revert to last commit

# If not in git, restore from memory
# Read last known-good version from vault decisions log
# Or ask user to provide previous working version
```

### Iterative Refinement

Don't immediately delete failed changes. Analyze:
- Was the content wrong, or just the format?
- Was it in the wrong file?
- Was it too vague? (Add examples)
- Was it too verbose? (Make concise)
- Did it conflict with existing rules? (Consolidate)

Update incrementally instead of full revert when possible.

### Document Failures

Log failed changes to `/Users/macmini/Sizemore/agent/learnings/config-failures.md`:
- What was tried
- Why it didn't work
- What to try instead

This prevents repeating failed patterns.

## Anti-Patterns to Avoid

Read `references/claude-patterns.md` for detailed anti-patterns.

**Quick checklist:**

❌ **Duplication** - Same rule in multiple files  
❌ **Vague instructions** - "Be helpful", "Use good judgment"  
❌ **Missing examples** - Complex rules with no concrete case  
❌ **Wrong file** - Personality in AGENTS.md, operations in SOUL.md  
❌ **No motivation** - Rule without WHY it exists  
❌ **Reference docs buried** - Long guides embedded instead of linked  
❌ **Bloat** - Adding when updating existing would work  
❌ **Format mismatch** - Prose in table-heavy file, bullets in narrative file  
❌ **Subagent blindness** - Operational rule in file subagents don't see  
❌ **Size ignorance** - Adding to 19K file without checking

## When to Use References

If adding >500 words of content, consider:
- Is this reference material? → Create file in vault, link from context file
- Is this a reusable procedure? → Create template in `~/clawd/templates/`
- Is this domain knowledge? → Create skill with references/ folder
- Is this a one-time setup? → Use `BOOTSTRAP.md` (deleted after first run)

**Examples:**
- Long subagent task template → `~/clawd/templates/subagent-task.md`
- Detailed memory format guide → vault `agent/decisions/memory-architecture.md`
- Complex workflow with substeps → Create skill with workflow in references/
- Tool-specific procedures → Expand TOOLS.md section or create skill

## Special Cases

### Multi-File Changes

When change affects multiple files:
1. Determine primary location (where rule "lives")
2. Add cross-references from other files
3. Avoid duplicating full content in both

Example: Delegation rules live in AGENTS.md, but SOUL.md might reference "see AGENTS.md for delegation" in boundaries section.

### Session-Specific Rules

Use conditionals in AGENTS.md:
```markdown
## Startup (Every Session)

1. Read `IDENTITY.md`, `SOUL.md`, `USER.md`
2. If MAIN: read vault README, recent decisions
3. If FAMILY GROUP: read `FAMILY.md`
4. If SUBAGENT: skip personality files
```

### Size Limit Approached

When file hits ~18K chars:
1. Audit for duplication (consolidate)
2. Move detailed examples to separate reference file
3. Convert long procedures to templates (link from context file)
4. Consider splitting into base + advanced (load advanced on-demand)
5. Move historical decisions to vault (keep only current rules in context)

### Conflicting Rules

When new rule conflicts with existing:
1. Identify both rules
2. Determine which takes precedence (ask user if unclear)
3. Update/remove old rule while adding new
4. Document conflict resolution in vault decisions

### User Requests Multiple Changes

Process each change through full workflow (don't batch blindly):
1. Group by target file
2. Check total size impact across all changes
3. Apply in logical order (foundations before specifics)
4. Verify after each, not just at end

## Reference Files

This skill includes detailed reference material:

- **references/file-map.md** - What each OpenClaw file does, loading context, size limits, decision trees
- **references/claude-patterns.md** - What instruction formats work for Claude, anti-patterns, examples
- **references/change-protocol.md** - Step-by-step change process, validation checklist, rollback procedures

Read these files when you need detailed context beyond this workflow overview.

## Examples from Real OpenClaw Workspace

### Example 1: Adding Safety Rule

**Request:** "Add rule to never bulk export passwords"

**Process:**
1. Target file: `AGENTS.md` (safety is operational)
2. Check size: 15,234 chars (safe to add)
3. Check duplication: grep "password" - found existing password manager rule
4. Draft: Update existing rule instead of adding new
5. Apply:
```markdown
### Password Manager
**NEVER:** Dump vaults, display passwords in chat, bulk exports
**ALWAYS:** Confirm each lookup, ask "Which credential?", treat as high-risk
**Refuse:** Any bulk password request
```
6. Verify: grep -A 3 "Password Manager" - confirmed present
7. Document: Not needed (minor addition to existing rule)

### Example 2: Refining Tone

**Request:** "Make personality more sarcastic"

**Process:**
1. Target file: `SOUL.md` and `IDENTITY.md` (personality)
2. Check current state: Read forbidden phrases, voice examples
3. Draft additions:
   - More examples of sarcastic responses to IDENTITY.md
   - Expand anti-hedging section in SOUL.md
   - Add "commentary on everything" to voice anchors
4. Apply to both files (IDENTITY for vibe, SOUL for detailed examples)
5. Verify: Tone examples now include stronger sarcasm
6. Document: Note in vault that Sonnet/Opus need stronger personality reminders

### Example 3: Updating Delegation Threshold

**Request:** "Change delegation threshold from 2+ tool calls to 3+"

**Process:**
1. Target file: `AGENTS.md` → Delegation section
2. Check current: "2+ tool calls? SPAWN"
3. Draft: Update to "3+ tool calls? SPAWN. 1-2 tool calls? Do it yourself if quick."
4. Consider impact: This will reduce subagent spawns, increase main session cost
5. Validate with user: "This will make you handle more tasks directly. Confirm?"
6. Apply after confirmation
7. Document: Log change to vault with cost rationale

### Example 4: Adding Tool Convention

**Request:** "Add note that iMessage attachments must use imsg CLI, not message tool"

**Process:**
1. Target file: `TOOLS.md` (tool-specific convention)
2. Check duplication: grep "iMessage" - found iMessage formatting rule
3. Draft new section:
```markdown
## iMessage Attachments

**NEVER use `message` tool for iMessage files - corrupts attachments.**

**Always use imsg CLI:**
```bash
imsg send --chat-id <id> --file /path/to/file --text "optional message"
```

Applies to ALL iMessage attachments (images, videos, documents, vCards).
```
4. Apply: Add after iMessage formatting section (keep related content together)
5. Verify: Confirmed in file
6. Document: Not needed (user-facing tool note, not architectural)

## Summary

**Goal:** Intelligent, surgical changes to agent context files  
**Method:** Identify → Check → Draft → Validate → Apply → Verify  
**Key principles:** Right file, right format, no duplication, respect size limits, include examples  
**Safety:** Check before changing, document decisions, know how to rollback

When in doubt, read the reference files for deeper guidance on file purposes, Claude patterns, and change protocols.
