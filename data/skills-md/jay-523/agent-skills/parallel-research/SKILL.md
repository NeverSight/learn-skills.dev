---
name: parallel-research
description: Decompose a research question into MECE domains and run parallel Claude agents via tmux
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[research topic or question]"
---

# /parallel-research -- Parallel Web Research via tmux + claude -p

Decompose a research question into MECE domains, spawn parallel Claude
agents in tmux panes (up to 12), each running `claude -p` with
pre-approved web tools. Collect findings into structured output files.

## Argument

A research topic or question to investigate broadly. Example:
"state of agentic coding patterns Dec 2025 - Feb 2026"

## Procedure

### Phase 1 -- Understand

Clarify the research question. Identify:
- The core topic
- The timeframe
- How many dimensions / angles the user wants covered
- Whether the user wants adversarial / contrarian coverage

If unclear, ask the user before proceeding.

### Phase 2 -- Decompose into MECE Domains

Split the research into 3-6 independent domains. For each domain,
create 2-3 search variants (a/b/c) that approach the same domain from
different angles. This multiplies coverage without redundancy.

Decomposition rules:
- Divide by **research domain**, NOT by source type. Each agent owns
  a vertical slice of a topic (e.g., "enterprise adoption", "failure
  stories"), not a horizontal layer (e.g., "find all tweets", "find
  all blogs"). Horizontal decomposition causes massive redundancy.
- Each variant within a domain should use different search terms and
  angles to maximize coverage.
- All domains together should be collectively exhaustive -- no gaps.

Present the decomposition table and wait for user approval:

```
| Domain | Agent A (Variant) | Agent B (Variant) | Model |
|--------|-------------------|-------------------|-------|
| Voices | Social media power users | Industry leaders & engineers | sonnet |
| Blogs  | Workflow pattern posts | Code quality problem posts | sonnet |
| Critics | Failure postmortems | Skeptics & contrarians | opus |
```

The **Model** column controls which Claude model each domain's agents
use. Default is `claude-sonnet-4-6`. Use `opus` for domains that
require deep analysis or nuanced reasoning; use `haiku` for simple
URL-scraping or aggregation agents. This maps to the second argument
of `run-agent.sh`.

Do NOT proceed until the user approves this decomposition.

### Phase 3 -- Create Agent Directories and Prompts

Create the directory structure:

```bash
mkdir -p research-agents/{agent-name-a,agent-name-b,...}
mkdir -p research-agents/outputs
```

For each agent, write `research-agents/{agent-name}/prompt.md` with
this structure:

```markdown
You are a research agent. DO NOT modify any files in any codebase.
Your ONLY job is to search the web and compile findings.

# Mission: [Specific research goal for this agent]

## Search Strategy
[10+ specific search queries, tailored to this agent's angle]

## What to Capture
[Structured template: what fields to record per finding]

## Output Format
[How to organize the output -- categories, ranking, etc.]
```

Prompt design rules:
- **Always** start with "DO NOT modify any files" -- prevents agents
  from touching code
- **10+ search queries per agent** -- ensures breadth
- **Structured output format** -- makes aggregation possible later
- **Variance between a/b agents** -- different search terms for the
  same domain to catch what the other misses

### Phase 4 -- Create Launcher Script

Write `research-agents/run-agent.sh`:

```bash
#!/bin/bash
# Usage: bash run-agent.sh /path/to/agent-dir [model]
# Pipes the agent prompt to claude -p with pre-approved web tools.
# Writes output to output.md and prints a COMPLETE marker when done.
cd "$1"
MODEL="${2:-claude-sonnet-4-6}"
echo "=== Starting research agent: $(basename $1) with model $MODEL ==="
echo "=== $(date) ==="
echo ""
cat prompt.md | claude -p \
  --model "$MODEL" \
  --allowedTools "WebSearch,WebFetch,Bash,Read,Write,Grep,Glob" \
  2>&1 | tee output.md
echo ""
echo "=== Agent $(basename $1) COMPLETE at $(date) ==="
```

Make it executable: `chmod +x research-agents/run-agent.sh`

CRITICAL details in this script:
- **Pipe prompt via stdin** (`cat prompt.md | claude -p`). NEVER pass
  the prompt as a positional argument after `--allowedTools` -- the
  variadic flag will consume it as a tool name.
- **Comma-separated tools** (`"WebSearch,WebFetch,..."`). NEVER use
  spaces -- they cause the same variadic consumption problem.
- **--allowedTools is mandatory**. `claude -p` runs non-interactively
  and cannot prompt for permission approval. Without this flag, every
  WebSearch call gets denied silently and the agent exits with
  "I'm blocked".
- `tee output.md` streams to both the terminal and a file.

### Phase 5 -- Build tmux Session

Calculate layout: ceil(total_agents / 4) windows, 4 panes each.

Create the session one window at a time. **Validate each window before
creating the next.**

```bash
# Create first window
tmux new-session -d -s research -n "{window-name}" -x 220 -y 55
tmux split-window -t research:{window-name}
tmux split-window -t research:{window-name}
tmux split-window -t research:{window-name}
tmux select-layout -t research:{window-name} tiled

# VALIDATE before continuing
tmux list-windows -t research -F "#{window_name}: #{window_panes} panes"
```

Repeat for additional windows with `tmux new-window`.

CRITICAL: **Always validate pane count** after creating each window.
Never proceed to launching agents without confirming the panes exist.
Sending `tmux send-keys` to non-existent panes can crash the tmux
server -- killing ALL tmux sessions on the machine, not just yours.

### Phase 6 -- Launch Agents

Send the launcher command to each pane, one window at a time:

```bash
BASE="$(pwd)/research-agents"
L="$BASE/run-agent.sh"

# Pass model as second arg (from decomposition table's Model column)
tmux send-keys -t research:{window}.0 "bash $L $BASE/{agent-a} claude-sonnet-4-6" Enter
tmux send-keys -t research:{window}.1 "bash $L $BASE/{agent-b} claude-sonnet-4-6" Enter
tmux send-keys -t research:{window}.2 "bash $L $BASE/{agent-c} claude-opus-4-6" Enter
tmux send-keys -t research:{window}.3 "bash $L $BASE/{agent-d} claude-sonnet-4-6" Enter
```

Match the model argument to the Model column from the approved
decomposition table. Omitting it defaults to `claude-sonnet-4-6`.

After launching all agents, verify the processes are running:

```bash
ps aux | grep "claude -p" | grep -v grep | wc -l
```

The count should match the number of agents launched.

Print monitoring instructions for the user:

```
## Parallel Research Agents Running

Attach to session:     tmux attach -t research
Switch windows:        Ctrl-b n (next) / Ctrl-b p (previous)
Switch panes:          Ctrl-b + arrow keys
Zoom a pane:           Ctrl-b z (toggle)
Kill session:          tmux kill-session -t research

Check progress:
  ls -la research-agents/*/output.md
```

### Phase 7 -- Monitor and Collect

#### Automatic Completion Detection

Use the `wait-for-text.sh` helper from the `/tmux` skill to poll each
pane for the COMPLETE marker that `run-agent.sh` prints on exit.

Build a polling loop that checks all panes:

```bash
WAIT="$HOME/Developer/personal_projects/agent-skills/skills/tmux/scripts/wait-for-text.sh"
TIMEOUT=600  # 10 minutes per agent; adjust as needed

all_done=true
for pane_id in {list of session:window.pane targets}; do
  agent_name="{name for this pane}"
  if bash "$WAIT" -t "$pane_id" -p "COMPLETE" -T "$TIMEOUT" -i 5; then
    echo "$agent_name: DONE"
  else
    echo "$agent_name: TIMED OUT or FAILED -- check pane manually"
    all_done=false
  fi
done

if $all_done; then
  echo "All agents complete."
else
  echo "Some agents did not finish. Check timed-out panes."
fi
```

Run this loop SEQUENTIALLY (one `wait-for-text.sh` call per agent) so
that each agent gets the full timeout. The loop will block until each
agent finishes or times out.

#### Manual Progress Check

If you prefer a quick status check instead of blocking:

```bash
for agent in {list-of-agents}; do
  dir="research-agents/$agent"
  if [ -s "$dir/output.md" ]; then
    bytes=$(wc -c < "$dir/output.md")
    echo "$agent: ${bytes} bytes"
  else
    echo "$agent: still running..."
  fi
done
```

Note: `tee` buffers lazily. Empty output files for 30-60 seconds is
normal while agents are doing web searches. Verify processes are alive
with `ps aux | grep "claude -p"` rather than relying on file sizes.

When all agents have completed, report the final output sizes and
proceed to synthesis.

### Phase 8 -- Synthesize

Read every `research-agents/*/output.md` file. Cross-reference the
findings and produce `research-agents/outputs/synthesis.md` with this
structure:

```markdown
# Research Synthesis: {topic}

## Executive Summary
[3-5 sentences capturing the most important findings across all agents]

## Key Findings by Domain
### {Domain 1}
- [Bullet points synthesizing findings from agents in this domain]
- [Include source attribution: "Agent {name} found..."]

### {Domain 2}
...

## Cross-Domain Patterns
[Themes, trends, or insights that appear across multiple domains.
These are the highest-value findings -- they show convergence.]

## Contradictions and Tensions
[Where agents found conflicting information or opposing viewpoints.
Note which sources support each side.]

## Gaps and Open Questions
[What the research did NOT cover well. Topics that need deeper
investigation. Questions raised by the findings.]

## Raw Source Index
| Agent | Domain | Output File | Key Sources |
|-------|--------|-------------|-------------|
| {name} | {domain} | {path} | [list of URLs/papers cited] |
```

Rules for synthesis:
- **Cross-reference aggressively**. The value is in connections between
  domains, not summaries of individual agents.
- **Preserve attribution**. Every claim traces back to a specific agent
  and source.
- **Flag contradictions explicitly**. Don't silently pick a side.
- **Keep the raw outputs**. Synthesis is additive, not a replacement.

Present the synthesis for user review before finalizing.

## Troubleshooting

**Check agent status**
Run the health-check recipe from `/tmux` to classify every pane:
```bash
DIAG="$HOME/Developer/personal_projects/agent-skills/skills/tmux/scripts/diagnose-agents.sh"
bash "$DIAG" research "research-agents/*/output.md"
```
Each pane is classified as DONE, WORKING, FAILED, or UNKNOWN. See the
`/tmux` skill's "Health-Check Running Agents" recipe for details on
what each state means and how it's detected.

**FAILED state -- what to do**
Inspect the pane for the root cause:
```bash
tmux capture-pane -t research:{window}.{pane} -p -S - | tail -30
```
Common causes: rate limit hit, permission denial (missing
`--allowedTools`), traceback, or OOM. Fix the cause and re-launch the
agent (see below).

**DONE but no output.md**
This is a `tee` buffering issue. The agent finished (COMPLETE marker
present in the pane) but the file wasn't flushed. Capture the pane
scrollback directly:
```bash
tmux capture-pane -t research:{window}.{pane} -p -S - > research-agents/{agent}/output.md
```

**Re-running a single failed agent**
Send the launcher command to the same pane (or a new one):
```bash
tmux send-keys -t research:{window}.{pane} "bash $L $BASE/{agent-name} {model}" Enter
```
The previous output.md will be overwritten by `tee`.

**tmux session died**
Re-create the session and windows (Phase 5). Run `diagnose-agents.sh`
or check which agents have output.md with content. Only re-launch
agents that didn't complete.

**Rate limits across many agents**
If multiple agents hit rate limits simultaneously, reduce the number
of concurrent agents or stagger launches with `sleep 30` between
`send-keys` commands.

## Important

- Always decompose by **research domain**, never by source type.
- Always wait for user approval of the decomposition before creating
  directories.
- NEVER pass the prompt as a positional argument to `claude -p` after
  `--allowedTools`. Always pipe via stdin.
- NEVER use space-separated tool names in `--allowedTools`. Always use
  commas.
- ALWAYS validate tmux panes exist before sending commands to them.
  Validate after each window creation, not at the end.
- ALWAYS launch one window of agents at a time. Verify that window's
  panes are alive before moving to the next window.
- The tmux session name is `research`. Do not reuse a session name
  that already exists -- check with `tmux has-session -t research`
  first and pick a different name if it exists.
- Do NOT modify any files in the codebase. This skill is research-only.

