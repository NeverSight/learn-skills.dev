---
name: housekeeping
description: This skill should be used when users want to clean up, audit, or optimize their Claude configuration folders (~/.claude or .claude). It analyzes hooks, scripts, plugins, commands, and storage for token waste, redundancy, and optimization opportunities, then produces a prioritized action plan with before/after benefits.
arguments: scope
argument_hints:
  scope: "Scope to analyze: 'user' (~/.claude), 'project' (.claude), or 'all' (both). Default: user"
---

# Claude Housekeeping - Configuration Cleanup & Optimization

This skill performs comprehensive audits of Claude configuration folders to identify waste, redundancy, and optimization opportunities.

## Parameters

- **scope**: `user` (default) | `project` | `all`
  - `user`: Analyzes `~/.claude` (global user configuration)
  - `project`: Analyzes `.claude` in current working directory
  - `all`: Analyzes both locations

## Workflow

### Phase 1: Discovery - Leave No Stone Unturned

Systematically scan the target directory for all configuration artifacts:

#### 1.1 Hooks Analysis
```bash
# Find all hook files
find <target> -name "*.js" -path "*/hooks/*" -type f
find <target> -name "*.ts" -path "*/hooks/*" -type f
```

For each hook, analyze:
- **Token efficiency**: Does it inject large context on every invocation?
- **Execution frequency**: Pre-tool, post-tool, session hooks - how often does it fire?
- **Output size**: How much data does it add to context?
- **Redundancy**: Does it duplicate information available elsewhere?
- **Error handling**: Silent failures that waste processing?

#### 1.2 Commands Analysis
```bash
find <target> -name "*.md" -path "*/commands/*" -type f
```

For each command:
- **Usage patterns**: Is it ever invoked?
- **Token cost**: How large is the command definition?
- **Duplication**: Does it overlap with built-in or plugin commands?
- **Optimization**: Can prompts be more concise?

#### 1.3 Plugins Analysis
```bash
ls -la <target>/plugins/
```

Analyze:
- **Cache bloat**: Multiple versions cached? Old temp directories?
- **Unused plugins**: Installed but never invoked?
- **Duplicate functionality**: Multiple plugins doing same thing?
- **MCP server configs**: Orphaned or broken configurations?

#### 1.4 Storage Analysis
```bash
du -sh <target>/*
find <target> -type f -size +100k
find <target> -name "*.log" -o -name "*.jsonl"
```

Identify:
- **Log files**: Accumulating without rotation?
- **Cache directories**: Stale or oversized?
- **Session files**: Old sessions cluttering storage?
- **Backup files**: .bak, .backup, copy files?
- **Temp files**: Orphaned temporary artifacts?

#### 1.5 Settings & Configuration
```bash
cat <target>/settings.json
cat <target>/.mcp.json
cat <target>/CLAUDE.md
```

Check for:
- **Outdated settings**: Old model references, deprecated options?
- **MCP server bloat**: Too many servers configured?
- **CLAUDE.md size**: Is it too large for efficient context loading?
- **Duplicate configurations**: Same settings in multiple places?

#### 1.6 Rules & Agents
```bash
find <target> -path "*/rules/*" -type f
find <target> -path "*/agents/*" -type f
```

Analyze:
- **Rule conflicts**: Overlapping or contradictory rules?
- **Agent redundancy**: Multiple agents with similar purposes?
- **Token overhead**: Verbose rules that could be condensed?

### Phase 2: Analysis & Metrics

For each discovered item, calculate:

1. **Token Cost**
   - File size in characters → approximate token count (÷4)
   - Frequency of loading into context
   - Total token impact per session

2. **Storage Impact**
   - Disk space consumed
   - Growth rate (if logs/caches)

3. **Value Assessment**
   - Is this actively used?
   - Does it provide unique value?
   - Could it be consolidated with something else?

4. **Risk Rating**
   - SAFE: Can remove without any impact
   - LOW: Minimal risk, unlikely to affect functionality
   - MEDIUM: May affect some workflows, backup recommended
   - HIGH: Core functionality, careful review needed

### Phase 3: Action Plan Generation

Compile findings into a structured action plan:

```markdown
# Claude Housekeeping Report
**Scope**: [user/project/all]
**Analyzed**: [timestamp]
**Total Files Scanned**: [count]

## Executive Summary
- Total potential token savings: ~[X]k tokens/session
- Storage recoverable: [X] MB
- Items requiring attention: [count]

## Priority Actions

### 🔴 High Priority (Immediate token savings)
| Item | Current Impact | Action | Savings |
|------|---------------|--------|---------|
| [file/item] | [X] tokens/load | [action] | [benefit] |

### 🟡 Medium Priority (Optimization opportunities)
| Item | Current Impact | Action | Savings |
|------|---------------|--------|---------|

### 🟢 Low Priority (Nice to have)
| Item | Current Impact | Action | Savings |
|------|---------------|--------|---------|

## Detailed Findings

### Hooks ([count] found)
[Per-hook analysis with specific recommendations]

### Commands ([count] found)
[Per-command analysis]

### Plugins ([count] found)
[Plugin cache and configuration analysis]

### Storage ([size] total)
[Storage breakdown and cleanup opportunities]

### Configuration
[Settings optimization opportunities]

## Before/After Comparison

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Context overhead | [X] tokens | [X] tokens | -[X]% |
| Disk usage | [X] MB | [X] MB | -[X]% |
| Startup time | [estimated] | [estimated] | [improvement] |

## Recommended Actions

Select which actions to perform:
1. [ ] [Action 1 - description]
2. [ ] [Action 2 - description]
...
```

### Phase 4: Interactive Execution

After presenting the plan, wait for user selection:

1. **User selects items** by number or category
2. **Confirm before destructive actions** - especially for HIGH risk items
3. **Create backups** before removing anything with MEDIUM+ risk
4. **Execute incrementally** - one action at a time with verification
5. **Report results** after each action

## Common Optimization Patterns

### Hook Token Waste Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Large JSON injection | Every tool call adds 1000+ tokens | Cache in file, load on demand |
| Verbose logging | Debug logs in production hooks | Add log level controls |
| Duplicate context | Same info in multiple hooks | Consolidate to single source |
| Synchronous file reads | Reading files that don't exist | Add existence checks |

### Command Optimization Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Verbose prompts | 500+ word command definitions | Condense to essentials |
| Unused commands | Old experiments never removed | Archive or delete |
| Duplicate commands | Same function, different names | Consolidate |

### Storage Cleanup Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| Log accumulation | No rotation, grows forever | Add log rotation |
| Cache sprawl | Old plugin versions cached | Clean old versions |
| Orphaned files | Temp files, failed operations | Remove orphans |

## Safety Protocols

1. **Never delete without backup**: Create `.housekeeping-backup/` before removing
2. **Confirm high-risk actions**: Always ask before touching core configs
3. **Incremental changes**: One action at a time, verify after each
4. **Rollback capability**: Keep backup until user confirms success
5. **Dry-run option**: Show what would happen without doing it

## Usage Examples

```
/housekeeping                    # Analyze ~/.claude (default)
/housekeeping scope=project      # Analyze .claude in current project
/housekeeping scope=all          # Analyze both user and project
```

## Output Interpretation

- **Token savings**: Approximate reduction in context window usage per session
- **Storage savings**: Actual disk space recoverable
- **Risk level**: How likely the change is to affect functionality
- **Benefit ratio**: Savings vs effort to implement

When presenting findings, always show the comparative benefit so users can make informed decisions about which optimizations to pursue.
