---
name: librarium
description: "Runs evidence-aware, multi-provider research with the Librarium v2 CLI. Use for deep research, competitive research, answer-engine visibility checks, or questions needing grounded multi-source coverage."
compatibility: Requires Node.js 22.12 or newer and the Librarium 2.x CLI.
---

# Librarium -- Multi-Provider Deep Research

Run research queries through Librarium’s v2 public provider/profile catalog.
There are 34 built-in providers and 41 implemented profiles. Preserve the
profile and collection provenance when reporting results; do not turn source
counts or agreement into a confidence claim.

## Prerequisites

Before the first query in an orb, run `librarium --version` and require major
version 2. The Librarium repository's `.agents/setup` installs its built v2
checkout globally. In other orbs, install the published v2 package when it is
available:

```bash
npm install -g 'librarium@^2'
```

Do not silently fall back to Librarium 1.x or install a mutable Git branch. If
npm has no v2 release yet, report that distribution blocker instead. Configure
available API keys with `librarium init --auto`, then inspect the usable matrix
offline with `librarium doctor` and `librarium ls --json`. This confirms only
configuration and credential presence, not authentication or connectivity, and
does not load configured custom provider code. Use `librarium doctor --live`
only when the user explicitly wants live connectivity tests; it loads trusted
custom providers, makes provider network requests, and may incur charges. Never
print secret values.

## 7-Phase Research Workflow

### Phase 1: Query Analysis
Analyze the user's research question. Determine:
- Is this a technical, business, or general knowledge query?
- Which built-in workflow is best suited? (`quick` for a curated low-latency
  set, `deep` for research-report profiles, `visibility` for an explicit
  nine-perspective comparison, `all` for catalog-derived coverage). Use
  `custom:<name>` for a user-authored group.
- What execution mode? (`sync` for quick queries, `mixed` for deep research)

### Phase 2: Provider Selection
Select providers based on query type:
- **Technical queries**: Start with `quick`; add named durable profiles or
  `deep` only when the question warrants the latency and possible spend.
- **Quick facts**: Use `quick` group (AI-grounded only, fast)
- **Competitive research**: Use `all` only after confirming its configured,
  credentialed membership and cost exposure.
- **Answer visibility**: Use `visibility` only when you deliberately want six
  SearchAPI-collected consumer-surface observations compared with three
  first-party API baselines. Treat the six collection-vendor results as
  correlated evidence, not independent confirmation.
- **Specific provider**: Use `--providers` (canonical IDs or display names,
  e.g. `-p "Exa Search,brave-search"`)

### Phase 3: Dispatch
Run the query:
```bash
librarium run "your query here" --group <group> [--mode mixed]
```

### Phase 4: Monitor Async Tasks
If a profile is `background/durable` and was submitted in async mode:
```bash
librarium status --wait
```

### Phase 5: Retrieve Results
Once the provider is observed complete, retrieve the terminal result:
```bash
librarium status --retrieve
```

### Phase 6: Analyze Output
Read the output files:
1. `summary.md` -- Overall research summary with statistics
2. `sources.json` -- Deduplicated citations ranked by frequency
3. Individual `{provider}.md` files for detailed per-provider results
4. `run.json` -- Machine-readable manifest

### Phase 7: Synthesize
Combine findings from multiple providers into a coherent answer. Record source
overlap and provenance, but do not convert a higher citation count into a
confidence score: shared collectors and repeated sources can make that evidence
correlated.

## Key Commands

| Command | Purpose |
|---------|---------|
| `librarium run <query>` | Run research query |
| `librarium run <query> --group quick` | Fast AI-grounded search |
| `librarium run <query> --group deep` | Deep research (async) |
| `librarium run <query> --group visibility` | Compare six collected consumer surfaces with three first-party API baselines |
| `librarium run <query> --group all` | Catalog-derived selectable coverage |
| `librarium answer <query>` | Fan out (default `quick`) and synthesize one grounded, cited answer to `answer.md` |
| `librarium run <query> --max-cost 0.50` | Stop launching providers once API-reported cost crosses the budget |
| `librarium run <query> --yes` | Skip the deep-research pre-flight confirm (3+ deep providers) |
| `librarium status` | Check async tasks |
| `librarium status --wait --retrieve` | Wait and fetch Node CLI async results |
| `librarium live-validation --fixture /absolute/path/to/fixture.json` | Replay a strict, network-free canonical fixture |
| `librarium usage [--days N] [--json]` | Aggregate API-reported cost and tokens across past runs |
| `librarium run <query> --html --open` | Run, then open an HTML report |
| `librarium run <query> --jsonl` | Run, then write machine-readable results.jsonl |
| `librarium browse` | Browse past runs interactively |
| `librarium html [run-dir]` | Generate report.html for a run |
| `librarium jsonl [run-dir]` | Generate results.jsonl for a run |
| `librarium refine <goal>` | Tier-tuned query variants, no dispatch |
| `librarium ls` | List providers and status |
| `librarium doctor` | Check provider configuration and credential presence offline |
| `librarium doctor --live` | Test connectivity with provider network requests; charges may apply |
| `librarium config` | Show resolved config |
| `librarium cleanup [--days N] [--dry-run]` | Delete run dirs older than N days (default 30) |
| `librarium clear [--dry-run] [-i] [--yes]` | Delete all run dirs (alias for `cleanup --all`); `-i` to pick interactively |

## MCP Server

Instead of shelling out to the CLI, agents can drive librarium over the Model Context Protocol with `librarium mcp` (stdio transport). Register it once with `claude mcp add librarium -- librarium mcp`, then call the tools: `research`, `get_results`, `check_async`, `list_providers`, `list_groups`. The `research` tool runs the same silent file-writing pipeline as `librarium run` and returns a compact structured result; fetch full provider markdown with `get_results`.

## Provider Tiers

| Tier | Providers | Speed | Depth |
|------|-----------|-------|-------|
| background/durable | `exa/research`, `openai-research/research`, `gemini-deep/research`, `perplexity-sonar-deep/research`, `perplexity-deep-research/research`, `you-research/research`, `parallel/research`, and `valyu/research` | Minutes to longer | Persisted handles that can be polled and retrieved |
| inline | Search, grounded, collected surface, and chat profiles | Usually seconds | Immediate response; no durable handle |

### Visibility and privacy boundary

The six SearchAPI surface profiles observe consumer-facing ChatGPT, Gemini,
Perplexity, Google AI Mode, Bing Copilot, and Google AI Overview output through
one upstream collector. Treat agreement among them as correlated visibility
evidence, not independent corroboration or parity with a particular logged-in
user. `zeroRetention` is an account capability: if explicitly configured,
Librarium fails closed when the account rejects it. It makes no broader
retention or privacy guarantee. SerpBase may log search queries for billing,
debugging, abuse prevention, and account logs; no zero-retention mode or fixed
public retention period is documented.

## Output Structure

```
./agents/librarium/{timestamp}-{slug}/
  prompt.md, run.json, summary.md, sources.json
  {provider}.md, {provider}.meta.json
  answer.md (when using `librarium answer`)
```
