---
name: claude-skill-prereq-audit
description: >
  Scan skills for prerequisite tools, MCP servers, and auth requirements,
  then check if everything is installed and authenticated. Offers to fix issues.
  Use when setting up a new machine, after installing skills, or to verify your
  environment. Triggers: "check prerequisites", "skill prereqs", "are my tools installed",
  "verify skill dependencies", "/claude-skill-prereq-audit".
argument-hint: "[skill-name ...]"
compatibility: Designed for Claude Code
metadata:
  author: jackchuka
  scope: generic
  confirms:
    - install missing tools
---

# Skill Prerequisite Check

Scan installed skills, discover their tool/MCP/auth dependencies via heuristic parsing, check if everything is installed and authenticated, and offer to fix issues interactively.

## When to Use

- Setting up a new machine
- After installing new skills
- Verifying environment is ready for all skills
- Debugging "tool not found" errors during skill execution

## Arguments

Parse from the user's invocation:

- **Skill names**: Any tokens after the command → filter to those skills only
- **Default**: scan all skills in `~/.claude/skills/` and `.claude/skills/`

## Workflow

### Phase 1: Discover Skills

1. Glob for `~/.claude/skills/*/SKILL.md` and `.claude/skills/*/SKILL.md`
2. Follow symlinks
3. If user specified skill names, filter the list to matching directory names
4. Exclude this skill (`skill-prereq-check`) from the scan list — its own SKILL.md contains tool references as parsing examples, not actual dependencies
5. Read each SKILL.md file

### Phase 2: Parse Prerequisites

For each SKILL.md, extract dependencies using these heuristics:

**CLI tools:**

- Extract command names (first token of each line) from fenced code blocks marked as `bash`, `shell`, or `sh`
- Also scan `## Prerequisites` sections and prose for backtick-quoted tool names followed by "CLI", "installed", or "required"
- Ignore shell builtins and coreutils: `echo`, `cat`, `ls`, `mkdir`, `cd`, `grep`, `sed`, `awk`, `rm`, `cp`, `mv`, `date`, `wc`, `head`, `tail`, `sort`, `uniq`, `export`, `set`, `test`, `true`, `false`, `if`, `then`, `else`, `fi`, `for`, `do`, `done`, `while`, `case`, `esac`, `command`, `which`, `local`, `return`, `read`, `shift`, `printf`, `declare`
- Ignore git subcommands: the tool is `git`, not `git commit`
- Deduplicate per skill

**MCP servers:**

- Scan for `mcp__<server>__` patterns — extract `<server>` as the MCP server name
- Also scan for `<Name> MCP server` or `<Name> MCP tools` in prose — extract `<Name>` lowercased
- Deduplicate per skill

**gh extensions:**

- Scan for `gh <word>` where `<word>` is NOT a built-in gh command: `pr`, `issue`, `release`, `api`, `auth`, `repo`, `project`, `run`, `extension`, `gist`, `ssh-key`, `gpg-key`, `secret`, `variable`, `codespace`, `label`, `ruleset`, `cache`, `attestation`, `status`, `browse`, `search`, `workflow`, `config`, `alias`
- Record as gh extension dependency

**Auth hints:**

- Scan for `auth status`, `auth login`, `auth test`, `auth check`, `authenticated` within 200 characters of a tool name
- Mark that tool as needing an auth check

### Phase 3: Check Dependencies

Run checks for all discovered dependencies. Use parallel Bash calls where possible. Deduplicate check commands across skills — if multiple skills depend on the same tool, run the check once and reuse the result.

**CLI tools:**

1. Run `command -v <tool>` — if exit code 0, installed; otherwise missing
2. If auth hint exists for this tool, run `timeout 10 <tool> auth status 2>&1` (or use the Bash tool's timeout parameter set to 10000ms) and check exit code. If exit code != 0, try `timeout 10 <tool> auth check 2>&1`. If both fail, mark auth as "FAIL". If the command times out, mark auth as "TIMEOUT". If no auth hint, mark as "—"

**MCP servers:**

1. Use ToolSearch with query `+<server>` to check if any `mcp__<server>__*` tools are available in the session
2. If tools found → installed = "yes". If auth tool was referenced in the skill (e.g. `auth_test`), call it to verify. Otherwise auth = "—"
3. If no tools found → installed = "no", auth = "—"

**gh extensions:**

1. Run `gh extension list` once (cache the result)
2. Check if each extension name appears as a suffix in any line of the output (e.g., the line contains `/<extension-name>` or ends with the extension name)

### Phase 4: Present Results

Print a table grouped by skill:

```
## Prerequisite Check

| # | Skill | Tool | Type | Installed | Auth |
|---|-------|------|------|-----------|------|
| 1 | slack-triage | slack | mcp | yes | yes |
| 2 | meeting-scheduler | gws | cli | yes | FAIL |
| 3 | daily-report | gh | cli | yes | yes |
| 4 | daily-report | slackcli | cli | no | — |
| 5 | oss-release | oss-watch | gh-ext | no | — |

Summary: N skills checked, M tools found, X issues
```

- "yes" = check passed
- "FAIL" = check ran and failed
- "—" = not applicable (not installed, or no auth pattern detected)
- Number each row for reference in the fix phase

If no issues found, print "All prerequisites satisfied." and stop.

### Phase 5: Interactive Fix

If issues exist, ask: **"Want me to fix any of these? (e.g. '2, 4' or 'all' or 'done')"**

For each selected item, attempt the appropriate fix:

| Type   | Issue         | Fix Strategy                                                                                   |
| ------ | ------------- | ---------------------------------------------------------------------------------------------- |
| cli    | not installed | Try `brew install <tool>`. If brew doesn't have it, search web for install instructions        |
| cli    | auth FAIL     | Run `<tool> auth login` (interactive)                                                          |
| mcp    | not available | Tell user: "Add the `<server>` MCP server to your Claude config. I can't auto-configure this." |
| gh-ext | not installed | Run `gh extension install <owner/repo>` — search GitHub for the extension first                |

After each fix attempt, re-run the check for that item and show the updated row.

When all selected fixes are attempted, re-print the full table with updated results.

## Error Handling

- If `~/.claude/skills/` doesn't exist, report "No skills directory found at ~/.claude/skills/" and check only `.claude/skills/`
- If a tool's auth check hangs (>10s), kill it and mark as "TIMEOUT"
- If `brew` is not installed, suggest manual install instructions instead

## Examples

Example 1: Check all skills

```
User: "check prerequisites"
Action: Scan all skills, parse deps, check each, show table
```

Example 2: Check specific skills

```
User: "/skill-prereq-check slack-triage meeting-scheduler"
Action: Scan only those two skills, parse deps, check, show table
```

Example 3: Fix issues

```
User: (after seeing table) "fix 2, 5"
Action: Run `gws auth login` for item 2, `gh extension install` for item 5, re-check
```
