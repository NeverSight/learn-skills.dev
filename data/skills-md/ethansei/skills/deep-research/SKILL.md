---
name: deep-research
description: >-
  Hypothesis-driven deep research swarm. Spawns specialist sub-agents to
  investigate a task across codebase patterns, web sources, MCP tools,
  installed skills, and project dependencies — with evidence grading and
  adversarial challenge. Activates on: research, investigate, discover,
  deep research, how should I, what's the best way, explore options,
  analyze approaches, scout, prior art, feasibility.
allowed-tools: Read Glob Grep Bash Agent Write Edit WebSearch WebFetch ListMcpResourcesTool ReadMcpResourceTool
metadata:
  version: 0.2.1
---

# Deep Research

Hypothesis-driven research swarm. Spawns specialist agents to investigate a task,
grades every finding by evidence quality, then adversarially challenges the emerging
conclusion before delivering a structured verdict.

## When This Skill Activates

Trigger on explicit research requests:
- User says: "research", "investigate", "discover", "how should I approach..."
- User asks: "what's the best way to...", "explore options for...", "deep research"
- User wants prior art, feasibility analysis, or approach comparison

Do NOT activate automatically on every task. This is an on-demand tool, not a gate.

## Phase 1: Hypothesis Formation

Before spawning agents, frame the research:

1. **Parse the task**: Extract the core question or goal. If ambiguous, ask the user
   to clarify before proceeding. Identify technology keywords (languages, frameworks,
   libraries mentioned or implied by the codebase).
2. **Identify repo context**: Run `git rev-parse --show-toplevel` to get `{repo_root}`.
   If this fails (not a git repo), set `{repo_root}` to the current working directory.
   Check for `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc. to identify
   the language/framework stack. Pass this as `{tech_stack}`. If no manifests are found,
   set `{tech_stack}` to the primary file extensions present or ask the user.
3. **speak-memory**: If `.speak-memory/index.md` exists and an active story matches
   the current work, read it for context. If `.speak-memory/` does not exist, skip.
4. **Form hypotheses**: State 1-3 hypotheses to investigate. For each:
   - **Question**: The specific question being answered
   - **Prior belief**: What you expect the answer to be (best guess before research)
   - **Disconfirming evidence**: What evidence would change the answer

   If the task is open-ended ("how should I build X?") and you have no prior belief,
   that's fine — set prior belief to "unknown" and frame the hypothesis as:
   "There is an established approach for X in this codebase/ecosystem."
   Disconfirming evidence: "No established patterns exist; this is novel."

5. **Set scope budget**: Declare upfront: "Budget: 5 research agents + 1 adversarial
   challenge = 6 agent calls, investigating N hypotheses." (substitute the actual
   hypothesis count for N). When budget is exhausted, synthesize what you have
   rather than expanding.

Present hypotheses to the user before proceeding:
```
Hypotheses:
1. [Question] — Prior belief: [X]. Would change if: [Y].
2. ...

Budget: 6 agents, [hypothesis count] questions. Proceed?
```

If the user declines or asks to revise, update the hypotheses and re-present.
Do not spawn agents until the user confirms.

## Phase 2: Evidence Gathering

Spawn all 5 agents **in a single message** (parallel Agent tool calls). Each agent
returns a JSON findings array — see `references/agent-roles.md` for full prompts.

| Agent | Subagent Type | Model | Focus |
|-------|---------------|-------|-------|
| codebase | Explore | opus | Existing patterns, utilities, similar implementations, conventions |
| web-research | general-purpose | opus | Solutions, libraries, best practices, documentation |
| tools-mcp | general-purpose | opus | Available MCP servers, tools, and resources |
| skills | general-purpose | opus | Installed skills and marketplace matches |
| dependencies | general-purpose | opus | Installed packages, version constraints, compatibility |

**Agent tool grants:**
- **codebase**: `Read, Glob, Grep` (read-only codebase exploration)
- **web-research**: `WebSearch, WebFetch` (external research)
- **tools-mcp**: `ListMcpResourcesTool, ReadMcpResourceTool` (tool discovery)
- **skills**: `Read, Glob, Grep, Bash` (read skills + `npx skills find`)
- **dependencies**: `Read, Glob, Grep, Bash` (read manifests + `npm ls`/`pip list`/`cargo tree`)

Pass each agent the hypotheses so they can focus their search, but instruct them
to also report unexpected relevant findings outside the hypothesis scope.

**Required output format** (every finding must include `evidence_tier`):
```json
[
  {
    "evidence_tier": "primary|secondary|speculative",
    "relevance": "high|medium|low",
    "source": "where this was found (file path, URL, tool name)",
    "finding": "what was discovered",
    "supports_hypothesis": "which hypothesis this relates to, or 'unexpected'",
    "recommendation": "how this finding applies to the task",
    "references": ["file paths or URLs for further reading"]
  }
]
```

**Evidence tiers:**
- **primary**: Direct from authoritative source — code you read, API response,
  official documentation, test output
- **secondary**: Reputable third-party — blog post with evidence, SO answer with
  code examples, well-maintained library README
- **speculative**: Inference, analogy, or "I think" — no direct source confirms this

Return empty array `[]` if no relevant findings in that domain.

Instruct each agent: "Return your top 10 findings maximum, prioritized by relevance.
Tag every finding with an evidence_tier. Never report speculative findings as primary."

**Error handling**: If an agent returns non-JSON output, strip code fences and attempt
JSON extraction. If extraction fails or the agent times out, treat as empty array `[]`
and log a warning. Continue with results from agents that succeeded.

## Phase 3: Synthesis

Merge all 5 finding arrays. Apply the synthesis rules from `references/synthesis.md`:

1. **Merge**: Collect all 5 JSON arrays into a single flat array. Tag each finding
   with its source agent name. Note which agents failed or returned empty.
2. **Deduplicate**: Merge identical findings; note corroborating sources.
3. **Resolve conflicts**: Flag when agents disagree; note the resolution.
4. **Grade evidence**: Flag any conclusion that rests entirely on speculative evidence.
   A conclusion needs at least one primary or secondary source to be credible.
5. **Rank**: Sort by evidence_tier (primary first), then relevance, then corroboration.
   Cap the merged array at **30 findings** — drop low-relevance speculative findings
   first to keep context manageable.
6. **Form preliminary conclusion**: Based on the ranked findings, form a preliminary
   answer to each hypothesis. State whether the prior belief was confirmed or changed.
7. **Generate approaches**: Propose **2-3 approaches** with trade-offs. Each approach
   must reference the evidence that supports it with tier tags.

## Phase 4: Adversarial Challenge

Before delivering findings, actively try to disprove the emerging conclusion.

Spawn one **devil's advocate** agent (`subagent_type: "general-purpose"`, `model: "opus"`).
Give it:
- The preliminary conclusion from Phase 3
- The recommended approach
- The hypotheses and their current status (confirmed/changed)

The devil's advocate agent's job:
- Search for disconfirming evidence using `WebSearch, WebFetch, Read, Glob, Grep`
- Find reasons the recommended approach would fail
- Identify assumptions that haven't been tested
- Look for alternatives the research may have missed

See `references/agent-roles.md` for the full devil's advocate prompt.

Handle the devil's advocate result:
- **`conclusion_holds`**: The conclusion survives — it's stronger. Note any speculative
  counterarguments as dissent but don't change the recommendation.
- **`conclusion_weakened`**: The devil's advocate found credible disconfirming evidence
  (primary or secondary tier). Revise the conclusion, note the revision, and
  **re-generate approaches** (re-run synthesis Step 7) to reflect the updated position.
- **`conclusion_overturned`**: The recommended approach is fundamentally flawed. Discard
  it, revise all affected hypothesis conclusions, and **re-generate approaches from
  scratch** based on the combined original + adversarial evidence.

**Error handling**: If the devil's advocate agent fails (non-JSON output, timeout, or
invalid structure), log a warning: "Devil's advocate failed — conclusion not adversarially
tested. Reduce confidence by one level." Continue to Phase 5 with the untested conclusion.

## Phase 5: Verdict

Output a structured verdict (use `assets/report-template.md` for formatting):

```
VERDICT: [one sentence answer]
CONFIDENCE: high|medium|low — [justification]
EVIDENCE:
  1. [primary] source — finding
  2. [secondary] source — finding
  3. ...
DISSENT: [strongest counterargument from devil's advocate]
ACTION: [what to do next — implement X, investigate Y further, do nothing]
```

After the verdict, output the **structured artifact** for downstream skills:

```json
{
  "task": "original task description",
  "tech_stack": ["identified technologies"],
  "hypotheses": [
    {
      "question": "...",
      "prior_belief": "...",
      "conclusion": "confirmed|changed|inconclusive",
      "conclusion_detail": "what we found"
    }
  ],
  "metadata": {
    "agents_completed": ["codebase", "web-research", "tools-mcp", "skills", "dependencies", "devils-advocate"],
    "agents_failed": [],
    "total_findings": 0,
    "speculative_only_conclusions": 0,
    "timestamp": "ISO-8601"
  },
  "findings": [... merged findings array (high/medium only, with evidence_tier) ...],
  "conflicts": [
    {
      "description": "what conflicts",
      "agents": ["which agents disagree"],
      "resolution": "how resolved, or null if user must decide"
    }
  ],
  "verdict": {
    "summary": "one sentence",
    "confidence": "high|medium|low",
    "confidence_justification": "why this confidence level",
    "dissent": "strongest counterargument"
  },
  "approaches": [
    {
      "name": "Approach A",
      "summary": "one-line description",
      "pros": ["..."],
      "cons": ["..."],
      "recommended": true,
      "evidence": ["[primary] source — finding", "..."],
      "relevant_files": ["paths from codebase agent"],
      "relevant_tools": ["MCP tools/skills discovered"],
      "dependencies_needed": ["new packages, if any"],
      "estimated_complexity": "low|medium|high"
    }
  ]
}
```

**No-findings edge case**: If all agents return empty arrays, output the structured
artifact with `findings: []`, `approaches: []`, and `verdict.confidence: "low"`.
Set `verdict.summary` to: "Research found no directly relevant prior art. Recommend
exploratory implementation or breaking the task into smaller sub-problems."

**speak-memory**: If an active story was loaded in Phase 1, use Write/Edit to update
the story file — append to Recent Activity and update Current Context.

## Key Constraints

- All research agents: **Opus** (`model: "opus"`) for maximum research quality.
- **Agent execution caps**: Research agents: `max_turns: 30`. Devil's advocate: `max_turns: 20`.
- Max **2 levels of nesting**: orchestrator → specialist. Specialists never spawn agents.
- **Scope budget**: 5 research agents + 1 devil's advocate = 6 total. Do not expand.
- **Findings cap**: Max 30 findings enter synthesis (after merge + dedup). Drop
  low-relevance speculative findings first.
- All **sub-agents** are read-only — no code modifications, no git changes. The
  orchestrator may write to `.speak-memory/` only.
- Bash (sub-agents only) limited to dependency queries (`npm ls`, `pip list`, `cargo tree`)
  and skill search (`npx skills find`). No other Bash commands.
- Conclusions resting entirely on speculative evidence must be flagged as low confidence.
- The structured artifact stays in conversation context — no file writing.

## Closing Checklist

Do not declare the research done until all boxes are checked:

- [ ] Hypotheses stated with prior beliefs and disconfirming criteria
- [ ] All 5 research agents completed (returned valid JSON) or failed (logged as warning)
- [ ] Every finding tagged with evidence_tier (primary/secondary/speculative)
- [ ] Preliminary conclusion formed and approaches generated
- [ ] Devil's advocate challenged the conclusion
- [ ] Structured verdict delivered (verdict, confidence, evidence, dissent, action)
- [ ] Structured artifact output for downstream consumption
- [ ] speak-memory story updated (if applicable)

## Reference Files

Load only when needed:

- `references/agent-roles.md` — Full prompt templates for each research agent + devil's advocate
- `references/synthesis.md` — Evidence grading, dedup, conflict resolution, approach generation
- `assets/report-template.md` — Verdict and report format
