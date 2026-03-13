---
name: evolving-config
description: >-
  Audit Claude Code configuration against latest features and best practices.
  Use when user says "evolve", "self-improve", "audit config", "what's new
  in claude code", "upgrade configuration", "check for improvements",
  "are we up to date".
user-invocable: true
model: sonnet
memory: project
context: fork
allowed-tools:
  - TaskCreate
  - TaskUpdate
  - TaskList
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - WebFetch
  - AskUserQuestion
  - mcp__perplexity-ask__perplexity_ask
argument-hint: "[--dry-run]"
---

# Evolve Configuration

Audit Claude Code config against latest capabilities. Conservative by default — says "no changes needed" when that's true.

**Use TaskCreate** to track these 6 phases:

1. Snapshot current configuration
2. Fetch latest capabilities
3. Research best practices
4. Gap analysis
5. Present report
6. Apply changes

---

## Phase 1: Snapshot Current Configuration

Read ALL config files in parallel:

```bash
# Glob these patterns
CLAUDE.md                           # Root instructions
.claude/CLAUDE.md                   # Project instructions
.claude/settings.json               # Settings + hooks
.claude/settings.local.json         # Local overrides
.claude/skills/*/SKILL.md           # All skills
.claude/agents/*.md                 # All agents (if present)
.claude/commands/**/*.md            # All commands (if present)
hooks/*                             # Hook scripts
```

Build inventory summary:

| Category    | Count | Details                       |
| ----------- | ----- | ----------------------------- |
| Skills      | N     | list names                    |
| Agents      | N     | list names                    |
| Commands    | N     | list names                    |
| Hooks       | N     | list events                   |
| MCP servers | N     | list names                    |
| Model refs  | list  | which models referenced where |

Note any staleness indicators (outdated model names, deprecated patterns).

---

## Phase 2: Fetch Latest Capabilities

Fetch the Claude Code changelog:

```
WebFetch(
  url="https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
  prompt="Extract ALL features, changes, and deprecations from the last 6 months. Group by: new features, configuration changes, breaking changes, new hook events, new settings, new CLI flags, new MCP capabilities, new agent types. Be thorough."
)
```

If WebFetch fails or returns insufficient data, note the gap and rely on Phase 3.

---

## Phase 3: Research Best Practices

Two targeted Perplexity queries:

**Query 1** — Features and configuration:

```json
mcp__perplexity-ask__perplexity_ask({
  "messages": [{ "role": "user", "content": "Claude Code CLI by Anthropic: what are the latest features, configuration options, best practices, and power user tips as of 2026? Include: hooks, skills, agents, MCP servers, settings.json options, CLAUDE.md patterns, team features, model routing, context management." }]
})
```

**Query 2** — Ecosystem and integrations:

```json
mcp__perplexity-ask__perplexity_ask({
  "messages": [{ "role": "user", "content": "Claude Code CLI advanced configuration 2026: MCP server recommendations, hook patterns, permission optimization, context fork strategies, agent orchestration patterns, skill design best practices. What are experienced users doing?" }]
})
```

If Perplexity returns cited URLs with high-value content, WebFetch top 2 for deeper details.

---

## Phase 4: Gap Analysis

Compare current config against latest capabilities. For EACH category below, produce findings:

### Audit Categories

| Category          | What to Check                                                                  |
| ----------------- | ------------------------------------------------------------------------------ |
| **Model routing** | Are model assignments optimal? New models available? Effort levels configured? |
| **Hooks**         | New hook events available? Async hooks? Hook v2 features?                      |
| **Skills**        | Stale patterns? New tool types to leverage? Missing `context: fork`?           |
| **Agents**        | New subagent types? Agent features (memory, skills)?                           |
| **MCP servers**   | New useful servers? Deprecated transports? OAuth improvements?                 |
| **Permissions**   | New permission syntax? Over-permissive rules? Missing deny rules?              |
| **Settings**      | New settings fields? Deprecated options? Sandbox improvements?                 |
| **CLAUDE.md**     | Outdated instructions? Stale references? Missing new patterns?                 |
| **Teams**         | New team features? Configuration improvements?                                 |
| **Commands**      | Deprecated command patterns? New frontmatter fields?                           |

### Classification Rules

For each finding, assign ONE rating:

| Rating             | Criteria                                        | Action           |
| ------------------ | ----------------------------------------------- | ---------------- |
| **STILL GOOD**     | Current config matches or exceeds best practice | No change needed |
| **DEPRECATED**     | Feature removed or replaced upstream            | Must update      |
| **WORTH ADOPTING** | Clear value, low disruption, proven stable      | Recommend        |
| **NICE-TO-HAVE**   | Minor improvement, some disruption              | Mention only     |
| **NOT YET**        | Too experimental or doesn't fit workflow        | Skip or note     |

**Critical rule**: Default classification is **STILL GOOD**. A finding must clear the bar: "Is this worth the disruption?" Changing working config has real cost — context relearning, potential breakage, testing overhead. Only promote to WORTH ADOPTING when the benefit clearly exceeds that cost.

**Cap**: Maximum 10 recommendations across WORTH ADOPTING + DEPRECATED. If more exist, prioritize by impact and note the overflow.

---

## Phase 5: Present Report

Format the report:

```markdown
## Configuration Audit Report

**Date**: {date}
**Changelog checked through**: {version or date}
**Sources**: {list: changelog, perplexity, docs URLs}

### What's Working Well (STILL GOOD)

- {explicit acknowledgment of things that don't need changing}
- {this section should be the longest — most config should be fine}

### Action Required (DEPRECATED)

- {breaking changes or removed features — empty is normal}

### Recommended Updates (WORTH ADOPTING)

- {high-value, low-disruption improvements}
- {each item: what to change, why, and estimated disruption}

### On Your Radar (NICE-TO-HAVE)

- {minor improvements that can wait}

### Not Yet (TOO EARLY)

- {experimental features, not ready for production config}

### Summary

- {X} areas reviewed — no changes needed
- {Y} updates recommended
- {Z} items informational
```

**STOP here.** Use `AskUserQuestion`:

| Header | Question                                      | Options                                                                                                      |
| ------ | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Action | How should we proceed with the audit results? | Apply all recommended (Recommended) / Select items to apply / Dry run only (show diffs) / Skip (report only) |

If `$ARGUMENTS` contains `--dry-run`: Skip the question, show diffs only, do not apply.

---

## Phase 6: Apply Changes

Based on user selection:

1. **Apply only approved items** — never sneak in extras
2. **Prefer Edit over Write** — modify existing files, don't recreate
3. **Show diff summary** after each change
4. **Verify** the change doesn't break existing config (quick sanity read)

If user selected "Dry run only": show what each edit would look like, then stop.

---

## Edge Cases

- **No changelog access**: Fall back to Perplexity-only research, note reduced confidence
- **No new features found**: Report "Configuration is up to date — no changes needed" — this is a valid, expected outcome
- **`--dry-run` flag in arguments**: Show full report, skip Phase 6
- **Too many suggestions**: Cap at 10, note overflow count
- **Perplexity unavailable**: Fall back to WebFetch of docs + changelog only
- **All findings are STILL GOOD**: Celebrate it — a well-maintained config is the goal

---
