---
name: lev
description: |
  Practical CLI reference for the Lev agent framework.
  Maps natural language to primitives: get, work, check, go.
  Triggers: "lev", "leviathan", "get", "search", "find", "lookup",
            "research", "work", "check", "align", "go", "handoff",
            "learn", "index", "build", "design", "execute"
skill_type: how-to
category: cli

sub_skills:
  - work
  - lev-cdo
  - lev-research
  - lev-workshop
  - lev-builder
  - lev-intake
  - lev-design
  - lev-design-os
  - lev-social
  - lev-orch-sidequest
  - lev-orch-thinking-parliament
  - skill-discovery
---

# lev CLI — Practical Reference

Four primitives: **get** (gather context), **work** (lifecycle), **check** (validate), **go** (execute/close).

---

## get (context gathering)

Everything about finding information. Subsumes the old lev-find, lev-index, lev-find-qmd, and llm-tldr skills.

### Local search

```bash
lev get "auth middleware"                         # auto-selects indexes
lev get "auth" --indexes codebase,documentation   # explicit indexes
lev get "auth" --depth=fs                         # filesystem only
lev get "auth" --depth=bd                         # include bd issues
lev get "auth" --depth=research                   # include external backends
```

Depth order: `context -> filesystem -> bd -> research`.

### External research backends

When `--depth=research` or `--scope=research`:

| Backend | What it does | Command |
|---------|-------------|---------|
| exa | Neural web + GitHub search | `lev get "query" --scope=web` |
| valyu | Recursive turn-based refinement | `valyu research "query" --turns 5` |
| deep-research | Tavily multi-query synthesis | `deep-research "query" --deep` |
| brave-search | Quick web lookup | `brave-search "query"` |

### Index management (LEANN)

Source: `core/index/` (gRPC server on port 50052, LEANN vendor lib)

```bash
lev index build ~/path my-index    # create index from directory
lev index search "query" --index X # semantic search
lev index add file.md --index X    # add content incrementally
lev index status --all             # list all indexes
```

Index locations: `~/.config/lev/indexes/` (leann/*.leann, ck/*.index)

Env: `LEV_INDEX_PATH` overrides base directory.

### Markdown/session search (qmd)

Binary: `~/.bun/bin/qmd` — BM25 + vector + reranking for local text files.

```bash
qmd query "topic" -c claude-sessions --full -n 10
qmd query "topic" -c claudesp-sessions -c clawdbot-sessions
qmd update           # incremental re-index
qmd embed -f         # generate embeddings
```

Index: `~/.cache/qmd/index.sqlite`. Keep sessions < 2 months in index.

### Code analysis (llm-tldr)

```bash
pip install llm-tldr
tldr warm /path/to/project         # index once
tldr context func_name --project . # function summary (95% token savings)
tldr semantic "validate JWT" .     # natural language code search
tldr impact func_name .            # callers + affected tests
tldr slice file.py func 42        # minimal code affecting line 42
```

### Search decision tree

```
Local code/docs    → lev get "query"
Session history    → qmd query "topic" -c <collection>
Code structure     → tldr context / tldr semantic
External web       → brave-search, exa, tavily-search
Deep research      → valyu research, deep-research
Social/real-time   → grok-research
Multi-perspective  → skill://lev-research
```

### Domain expansion ladder (when stuck)

Start at your certainty level, climb UP when results are sparse:

1. **File/Function** — `"find auth.ts"` (exact)
2. **Component** — `"authentication module"` (sweet spot for codebase)
3. **Topic** — `"auth patterns"` (pattern match)
4. **Similar** — `"how NextAuth does this"` (prior art)
5. **Goals** — `"secure user sessions"` (problem space)
6. **Ideas** — `"zero-trust principles"` (concepts)

---

## work (lifecycle routing)

Source: `plugins/core-sdlc/src/commands/work.ts`

The `work` command owns lifecycle detection, artifact generation, and stage transitions.

```bash
work                              # auto-detect stage from context
work --stage=crystallizing        # force stage
work "spec auth system"           # keyword routing
```

Related commands in `plugins/core-sdlc/src/commands/`:
- `review.ts` — review queue
- `instruct.ts` — instruction generation
- `loop.ts` — autodev chore loop

### Lifecycle stages

```
ephemeral → captured → classified → crystallizing → crystallized → manifesting → completed
  [inline]   [report]    [typed]     [proposal]      [spec]       [handoff]     [archive]
```

### Keyword routing

| Keywords | Stage | Route |
|----------|-------|-------|
| research, analyze, prior art | captured | `lev get --depth=research` |
| design, propose, architect | crystallizing | `lev-cdo` |
| plan, spec, implement | crystallized | `work` |
| execute, do it | manifesting | `bd` |
| handoff, checkpoint, resume | manifesting | `work` |

### Learn mode

For fuzzy/early-stage intent that needs structured intake before spec:

```bash
learn                    # guided question-by-question interview
learn "some context"     # with seed context
```

Produces a proposal in `.lev/pm/proposals/`, then hands off to `work --stage=crystallized`.

---

## check (validation/ops)

Alignment, drift detection, and health checks. Runs inside `work` by default.

### Alignment audit

```bash
work "check alignment"           # preferred: runs inside work
```

What it checks:
- North star freshness (README.md vision, docs/, `.lev/pm/`)
- Priority alignment (bd issues vs. stated roadmap)
- Drift types: stale docs, product pivot, coverage gap, status drift, path drift

For deep standalone audit: scan git log, bd issues, ADRs, session handoffs, compare against north star docs.

### Issue tracking (bd)

```bash
bd ready --json                  # unblocked work
bd create "title" -p 1 --json   # new issue
bd update <id> --claim --json   # claim task
bd close <id> --reason "Done"   # complete
bd list --limit 100 --json      # list issues
```

### Doctor / status

```bash
lev index status --all           # index health
qmd status                       # qmd collection freshness
```

---

## go (execute/close)

Ship work and hand off.

```bash
bd close <id> --reason "Completed"   # close issue
git add <files> && git commit        # commit work
git push                             # push (MANDATORY before session end)
```

### Session handoff checklist

1. File bd issues for remaining work
2. Run quality gates (tests, lint, build) if code changed
3. Update bd status — close finished, update in-progress
4. `git pull --rebase && git push` — work is NOT done until push succeeds
5. Write handoff context for next session

---

## Config

Source: `core/config/src/` — resolver chain, schema validation, XDG paths.

### Resolution chain (later overrides earlier)

1. System: `~/.config/lev/config.yaml`
2. Project: `<project>/.lev/config.yaml`
3. Module: `<module>/config.yaml`
4. Environment: `LEV_*` variables

### Key paths

```
~/.config/lev/              # user config (XDG_CONFIG_HOME/lev)
~/.local/share/lev/         # persistent data
~/.local/state/lev/         # runtime state
~/.cache/lev/               # disposable cache
```

### Autodev surfaces

- Plan files: `.lev/pm/plans/plan-*.md`
- Proposals: `.lev/pm/proposals/`
- Handoffs: `.lev/pm/handoffs/`
- Specs: `docs/specs/`

---

## Source map

| Domain | Path | What it does |
|--------|------|-------------|
| CLI dispatch | `core/poly/src/surfaces/cli/` | Envelope, discovery, aliases |
| CLI binary | `core/poly/bin/lev` | Entry point |
| Work/review | `plugins/core-sdlc/src/commands/` | Lifecycle routing, review queue |
| Exec runtime | `core/exec/src/` | Execution SDK |
| Config | `core/config/src/` | Resolver chain, XDG paths |
| Index | `core/index/` | LEANN vector search, gRPC service |
| Domain types | `core/domain/` | Shared contracts and interfaces |
| Event bus | `core/event-bus/` | Inter-module events (LevEvent) |
| FlowMind | `core/flowmind/` | Flow declaration/runtime |
| Daemon | `core/daemon/` | Process supervision, health |

---

## Sub-skills (specialists)

These have real independent logic and remain as separate skills:

| Skill | What it does |
|-------|-------------|
| `work` | Lifecycle router — auto-detects stage, generates artifacts |
| `lev-cdo` | CDO deliberation framework — multi-perspective design decisions |
| `lev-research` | Deep research orchestration — multi-backend, cross-validation |
| `lev-workshop` | Workshop lifecycle — intake, analysis, POC, poly pipeline |
| `lev-builder` | Build/migrate workflows — POC to production placement |
| `lev-intake` | Content intake system |
| `lev-design` | UX pipeline |
| `lev-design-os` | Product design |
| `lev-social` | Social research |
| `lev-orch-sidequest` | Autonomous SDLC router |
| `lev-orch-thinking-parliament` | Multi-model deliberation |
| `skill-discovery` | Find skills: `~/.agents/skills/` |

Load any sub-skill with `s://<skill-name>`.
