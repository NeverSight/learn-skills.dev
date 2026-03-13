---
name: cache-audit
description: "Audit your Claude Code setup for prompt caching efficiency. Measures prefix size, hook patterns, rule duplication, dynamic injection sizes, and tool stability. Returns a scored report with fixes ranked by token savings."
---

# Prompt Cache Audit

**Trigger:** `/cache-audit` or "audit my caching" or "check my cache setup"

**What it does:** Reads your live Claude Code configuration and measures it against prompt caching best practices. Returns a scored report with specific, actionable fixes ranked by token savings.

**Background:** The API caches the prefix of each request (system prompt, tool definitions, CLAUDE.md, rules, skill registry, MEMORY.md). An identical prefix between turns = ~90% cost reduction on those tokens. ANY change to the prefix invalidates everything after the change point.

---

## When Invoked

Run ALL 8 checks automatically. Do NOT ask for confirmation. Read the relevant files, measure sizes, and produce the full report in one pass.

Use `$PROJECT` to refer to the current working directory throughout.

---

## The 8 Checks

### Check 1 — Prefix Ordering (Static Before Dynamic)

**Read:** `~/.claude/CLAUDE.md`, `$PROJECT/CLAUDE.md`, `~/.claude/rules/*.md`, `$PROJECT/.claude/rules/*.md`, and the MEMORY.md file for the current project (find it under `~/.claude/projects/*/memory/MEMORY.md` — match by project path).

**Flag any dynamic content in these files:**
- Timestamps, `new Date()`, hardcoded dates that go stale
- Git refs, commit hashes, branch names
- Session IDs, task IDs, "currently working on X"
- File counts, line counts, or any computed metrics
- `currentDate` entries in MEMORY.md

These files are part of the **static prefix**. Dynamic data here means cache misses on every turn where it changes.

**Scoring:**
- PASS: All prefix files contain only static instructions and conventions
- WARNING: Low-frequency dynamic data (e.g., a date updated daily)
- FAIL: High-churn content (timestamps, computed values) in any prefix file

---

### Check 2 — Hook Injection Pattern

**Read:** `~/.claude/settings.json` and `$PROJECT/.claude/settings.json` to find all hook commands. Then read each referenced hook file.

**For each hook, verify:**
- Hooks that inject context MUST use `additionalContext` in their JSON output (this becomes a `<system-reminder>` message — part of the message history, NOT the prefix)
- Hooks that only log/backup should produce no `hookSpecificOutput` at all

**Specifically flag:**
- Any hook that opens and writes to CLAUDE.md, MEMORY.md, or rule files mid-session
- Any hook that modifies tool definitions or the system prompt directly
- Any hook that uses `hookSpecificOutput` keys other than `additionalContext`

**Check each hook and report its pattern:**

| Hook Event | Expected Pattern |
|------------|-----------------|
| SessionStart | `additionalContext` with compact git context OR no output |
| UserPromptSubmit | Logging only, no `additionalContext` |
| PreCompact | Logging/backup only, no context injection |
| All others (Stop, SessionEnd, Notification, etc.) | No prefix modification |

**Scoring:**
- PASS: All hooks use `additionalContext` or no-inject patterns
- FAIL: Any hook modifies prefix files (CLAUDE.md, rules, MEMORY.md) mid-session

---

### Check 3 — Tool Stability

**Read:** `~/.claude.json` for global MCP servers, `$PROJECT/.mcp.json` for project MCP servers (if exists).

**Measure and report:**
- Total MCP server count (global + project-level)
- Each server name and whether it's deduplicated across levels

**Flag:**
- Same MCP server name at both global and project level (tool schema loaded twice?)
- Any skill that explicitly adds or removes tools when invoked
- > 8 total MCP servers (each adds tool schema tokens to the prefix)

**Note:** MCP tools use deferred loading via `ToolSearch` by default — this is the correct pattern. Stubs are lightweight; full schemas load on demand.

**Scoring:**
- PASS: Fixed tool set at session start, no conditional loading
- WARNING: > 8 MCP servers (consider if all are needed per-project)
- FAIL: Dynamic tool add/remove detected mid-conversation

---

### Check 4 — Model Consistency

**Read:** `~/.claude/settings.json` for `model` or `alwaysThinkingEnabled` fields.

**Check:**
- Is there a stable model configuration? (Default model is fine if consistent)
- Do any agent definitions (`.claude/agents/*.md`) specify different `model:` in frontmatter for inline use?
- Subagent model delegation (Task tool with `model:` parameter) is FINE — separate conversations don't break parent cache

**Scoring:**
- PASS: Consistent model per conversation, subagents handle model switching
- FAIL: Evidence of inline model switching in same conversation thread

---

### Check 5 — Dynamic Content Size

**Measure actual injection sizes. For each source, read the hook code and estimate output:**

| Source | How to Measure | PASS | WARNING | FAIL |
|--------|---------------|------|---------|------|
| SessionStart hook | Read code — estimate `additionalContext` output chars | < 200 | 200–2K | > 2K |
| UserPromptSubmit hook | Read code — does it emit `additionalContext`? | No output | < 500 | > 500 |
| Built-in git status | Run `git status --porcelain \| wc -c` | < 2K | 2–10K | > 10K |
Use ~4 chars per token as the conversion estimate.

**Also report:**
- Total hook count across all events (each hook = execution latency per trigger)
- Any hook with timeout > 10 seconds

**Overall scoring:**
- PASS: All per-turn injections total < 2K chars
- WARNING: 2–10K chars per turn
- FAIL: > 10K chars injected per turn into the main conversation

---

### Check 6 — Fork Safety (Compaction & Subagents)

**Read:** PreCompact hook code.

**Verify:**
- PreCompact hook does NOT modify the prefix (logging/backup only is correct)
- No custom compaction logic that rebuilds the system prompt differently
- Claude Code's built-in compaction preserves system prompt + tools by default

**Scoring:**
- PASS: Using built-in compaction + `additionalContext`-only hook injection
- FAIL: Any hook modifies prefix during compaction or subagent spawn

---

### Check 7 — Static Prefix Budget

**This is the most actionable check.** Measure every component of the static prefix.

**Read and measure (report in chars AND estimated tokens at ~4 chars/token):**

| Component | How to Find |
|-----------|-------------|
| CLAUDE.md (global) | `~/.claude/CLAUDE.md` |
| CLAUDE.md (project) | `$PROJECT/CLAUDE.md` |
| Rules (global) | Each file in `~/.claude/rules/*.md` |
| Rules (project) | Each file in `$PROJECT/.claude/rules/*.md` |
| MEMORY.md | Match current project under `~/.claude/projects/*/memory/MEMORY.md` |

**Use `wc -c` via Bash to measure file sizes. Measure EACH file individually.**

**Calculate:**
1. Grand total chars across all measured files
2. Estimated tokens (chars / 4)
3. Percentage of 200K context window consumed by static prefix

**Report the top 5 largest individual files.**

**Scoring:**
- PASS: Total static prefix < 60K chars (~15K tokens, ~7.5% of context)
- WARNING: 60–120K chars (~15–30K tokens, 7.5–15% of context)
- FAIL: > 120K chars (~30K tokens, > 15% of context)

---

### Check 8 — Rule Layer Efficiency

**Read:** List filenames in `~/.claude/rules/` and `$PROJECT/.claude/rules/`.

**Key fact:** Rules at both levels are **additive** — Claude Code loads ALL of them. This means duplicate filenames = duplicate content = wasted tokens.

**Check for:**
1. Any filename that exists at BOTH `~/.claude/rules/` and `$PROJECT/.claude/rules/` — these load twice
2. For each duplicate, read both versions and estimate content overlap
3. Whether the project uses a single `project-implementation.md` for overrides (correct pattern) vs. many files that duplicate user-level rules

**The correct pattern:**
- **User-level** (`~/.claude/rules/`): Generic patterns — the WHAT (applies to all projects)
- **Project-level** (`$PROJECT/.claude/rules/`): Single `project-implementation.md` — the HOW (framework-specific overrides)

**Scoring:**
- PASS: No duplicate filenames, project uses `project-implementation.md` only
- WARNING: 1–3 duplicate files
- FAIL: > 3 duplicate files — significant token waste from additive loading

---

## Output Format

After running all 8 checks, output this exact report format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PROMPT CACHE AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Score: X/8

[✅/⚠️/❌]  Check 1 — Prefix Ordering: [PASS/WARNING/FAIL]
   → [finding]

[✅/⚠️/❌]  Check 2 — Hook Injection: [PASS/WARNING/FAIL]
   → [each hook and its pattern]

[✅/⚠️/❌]  Check 3 — Tool Stability: [PASS/WARNING/FAIL]
   → [N global + N project MCP servers, any issues]

[✅/⚠️/❌]  Check 4 — Model Consistency: [PASS/WARNING/FAIL]
   → [model config]

[✅/⚠️/❌]  Check 5 — Dynamic Content: [PASS/WARNING/FAIL]
   → [size breakdown per injection point]

[✅/⚠️/❌]  Check 6 — Fork Safety: [PASS/WARNING/FAIL]
   → [compaction + subagent pattern]

[✅/⚠️/❌]  Check 7 — Prefix Budget: [PASS/WARNING/FAIL]
   → Total: XX,XXX chars (~X,XXX tokens, X.X% of 200K)
   → Top 5 largest:
     1. filename — X,XXX chars (~X,XXX tokens)
     2. filename — X,XXX chars (~X,XXX tokens)
     3. ...

[✅/⚠️/❌]  Check 8 — Rule Efficiency: [PASS/WARNING/FAIL]
   → [duplicate count + wasted tokens]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TOKEN BUDGET SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Static prefix:          ~XX,XXX tokens (X.X% of 200K window)
Per-turn injection:     ~XXX tokens
Per-builder spawn:      ~X,XXX tokens
Per-lightweight spawn:  ~XX tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TOP FIXES (ranked by token savings)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Most impactful fix — exact steps]
2. [Second most impactful — exact steps]
3. [Third — if applicable]
```

If all checks pass: confirm the setup is well-optimised and estimate cost savings vs a naive configuration (no caching awareness).

---

## Prompt Caching Cheatsheet

| Rule | Do | Don't |
|------|----|-------|
| Ordering | Static CLAUDE.md + rules, dynamic in messages | Timestamps/dates/git refs in prefix files |
| Updates | `additionalContext` → `<system-reminder>` | Edit CLAUDE.md or rules mid-session |
| Tools | Fixed tool set + deferred MCP stubs | Add/remove tools per turn |
| Models | One model per conversation, subagents for switches | Inline model switching |
| Size | Trim injections to minimum needed | Dump full git status (40K+ chars) |
| Forks | Built-in compaction, `additionalContext` only | Custom prefix rebuilds |
| Budget | Static prefix < 15K tokens | Bloated CLAUDE.md, massive rule files |
| Layers | User-level generic + project-level `project-implementation.md` | Same rule files at both levels |
