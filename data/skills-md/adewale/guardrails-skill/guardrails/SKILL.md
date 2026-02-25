---
name: guardrails
description: >
  Code quality verification gates wired into the agent lifecycle. Use this skill
  whenever writing, modifying, reviewing, or debugging code — including new features,
  bug fixes, refactors, troubleshooting, CI/CD setup, or project bootstrapping. Also
  use when the user mentions "quality", "testing strategy", "CI pipeline", "guardrails",
  "debugging", or asks how to improve code reliability. If you're writing code or
  trying to understand why code isn't working, this skill applies.
hooks:
  SessionStart:
    - matcher: "startup"
      hooks:
        - type: agent
          prompt: "Run guardrails SessionStart discovery: git baseline, config/CI/test directory inspection, project type identification, fast-check and full-suite command discovery, test convention learning, LESSONS_LEARNED.md, script/agent-tools/. Defer to existing conventions. Report findings."
          timeout: 120
          once: true
          statusMessage: "Guardrails: discovering project..."
  Stop:
    - hooks:
        - type: prompt
          prompt: "Guardrails stop check. Verify: (1) fast check ran this turn, (2) production code changes have test changes, (3) circuit breaker respected — no 3rd direct retry without diagnostic tool. Block if violated. $ARGUMENTS"
          statusMessage: "Guardrails: stop check..."
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: prompt
          prompt: "If git commit: verify full suite passed, secrets scanned, commit message conventional, new code reachable. Else allow. $ARGUMENTS"
          statusMessage: "Guardrails: commit gate..."
    - matcher: "Edit|Write"
      hooks:
        - type: prompt
          prompt: "Config protection: block edits to test scripts, lint/format/type config, CI definitions, pre-commit config, coverage thresholds. Agent must propose config changes to user. $ARGUMENTS"
          statusMessage: "Guardrails: config protection..."
---

# Guardrails

Verification gates that block the agent from proceeding until checks pass. The agent
already knows what linting, testing, type checking, and security scanning are. This
skill doesn't re-teach those concepts. Instead, it specifies:

- **When** each check runs in the agent lifecycle (hooks that block progress)
- **What to do when stuck** (diagnostic escalation instead of retrying)
- **What not to touch** (config protection, high-risk action gating)
- **How to accumulate knowledge** (lessons learned, agent tool library)

These are the behaviors a coding agent wouldn't exhibit without being told. Everything
else — which linter to use, how to structure a unit test — the agent already knows from
training and discovers from the project's existing config.

**Bundled resources:** `references/tool-building.md` contains the diagnostic tool and
notation catalogs with worked examples. `references/language-defaults.md` is a lookup
table for tool selection by ecosystem. Read these when directed, not proactively.

---

## Scope

Not every check applies to every project. The common base applies everywhere: lint,
format, types, SAST, dependency audit, secrets scan, dead code detection, duplicate
code detection, coverage, unit tests. Beyond that,
add layers by project type:

- **Backend / API:** integration tests. Usually: property-based, contract, performance.
- **Frontend:** integration tests. Usually: screenshot, E2E, accessibility.
- **Full-stack:** integration tests. Usually: screenshot, E2E, contract, accessibility.
- **Library / SDK:** Usually: property-based, mutation.
- **Data pipeline:** integration tests. Usually: property-based, performance.
- **Infrastructure / IaC:** integration tests (plan/apply validation).

Scale up as the project matures. A prototype needs the common base. A production system
serving users needs the full suite.

> **Common base:** lint, format, types, SAST, dependency audit, secrets scan, dead code
> detection, duplicate code detection, coverage, unit tests. Dead code and duplicate
> code tools by ecosystem are listed in `references/language-defaults.md`.

---

## Lifecycle Hooks

Everything above is just guidance — the agent might follow it, might not. The hooks
below are what make guardrails real. They block the agent from proceeding until checks
pass. The distinction matters: a lint rule that runs in 20ms and fails the build gives
the agent concrete, unambiguous feedback. A prose instruction in a skill file sits in
the context window competing for attention with everything else.

### Test Runner Discovery

The enforcement system needs two commands in the target project — one fast, one full:

**Fast check** — Runs in seconds. Fires on every agent stop. Covers: format check,
lint, type check, unit tests.

**Full suite** — Runs before every commit. Covers: everything in the fast check plus
integration tests, property tests, secrets scan, dead code detection, duplicate code
detection, coverage floor.

**Discover, don't impose.** Every ecosystem has its own convention: npm scripts
(`npm test`, `npm run test:unit`), Makefile targets (`make test`, `make check`), Go
commands (`go test ./...`), pytest (`pytest tests/unit`), bun scripts, Cargo, etc.
During SessionStart, find what the project already uses by inspecting package.json
scripts, Makefile targets, CI workflow steps, and README instructions. Adapt to the
project's existing runner — don't create a new one alongside it.

If no test runner exists at all, create one using the project's native tooling. Consult
`references/language-defaults.md` for tool selection. The runner must exit non-zero on
failure.

### SessionStart

Fires when the agent boots up. Discovery and baseline before touching anything.

- Record git state (HEAD SHA, working tree status) as a session baseline.
- Discover existing guardrails: inspect config files, CI pipelines, test directories.
  Identify the project type (Scope section) and determine which checks apply.
- Read existing test files to learn conventions — naming, structure, assertion style,
  mocking, fixtures. Match them.
- Read `LESSONS_LEARNED.md` if it exists. Apply project-specific lessons.
- Check for `script/agent-tools/`. Read the directory and description comments to know
  what diagnostic tools are available from previous sessions.

**Defer to existing conventions.** When the project has tooling or patterns in place,
follow them — even when they conflict with this skill. Do not switch tools or frameworks
without explicit user approval.

### Stop

Fires every time the agent returns control. Prevents declaring success without
verification.

- Run the fast check. Block if it fails.
- If production code changed, verify tests also changed. Untested code is unverified
  code, regardless of whether it "looks right."

**Thrashing circuit breaker.** If the fast check fails and the agent has already
attempted the same fix twice, it cannot try a third direct fix:

1. **After attempt 1 fails:** Try a direct fix. Normal.
2. **After attempt 2 fails:** Stop. Build a diagnostic tool or switch to a notation
   (read `references/tool-building.md`). Two failed attempts means the agent's model
   of the problem is wrong — re-reading the same code produces the same wrong model.
   New information or a different representation breaks the loop.
3. **After attempt 3 fails (with diagnostic):** Stop entirely. Report to the user:
   what's failing, what was tried, what the diagnostic revealed, why it isn't converging.

The breaker resets when the user provides new direction. Persist useful diagnostics
to `script/agent-tools/`.

**Completion check.** After the fast check passes, check your task list. If planned
work items remain and you are not blocked, continue to the next slice — do not hand
off. Hand off only when: all items are done, the circuit breaker fired, or context
is running low (in which case, commit completed slices and report remaining items).

**Work in slices, but finish the job.** Verify frequently — a good slice is 1-3
production files plus tests. An agent that writes 15 files then discovers a type
error in file 3 has wasted 4-15. But verifying a slice is not completing the task.
Do not hand off to the user until all planned work items are done or you are
explicitly blocked.

### Commit (PreToolUse + git hooks)

Fires on any `git commit`, whether from the agent or a human. Same enforcement for both.

- Run the full suite. Block if it fails.
- Secrets scan on staged files.
- Verify commit message follows project conventions.
- **Integration/deployment check:** Verify the change is reachable, not just correct.
  Code that passes tests but isn't wired into the application is a deployment gap.
  Confirm: new modules imported? Routes registered? Migrations included? Entry points
  updated? If nothing invokes the new code, that's a failure even with passing tests.

---

## Tool Building and Notation

When direct fixes fail, the agent needs new information or a different problem
representation. **Read `references/tool-building.md`** for the full catalog of
diagnostic tools, notations, and three worked examples.

The circuit breaker (Stop hook) mandates reading this reference after 2 failed attempts.
But the best use is *proactive*: recognize the problem shape during planning and build
scaffolding before writing code. Common patterns:

- Modifying a function's interface → build a call site inventory first
- Complex conditional logic (>3 booleans or >4 branches) → build a decision matrix
- State machine behavior → build a state transition table
- Data transformation pipeline → trace sample values through each stage
- Unfamiliar codebase area → build a codebase index before editing

Diagnostic tools often graduate into permanent infrastructure — reproduction scripts
become test cases, schema checkers become health checks, dependency mappers feed the
integration check. Building a diagnostic tool is not a detour; it's often the most
direct path to completing the task.

---

## Config Protection

The agent does not edit its own guardrail configuration. An agent under pressure to make
tests pass has an incentive to weaken the tests rather than fix the code. Block the agent
from modifying: test scripts, lint/format/type config, CI definitions, pre-commit config,
and coverage thresholds. If config needs changing, propose it to the user.

---

## High-Risk Action Gating

Some operations have blast radius beyond the current code change. Even if the user's
request implies them, the agent stops and asks because these are irreversible or affect
systems beyond the codebase:

- Destructive data operations (DROP TABLE, deleting records, truncating logs)
- Permission and access changes (auth rules, IAM policies, CORS)
- Deployment actions (pushing to production, triggering deploys, scaling)
- Bulk or irreversible operations (mass updates, migrations, force-pushes)
- Financial or billing changes (anything committing to spend)

Describe the operation and blast radius, then wait for confirmation.

---

## Lessons Learned

The agent accumulates project-specific knowledge across sessions. Without a persistent
record, each session starts from zero and risks repeating the same mistakes.

Maintain `LESSONS_LEARNED.md` in the project root. Append an entry when encountering:
a guardrail failure requiring multiple attempts, a non-obvious project convention, a
surprising tool behavior, a deployment gap tests didn't catch, a thrashing episode, or
a diagnostic tool that proved useful. Each entry: **Date**, **Context**, **What
happened**, **Resolution**, **Rule** (concise directive for future sessions).

Commit to version control. If a lesson reveals a missing guardrail, propose adding
one — don't just document the workaround.

---

## Agent Responsibilities (Not Hookable)

Behaviors the agent follows because the reasoning is sound, not because a hook enforces
them.

**Planning:** Define completion criteria — what "done" looks like for this task (files
changed, tests added, routes wired, etc.). Decide testing layers before writing code.
Check problem shape against the proactive table in `references/tool-building.md`.
Assess security relevance.

**Code writing:** Format and type-check incrementally. If the same type error reappears
after one fix, that signals a structural misunderstanding — switch to a notation rather
than continuing to guess.

**Handoff / PR:** Report what was verified, which layers were skipped and why, security
findings, and coverage delta. Do not present work as complete if any hook failed.
