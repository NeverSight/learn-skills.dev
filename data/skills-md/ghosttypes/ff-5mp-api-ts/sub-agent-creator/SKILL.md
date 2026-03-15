---
name: sub-agent-creator
description: Interactive sub-agent creation skill for Claude Code. Use when user wants to create a custom subagent or mentions needing a specialized agent for specific tasks. This skill guides the entire subagent creation process including identifier design, system prompt generation, skill/context selection, and writing properly formatted agent files to .claude/agents.
---

# Sub-Agent Creator

Interactive skill for creating Claude Code subagents. Guides the complete process: gathering requirements, designing the agent's purpose and persona, selecting helpful skills and documentation, and writing a properly formatted agent file to `.claude/agents/`.

## Critical Formatting Rules

Subagents MUST follow strict formatting or they will fail validation and not load:

| Rule | Requirement | Consequence |
|------|-------------|-------------|
| **Single-line description** | `description` must be one line, no `\n` | Validation failure |
| **No literal `\n`** | Use actual newlines in body, not `\n` escapes | Validation failure |
| **Valid colors only** | If specified: red, blue, green, yellow, purple, orange, pink, cyan | Agent won't load |
| **Valid models only** | `sonnet`, `opus`, `haiku`, or `inherit` | Validation failure |
| **Name format** | Lowercase letters, numbers, hyphens only | Validation failure |

### Examples of WRONG vs RIGHT

```yaml
# WRONG - Multi-line YAML syntax
description: |
  Expert code reviewer.
  Use after code changes.

# WRONG - Actual newlines in value
description: Expert code reviewer.
  Use after code changes.

# RIGHT - ONE continuous line
description: Expert code reviewer. Use proactively after code changes.
```

```yaml
# WRONG - Literal \n in body
---
name: test-runner
description: Run tests
---

You are a test runner.\nWhen invoked:\n1. Run tests\n2. Report results

# RIGHT - Actual newlines
---
name: test-runner
description: Run tests
---

You are a test runner.
When invoked:
1. Run tests
2. Report results
```

## Workflow

### 1. Understand Requirements

When this skill triggers, the user has described what kind of agent they want. First, extract:

- **Core purpose**: What should this agent do?
- **Trigger conditions**: When should Claude delegate to this agent?
- **Key capabilities**: What specific tasks will it handle?
- **Existing context**: Any relevant skills, docs, or project patterns?

### 2. Use AskUserQuestion for Details

Ask clarifying questions using the AskUserQuestion tool. Confirm:

- **Identifier**: What should the agent be named? (lowercase-with-hyphens)
- **Proactive usage**: Should this agent be used proactively or only on explicit request?
- **Model**: Default to `inherit`. Only suggest `haiku` for simple, fast tasks. ALWAYS confirm before using non-inherit models.
- **Color**: Auto-select from valid options (red, blue, green, yellow, purple, orange, pink, cyan) OR let user choose.

### 3. Identify Helpful Context

Search the workspace for:

**Relevant skills**: Check `.claude/skills/` and project skills that would help the agent.
```bash
ls .claude/skills/
```

**Relevant documentation**: Look for references files, CLAUDE.md, API docs, etc.
```bash
find . -name "*.md" -type f | head -20
```

### 4. Design the System Prompt

Using the agent creation architect framework (see `references/agent-creation-prompt.md`):

1. **Extract Core Intent** - Fundamental purpose and success criteria
2. **Design Expert Persona** - Compelling identity with domain knowledge
3. **Architect Instructions** - Behavioral boundaries, methodologies, edge cases
4. **Optimize for Performance** - Decision frameworks, quality control
5. **Create whenToUse Examples** - Concrete examples showing delegation

The system prompt should be in second person ("You are...", "You will...").

### 5. Write the Agent File

Write the agent file to `.claude/agents/<identifier>.md`:

```yaml
---
name: <identifier>
description: <single-line description with when to use>
model: inherit
---

<system prompt in markdown body>
```

**Default settings:**
- `model`: Always `inherit` unless user confirms otherwise
- `tools`: Omit to allow all tools (user preference: never restrict)
- `skills`: Include if specific skills would help the agent

### 6. Validate Before Completing

Run the validation script:
```bash
python .claude/skills/sub-agent-creator/scripts/validate_agent.py .claude/agents/<identifier>.md
```

Only proceed if validation passes. Fix any errors and re-validate.

## Agent File Template

```yaml
---
name: agent-identifier
description: Brief single-line description starting with what it does. Use proactively when [trigger condition].
model: inherit
skills:
  - relevant-skill-1
  - relevant-skill-2
---

You are an expert [domain] specialist.

When invoked:
1. [First step]
2. [Second step]
3. [Continue as needed]

Your approach:
- [Guideline 1]
- [Guideline 2]

For each [task], provide:
- [Output format 1]
- [Output format 2]

Focus on [core principle].
```

## Description Best Practices

The `description` field is Claude's primary signal for when to delegate. Include:

- **What the agent does**: "Expert code reviewer specializing in..."
- **When to use**: "Use proactively after writing code" or "Use when analyzing..."
- **Triggers**: Specific situations that should trigger delegation

Examples:
```yaml
description: Test execution specialist. Use proactively after writing tests or modifying test files.
description: Database query analyst. Use when needing to analyze data or generate reports from BigQuery.
description: Code archaeology expert. Use when exploring legacy codebases or understanding unfamiliar code.
```

## Resources

- **scripts/validate_agent.py** - Validates agent files for formatting errors
- **references/sub-agents-docs.md** - Complete Claude Code subagents documentation
- **references/agent-creation-prompt.md** - Agent creation architect system prompt framework

After creating an agent, verify it appears in `/agents` command output.
