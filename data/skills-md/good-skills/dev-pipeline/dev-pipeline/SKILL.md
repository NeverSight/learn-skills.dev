---
name: dev-pipeline
description: >-
  Runs a phase-based product development tracking pipeline for AI-agent
  workflows: pre-prod docs, adopt mid-flight projects from existing docs,
  phase briefs that update business logic and backlog from user prose with
  claim deduplication, product-wide SHARED user stories (create or extract from
  implemented features) with per-flow coverage checks on task handoffs,
  epics/features/tasks with stable IDs, phase switching without breaking
  changes, product-wide shared source of truth for contracts across
  surfaces/services (frontend→backend and new services), surface registration,
  Caveman prose compression for agent handoffs (--compress/--caveman), and
  self-contained task prompt handoffs. Use when the user starts with
  /dev-pipeline, asks to init or adopt a product backlog pipeline, brief a
  phase, create or extract user stories, create or switch phases, register a
  new surface/service, refresh shared contracts, emit the next agent task
  prompt, optionally deepen a handoff with Promptize, or track epic/feature
  status across multi-agent development.
disable-model-invocation: true
version: 1.9.0
---

# Dev Pipeline

When the user message begins with `/dev-pipeline`, this skill is attached, or they explicitly ask to run the **dev-pipeline** / product tracking pipeline, activate this skill **immediately**.

**Purpose:** Persist product evolution as token-efficient, ID-linked docs so sequential or parallel agents can continue work without losing business-logic integrity or product identity. Emits self-contained task prompts for another agent; does **not** implement product code unless the user also asks.

**Companions:** `/commit` (commit skill) after implementation; `/review-task` (review-task skill) after a task lands; `/promptize` (Promptize skill) for **optional deep engineering specs** — not a substitute for pipeline tracking (see Design decision 11).

## Design decisions

1. **Docs are source of truth** — code follows tracked epics/features/tasks; do not invent backlog state not reflected in files.
2. **Phases are switchable** — incomplete phases stay parked; switching must not rewrite IDs or break contracts.
3. **IDs are stable forever** — never renumber; mark superseded instead.
4. **Prompts are handoffs** — write under `agent-prompts/` (gitignored); do not commit prompt bodies unless the user explicitly requires it.
5. **Minimal tokens** — prefer tables, IDs, and short evidence pointers over prose dumps.
6. **Reuse existing docs** — if the repo already has `docs/epics/`, `ROADMAP.md`, etc., **extend** them; do not duplicate parallel trees without cause.
7. **Adopt mid-flight** — for repos already in development with a docs tree, `adopt` reads that tree, records current state with evidence tags, and overlays the pipeline without clobbering existing docs.
8. **Phase briefs with dedup** — user prose about a phase is documentation input; absorb only **new** claims into business rules/backlog; repeats must not rewrite docs; never disturb IDs or in-flight tasks.
9. **User stories as product-wide SHARED SoT** — durable `US-*` files under `docs/user-stories/`; indexed in `SHARED.md` for **all** surfaces; **not** owned by a single service/phase. Each story holds business logic and ordered **flows**; task prompts must cite related stories and check flow coverage. Mid-flight: `story extract` harvests journeys from implemented features into that shared spine.
10. **Shared SoT for all surfaces** — phases plus `docs/dev-pipeline/SHARED.md` are the **whole source of truth** for contracts, entities, user stories, and absorbed product rules when adding a backend during/after frontend or any new service; never fork a parallel contract or story spine per surface.
11. **Promptize is a companion, not the tracker** — `/dev-pipeline` owns product identity, phases, briefs, stories, backlog, and compact `agent-prompts/` handoffs. `/promptize` owns **one-off or deep** repository-aware engineering specs (inspect → structured Promptize body → optional `--execute`). Use Promptize **outside** the queue for ad-hoc work, or **after** `next`/`task` (or with `--promptize`) when a backlog task needs a fuller engineering spec. Never replace `brief` / `story` / `backlog` / `adopt` with Promptize.
12. **Session cache + delta handoffs** — `docs/dev-pipeline/SESSION-CACHE.md` (gitignored) records paths already read and stable carry-over; consecutive `next` reuses PRODUCT/SHARED summaries and reads **delta only** ([../shared/context-cache.md](../shared/context-cache.md)).
13. **Artifact Boundary & Cavecrew Integration** — Task handoff prompts (`agent-prompts/`) automatically apply Caveman prose compression (`--compress`/`--caveman`) to minimize context for downstream implementers. Subcommands `adopt` and `story extract` delegate code search to `cavecrew-investigator` when available. Product docs (`PRODUCT.md`, `PHASES.md`, `US-*.md`) strictly preserve natural human prose.

## Activation

| Form | Behavior |
|------|----------|
| `/dev-pipeline init [name]` | Bootstrap layout + product identity docs (greenfield) |
| `/dev-pipeline adopt` | Attach pipeline to an **existing** documented project (see [adopt.md](adopt.md)) |
| `/dev-pipeline brief [PH-ID] …` | Ingest user phase descriptions → docs/backlog with claim dedup (see [briefing.md](briefing.md)) |
| `/dev-pipeline story …` / `/dev-pipeline stories` | Create/refine product user stories (`US-*`) + flows; coverage status (see [user-stories.md](user-stories.md)) |
| `/dev-pipeline story extract` | Harvest `US-*` from implemented/shipped features (mid-flight) into SHARED story spine |
| `/dev-pipeline backlog` / `/dev-pipeline plan` | Inspect product → create/update backlog (epics/features) |
| `/dev-pipeline phase new <slug>` | Create a phase; optionally set active; trailing prose → first brief |
| `/dev-pipeline phase switch <PH-ID>` | Activate another phase without breaking prior work |
| `/dev-pipeline phase status` | Show active phase + epic/feature summary |
| `/dev-pipeline next` / `/dev-pipeline task` | Emit next ready task prompt under `agent-prompts/` (Caveman compressed) |
| `/dev-pipeline task <FEATURE-ID>` | Emit prompt for a specific feature/task |
| `/dev-pipeline status` | Compact pipeline overview (phases, surfaces, blockers, priorities) |
| `/dev-pipeline shared` / `/dev-pipeline shared status` | Show product-wide shared SoT (`SHARED.md`) |
| `/dev-pipeline shared refresh` | Additive rebuild of shared contract index from docs/phases |
| `/dev-pipeline surface new <slug>` | Register a new surface/service that inherits shared SoT |
| `/dev-pipeline --help` / `-h` | Display interactive CLI help, subcommands, flags, and token policies |
| Natural language: “dev pipeline”, «پایپلاین توسعه», «رهگیری فاز», «adopt از روی docs», «درباره این فاز بگو», «brief فاز», «یوزر استوری», «user story», «داستان کاربری», «استخراج استوری», «سرویس جدید», «شروع بک‌اند», «shared source of truth» | Same as matching subcommand intent |

Flags may appear anywhere after `/dev-pipeline`:

| Flag | Meaning |
|------|---------|
| `--set-active` | With `phase new`, `adopt`, or `surface new`: mark new/intake phase (and surface) active |
| `--suite <dir>` | Epic suite folder under `docs/` (default: discover) |
| `--docs <dir>` | Docs root for `adopt` (default: discover `docs/`, `documentation/`, …) |
| `--refresh` | With `adopt`: rebuild adoption snapshot + CONTEXT links only |
| `--phase PH-XX` | Target phase for `brief` or phase tag for `story` |
| `--brief-only` | With `brief`: record claims only; skip backlog/rule writes |
| `--story-only` | With `story`: persist story files + INDEX only; skip backlog/rule/queue writes |
| `--extract-stories` | With `adopt`: after adopt writes, run one `story extract` pass |
| `--from-docs-only` | With `story extract`: docs/ADOPTION only; no code-path inference |
| `--include-partial` | With `story extract`: also harvest `partial` features |
| `--kind <kind>` | With `surface new`: `frontend` \| `backend` \| `worker` \| `mobile` \| `bff` \| `shared-lib` \| `other` |
| `--phase-slug <slug>` | With `surface new`: also create a phase for that surface |
| `--compress` / `--caveman` | Force Caveman prose compression pass on generated handoff prompt |
| `--promptize` | With `next` / `task`: also deepen via Promptize skill (see below) |
| `--help` / `-h` | Display usage, subcommands, options, and token budget rules |
| `--dry-run` | Report planned file writes; do not write |

Do not treat ambient coding as this skill unless `/dev-pipeline` or an explicit pipeline ask is present.

## Product prose routing (brief vs story)

| User input | Command | Why |
|------------|---------|-----|
| Phase capability, domain rule, “this phase should…” | `brief` | Phase-local claims → `CLAIMS.md` / rules / backlog links |
| User journey, flow steps, “as a user I…” | `story` | Product-wide `US-*` + flows in SHARED |
| Epic/feature delivery shape, priorities, deps | `backlog` | Delivery units — link stories, do not duplicate journey text |
| Mid-flight: harvest from shipped work | `story extract` | Evidence-tagged `US-*` from Built/open features |
| Deep engineering spec for one change | `/promptize` | Repo inspect → spec — **not** product ingest |

If prose mixes journey + delivery, run `story` first for flow SoT, then `brief` or `backlog` for phase/backlog links.

## References

- Token efficiency (read first): [../shared/token-efficiency.md](../shared/token-efficiency.md)
- Session read cache: [../shared/context-cache.md](../shared/context-cache.md)
- Unified inspect: [../shared/inspect.md](../shared/inspect.md)
- Folder layout, IDs, statuses, templates: [schema.md](schema.md)
- Phase rules & switching: [phases.md](phases.md)
- Shared SoT + surfaces (multi-service): [shared.md](shared.md)
- Task prompt format: [prompt-template.md](prompt-template.md)
- Mid-flight attach from existing docs: [adopt.md](adopt.md)
- Phase user briefs + claim dedup: [briefing.md](briefing.md)
- User stories + flow coverage: [user-stories.md](user-stories.md)

## Discover project conventions (do not invent)

Look for, in order:

1. `docs/dev-pipeline/PHASES.md` — canonical phase index (this skill)
2. `docs/dev-pipeline/SHARED.md` — product-wide shared SoT (surfaces + authoritative contracts)
3. `docs/dev-pipeline/ADOPTION.md` — last adopt/refresh snapshot (if present)
4. Existing `docs/ROADMAP.md`, `docs/ARCHITECTURE.md`, `docs/epics/**`, suite folders like `docs/epics-*/`
5. `docs/user-stories/` or existing use-case / user-story trees (index in SHARED)
6. `docs/**/TASK-QUEUE.md` or `**/BOLT-TASK-QUEUE.md`
7. `agent-prompts/` or legacy `bolt-prompts/`
8. Entity/API docs (`docs/**/Entities/`, `*api-contract*`, `*dto*`) — must be indexed in SHARED when used cross-surface
9. Alternate docs roots when adopting: `documentation/`, `Documentation/`, `doc/` (see [adopt.md](adopt.md))

If both legacy and `docs/dev-pipeline/` exist, treat **legacy epic IDs as authoritative**; store phase/queue overlays under `docs/dev-pipeline/` and link out.

## Safety

**Noisy Command Execution:** Whenever executing tests, builds, static analysis, or broad searches (which generate large stdout logs) during inspection or tasks, you MUST wrap the command using `caveman shrink -- <command>`. Do not run naked verbose commands.

- Never overwrite unrelated user edits; if a target file is dirty with unrelated changes, surface overlap before editing.
- Never delete epic/feature history; use status `cancelled` / `superseded`.
- Never invent stack, APIs, or architecture — tag Observed / Inferred / Unknown (same evidence rules as Promptize).
- Do not add dependencies. Do not implement product features in this skill unless the user also requested implementation in the same message.
- Destructive doc wipes require explicit confirmation.
- **Briefing:** never renumber IDs; never mutate in-flight/done task rows from repeats; duplicates must not rewrite business-rules/backlog (see [briefing.md](briefing.md)).
- **User stories:** never renumber `US-*` / flow IDs; duplicates must not rewrite story bodies; never mark a story `implemented` while non-cancelled flows remain open; never fork surface-local story trees; task prompts must cite related stories and flow coverage (see [user-stories.md](user-stories.md)).
- **Extract:** never invent done flows without evidence; tag Observed / Inferred / Unknown.

## Workflow (sequential)

### 0. Parse

Extract subcommand, IDs, flags, and short request remainder.

### 1. Inspect (task-scoped)

Follow [../shared/inspect.md](../shared/inspect.md) — run only slices needed for this subcommand:

| Subcommand | Slices |
|------------|--------|
| `init`, `phase *`, `shared`, `status` | docs (minimal), pipeline, git if writing |
| `adopt` | docs, manifest (index-first), pipeline overlay paths, git if writing |
| `brief`, `story` (prose) | docs, pipeline |
| `backlog`, `story extract` | docs, pipeline, **manifest + code skim** |
| `next`, `task` | cache → pipeline delta (queue row + new links only) |
| `next --promptize` / `task --promptize` | cache → handoff → Promptize (no full re-inspect) |

Reuse **SESSION-CACHE** carry-over + **Inspect snapshot** from `ADOPTION.md` when fresh. See [../shared/context-cache.md](../shared/context-cache.md).

### 2. Branch by subcommand

#### `init`

1. Create layout per [schema.md](schema.md) (skip files that already exist with real content).
2. Write `docs/PRODUCT.md` (identity, surfaces: frontend/backend/other).
3. Write or link `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`.
4. Write `docs/dev-pipeline/PHASES.md` with no active phase or `PH-00` intake.
5. Write stub `docs/dev-pipeline/SHARED.md` (surfaces from PRODUCT + empty authoritative table, or seed if contract paths already exist).
6. Create stub `docs/user-stories/README.md` + `INDEX.md` + empty `intake/` (see [user-stories.md](user-stories.md)); index the path in SHARED when seeding.
7. Ensure `.gitignore` contains `agent-prompts/` and `docs/dev-pipeline/SESSION-CACHE.md` (keep `bolt-prompts/` if already ignored).
8. Create stub `docs/dev-pipeline/SESSION-CACHE.md` per [../shared/context-cache.md](../shared/context-cache.md).
9. Stop with paths created + next suggested command (`backlog`, `phase new`, `story`, or `surface new`).

Use `init` for greenfield. If the repo already has a substantial docs tree, prefer **`adopt`**.

#### `adopt` / `import` / `from-docs`

Attach the pipeline to a mid-flight project by reading its docs folder and recording current state.

1. Follow [adopt.md](adopt.md) fully (discover docs root → inventory → evidence-tagged synthesis → additive writes).
2. Write `docs/dev-pipeline/ADOPTION.md` (source map, built vs open, authoritative paths, unknowns).
3. Create-if-missing only: `PRODUCT.md` / `ARCHITECTURE.md` / `ROADMAP.md` stubs or links; `PHASES.md` + `PH-00-intake` with seeded `CONTEXT.md`; `SHARED.md` seeded from ADOPTION authoritative paths + Observed surfaces (include user-stories path for **all** surfaces).
4. Do **not** invent stack/APIs/features; do **not** emit task prompts; do **not** overwrite contentful existing docs.
5. If `--extract-stories`: run **one** [user-stories.md](user-stories.md) `story extract` pass (product-wide SHARED stories from implemented features).
6. Stop with adoption report + next suggested command (`story extract` if stories thin, `backlog`, `phase new`, `surface new`, or `status`).

Aliases: `import`, `from-docs`. Natural language: «از روی مستندات وصل کن», «adopt».

#### `backlog` / `plan`

1. Inspect product + code/docs evidence.
2. Produce/update epic suite README + epic files with stable IDs.
3. For each feature: status, priority, depends-on, co-req, blocks, acceptance sketch.
4. Record cross-links to entities, modules, API contracts, DTOs (paths only).
5. Do **not** emit an agent task prompt unless also `next`/`task` was requested.

#### `phase new` / `phase switch` / `phase status`

Follow [phases.md](phases.md). Switching must preserve all IDs and prior queues.

Before seeding a new/resumed phase CONTEXT: read [shared.md](shared.md) and inherit `SHARED.md` authoritative paths (register the surface first if missing).

After `phase new`, if the user message still contains capability/domain prose (beyond slug and flags), run **one** [briefing.md](briefing.md) pass as `BRIEF-001` for that phase.

#### `shared` / `shared status` / `shared refresh`

Follow [shared.md](shared.md). `status` is read-mostly (create stub only if missing). `refresh` is additive path indexing only — no ID renumbers, no contract body rewrites.

#### `surface new`

Follow [shared.md](shared.md). Registers a new product surface/service that **must** consume the shared SoT. Optionally creates a phase via `--phase-slug`.

Typical flow when starting backend after/during frontend:

1. `/dev-pipeline shared` (confirm spine) or `shared refresh`
2. `/dev-pipeline surface new backend --kind backend --phase-slug backend-api --set-active`
3. `/dev-pipeline brief …` for backend capabilities (dedup against SHARED + CLAIMS)
4. `/dev-pipeline next` — prompts cite Shared SoT

#### `brief` / `tell` / `phase brief` / `intake-notes`

Ingest user descriptions of phase capabilities as documentation; update business logic and backlog for **new** claims only.

1. Follow [briefing.md](briefing.md) fully (resolve phase → read `CLAIMS.md` → classify new/duplicate/refinement/contradiction → persist BRIEF → apply only allowed deltas).
2. Treat verbatim user prose as Observed documentation input (store under `briefs/BRIEF-*.md`).
3. **Duplicates:** ledger note only — do not re-edit docs or backlog.
4. **Never** renumber IDs, delete queue rows, change `in_progress`/`done`/`review` task status, or switch phases as a side effect.
5. Do not emit `agent-prompts/` during `brief`.
6. Stop with classification table + paths touched + any contradictions needing user input.

#### `story` / `user-story` / `stories` / `us`

Ingest user journeys as **durable product-wide SHARED business-flow SoT**; one file per story under `docs/user-stories/` (not owned by a single surface/service).

1. Follow [user-stories.md](user-stories.md) fully.
2. **Prose mode** (`story <prose>`): classify → `intake/STORY-*` → create/extend `US-*.md` + flows → optional business-rules/backlog links; `origin: user`.
3. **Extract mode** (`story extract` / `stories extract` / `story harvest`): harvest journeys from implemented/shipped features (ADOPTION Built vs open, done features, existing journey docs) into `US-*` with evidence tags; `origin: extracted`; index SHARED for **all** surfaces.
4. `stories` / `story status` with no prose: report coverage (open vs done flows) + confirm SHARED listing.
5. **Duplicates:** INDEX note only — do not rewrite story bodies.
6. **Never** renumber `US-*`/flow IDs, disturb in-flight tasks, switch phases, or fork surface-local story trees.
7. Do not emit `agent-prompts/` during `story` / `story extract`.
8. Stop with classification/coverage table + paths touched + open-flow gaps.

#### `next` / `task`

1. Read `docs/dev-pipeline/SESSION-CACHE.md` if present — reuse **Carry-over**; read **Delta** paths only when `last_handoff` exists and same phase ([../shared/context-cache.md](../shared/context-cache.md)).
2. Resolve active phase + queue; pick highest-priority **ready** item (or forced Feature/Task ID).
3. Resolve related `US-*` — read only stories/flows **not** already in cache Loaded table.
4. Write handoff via [prompt-template.md](prompt-template.md) to `agent-prompts/{TASK-ID}.md` — use **Inherited context** line when carry-over applies.
5. **Update SESSION-CACHE.md**: `last_handoff`, Loaded rows, Carry-over, Delta for following `next`.
6. Set queue row to `ready` or `in_progress` as appropriate.
7. Tell user: hand off file → `/commit` → `/review-task`; PASS → `/dev-pipeline next`.
8. **Optional `--promptize`:** after step 4, run Promptize with handoff path only ([../shared/token-efficiency.md](../shared/token-efficiency.md)) — prompt-only + compact; link `docs/promptize-prompts/{TASK-ID}.md`.
9. Without `--promptize`: mention `/promptize` for complex tasks only.

#### When to use Promptize vs this skill (routing)

| Need | Use |
|------|-----|
| Track product, phases, briefs, stories, backlog, emit queue handoff | `/dev-pipeline …` only |
| Deepen a **queued** task into a full engineering spec (inspect repo, AC, impact) | `/dev-pipeline next` then `/promptize …`, or `next --promptize` / `task … --promptize` |
| Ad-hoc fix / spike **not** on the pipeline queue | `/promptize` alone (optionally `--execute`) |
| Absorb product prose into docs/backlog/stories | `brief` / `story` — **not** Promptize |
| Implement after a pipeline handoff | Implementer agent (or `/promptize --execute` only if user asked) → `/commit` → `/review-task` |

#### `status`

Emit a compact table: active phase, surfaces from SHARED, epic/feature counts by status, blockers, next ready IDs. No file writes unless fixing a broken index was requested.

### 3. Stop

Default: documentation + prompt handoff only. Implementation belongs to the other agent (or a separate user ask).

## Context loading order (for agents using the docs)

Check `SESSION-CACHE.md` first. Load **only** delta paths — stop when the task is actionable.

1. Cache Carry-over (PRODUCT one-liners, SHARED path list) if fresh
2. Else `docs/PRODUCT.md` (short)
3. Else `docs/dev-pipeline/SHARED.md` if task touches contracts/surfaces
4. `docs/dev-pipeline/ADOPTION.md` inspect snapshot if adopt context needed
5. Active `TASK-QUEUE.md` row + parent epic section for **this** feature only
6. Linked `US-*.md` only if cited and not in cache Loaded
7. Contract/entity paths **new to this task** only
8. Skip unrelated suites and cached paths

## Out of scope for this skill

- Implementing application code (unless user separately asks)
- `/commit` or `/review-task` workflows (delegate to those skills)
- Rewriting legacy epic IDs
- Opening PRs / force-push / destructive git
- Replacing Promptize for one-off engineering specs (use `/promptize` for that)
- Running Promptize instead of `brief` / `story` / `backlog` / `adopt` / phase ops
- Embedding Promptize’s full template as the default `agent-prompts/` body (pipeline template stays default; Promptize is optional deepen)
- Using `adopt` to invent a full backlog without doc evidence (use `backlog` after adoption with user confirmation)
- Using `brief` to reshuffle or renumber the entire backlog (additive deltas + explicit cancel/supersede only)
- Using `story` to delete or renumber stories/flows, or to mark a story `implemented` while flows remain open
- Forking surface-local user-story trees or treating stories as owned by one service
- Forking a second API/DTO/entity spine for a new surface instead of extending `SHARED.md`

## Version

When `--version` or `-v` is detected as the only meaningful flag, emit the skill version (from the frontmatter) verbatim and stop. Do not inspect, reason, or generate.


## Caveman Integrations (Token Optimization)

When interacting with the repository or external sources, use the following Caveman commands to drastically reduce token usage:

1. **`caveman browse <url>`**: Whenever the user provides an external URL during `brief` or `story` gathering (e.g., API docs), do NOT fetch it raw. You MUST run `caveman browse <url>` to read a compressed, token-efficient view of the page.
2. **`caveman explore install`**: During `adopt` or heavy code inspections on large repositories, if you need broad searches, run `caveman explore install`. Delegate searches to this FastContext subagent to receive precise `path:line` results instead of flooding your main context with file contents.
3. **`caveman stats`**: When finishing a large pipeline operation (like full `backlog` generation or extensive `adopt`), you may run `caveman stats` and append a one-line token savings estimate to the final output to keep the user informed.
