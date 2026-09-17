---
name: promptize
description: >-
  Transforms short natural-language requests into repository-aware engineering
  task prompts after reuse lookup, ultra/micro gates, and delta inspect.
  Use when the user starts with /promptize, or asks to promptize / expand a
  brief request into an engineering spec. Supports --execute, --full, --minimal,
  --compress, --caveman, --save-to-file, and --save. Default compact; auto-minimal
  for ultra-low tasks; Caveman prose compression for agent handoffs.
  File-based Promptize reuse (exact/normalized) in SESSION-CACHE — no Redis.
disable-model-invocation: true
version: 2.3.0
---

# Promptize

When the user message begins with `/promptize`, or the user explicitly asks to **promptize** / expand a short request into an engineering task prompt, activate Promptize mode.

**Purpose:** Produce a self-contained, repository-aware engineering task prompt **before** implementation — ultra-lean by default — without a heavyweight engineering report.

**Promptize specification version:** 3  
**Edition:** Ultra Lean (v2.3 — Caveman & Cavecrew Enhanced)

## References

- Token efficiency: [../shared/token-efficiency.md](../shared/token-efficiency.md)
- Selective Caveman policy: [../shared/caveman-token-policy.md](../shared/caveman-token-policy.md)
- Session cache + Promptize reuse: [../shared/context-cache.md](../shared/context-cache.md)
- Unified inspect: [../shared/inspect.md](../shared/inspect.md)
- Gate order (reuse → ultra → micro → delta): [inspection.md](inspection.md)
- Spec, lint, tiers: [specification.md](specification.md)
- Domain policies (load only when needed): [policies.md](policies.md)

## Design decisions

1. **Prompt-only vs auto-execute** — Default: emit prompt and stop. Execute only with `--execute` or follow-up (`execute` / `implement` / «انجامش بده»).
2. **Ultra Lean** — Reuse → ultra/micro direct-render before any inspect; 4-section minimal; one-sentence decisions; silent prompt-only lint.
3. **File reuse cache** — SESSION-CACHE **Promptize reuse**: exact/normalized `norm_key` + matching HEAD. Rephrased text = miss (no semantic layer).
4. **Executable contracts** — MUST/artifact counts/precedence stay verifiable when they apply — compressed, not diluted.
5. **Evidence** — Auto-alias; map only if ≥2 files; else short path.
6. **Tiers** — `compact` default; auto-`minimal` for `ultra-low`/`low`; `--full` only when explicit.
7. **Smart lint** — Prompt-only: no WARN/ERROR dumps; surface only count-blocking CONFLICT/BLOCKED. `--execute`: ask only on BLOCKED.
8. **Testing** — Repo validation commands only; invent neither harness nor commands.
9. **Scope** — MUST = requested; OoS 3–4 hard excludes. Optional out unless asked.
10. **Risky ops** — Confirm destructive/migration/security even with `--execute`. Never ultra/micro for those or `--full`.
11. **Save** — Ultra-light metadata ([specification.md](specification.md)); upsert reuse row after render.
12. **Activation** — Still requires `/promptize` or explicit promptize ask — no ambient “help me with this code”.
13. **Skill frontmatter** — `disable-model-invocation: true`; versioned.
14. **Adaptive Caveman** — Reuse/direct gates run first; Caveman compresses only internal exploration, handoffs, and response prose when its overhead is justified, never immutable technical spans.
15. **Cavecrew & Artifact Boundary Integration** — Delta inspect delegates code localization to `cavecrew-investigator` to keep main context clean. Handoff prompts saved for subagents (`agent-prompts/`) automatically apply Caveman prose compression (`--compress` / `--caveman`), while human-facing reports preserve natural prose.

## Activation

| Form | Behavior |
|------|----------|
| `/promptize <short request>` | Build prompt only; **stop** |
| `/promptize --execute …` | Build, then implement (risk rules) |
| `/promptize --minimal …` | Force minimal (4 sections) |
| `/promptize --full …` | Force full 20-section template |
| `/promptize --compress` / `--caveman` | Force Caveman prose compression on rendered prompt body |
| `/promptize --save-to-file [path] …` | Build, output, save |
| `/promptize --save …` | Alias of `--save-to-file` |
| `/promptize --help` / `-h` | Display help message with usage, options, tiers, and token budgets |
| Natural language promptize / expand | Prompt-only |
| Follow-up execute / implement / «انجامش بده» | Revalidate, then implement |

Same normalized follow-up text → **reuse hit**. Rephrased text → miss. Flags may combine. `--full` + `--minimal` together → ask which.

## Flag parsing

| Flag | Meaning |
|------|---------|
| `--execute` | Implement after prompt |
| `--minimal` | Minimal tier |
| `--full` | Full tier |
| `--compress` / `--caveman` | Compress rendered prompt prose (preserves code, MUST, paths, AC) |
| `--save-to-file` / `--save` | optional path; else auto-name under `docs/promptize-prompts/` |
| `--help` / `-h` | Display usage, flags, tiers, and token budget policies |

### Save rules

1. Path-like token after flag → `{FILE_PATH}`; else `{slug}-{YYYYMMDD-HHMMSS}.md`.
2. Create parents; UTF-8 Markdown; **ultra-light** YAML only: `schema_version`, `skill_version`, `generated_at`, `tier`, `mode`.
3. Ask before overwrite unless user said overwrite.
4. Save ≠ execute. After save/render: upsert Promptize reuse ([../shared/context-cache.md](../shared/context-cache.md)).

## Workflow

`Parse → Understand → Reuse lookup → Ultra/Micro gate → [Delta inspect] → [Specify → Lint] → Render → Persist + cache upsert → [Revalidate → Implement → Validate → Diff Review → Verify AC → Report]`

1. **Parse** — flags + request; provisional tier.
2. **Understand** — outcome, scope, risks; set `estimated_tokens` (`ultra-low`/`low`/`mid`/`high`). Auto-`minimal` when `ultra-low`/`low` and no artifact inventory (unless `--full`).
3. **Reuse lookup** — SESSION-CACHE Promptize reuse: `norm_key` + HEAD ([inspection.md](inspection.md)). **Hit** → emit prior body (`Cache: REUSE_HIT`); skip to Persist upsert / Execute revalidation. **Miss** → continue.
4. **Ultra / Micro** — handoff deepen or micro fix/update → direct-render `minimal` (`Cache: ULTRA`); skip three-stage. Else continue.
5. **Inspect (delta)** — only if needed; policies only for security/DB/API/UI/async. For broad localization, apply the compact explorer contract in [../shared/caveman-token-policy.md](../shared/caveman-token-policy.md); skip delegation when a direct path or symbol is known.
6. **Extract → Specify → Lint** — skip on reuse/ultra/micro. Lean schema ([specification.md](specification.md)). Silent lint (prompt-only). Deduplicate internal context before rendering.
7. **Render** — density rules; header includes `Cache: …` when known. Apply Caveman prose compression only when it shortens output without changing exact code, commands, paths, errors, identifiers, numbers, negation, or safety language.
8. **Persist + cache upsert** — save if flagged; always upsert reuse row (cap 5).
9. **Execute tail** — only on `--execute` / follow-up.

---

# Engineering Contracts

### Evidence

| Status | Use |
|--------|-----|
| **Observed** | `[Observed: alias]` or short path |
| **Inferred** / **Assumption** / **Unknown** | Labeled; never upgrade to Observed |

### Uncertainty

Unknown may document. Conflict → do not silently pick. Blocked → `--execute` asks. Unknown ≠ Blocked.

### Priority

1. User requirements → 2. Repo evidence → 3. Inferences → 4. Assumptions (minimize).

### Obligation levels

`MUST` / `SHOULD` / `MAY` / `GUIDANCE` / `CONTEXT` / `ACCEPTANCE`. MUST exact and unique.

### Touch Set

Minimal paths. Dirty not auto-included. In minimal output: ≤3 lines.

### Clarification

Prompt-only: useful spec OK; BLOCKED counts → one-line blocker. Soft gaps omitted.  
`--execute`: resolve BLOCKED before coding. Do not ask what reuse/handoff/delta already established.

### Scope

OoS: **3–4** hard excludes (`❌` or `Do not:`).

### Self-contained

No “as discussed”. Aliases defined in-prompt when map used.

### Engineering Decisions

**One sentence** when possible (never more than two).

---

# Generated Prompt Format

```text
Promptize specification version: 3
Output tier: minimal | compact | full
Cache: REUSE_HIT | ULTRA | FAST | DELTA
```

| Tier | When |
|------|------|
| **minimal** | `--minimal`, or auto `ultra-low`/`low` without artifact inventory |
| **compact** | default |
| **full** | `--full` only |

Artifacts/inventories (any tier): tight Artifact line, Precedence if multi-source, Naming if needed, MUST once, Evidence map only if ≥2 files.

---

## Minimal format (4 sections)

1. **Objective** — one sentence  
2. **Context & decisions** — one-sentence decision; key paths; evidence map if ≥2 files  
3. **Behavior** — current → desired  
4. **Requirements** — MUST; artifact/naming if any; Touch Set ≤3 lines; OoS 3–4; AC ≤5; validation commands inline if known  

---

## Compact format (default — 8 sections)

Skip empties. Density: [specification.md](specification.md).

1. Objective  
2. Engineering Decisions (one sentence)  
3. Repository Context  
4. Current Behavior  
5. Desired Behavior  
6. Requirements (MUST + artifact)  
7. Constraints & Out of Scope  
8. Acceptance, Validation & Plan  

---

## Full format (`--full` — 20 sections)

Objective → Engineering Decisions → Assumptions → Repository Context (Stack, Architecture, Relevant Files, Source Precedence, Patterns, Tests & Validation, Project Instructions) → Current Behavior → Desired Behavior → Functional Requirements → Technical Requirements → Impact Analysis → Edge Cases & Error Handling → Security Considerations → Non-Functional Requirements → Constraints → Out of Scope → Testing & Validation Strategy → Acceptance Criteria → Definition of Done → Implementation Plan.

Unused: `N/A — Not applicable to this task.` Prefer aliases; AC agrees with artifact counts. Bad: “about N or equivalent.”

---

# Execution Rules

### Revalidation

Before coding, compare to generation baseline. Material: HEAD/branch change; Touch Set churn; behavior/manifest drift; handoff stale; inventory mismatch; **reuse body stale vs HEAD**. → update or regenerate via gate order. Safety → stop and ask.

On **reuse hit** + `--execute`: revalidate Touch Set/dirty paths; do not trust stale counts blindly.

### Path states

| State | Rule |
|-------|------|
| Dirty Touch Set | Scoped diff; protect user intent |
| Planned new | Allowed if task creates it |
| Unexpected | Protected — reassess |

### During implementation

Change budget: Touch Set only. Honor artifacts exactly. Protect unstaged/staged/untracked. Confirm destructive/security work. Resolve BLOCKED before coding.

### After

Diff review + validation + artifact checks. Upsert reuse row if prompt regenerated.

### Save sequencing

Save before implement when save flags set; resolve overwrite first.

---

# Token Budget System

Promptize must be token-aware. Goal: same engineering value, less context, less tool output, less repetition, fewer loops.

## Context budgets

| Budget | Scope | Heuristic |
|--------|-------|-----------|
| `CONTEXT_BUDGET` | Total session context | Keep under provider safe limit; prefer bottom third |
| `SKILL_BUDGET` | Skill file loading | Minimal/compact: load only referenced sections |
| `RETRIEVAL_BUDGET` | Files read per task | ≤5 targeted reads before justification |
| `READ_BUDGET` | Lines per file | <300 full; 300–1000 targeted; >1000 strongly targeted |
| `TOOL_OUTPUT_BUDGET` | Single tool result | ≤200 lines or ≤4KB |
| `OUTPUT_BUDGET` | Agent response | Compact: artifact + minimal explanation |
| `LOOP_BUDGET` | Inspect/retry cycles | ≤3 before escalation |

## Context budget policy

Priority order for loading context:

```text
requested files → relevant symbols → direct dependencies → tests → broader only if needed
```

Never load entire repository, documentation tree, or history without justification.

## Read budget

| File size | Strategy |
|-----------|----------|
| <300 lines | Full read acceptable |
| 300–1000 lines | Targeted read preferred |
| >1000 lines | Targeted strongly preferred |
| generated/vendor/log | Exclude by default unless task targets them |

## Tool output budget

Each tool must return high signal, low noise:

| Tool | Bound |
|------|-------|
| search/grep | Top N results, capped |
| git diff | Relevant files only |
| git log | --oneline -10, scoped |
| tests | First meaningful failure + stack |
| logs | tail/head, not full dump |

## Search budget

Scoped search preferred:

```bash
rg "foo" src/        # prefer
rg "foo" .           # only when justified
```

Default excludes: `node_modules`, `dist`, `build`, `coverage`, `.cache`, `.git`, `vendor`, `generated`, `logs`

Reuse repo ignore rules when present.

## Git budget

Bounded inspection:

```bash
git diff -- path/to/file           # prefer
git log -5 --oneline -- path       # prefer
git diff --stat                    # summary only
```

Never dump full repo history.

## Test output budget

Extract first failing test, relevant stack, relevant source. Never dump thousand-line output.

## Conversation context

Each stage must distinguish new information from already known. No re-injection of compacted data.

## Context compression

When context grows large:

```text
raw context → compact structured summary → continue
```

Summary includes only: Goal, Files, Findings, Constraints, Decisions, Open issues, Validation.

## Reuse cache

Cache hit must cause:

```text
reuse → skip unnecessary inspect → skip unnecessary retrieval → render directly
```

Cache hit must not re-load non-essential dependencies.

## Ultra / Micro gate

For simple requests:

```text
NO full repo inspection
NO broad retrieval
NO unnecessary tool calls
```

Sequence: Parse → Reuse lookup → Ultra/Micro gate → if sufficient: render → otherwise Delta inspect → specify.

## Delta inspection

When cache is incomplete/stale:

```text
known context + changed context only
```

Never full re-inspection. Example: HEAD changed → inspect changed relevant files only.

## Prompt tiers

| Tier | Trigger | Token target |
|------|---------|--------------|
| minimal | ultra-low/low, `--minimal` | ≤500 tokens |
| compact | default, mid | ≤1500 tokens |
| full | `--full` only, complex | ≤3000 tokens |

## Automatic downgrade

When context budget is tight:

```text
full → compact → minimal
```

Preserve executable contracts (MUST, AC, artifacts) even when downgrading.

## Never remove critical information

Compression must preserve: MUST, Acceptance Criteria, Touch Set, Out of Scope, Risk, Validation, Constraints, Required artifacts, Dependencies.

Compression reduces verbosity, not contracts.

## Duplicate instruction elimination

One concept → one canonical statement. No repetition across Rules, Validation, Notes, Summary.

## Smart lint additions

Lint must detect: duplicate instructions, unbounded file reads, unbounded searches, large tool outputs, unnecessary dependencies, repeated context, unbounded retries, missing scope, missing validation, missing risk handling.

Lint itself must not produce large output.

## Loop budget

| Budget | Default | On exceed |
|--------|---------|-----------|
| `MAX_INSPECT_LOOPS` | 3 | Stop, summarize, ask |
| `MAX_RETRY_LOOPS` | 2 | Stop, classify, escalate |
| `MAX_VALIDATION_LOOPS` | 3 | Stop, report failures |

Prompt-only mode: no loops.

## Retry policy

Same input + same tool must not repeat without change. On failure: classify → change strategy → retry only if justified.

## Output budget

Prompt-only: required artifact + minimal explanation.
Execution report: Changed, Validation, Failures, Remaining.

## Noise protection

Exclude by default: `node_modules/`, `dist/`, `build/`, `coverage/`, `.cache/`, `.git/`, `vendor/`, `tmp/`, `logs/`, `generated/`.

Allow inspection only when task directly targets them.

## Version

When `--version` or `-v` is detected as the only meaningful flag, emit the skill version (from the frontmatter) verbatim and stop. Do not inspect, reason, or generate.

