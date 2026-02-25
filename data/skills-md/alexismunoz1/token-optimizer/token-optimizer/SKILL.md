---
name: token-optimizer
description: >
  Practical guide to reduce token consumption, lower AI costs, and improve
  Claude Code performance through file organization, context management,
  and strategic model selection. Backed by real experiment data.
  Use when user mentions "optimize tokens", "reduce costs", "Claude is slow",
  "too many tokens", "token budget", "context window full", "organize codebase
  for AI", or "reduce token consumption". Do NOT use for general coding questions,
  debugging, or performance optimization unrelated to AI token usage.
compatibility: Claude Code
license: MIT
metadata:
  author: alexismunoz1
  version: 1.2.0
---

# Token Optimizer

A comprehensive toolkit to reduce token consumption, lower AI costs, and improve Claude Code performance. Every recommendation is backed by real experiment data from a controlled comparison of monolithic vs modular code architectures.

## Installation

```bash
npx skills add alexismunoz1/token-optimizer
```

Or manually:

```bash
cp -r token-optimizer ~/.claude/skills/
```

## Core Features

### 1. File Organization Optimization

The single highest-impact optimization. Small, focused files reduce token consumption by 18.2% and noise by 92% on focused tasks (the majority of daily development work).

**Core rules:**
- Maximum 150 lines per file — split by responsibility if longer
- Single responsibility — one concern per file
- Descriptive names in kebab-case — the filename tells the AI exactly what's inside

**Real example:** Fixing an email validation bug required reading 814 lines in a monolithic file (49,466 tokens) vs only 67 lines in a modular setup (40,447 tokens) — **18.2% savings, 92% less noise**.

> For naming conventions, avoid/prefer tables, and project structure templates, see `references/file-organization-guide.md`

### 2. CLAUDE.md Optimization

A well-structured CLAUDE.md can reduce token consumption by 50-70%. Most projects have bloated CLAUDE.md files that load unnecessary context on every interaction.

**Key principles:**
- Keep it under 500 lines — essentials only
- Be specific — "PostgreSQL with Prisma" not just "database"
- Include project structure and commands — save the AI from guessing
- Use triggers, not full docs — reference skills/files for details, don't inline everything

> For a ready-to-use optimized template, see `references/claude-md-template.md`

### 3. Context Management

Token waste often comes from accumulated irrelevant context, not from individual operations.

**Essential commands:**

| Command | When to Use | Effect |
|---------|-------------|--------|
| `/clear` | Switching tasks, after major corrections | Resets context completely |
| `/compact` | Long conversation (>50 exchanges) | Compresses history, keeps essentials |
| `/context` | Diagnosing high token use | Shows what's consuming tokens |

**Lazy loading:** Don't front-load all information. One project achieved **54% reduction** in initial tokens (7,584 → 3,434) by keeping only triggers in CLAUDE.md and loading details on demand.

> For advanced strategies, subagent patterns, and MCP management, see `references/context-management-guide.md`

### 4. Strategic Model Selection

Choosing the right model per task type is one of the easiest cost savings to implement.

| Task Type | Model | Why |
|-----------|-------|-----|
| 80% of daily tasks | Sonnet | Best cost/performance ratio |
| Complex architecture | Opus | Deeper reasoning needed |
| Simple/quick tasks | Haiku | Up to 18x cheaper than Opus |

Default to Sonnet. Escalate to Opus only for genuinely complex problems. Use Haiku for simple tasks, tests, and searches.

### 5. MCP & Subagent Optimization

**MCP Management:**
- Keep maximum 10 active MCPs at a time (max 80 total tools)
- Disable MCPs not needed for the current task
- Each unused MCP still costs tokens in tool descriptions

**Subagents for verbose tasks:** Use the Task tool for operations that generate large output (test runs, builds, searches). The verbose output stays in the subagent's context — only the summary returns to your main conversation.

## Quick Wins Checklist

Apply these in order of impact:

1. **Split large files** (>150 lines) into focused modules → saves 18%+ tokens
2. **Optimize your CLAUDE.md** → can reduce consumption 50-70%
3. **Use `/clear` between tasks** → eliminates irrelevant context
4. **Use `/compact` in long conversations** → compresses history
5. **Use the right model** → Haiku costs 18x less than Opus for simple tasks
6. **Limit active MCPs** to ≤10 → fewer tools = less overhead per call
7. **Use subagents for verbose tasks** → output stays in subagent context

## Expected Savings

Results from our controlled experiment with an 814-line TypeScript e-commerce app:

| Optimization | Impact |
|-------------|--------|
| Modular files (focused tasks) | **-18.2% tokens** |
| Noise reduction (lines processed) | **-92%** |
| Optimized CLAUDE.md | **-50-70% consumption** |
| Lazy loading context | **-54% initial tokens** |
| Haiku vs Opus (simple tasks) | **-94% cost** |

**Key insight:** Focused tasks (bug fixes, specific changes — ~80% of daily work) benefit enormously from modular code. Cross-cutting tasks show minimal difference at small scale (+1-5%) but modular wins decisively at 5,000+ lines.

> For the complete experiment methodology and raw data, see `references/metrics-report.md`

## Diagnostic Workflow

When activated, follow this process:

1. **Assess**: Ask the user to run `/context` to see current token usage
2. **Identify**: Determine the biggest source of waste (large files, bloated CLAUDE.md, accumulated context, too many MCPs)
3. **Recommend**: Suggest the highest-impact optimization from the Quick Wins Checklist
4. **Verify**: After changes, have the user re-run `/context` to measure improvement

**Important guidelines:**
- Always diagnose first — don't dump all optimizations
- Measure before and after — every optimization should be verified with metrics
- Focus on the user's specific problem — identify the most impactful change first
- Be transparent about trade-offs — modular files save 18%+ on focused tasks but show minimal difference on cross-cutting tasks at small scale

## Usage Examples

### "My Claude Code sessions are getting expensive"

1. Run `/context` to see current token consumption breakdown
2. Audit CLAUDE.md size — if over 500 lines, trim to essentials
3. Check for files >150 lines — identify candidates for splitting
4. Count active MCPs — disable unused ones
5. Review model usage — switch routine tasks to Sonnet/Haiku

### "Organize my codebase for AI"

1. Scan the project for files exceeding 150 lines
2. Identify generic filenames (`utils.ts`, `helpers.ts`, `index.ts` with logic)
3. Propose file splits by responsibility with new descriptive names
4. Suggest a project structure following the organization guide

### "My context window keeps filling up"

1. Run `/context` to identify what's consuming tokens
2. Check if CLAUDE.md has inline documentation that should be referenced instead
3. Recommend `/clear` between tasks and `/compact` for long sessions
4. Suggest moving verbose content to referenced files (lazy loading)

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No improvement after optimizations | No baseline measurement taken | Run `/context` before AND after each change |
| Don't know how many tokens I'm using | Token consumption not visible by default | Use `/context` to see the full breakdown |
| `/compact` doesn't reduce enough | Compresses but keeps essentials | Use `/clear` if prior context is irrelevant |
| Cross-cutting tasks slower after splitting | Multiple reads needed (1-5% more tokens) | Expected and marginal — focused tasks (80% of work) still save 18%+ |

## Reference Materials

- `references/file-organization-guide.md` — Naming conventions, project structure templates, and implementation checklist
- `references/context-management-guide.md` — Lazy loading, subagents, MCP management, and model selection strategies
- `references/metrics-report.md` — Complete experiment data and methodology with raw numbers
- `references/claude-md-template.md` — Ready-to-use optimized CLAUDE.md template
