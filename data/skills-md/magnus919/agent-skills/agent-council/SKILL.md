---
name: agent-council
description: >-
  Run a structured multi-agent debate by spawning a panel of expert
  agents on any question, with convergence-aware iteration and typed
  synthesis output via the `agent-council` CLI. Use when a decision has
  genuine tradeoffs, high stakes, or hidden assumptions worth adversarial
  collaboration, or when confidence diagnostics matter more than a
  single recommendation. Compatible with any AI agent harness that
  supports agentskills.io skills (Claude Code, Cursor, Hermes Agent,
  OpenHands, etc.). Do not use for simple factual lookups, tasks with a
  clear correct answer, routine single-perspective work, or code
  execution and tool orchestration beyond debate.
license: MIT
compatibility: Requires Python 3.10+ and pydantic-ai. CLI tool installs via pip.
metadata:
  source: https://github.com/magnus919/agent-skills/tree/main/agent-council
  spec-version: "1.1"
---

# Agent Council

Spawn a panel of expert agents to debate any question. The council runs a structured protocol — compose, premortem, position, cross-examination (iterative), synthesis — and produces a decision landscape with convergence diagnostics.

## When to Use

Invoke the council when any of these apply:

- The question has genuine tradeoffs with no clear correct answer
- You want multi-perspective analysis to surface hidden assumptions
- A decision would benefit from adversarial collaboration
- You want confidence diagnostics (not just a recommendation)
- The question has high stakes or irreversible consequences

**Signal phrases:** "Let's get multiple perspectives on this" / "Debate this: X" / "What would experts say about X" / "What are we missing?"

## Quick Start

### 1. Install

```bash
# One-time setup
pip install pydantic-ai
pip install agent-council

# Or install from this skill directory:
python3 scripts/bootstrap.py
```

### 2. Configure

```bash
export AGENT_COUNCIL_API_KEY="sk-..."
export AGENT_COUNCIL_MODEL="openai:gpt-5.6-luna"
```

### 3. Run

```bash
agent-council "Should we use Postgres or SQLite for this service?"
```

## Command Reference

```
agent-council [OPTIONS] <question>

Options:
  --agents, -n {3,4,5,6,7}  Number of agents (default: 5)
  --mode, -m {quick,medium,deep}  Debate depth (default: medium)
  --profiles TEXT          Comma-separated profile names from the hermes-profiles
                           library (e.g. "debugger,researcher,product-manager")
  --persona-file PATH      JSON file with custom agent personas
  --json                   Output structured JSON instead of markdown
  --verbose, -v            Show phase-by-phase progress
  --max-rounds INTEGER     Max cross-examination rounds (default: 4)
  --convergence FLOAT      Convergence threshold (default: 0.10)
```

### Mode Selection

| Mode | Agents | Rounds | When to use |
|------|--------|--------|-------------|
| `quick` | 3 | 1 cross-examine round | Low-stakes check, fast answer needed |
| `medium` (default) | 5 | Eval-driven, up to 4 rounds | Standard decisions |
| `deep` | 7 | Eval-driven, up to 4 rounds | High-stakes, hidden assumptions |

## Profile Selection

In a recursive source checkout, the council auto-selects relevant real professional profiles from the included [hermes-profiles](https://github.com/magnus919/hermes-profiles) library. Each profile has a SOUL.md — an identity document with real methodology, values, and operating principles — rather than a fabricated persona. Pip and wheel installs do not bundle that library; use generated or user-supplied personas instead.

### Auto-selection

When no `--profiles` flag is given, the council scores each profile's description against your question using keyword overlap. The top N most relevant profiles are selected. This works best for focused, single-domain questions.

### Explicit selection

```bash
agent-council --profiles debugger,data-scientist,product-manager "What architecture should we choose?"
```

Comma-separated profile names. Available profiles include: `ceo`, `cfo`, `cmo`, `coo`, `cpo`, `cto`, `curator`, `data-architect`, `data-engineer`, `data-scientist`, `debugger`, `editor`, `frontend-engineer`, `ml-engineer`, `orchestrator`, `product-manager`, `researcher`, `reviewer`, `security-engineer`, `site-reliability-engineer`, `technical-architect`, `technical-writer`, `ux-designer`, `verifier`, `wonderer`, `writer`, and more.

### Choosing a Profile Source

Three ways to populate the council, with different tradeoffs:

| Method | Best for | Diversity | Setup |
|--------|----------|-----------|-------|
| `--profiles` (auto-select) | Single-domain questions with clear keywords | High — profiles have real SOUL.md methodology | Recursive source checkout required |
| `--profiles name1,name2` | Targeted debates where you know the stakeholders | Highest — you pick specific methodological voices | Recursive source checkout and profile names |
| `--persona-file file.json` | Full control over agent identities, custom domains | Variable — depends on how you design them | Create a JSON file |
| Auto (no flag) | Default — uses profiles if available, falls back to generated | Good — varies with available profiles | No setup for generated personas; recursive source checkout for real profiles |

For most cases, let it auto-select or use `--profiles` with 3-5 names. Only use `--persona-file` when you need specific invented expertise that doesn't map to any existing profile.

### Custom personas (fallback)

If the profile library is unavailable or you want full control, use `--persona-file` to supply your own persona definitions. If neither `--profiles` nor `--persona-file` is provided, the council auto-selects profiles from the library; if the library is missing, it falls back to LLM-generated personas.

## How It Works

### Pipeline

```
Compose ──► Premortem ──► Position ──► Cross-examine ──► [eval] ──► Synthesis
  (1)        (parallel)    (parallel)    (iterative loop)    ↑        (1)

                    ┌── converged ──────┐
                    ├── diminishing_ret │
    eval ───────────┼── genuine_disagr──┼──► Synthesis
                    └── continue ───────┘
                          ↓
                   Cross-examine (next round)
```

### Phases

| Phase | What happens | Method |
|-------|-------------|--------|
| **Compose** | A single LLM call generates N expert personas tuned to the question | 1 call |
| **Premortem** | Each agent independently imagines how the decision already failed — bypasses positional commitment bias | N parallel calls |
| **Position** | Each agent forms an independent position, referencing their own premortem | N parallel calls |
| **Cross-examine** | Each agent reads all other positions and responds — concedes, disagrees, updates confidence | N parallel calls per round |
| **Eval** | Convergence detection: measures dispersion, argument novelty, concession rate. Decides whether to loop or stop | Algorithmic |
| **Synthesis** | Collates all phases into a structured decision landscape with LLM-generated narrative | 1 call |

### Convergence Detection

The council doesn't use a fixed number of rounds. After each cross-examination round, it measures:

- **Confidence dispersion** — standard deviation of agent confidence scores. Below threshold = converged.
- **Argument novelty** — new arguments not seen in prior rounds. Near zero = diminishing returns.
- **Concession rate** — points where agents shifted position. Zero + no new arguments = stalled.

Stopping conditions:
| Condition | Meaning |
|-----------|---------|
| `converged` | Dispersion below threshold, confidence stable. Genuine agreement. |
| `diminishing_returns` | No new arguments or concessions. Nothing more to surface. |
| `genuine_disagreement` | Dispersion widened, positions hardened. Summary of irreducible tension. |
| `max_rounds` | Hard cap reached. Inconclusive — principal must decide. |

## Bootstrapping

If `agent-council` is not available on PATH, the invoking agent should run:

```bash
python3 scripts/bootstrap.py
```

This installs the package from the skill directory using the current Python's pip, falling back to pipx. No PyPI dependency for the bootstrap path — the package ships inside the skill directory.

**If bootstrap fails:** Run one of these manually:
```bash
pip install pydantic-ai
pip install agent-council

# Or from this directory:
python3 -m pip install -e /path/to/agent-council/
```

## Available Scripts

This skill bundles one script; there are no others to discover.

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/bootstrap.py` | First-run installer: checks whether `agent-council` is already on PATH and, if not, installs the package from the skill directory using the current Python's pip, falling back to pipx. Run it whenever `agent-council` is not found on PATH (an invoking agent should run it automatically in that case); it exits 0 when the CLI is available and 1 with manual-install instructions when it could not install. If bootstrap fails, follow the manual steps above. | `python3 scripts/bootstrap.py` |

## Configuration

| Env var | Required | Default | Description |
|---------|----------|---------|-------------|
| `AGENT_COUNCIL_API_KEY` | Yes | — | API key for your LLM provider |
| `AGENT_COUNCIL_MODEL` | No | `openai:gpt-5.6-luna` | Model string (`provider/model`) |
| `AGENT_COUNCIL_BASE_URL` | No | Provider default | Custom API endpoint (OpenRouter, LiteLLM, etc.) |

You can set these as environment variables or create a `.env` file in the directory you run `agent-council` from:

```bash
# .env file
AGENT_COUNCIL_API_KEY=sk-...
AGENT_COUNCIL_MODEL=openai:gpt-5.6-luna
```

Environment variables take precedence over `.env` file values.

Model strings follow PydanticAI convention: `openai:gpt-5.6-luna`, `anthropic:claude-sonnet-4-20250514`, `deepseek:deepseek-v4-flash`, `google:gemini-2.0-flash`.

## Output

The synthesis report is a structured decision landscape. In markdown mode it includes:

1. **Confidence dispersion table** — per-round confidence metrics with diagnostic
2. **Shared risks** — failure modes from the pre-mortem (pre-positional, uncontaminated)
3. **Shared concerns** — what survived cross-examination as genuine shared risk
4. **Remaining disagreements** — positions that did not resolve
5. **Assumptions per position** — what must hold for each position to be valid
6. **Principal's path** — narrative synthesis of the decision landscape

Use `--json` for programmatic consumption. The JSON output follows this structure:

```json
{
  "question": "string",
  "mode": "quick|medium|deep",
  "num_agents": 3,
  "rounds_completed": 2,
  "stopped_reason": "converged|max_rounds|diminishing_returns|genuine_disagreement",
  "confidence_history": [
    {"round": 1, "mean_confidence": 0.74, "dispersion": 0.061, "new_arguments": 20, "concessions_made": 17}
  ],
  "shared_risks": [{"description": "...", "severity": "low|medium|high", "phase_discovered": "premortem"}],
  "shared_concerns": ["..."],
  "disagreements": [{"topic": "...", "positions": {"agent_a": "position_a", "agent_b": "position_b"}}],
  "assumptions_per_position": {"agent_name": ["assumption1", "assumption2"]},
  "principal_path": "narrative text"
}
```

### Claims Verification

Every synthesis output includes a post-debate verification scan. A separate LLM call reads the narrative synthesis and identifies any claims about verifiable external facts (domain availability, package namespace status, pricing, statistics) that the debate could not have verified from its own reasoning. Flagged claims are appended as a **⚠️ Claims Not Verified** section:

```
⚠️  Claims Not Verified
The following assertions in this synthesis could not be verified
by the council's own reasoning and should be checked before acting:
  • "Dialekt passes all five checks..." — domain availability:
    No evidence the council checked domain registries
```

This is not a rejection of the synthesis — it is a quality signal. Claims in this section should be treated as hypotheses to verify, not as facts.

### Reading the Convergence Diagnostic

The confidence dispersion table tells you whether the debate was productive:

| Pattern | Meaning | What to do |
|---------|---------|------------|
| Mean confidence DROPPED, dispersion WIDENED | Council surfaced genuine doubt — healthy debate | Trust the shared concerns; investigate the newly surfaced risks |
| Mean confidence ROSE, dispersion NARROWED | Genuine convergence — agents convinced each other | The strongest signal; highest-confidence path forward |
| Mean confidence STABLE, dispersion NARROWED | Possible false consensus — agents agreed before debating | Probe the assumptions section for shared blind spots |
| Mean confidence ROSE, dispersion WIDENED | Polarization — agents became more entrenched | The question may be genuinely irresolvable by argument alone; look for an experimental path |
| `stopped_reason: converged` | Dispersion fell below threshold | Good — run with the recommendation |
| `stopped_reason: max_rounds` | Hit hard cap before converging | The debate was cut off; consider a second run with `--max-rounds` higher or `--mode quick` for faster convergence |
| `stopped_reason: diminishing_returns` | No new arguments surfaced | The council exhausted what it could discover — make a call |
| `stopped_reason: genuine_disagreement` | Positions hardened, dispersion widened | The council could not resolve the tension. The output is valuable precisely because it maps irreconcilable disagreement — read the disagreements section carefully |

## Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Debate fails with "Exceeded maximum output retries" | Model couldn't produce valid structured output for a phase | Retry the debate. If persistent, try a different model or add `--verbose` to see which agent failed. |
| Debate runs for 5+ minutes with no output | DeepSeek or slow model with many agents | Use `--mode quick --agents 3` for fast turnarounds, or use `--verbose` to see progress in real time. |
| All agents agree immediately with high confidence | False consensus — same model shares blind spots | Check the dispersion diagnostic. Try `--profiles` with diverse identities to force methodological diversity. |
| "Profile X not found" warning | Typo in profile name | Run `agent-council --profiles list` (or check the profiles list above) for valid names. |
| Synthesis contains obvious factual errors | Agents fabricated claims during debate | Check the ⚠️ Claims Not Verified section. The guardrail reduces fabrication but cannot eliminate it. Verify any statistics, pricing, or availability claims before acting. |

## Architecture Decision

**Single-model debate:** All agents share one LLM configuration. Diversity comes from persona definitions (system prompts with distinct backgrounds, analytical approaches, biases), not from different model instances. This minimizes setup friction — one API key, one endpoint, predictable cost.

**Limitation:** All agents share the model's knowledge cutoff and blind spots. The convergence diagnostics include a "possible false consensus" flag when confidence starts high and never shifts.

## Reference Files

| File | Load when |
|------|-----------|
| `references/convergence.md` | Understanding the convergence detection algorithm |
| `references/debate-protocol.md` | Deep dive into phase structure and round design |
| `references/configuration.md` | Provider setup, troubleshooting, model strings |

## Directory Structure

```
agent-council/
├── SKILL.md                      # This file — skill entry point
├── pyproject.toml                # Pip package definition
├── README.md
├── LICENSE                       # MIT
├── agent_council/                # Python package
│   ├── cli.py                    # CLI entry point
│   ├── config.py                 # Env var loading
│   ├── state.py                  # Typed state + Pydantic models
│   ├── convergence.py            # Convergence detection
│   ├── graph.py                  # Debate graph orchestration
│   └── phases/
│       ├── compose.py            # Persona generation
│       ├── premortem.py          # Failure pre-mortem
│       ├── position.py           # Initial positions
│       ├── cross_examine.py      # Iterative cross-examination
│       └── synthesis.py          # Decision landscape
├── scripts/
│   └── bootstrap.py              # First-run installation
├── templates/
│   └── personas.json             # Example custom personas
└── references/
    ├── convergence.md
    ├── debate-protocol.md
    └── configuration.md
```

## Prerequisites

- Python 3.10+ with the `pydantic-ai` package; install via `pip`, `pipx`, or `python3 scripts/bootstrap.py` (the package ships inside this skill directory, so bootstrap needs no PyPI access).
- An LLM provider API key exported as `AGENT_COUNCIL_API_KEY` (or set in a `.env` file); optionally `AGENT_COUNCIL_MODEL` and `AGENT_COUNCIL_BASE_URL`.
- The real professional profiles from the hermes-profiles library are available only in a recursive source checkout; pip and wheel installs use generated or user-supplied personas.

## Limitations

- Single-model debate: all agents share one LLM configuration and therefore its knowledge cutoff and blind spots; diversity comes from persona definitions, not model instances (see Architecture Decision).
- Debates consume many parallel LLM calls per round — expect minutes on slow models or deep mode, and check ⚠️ Claims Not Verified in every synthesis before acting on verifiable external facts.
- Convergence diagnostics reduce fabrication and false consensus but cannot eliminate them; `max_rounds` stops mean an inconclusive debate that the principal must resolve.
- This is not a general agent-orchestration framework: it runs debates only — for state-machine orchestration beyond the debate protocol, route to langgraph.

## Related Skills

- **ai-frameworks** — umbrella bundle for all AI framework skills. Load this when comparing agent-council against other multi-agent approaches (LangGraph, AutoGen, CrewAI).
- **langgraph** — for complex state-machine multi-agent orchestration beyond the debate protocol
- **pydanticai** — the underlying framework for type-safe agent definitions
- **spec-driven-development** — for building specs that agent-council can help you evaluate
- **hermes-profiles** — the 39-profile library that powers the profile selection system
