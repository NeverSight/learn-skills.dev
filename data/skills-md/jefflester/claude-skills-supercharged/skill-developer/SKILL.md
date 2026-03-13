---
name: skill-developer
description: Create and manage Claude Code skills following Anthropic best practices. Use when creating new skills, modifying skill-rules.json, understanding trigger patterns, working with hooks, debugging skill activation, or implementing progressive disclosure. Covers skill structure, YAML frontmatter, keyword triggers, hook mechanisms (UserPromptSubmit), session tracking, and the 500-line rule.
---

# Skill Developer Guide

## Purpose

Comprehensive guide for creating and managing skills in Claude Code with auto-activation system, following Anthropic's official best practices including the 500-line rule and progressive disclosure pattern.

## Domain Skill for Skill System

This is a domain skill for the skills system itself. It's automatically loaded when you work with skills.

**This skill covers:**

- The 500-line rule (max 5 files > 500 lines, none > 600 lines)
- TOC and line number prohibition (never add these to skills)
- When skills need updates (new dirs, patterns, docs, triggers)
- Self-healing mechanisms (pre-commit hook, /wrap checklist)
- Progressive disclosure patterns (main file → resource files)

**Use this skill explicitly when:**

- Creating or modifying any skill
- Debugging skill activation issues
- Understanding the skills system architecture

## When to Use This Skill

Automatically activates when you mention:

- Creating or adding skills
- Modifying skill triggers or rules
- Understanding how skill activation works
- Debugging skill activation issues
- Working with skill-rules.json
- Hook system mechanics
- Claude Code best practices
- Progressive disclosure
- YAML frontmatter
- 500-line rule

## Related Skills

This skill helps create and manage all other skills. When building skills, reference:

- **testing-strategy** - Skills should be tested with real scenarios before extensive documentation

## Relationship to CLAUDE.md

**Division of Responsibilities:**

- **CLAUDE.md**: Global project context, high-level architecture, universal style rules
- **Skills**: Domain-specific detailed guidance, patterns, procedures (triggered by context)
- **skill-developer**: Domain skill that guides the skills system and explains its relationship to CLAUDE.md

**When to Update:**

- Global style rules (numpy docstrings, no emojis, use venv) → Update CLAUDE.md
- Domain patterns/practices (test patterns, architecture design) → Update relevant skill
- Skill system mechanics (triggers, hooks, 500-line rule) → Update skill-developer

**Integration:**

- CLAUDE.md references skills for detailed guidance (1-line pointers)
- Skills don't reference CLAUDE.md (avoid circular dependencies)
- skill-developer explains the complete hierarchy (this section)

**Progressive Disclosure Hierarchy:**

```
CLAUDE.md (Global Context)
    ↓ references
Skills (Domain Guidance)
    ↓ maintained by
skill-developer (Domain Skill)
```

______________________________________________________________________

## System Overview

The skills system uses **automatic injection** to seamlessly provide domain-specific context when you need it.

**Key concepts:**

- **Domain skills** (e.g., python-best-practices, skill-developer): Automatically injected when detected based on prompt keywords and AI intent analysis (autoInject: true)
- **Guardrail skills** (e.g., api-security): Enforce critical best practices, automatically injected when detected
- **Automatic detection & injection**: Skills detected via AI-powered intent analysis and immediately loaded into context - no manual intervention needed

**For complete details**, see [two-tier-system.md](resources/two-tier-system.md):

- Skill detection mechanism
- Automatic skill detection and injection
- Hook architecture and flow
- Workflow examples and scenarios
- Session state management

______________________________________________________________________

## Skill Types

### 1. Guardrail Skills

**Purpose:** Enforce critical best practices that prevent errors

**Characteristics:**

- Type: `"guardrail"`
- Automatically injected when detected (autoInject: true)
- Prevent common mistakes (column names, critical errors)
- Session-aware (only inject once per conversation)

**Examples:**

- `database-verification` - Verify table/column names before Prisma queries
- `frontend-dev-guidelines` - Enforce React/TypeScript patterns

**When to Use:**

- Mistakes that cause runtime errors
- Data integrity concerns
- Critical compatibility issues

### 2. Domain Skills

**Purpose:** Provide comprehensive guidance for specific areas

**Characteristics:**

- Type: `"domain"`
- Advisory, not mandatory
- Topic or domain-specific
- Comprehensive documentation
- Automatically injected when detected (autoInject: true)

**Examples:**

- `backend-dev-guidelines` - Node.js/Express/TypeScript patterns
- `frontend-dev-guidelines` - React/TypeScript best practices
- `error-tracking` - Sentry integration guidance

**When to Use:**

- Complex systems requiring deep knowledge
- Best practices documentation
- Architectural patterns
- How-to guides

______________________________________________________________________

## Creating New Skills

**5-step process:**

1. Create SKILL.md with YAML frontmatter
1. Add to skill-rules.json with triggers
1. Test detection (UserPromptSubmit hook)
1. Refine patterns based on results
1. Keep under 500 lines with progressive disclosure

**For complete step-by-step guide**, see [skill-creation-guide.md](resources/skill-creation-guide.md):

- File templates and naming conventions
- skill-rules.json configuration
- Trigger testing commands
- Pattern refinement strategies
- Best practices and common mistakes

______________________________________________________________________

## CRITICAL: The 500-Line Rule

**Absolute Limits for ALL Skill Markdown Files:**

- ✅ **Target**: ALL skill files under 500 lines
- ⚠️ **Warning Zone**: Only **5 files maximum** can breach 500 lines across entire skills system (~50 files)
- 🚫 **HARD LIMIT**: **NO file should EVER breach 600 lines**

**Why This Matters:**

- Agents process files linearly - long files waste tokens and context
- 500 lines is the sweet spot for focused, scannable content
- Progressive disclosure (main file → resource files) is more effective than one giant file

**Enforcement Strategy:**

- If approaching 500 lines → **STOP** and extract content to resource files
- If already > 500 lines → Refactor immediately unless you can justify it's in the top 5 most important files
- If approaching 600 lines → **MANDATORY** refactor, no exceptions

**How to Stay Under 500:**

1. Move detailed examples to `resources/` subdirectory
1. Extract deep-dive content to topic-specific resource files
1. Use concise summaries in main SKILL.md, point to resources for details
1. Remove redundancy and wordiness

______________________________________________________________________

## FORBIDDEN: TOCs and Line Number References

**NEVER include in skill markdown files:**

- ❌ **Table of Contents (TOC)** - Bloat for agents, not useful for scanning
- ❌ **Line number references** (e.g., "see line 42") - Change too frequently, create maintenance burden
- ❌ **Heading navigation links** - Agents can scan headings natively

**Why TOCs Are Harmful:**

- Add 10-50 lines of noise
- Agents don't benefit from them (they scan headings natively)
- Become stale when structure changes
- Waste precious lines toward 500-line limit

**Instead:**

- ✅ Use clear, descriptive section headings
- ✅ Use anchor text for cross-references (e.g., "See patterns-library.md")
- ✅ Keep files under 500 lines so navigation is unnecessary
- ✅ Use progressive disclosure (link to resource files for deep dives)

______________________________________________________________________

______________________________________________________________________

## Session State & Deduplication

**Automatic session tracking prevents duplicate injection:**

1. **Session tracking**: Skills are injected once per conversation; subsequent detections reuse already-loaded skills
1. **State file**: `.claude/hooks/state/{conversation_id}-skills-suggested.json` tracks loaded skills
1. **Manual loading**: If `autoInject: false` (meta-skills), use `Skill("skill-name")` tool manually

______________________________________________________________________

## Testing & Validation

Test your skills with multiple real-world scenarios before extensive documentation. Verify triggers activate correctly and content provides useful guidance.

______________________________________________________________________

## Reference Files

For detailed information on specific topics, see:

### [trigger-types.md](resources/trigger-types.md)

Complete guide to keyword triggers:

- Keyword triggers (explicit topic matching)
- Best practices and examples
- Common pitfalls and testing strategies

### [skill-rules-reference.md](resources/skill-rules-reference.md)

Complete skill-rules.json schema:

- Full TypeScript interface definitions
- Field-by-field explanations
- Complete guardrail skill example
- Complete domain skill example
- Validation guide and common errors

### [hook-mechanisms.md](resources/hook-mechanisms.md)

Deep dive into hook internals:

- UserPromptSubmit flow (detailed)
- Exit code behavior table (CRITICAL)
- Session state management
- Performance considerations

### [patterns-library.md](resources/patterns-library.md)

Ready-to-use pattern collection:

- Keyword pattern library
- Organized by use case
- Copy-paste ready

### [two-tier-system.md](resources/two-tier-system.md)

Complete two-tier architecture guide:

- Meta-skills vs domain skills
- Automatic skill detection
- Hook flow and enforcement
- Workflow examples
- Session state management

### [skill-creation-guide.md](resources/skill-creation-guide.md)

Step-by-step skill creation:

- File templates and structure
- skill-rules.json configuration
- Trigger testing
- Pattern refinement
- Best practices and common mistakes

______________________________________________________________________

## Quick Reference

**Create New Skill:**

1. Create SKILL.md with frontmatter → 2. Add to skill-rules.json → 3. Test triggers → 4. Refine → 5. Keep < 500 lines

**Critical Rules:**

- ✅ 500-line limit (max 5 files can breach, none > 600)
- ✅ Progressive disclosure (use resource files)
- ✅ NO TOCs or line numbers (forbidden)
- ✅ Test before documenting (3+ scenarios)

**For Details:** See [trigger-types.md](resources/trigger-types.md), [hook-mechanisms.md](resources/hook-mechanisms.md)

______________________________________________________________________

## Self-Healing & Skill Maintenance

### Automated Skill Health Checks

The skills system includes automated maintenance to prevent skill drift:

**1. Pre-commit Hook - Skill Reference Validator**

- **Script**: `scripts/pre-commit/validate_skill_references.py`
- **Runs on**: Changes to skills, internal docs, or src/ files
- **Validates**:
  - All file links in SKILL.md point to existing files (prevents broken refs)
  - New internal docs not yet referenced by skills (suggestions)
- **Exit behavior**: Fails on broken links, warns on missing references

**2. Manual Checklist - /wrap Command**

When wrapping up work, the `/wrap` command includes a skill update checklist:

- New constants/utilities in shared modules → Update code-reuse patterns
- New docs in project documentation → Update skill resource file links
- New patterns/features → Update promptTriggers keywords

### Skill Update Workflow

**When code changes:**

1. Pre-commit hook catches broken skill references (automatic)
1. Pre-commit hook suggests new patterns to add (informational)
1. `/wrap` command reminds you to check skills (manual)
1. Review `.claude/skills/` for affected skills
1. Update skill-rules.json or SKILL.md as needed

**Common updates:**

- **New constants/utilities in shared modules**: Update skill references and patterns
- **New doc**: Add link to relevant skill's resources section
- **New keyword**: Add to promptTriggers.keywords in skill-rules.json

### Best Practices for Skill Health

✅ Run `/wrap` at end of sessions to check for skill updates
✅ Trust pre-commit warnings about unreferenced docs
✅ Keep skill-rules.json in sync with codebase structure
✅ Update skill descriptions when adding new trigger keywords
✅ Test skills after updates to verify triggers still work

______________________________________________________________________

## Related Files

**Configuration:**

- `.claude/skills/skill-rules.json` - Master configuration
- `.claude/hooks/state/` - Session tracking

**Hooks:**

- `.claude/hooks/skill-activation-prompt.ts` - UserPromptSubmit
- `.claude/hooks/error-handling-reminder.ts` - Stop event (gentle reminders)

**All Skills:**

- `.claude/skills/*/SKILL.md` - Skill content files

______________________________________________________________________

**Skill Status**: COMPLETE - Restructured following Anthropic best practices ✅
**Line Count**: < 500 (following 500-line rule) ✅
**Progressive Disclosure**: Reference files for detailed information ✅

**Next**: Create more skills, refine patterns based on usage
