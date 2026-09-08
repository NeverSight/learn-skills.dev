---
name: architectural-refactor
description: >
  Execute architectural refactoring from an assessment document with deterministic, chunked operations
  and aggressive verification at every step. Use when you have an architectural assessment, clean
  architecture review, refactoring recommendations, or seam-ripper output and need to actually perform
  the refactoring safely. Also use when asked to "refactor based on this assessment", "execute these
  architectural recommendations", "fix architectural drift", "refactor in chunks", or any request to
  systematically restructure a codebase according to a plan. Designed specifically to prevent the
  kind of agent drift that causes architectural problems in the first place.
license: MIT
metadata:
  author: petekp
  version: "0.1.0"
---

# Architectural Refactor

Turn architectural recommendations into reality without breaking anything.

Coding agents are great at local changes but bad at maintaining architectural coherence across long sessions, context compactions, and multi-session work. This skill solves that by externalizing the plan to disk, tracking progress in a manifest, and enforcing verification gates between every chunk. The agent can lose context entirely and pick up exactly where it left off.

## Core Mechanism

The entire approach rests on three files that live on disk (not in context):

1. **`refactor-plan.md`** — The concrete, ordered plan derived from the assessment. Every chunk has explicit entry criteria, steps, and exit criteria.
2. **`refactor-manifest.json`** — Machine-readable progress tracker. What's done, what's next, what failed, verification results.
3. **`refactor-log.md`** — Append-only human-readable log of what happened and why, so any agent (or human) can understand the history.

These files are the source of truth. Not your memory. Not the conversation. The files.

## Phase 1: Ingest the Assessment

Read the assessment document(s) the user provides. These might be markdown files, seam-ripper output, simplicity audit results, or any structured analysis with recommendations.

Extract from the assessment:
- **What needs to change** — the specific problems identified
- **What the target architecture looks like** — the desired end state
- **Any ordering constraints** — dependencies between changes (e.g., "extract module X before you can decouple Y from Z")

If the assessment is vague or missing critical details, stop and ask. A refactoring plan built on ambiguous recommendations will drift — which is exactly what we're trying to prevent.

## Phase 2: Build the Plan

Convert the assessment into a concrete, ordered sequence of **chunks**. Each chunk is a self-contained unit of refactoring that moves the codebase from one valid state to another.

### How to decide chunk boundaries

A chunk should be:
- **Independently verifiable** — after completing it, you can run tests/types/lint and confirm nothing broke
- **Independently committable** — it makes sense as a single commit with a clear message
- **Small enough to hold in your head** — if a chunk requires understanding 15 files simultaneously, break it down further
- **Large enough to be meaningful** — moving a single import is not a chunk; extracting a module is

Good chunks typically look like:
- Extract a set of related functions/types into a new module
- Move a responsibility from module A to module B (and update all references)
- Replace an abstraction with a simpler alternative
- Invert a dependency direction
- Collapse multiple files/abstractions into one
- Remove dead code identified in the assessment

Bad chunks:
- "Refactor the auth system" (too vague — what specifically?)
- "Rename variable on line 42" (too granular — group related renames)
- "Restructure everything" (not independently verifiable)

### Dependency analysis

Before ordering chunks, map which chunks depend on which:
- Does chunk B move code into a module that chunk A creates? → A before B
- Does chunk C remove an abstraction that chunk D's changes assume is gone? → C before D
- Are chunks E and F independent? → Order doesn't matter (but pick one for consistency)

If you find circular dependencies between chunks, the chunk boundaries are wrong. Re-slice until the dependency graph is a DAG (directed acyclic graph — meaning no circular dependencies).

### Write the plan

Create `refactor-plan.md` in the project root (or wherever the user prefers):

```markdown
# Refactoring Plan

**Source:** [link/path to assessment document]
**Created:** [date]
**Target:** [one-sentence description of desired end state]

## Pre-flight Checks
- [ ] All tests pass before starting
- [ ] No uncommitted changes
- [ ] Working branch created

## Chunk 1: [Descriptive Name]
**Why:** [Which assessment finding this addresses]
**Entry criteria:** All tests pass, no prior chunks pending
**Steps:**
1. [Concrete action — e.g., "Create `src/auth/tokens.ts` with the TokenService class"]
2. [Next action — e.g., "Move `generateToken()` and `validateToken()` from `src/core/utils.ts`"]
3. [Continue — e.g., "Update imports in `src/api/middleware.ts` and `src/api/routes/login.ts`"]
4. [e.g., "Remove the now-empty token section from `src/core/utils.ts`"]
**Exit criteria:** All tests pass, types check, lint clean
**Commit message:** `refactor: extract token management into dedicated auth module`

## Chunk 2: [Descriptive Name]
**Depends on:** Chunk 1
**Why:** [...]
**Entry criteria:** Chunk 1 complete and verified
**Steps:**
1. [...]
**Exit criteria:** All tests pass, types check, lint clean
**Commit message:** `refactor: ...`

[...continue for all chunks...]

## Post-flight Checks
- [ ] Full test suite passes
- [ ] No TODO/FIXME markers left from refactoring
- [ ] Assessment findings are resolved
```

The steps within each chunk should be concrete enough that an agent with zero prior context could execute them mechanically. File paths, function names, specific moves — not "restructure as needed."

### Initialize the manifest

Create `refactor-manifest.json`:

```json
{
  "plan_file": "refactor-plan.md",
  "assessment_source": "[path to assessment]",
  "created": "[ISO date]",
  "total_chunks": 5,
  "current_chunk": 0,
  "status": "ready",
  "preflight_passed": false,
  "chunks": [
    {
      "id": 1,
      "name": "Extract token management",
      "status": "pending",
      "depends_on": [],
      "verification": null,
      "commit_sha": null,
      "started_at": null,
      "completed_at": null
    },
    {
      "id": 2,
      "name": "Decouple auth from core",
      "status": "pending",
      "depends_on": [1],
      "verification": null,
      "commit_sha": null,
      "started_at": null,
      "completed_at": null
    }
  ]
}
```

### Get user sign-off

Present the plan to the user before executing anything. They should confirm:
- The chunks make sense and cover the assessment's recommendations
- The ordering is correct
- Nothing critical is missing
- The chunk granularity feels right

If the user wants changes, update the plan and manifest before proceeding.

## Phase 3: Execute

This is the main loop. It's deliberately rigid because rigidity prevents drift.

### Starting a session (or resuming after compaction)

Every time you begin work — whether it's the first time or you're resuming after a context compaction or new session — do this:

1. **Read `refactor-manifest.json`** — find where you are
2. **Read `refactor-plan.md`** — understand the current chunk
3. **Read `refactor-log.md`** — understand what happened recently
4. **Verify the current state** — run the verification suite to confirm the codebase is in a good state

This takes 30 seconds and prevents the #1 cause of agent drift: starting work based on stale or assumed context.

### The chunk execution loop

```
FOR each chunk (in order):

  1. READ the chunk from refactor-plan.md
  2. CHECK entry criteria
     - Dependencies met? (check manifest)
     - Tests passing? (run them)
     - If not: STOP. Fix or escalate to user.

  3. UPDATE manifest: chunk status → "in_progress"
  4. LOG: "Starting chunk N: [name]"

  5. EXECUTE each step in the chunk sequentially
     - Follow the plan literally
     - If a step can't be done as written: STOP
       → Log what went wrong
       → Update manifest with the blocker
       → Ask the user how to proceed
       → Do NOT improvise a workaround

  6. VERIFY (the gate)
     - Run the full test suite
     - Run type checking
     - Run linter
     - If ANY verification fails:
       → Fix the issue (if it's clearly caused by this chunk's changes)
       → Re-verify
       → If you can't fix it in 2 attempts: STOP
         → Revert the chunk (git checkout/restore)
         → Log the failure
         → Update manifest: chunk status → "failed"
         → Ask the user

  7. COMMIT
     - Stage only the files changed in this chunk
     - Use the commit message from the plan
     - Record the commit SHA in the manifest

  8. UPDATE manifest: chunk status → "completed"
  9. LOG: "Completed chunk N. Verification: [pass/fail details]"

  10. Proceed to next chunk
```

### What "STOP" means

When the skill says STOP, it means: do not continue to the next chunk, do not try creative workarounds, do not "fix it and move on." The whole point of this skill is that deviating from the plan is how codebases get into the mess that required this refactoring in the first place.

When you stop:
1. Update the manifest with the current state
2. Write a clear log entry explaining what happened
3. Tell the user exactly what went wrong and what decision they need to make

The user might say "skip this chunk," "modify the plan," or "here's how to handle it." All fine. The decision is theirs, not the agent's.

### Handling drift signals

Watch for these signs that you're drifting from the plan:
- You're editing a file not mentioned in the current chunk's steps
- You're "also fixing" something you noticed that isn't in the plan
- You're reordering steps because "it makes more sense this way"
- You're skipping a step because "it's not needed anymore"

If any of these happen, STOP and re-read the plan. If the plan is genuinely wrong, update it (and the manifest) with the user's approval. Don't silently deviate.

## Phase 4: Post-flight

After all chunks are complete:

1. Run the full verification suite one final time
2. Review the refactor log for any anomalies
3. Compare the final state against the assessment's target architecture
4. Update the manifest: `status → "completed"`
5. Present a summary to the user:
   - Chunks completed successfully
   - Any chunks that were skipped or modified
   - Any remaining items from the assessment not addressed
   - Verification results

## Verification Suite

The verification commands depend on the project. Detect them on first run and record in the manifest so they're stable across sessions:

```json
{
  "verification": {
    "test": "npm test",
    "typecheck": "npx tsc --noEmit",
    "lint": "npm run lint",
    "detected_at": "[ISO date]"
  }
}
```

Detection order:
1. Check `package.json` scripts, `Makefile`, `Cargo.toml`, `pyproject.toml`, etc.
2. Check for common commands (`npm test`, `pytest`, `cargo test`, `go test ./...`)
3. If nothing is found, ask the user what commands verify the codebase

All three checks (test, typecheck, lint) must pass at every gate. If the project doesn't have one of them (e.g., no type checker for plain JS), note it in the manifest and skip that check — but never skip tests.

## Recovering from Failures

If a chunk fails and you need to retry:

1. `git stash` or `git checkout .` to revert uncommitted changes from the failed chunk
2. Update the manifest: chunk status → "pending" (reset from "failed")
3. Log the retry attempt
4. Re-read the chunk from the plan
5. Execute again from step 1 of the chunk

If the same chunk fails twice, do not retry again. Update the manifest, log the details, and escalate to the user. Two failures on the same chunk means the plan needs revision, not more attempts.

## Session Handoff

If you're ending a session before all chunks are done, or if you're creating a handoff for another agent/session:

1. Ensure the manifest is fully up to date
2. Add a log entry: "Session ended. Current state: chunk N of M complete. Next: chunk N+1."
3. Commit the manifest and log files

The next session starts by reading the manifest — all context needed to continue is on disk.

## What This Skill Does NOT Do

- **Decide what to refactor.** That's the assessment's job (use `/seam-ripper`, `/simplicity-audit`, or bring your own analysis).
- **Make architectural judgment calls.** If the plan is ambiguous, it stops and asks rather than guessing.
- **"Improve" things not in the plan.** Opportunistic cleanup is how drift starts. If you see something worth fixing, add it to the plan for a future chunk — don't do it now.
- **Skip verification.** Ever. For any reason. "The tests are slow" is not a reason. "It's obviously fine" is not a reason.
