---
name: bench-new-skill
description: Create new skills for the bench-skills repo following all conventions. Use when the user says "create a new skill", "add a skill", "new slash command", or wants to extend bench-skills with additional capabilities.
allowed-tools: ["Read", "Glob", "Grep", "Write", "AskUserQuestion", "Bash"]
---

# /bench-new-skill — Create New Skills

Scaffold new skills following established conventions, the official [Claude Code skills spec](https://code.claude.com/docs/en/skills), and Anthropic's [Complete Guide to Building Skills](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf).

## When to Use

- User wants to create a new skill (anywhere — global, project-local, or bench-skills repo)
- User says "create a new skill", "add a skill", "new slash command"
- User wants to create a plugin (see [references/plugin-guide.md](references/plugin-guide.md))

## Principles

1. **Start with use cases, not code.** Define 2-3 concrete use cases before writing anything. See [references/anthropic-guide-insights.md](references/anthropic-guide-insights.md) for the use case template.
2. **Description = `[What it does] + [When to use it] + [Key capabilities]`.** Must include BOTH what and when. Under 1024 chars. No XML tags. Include specific trigger phrases users would say.
3. **Include only what Claude doesn't already know.** Don't teach Claude how to write code — teach it your specific process, conventions, and standards.
4. **Be specific and actionable.** Vague instructions like "validate the data" get ignored. Explicit instructions like "Run `scripts/validate.py --input {file}`" get followed.
5. **Self-contained skills.** Each skill directory must work independently when installed.
6. **Progressive disclosure.** Keep SKILL.md focused on core instructions (under 300 lines / 5,000 words). Move detailed docs to `references/` and link to them.
7. **Right invocation model.** Decide upfront: should the user invoke this, Claude invoke it, or both? Use `disable-model-invocation` and `user-invocable` accordingly.
8. **Support arguments when appropriate.** If the skill operates on a target (file, PR number, issue), use `$ARGUMENTS` and add an `argument-hint`.
9. **No README.md inside skill folders.** All documentation goes in SKILL.md or references/.

## Process

### Step 1: Understand the Skill

Ask the user:

```
AskUserQuestion:
  question: "What should this skill do? Give me 2-3 examples of what you'd say to trigger it."
```

From their response, identify:
- **Use cases** — Define 2-3 concrete scenarios (Use Case → Trigger → Steps → Result)
- **Trigger phrases** — What the user would say to invoke this
- **Core process** — What steps the skill should follow
- **Output** — What the skill produces
- **Skill category** — Document/Asset Creation, Workflow Automation, or MCP Enhancement (see [references/anthropic-guide-insights.md](references/anthropic-guide-insights.md))
- **Agents needed** — Does it need parallel subagents? For what?

### Step 2: Choose Save Location

Ask the user where the skill should be saved:

```
AskUserQuestion:
  question: "Where should this skill be saved?"
  header: "Location"
  options:
    - label: "bench-skills repo (Recommended)"
      description: "Save to ~/bench-skills/skills/{name}/ — part of the shared skill collection, installable via npx skills add"
    - label: "Global personal"
      description: "Save to ~/.claude/skills/{name}/ — available in all your projects, personal use"
    - label: "Project-local"
      description: "Save to .claude/skills/{name}/ in the current project — scoped to this repo only"
    - label: "Plugin"
      description: "Package as a distributable plugin — for sharing across teams or community"
```

Use the chosen location for all file creation in later steps. If "Plugin" is selected, see [references/plugin-guide.md](references/plugin-guide.md).

### Step 3: Name the Skill

Follow the `{area}-{name}` convention:

| Area | For |
|------|-----|
| `engineer-` | Engineering workflow (plan, build, review) |
| `product-` | Product management (specs, requirements) |
| `security-` | Security auditing and best practices |
| `knowledge-` | Documentation and learning capture |
| `bench-` | Meta skills for bench-skills itself |

Suggest a name and confirm with the user. **Critical rules**: kebab-case only, no spaces/underscores/capitals, no "claude" or "anthropic" in the name.

### Step 4: Choose Content Type and Invocation Model

**Content type** — Determines what goes in SKILL.md:
- **Reference content**: Knowledge Claude applies to current work (conventions, patterns, style guides). Runs inline so Claude can use it alongside conversation context.
- **Task content**: Step-by-step instructions for a specific action (deployments, commits, code generation). Often invoked manually with `/skill-name`.

**Invocation model** — Who triggers the skill:

| Setting | User invokes | Claude invokes | Best for |
|---------|-------------|---------------|----------|
| Default (no flags) | Yes | Yes | General-purpose skills |
| `disable-model-invocation: true` | Yes | No | Workflows with side effects (deploy, commit, send messages) |
| `user-invocable: false` | No | Yes | Background knowledge (legacy-system-context, coding-standards) |

Ask the user which model fits their skill.

### Step 5: Design Arguments and Dynamic Context

**Arguments** — If the skill operates on a target, use `$ARGUMENTS`:
- `$ARGUMENTS` — All arguments as a string
- `$ARGUMENTS[0]`, `$ARGUMENTS[1]`, or shorthand `$0`, `$1` — Positional access
- `${CLAUDE_SESSION_ID}` — Current session ID (for logging/correlation)
- Add `argument-hint: [issue-number]` to show hints during autocomplete

**Dynamic context** — Use `!`command`` to inject live data before Claude sees the prompt:
```yaml
## Context
- Current branch: !`git branch --show-current`
- Changed files: !`git diff --name-only`
```
The shell commands run first; their output replaces the placeholder.

### Step 6: Decide on Execution Context

**Inline (default)** — Skill runs in the user's conversation. Best for reference content and skills that need conversation history.

**Forked (`context: fork`)** — Skill runs in an isolated subagent. The skill content becomes the subagent's prompt (no access to conversation history). Best for:
- Tasks that produce a lot of output
- Skills that shouldn't see conversation context
- Read-only research (use `agent: Explore`)
- Planning tasks (use `agent: Plan`)

```yaml
---
context: fork
agent: Explore    # or Plan, general-purpose, or a custom agent name
---
```

Only use `context: fork` when the skill contains an explicit task. If it's just guidelines/conventions, the subagent won't have an actionable prompt.

### Step 7: Scaffold the Skill

Create the skill directory in the location chosen in Step 2:

```
# bench-skills repo:
~/bench-skills/skills/{skill-name}/

# Global personal:
~/.claude/skills/{skill-name}/

# Project-local:
.claude/skills/{skill-name}/
```

Each skill directory contains:
```
{skill-name}/
├── SKILL.md              # Required — the main skill file
└── references/           # Only if needed for large templates/catalogs
    └── {reference}.md
```

Write SKILL.md with this structure:

```markdown
---
name: {skill-name}
description: {triggering conditions — focus on when/why, not what}
allowed-tools: [{tools needed}]
# Optional fields — include only those that apply:
# argument-hint: [{hint}]
# disable-model-invocation: true
# user-invocable: false
# context: fork
# agent: {agent-type}
# model: {model-name}
---

# /{skill-name} — {Short Title}

{One sentence explaining what this skill does.}

## When to Use

- {Trigger condition 1}
- {Trigger condition 2}
- {Trigger condition 3}

## Process

### Step 1: {First Step}
{Instructions — use $ARGUMENTS where appropriate}

### Step 2: {Second Step}
{Instructions}

...

## Output

{What the skill produces and where it's saved.}

## Next Steps

{What to do after running this skill. Link to other skills.}
```

**Supporting files** — If the skill needs large reference material, templates, or scripts:
- Keep SKILL.md focused on the essentials and navigation
- Put detailed content in `references/` files
- Reference them from SKILL.md: `See [references/catalog.md](references/catalog.md) for full details.`
- Scripts go in `scripts/` and can be in any language

### Step 8: Validate

Check the skill against conventions and the [Anthropic guide checklist](references/anthropic-guide-insights.md):
- [ ] Name follows `{area}-{name}` pattern (kebab-case, no spaces/capitals, no "claude"/"anthropic")
- [ ] Description follows `[What it does] + [When to use it]` formula, under 1024 chars
- [ ] Description includes specific trigger phrases users would actually say
- [ ] No XML tags (< >) anywhere in frontmatter
- [ ] SKILL.md under 300 lines / 5,000 words (large content in `references/`)
- [ ] No README.md inside skill folder
- [ ] Instructions are specific and actionable (not vague)
- [ ] Steps are numbered and actionable
- [ ] Error handling / troubleshooting included where appropriate
- [ ] Self-contained (no dependencies on shared files)
- [ ] `allowed-tools` includes only tools actually used
- [ ] Invocation model matches intent (`disable-model-invocation` / `user-invocable`)
- [ ] `$ARGUMENTS` used if skill operates on a target; `argument-hint` set
- [ ] If `context: fork` is used, skill contains an explicit task (not just guidelines)
- [ ] Frontmatter only includes fields that apply (see [references/frontmatter-reference.md](references/frontmatter-reference.md))
- [ ] Tested: triggers on obvious tasks, paraphrased requests, and does NOT trigger on unrelated topics

### Step 9: Consider Plugin Packaging

Ask the user if this skill should be part of a **plugin** instead of a standalone skill. Use a plugin when:
- The skill needs to be shared with a team or community
- It should work across multiple projects
- It bundles multiple skills, agents, hooks, or MCP servers together
- It benefits from versioned releases

If yes, see [references/plugin-guide.md](references/plugin-guide.md) for the plugin creation process.

If no, proceed with standalone installation.

### Step 10: Install

Installation depends on the save location chosen in Step 2:

**bench-skills repo:** Create a symlink directly to the repo so edits are live:
```bash
ln -s /Users/elliottjacobs/bench-skills/skills/{skill-name} ~/.claude/skills/{skill-name}
```
Verify: `ls -la ~/.claude/skills/{skill-name}`

**Global personal:** Already available — saved directly to `~/.claude/skills/`.

**Project-local:** Already available — saved directly to `.claude/skills/`.

**Plugin:** Test with `claude --plugin-dir ./my-plugin`. See [references/plugin-guide.md](references/plugin-guide.md).

**After install**, tell the user to start a new conversation and test with the trigger phrases identified in Step 1.

## Skill Design Checklist

Before finalizing, verify:

1. **Did you define 2-3 concrete use cases?** If you can't articulate specific scenarios, the skill isn't ready.
2. **Would this be triggered naturally?** If the description requires users to know specific phrases, it's too narrow. If it triggers on everything, it's too broad. Test both directions.
3. **Is this distinct from existing skills?** Check that it doesn't overlap with: engineer-plan, engineer-plan-review, engineer-work, engineer-review, product-brainstorm, product-prd, product-tech-spec, product-naming, security-audit, knowledge-compound.
4. **Is this teaching Claude something new?** If Claude already knows how to do this without special instructions, the skill may not be needed. Skills capture *how Claude should do it*, not *what Claude can do*.
5. **Is this the right granularity?** A skill should be a complete workflow, not a single step. But it shouldn't try to do everything either.
6. **Are the instructions specific and actionable?** Vague instructions get ignored. Every step should tell Claude exactly what to do, not just what to consider.
7. **Is the invocation model right?** Side-effect skills should be user-only. Background knowledge should be Claude-only. General skills can be both.
8. **Plugin or standalone?** If sharing across projects/teams, consider a plugin.

## Additional Resources

- For patterns, testing, troubleshooting, and success criteria from the official guide, see [references/anthropic-guide-insights.md](references/anthropic-guide-insights.md)
- For complete frontmatter field catalog, see [references/frontmatter-reference.md](references/frontmatter-reference.md)
- For plugin creation guidance, see [references/plugin-guide.md](references/plugin-guide.md)
- Official docs: [Skills](https://code.claude.com/docs/en/skills) | [Plugins](https://code.claude.com/docs/en/plugins)
- Anthropic guide: [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
