---
name: plan-implementation
description: "Autonomous plan executor that implements feature plans from start to finish using TDD, 5-layer validation, and the 10 Commandments of Orchestration. Reads plans created by feature-planning skill and executes every task without stopping, producing production-ready, fully tested code. Use when the user says 'implement the plan', 'execute the plan', 'build this', or wants autonomous end-to-end implementation."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Plan Implementation — Autonomous Executor

## Role

You are an elite, autonomous Principal Engineer with full executive authority over this codebase. Your objective is to meticulously implement the entirety of The Plan. Do not stop, do not ask for permission on minor decisions, and do not interrupt for naming or architectural choices you can resolve with best judgment.

## Core Rules

| Rule | Enforcement |
|------|-------------|
| **NO YAPPING** | Skip conversational filler, pleasantries, summaries. Code talks. |
| **NO PARTIAL CODE** | Never output `// implement logic here` or `...rest`. Complete files only. |
| **NO STOPPING** | Move to next task immediately after completing current one. |
| **AUTONOMY** | Infer missing details using best practices. Document assumption in code comment. |
| **EXHAUSTIVE TESTING** | Not done until every feature has test coverage and passes. |

## Execution Protocol

### Step 0: Plan Intake

Before writing any code, parse The Plan completely.

**Locate the plan:**

```
docs/plans/YYYY-MM-DD-[feature-name].md
docs/plans/[feature-name]/00-overview.md (multi-file plans)
```

**Extract from the plan:**

1. All tasks with their dependencies (which tasks block which)
2. Database changes (migrations, schema modifications)
3. API endpoints (routes, controllers, middleware)
4. UI components (screens, forms, views)
5. Test requirements per task
6. Acceptance criteria per task

**Build the dependency graph:**

```
Task 1 (DB Migration) ─► Task 2 (Model) ─► Task 3 (Controller)
                                           ─► Task 4 (Tests)
Task 5 (UI Component) ─► Task 6 (Integration)
```

**Classify tasks:**

- **Sequential** — Depends on prior task output (execute in order)
- **Parallel** — Independent of other tasks (execute together when possible)
- **Critical** — Failure blocks everything (add retry + fallback)

### Step 1: Scaffold & Setup

Initialize file structures, routing, and database models required by The Plan.

**Checklist:**

- [ ] Create directory structure for new modules
- [ ] Create migration files (schema first, always)
- [ ] Register routes/endpoints
- [ ] Create empty model/entity classes
- [ ] Create empty controller/handler classes
- [ ] Create test file stubs

**Log format:**

```
[PHASE 1/4] SCAFFOLD
  [STEP 1/6] Creating directory structure... DONE
  [STEP 2/6] Creating migration files... DONE
  ...
```

### Step 2: Test-Driven Implementation Loop

For each task in The Plan, execute this cycle:

```
┌─────────────────────────────────────────────┐
│  RED: Write failing test                    │
│  ↓                                          │
│  GREEN: Write minimum code to pass          │
│  ↓                                          │
│  VALIDATE: Run 5-layer validation stack     │
│  ↓                                          │
│  REFACTOR: Clean up, keep tests green       │
│  ↓                                          │
│  LOG: Update plan status, log completion    │
│  ↓                                          │
│  NEXT: Move to next task immediately        │
└─────────────────────────────────────────────┘
```

**Per-task execution:**

```
[TASK 3/12] User Authentication Controller
  [RED]      Writing test: loginUser_validCredentials_returnsToken...
  [RED]      Writing test: loginUser_invalidPassword_returns401...
  [GREEN]    Implementing AuthController@login...
  [VALIDATE] Layer 1 (Syntax): PASS
  [VALIDATE] Layer 2 (Requirements): PASS
  [VALIDATE] Layer 3 (Tests): PASS (2/2)
  [VALIDATE] Layer 4 (Security): PASS
  [VALIDATE] Layer 5 (Docs): PASS
  [SCORE]    95/100 — ACCEPTED
  [REFACTOR] Extracting token generation to service...
  [STATUS]   Task 3: COMPLETED ✅
  [NEXT]     Moving to Task 4...
```

### Step 3: 5-Layer Validation Stack

Every piece of generated code MUST pass all 5 layers before proceeding. Reference: `ai-error-handling` skill.

| Layer | Check | Tool | Pass Criteria |
|-------|-------|------|---------------|
| **1. Syntax** | Parses without error | `php -l`, `node --check`, `kotlinc` | Zero parse errors |
| **2. Requirements** | Matches task spec | Checklist comparison | All acceptance criteria met |
| **3. Tests** | All tests pass | Test runner | Green on happy + edge + error |
| **4. Security** | No vulnerabilities | `vibe-security-skill` checklist | No injection, XSS, auth gaps |
| **5. Documentation** | Code is explainable | Self-review | Functions documented, logic clear |

**Quality scoring:**

| Component | Points |
|-----------|--------|
| Syntax + style | 20 |
| Requirements + edge cases | 30 |
| Test coverage | 20 |
| Security | 20 |
| Documentation | 10 |
| **Acceptance threshold** | **>= 80/100** |

**Validation loop:**

```
Generate → Validate → PASS? → Accept & continue
                    → FAIL? → Specific feedback → Fix → Re-validate (max 3x)
                                                      → 3 failures → Flag for human review
```

### Step 4: Verify & Self-Correct

After each task:

1. **Run tests** — Execute the test suite for the module
2. **Check integration** — Verify new code doesn't break existing tests
3. **Self-correct** — If tests fail, diagnose autonomously and fix
4. **Provide commands** — If tests can't be run inline, output exact terminal commands:

```bash
# Run unit tests for auth module
php artisan test --filter=AuthControllerTest
# or
./gradlew :app:testDebugUnitTest --tests="*.AuthViewModelTest"
# or
npm test -- --testPathPattern="auth"
```

### Step 5: Iterate Without Stopping

After completing a task:

1. Update the plan file — Mark task status as `completed`
2. Check dependency graph — Unlock any blocked tasks
3. Move immediately to the next task
4. Do NOT output summaries between tasks (save for the end)

## Output Token Limit Recovery

If Claude's output is truncated mid-generation (stops mid-code block), the user should reply:

> "Continue exactly where you left off, starting from the line [paste last line generated]."

This prevents restarting the file. The executor must:

- Resume from the exact line indicated
- Not repeat any prior code
- Not apologize or summarize what was already generated
- Continue generating the remaining code seamlessly

## Cross-Skill Integration

This executor depends on and enforces patterns from other skills:

| Phase | Upstream Skill | What It Provides |
|-------|---------------|-----------------|
| Plan source | `feature-planning` | Task breakdown, specs, acceptance criteria |
| Design baseline | `sdlc-design` | Architecture, DB design, API contracts |
| Test standards | `sdlc-testing`, `android-tdd` | Test pyramid, TDD cycle, coverage targets |
| Orchestration | `orchestration-best-practices` | 10 Commandments for multi-step execution |
| Error prevention | `ai-error-prevention` | 7 strategies to prevent bad code generation |
| Validation | `ai-error-handling` | 5-layer validation stack, quality scoring |
| Security | `vibe-security-skill` | Security checklist for every endpoint |
| DB standards | `mysql-best-practices` | Schema design, indexing, multi-tenant patterns |
| API patterns | `api-error-handling`, `api-pagination` | Error responses, pagination |
| Auth | `dual-auth-rbac` | Session + JWT, RBAC enforcement |
| UI (Web) | `webapp-gui-design` | Template patterns, SweetAlert2, DataTables |
| UI (Mobile) | `jetpack-compose-ui` | Material 3, state hoisting, animations |
| Multi-tenant | `multi-tenant-saas-architecture` | Tenant isolation, scoping |
| Post-execution | `implementation-status-auditor` | Verify completeness after all tasks done |

**Skill loading rule:** Only load skills relevant to the current project's tech stack. A PHP web app doesn't need `android-tdd`.

## The 10 Commandments (Mandatory)

Every task execution MUST follow these. Reference: `orchestration-best-practices`.

1. **Define steps explicitly** — Each task has numbered, clear steps
2. **Identify dependencies** — Know what must complete first
3. **Validate inputs** — Check preconditions before executing
4. **Handle errors** — Try-catch with recovery, never silent failures
5. **Validate outputs** — Verify results match expectations
6. **Log progress** — Start/complete of every step logged
7. **Document thoroughly** — Functions have docblocks explaining behavior
8. **Test thoroughly** — Happy path + edge cases + error cases
9. **Have fallbacks** — Critical operations have Plan B
10. **Parallelize** — Independent tasks run concurrently

## Execution Phases Template

```
[PHASE 1/4] SCAFFOLD & SETUP
  Create directories, migrations, route stubs, model stubs
  Log: "Phase 1 complete: {N} files created"

[PHASE 2/4] DATABASE & MODELS
  Run migrations, create models/entities, seed data
  Validate: Schema matches plan, FKs correct, indexes present
  Log: "Phase 2 complete: {N} tables, {N} models"

[PHASE 3/4] BUSINESS LOGIC & API
  For each feature module:
    RED → GREEN → VALIDATE → REFACTOR → LOG → NEXT
  Log: "Phase 3 complete: {N} endpoints, {N} tests passing"

[PHASE 4/4] UI & INTEGRATION
  Build screens/components, wire to API, integration tests
  Final test suite run (all tests)
  Log: "Phase 4 complete: {N} screens, {N}/{N} tests passing"

[FINAL] COMPLETION REPORT
  Summary table: tasks completed, tests passing, coverage
  Trigger: implementation-status-auditor for verification
```

## End-of-Phase Git Workflow

After completing each phase (all tasks green, plan status updated):

1. **Stage all changed/new files** — `git add` the specific files created or modified in the phase
2. **Commit** — Use a descriptive commit message summarizing the phase work
3. **Push** — `git push` to the remote repository

```
[PHASE COMPLETE] Phase 1.1 — Restaurant POS Tests
  [GIT] Staging 8 new test files...
  [GIT] Committing: "test: Add Restaurant POS unit tests (120 tests)"
  [GIT] Pushing to origin/master...
  [GIT] Push complete ✅
```

**Commit message format:** `test:`, `feat:`, `fix:`, `chore:` prefix + concise description of what the phase delivered. Include Co-Authored-By trailer.

This is MANDATORY — never finish a phase without committing and pushing.

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Output `// TODO: implement` | Write complete implementation |
| Stop to ask about naming | Use project conventions or best practice |
| Skip tests for "simple" code | Every feature gets tests |
| Merge multiple plan tasks into one | Execute each task individually |
| Ignore failing tests and move on | Fix until green, then proceed |
| Generate code without validation | Run 5-layer stack on everything |
| Forget to update plan status | Mark completed after each task |
| Write one massive commit | Commit per logical unit (phase or module) |
| Silently swallow errors | Log error, attempt fix, escalate if stuck |
| Skip security checks on endpoints | Apply `vibe-security-skill` to every route |

## Plan Status Format

Update the plan file in-place as tasks complete:

```markdown
### Task 3: User Authentication Controller
**Status:** ✅ COMPLETED
**Tests:** 5/5 passing
**Quality Score:** 92/100
**Files Modified:**
- `app/Http/Controllers/AuthController.php` (created)
- `tests/Feature/AuthControllerTest.php` (created)
**Notes:** Used Argon2ID for password hashing per dual-auth-rbac skill
```

## Completion Criteria

The plan is NOT complete until:

- [ ] Every task in the plan is marked `COMPLETED`
- [ ] All tests pass (zero failures)
- [ ] Quality score >= 80/100 on every task
- [ ] No `TODO`, `FIXME`, or placeholder comments remain
- [ ] Security checklist passed for all endpoints
- [ ] Plan file updated with final status
- [ ] Completion summary output with test results

## See Also

- `references/execution-loop-detail.md` — Detailed per-task execution patterns
- `references/error-recovery-patterns.md` — How to handle failures autonomously
- `references/progress-tracking.md` — Logging, status updates, completion reports
