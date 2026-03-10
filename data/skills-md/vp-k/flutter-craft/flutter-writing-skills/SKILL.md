---
name: flutter-writing-skills
description: Use when creating new skills for flutter-craft or editing existing skills
---

# Writing Flutter-Craft Skills

## Overview

Create new skills for flutter-craft that follow the established patterns and integrate with the skill system.

**Announce at start:** "I'm using the flutter-writing-skills skill to create a new skill."

## Skill Structure

Every skill needs:

```
skills/
└── skill-name/
    └── SKILL.md
```

## SKILL.md Format

```markdown
---
name: skill-name
description: Use when [trigger condition] - [what it does]
---

# Skill Title

## Overview

[1-2 sentence description of what this skill does]

**Core principle:** [The key rule this skill enforces]

**Announce at start:** "I'm using the [skill-name] skill to [purpose]."

## When to Use

[Clear criteria for when to trigger this skill]

## The Process

[Step-by-step workflow]

## [Domain-Specific Sections]

[Add sections relevant to the skill's domain]

## Red Flags

**Never:**
- [Things to avoid]

**Always:**
- [Things to ensure]

## REQUIRED SUB-SKILL (if applicable)

After completing this skill, you MUST invoke:
→ **flutter-craft:[next-skill]**

## Integration

**Called by:** [Which skills trigger this one]
**Pairs with:** [Related skills]
```

## Frontmatter Rules

The frontmatter is critical - it's how Claude Code discovers skills:

```yaml
---
name: skill-name           # kebab-case, unique
description: Use when...   # Must start with "Use when"
---
```

**Description format:**
- Start with "Use when [trigger]"
- Add " - [what it does]" after trigger
- Be specific about the trigger condition

**Examples:**
```yaml
# Good
description: Use when implementing Flutter features - follows Clean Architecture layer order

# Bad (too vague)
description: Helps with Flutter development
```

## Flutter-Craft Skill Conventions

### Naming

- Use `flutter-` prefix for Flutter-specific skills
- Use kebab-case: `flutter-feature-name`
- Be descriptive but concise

### Core Principles

Include a **Core principle** that captures the essence:
- "Evidence before claims, always"
- "Fresh subagent per task + two-stage review"
- "Domain → Data → Presentation layer order"

### Announce Pattern

Skills should announce themselves:
```
"I'm using the [skill-name] skill to [action]."
```

This helps users understand which skill is active.

### REQUIRED SUB-SKILL

If the skill MUST be followed by another skill:

```markdown
## REQUIRED SUB-SKILL

After completing brainstorming, you MUST invoke:
→ **flutter-craft:flutter-planning**

This is NOT optional. The workflow is incomplete without planning.
```

### Flutter-Specific Content

Include Flutter commands where relevant:
```bash
flutter analyze
flutter test
flutter build apk --debug
flutter pub get
flutter pub run build_runner build
```

## Testing Your Skill

### 1. Syntax Check

```bash
# Read the skill file
cat skills/my-skill/SKILL.md

# Check frontmatter is valid
head -5 skills/my-skill/SKILL.md
```

### 2. Trigger Test

Verify the skill triggers correctly:
1. Start a new Claude Code session
2. Describe a scenario matching the trigger
3. Check if Claude invokes the skill

### 3. Workflow Test

Run through the complete workflow:
1. Follow every step in the process
2. Check REQUIRED SUB-SKILLs are invoked
3. Verify integration with other skills

## Skill Categories

### Workflow Skills (Core)
- Process-oriented
- Have clear steps
- Often have REQUIRED SUB-SKILLs
- Examples: brainstorming, planning, executing

### Verification Skills
- Focus on checking/validating
- Include specific commands
- Examples: verification, debugging

### Utility Skills
- Support other skills
- May be invoked by multiple skills
- Examples: worktrees, parallel-agents

### Review Skills
- Handle feedback loops
- Two-way communication
- Examples: review-request, review-receive

## Common Mistakes

**Vague trigger:**
```yaml
# Bad
description: Use for Flutter stuff

# Good
description: Use when starting a new Flutter feature - explores requirements and designs before implementation
```

**Missing announce:**
```markdown
# Bad - no announcement
## Overview
This skill helps with...

# Good
**Announce at start:** "I'm using the flutter-brainstorming skill to design this feature."
```

**No verification steps:**
```markdown
# Bad - no verification
After implementation, you're done.

# Good
After implementation, run:
$ flutter analyze
$ flutter test
```

## Checklist for New Skills

- [ ] Frontmatter has valid name and description
- [ ] Description starts with "Use when"
- [ ] Has "Announce at start" instruction
- [ ] Has clear "When to Use" section
- [ ] Has step-by-step "Process" section
- [ ] Includes Flutter-specific commands where relevant
- [ ] Has "Red Flags" section
- [ ] REQUIRED SUB-SKILL documented if applicable
- [ ] Tested trigger in Claude Code session
- [ ] Tested full workflow
