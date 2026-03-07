---
name: llm-council
description: Orchestrate multi-LLM parallel debate and synthesis. Dispatches prompts to available omega CLI wrappers in parallel, collects independent responses, runs anonymized peer review ranking, and synthesizes via a chairman model. No server required.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read, Write]
args: '"PROMPT" [--models MODEL1,MODEL2,...] [--chairman MODEL] [--skip-review] [--timeout-ms N]'
best_practices:
  - Always check available CLIs before dispatching (run verify-setup.mjs for each)
  - Use at least 3 models for meaningful peer review rankings
  - Set --timeout-ms per model to prevent one slow model from blocking the council
  - Anonymize responses before peer review to prevent model identity bias
  - Store council results in .claude/context/tmp/ for downstream consumption
error_handling: graceful
streaming: not_supported
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# LLM Council Skill

<identity>
Multi-LLM deliberation orchestrator. Implements a 3-stage council process:
Stage 1 (parallel independent responses) -> Stage 2 (anonymized peer review with ranking) ->
Stage 3 (chairman synthesis). Uses omega CLI wrapper skills for model invocation.
No server required -- pure Bash-level orchestration.
</identity>

<capabilities>
- Parallel dispatch to multiple LLM CLIs (Gemini, Codex, Cursor, Claude)
- Dynamic availability detection (only dispatches to available CLIs)
- 3-stage council protocol:
  - Stage 1: Independent parallel responses
  - Stage 2: Anonymized peer review with FINAL RANKING
  - Stage 3: Chairman synthesis of all inputs
- Anonymized labeling (Response A, B, C...) to prevent model identity bias
- Configurable chairman model (default: current Claude session)
- Per-model timeout enforcement
- Graceful degradation (skips unavailable models)
- Structured output with all 3 stages preserved
</capabilities>

## Council Protocol

### Stage 1: Independent Responses

Dispatch the user's prompt to all available omega CLIs in parallel:

```bash
# Check availability
node .claude/skills/omega-gemini-cli/scripts/verify-setup.mjs && HAS_GEMINI=1
node .claude/skills/omega-codex-cli/scripts/verify-setup.mjs && HAS_CODEX=1
node .claude/skills/omega-claude-cli/scripts/verify-setup.mjs && HAS_CLAUDE_CLI=1
node .claude/skills/omega-cursor-cli/scripts/verify-setup.mjs && HAS_CURSOR=1

# Parallel dispatch to available CLIs
TMPDIR=$(mktemp -d)
[ "$HAS_GEMINI" = "1" ] && node .claude/skills/omega-gemini-cli/scripts/ask-gemini.mjs "$PROMPT" --timeout-ms 120000 > "$TMPDIR/gemini.txt" 2>"$TMPDIR/gemini.err" &
[ "$HAS_CODEX" = "1" ] && node .claude/skills/omega-codex-cli/scripts/ask-codex.mjs "$PROMPT" --timeout-ms 120000 > "$TMPDIR/codex.txt" 2>"$TMPDIR/codex.err" &
[ "$HAS_CLAUDE_CLI" = "1" ] && node .claude/skills/omega-claude-cli/scripts/ask-claude.mjs "$PROMPT" --timeout-ms 120000 > "$TMPDIR/claude.txt" 2>"$TMPDIR/claude.err" &
[ "$HAS_CURSOR" = "1" ] && node .claude/skills/omega-cursor-cli/scripts/ask-cursor.mjs "$PROMPT" --yolo --trust --timeout-ms 120000 > "$TMPDIR/cursor.txt" 2>"$TMPDIR/cursor.err" &
wait
```

### Stage 2: Anonymized Peer Review

1. Collect all successful Stage 1 responses
2. Assign anonymous labels: Response A, Response B, Response C, ...
3. Maintain label_to_model mapping (e.g., A=gemini, B=codex, C=claude)
4. Send all anonymized responses back to each available model with:

```
You are reviewing responses to this question: "$PROMPT"

Response A:
[content]

Response B:
[content]

Response C:
[content]

Evaluate each response for accuracy, completeness, and reasoning quality.
Then provide your FINAL RANKING (best to worst):
1. Response [X]
2. Response [Y]
3. Response [Z]
```

1. Parse FINAL RANKING from each reviewer's output using regex: `\d+\.\s*Response [A-Z]`
2. Compute aggregate ranking (average position across all reviewers)

### Stage 3: Chairman Synthesis

Send to chairman model (default: current Claude session or ask-claude.mjs):

```
You are the Chairman synthesizing a multi-model council discussion.

Original question: "$PROMPT"

Stage 1 Responses (with de-anonymized model names):
[Model]: [Response]
...

Stage 2 Peer Review Rankings:
Aggregate ranking: [best to worst with scores]

Synthesize the best insights from all responses into a single comprehensive answer.
Highlight areas of consensus and dissent. Provide the strongest possible answer.
```

## Usage

### Full council (all available models)

```bash
Skill({ skill: 'llm-council' })
# Then in agent: run full council protocol above
```

### Quick consultation (skip peer review)

```bash
# Stage 1 only -- parallel dispatch, collect responses, skip ranking
# Use when speed matters more than rigorous evaluation
```

## When to Use

- High-stakes architectural decisions requiring multiple perspectives
- Code review where diverse model viewpoints reduce blind spots
- Plan critique and validation
- Resolving disagreements about implementation approach
- Cross-validation of security analysis
- When the user explicitly requests "council", "multiple perspectives", or "cross-validate"

## Iron Laws

1. ALWAYS check CLI availability before dispatch -- never assume a model is present
2. ALWAYS anonymize responses before peer review -- model identity bias is real
3. NEVER skip Stage 2 for high-stakes decisions -- the peer review is the core innovation
4. ALWAYS preserve all 3 stages in output for transparency
5. ALWAYS set per-model timeout to prevent one slow model from blocking the council

## Anti-Patterns

| Anti-Pattern                           | Why Bad                              | Correct Approach                        |
| -------------------------------------- | ------------------------------------ | --------------------------------------- |
| Dispatching to unavailable CLIs        | Silent failure, missing responses    | Run verify-setup.mjs first              |
| Showing model names during peer review | Introduces identity bias             | Use anonymous labels (Response A, B, C) |
| Using only 2 models for council        | Peer review meaningless with 2       | Require minimum 3 for ranking value     |
| Ignoring failed model responses        | May miss degradation                 | Log failures, include in metadata       |
| Running council for simple questions   | Massive overhead for trivial queries | Reserve for high-stakes decisions       |

## Exit Codes

| Code | Meaning                                                         |
| ---- | --------------------------------------------------------------- |
| 0    | Council completed successfully (at least 2 models responded)    |
| 1    | Council failed (fewer than 2 models available or all timed out) |

## Configuration

| Env Var                  | Default           | Purpose                                        |
| ------------------------ | ----------------- | ---------------------------------------------- |
| `LLM_COUNCIL_TIMEOUT_MS` | 120000            | Per-model timeout for Stage 1 and Stage 2      |
| `LLM_COUNCIL_MIN_MODELS` | 2                 | Minimum models required for council to proceed |
| `LLM_COUNCIL_CHAIRMAN`   | (current session) | Chairman model for Stage 3 synthesis           |

## Integration Notes

- This skill does NOT require the llm-council-master FastAPI server
- Uses omega wrapper scripts directly via Bash backgrounding for parallelism
- Anonymized peer review is preserved from llm-council-master's design (its core innovation)
- Chairman synthesis can use the current Claude session (no additional CLI call needed)
- Temporary files stored in system temp dir, cleaned up after council completes
- Minimum 2 available models required for council to proceed
