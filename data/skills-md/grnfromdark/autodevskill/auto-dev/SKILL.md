---
name: auto-dev
description: >
  Generate complete automated TDD development pipelines from a todolist.md file. Creates a self-contained
  directory with autodev.sh, system_prompt.md, gate_check.sh, and task cards that drive Claude Code through
  spec-anchored, gate-guarded, card-by-card development — fully automated with no human in the loop.
  Features: TDD 5-step closure, 3-level AI decision protocol, independent acceptance verification,
  auto-repair on test failure, Bug Hunt phase for post-development P0/P1/P2 bug scanning and fixing.
  Use when user says "帮我生成 autodev", "create autodev for", "generate autodev pipeline", or needs
  to turn a todolist.md into an automated gated TDD development pipeline.
---

# Autodev Pipeline Generator

## Overview

This skill generates a complete **Autodev automated development pipeline** from a structured todolist.md file. The output is a self-contained directory that runs `autodev.sh` to drive Claude Code through a gated, TDD-enforced, card-by-card development workflow — fully automated, no human in the loop.

**Trigger phrases**: "帮我生成 xxx 的 autodev 文件", "create autodev for", "generate autodev pipeline"

## What is Autodev?

Autodev is a **spec-anchored, gate-guarded, TDD-enforced automated development methodology**. It:

1. Splits a task list into sequential **Task Cards** (one AI session per card)
2. Enforces **TDD 5-step closure** per card (RED → GREEN → SPEC → LINT → GATE)
3. Runs **automated gate checks** between phases
4. **Auto-repairs** test failures (up to 10 retries per card)
5. Tracks progress in a **state file** for resumable execution
6. **Independent acceptance verification** per card (separate AI verifies ACs)
7. **AI mutual review** for high-risk decisions (SPEC-DECISION / AI-REVIEW / AI-GATE 三级)
8. **Decision audit trail** (`decisions.jsonl`) for cross-card traceability
9. **Pipeline completion summary** — auto-generates structured report: what was implemented, files changed, decisions made, test results
10. **Bug Hunt phase** — multi-round bug scanning + fixing after development: independent auditor finds P0/P1/P2 bugs, developer AI fixes with regression tests, loops until clean (up to 15 rounds)

## Checklist

You MUST complete these steps in order:

1. **Read the todolist** — understand groups, tasks, phases, dependencies, test commands
2. **Gather project context** — identify spec doc, source files, test paths, key constraints
3. **Design the pipeline** — map todolist groups → phases → cards, define gate checks
4. **Generate all files** — autodev.sh, system_prompt.md, gate_check.sh, cards/*.md, phase_gate.md, state, decisions.jsonl
5. **Verify** — dry-run the script, confirm all card files exist, paths resolve correctly

## Step 1: Read the Todolist

Read the todolist.md file completely. Extract:

| Item | What to look for |
|------|-----------------|
| **Groups** | Top-level sections (Group 1, Group 2...) — these become Phases |
| **Tasks** | Individual numbered items within groups — these become Cards (or get merged into Cards) |
| **Dependencies** | Which tasks depend on others — determines Card ordering |
| **Execution phases** | If the todolist defines phases (Phase A, B, C...) — use them directly |
| **Test commands** | How to run tests — becomes the test verification step |
| **Key constraints** | Backward compatibility, safety rules, P1 fixes — become system_prompt constraints |
| **Source files** | Which files are being modified — becomes Card "read existing code" sections |
| **Spec/design docs** | Referenced design documents — becomes the "single source of truth" |

## Step 2: Gather Project Context

Resolve context autonomously (no human confirmation in runtime):

```
1. What is the spec/design document path?
   → This is the "single source of truth" referenced by all cards

2. What is the test command?
   → e.g., "python3 -m pytest tests/test_foo.py -q" or "npm test"

3. Are there any interactive/manual tests that must be excluded?
   → CRITICAL: Scan the test directories for tests that require interactive input
     (stdin prompts, private keys, manual confirmation, GUI interaction, network
     services that won't be available in CI). These MUST be excluded from the test
     command via --ignore or path filtering.
   → Common patterns to look for:
     - input(), getpass(), prompt(), readline() calls in test files
     - Tests under directories named: live/, manual/, interactive/, e2e/, integration/
     - Tests that connect to external wallets, require API keys at runtime, or need
       running services
   → Add --ignore flags for each such directory/file. The generated test command must
     be fully non-interactive and able to run unattended.

4. What are the core source files being modified?
   → Listed in system_prompt as "project files"

5. What are the project-specific constraints?
   → e.g., "backward compatible", "no breaking changes", "量纲一致性"

6. Where should the Autodev directory live?
   → Convention: Autodev/{project_name}/

7. If anything is unclear, how should ambiguity be resolved?
   → Infer from repo evidence (todolist, spec, tests, git history, existing patterns),
     choose the most conservative backward-compatible option, and record assumptions in
     system_prompt.md ("Assumptions & Defaults"). Do NOT block for user confirmation.
```

## Step 3: Design the Pipeline

### Mapping Groups to Phases

Each **Group** in the todolist becomes a **Phase**. Each Phase ends with a **GATE**.

```
Group 1 → Phase A → GATE:A
Group 2 → Phase B → GATE:B
...
Last Group → Phase N → GATE:FINAL
```

### Mapping Tasks to Cards

**Merge small related tasks** into single Cards. **Keep complex tasks** as their own Card. Target: **2-5 tasks per Card**, **3-7 Cards per Phase**.

Heuristics for merging:
- Same source file → merge
- Sequential dependency with no external dependency → merge
- Total estimated complexity < 1 Claude session → merge

Heuristics for splitting:
- Different source files → separate
- Independent testable unit → separate
- High complexity (e.g., "MC simulation core") → own Card

### Card ID scheme

Use `{Phase}.{Sequence}` format:
- Alphanumeric phases: A.1, A.2, B.1, C.1
- Numeric phases: 0.1, 0.2, 1.1, 2.1

### Adding verification Cards

Add a **verification Card** at the end of each Phase (before the GATE) that:
- Runs all tests for that phase
- Checks test coverage against the todolist
- Runs full regression

### Gate checks

Design gate_check.sh with:
- **Universal checks** (always include):
  - Unit tests pass
  - Full regression tests pass
  - SPEC-DECISION audit (grep for AI decisions)
- **Project-specific checks** (customize):
  - Backward compatibility verification
  - Contract/interface checks
  - Config consistency
  - Import validation

## Step 4: Generate All Files

### Directory Structure

```
Autodev/{project_name}/
├── autodev.sh              # Main pipeline script
├── system_prompt.md        # AI session prompt
├── gate_check.sh           # Automated gate checks
├── state                   # Progress tracker (empty file)
├── decisions.jsonl         # Decision audit trail (empty file, runtime populated)
├── logs/                   # Runtime logs (empty dir)
├── bug_reports/            # Bug Hunt reports per round (runtime populated)
└── cards/
    ├── {A.1}.md            # Task cards
    ├── {A.2}.md
    ├── ...
    └── phase_gate.md       # Phase gate audit template
```

`summary.md` is a runtime artifact. Do NOT pre-create it during scaffolding.

### File Templates

Generate each file using the corresponding template reference. Read the template, customize all `{PLACEHOLDER}` values for the project, and write the complete file.

| File | Template Reference | Description |
|------|--------------------|-------------|
| `autodev.sh` | [references/autodev-template.md](references/autodev-template.md) | Main pipeline script with card execution, testing, AC verification, Bug Hunt |
| `system_prompt.md` | [references/system-prompt-template.md](references/system-prompt-template.md) | AI session prompt with TDD flow, decision protocol, safety rules |
| `cards/{ID}.md` | [references/card-template.md](references/card-template.md) | Task card with context, tasks, acceptance criteria |
| `gate_check.sh` | [references/gate-check-template.md](references/gate-check-template.md) | Automated gate checks (tests, audit, coverage) |
| `cards/phase_gate.md` | [references/phase-gate-template.md](references/phase-gate-template.md) | Phase gate audit template for AI auditor |

**IMPORTANT**: Do NOT use templates literally. Generate FULL files with all `{PLACEHOLDER}` values replaced for the specific project. The autodev.sh template shows the *structure* -- the actual output must be a complete, runnable bash script with all functions expanded.

## Step 5: Verify

After generating all files:

1. `chmod +x autodev.sh gate_check.sh`
2. Run `./autodev.sh --dry-run` — verify all steps listed correctly
3. Run `./autodev.sh --status` — verify display works
4. Run `./autodev.sh --help` — verify help text
5. Verify all card files exist: `ls cards/`
6. Verify state file is empty: `cat state`
7. Verify decisions.jsonl exists and is empty: `test -f decisions.jsonl && [ ! -s decisions.jsonl ]`
8. Verify summary.md does NOT exist yet (it's auto-generated at runtime)
9. Verify generated files contain no unresolved placeholders/stubs:
   - `! rg -n '\{(PROJECT|SPEC|TODOLIST|TEST_CMD|ALL_STEPS_CONTENT|FIRST_CARD_ID|SOURCE_DIRS|AUTODEV_PATH|AUTODEV_DIR|ENV_PREFIX|ADDITIONAL_FILES|RELEVANT|EXISTING_FILES|ACCEPTANCE_CRITERION|CARD_TITLE|CARD_ID|REVIEWER_ROLE|TASKS_WITH)[^}]*\}' autodev.sh gate_check.sh system_prompt.md cards/*.md`
   - `! rg -n 'show_help\(\) \{ \.\.\. \}|show_status\(\) \{ \.\.\. \}' autodev.sh`

## Key Principles

1. **Todolist is the source of truth** — every Card traces back to todolist tasks
2. **P1/P2 fixes become constraints** — embed audit corrections into Card acceptance criteria
3. **Test command is sacred** — must match what the todolist specifies
4. **Test command must be non-interactive** — the generated test command must run fully unattended with no stdin prompts. Scan the test directory for interactive tests (input(), getpass(), wallet prompts, manual e2e) and add --ignore flags to exclude them. A test command that hangs waiting for input will block the entire pipeline.
5. **Backward compatibility** — if todolist mentions fallback/compatibility, enforce in gate checks
6. **No gold-plating** — Cards only implement what the todolist describes
7. **Each Card is self-contained** — reads its own context, doesn't assume prior Card output was read

## Generator Self-Check

After generating all files, verify these cross-cutting concerns:

1. **system_prompt.md** contains the full 3-level decision protocol (copy from template verbatim)
2. **Reviewer role table** is customized for the project (add/remove roles as needed; severity levels BLOCK/WARN/SUGGEST are universal — never modify)
3. **gate_check.sh** includes decisions.jsonl audit checks
4. **phase_gate.md** includes decision audit as step 5
5. **All fix prompts** include: test output verbatim, spec/todolist references, "no extra changes", backward compatibility reminder
6. **`decisions.jsonl` path** flows correctly: config var → `build_prompt()` injects `DECISIONS_FILE:` → Card AI reads it from prompt
