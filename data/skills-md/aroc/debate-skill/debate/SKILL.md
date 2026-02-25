---
name: debate
description: |
  Orchestrate a debate between Claude and Codex to reach consensus.
  Use when the user asks for a "second opinion", "debate", "consensus",
  "crosscheck", or wants another model to review a proposal or diff.
allowed-tools: Read, Glob, Grep, Bash
---

# Debate Skill

Orchestrate a back-and-forth debate between two AI models (Claude and Codex) until they reach consensus on a technical decision, code review, or root cause analysis.

## Activation

This skill activates when:
- User invokes `/debate [topic]`
- User asks for a "second opinion", "debate", "consensus", or "crosscheck"
- User wants another model to review a proposal, diff, or decision

## Arguments

- `--vs <claude|codex>`: Choose opponent (default: auto-detect opposite of current)
- `--model <model>`: Specify opponent's model (e.g., `opus`, `sonnet`, `o3`, `gpt-4.1`)
- `--reasoning <level>`: Codex reasoning effort: `low`, `medium`, `high` (default: from config)
- `--quick`: Single round only, get feedback without iterating to consensus
- Topic: Any technical question, code review request, or decision point

### Examples

```bash
# Debate with Codex (default when running from Claude)
/debate should we use Redis or Memcached?

# Explicitly debate with Claude (e.g., Claude vs Claude)
/debate --vs claude --model opus should we use a monorepo?

# Debate with Codex using a specific model
/debate --vs codex --model o3 review my authentication changes

# Debate with Codex with low reasoning (faster, cheaper)
/debate --vs codex --model gpt-5.3-codex --reasoning low quick sanity check

# Debate with Codex with high reasoning (thorough analysis)
/debate --vs codex --reasoning high review this complex algorithm

# Quick single-round feedback from Codex
/debate --quick --vs codex what do you think of this API design?
```

### Available Models

The `--model` value is passed directly to the CLI, so use whatever model identifiers that CLI accepts.

**Claude CLI models:**
- Shorthand: `opus`, `sonnet`, `haiku`
- Full IDs: `claude-opus-4-5-20251101`, `claude-sonnet-4-6-20250514`, etc.
- Check available models: `claude --help` or your Claude config

**Codex CLI models:**
- Examples: `o3`, `o4-mini`, `gpt-4.1`, `gpt-5.3-codex`
- Check available models: `codex --help` or your Codex config
- Default is determined by your `~/.codex/config.toml`

## Orchestration Steps

**Important:** The skill's base directory is provided when the skill is invoked (shown as "Base directory for this skill: ..."). Use this as `SKILL_DIR` in all script paths below.

### Step 1: Gather Context

Based on the topic, gather relevant context:

```bash
# For code changes
git diff HEAD 2>/dev/null || git diff --staged 2>/dev/null

# For specific files, read them
# For architecture discussions, explore relevant code
```

### Step 2: Formulate Initial Proposal

As Claude, analyze the topic and formulate a clear proposal:

```
## Topic
[User's original question/request]

## Context
[Relevant code, diffs, or information]

## My Proposal
[Your analysis and recommendation]

## Key Points
- [Point 1]
- [Point 2]
- [Point 3]
```

### Step 3: Determine Opponent

Parse the user's arguments to determine:
1. **Opponent CLI**: From `--vs` flag, or default to the opposite of current (if running from Claude, default to codex; if from Codex, default to claude)
2. **Opponent Model**: From `--model` flag, or omit to use CLI default

Detect current environment:
```bash
# Check if running from Claude
if [ -n "$CLAUDE_SESSION_ID" ] || [ -n "$CLAUDE_CODE_ENTRYPOINT" ]; then
    CURRENT="claude"
    DEFAULT_OPPONENT="codex"
else
    CURRENT="codex"
    DEFAULT_OPPONENT="claude"
fi
```

### Step 4: Invoke Opponent

Use the invoke script with explicit opponent, optional model, and optional reasoning level:

```bash
# Basic invocation (opponent required)
bash $SKILL_DIR/scripts/invoke_other.sh \
    --opponent codex \
    "Your prompt here"

# With specific model
bash $SKILL_DIR/scripts/invoke_other.sh \
    --opponent claude \
    --model opus \
    "Your prompt here"

# With model and reasoning level (Codex only)
bash $SKILL_DIR/scripts/invoke_other.sh \
    --opponent codex \
    --model gpt-5.3-codex \
    --reasoning high \
    "Your prompt here"
```

Example critique prompt:

```bash
bash $SKILL_DIR/scripts/invoke_other.sh \
    --opponent "$OPPONENT" \
    ${MODEL:+--model "$MODEL"} \
    ${REASONING:+--reasoning "$REASONING"} \
    "
You are reviewing a proposal.

## Context
[Include gathered context]

## Proposal
[Your proposal]

## Your Task
Evaluate this proposal critically. Consider:
- Technical correctness
- Edge cases missed
- Alternative approaches
- Potential issues

End your response with exactly one verdict:
- AGREE: [confirmation and why]
- REVISE: [specific changes needed]
- DISAGREE: [fundamental issues]
"
```

### Step 5: Parse Verdict

The invoke script outputs the response file path to stdout. Capture it and parse:

```bash
# Capture the output file path from the invoke script
RESPONSE_FILE=$(bash $SKILL_DIR/scripts/invoke_other.sh \
    --opponent "$OPPONENT" \
    ${MODEL:+--model "$MODEL"} \
    ${REASONING:+--reasoning "$REASONING"} \
    "Your critique prompt here")

# Parse the verdict from the response
python3 $SKILL_DIR/scripts/parse_verdict.py "$RESPONSE_FILE"
```

This returns: `AGREE|REVISE|DISAGREE` and the explanation.

### Step 6: Iterate Based on Verdict

**If AGREE:**
- Consensus reached! Present final solution to user.

**If REVISE:**
- Incorporate the suggested changes into your proposal
- Re-invoke the opponent with the revised proposal
- Continue until AGREE or max rounds

**If DISAGREE:**
- Address the fundamental concerns raised
- Formulate a counter-proposal or clarification
- Re-invoke the opponent
- Continue until AGREE or max rounds

### Step 7: Handle Max Rounds

If 5 rounds pass without consensus, generate a disagreement summary (see below).

## Quick Mode (--quick)

When `--quick` flag is present:
1. Formulate initial proposal
2. Get single critique from opposing model
3. Present both perspectives to user
4. Do NOT iterate - stop after one round regardless of verdict

## Output Format

Display the debate to the user in this format. Use the actual model names (e.g., "CLAUDE (opus)" or "CODEX (o3)"):

```
═══════════════════════════════════════════════
CONSENSUS DEBATE: [Topic]
Participants: [Current] vs [Opponent] ([model if specified])
═══════════════════════════════════════════════

--- Round 1 ---
[CURRENT]: [proposal]

[OPPONENT]: [critique]
Verdict: [AGREE|REVISE|DISAGREE]

--- Round 2 --- (if needed)
[CURRENT]: [revised proposal]

[OPPONENT]: [response]
Verdict: [AGREE|REVISE|DISAGREE]

═══════════════════════════════════════════════
CONSENSUS REACHED (Round N)
═══════════════════════════════════════════════
[Final agreed solution with key points]
```

## No Consensus Summary

When max rounds (5) reached without consensus:

```
═══════════════════════════════════════════════
NO CONSENSUS REACHED (5 rounds)
═══════════════════════════════════════════════

## Points of Agreement
- [Things both models agreed on]

## Points of Disagreement
- [Issue 1]: [Current] thinks X, [Opponent] thinks Y
- [Issue 2]: ...

## Root Cause of Disagreement
[Why consensus couldn't be reached - e.g., different assumptions,
missing information, genuinely valid competing approaches]

## Recommendation
[Best path forward given the disagreement]
═══════════════════════════════════════════════
```

## Error Handling

**CLI not installed:**
```bash
if ! command -v codex &> /dev/null && ! command -v claude &> /dev/null; then
    echo "Neither codex nor claude CLI found. Falling back to self-critique mode."
    # Provide self-critique instead
fi
```

**Network/timeout error:**
- Retry once
- If still fails, present partial results with note about the error

**Empty response:**
- Treat as implicit DISAGREE
- Request clarification in next round

## Prompt Templates

### Initial Critique Request

```
You are {opponent_name}, reviewing a proposal from {current_name}.

## Original Question
{user_topic}

## Context
{gathered_context}

## Proposal Being Reviewed
{proposal}

## Your Task
Critically evaluate this proposal. Consider:
1. Is the technical approach correct?
2. Are there edge cases or failure modes missed?
3. Are there better alternatives?
4. What are the risks or downsides?

Be constructive but thorough. If you agree, explain why it's solid.
If you have concerns, be specific about what should change.

End with exactly one of:
- AGREE: [your confirmation and reasoning]
- REVISE: [specific changes you recommend]
- DISAGREE: [fundamental issues that need addressing]
```

### Revision Request

```
You are {opponent_name}, continuing a debate with {current_name}.

## Original Question
{user_topic}

## Previous Exchange
{conversation_history}

## Latest Revision
{revised_proposal}

## Your Task
Evaluate whether the revision addresses your previous concerns.

End with exactly one of:
- AGREE: [if concerns are resolved]
- REVISE: [if minor issues remain]
- DISAGREE: [if fundamental issues persist]
```

## Implementation Notes

- Accumulate conversation history between rounds
- Each model should see the full debate context
- Keep proposals concise but complete
- Focus on technical merit, not rhetorical style
- Maximum response from opposing model: ~2000 tokens
