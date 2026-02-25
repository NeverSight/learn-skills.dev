---
name: skill-exporter
description: Generate npx skills add commands to reproduce installed skills. Use when user wants to export, backup, share, or replicate their skills setup on another machine.
---

# Skill Exporter

Generate `npx skills add` commands from current installation.

## Workflow

Copy this checklist and track progress:

```
Export Skills:
- [ ] Step 1: Collect installation data
- [ ] Step 2: Parse and map agent names
- [ ] Step 3: Group by source and agent-set
- [ ] Step 4: Generate commands
```

### Step 1: Collect Installation Data

Run these commands:

```bash
npx skills ls -g
cat ~/.agents/.skill-lock.json
```

### Step 2: Parse and Map Agent Names

**Parse `npx skills ls -g` output:**

```
<skill-name> <path>
  Agents: <Agent1>, <Agent2>, ...
```

Extract skill name (first word of non-indented line) and agents (comma-separated after "Agents:").

**Map display names to CLI values:** See [references/agents.md](references/agents.md)

### Step 3: Group by Source and Agent-Set

**Lock file path:** `~/.agents/.skill-lock.json`

```json
{ "<skill-name>": { "source": "<owner/repo>", ... } }
```

Group skills sharing same source repo AND same agent set into one command.

### Step 4: Generate Commands

**Command format:**

```bash
npx skills add <source> -g -y -s <skill1> -s <skill2> -a <agent1> -a <agent2>
```

## Error Handling

- **Lock file missing**: Use `npx skills ls -g` only; source repo info will be unavailable
- **Skill not in lock file**: Skip or prompt user for source repo

## Example

**Input:**

```
docx ~/.agents/skills/docx
  Agents: Antigravity, Claude Code
pdf ~/.agents/skills/pdf
  Agents: Antigravity, Claude Code
```

**Lock:** `docx` and `pdf` both have `"source": "anthropics/skills"`

**Output:**

```bash
npx skills add anthropics/skills -g -y -s docx -s pdf -a antigravity -a claude-code
```
