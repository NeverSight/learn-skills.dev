---
name: memory-capture
description: Capture and organize memories, decisions, and learnings to a memories.md file. Use when you want to save context for future sessions.
---

# Memory Capture

Help users capture important decisions, preferences, and learnings to their memories file for future reference.

## When to Use

Invoke this skill when the user wants to:
- Record a decision they made
- Save a preference for future sessions
- Document something they learned
- Create a note about the project or codebase

## Memory Locations

- **Personal memories**: `~/.factory/memories.md` - preferences that apply across all projects
- **Project memories**: `.factory/memories.md` - decisions specific to the current project

## Capture Process

### Step 1: Understand What to Remember

Ask the user to clarify:
- What specifically should be remembered?
- Is this a personal preference or project-specific?
- What's the context (why is this worth remembering)?

### Step 2: Categorize the Memory

Common categories:

**For Personal Memories:**
- Code style preferences
- Tool preferences
- Communication style
- Workflow patterns

**For Project Memories:**
- Architecture decisions
- Design choices
- Domain knowledge
- Known issues
- Team conventions

### Step 3: Format the Entry

Use this format:

```markdown
### [Date]: [Short Title]
**Category**: [Decision/Preference/Learning/Context]
**Summary**: [One sentence description]
**Details**: [Full explanation if needed]
**Reasoning**: [Why this matters - optional]
```

For simpler entries:
```markdown
- [Date] [Category]: [Description]
```

### Step 4: Append to Memories File

Add the formatted entry to the appropriate memories file.

If the file doesn't exist, create it with proper structure:

**For Personal (~/.factory/memories.md):**
```markdown
# My Development Memory

## Preferences
[preferences entries]

## Learnings
[learning entries]
```

**For Project (.factory/memories.md):**
```markdown
# Project Memory

## Decisions
[decision entries]

## Context
[context entries]

## Known Issues
[issue entries]
```

## Example Captures

### Architecture Decision

User says: "Remember that we chose PostgreSQL over MongoDB for this project"

Capture as:
```markdown
### 2024-02-15: Database Selection
**Category**: Architecture Decision
**Summary**: Chose PostgreSQL over MongoDB for the primary database
**Reasoning**: 
- Strong relational data model fits our domain
- ACID compliance needed for financial transactions
- Team has more PostgreSQL experience
- Better tooling for complex queries and reporting
```

### Personal Preference

User says: "I prefer early returns over nested conditionals"

Capture as:
```markdown
## Code Style Preferences

- [2024-02-15] I prefer early returns over nested conditionals for better readability
```

### Domain Knowledge

User says: "Note that free tier users are limited to 3 team members"

Capture as:
```markdown
### Business Rules

- Free tier: Limited to 3 team members
- Pro tier: Up to 20 team members
- Enterprise: Unlimited team members
```

### Technical Context

User says: "The auth service has a known issue with refresh tokens (#234)"

Capture as:
```markdown
## Known Issues

- [ ] Auth refresh token race condition (#234) - Can cause session loss during concurrent requests
```

## Tips

1. **Keep entries scannable** - Use headers and bullet points
2. **Include dates** - Context matters, decisions may change
3. **Note the "why"** - Future you will want to know
4. **Link to issues/PRs** - For traceability
5. **Review periodically** - Archive outdated memories

---

## Alternative Implementations

This skill is one of three ways to capture memories. Choose based on your workflow:

### Option 1: This Skill (Interactive)

Droid invokes this skill when you ask to remember something. Best when you want help categorizing and formatting memories.

**Usage:** "Remember that we chose PostgreSQL for ACID compliance"

### Option 2: Hook (Automatic)

A [UserPromptSubmit hook](/cli/configuration/hooks-guide) that triggers on phrases like "remember this:". Best for zero-friction capture.

See the [Memory Management guide](/guides/power-user/memory-management#automatic-memory-capture) for the hook implementation.

**Usage:** "Remember this: we use the repository pattern for data access"

### Option 3: Custom Slash Command (Manual)

A [custom slash command](/cli/configuration/custom-slash-commands) for quick, consistent capture.

Create `~/.factory/commands/remember.md`:

```markdown
---
description: Save a memory to your memories file
argument-hint: <what to remember>
---

Add this to my memories file (~/.factory/memories.md):

$ARGUMENTS

Format it appropriately based on whether it's a preference, decision, or learning. Include today's date.
```

**Usage:** `/remember we chose PostgreSQL for ACID compliance`

### Comparison

| Approach | Trigger | Best For |
|----------|---------|----------|
| **Skill** | Droid decides | Interactive categorization |
| **Hook** | Automatic on keywords | Zero-friction capture |
| **Slash Command** | You type `/remember` | Quick manual capture |
