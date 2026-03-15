---
name: continuous-learning
description: Bootstrap or operate a repo-local continuous learning system for any software repository. Use when the user says "save what we learned", "update learning", "extract lessons", "mine this session", "remember this repo pattern", "update AGENTS.md from the session", or wants a `learning/` folder that stores engineering knowledge as items, episodes, decision traces, triples, lessons, collections, procedures, and beliefs, then promotes durable signals into AGENTS.md, SOUL.md, PRINCIPLES.md, READMEs, TESTS.md, and architecture docs.
---

# Continuous Learning

Run a file-based learning loop modeled on Clous's memory system, but keep everything inside the repo. Do not rely on embeddings, external databases, or SaaS memory services.

## Working Rules

- Keep `learning/` at the repo root.
- Prefer updating existing artifacts over creating near-duplicates.
- Capture raw signals first; synthesize later.
- Treat `items -> episodes -> triples -> lessons` as the promotion ladder.
- Write to identity files and human docs only when the signal is durable enough to outlive the current task.
- Do not turn trivial work into memory noise.

## Operating Loop

### 1. Orient before work

- If `learning/` does not exist, initialize it first.
- Read `learning/README.md`, the most relevant collections, recent lessons, and matching triples before starting.
- Use `scan-learning.py` to avoid rediscovering known patterns.
- Use `references/repo-adaptation.md` to choose or refine collection files for the repo type.

### 2. Capture during work

- Append `items` as soon as you discover a non-obvious observation, failed attempt, fix, decision, warning, or codebase fact.
- Capture facts while they are still precise. Do not wait until the end of the session.
- Prefer short summaries plus enough detail to make the item reusable later.

### 3. Consolidate after work

At session end, process signals in this order:

1. Write or update the session `episode`.
2. Write a `decision-trace` when the session involved trade-offs, uncertainty, bias checks, or follow-up risks.
3. Extract stable `triples`.
4. Promote only verified, reusable, non-trivial outcomes into `lessons`.
5. Update `collections`, `procedures`, and `beliefs` where the knowledge belongs.
6. Refresh `learning/README.md` and `learning/.state/index.json`.

### 4. Promote into source-of-truth docs

After the learning artifacts are written, check whether the knowledge should also change:

- `AGENTS.md` for stable operating rules and repo facts.
- `SOUL.md` for persistent collaboration or tone corrections.
- `PRINCIPLES.md` for decision heuristics.
- Service docs such as `README.md`, `ARCHITECTURE.md`, `TESTS.md`, `SETUP.md`, or project docs under `docs/` when humans should benefit too.

Use `references/agents-md-iteration.md` for the promotion rules.

## Memory Model

| Artifact | Use it for | Write rule |
|---|---|---|
| `items/` | Raw observations during work | Append immediately |
| `episodes/` | Session summary and audit trail | Write for every meaningful session |
| `decision-traces/` | Reflection, trade-offs, assumptions, risks | Write when reasoning quality matters |
| `triples/` | Atomic facts for grep-based retrieval | Append stable facts only |
| `lessons/` | Verified outcome knowledge | Require all lesson gates |
| `collections/` | Topic-based repo knowledge | Update in place |
| `procedures/` | Repeatable workflows | Update in place with last-verified date |
| `beliefs/` | Current model of the repo | Regenerate when enough evidence accumulates |

## Folder Shape

```text
learning/
├── README.md
├── .state/index.json
├── items/
├── episodes/
├── decision-traces/
├── triples/facts.jsonl
├── lessons/
├── collections/
├── procedures/index.md
└── beliefs/current.md
```

See `references/folder-structure.md` for schemas and naming rules.

## Commands

Initialize the system:

```bash
bash .agents/skills/continuous-learning/scripts/init-learning.sh
```

Capture a signal while working:

```bash
python .agents/skills/continuous-learning/scripts/capture-item.py \
  --type discovery \
  --summary "CandidateSerializer owns nested score normalization" \
  --file services/candidates/serializers.py \
  --tag serializer \
  --tag scores
```

Search memory before starting related work:

```bash
python .agents/skills/continuous-learning/scripts/scan-learning.py "serializer normalization"
```

Refresh the index and incremental state after consolidation:

```bash
python .agents/skills/continuous-learning/scripts/refresh-learning.py
```

## Promotion Bar

Promote only when the knowledge is:

- reusable across future sessions
- specific enough to change behavior
- verified by real work, not theory
- non-sensitive
- not already captured more authoritatively elsewhere

Most sessions should update `episodes/`, `triples/`, or `collections/`. Fewer should produce `lessons/`. Even fewer should change `SOUL.md` or `PRINCIPLES.md`.

## Anti-Patterns

- Dumping entire transcripts into `learning/`
- Creating a lesson for every bug fix
- Storing transient branches, commits, or one-off task instructions
- Copying the same fact into items, triples, lessons, AGENTS, and docs without a reason
- Updating identity docs from a single weak signal

## Reference Files

- `references/folder-structure.md`
- `references/extraction-patterns.md`
- `references/agents-md-iteration.md`
- `references/knowledge-graph.md`
- `references/memory-types.md`
- `references/repo-adaptation.md`
