---
name: chunky
license: MIT
description: Spec-first workflow for planning and shipping large features with coding agents. Chunks work into independently executable units with minimal context routing. Includes pre-flight Q&A to surface unknowns before execution and knowledge packs for external docs (llms.txt, API references). Use when planning a large feature, breaking down complex scope, chunking work for agents, oneshot implementation, or spec-driven development.
---

# Chunky

Spec-first, chunk-based feature shipping for coding agents.

When this skill is activated, follow the three phases below in order. Each phase produces concrete artifacts in the target repo. Do not skip phases.

## Assumptions

- **CWD is always the target repo root.**
- Scripts and assets live in the skill directory — the directory containing this `SKILL.md` file. Derive the skill directory from this file's path and use it when running scripts (e.g., if this file is at `/home/user/.agents/skills/chunky/SKILL.md`, the skill directory is `/home/user/.agents/skills/chunky`).
- `jq` is required for chunk/task context resolution and wave planning. Only `resolve-context.sh --mode plan` degrades gracefully without it.

## Phase 1 — Design

**Goal:** Produce a single spec document the rest of the workflow depends on.

1. Create `docs/SPEC.md` in the target repo.
2. The spec must include these sections:
   - **Problem / Goal** — what we're building and why.
   - **Non-goals** — what is explicitly out of scope.
   - **Acceptance criteria** — global conditions for the feature to be considered done.
   - **Constraints** — technical, security, or compatibility requirements.
   - **Verification approach** — how we prove it works (test commands, manual steps).
3. Stop. Before moving to Phase 2, confirm: every acceptance criterion is testable, constraints don't contradict goals, and the verification approach can actually prove the criteria are met.

## Phase 2 — Plan

**Goal:** Break the spec into independently executable chunks with routing metadata.

### Step 1: Create `llms-map.json`

Use `assets/llms-map.template.json` as a starting point. Populate:

- `schema_version` — use `"1.0.0"`.
- `updated` — today's date in `YYYY-MM-DD` format.
- `baseline_read_order` — files an agent should read when planning (at minimum `docs/SPEC.md`).
- `sub_agent_context.always_read` — files loaded for every chunk (at minimum `docs/SPEC.md`).
- `context_budgets` — max files and bytes per mode. Keep chunk budgets small.
- `verification.per_chunk` — commands every chunk must pass after implementation.
- `chunks` — one entry per chunk. Each chunk requires:
  - `title` — short name.
  - `target` — the directory or package this chunk modifies.
  - `depends_on` — array of chunk IDs that must be completed first (empty array if none).
  - `docs` — files the agent needs to read for this chunk.
  - `capsule` — path to the chunk capsule file (e.g. `docs/chunks/P1-C1.md`).
  - `complexity` — `"S"`, `"M"`, or `"L"`.

Optional fields: `knowledge_packs`, `preflight`, `task_router`, `orchestrator`, `phases`, `freshness`. See `assets/llms-map.schema.json` for the full schema.

### Step 2: Write chunk capsules

For each chunk in `llms-map.json`, create `docs/chunks/<CHUNK_ID>.md` using the template in `references/schema-and-templates.md`. Each capsule must include what to build, acceptance criteria, file ownership, and verification commands.

### Step 3: Create `llms.txt`

Create `llms.txt` in the target repo root. Use `assets/llms.txt.template` as a starting point. It must include:

1. What this repo/feature is.
2. Start here → `docs/SPEC.md`.
3. Chunk navigation → `llms-map.json` and `docs/chunks/`.
4. Verification commands that must pass.

### Step 4: Register knowledge packs

If any chunk depends on external documentation (library docs, API references, llms.txt files), add a `knowledge_packs` map to `llms-map.json` and reference pack IDs from each chunk's `knowledge_packs` array. See `references/schema-and-templates.md` for the format.

### Step 5: Pre-flight Q&A

The preflight has two stages. Stage A is read-only — no file edits. Stage B writes the results.

#### Stage A — Draft questions (read-only)

1. Read the spec, all chunk capsules, and any knowledge pack URLs registered in `llms-map.json`.
2. Identify every question the agent cannot answer from available context. Only ask questions that would change code, schema, verification, rollout, or security decisions. For anything else, state an assumption.
3. Present the questions **in the conversation** (not in a file yet) using this format:

```
## Pre-flight Questions

### Blocking (must answer before execution)
1. <question> — Assumption if unanswered: <default>
2. <question>

### Non-blocking (will assume default unless overridden)
3. <question> — Default assumption: <assumption>
```

4. **Stop. Do not proceed.** Ask the human to reply with numbered answers. Do not narrate next steps or continue into Phase 3.

> **Claude Code hint:** If available, use Plan mode or a Plan subagent for Stage A to enforce read-only research and prevent accidental edits.
>
> **Codex hint:** Use the `update_plan` tool to track preflight status (Drafting → Awaiting answers → Recording → Done).

#### Stage B — Record answers

After the human answers (or marks questions N/A):

1. Create `docs/PREFLIGHT_QA.md` using the template in `references/schema-and-templates.md`.
2. Transcribe all questions, answers, decisions, and discovered constraints into the file.
3. Set `preflight.doc` in `llms-map.json` to `"docs/PREFLIGHT_QA.md"`.
4. If any answer reveals new constraints, update `docs/SPEC.md` and affected chunk capsules.
5. If any answer reveals missing external docs, register them in `knowledge_packs` and add references to the relevant chunks.

Confirm before proceeding:
- [ ] All blocking questions answered or marked N/A with stated assumption.
- [ ] `docs/PREFLIGHT_QA.md` written and complete.
- [ ] `llms-map.json` `preflight.doc` set.
- [ ] Spec and capsules updated if answers changed constraints.

### Step 6: Plan execution waves

Chunks that share no dependencies can run in parallel. Derive execution waves automatically:

```bash
$SKILL_DIR/scripts/plan-waves.sh --map llms-map.json --waves
```

This computes waves from the `depends_on` graph — wave 1 is all chunks with no dependencies, wave 2 is chunks whose deps are all in wave 1, and so on. Review the output. If chunks in the same wave touch overlapping files, either add a `depends_on` edge or split the chunk.

You may optionally materialize waves in `llms-map.json` under `orchestrator.waves` for readability, but this is not required — the script derives waves from the dependency graph at execution time.

#### Human gates (optional)

By default, execution proceeds autonomously through all waves without human approval. Only add `orchestrator.human_gates` when a wave boundary involves:

- Security-sensitive changes (auth, crypto, secrets)
- Billing or entitlement logic
- Destructive migrations (data loss risk)
- Production configuration or infrastructure

Gates pause between waves. Example: `"after_wave_2": ["approve before proceeding"]` means pause after wave 2 completes and await human approval before starting the next wave.

### Step 7: Validate

Run these from the target repo root (replace `$SKILL_DIR` with the absolute path to this skill's directory):

```bash
$SKILL_DIR/scripts/check-agent-context.sh .
$SKILL_DIR/scripts/validate-llms-map-schema.sh --map llms-map.json
```

If either fails, fix the artifacts before proceeding.

## Phase 3 — Execute

**Goal:** Implement all chunks with maximum parallelism and minimal human intervention.

Execution proceeds wave by wave. All chunks in a wave run in parallel unless they share file ownership — in that case, add a `depends_on` edge or move one to a later wave.

### Execution loop

Repeat until all chunks are done:

#### 1. Get the next runnable chunks

```bash
$SKILL_DIR/scripts/plan-waves.sh --map llms-map.json --next
# or, if tracking completion:
$SKILL_DIR/scripts/plan-waves.sh --map llms-map.json --next --done docs/CHUNKS_DONE.txt
```

This outputs the chunk IDs that can run now (all dependencies satisfied).

#### 2. Execute all runnable chunks in parallel

For **each** chunk in the runnable set, do the following simultaneously:

**a. Resolve context:**

```bash
$SKILL_DIR/scripts/resolve-context.sh --mode chunk --chunk <CHUNK_ID> --map llms-map.json
```

**b. Fetch external docs:** If the resolver emits `knowledge_packs` on stderr, fetch those URLs (prefer `llms_full_url`, fall back to `llms_txt_url` or `url`). Use these as authoritative references. Do not guess at APIs or conventions covered by a knowledge pack.

**c. Implement:** Read **only** the resolved context pack and fetched knowledge packs. Do not browse the repo. If you discover missing context, update the chunk's `docs` in `llms-map.json` and its capsule, then re-resolve.

**d. Verify:** Run the chunk's verification commands (from the capsule and `verification.per_chunk` in `llms-map.json`). Confirm all acceptance criteria are met. Fix and re-verify until all checks pass.

#### 3. Mark completion

The coordinating agent (main thread / lead) appends each completed chunk's ID to `docs/CHUNKS_DONE.txt` (one ID per line) after it passes verification. Do not let parallel workers write to this file directly — the coordinator owns it.

#### 4. Advance to the next wave

Re-run `plan-waves.sh --next --done docs/CHUNKS_DONE.txt` to get the next runnable set. Repeat until no chunks remain.

### Parallelism by environment

The execution loop above is environment-agnostic. Use your agent's native parallelism primitives to run chunks concurrently:

> **Amp / Claude Code hint:** Use the Task tool to spawn one subagent per chunk in the runnable set. Each subagent gets its own context window, resolves context, implements, and verifies independently. The main thread coordinates: computes the runnable set, spawns tasks, collects results, updates `docs/CHUNKS_DONE.txt`, and advances to the next wave.

> **Claude Code agent team hint:** For large wave sizes (4+ chunks), consider agent teams instead of subagents. The lead assigns one chunk per teammate. Teammates work in separate sessions with inter-agent messaging — useful when chunks in the same wave need light coordination. Pre-approve common file operations in permission settings to reduce interruptions.

> **Codex hint:** Use background tasks to run chunks in parallel. Each background task handles one chunk's resolve → implement → verify cycle.

### Sequential fallback

If your environment does not support parallel execution, execute chunks one at a time in dependency order. The loop is the same — the runnable set just processes sequentially.

## Execution Modes

The context resolver supports three modes:

| Mode | When | Command |
|------|------|---------|
| **chunk** | Implement one chunk | `--mode chunk --chunk <CHUNK_ID>` |
| **task** | Route a keyword to likely chunks | `--mode task --task <keyword>` |
| **plan** | Load full planning context | `--mode plan` |

The wave planner supports two modes:

| Mode | When | Command |
|------|------|---------|
| **waves** | Show all derived waves | `--waves` |
| **next** | Show next runnable chunks | `--next [--done <file>]` |

## Skill Contents

- `SKILL.md` — this file
- `scripts/resolve-context.sh` — resolve minimal context pack from `llms-map.json`
- `scripts/plan-waves.sh` — derive execution waves and next runnable chunks from dependency graph
- `scripts/check-agent-context.sh` — validate artifact coherence
- `scripts/validate-llms-map-schema.sh` — validate `llms-map.json` against schema
- `assets/llms-map.schema.json` — canonical JSON schema
- `assets/llms-map.template.json` — starter template for `llms-map.json`
- `assets/llms.txt.template` — starter template for `llms.txt`
- `references/schema-and-templates.md` — quick reference for schemas and templates
