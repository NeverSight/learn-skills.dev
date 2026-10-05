---
name: token-optimization
description: Optimize token consumption in Claude Code through cache management, context forking, model selection, and input filtering. Use when user mentions high token costs, context window bloat, slow sessions, cache invalidation, verbose agent output, heavy MCP load, or any context management issues. Covers four critical axes - cache misses, context bloating, wrong model/effort level, and verbose input formats. Triggers on "tokens", "cost", "expensive", "context", "cache", "slow session", "optimize", or symptoms of token waste even without explicit mention.
metadata:
  author: valorisa
  version: 1.0.0
  category: workflow-automation
  requires: [bash, git]
---

# Token Optimization — Claude Code

## Overview

Token overconsumption in Claude Code stems from **four main sources**:

1. **Cache miss** — uncached or invalidated requests
2. **Context bloating** — unnecessarily growing context window
3. **Wrong model / wrong effort** — reasoning overuse
4. **Verbose input format** — overly verbose data injected into context

---

## Phase 1: Initial Session Audit

Before any work, run these two commands:

```bash
/context   # Shows loaded MCPs and tokens already consumed
/plugin    # Lists active plugins
```

**Systematic actions:**

- Disable all MCPs not needed for current project
- Disable all unused plugins
- One project ≠ one global config → customize per project

> Real example: empty session with Canva + Gmail + Google Calendar MCPs loaded = **23,000 tokens consumed before first keystroke**.

**Red flags to check:**

- More than 3 MCPs loaded
- Plugins unrelated to current work
- Base token count >10,000 on empty session

---

## Phase 2: Cache Management

### Principle

Claude Code caches: system instructions (CLAUDE.md), tool/MCP list, and message history. Any **modification during session** invalidates this cache, causing complete re-billing of affected tokens.

### Imperative rules

- **Never add a tool, MCP, or model mid-session.**
  Configure everything *before* starting, or in a dedicated setup session.
- If a critical addition is required mid-session (heavy skill, MCP, critical command):
  1. Compact the session (`/compact`)
  2. Start new session with compacted summary as starting point
- Treat cache like **HTTP cache**: changing a header invalidates everything downstream.

### Cache invalidation hierarchy

```
┌─────────────────────────────────────────────┐
│ BASE SYSTEM INSTRUCTIONS (CLAUDE.md + tools)│  ← Invalidated if tool added
├─────────────────────────────────────────────┤
│ SESSION STATE (project files, memory)       │  ← Invalidated if file changes
├─────────────────────────────────────────────┤
│ MESSAGE HISTORY                             │  ← Invalidated if message edited
│  msg 1 → msg 2 → msg 3 → ...                │     (invalidates everything after)
└─────────────────────────────────────────────┘
```

**What invalidates cache:**

| Action | Layer invalidated | Impact |
|---|---|---|
| Add MCP mid-session | Base instructions | Very high |
| Add tool (tool calling) | Base instructions | Very high |
| Modify CLAUDE.md | Base instructions | Very high |
| Edit message in middle of history | Message history (from that point) | Moderate |
| Load new file into context | Session state | Moderate |

**Optimal session strategy:**

```
1. Full configuration (MCP, tools, CLAUDE.md) → BEFORE starting
2. Work session → NEVER modify configuration
3. If modification needed → /compact → new session
4. Agents → context fork → isolated work → result only
```

For technical details on cache issues, see `references/cache-deep-dive.md`.

---

## Phase 3: Context Window Optimization

### Reduce default context window

The 1M token window is tempting but dangerous: it encourages bad habits and overloads child agents.

**Conditional recommendation:**

- Small/medium codebase → limit to ~200,000 tokens in `settings.json`:

  ```json
  { "contextWindow": 200000 }
  ```

  *(not committed by default — use local file)*
- Very large codebase → keep 1M, but optimize practices below even more aggressively.

> **RAM analogy**: having 32GB RAM doesn't justify poor memory management. A constrained window forces better discipline.

### Context forking and isolated agents

Agents inherit parent context at spawn time. **The longer you wait, the heavier they start.**

Target behavior:

- Call each skill or agent in a **forked context** (`context: fork` in parameters)
- Agent works in its own window → at completion, returns *only the result*, not full history
- When agent is destroyed, main context hasn't moved

**Systematic use cases to isolate in subagent:**

| Task | Why isolate |
|---|---|
| Web search | Markdown history of visited pages pollutes main window |
| PDF / audio transcription | High-volume output, unnecessary in main context |
| Planning / test generation | Long work, clean context |
| Codebase exploration | Native `explore` agent (uses IQ) already optimized for this |

**Prompt to add to CLAUDE.md:**

```
For any web search, systematically delegate to isolated subagent.
Return only extracted relevant information, not full history.
```

### Compaction and Rewind

- **Automatic compaction**: triggers when agent reaches ~80% of window. Desirable for agents, not for main session.
- **Rewind** (double `Esc`): allows returning to previous conversation and deleting unnecessary context branch. Use immediately when going in wrong direction.

---

## Phase 4: Model & Reasoning Effort Selection

### Reasoning effort

The effort system loops on the prompt to verify response quality. Each loop = additional tokens.

| Situation | Recommended effort |
|---|---|
| Clear, well-defined task | Medium (default) |
| Complex reasoning, architecture, design | High |
| Simple task, known command | Low / none (`think` unnecessary) |

> Rule: if the answer is clear in your mind, use `medium`. Ask Claude to **think with you**, not for you.

### Model choice

- **Claude Code subscription** → use native Anthropic models (Sonnet / Opus). No proxy.
  - Opus: prefer for complex tasks despite latency
  - Sonnet: fast tasks, common code generation
- **Proxy to other LLMs (GLM, Kimi...)**: only relevant if using SDK/API directly, not in standard Claude Code. Proxies are unstable and unoptimized.

**Add to CLAUDE.md:**

```markdown
## Reasoning effort
- Simple task / known command → minimal effort, no `think`
- Design / architecture task → medium effort
- Complex unsolved problem → high effort only on explicit request
Never over-reason a simple task.
```

---

## Phase 5: Input Format Optimization

### Browser automation: DOM over screenshots

Native Claude Code browser agent takes **screenshots** at each step → very costly in tokens and time.

**Recommended alternative: [Stagehand / Agent Browser (Vercel)](https://github.com/browserbase/stagehand)**

- Operates directly on DOM (invisible, no screenshots)
- Installation: open new Claude Code instance → `Install [stagehand URL]`
- Result: 10× faster, drastically reduced tokens

### Filter verbose CLI output

Commands like `git status`, `git diff` are extremely verbose once injected into context.

**Recommended tool: [RTK](https://github.com/simonw/rtk)** (developed by French developer)

- Filters command output before context window injection
- Example: `git status` goes from ~50 lines to ~5 essential lines → **~80% savings on this command**
- Global installation:

  ```bash
  # Run in Claude Code
  npx rtk init --global
  ```

### Concise responses: Caveman Skill / CLAUDE.md

By default, Claude Code is very verbose. Drastically reduce response volume:

**Directives to add to CLAUDE.md:**

```markdown
## Response style
Ultra-concise responses. Remove articles, politeness phrases, reformulations.
Get to the point. Format: short bullet points. No intro, no conclusion.
```

**Caveman Skill** (available on GitHub, ~50k stars): ready-to-use directives to integrate directly into CLAUDE.md. See `references/claude-md-templates.md` for examples.

### Specify file paths explicitly

Don't let Claude discover files on its own in commands:

```
# ❌ Costly: Claude will list, explore, read
"Update project memory"

# ✅ Optimal: explicit paths in command
"Update ./docs/memory.md and ./CLAUDE.md with following items: ..."
```

**Template for memory commands:**

```markdown
## Memory/Learning commands
`/learn` command: updates ONLY the following files:
- ./docs/project-memory.md
- ./CLAUDE.md (section "Project Context")
Do not scan other files unless explicitly instructed.
```

---

## Phase 6: Validation & Monitoring

### Check context consumption

After implementing optimizations, verify:

```bash
/context    # Check current token count
```

**Success criteria:**

- Base session <5,000 tokens (with necessary MCPs only)
- After 10 interactions: <30,000 tokens
- No agents exceeding 50,000 tokens for isolated tasks

### Team monitoring

For teams needing consumption tracking:

- Local dashboard tool (created by reference article author): displays sessions, called models, tokens per session
- More useful for managers/leads than solo developers
- See references below for link

**Documented concrete result:** went from $750/month to $100/month with these optimizations (source: article linked in reference video).

---

## Troubleshooting

### High token count despite optimizations

**Diagnosis steps:**

1. Run `/context` → identify which MCPs are loaded
2. Check `settings.json` → verify contextWindow setting
3. Review recent commands → identify verbose outputs
4. Check agent spawns → verify context forking

**Common fixes:**

- Disable unused MCPs
- Add RTK filtering for git commands
- Move to subagents for research tasks
- Reduce contextWindow if codebase allows

### Cache invalidation happening frequently

**Diagnosis:**

1. Check if skills are being loaded mid-session
2. Verify CLAUDE.md isn't changing
3. Look for tool additions in session

**Fixes:**

- Preload all needed skills at session start
- Lock CLAUDE.md configuration
- Use dedicated setup session for config changes

### Agents consuming too many tokens

**Diagnosis:**

1. Check if agents inherit bloated parent context
2. Verify agents aren't loading unnecessary MCPs
3. Look for verbose tool outputs in agent history

**Fixes:**

- Spawn agents earlier (lighter parent context)
- Use `context: fork` parameter
- Return only results, not full agent history

---

## Examples

### Example 1: Project setup with token optimization

**User says:** "Set up new project with optimal token configuration"

**Actions:**

1. Create minimal CLAUDE.md with concise response directives
2. Configure contextWindow based on codebase size
3. Enable only essential MCPs for project type
4. Add RTK filtering for git commands
5. Define subagent delegation rules
6. Verify base session <5,000 tokens

**Expected result:** Optimized session configuration, documented in project CLAUDE.md

### Example 2: Diagnosing high token consumption

**User says:** "My sessions are consuming too many tokens, help diagnose"

**Actions:**

1. Run `/context` to audit current state
2. Check loaded MCPs and plugins
3. Review recent command outputs for verbosity
4. Identify cache invalidation patterns
5. Generate optimization recommendations
6. Implement fixes prioritized by impact

**Expected result:** Identified root causes, implemented fixes, reduced token consumption by 50-80%

### Example 3: Web research task

**User says:** "Research best practices for React Server Components"

**Actions:**

1. Spawn isolated subagent with context fork
2. Subagent performs web searches
3. Subagent extracts key findings only
4. Return summary to main context (not full search history)
5. Main context receives ~500 tokens instead of ~5,000

**Expected result:** Research completed with 90% token savings vs direct search

---

## References

For detailed technical information:

- `references/cache-deep-dive.md` — Cache behavior and invalidation patterns
- `references/claude-md-templates.md` — Ready-to-use CLAUDE.md configuration blocks
- `references/tools.md` — External tools (Stagehand, RTK) setup guides

**External resources:**

- [Anthropic Prompt Caching Documentation](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Stagehand Browser Automation](https://github.com/browserbase/stagehand)
- [RTK CLI Output Filter](https://github.com/simonw/rtk)

---

## Quality Checklist

Before completing optimization:

- [ ] Base session <5,000 tokens
- [ ] Only essential MCPs loaded
- [ ] CLAUDE.md includes concise response directives
- [ ] Context forking configured for research tasks
- [ ] RTK or equivalent filtering installed for verbose commands
- [ ] contextWindow set appropriately for codebase size
- [ ] Team members trained on cache invalidation rules (if applicable)
