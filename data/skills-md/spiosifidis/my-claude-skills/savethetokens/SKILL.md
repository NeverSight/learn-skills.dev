---
name: savethetokens
description: Reduce Claude Code token burn with proactive compacting, task-scoped sessions, checkpoint files, tiered docs, and relevance-based context pruning. Use when a user explicitly asks to reduce context usage/cost, run token benchmarks, or optimize CLAUDE.md. Do not use to expand product scope or skip correctness checks.
---

# Context Governor

Optimize context usage with practical, high-impact workflows and scripts.

## Non-Negotiable Guardrails

1. Keep scope locked to the user request. Do not add extra features, pages, or telemetry unless asked.
2. Treat token optimization as a constraint, not the goal. Correctness and security win over token reduction.
3. Never claim token savings without before/after measurement on comparable tasks.
4. If context-saving actions risk quality loss, keep the extra context and state the tradeoff.
5. **Never reduce code thoroughness to save tokens.** Tests, strict config, safety checks, and error handling are non-negotiable. Save tokens from message verbosity — never from output completeness.

## Operating Modes

- `Lean Mode` (default): Use lightweight context hygiene only; do not create new benchmark artifacts.
- `Measurement Mode`: Use launch-readiness or A/B telemetry scripts only when user asks for proof/percentages.

## Claude Code Message Budget (required)

1. Keep progress updates short and phase-based. Do not narrate every file write.
2. Do not paste long command output unless user asks. Summarize only key signals.
3. Do not repeat the same command without a code/input change; if retried, state the reason once.
4. If `/context` shows message growth is unusually high, switch to stricter concise mode:
   - fewer updates
   - shorter summaries
   - batch related edits before reporting
5. Prefer one concise final summary over long running commentary.
6. For benchmark runs, enforce matched behavior on both variants:
   - same stop criteria
   - same compact policy
   - same output style (no extra giant report in one variant only)

## Operating Playbook

1. Confirm objective and lock scope in one sentence.
2. Keep one chat session per task. Start a new session for unrelated work.
3. Use `! <command>` for direct shell commands when no reasoning is required.
4. Run `/context` periodically. Compact around 50% usage instead of waiting for hard limits.
5. Before `/compact` or `/clear`, create a checkpoint file with next steps and touched files.
6. Keep top-level docs lean; move deep details to linked `docs/*.md`.
7. Before final output on code tasks, run the quality gates in `docs/QUALITY_GATES.md`.
8. For token-savings claims, run matched A/B using `docs/BENCHMARK_PROTOCOL.md`.
9. For Claude benchmark runs, use `docs/STRICT_BENCHMARK_PROMPT.md` as the session starter.

## Quick Commands

```bash
# Generate execution plan
python ~/.claude/skills/savethetokens/scripts/govern.py --budget 8000

# Generate checkpoint before compact/clear
python ~/.claude/skills/savethetokens/scripts/session_checkpoint.py \
  --task "..." \
  --done "..." \
  --next "..." \
  --context-percent 52 \
  --message-count 36

# Create session hook (Claude Code)
python ~/.claude/skills/savethetokens/scripts/session_hook_generator.py --project .

# Optimize CLAUDE.md
python ~/.claude/skills/savethetokens/scripts/claude_md_optimizer.py --analyze

# Calculate cost savings
python ~/.claude/skills/savethetokens/scripts/cost_calculator.py --developers 5

# Run launch-readiness benchmark with section-wise savings
python ~/.claude/skills/savethetokens/scripts/launch_readiness.py

# Run live A/B telemetry session (auto split control/optimized)
python ~/.claude/skills/savethetokens/scripts/govern.py \
  --input context.json \
  --budget 8000 \
  --experiment-id claude-launch-v1 \
  --variant auto \
  --assignment-key TICKET-123

# Generate measured A/B report from live sessions
python ~/.claude/skills/savethetokens/scripts/ab_telemetry.py \
  --experiment-id claude-launch-v1 \
  --days 14 \
  --required-intents code_generation,debugging,planning,review \
  --min-samples-per-intent 5

# Strict mode: exit 2 if claim gates fail (CI-friendly)
python ~/.claude/skills/savethetokens/scripts/ab_telemetry.py \
  --experiment-id claude-launch-v1 \
  --strict-claim-mode

# Print report JSON to stdout (pipe to jq, etc.)
python ~/.claude/skills/savethetokens/scripts/ab_telemetry.py \
  --experiment-id claude-launch-v1 \
  --json-stdout

# Code-task quality gate checklist (required before final answer)
cat ~/.claude/skills/savethetokens/docs/QUALITY_GATES.md

# Compare two /context snapshots (control vs optimized)
python ~/.claude/skills/savethetokens/scripts/context_snapshot_diff.py \
  --before-file before.txt \
  --after-file after.txt \
  --strict

# Compact watchdog (advisory, safe defaults)
python ~/.claude/skills/savethetokens/scripts/compact_watchdog.py \
  --context-file context_snapshot.txt \
  --require-checkpoint

# Dynamic tool filtering (fail-open recommended)
python ~/.claude/skills/savethetokens/scripts/tool_filter.py \
  --input tools.json \
  --query "..." \
  --fail-open

# Semantic skill selection (recommendation only)
python ~/.claude/skills/savethetokens/scripts/skill_selector.py \
  --query "..."

# External memory store (bounded retrieval)
python ~/.claude/skills/savethetokens/scripts/memory_store.py search \
  --query "..." \
  --for-prompt \
  --top-k 5 \
  --max-chars 1200

# Print lean session prompt template
cat ~/.claude/skills/savethetokens/docs/LEAN_SESSION_PROMPT.md

# Print strict benchmark harness prompt
cat ~/.claude/skills/savethetokens/docs/STRICT_BENCHMARK_PROMPT.md

```

## Scripts

| Script | Purpose |
|--------|---------|
| `govern.py` | Main entry - execution plans |
| `analyze.py` | Context analysis |
| `prune.py` | Prune to budget (max 40%) |
| `session_hook_generator.py` | Session-start hooks |
| `session_checkpoint.py` | Save compact-ready session checkpoints |
| `claude_md_optimizer.py` | Optimize CLAUDE.md |
| `quick_ref_generator.py` | Generate QUICK_REF.md |
| `tiered_context.py` | 3-tier context classification |
| `relevance_scorer.py` | Score context relevance |
| `cost_calculator.py` | ROI tracking |
| `launch_readiness.py` | Launch benchmark + section-wise savings report |
| `ab_telemetry.py` | Live A/B telemetry report with confidence checks |
| `context_snapshot_diff.py` | Detect token regressions from /context snapshots |
| `compact_watchdog.py` | Safe advisory for `/compact` and `/clear` decisions |
| `tool_filter.py` | Dynamic tool filtering with fail-open safeguards |
| `skill_selector.py` | Semantic skill ranking with confidence gating |
| `memory_store.py` | External memory store with bounded retrieval |
| `path_filter.py` | Filter package dirs |

## Quality Rules

- **NEVER** prune system prompts, errors, recent messages
- Max pruning: 40% (keeps quality)
- When uncertain → KEEP content
- Will exceed budget rather than harm quality
- Keep solution minimal and request-aligned; avoid speculative architecture
- Run relevant tests/checks for touched areas, or explicitly state what could not be run

## Completeness Checklist (never skip under token pressure)

Token savings come from shorter messages and smarter context — never from cutting corners on output quality. Before finalizing any code task, verify:

1. **Strict config** — Enable strictest compiler/linter settings available (e.g. `"strict": true` in tsconfig). Zero `any` types, zero `@ts-ignore`, zero `@ts-nocheck`.
2. **Tests for touched code** — Every changed function/module has corresponding tests. Minimum: one happy path, one error path per public function.
3. **Safety limits** — Runtime code that loops, recurses, or processes unbounded input must have explicit guards (max iterations, call depth, step limits, timeouts).
4. **Error handling with context** — Errors include location info (file, line, span) and actionable messages. No bare `catch(e) {}` or `except Exception: pass`.
5. **Input validation at boundaries** — Validate user input, API responses, and file I/O. Internal code can trust internal types.
6. **Security basics** — No command injection, no unsanitized template interpolation, no hardcoded secrets. Parameterize queries.
7. **Build passes** — Run type-check/compile/build before declaring done. If it can't be run, state why.
8. **State what was not verified** — If any check above could not be performed (no test runner, no build script), explicitly list it in the final summary.

Where to save tokens instead: shorter progress updates, batch related edits, omit command output unless asked, compact at 50% context.

## Detailed Docs (read on-demand)

- [EXECUTION_PLANS.md](docs/EXECUTION_PLANS.md) - Plan structure
- [PRUNING_STRATEGIES.md](docs/PRUNING_STRATEGIES.md) - Pruning logic
- [MODEL_SELECTION.md](docs/MODEL_SELECTION.md) - Model recommendations
- [TOKEN_ESTIMATION.md](docs/TOKEN_ESTIMATION.md) - Token counting
- [SESSION_PLAYBOOK.md](docs/SESSION_PLAYBOOK.md) - Practical compact/reset workflow
- [QUALITY_GATES.md](docs/QUALITY_GATES.md) - Mandatory code-quality and claim-quality gates
- [BENCHMARK_PROTOCOL.md](docs/BENCHMARK_PROTOCOL.md) - Matched A/B process for fair measurement
- [LEAN_SESSION_PROMPT.md](docs/LEAN_SESSION_PROMPT.md) - Paste-ready strict token-discipline prompt
- [STRICT_BENCHMARK_PROMPT.md](docs/STRICT_BENCHMARK_PROMPT.md) - Paste-ready harness for fair Claude Code A/B testing
- [ADVANCED_AUTOMATION.md](docs/ADVANCED_AUTOMATION.md) - Optional advanced features with safety controls
- [LAUNCH_READINESS.md](docs/LAUNCH_READINESS.md) - Measured launch benchmark report
- [LIVE_TELEMETRY.md](docs/LIVE_TELEMETRY.md) - Live control vs optimized experiment report
