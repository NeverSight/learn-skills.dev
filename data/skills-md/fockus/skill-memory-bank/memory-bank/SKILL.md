---
name: memory-bank
description: "Agent-agnostic long-term project memory through `.memory-bank/` + RULES (TDD/SOLID/Clean Architecture/FSD/Mobile) + dev-toolkit commands. Use when working in a project with a `.memory-bank/` directory or when the user explicitly asks for memory-bank workflow, code rules, or dev-toolkit commands."
---

# Memory Bank Skill

Three-in-one skill for code agents:

1. **Memory Bank** — long-term project memory through `.memory-bank/` (`STATUS`, `plan`, `checklist`, `RESEARCH`, `BACKLOG`, `progress`, `lessons`, `notes/`, `plans/`, `experiments/`, `reports/`, `codebase/`).
2. **RULES** — global engineering rules: TDD, Clean Architecture (backend), FSD (frontend), Mobile (iOS/Android UDF), SOLID, Testing Trophy.
3. **Dev toolkit** — 33 commands: `/mb`, `/start`, `/done`, `/plan`, `/brief`, `/discuss`, `/groom`, `/sdd`, `/work`, `/drive`, `/config`, `/pipeline`, `/profile`, `/commit`, `/pr`, `/review`, `/test`, `/refactor`, `/doc`, `/changelog`, `/catchup`, `/adr`, `/contract`, `/security-review`, `/api-contract`, `/db-migration`, `/observability`, `/roadmap-sync`, `/traceability-gen`, `/analyze-task`, `/flow`, `/goal`, `/agree`.

> **Design contract.** Memory Bank rests on one inviolable promise — *agents remember* — and a stack of fully configurable, token-economical layers above it. Default behaviour never changes without explicit opt-in; user customisations survive upgrades; expensive paths are off by default. See [`references/design-principles.md`](references/design-principles.md) for the full contract.

Supported host model:
- **Claude Code / OpenCode** — native command surface + global install.
- **Cursor** — native full support: global skill alias (`~/.cursor/skills/memory-bank/`), global hooks (`~/.cursor/hooks.json`), global slash commands (`~/.cursor/commands/`), `~/.cursor/AGENTS.md` with managed section, plus a paste-ready file for Settings → Rules → User Rules. Project-level `.cursor/` adapter remains available as an add-on via `--clients cursor`.
- **Codex** — global skill discovery + `AGENTS.md` hints + project-level `.codex/` adapter; no separate native slash-command surface.
- **Other code agents** — via adapters, `AGENTS.md`, local hooks/configs, or direct CLI/script usage.

---

## Development flow — stages a code agent should expect

Work in a Memory Bank project follows this order. Depth scales with task complexity — every stage except development itself can be skipped for trivial work; review and judge are **opt-in**.

| # | Stage | Command | Notes |
|---|-------|---------|-------|
| 1 | **Interview** | `/mb discuss <topic>` (alias `/mb ask_me`) | Grilling interview → decisions + EARS-validated requirements draft in `context/<topic>.md` |
| 2 | **Spec or plan** | `/mb sdd <topic>` · `/mb plan <type> <topic>` | Pick by complexity: feature/multi-task → spec triple (`specs/<topic>/requirements+design+tasks.md`, executable `<!-- mb-task:N -->`); smaller bounded change → plan (`plans/*.md`, `<!-- mb-stage:N -->`); trivial fix → no artifact (rules still apply) |
| 3 | **Development** | `/mb work <target>` | Executes spec tasks / plan stages one by one through an implement → verify loop with role subagents (TDD, contract-first) |
| 4 | **Verification** | `/mb verify` | plan-verifier audits diff vs plan/spec DoD; **mandatory before `/mb done`** when work followed a plan/spec |
| 5 | **Review** *(optional)* | `/mb work <target> --review` | Reviewer verdict (subagent ensemble or external codex) + severity gate; off by default |
| 6 | **Judge** *(optional)* | `/mb work <target> --judge` | `mb-judge` decides GO / GO_WITH_BACKLOG / NO_GO and terminates the review loop |
| 7 | **Close** | `/mb done` | Actualize bank: progress append, checklist/status update |

**Grooming (any stage).** `/mb groom <topic>` (also `grooming`) runs a critical grooming session outside the fixed order — for a raw idea, a task that already has a spec, or a decision worth revisiting. Unlike `/mb discuss`, the goal is not a spec: the agent challenges necessity and approach, proposes its own solutions, covers white spots; the summary lands in `context/<topic>-groom.md`, confirmed decisions go to `agreements.md` / backlog (ADR/Ideas), and the session ends with proposed next steps (e.g. `/mb sdd`).

**Pipeline.** The whole chain can be encoded in `<bank>/pipeline.yaml` as a named workflow (steps, per-role `model`/`thinking`, severity gates, protected paths, budget). When present, `/mb work` resolves it automatically (`mb-workflow.sh`) and follows the configured steps — e.g. governed `implement → verify → review → judge → fix → done` — without per-run flags. Manage with `/mb pipeline` / `/mb config`; validate with `/mb config validate`. Defaults never change without opt-in: no pipeline and no flags = simple implement → verify.

**Command index — all `/mb` subcommands** (know these exist; suggest them to the user when relevant; details per subcommand → `commands/mb.md` or `/mb help <sub>`):

- **Session & context:** `context` (default, empty arg) · `start` · `done` · `update` · `tasks` · `note <topic>` · `index`
- **Requirements & decisions:** `discuss <topic>` (alias `ask_me`) · `groom <topic>` (alias `grooming`) · `sdd <topic>` · `openspec <import|list|status|sync>` · `plan <type> <topic>` · `idea <title>` · `idea-promote <I-NNN>` · `adr <title>` · `agree <sub>` · `goal`
- **Execution:** `work [target]` · `verify` · `config <sub>` · `pipeline <sub>` · `flow <route>` · `analyze-task`
- **Codebase intelligence & memory:** `map [focus]` · `graph` · `wiki` · `research <query>` · `search <query>` · `recall <query>` · `recap <sid>` · `conflicts` · `consolidate` · `tags`
- **Setup & maintenance:** `init` · `install` · `profile <sub>` · `doctor` · `compact` · `migrate-structure` · `import` · `upgrade` · `deps` · `statusline` · `help [sub]`

Beyond `/mb`, the toolkit ships standalone commands (see the list in the intro above): `/commit`, `/pr`, `/review`, `/test`, `/refactor`, `/doc`, `/changelog`, `/catchup`, `/contract`, `/security-review`, `/api-contract`, `/db-migration`, `/observability`, `/roadmap-sync`, `/traceability-gen`.

---

## Quick start

```bash
# Storage modes — pick one per project:
/mb init                                      # local mode (default) — bank in repo (.memory-bank/)
/mb init --storage=local                      # explicit local mode — same as above
/mb init --storage=global --agent=claude-code # global mode — bank in ~/.claude/memory-bank/...
                                              # (personal, NOT committed to the repo)
# Rules-only mode: no /mb init at all — [MEMORY BANK: ABSENT] state;
# /mb lifecycle stays inactive; all TDD/SOLID/Clean Architecture/DRY/KISS/YAGNI rules still apply.

# Initialization flags
/mb init --full          # same as /mb init (stack auto-detect + CLAUDE.md generation)
/mb init --minimal       # only the .memory-bank/ structure

# Session flow (basic)
/mb start                # load context
# ... work, checklist.md updates as tasks complete ...
/mb verify               # verify plan alignment (if there was a plan)
/mb done                 # actualize + note + progress

# Unified SDD flow (spec-driven features)
/mb discuss <topic>      # EARS-validated requirements → context/<topic>.md
/mb sdd <topic>          # spec triple: requirements / design / tasks.md (executable)
# specs/<topic>/tasks.md is a first-class executable artifact with <!-- mb-task:N --> markers,
# NOT a scaffold — each block is resolved by /mb work <topic> as a work item.
# requirements.md may add an optional `## Scenarios` layer: <!-- mb-scenario:N --> blocks
# (### Scenario: + **Covers:** REQ-x + GIVEN/WHEN/THEN). They become a test-plan
# (mb-scenario-extract.py) that /mb plan links and /mb work turns into one real test
# per scenario in the project's stack. Enforce coverage with
# `mb-spec-validate.sh --require-scenarios`; off by default (EARS-only specs stay valid).
/mb work <topic>         # execute spec tasks one by one (reads <!-- mb-task:N --> blocks)
/mb verify               # verify against spec + plan
/mb done                 # actualize + progress
```

# Personalize rules for your stack (optional):
/mb profile init --scope=project --role=backend --stack=go --architecture=microservices --delivery=contract-first
# or user-global (works even without a project Memory Bank):
/mb profile init --scope=user --role=frontend --stack=typescript

If the host does not support native slash commands, use:
- `commands/mb.md` as the workflow entrypoint;
- the `memory-bank ...` CLI for install/init/doctor flows;
- bundled scripts and agent prompts from this skill bundle.

---

## Workspace resolution — agent-agnostic storage

Memory Bank resolves its active bank through `scripts/_lib.sh::mb_resolve_path`. The precedence is fixed and explicit:

1. **Explicit argument** — `mb-*.sh <mb_path>` always wins.
2. **`MB_PATH` env override** — for ad-hoc redirection in shell sessions.
3. **Local mode** — `<project>/.memory-bank/` (default of `/mb init`, team-shared, committable).
4. **Global mode** — registered in `<agent_config>/memory-bank/registry.json`. Requires `--storage=global --agent=<name>` on init (or `$MB_AGENT` env). Per supported agent:
   - `claude-code` → `$HOME/.claude/memory-bank/projects/<id>/.memory-bank`
   - `cursor` → `$HOME/.cursor/memory-bank/projects/<id>/.memory-bank`
   - `codex` → `$HOME/.codex/memory-bank/projects/<id>/.memory-bank`
   - `opencode` → `$HOME/.config/opencode/memory-bank/projects/<id>/.memory-bank`
   - `pi` → `$HOME/.pi/agent/memory-bank/projects/<id>/.memory-bank`
   - `windsurf`/`cline`/`kilo` → analogous under the respective config dir
5. **Legacy `.claude-workspace`** — kept for backward compatibility (`storage: external` + `project_id: <id>` → `~/.claude/workspaces/<id>/.memory-bank`). New projects should use `--storage=global` instead.
6. **Fallback** — relative `.memory-bank` (compat with existing scripts).

### Active-state semantics

- `[MEMORY BANK: ACTIVE]` — when the resolver returns an **existing** bank (local or registered global).
- `[MEMORY BANK: ABSENT]` — when no bank exists for the current project. Surface this and **stop** the Memory Bank lifecycle — do **not** silently initialize.
- `[MEMORY BANK: INITIALIZED]` — only after a successful explicit `/mb init`.

### Rules-only mode

A project may intentionally have no Memory Bank (`[MEMORY BANK: ABSENT]`). In that case:

- `/mb` lifecycle commands stay inactive until the user explicitly runs `/mb init`.
- The **engineering rules baseline still applies**: TDD, SOLID, Clean Architecture / FSD, DRY/KISS/YAGNI, Testing Trophy, protected files, no placeholders, verification before completion. Global skill installation never auto-enables Memory Bank state.

When invoking MB Manager or scripts, always pass the resolved `mb_path`.

---

## Tools — shell scripts

All scripts live in `scripts/` next to this `SKILL.md`. In global installs, the bundle is typically available through host aliases:
- Claude Code: `~/.claude/skills/memory-bank/`
- Codex: `~/.codex/skills/memory-bank/`
- Cursor: `~/.cursor/skills/memory-bank/`

Scripts work with `.memory-bank/` in the current directory or through the `mb_path` argument.

### GraphRAG-lite retrieval routing

`code_context is the default` for ambiguous code-understanding questions such as "where is the logic for X?" or "find similar implementation". Exact structural questions route directly to graph tools: "who calls/imports/defines X?" → `graph_neighbors`, "reverse deps" or change impact → `graph_impact`, and "what tests cover this file/symbol?" → `graph_tests`. User explicitly asks "semantic search" → `search_code` because explicit tool intent wins.

Fail open: missing graph, stale graph, missing semantic provider, or unavailable native extension must not block the agent. Use `scripts/mb-graph-query.py` and `scripts/mb-code-context.py` as the universal CLI fallback; Pi and OpenCode may expose native tool wrappers, while Claude Code, Codex, and generic AGENTS.md agents can call the scripts directly.

| Script | Purpose |
|--------|---------|
| `_lib.sh` | Shared helpers sourced by other scripts |
| `mb-context.sh [--deep]` | Build context from core files (`STATUS` + `plan` + `checklist` + `RESEARCH` + codebase summary). `--deep` shows full codebase docs, `--full` disables the per-file byte cap (`MB_CONTEXT_MAX_BYTES` / `context_max_bytes`, default 12 KB) |
| `mb-statusline.py [--install]` | Claude Code statusline showing context-window fill `%` (`used/limit`, 1M-aware) + model · branch · project. Reads the status JSON on stdin; `--install` wires it into `~/.claude/settings.json` (backup, no clobber) |
| `mb-search.sh <q> [--tag t]` | Keyword search across the memory bank. `--tag` filters via `index.json` |
| `mb-note.sh <topic>` | Create `notes/YYYY-MM-DD_HH-MM_<topic>.md`. Collision-safe (`_2` / `_3`) |
| `mb-plan.sh <type> <topic>` | Create `plans/YYYY-MM-DD_<type>_<topic>.md` with `<!-- mb-stage:N -->` markers |
| `mb-plan-sync.sh <plan>` | Synchronize a plan ↔ checklist + roadmap + status (idempotent) |
| `mb-plan-done.sh <plan>` | Close a plan: `⬜→✅` + move to `plans/done/` |
| `mb-idea.sh <title> [HIGH\|MED\|LOW]` | Capture a new idea in `backlog.md` with monotonic `I-NNN` |
| `mb-idea-promote.sh <I-NNN>` | Promote an idea (I-NNN) into an active plan |
| `mb-adr.sh <title>` | Capture an Architecture Decision Record in `backlog.md` (ADR-NNN) |
| `mb-init-bank.sh` | Deterministic, locale-aware `.memory-bank/` scaffolder |
| `mb-config.sh` | Memory Bank config resolver + locale auto-detector |
| `mb-metrics.sh [--run]` | Language-agnostic metrics (12 stacks). `--run` captures `test_status=pass\|fail` |
| `mb-index.sh` | Registry of all entries (core + notes/plans/experiments/reports) |
| `mb-index-json.py` | Build `index.json` (frontmatter notes + lessons headings). Atomic write |
| `mb-drift.sh` | 8 deterministic drift checkers (path, staleness, script coverage, dependency, cross-file, index sync, command, frontmatter) |
| `mb-progress-chain.sh` | `--rebuild-tail` / `--verify` the `progress.md` append-only hash chain (`index.json:progress_chain`); CRITICAL drift on tamper (handoff-v2) |
| `mb-rules-check.sh` | Deterministic rules enforcement (SRP / Clean Architecture / TDD delta) |
| `mb_rules_check_lib.sh` | Shared helper library for `mb-rules-check.sh` |
| `mb_rules_check_profile.sh` | Profile resolution and output emitters for `mb-rules-check.sh` |
| `mb_rules_check_baseline.sh` | Baseline SRP / Clean Architecture / TDD checks for `mb-rules-check.sh` |
| `mb_rules_check_stack.sh` | Stack-aware and FSD checks for `mb-rules-check.sh` |
| `mb-done-gates.sh` | Mandatory `/mb done` gate set (tests + rules + placeholder scan); `--force --reason` records a NOTE in `progress.md` (handoff-v2) |
| `mb-test-run.sh` | Structured test runner with per-stack output parsing → strict JSON |
| `mb-deps-check.sh [--install-hints]` | Preflight dependency checker (python3, jq, git + optional tree-sitter, networkx) |
| `mb-checklist-prune.sh [--apply]` | Compact `checklist.md` to the v2 format — fold a plan's per-stage blocks into one `## <title> — k/n` block, move closed plans and fully-done `plans/done`-linked sections **verbatim** into `progress.md`. Cap `MB_CHECKLIST_MAX_LINES` → `.mb-config` `checklist_max_lines=` → 100; still over cap → exit 3 with a per-plan diagnostic (live work is never cut). **Rule: `checklist.md` = open TODO only; commit hashes / test counts / closeouts go to `progress.md`.** Composed by `mb-core-cap.sh fix` |
| `mb-checklist-v2.py <cmd>` | Single reader/writer for the `checklist.md` v2 format (`plan` / `apply` / `upsert` / `flip` / `extract`), used by `mb-checklist-prune.sh`, `mb-plan-sync.sh`, `mb-plan-done.sh` and `mb-work-checkbox.sh` |
| `mb-status-rotate.sh [--keep N] [--dry-run|--apply]` | Archive dated `## ` sections of `status.md` past the newest N (default 3) into `progress.md` as `## [status archive] …` blocks, through the locked append-only helper. Undated sections (`## Current phase`, `## Open backlog`) never move. Called by the actualize step (`/mb done`, `/mb update`) before `status.md` is rewritten |
| `mb-core-cap.sh check\|fix [--mb <path>] [--json]` | Hard line caps for the two core registries (AGR-043): `status.md` = current state, `checklist.md` = plans in flight, everything else in `progress.md`. `check` prints `status_lines/status_cap checklist_lines/checklist_cap over=<csv|none>` (exit 1 when over); `fix` composes `mb-status-rotate.sh --apply` + `mb-checklist-prune.sh --apply` and re-checks — exit 1 = still over (dispatch MB Manager `actualize --strict`), exit 3 = live plans do not fit (owner decision, never a trim). Caps `MB_STATUS_MAX_LINES` / `MB_CHECKLIST_MAX_LINES` → `.mb-config` → 60 / 100; `MB_CORE_CAP=off` disables |
| `mb-coord.sh active [--tail N]` / `mb-coord.sh append --type <T> --title <t>` | Read/write the cross-session board `COORDINATION.md` without loading it: `active` prints active FREEZEs (tagged, plus `[legacy]` ones declared in a **bolded** body marker), HANDOVERs with no ACK, the last N entries (default 3) and a `board: <entries>, <bytes>` line — a few hundred bytes instead of hundreds of KB. `append` writes `## <TYPE> · YYYY-MM-DD · <title>` through a locked atomic append. No board → `no board`, exit 0 |
| `mb-compact.sh [--apply]` | Status-based compaction decay — archive old done plans + low-importance notes |
| `mb-handoff.sh` | Handoff capsule manager — `--actualize` / `--read` / `--rotate` a ≤1500-byte session capsule under `handoff/` (handoff-v2) |
| `mb-tags-normalize.sh [--apply]` | Levenshtein-based tag synonym detection + merge across `notes/` |
| `mb-roadmap-sync.sh` | Regenerate `roadmap.md` autosync block from `plans/*.md` frontmatter |
| `mb-traceability-gen.sh` | Regenerate `traceability.md` from specs + plans + tests |
| `mb-ears-validate.sh <file>` | Validate REQ bullets against the 5 EARS patterns |
| `mb-req-next-id.sh` | Emit the next monotonic `REQ-NNN` identifier |
| `mb-sdd.sh <topic>` | Create a Kiro-style spec triple under `specs/<topic>/` (requirements / design / tasks). Scaffolds an optional `## Scenarios` (GIVEN/WHEN/THEN) section |
| `mb-scenario-extract.py <file>` | Extract `<!-- mb-scenario:N -->` GIVEN/WHEN/THEN blocks → normalized test-plan (JSON Lines: covers + steps + stable `test_id`). `--validate` checks present scenarios are well-formed. Opt-in layer; absent scenarios → empty/no-op |
| `mb_work_items.py` | Shared parser for plan stages (`<!-- mb-stage:N -->`) and spec tasks (`<!-- mb-task:N -->`); CLI emits JSON Lines |
| `mb_req_id.py` | Shared REQ-ID grammar (single source of truth) used by traceability / spec-validate / ears-validate. Supports prefixed schemes (`REQ-RS-008`), distinguishes a definition from a mid-line mention, expands `REQ-RS-002/003` slash-shorthand, and maps pytest identifiers (`req_rs_008`) onto canonical ids |
| `mb-spec-validate.sh <topic\|spec-dir\|spec-file>` | Validate spec triple integrity (EARS, parseable tasks, per-task Covers/DoD/Testing, no REQ orphans). Present GIVEN/WHEN/THEN scenarios are structure-checked; `--require-scenarios` (opt-in) enforces ≥1 scenario per REQ; `--require-tests` (opt-in) enforces ≥1 covering test per REQ (scans `<repo>/tests`, `<mb>/tests`, or `MB_TEST_ROOTS`). `--json` mode for structured output |
| `mb-spec-tasks-migrate.sh <topic\|tasks-file> [--apply\|--dry-run]` | Migrate legacy `## N. ...` tasks to `<!-- mb-task:N -->` format. Dry-run default, --apply writes backup before changes, idempotent |
| `mb-pipeline.sh` | Manage the project's `pipeline.yaml` (spec §9) |
| `mb-pipeline-validate.sh` | Structural validation for `pipeline.yaml` (spec §9) |
| `mb-work-resolve.sh` | Resolve `<target>` arg into a plan/spec path (spec §8.2) |
| `mb-work-range.sh` | Emit per-stage indices (plan mode) or per-sprint paths |
| `mb-work-plan.sh` | Emit per-stage execution plan as JSON Lines (spec §8) |
| `mb-work-budget.sh` | Token budget tracker for `/mb work --budget` |
| `mb-work-protected-check.sh` | Match files against `pipeline.yaml:protected_paths` |
| `mb-work-review-parse.sh` | Validate reviewer output for `/mb work` review-loop |
| `mb-work-severity-gate.sh` | Apply `pipeline.yaml:severity_gate` to review counts |
| `mb-work-trend.sh` | Review-cycle trend: weighted score (10×blocker + 3×major + 1×minor) vs the previous cycle → `improving` / `stagnant` / `regressing` / `null` (work-loop-v2 G2) |
| `mb-work-pivot.sh` | Decide `refine` / `pivot_in_role` / `pivot_via_architect` from the trend + cycle count, instead of grinding the same fix (`pivot_after_cycles`, `pivot_escalate_to_architect_on`) |
| `mb-work-contract.sh` | Per-stage "what done means" contract under `<bank>/contracts/<topic>_stage-<N>.md` — `create` / `read` / `validate` / `path`; the reviewer can judge against it |
| `mb-workflow.sh` | Resolve the active workflow + per-step `model`/`thinking` config from `pipeline.yaml` for `/mb work` |
| `mb-drive.sh` | Autonomous goal-driven loop: `next` reads goal-acceptance + the firewall + work-state + budget and emits exactly one action (`implement` / `repair` / `pivot` / `stop_*`). Stateless, fail-closed — `stop_success` requires a green firewall AND 100% acceptance (REQ-DR-014) |
| `mb-drive-preflight.sh` | Initialize missing drive components or resume the same run without resetting cycles, steps, limits, or spend; refuse corrupt state and conflicting resume limits |
| `mb-drive-stop.sh` | Drive-loop stop telemetry + per-run drive state: `arm` marks a drive live (arms the Stop-hook resume-gate), `record --reason\|--action` writes the stop reason once into the `mb-flow` fence, `progress.md`, and the run's state slot (REQ-DR-033/034) |
| `mb-work-state.sh` | Durable `/mb work` loop-state + `max_cycles` enforcement; optional per-run isolation/claim under `MB_WORK_PARALLEL` |
| `mb-work-slots.sh` | Sourced helper: per-run state/budget/drive slot-path resolution + source→run claim index (gated behind `MB_WORK_PARALLEL`) |
| `mb-work-checkbox.sh` | Deterministic DoD-checkbox flip, gated on the run's work-state phase (single-writer for `checklist.md`) |
| `mb-work-diff.sh` | Baseline-scoped diff for a `/mb work` run — feeds verify/review with the stage's own changes only |
| `mb-work-progress-append.sh` | Locked, atomic, append-only writer for `<bank>/progress.md` (safe under concurrent runs) |
| `mb-work-codex-preflight.sh` | Fail-safe codex CLI availability/auth health-check before a cross-model review wave |
| `mb-session-doctor.sh` | Diagnose session-memory subsystem health (unsummarized sessions, missing index/adapters, legacy stubs) |
| `mb-agent-caps.sh` | Capability-aware dispatch: resolve CLI transport (pi/opencode/codex/claude-agent) + concrete model per role by probing CLI presence and model availability |
| `mb-agent-render.py` | Installer helper: builds the installed form of an agent by placing the partials listed in its `compose:` frontmatter above its body (`--host` adapts the frontmatter for OpenCode, pi, or Codex; for Codex it writes a TOML role) |
| `mb-language.py` | `/mb language`: per-project response / code-comment language as a managed block at the top of the project's `AGENTS.md` and `CLAUDE.md` (`set`, `off`, `show`) |
| `mb-reviewer-resolve.sh` | Pick the active reviewer agent name |
| `mb-review.sh` | Review orchestrator entry point: deterministic 5-section payload assembly (diff + calibration examples + test evidence + auto-findings), model-agnostic, `--emit-payload`/`--input` |
| `mb-review-cache.sh` | Touched-file test-evidence cache: `compute_touched_sha` + TTL HIT/MISS resolution under `.memory-bank/tmp/` |
| `mb-review-examples.sh` | Layered calibration-example loader: project-over-skill precedence by `example_id`, fence-aware parser, per-category rotation, path-traversal/symlink-safe; renders the `## Calibration examples` payload section |
| `mb-session-spend.sh` | Session token-spend tracker (sprint context guard) |
| `mb-session-recent-rebuild.sh` | Regenerate `session/_recent.md` from `session/*.md` (keeps newest `MB_RECENT_KEEP`; deterministic, idempotent) |
| `mb-recap.sh <sid>` | `/mb recap`: reconstruct a full `progress.md` entry from `session/<sid>*.md` via one Haiku call, replacing that session's auto-capture stub idempotently (`recapped` frontmatter). Missing session → exit non-zero, no writes; real entry already present → refuse |
| `mb-conflicts.sh [--judge] [--threshold N]` | `/mb conflicts`: report memory entries with high lexical overlap **and** opposing/replacement assertions (en+ru markers) as conflict candidates — `$0` pass (token-set Jaccard > `N`, default 0.3) over `notes/` + `lessons.md` + recent `progress.md`, zero LLM calls. `--judge` confirms/rejects each pair via one Sonnet call + prints a suggested `[SUPERSEDED: YYYY-MM-DD -> <ref>]` marker. PRINT-ONLY — never writes to any bank file |
| `mb-consolidate.sh [--apply] [--days N]` | `/mb consolidate`: fold sessions older than `N` days (default 30) that cluster by shared files / lexical overlap into 5–15 line `notes/` candidates, archive those session files VERBATIM → `session/archive/`, and move their contiguous auto-capture progress STUBS VERBATIM → `progress-archive.md`. Zero LLM calls. Dry-run is the DEFAULT (writes nothing — bank byte-identical); `--apply` performs it. Real progress entries are immutable and never move |
| `mb-auto-commit.sh` | Opt-in auto-commit of `.memory-bank/` after `/mb done` (`MB_AUTO_COMMIT=1` or `--force`) — 4 safety gates, MB-only staging, never pushes |
| `mb-freshness.sh [--porcelain\|--stop-nudge\|--banner]` | Deterministic MB-vs-code drift alarm (`behind`/`dirty`); drift-gated Stop nudge + SessionStart banner (`MB_DRIFT_WARN_COMMITS`/`MB_DRIFT_WARN_DIRTY_LINES`, opt-out `MB_FRESHNESS_BANNER=off`). See `docs/concepts/session-memory.md` for the auto-commit recipe |
| `mb-migrate-v2.sh` | One-shot v1 → v2 migrator for `.memory-bank/` |
| `mb-migrate-structure.sh` | One-shot v3.0 → v3.1 structure migrator for `.memory-bank/` |
| `mb-import.py` | Claude Code JSONL → Memory Bank bootstrap importer |
| `mb-openspec.sh` | Thin dispatcher for the OpenSpec import adapter: `import\|list\|status\|sync` → `mb-openspec.py` |
| `mb-openspec.py` | One-way OpenSpec `changes/<id>/` → MB spec triple `specs/<topic>/` import + drift-aware `list`/`status`/`sync` (opt-in `--normalize` LLM slot layer) |
| `mb_openspec_model.py` | Dataclasses shared by the OpenSpec adapter's parser/converter |
| `mb_openspec_parse.py` | Read-only OpenSpec change parser (`parse_change`, `compute_source_hash`) |
| `mb_openspec_convert.py` | Deterministic OpenSpec → MB spec-triple converter (anchors, EARS classify, re-import anchor reuse) |
| `mb_openspec_normalize.py` | Opt-in `--normalize` LLM slot layer + source-hash cache for the OpenSpec adapter (fail-open) |
| `mb-agree.sh` | Single writer for the running list of agreements (`agreements.md`): `add\|defer\|reject\|question\|resolve\|list\|sync` + managed-block sync |
| `mb-codegraph.py` | Code graph orchestrator. Extractors in `memory_bank_skill/`: `codegraph_python` (stdlib `ast`), `codegraph_shell` (Bash/Bats via stdlib `re`) — both always on — `codegraph_treesitter` (multi-language, opt-in), `codegraph_analytics` (communities/cohesion/betweenness, optional networkx), `codegraph_cochange` (git co-change edges via opt-in `--cochange`) |
| `mb-graph-query.py` | Query `codebase/graph.json`: `neighbors`, `impact`, `tests`, `explain`, `summary` with JSON/markdown output |
| `mb_graph_query_core.py` | Core graph loading, matching and payload builders for `mb-graph-query.py` |
| `mb_graph_query_render.py` | Markdown summary renderers for graph-query output |
| `mb-code-context.py` | GraphRAG-lite evidence pack: optional semantic candidates + graph expansion + text/read fallback |
| `mb_code_context_core.py` | Core evidence-pack orchestration for `mb-code-context.py` |
| `mb-semantic-search.py` | Semantic code search over `graph.json` (+ wiki): `--backend auto` (embeddings when `fastembed` installed, else pure-Python BM25 — the $0 zero-dep base), `--source-only`, disk cache in `.index/codesearch/` warmed by `/mb graph --apply`. Modules in `memory_bank_skill/`: `semantic_search`, `semantic_embeddings`, `codegraph_loader` |
| `mb-wiki.py` | `/mb wiki` engine (deterministic prep): `plan`/`packs`/`write-article`/`merge-edges`/`index`. LLM articles + surprising-connection edges via host subagents. Modules: `wiki_evidence`, `wiki_store` |
| `mb-context-slim.py` | Slim a full agent prompt on stdin → terse version on stdout |
| `mb-cost-report.py [--project <dir>] [--since N] [--json]` | `/mb cost` engine: mine Claude Code transcripts (`~/.claude/projects/<slug>/`) into per-session, per-subagent-role and per-work-item (`mb-work-state.sh init` → `mb-work-checkbox.sh flip`) cost. Parsing in `memory_bank_skill/cost_report.py` |
| `mb-upgrade.sh [--check\|--force]` | Self-update the skill from GitHub |
| `mb-version-check.sh [--force]` | Is a newer release out? Compares local `VERSION` against the latest GitHub Release (PyPI JSON as fallback), cached with a TTL. Prints strict JSON (`current`/`latest`/`update_available`/`flavor`/`upgrade_command`/`checked_at`/`source`). Always fail-open — exit 0, silent, never blocks a session. Off: `MB_UPDATE_CHECK=off` |
| `mb-profile.sh` | Rule profile manager: `init`, `show`, `path`, `validate`, `set` — user/project scopes |
| `mb-diff-scope.sh` | L5 diff-scope backstop: compare changed files against an allowed glob scope and report out-of-scope changes (exits 0, JSON report; ADR-4) |
| `mb-fanout.sh` | Stateless fan-out helper: run N branch prompts concurrently via background jobs, capture JSON results, and aggregate into one object — exit-code authority for failed branches (REQ-DF-084) |
| `mb-flow-branch-sink.sh` | Per-branch result sinks with write-once discipline for `<!-- mb-flow -->` fence: each parallel branch writes to its own `.mb-flow/branch-<i>.json` to prevent races (ADR-9) |
| `mb-flow-route.sh` | Deterministic route resolver: apply route-floor rules (REQ-DF-022) to an LLM-proposed or user-supplied route and write the resolved `route:` into the `<!-- mb-flow -->` fence in status.md |
| `mb-flow-sync.sh` | Regenerate the `<!-- mb-flow -->` runtime fence in status.md: emit route, phase, checks, gate, last-verify-sha, stall-count, and stop-reason fields (REQ-DF-030/031/032, REQ-DR-033) |
| `mb-flow-verify.sh` | THE firewall fan-out: run route-relevant check runners, normalize verdicts via `mb-work-severity-gate.sh`, and exit 0/1/2 — the sole exit-code authority of the dynamic-flow firewall (ADR-3) |
| `mb-goal-acceptance.sh` | L5 goal-acceptance aggregator: parse `## Acceptance criteria` checkboxes in goal.md and report whether every criterion is satisfied (exits 0, JSON report; REQ-DF-042) |
| `mb-goal-validate.sh` | Validate a goal.md before a Dynamic Flow run: enforce required sections, acceptance-criteria items, and field completeness — fail-loud exit 1 on malformed goals (REQ-DF-004) |
| `mb-lint-run.sh` | L5 lint runner: auto-detect project stack via `mb-metrics.sh`, map to linter (ruff/shellcheck), run it, and report findings (exits 0, JSON report; ADR-3; unknown stack = SKIP) |
| `mb-no-todo.sh` | L5 residual-placeholder runner: scan target files for TODO/FIXME/HACK markers, reusing `mb_rules_check_lib.sh::scan_placeholders` patterns and exemptions (exits 0, JSON report; REQ-DF-042) |
| `mb-session-prune.sh` | Archive contentless session stubs out of `<bank>/session/` into `session/archive/stubs/`; dry-run is the default, `--apply` performs the move. Also flags/repairs bloated files (`>MB_SESSION_BLOAT_BYTES`) with post-`## Summary` bullets |
| `mb-session-repair.sh [--apply] <file>` | Repair a session file corrupted by the legacy append-after-`## Summary` bug: move turn-bullets back into `## Live log`, reset `summarized=false`, re-cap over-long bullets, keep a `archive/pre-repair/` backup. Dry-run default, idempotent, fail-safe |
| `mb-settings-ensure-timeout.py` | Surgically ensure the SessionEnd `mb-session-end.sh` hook command carries a per-command `timeout` so the Haiku summarizer is not SIGKILLed before writing `## Summary` |
| `mb-subinvoke-resolve.sh` | Resolve the per-agent shell sub-invoke command template for the active agent (mirrors `mb-reviewer-resolve.sh`); used by `mb-fanout.sh` to bake `--cmd` when the operator does not supply one (REQ-DF-082) |
| `mb-brief.sh` | Deterministic helper behind `/mb brief`: `create` (topic + candidate + `--input` documents), `context`, `accept` — the file effects of the brief stage live in a script, not a prompt |
| `mb-brief-validate.sh` | Structural validator for a brief one-pager — section order, required fields, single-page budget |
| `mb_brief_candidate.py` | Candidate inspection for `mb-brief.sh` (contract C6 steps 4–5) |
| `mb-glossary.sh` | Atomic upsert of a single `<term> — <definition>` line in `<bank>/glossary.md`; term and definition are read from files, so no quoting loss (REQ-017) |
| `mb-estimate-check.sh` | Deterministic size-estimate validator: the `/mb discuss` context estimate and the spec-triple / candidate budget gate. No LLM, no PyYAML |
| `mb-estimate-lib.sh` | Sourced parsers for `mb-estimate-check.sh` (context-file and spec/candidate estimates). Not a standalone entry point |
| `mb-interview-artifact-check.sh` | Deterministic structural validator for `/mb discuss` interview artifacts — `plan`, `--require-closed`, `--print-digest`. No LLM |
| `mb-interview-artifact-write.sh` | Deterministic writer for `/mb discuss` file effects: atomic publish, and byte-identity of a rejected target is a script-proven fact rather than a prompt promise |
| `mb-secret-scan.sh` | Canonical secret-scan dispatcher (`transcript` and `brief-input` policies); patterns are single-sourced from `mb-import.py`, never a second regex set |
| `mb-sdd-candidate.sh` | Candidate lifecycle for `/mb sdd` generation: the seam separating a GENERATED `tasks.md` from an ACCEPTED one (`<bank>/tmp/sdd/<topic>/tasks.candidate.md`) |
| `mb-sdd-self-check.sh` | Deterministic executor of the C8 generation self-check battery over a published draft triple, so `commands/sdd.md` decides draft→ready by exit code, not prompt judgement. Pure checker — writes nothing |
| `mb-sdd-self-check-eval.sh` | Sourced half of the C8a battery: how ONE `**Eval:**` declaration is classified in a given phase (`--phase generation` requires red, `--phase done` requires green) |
| `mb-sdd-review-result.sh` | Executable owner of the spec-review exit codes: validation, the append-only record, and 0/1/2 — `commands/sdd.md` owns only the model dispatch |
| `mb_sdd_judge_journal.py` | Judge / override / status half of the spec-review journal (append-only, symlink-safe) |
| `mb-sdd-layers-render.py` | Deterministic renderer for the test-layer tasks and the `## Quality DoD` block |
| `mb-quality-dod.sh` | Render the one canonical `## Quality DoD` block; the orchestrator runs it ONCE per item and hands the same file to implementer, reviewer, and judge |
| `mb_quality_dod.py` | The `## Quality DoD` renderer core — one renderer, three receivers |
| `mb-rules-resolve.sh` | Resolve the rule sources a spec is judged against — `discovery` and `validation` modes behind one JSON contract |
| `mb_rules_resolve.py` | Rule-source resolution core for `mb-rules-resolve.sh` |
| `mb-contract-gate.sh` | Execute a spec's Contract-checkers registry (the fenced ```json``` block of the `**Layer:** contract` task) |
| `mb_contract_gate.py` | Runner for the Contract-checkers registry |
| `mb_contract_registry.py` | The Contract-checkers registry — one reader, one schema, two consumers |
| `mb-work-state-eval.sh` | Sourced eval-first layer for `mb-work-state.sh`: the red→green Eval gate. Not a standalone entry point |
| `mb-work-state-lib.sh` | Sourced helpers for `mb-work-state.sh` that shell out to external tooling (pipeline YAML, uuid). Not a standalone entry point |
| `mb_work_eval_proof.py` | Canonical eval-proof payload for the `mb-work-state` red→green gate |
| `mb_work_source.py` | Shared declaration-source resolution for work-state init and Eval; canonicalizes relative locators before they can change with cwd |
| `mb_work_plan_wrapper.py` | Wrapper-plan resolution for `mb-work-plan.sh` (`linked_spec` / `<!-- mb-stage:N -->`) |
| `mb-backlog-state.sh` | Backlog state machine, hierarchy, and briefs: `transition <I-NNN> <STATE>`, `annotate --brief --parent` |
| `mb_backlog_state_engine.py` | Backlog parser + state engine behind the backlog scripts |
| `mb_backlog_validate.py` | Backlog metadata validation: the brief gate (REQ-007) + single-line safety |
| `mb_roadmap_group.py` | Group-section rendering + progress aggregation for `mb-roadmap-sync.sh` |
| `mb_roadmap_order.py` | Pure ICE-component parsing + priority ordering for `mb-roadmap-sync.sh` |
| `mb_roadmap_plans.py` | Plan-frontmatter parsing + collection for `mb-roadmap-sync.sh` |
| `mb_roadmap_render.py` | Fence handling, bootstrap transfer, and atomic publish for `mb-roadmap-sync.sh` |
| `mb_spec_validate_v2.py` | v2 / C8 battery gates for `mb-spec-validate.sh` |
| `mb_spec_validate_tasks.py` | Per-task structural checks 3–6 for `mb-spec-validate.sh` |
| `mb_spec_validate_structural.py` | Scope classification + structural Eval grammar (REQ-049) |
| `mb_spec_validate_scope_eval.py` | I-174 gate: a task's `**Eval:**` must actually run the test files its `**Scope:**` claims |
| `mb_spec_validate_layers.py` | Test-layer gates C3/C4 and the Contract-checkers schema |
| `mb_spec_validate_graph.py` | `blocked_by` dependency-graph gates (REQ-052 / C8.5) |
| `mb_pipeline_validate_core.py` | Pipeline config validation core for `mb-pipeline-validate.sh` |
| `mb_pipeline_validate_blocks.py` | Per-block pipeline validators (budget … named-pipeline metadata) |
| `mb_pipeline_minimal_yaml.py` | PyYAML-optional minimal loader for `pipeline.yaml` — the zero-dep base |
| `mb_fs_atomic.py` | One atomic file-publish primitive, shared by every writer |

---

## Agents — subagents

| Agent | When to invoke | Prompt |
|-------|----------------|--------|
| `mb-manager` | `/mb context`, `search`, `note`, `tasks`, `done`, `update`, PreCompact hook | `agents/mb-manager.md` |
| `mb-doctor` | `/mb doctor` — memory-bank inconsistencies (use `mb-plan-sync.sh` first, only edit for semantic drift) | `agents/mb-doctor.md` |
| `mb-codebase-mapper` | `/mb map [focus]` — scan the codebase → `.memory-bank/codebase/{STACK,ARCHITECTURE,CONVENTIONS,CONCERNS}.md` | `agents/mb-codebase-mapper.md` |
| `plan-verifier` | `/mb verify` — required before `/mb done` when work followed a plan. Uses `**Baseline commit:**` from plan header for `git diff`, runs `mb-test-run.sh` and `mb-rules-check.sh` directly | `agents/plan-verifier.md` |
| `mb-rules-enforcer` | `/review`, `/commit`, `/pr`, `plan-verifier` step 3.6 — runs `mb-rules-check.sh` (solid/srp, clean_arch/direction, tdd/delta) + LLM ISP/DRY judgment. Returns strict JSON + summary | `agents/mb-rules-enforcer.md` |
| `mb-test-runner` | `/test`, `plan-verifier` step 3.5 — runs `mb-test-run.sh`, correlates failures with session diff. Returns JSON `{stack, tests_pass, tests_total, failures[], coverage, duration_ms}` | `agents/mb-test-runner.md` |
| `mb-reviewer` | `/mb work` legacy single-reviewer fallback — reads stage diff + `pipeline.yaml:review_rubric`, emits structured JSON verdict | `agents/mb-reviewer.md` |
| `mb-reviewer-logic` | `/mb work` governed review ensemble — correctness / logic aspect reviewer with scoped context | `agents/mb-reviewer-logic.md` |
| `mb-reviewer-tests` | `/mb work` governed review ensemble — test-coverage / quality-of-tests aspect reviewer | `agents/mb-reviewer-tests.md` |
| `mb-reviewer-quality` | `/mb work` governed review ensemble — code-quality / maintainability aspect reviewer | `agents/mb-reviewer-quality.md` |
| `mb-reviewer-security` | `/mb work` governed review ensemble — security aspect reviewer | `agents/mb-reviewer-security.md` |
| `mb-reviewer-scalability` | `/mb work` governed review ensemble — performance / scalability aspect reviewer | `agents/mb-reviewer-scalability.md` |
| `mb-reviewer-lead` | `/mb work` governed review — synthesizes aspect reports, verifies previous master report closure, separates blockers from backlog | `agents/mb-reviewer-lead.md` |
| `mb-judge` | `/mb work` governed final gate — decides GO / GO_WITH_BACKLOG / NO_GO from plan, verifier, lead-review, and evidence | `agents/mb-judge.md` |
| `mb-engineering-core` | **[partial — not dispatched directly]** Composed into every dev-role agent below at install time (`compose:` frontmatter). Carries the shared discipline: TDD, Contract-First, Clean Architecture, production-wiring, evidence-before-claims (Iron Law), escalation, STATUS contract, anti-rationalization. Excluded from the `~/.claude/agents/` registry via `partial: true` frontmatter. | `agents/mb-engineering-core.md` |
| `mb-tooling-core` | **[partial — not dispatched directly]** Composed at install time into the dev-role agents, `mb-reviewer`, and `plan-verifier`. Carries the graph-first, fail-open code-understanding routing (`code_context` / `graph_neighbors` / `graph_impact` / `graph_tests` / `search_code` / `recall`). Optional indexes degrade to `Grep`/`Read`. Excluded from the registry via `partial: true`. | `agents/mb-tooling-core.md` |
| `mb-developer` | `/mb work` — generic implementer when no specialist role matches. Discipline from `mb-engineering-core` + DoD-driven implementation | `agents/mb-developer.md` |
| `mb-architect` | `/mb work` — architecture / ADR / system-design specialist. Domain modelling, interface definition, refactoring strategy | `agents/mb-architect.md` |
| `mb-backend` | `/mb work` — APIs, services, database, async/concurrency, server-side business logic | `agents/mb-backend.md` |
| `mb-frontend` | `/mb work` — React/Vue/Svelte/Solid components, browser UI, accessibility, responsive layouts | `agents/mb-frontend.md` |
| `mb-ios` | `/mb work` — SwiftUI/UIKit, Combine, async/await, Apple platform conventions | `agents/mb-ios.md` |
| `mb-android` | `/mb work` — Jetpack Compose, Kotlin coroutines, Hilt/DI, Room, Material3 | `agents/mb-android.md` |
| `mb-devops` | `/mb work` — CI/CD, Docker, Kubernetes, Terraform, observability, release engineering | `agents/mb-devops.md` |
| `mb-qa` | `/mb work` — test design, coverage strategy, edge-case enumeration, flake elimination, contract tests | `agents/mb-qa.md` |
| `mb-analyst` | `/mb work` — data / analytics / metrics: SQL, dashboards, cohorts, ETL pipelines, instrumentation | `agents/mb-analyst.md` |
| `mb-research` | `/mb research` (and broad `/mb work` research steps) — graph-first, multi-source research over codebase + project memory + library docs + GitHub prior-art + open web; read-only (no Write/Edit), returns `file:line` / source-grounded conclusions, degrades to `Grep` when indexes are absent | `agents/mb-research.md` |
| `mb-researcher` | `/mb work` governed research role (wired in `pipeline.default.yaml`) — ecosystem research, implementation reconnaissance, source comparisons, technical due diligence, and evidence-backed option matrices before planning or implementation | `agents/mb-researcher.md` |
| `mb-wiki-author` | `/mb wiki` — bulk worker pinned to a small model (`model: haiku`). Writes one codebase-wiki article per community from a deterministic evidence pack | `agents/mb-wiki-author.md` |
| `mb-wiki-synthesizer` | `/mb wiki` — finds surprising cross-community connections, emits strict-JSON `semantic` edges | `agents/mb-wiki-synthesizer.md` |

> **Composition.** An agent lists the partials it needs under `compose:` in its frontmatter; the
> installer (`scripts/mb-agent-render.py`) places those partials above the agent's own text, so the
> installed agent carries the shared discipline and a dispatch by name needs only the task data.
> Reading a role file from the skill directory directly (clients without named dispatch) means reading
> its `compose:` partials first.

Plan authoring and ML-result evaluation stay with the main agent: it holds the user's context and decisions. `mb-architect` executes the architecture items of an approved plan.

> **Plan hierarchy:** Phase → Sprint → Stage. See `references/templates.md` § *Plan decomposition* for size thresholds, terminology, and when to use which level. Cyrillic «Этап / Спринт / Фаза» — legacy alias, allowed only in `plans/done/*.md`.

### Invocation

Dispatch agents by name — `Agent(subagent_type="mb-manager", description="…", prompt="action: <action>\n\n<context>")`.
Model, reasoning effort, and tools come from the installed agent definition or `pipeline.yaml`, not from the call.
The commands write this Claude Code form; other hosts dispatch the same installed role with their own tool:

| Host | Dispatch by name | Where the role is installed |
|---|---|---|
| Claude Code | `Agent(subagent_type=<name>, prompt=…)` (older builds: `Task`) | `~/.claude/agents/<name>.md` |
| OpenCode | `task(subagent_type=<name>, prompt=…)` | `.opencode/agent/<name>.md` |
| Codex | `spawn_agent(agent_type=<name>, message=…)`; a pipeline `thinking` goes to `reasoning_effort` | `~/.codex/agents/<name>.toml` |
| Pi | `mb_dispatch_subagent(role=<name>, task=…)` or pi-subagents `subagent(agent=<name>, task=…)`; `thinking` passes through | `~/.pi/agent/agents/<name>.md` |

A host without named dispatch reads the role file and its `compose:` partials and does the work inline.

---

## Hooks

Lifecycle hooks shipped in `hooks/`. Installed automatically by `install.sh` (Claude Code, Cursor, Codex, OpenCode); see `references/hooks.md` for per-host wiring details.

| Hook | Trigger | Purpose |
|------|---------|---------|
| `_skill_root.sh` | sourced helper | Resolve bundled skill root and effective Memory Bank path for hook scripts |
| `block-dangerous.sh` | PreToolUse (Bash) | Block dangerous shell patterns (`rm -rf /`, `~`, `/*`) — best-effort guardrail |
| `mb-protected-paths-guard.sh` | PreToolUse (Write/Edit) | Block writes to `pipeline.yaml:protected_paths` (e.g. `.env`, CI configs) |
| `mb-ears-pre-write.sh` | PreToolUse (Write) | Validate REQ bullets in `context/<topic>.md` against EARS patterns before save |
| `mb-context-slim-pre-agent.sh` | PreToolUse (Task) | Slim oversized agent prompts on subagent dispatch |
| `mb-sprint-context-guard.sh` | PreToolUse (Task) | Hard-stop subagent dispatch if `mb-session-spend.sh` shows budget exhaustion |
| `mb-graph-nudge.sh` | PreToolUse (Grep/Bash) | Non-blocking nudge toward `mb-graph-query` on structural greps, only when the code graph is fresh; throttled 1×/session, `MB_GRAPH_NUDGE=off`, fail-safe |
| `mb-plan-sync-post-write.sh` | PostToolUse (Write) | Auto-sync plan ↔ checklist + roadmap after editing a plan file |
| `file-change-log.sh` | PostToolUse (Write/Edit) | Append change log + scan for placeholders / secrets in committed files |
| `session-end-autosave.sh` | SessionEnd | Memory Bank auto-capture (`MB_AUTO_CAPTURE=auto\|strict\|off`) when `/mb done` was skipped |
| `mb-core-cap-guard.sh` | Stop | Enforce the core-file line caps (AGR-043): runs `mb-core-cap.sh fix`, and when the bank is still over cap blocks the stop **once per session** (marker `<bank>/.core-cap.nudged.<session_id>`) with `dispatch MB Manager action: actualize --strict`. **On by default** — kill-switch `MB_CORE_CAP=off` (env or `.mb-config core_cap=off`); `stop_hook_active`, no bank, or any tool error → allow |
| `mb-pre-compact.sh` | PreCompact (Claude Code) / preCompact (Cursor) | Handoff-v2: runs `mb-handoff.sh --actualize` to write a fresh `handoff/latest.md` capsule before compaction. Bounded to ~2s, never blocks (`MB_PRECOMPACT_HANDOFF=off` to disable) |
| `mb-session-start-context.sh` | sessionStart (Cursor) | Auto-inject compact Memory Bank context at session start (`MB_AUTOLOAD_CONTEXT=off` to disable) |
| `mb-session-turn.sh` | Stop | Session memory: append one per-turn bullet (request + tools + files) to `session/*.md`, no LLM (`MB_SESSION_CAPTURE=off` to disable) |
| `mb-session-end.sh` | SessionEnd | Session memory: Haiku summary + gated Sonnet auto-notes; updates `session/_recent.md` |
| `mb-session-start.sh` | SessionStart | Session memory: inject `# Recent Sessions` from `session/_recent.md` + a how-to cheat-sheet (graph / `/mb recall` / `/mb context` quick ref), read-only (`MB_SESSION_CHEATSHEET=off` to drop the cheat-sheet) |
| `mb-update-notify.sh` | SessionStart | "A newer release is out?" notice: silent when current, else a ≤3-line notice with `current -> latest` + the exact upgrade command for the detected install flavor (git/pipx/pip/brew), local-only (`--cache-only`, no network), fail-open, never blocks (`MB_UPDATE_CHECK=off` to disable). Opt-in `MB_AUTO_UPDATE=on` auto-applies for a clean git-clone install only |
| `mb-recall.sh` | `/mb recall <query>` | Session memory: hybrid recall — model-free BM25 matches first (over `agreements.md` + `progress.md` + `notes/` + `session/`; embeddings opt-in via `MB_SEMANTIC_BACKEND=embeddings`) + ripgrep lexical fallback |
| `mb-semantic-recall.sh` | UserPromptSubmit | Session memory: inject `# Relevant Memory` — top-K relevant past-chat snippets via the model-free BM25 index (I-132: ~50 MB / <0.5 s per prompt; prompt-gated — slash-commands and prompts under `MB_SEMANTIC_MIN_PROMPT` chars skip the spawn); fail-safe (`MB_SEMANTIC=off` to disable) |
| `mb-reindex.sh` | `/mb reindex` | Session memory: (re)build the per-project semantic vector index (`--full`/`--incremental`); bootstraps the venv if needed |
| `mb-semantic-bootstrap.sh` | sourced by `/mb reindex` | Session memory: idempotent venv + fastembed/numpy installer (opt-in; semantic layer falls back to lexical without it) |
| `mb-flow-closure-guard.sh` | Stop | Dynamic-flow closure gate: when a flow is active, blocks the Stop event if `mb-flow-verify.sh` exits non-zero, preventing the agent from declaring done on a red firewall (REQ-DF-045) |
| `mb-drive-resume-gate.sh` | Stop | Drive-loop resume-gate: while a `/mb drive` loop is armed, blocks a stop when the goal is not done AND no stop condition fired, so the loop resumes instead of ending early (REQ-DR-032). Decides by reading files only — never runs the firewall or a test battery (`MB_DRIVE_RESUME_GATE=off` to disable) |
| `mb-session-catchup.sh` | SessionStart | Lazy summarize sessions left `summarized:false` by a prior SIGKILLed SessionEnd; dispatched in the background so session startup is never delayed (`MB_CATCHUP_MAX` tuneable, off via `MB_SESSION_CAPTURE=off`) |
| `mb-session-summarize.sh` | sourced/dispatched (not directly registered) | Generate the Haiku `## Summary` for one session file and rotate `_recent.md`; extracted from `mb-session-end.sh` (DRY) and driven by both the SessionEnd hook and `mb-session-catchup.sh` |

---

## Host-specific notes

### Claude Code and native memory

Claude Code has built-in `auto memory` (user-level cross-project memory in `~/.claude/projects/.../memory/`). This skill does **not replace** it — the two complement each other:

| Aspect | `.memory-bank/` | Native `auto memory` |
|--------|------------------|----------------------|
| Scope | Project | User, cross-project |
| Stores | Status, plans, checklists, research, ADRs, lessons | Preferences, role, feedback |
| Owner | Team (via git) | Individual user |

Rule of thumb: if it helps a teammate pick up the project tomorrow, store it in `.memory-bank/`. If it helps you in another project, store it in native memory. They can coexist without conflict.

### Codex

For Codex, this skill is positioned as a global skill bundle plus a guidance layer:
- discovery goes through `~/.codex/skills/memory-bank/`
- global entrypoint/guidance goes through `~/.codex/AGENTS.md`
- hook/config integration remains primarily project-level through `.codex/`

Codex therefore uses the same Memory Bank workflow, but it does not need to expose the same native command surface as Claude Code/OpenCode.

### Cursor

Cursor is a first-class global target. `install.sh` writes five artifacts to `~/.cursor/`:

| Artifact | Purpose |
|----------|---------|
| `~/.cursor/skills/memory-bank/` | Personal skill alias — Cursor auto-discovers it by description |
| `~/.cursor/hooks.json` | Global hooks (10 commands → skill bundle `hooks/`): `sessionStart` (auto-context), `sessionEnd`, `preCompact`, `beforeShellExecution`, four `preToolUse` matchers (`Write|Edit`, `Write`, `Task`×2), two `postToolUse` matchers. Each command runs `~/.cursor/skills/memory-bank/hooks/<script>.sh` with `MB_AGENT=cursor`. Tagged `_mb_owned: true` so user hooks are preserved |
| `~/.cursor/commands/*.md` | User-level slash commands mirrored from the skill `commands/` directory |
| `~/.cursor/AGENTS.md` | Marker section `memory-bank-cursor:start/end` — entrypoint for future Cursor versions that read global `AGENTS.md` |
| `~/.cursor/memory-bank-user-rules.md` | Paste-ready rules bundle for **Settings → Rules → User Rules** (Cursor exposes no file API for global User Rules, so this is a one-time manual step) |

Cursor User Rules paste flow:

```bash
# macOS
pbcopy < ~/.cursor/memory-bank-user-rules.md
# Linux
xclip -selection clipboard < ~/.cursor/memory-bank-user-rules.md
```

The project-level adapter (`.cursor/rules/memory-bank.mdc` + `.cursor/hooks.json`) remains available and is installed only when the user passes `--clients cursor`. Global and project-level installs coexist — Cursor merges hooks from both.

---

## Private content — `<private>...</private>` (since v2.1)

Markdown syntax for excluding sensitive information (client data, API keys, partner names) from indexing and search:

```markdown
---
type: note
tags: [auth, partner-x]
importance: high
---

Discussed with client <private>Jane Doe, +1-555-***</private>.
Integration with <private>api_key=sk-abc123...</private> is scheduled for Tuesday.
```

**Protection model:**
- Content inside `<private>...</private>` does **not** go into `index.json` (neither `summary` nor `tags`)
- `mb-search` output redacts it as `[REDACTED]` (inline) or `[REDACTED match in private block]` (multi-line)
- The entry gets a `has_private: true` flag for downstream filtering
- An unclosed `<private>` without `</private>` makes the rest of the file private (fail-safe)
- `hooks/file-change-log.sh` warns when committing a file containing `<private>` blocks (reminder to review git exposure)

**Double confirmation for reveal:**
```bash
# Rejected without env:
mb-search --show-private <query>
# [error] --show-private requires MB_SHOW_PRIVATE=1

# Only with explicit opt-in:
MB_SHOW_PRIVATE=1 mb-search --show-private <query>
```

**Important:** `<private>` protects against leakage through `index.json` / `mb-search`, but it does **not** filter `git diff`. For full protection, consider `.gitattributes` filters or git hooks.

---

## Auto-capture (since v2.1)

The SessionEnd hook automatically appends a placeholder entry to `progress.md` when a session ends without an explicit `/mb done`. Work is not lost even if manual actualization was skipped.

**Modes (`MB_AUTO_CAPTURE` env):**
- `auto` (default) — hook writes an entry on session end
- `strict` — hook skips but prints a warning to stderr (for flows where manual actualization is required)
- `off` — full noop

**How it works:**
- After successful `/mb done`, the command writes `.memory-bank/.session-lock` → the hook sees the fresh lock (<1h) and skips auto-capture (manual actualization already happened)
- Without a lock, the hook adds a short note to `progress.md`. Full details can be reconstructed by `/mb start` in the next session (MB Manager can read the JSONL transcript)
- Concurrency-safe through a short `.auto-lock` (30 seconds) — prevents duplicates on parallel invocations
- Idempotent by `session_id` — same session + same day = one entry

**Opt-out:** `export MB_AUTO_CAPTURE=off` in `~/.zshrc` or disable the hook via `/mb upgrade` once that flag is available.

---

## Session memory — native session logging (session-memory subsystem)

A richer, native alternative to the placeholder auto-capture above. Logs every session to
`.memory-bank/session/*.md` (markdown, git-tracked) and auto-curates notes. Scripts live in
`~/.claude/hooks/` (and the repo's `.memory-bank/bin/` when present); registered in `settings.json`.

- **Stop → `mb-session-turn.sh`** — appends one `## Live log` bullet per turn (last user request,
  tools, touched files) **without an LLM**; persists the transcript path to frontmatter; deduped by
  turn `uuid` so duplicate (project + global) registration is safe. Guards: `stop_hook_active`,
  `MB_CAPTURE_SUBPROCESS`, `MB_SESSION_CAPTURE=off`, missing jq → exit 0.
- **SessionEnd → `mb-session-end.sh`** — a Haiku `claude -p` writes `## Summary` + updates
  `_recent.md`; then a **gated** Sonnet judge (only if the session had Write/Edit or ≥4 turns) writes
  0–2 durable `notes/`. Idempotent by `session_id` (`summarized` frontmatter flag). Anti-recursion:
  `env -u CLAUDECODE MB_CAPTURE_SUBPROCESS=1 claude -p --strict-mcp-config --no-session-persistence --no-chrome`.
- **SessionStart → `mb-session-start.sh`** — injects `# Recent Sessions` from `_recent.md`;
  drains stdin (`exec < /dev/null`) to avoid hanging on `claude --resume` (macOS). Read-only (runs
  even while capture is `off`). When a code graph exists it also dispatches the bounded
  `mb-graph-query.py catchup` detached (flock + budget + cooldown, result in
  `codebase/.graph-catchup.log`) without blocking startup. It catches the graph up to new
  commits and tracked edits only — a bank whose graph is merely OLD (no drift, empty dirty
  queue) still needs `/mb graph --apply`. `MB_GRAPH_CATCHUP=off` disables it.
- **Recall:** `/mb recall <query>` → hybrid semantic + lexical search over `session/` + `notes/`,
  fused by RRF (Reciprocal Rank Fusion) when the semantic backend is available; fails open to
  lexical-only otherwise.

**Off-switch:** `export MB_SESSION_CAPTURE=off`. **Suppress the legacy stub** (above) with
`MB_AUTO_CAPTURE=off` so `progress.md` is not double-written once this subsystem owns capture.
**Cost:** a significant session spends 2 `claude -p` calls on SessionEnd (Haiku summary + Sonnet
judge); trivial sessions spend only the summary. **Portable lock:** mkdir-based (no `flock` on macOS).
Active only where an active Memory Bank resolves.

---

## PreCompact handoff capsule (handoff-v2)

The PreCompact hook `hooks/mb-pre-compact.sh` runs just before context compaction. It invokes
`scripts/mb-handoff.sh --actualize <bank> pre_compact`, which writes a fresh handoff capsule to
`.memory-bank/handoff/latest.md`. The NEXT session's SessionStart hook
(`hooks/mb-session-start-context.sh`) prepends that capsule when it is newer than the most recent
`progress.md` entry, so the agent resumes from an up-to-date snapshot instead of stale state.

**Never blocks compaction (design §9):**
- bounded to ~2s via a portable background-poll-and-kill loop (no `timeout`/`flock`, macOS-safe)
- on timeout, actualize failure, or missing handoff script → one-line stderr WARN and `exit 0`
- on no resolvable bank → silent `exit 0`
- on success → one-line stderr marker `[mb] handoff capsule actualized (pre_compact)`

**Opt-out:** `export MB_PRECOMPACT_HANDOFF=off`.

---

## Cross-session coordination — `.memory-bank/COORDINATION.md`

When two or more sessions work in the same working tree in parallel (two agent CLIs, or agent + human), they coordinate through a single append-only board file at the bank root — `COORDINATION.md`. Opt-in by nature: the first session that learns about a parallel session creates it; no board file → no protocol overhead.

- **Read it with `scripts/mb-coord.sh active`**, never `cat` — the board is append-only and reaches hundreds of KB; the command prints active FREEZEs, HANDOVERs with no ACK, the last 3 entries and a totals line. Write entries with `mb-coord.sh append --type <T> --title <t>`.
- Entries `## <TYPE> · YYYY-MM-DD · <scope>` (`FREEZE` / `LIFT` / `HANDOVER` / `ACK` / `STATUS`), never edited after append (same invariant as `progress.md`); a LIFT cancels an earlier FREEZE with the same scope, an ACK cancels an earlier HANDOVER. Untagged legacy headings read as STATUS.
- Checkpoints — every session reads the board: at session start (`/mb start` / `/mb context` surface it when present), before starting a stage/plan item, before ANY commit, before editing a shared-watchlist file; and appends a COMMIT entry (hash + scoped file list) after committing.
- Shared-tree hard rules: never `git add -A`; commit only your own work with ordering for interleaved files agreed on the board; full suite green before commit; surprise foreign diffs escalate on the board instead of being reverted; affected plans carry a ⚠️ pointer to the board (compaction-proof).
- Full protocol (entry conventions, race handling, trust rules, hookup prompt for a new session): `references/coordination.md`.

---

## Running list of agreements — `.memory-bank/agreements.md`

The canonical registry of confirmed decisions currently in force, distinct from `progress.md`
(narrative history) and ADRs (rationale for the hard-to-reverse subset). Every mutation goes
through `scripts/mb-agree.sh` (`add | supersede | defer | reject | question | resolve | list |
sync`) — never a direct model edit — and auto-syncs a managed block
(`<!-- mb-agreements:start/end -->`) into project-root `CLAUDE.md`/`AGENTS.md` so a fresh session
sees every active agreement without being reminded.

- **Lazy activation, opt-in by nature:** the rules trigger ships with the skill for every project,
  but zero files/blocks exist until the first `/mb agree add` — no added tokens in banks that never
  use the feature. Kill-switch: `MB_AGREEMENTS=off` (env or `.mb-config`).
- **Model conduct:** only an explicitly confirmed user decision is written, announced visibly as
  `→ AGR-NNN записано: <statement>`; unconfirmed hypotheses go to Open Questions instead.
- **`/mb verify` integration:** when `agreements.md` exists, the Plan Verifier classifies every
  active agreement as satisfied / violated / not-applicable; a violation fails the verdict.
- Full protocol (what is/isn't an agreement, anti-examples, statuses, ADR routing): `references/agreements.md`. Command reference: `commands/agree.md`.

---

## References

- Rule profiles schema (dimensions, immutable baseline, precedence, validation): `references/rules-profile.schema.md`
- Design principles (inviolable memory promise + configurable layers): `references/design-principles.md`
- Metadata protocol + `index.json` + 8 key rules: `references/metadata.md`
- Plan decomposition (Phase / Sprint / Stage), templates, drift checks: `references/templates.md`
- Planning + Plan Verifier workflow: `references/planning-and-verification.md`
- `/mb work` reference material (workflow modes, JSON schema, examples, scripts, parallel runs): `references/work-reference.md`
- `/mb work` sprint contracts, progress trend, strategic pivoting: `references/work-loop-v2.md`
- Structure of `.memory-bank/`: `references/structure.md`
- Code graph cookbook (jq library, `graph.json` schema, intelligence layer, semantic-search routing): `references/code-graph.md`
- Workflow (session lifecycle): `references/workflow.md`
- Session memory (cross-chat capture, `/mb recall`, session-doctor): `references/session-memory.md`
- Cross-session coordination board (`COORDINATION.md` protocol): `references/coordination.md`
- Running list of agreements (`agreements.md` protocol, statuses, anti-examples): `references/agreements.md`
- Command file template: `references/command-template.md`
- Hooks (per-host wiring + lifecycle): `references/hooks.md`
- Adapter manifest schema: `references/adapter-manifest-schema.md`
- Tags vocabulary: `references/tags-vocabulary.md`
- CLAUDE.md auto-generation template: `references/claude-md-template.md`
- CHANGELOG: `CHANGELOG.md`
- Migration v1→v2: `docs/MIGRATION-v1-v2.md`
- Primary entrypoint:
  - `/mb` — if the host supports native commands
  - `commands/mb.md` / `memory-bank` CLI — if native command surface is unavailable
