---
name: execute
description: Use when implementing a feature plan file, choosing between sequential and team-based parallel execution with mandatory validation gates
---

# Execute: Implement from Plan

## Plan to Execute

Read plan file and execute all tasks according to the plan's specifications.

## ⚠️ CRITICAL: Mandatory Validation Requirements

**This skill enforces BLOCKING validation gates.**

Execution is NOT complete until:
- ✅ All implementation tasks finished
- ✅ All tests created and passing
- ✅ All validation commands executed and passed
- ✅ All verification gates passed

**You CANNOT claim execution complete or generate the final Output Report until ALL validation requirements pass.**

Validation steps use MANDATORY, BLOCKING, and CRITICAL language to indicate enforcement. These are not optional or advisory - they are hard requirements that gate completion.

---

## Step 0: Acceptance Criteria Gate

**MANDATORY — runs before anything else, including execution mode selection.**

This gate ensures every execution run has explicit, user-confirmed acceptance criteria before a single line of code is written.

### 0.1. Locate Acceptance Criteria

Work through the following sources in order, stopping as soon as criteria are found.

**Source 1 — Plan file** (when executing a pre-made plan):
- Read the plan file
- Search for any of these headings (case-insensitive): `## ACCEPTANCE CRITERIA`, `## Acceptance Criteria`, `## Success Criteria`, `## Completion Criteria`, `## Done When`
- Also scan `## COMPLETION CHECKLIST` — individual checklist items there may serve as criteria
- If found → **criteria located, skip to Step 0.3**

**Source 2 — `acceptance_criteria.md`** (supplementary):
- Check `.agents/acceptance_criteria.md` and `acceptance_criteria.md` in the project root
- Look for a section that matches the current feature by name or date
- If found → **criteria located, skip to Step 0.3**

**Source 3 — The request itself**:
- Re-read the user message or the context passed to this skill
- Look for explicit success conditions: numbered/bulleted requirements, "done when", "I expect", "it should", "must", acceptance/success criteria stated inline
- If found → **criteria located, skip to Step 0.3**

**If all three sources yield nothing → proceed to Step 0.2.**

---

### 0.2. No Criteria Found — Stop and Resolve

**STOP. Do NOT proceed to execution mode selection.**

#### Option A: Delegate to `acceptance-criteria-define` skill (preferred)

If the `acceptance-criteria-define` skill is available in this system, invoke it now via the Skill tool:

```
skill: "acceptance-criteria-define"
context: "<plan file path, or a summary of the execution request if no plan file>"
```

Pass the plan file path (if one exists) or a concise description of what is being implemented as context. The skill will derive suggested criteria, confirm them with the user, and write them to the plan file or `acceptance_criteria.md`.

**After the skill completes:** the criteria are now written. Proceed to Step 0.4 (skip Step 0.3 — the skill has already handled writing).

---

#### Option B: Inline fallback (only if `acceptance-criteria-define` is not available)

Output this message verbatim (filling in the bracketed parts):

```
⚠️ No acceptance criteria found

I could not find acceptance criteria for this execution request in:
- The plan file (if provided): [plan file path or "N/A"]
- acceptance_criteria.md
- The request itself

Before I start implementing, we need to agree on what "done" looks like.

Here are my suggested acceptance criteria based on my understanding of the request/plan:

## Suggested Acceptance Criteria

### Functional
- [ ] <criterion>
- [ ] <criterion>

### Error Handling
- [ ] <criterion>

### Validation
- [ ] <criterion> — verified by: `<command>`

### Out of Scope
- <item> — not required for this task
```

Then use **AskUserQuestion** to ask:

**Question:** "How would you like to proceed?"

**Options:**
1. **Approve** — use the suggested criteria as-is and start execution
2. **Revise** — I'll describe changes and you'll update them before starting
3. **Define from scratch** — I'll write my own criteria; start execution once confirmed
4. **Abort** — cancel this execution run

**Wait for the user's response. Do NOT proceed until one of the four options is chosen.**

**Handling each response:**

- **Option 1 (Approve):** Use the suggested criteria verbatim. Proceed to Step 0.3.
- **Option 2 (Revise):** Read the user's modifications. Merge them with the suggested criteria (add, update, or remove items as directed). Show the merged result to the user and confirm. Proceed to Step 0.3.
- **Option 3 (Define from scratch):** Wait for the user to supply their own criteria. Use exactly what they provide — do not augment. Proceed to Step 0.3.
- **Option 4 (Abort):** Output "Execution aborted." and **STOP. Do not execute anything.**

---

### 0.3. Write the Criteria

**If a plan file exists** (this skill was invoked with a plan file path):
- Open the plan file
- Find the `## ACCEPTANCE CRITERIA` section if it exists, or append one before `## COMPLETION CHECKLIST` (or at the very end if that section is absent)
- Write or overwrite the section with the final agreed criteria using `- [ ]` checkboxes
- Use the Edit tool to make this change
- Output: "Acceptance criteria written to `<plan-file-path>`."

**If no plan file** (ad-hoc request):
- Print the final agreed criteria to the console so they are visible in the conversation
- Output: "Acceptance criteria confirmed (no plan file — criteria recorded above)."

---

### 0.4. Continue

Proceed to the Execution Mode Decision Protocol below.

---

## Execution Mode Decision Protocol

**REQUIRED:** Before executing, analyze the plan and explicitly state your execution mode decision.

### Step 1: Parse Plan for Parallel Signals

Read the plan and check for these explicit parallel execution indicators:

1. **"Parallel Execution Strategy" section** - Strongest signal
   - If present, extract the team structure, agent roles, and phase definitions
   - This section takes precedence over generic heuristics

2. **"Parallel Execution:" metadata** - Top-level plan metadata
   - Look for: `**Parallel Execution:** ✅ **Yes**` or similar
   - Indicates plan author explicitly designed for parallelism

3. **"Team Structure" section** - Defined agent assignments
   - Lists specific agents (e.g., "Agent 1 (Backend-API)", "Agent 2 (Frontend)")
   - Shows clear role separation suitable for parallel work

4. **"Execution Order" with phases** - Multi-phase execution plan
   - Shows dependencies between phases
   - Indicates which tasks can run concurrently

### Step 2: Evaluate Complexity and Task Count

If no explicit parallel signals found, fall back to task analysis:

- Count total tasks in "Step by Step Tasks" section
- Identify task dependencies (sequential chains vs. independent tasks)
- Assess task domains (frontend/backend separation enables parallelism)
- Consider execution time (long-running tasks benefit from parallelism)

### Step 3: Output Execution Mode Decision

**MANDATORY OUTPUT:** Print your decision using this template:

\`\`\`
## EXECUTION MODE DECISION

**Plan:** [plan name]
**Decision:** [TEAM-BASED PARALLEL | SEQUENTIAL]

**Reasoning:**
- Parallel signals found: [Yes/No]
  - Has "Parallel Execution Strategy" section: [Yes/No]
  - Has explicit team structure: [Yes/No]
  - Has phase-based execution order: [Yes/No]
- Task count: [N tasks]
- Task dependencies: [describe dependency structure]
- Complexity assessment: [Simple/Medium/Complex]

**Conclusion:**
[1-2 sentences explaining why you chose team-based or sequential execution]

**Team structure (if parallel):**
[List agent roles and responsibilities from plan, or design team if not specified]
\`\`\`

### Step 4: Proceed with Chosen Strategy

Based on your decision, jump to either:
- **Team-Based Parallel Execution** section (if team-based)
- **Sequential Execution** section (if sequential)

---

## Decision Criteria (Priority Order)

Use these criteria in priority order. Higher priority criteria override lower ones.

### Priority 1: Explicit Parallel Strategy in Plan (HIGHEST)
- ✅ **Use Team-Based:** Plan has "Parallel Execution Strategy" section
- ✅ **Use Team-Based:** Plan has "Team Structure" with named agents
- ✅ **Use Team-Based:** Plan has "Execution Order" with parallel phases

### Priority 2: Plan Metadata
- ✅ **Use Team-Based:** Complexity marked as 🔴 Complex or ⚠️ Medium with 4+ tasks
- ✅ **Use Team-Based:** Parallel Execution metadata says "✅ Yes"
- ⚠️ **Consider Team-Based:** Complexity marked as ⚠️ Medium with frontend + backend split

### Priority 3: Task Analysis (Fallback)
- ✅ **Use Team-Based:** 4+ tasks with clear domain separation (frontend/backend)
- ✅ **Use Team-Based:** 3+ independent long-running tasks (e.g., multiple test suites)
- ❌ **Use Sequential:** 1-3 simple tasks with sequential dependencies
- ❌ **Use Sequential:** All tasks tightly coupled (changes require coordination)

### Priority 4: Efficiency Tradeoff
- ⚠️ **Avoid Team-Based:** Team overhead > time savings (very simple plans)
- ✅ **Use Team-Based:** Estimated sequential time > 2 hours
- ✅ **Use Team-Based:** Validation can run in parallel with implementation

---

## Execution Mode

After completing the Execution Mode Decision Protocol above, you will execute using one of these strategies:

- **Sequential Execution:** For simple plans (see criteria in Decision Protocol)
- **Team-Based Parallel Execution:** For complex plans or plans with explicit parallel strategy

**NOTE:** If the plan includes a "Parallel Execution Strategy" section, you MUST use team-based execution, even if task count is low. The plan author has explicitly designed the work for parallelism.

---

## Sequential Execution

For simple plans (1-3 independent tasks, no parallel execution strategy):

### 1. Read and Understand

- Read the ENTIRE plan carefully
- Understand all tasks and their dependencies
- Note the validation commands to run
- Review the testing strategy

### 1.25. MANDATORY: Baseline Test Run

**REQUIRED BEFORE ANY CODE CHANGES:**

Run the full test suite once on the unmodified codebase and record the results:

1. Run: `[project test command]` (e.g., `uv run pytest tests/ -v` or `npm test`)
2. Record: N passing, N failing, N skipped
3. Note the names of any failing tests — these are **pre-existing failures**

**Document your baseline in your working notes:**
```
Pre-implementation baseline: X/Y passing.
Pre-existing failures (not introduced by this work):
  - test_foo_bar — [reason if known]
  - test_baz_qux — [reason if known]
```

**Why this runs before implementation, not after:**
Without a baseline, you cannot tell whether a failing test at validation time is something
you broke or something that was already broken. Pre-existing failures must be excluded from
the "all tests pass" acceptance criterion — but only if documented before you started.
If you discover failures mid-execution, you cannot retroactively claim they are pre-existing.

**If pre-existing failures are found:**
- For trivial fixes (≤30 min, clearly unrelated to your feature): fix them now before proceeding
- For non-trivial pre-existing issues: note them explicitly and exclude them from your acceptance criteria scope

### 1.5. MANDATORY: Enumerate Manual Prerequisites Before Writing Code

**REQUIRED IMMEDIATELY AFTER READING THE PLAN — before touching any files:**

Scan the plan for steps that cannot be automated: secrets, `.env` files, credentials, migrations, service setup, CLI installs.

**For EACH manual prerequisite found:**

1. Classify it:
   - **Runtime-critical** — required for the app to start or for any code path to function (e.g., `KB_API_KEY` in `.env`, DB migration)
   - **Validation-only** — only needed to run the final demo or integration tests

2. For **runtime-critical** prerequisites:
   - **STOP here** — do NOT write any code yet
   - Ask the user to complete the step now and confirm when done
   - Only proceed after confirmation

3. For **validation-only** prerequisites:
   - Note them — you will revisit at Step 2.8

**Why this must happen before coding, not just before validation:**

If you start writing tests before required secrets exist, you will inject env vars directly into test fixtures to make tests pass. This masks wiring bugs — e.g., `load_dotenv()` is never called because tests bypass it with `os.environ["KEY"] = "..."`. The gap is invisible: every file looks correct in isolation and every test passes. The user discovers the bug on first real startup.

---

### 2. Execute Tasks in Order

For EACH task in "Step by Step Tasks":

#### a. Navigate to the task
- Identify the file and action required
- Read existing related files if modifying

#### b. Implement the task
- Follow the detailed specifications exactly
- Maintain consistency with existing code patterns
- Include proper type hints and documentation
- Add structured logging where appropriate

#### b.5. Add Concise Code Remarks

**REQUIRED as part of every implementation task:**

**File-level comments** — Add a short comment block at the top of every file you create or significantly modify, unless one already exists. It should state:
- What the file is responsible for
- Why it exists / what role it plays in the system

Example (Python):
```python
# auth/token_validator.py
# Validates JWT tokens on incoming API requests.
# Lives here (not in middleware) so validation logic can be unit-tested independently.
```

Example (TypeScript):
```typescript
// hooks/useSession.ts
// Custom hook that manages user session state and syncs it with localStorage.
// Centralizes session logic so all components get a consistent view of auth state.
```

**Inline remarks** — Add a concise comment directly above (not inline with) any of the following, where the reason isn't immediately obvious from the code itself:
- Non-trivial algorithms or calculations
- Workarounds, hacks, or gotchas
- Critical business-logic decisions
- Async/concurrency patterns (why a lock, why a retry, etc.)
- Any code where a reasonable developer would ask "why is this here?"

**Rules:**
- Keep comments short (1–3 lines max)
- Explain the *why*, not the *what* — the code already shows what
- Do NOT add comments for self-explanatory code (getters, simple assignments, obvious CRUD)
- Do NOT add comments to every function — only where complexity or purpose warrants it

#### c. Verify as you go
- After each file change, check syntax
- Ensure imports are correct
- Verify types are properly defined

### 2.5. MANDATORY: Test Implementation Check

**REQUIRED BEFORE PROCEEDING TO STEP 3:**

1. **Check if plan specifies test files or test cases**
   - Review "Testing Strategy" section in plan
   - Review "Validation" section for test requirements
   - Check task descriptions for test-related work

2. **If tests ARE specified in plan:**
   - Create/update all specified test files
   - Implement all specified test cases
   - Run the test suite and capture output
   - Fix any failures
   - Confirm all tests pass
   - Show test results

3. **If NO tests specified in plan:**
   - Confirm with user: "Plan doesn't specify tests. Should I add tests for [implemented features]?"
   - Wait for user response before proceeding

4. **Do not mock away required user setup:**
   When a test fixture injects an env var that a user is supposed to supply (e.g., `os.environ["API_KEY"] = "test-key"`), this is fine for unit tests — but you must also ensure at least one validation command exercises the real loading path. Specifically: if an env-loading library (`python-dotenv`, `dotenv`, etc.) is in the plan or requirements, confirm that `load_dotenv()` (or equivalent) is called in the app entry point — not just that the library is installed. Search for the call site; if it is missing, add it before proceeding.

**DO NOT skip to validation without addressing test requirements.**

### 2.8. MANDATORY: Pre-Validation User Action Check

**CRITICAL:** Before running validation commands, check if the plan requires user actions that must be completed BEFORE tests can pass.

**Check the plan for these blocking prerequisites:**

1. **Database migrations** (explicitly mentioned example)
   - Search for "migration", "SQL", "schema changes", "CREATE TABLE", "ALTER TABLE"
   - If found: User must apply migration before tests will pass

2. **External service setup**
   - API key configuration (beyond .env.example updates)
   - Third-party account creation
   - Service deployments

3. **Infrastructure changes**
   - DNS updates
   - Environment provisioning
   - Deployment prerequisites

4. **Manual installations**
   - System-level dependencies (beyond pip/npm)
   - CLI tools
   - Database setup

5. **Env-loading wiring** — when `python-dotenv`, `dotenv`, or any config-loading library appears in requirements or the plan:
   - Search the codebase for the actual `load_dotenv()` call (or equivalent)
   - Verify it is in the app entry point (`main.py`, `app.py`, etc.) — not just in `requirements.txt` or `pyproject.toml`
   - If the call is missing: add it before running validation

**If ANY blocking user actions are required:**

1. **STOP execution** - Do NOT run validation commands yet
2. **List all required actions:**
   ```
   ⚠️ USER ACTIONS REQUIRED BEFORE VALIDATION

   The following actions must be completed before tests can pass:

   1. [Action description]
      - Why needed: [Brief explanation]
      - How to do it: [Clear instructions or reference to plan section]

   2. [Next action...]
   ```

3. **Ask user to notify when complete:**
   ```
   Please complete these actions and reply "done" or "ready" when finished.
   I will then continue with validation testing.
   ```

4. **WAIT for user confirmation** - Do NOT proceed until user responds

5. **After user confirms** - Continue to Step 3 (Run Validation Commands)

**If you did NOT block on manual prerequisites at Step 1.5** (missed them during planning):
- This is the same situation — STOP now, enumerate all uncompleted steps, ask the user to complete them, and wait before running validation.

**If NO blocking user actions found:**
- Proceed directly to Step 3

**Example blocking action (database migration):**
```
⚠️ USER ACTIONS REQUIRED BEFORE VALIDATION

1. Apply Database Migration
   - Why needed: Tests require new RPC functions (hybrid_search_chunks, keyword_search_chunks)
   - How to do it:
     * Open Supabase Dashboard → SQL Editor
     * Copy contents of supabase/migrations/013_hybrid_search.sql
     * Paste and execute in SQL Editor

Please complete this action and reply "done" when finished.
I will then run the full test suite to verify everything works.
```

**DO NOT claim tests "can't run" or mark execution complete without running tests after user completes required actions.**

### 3. MANDATORY: Run Validation Commands

**CRITICAL:** Execute EVERY validation command listed in the plan.

For EACH validation command:

1. **Run the command** - Execute exactly as specified in plan
2. **Capture and display full output** - Show complete command output
3. **Evaluate result:**
   - ✅ **PASS:** Mark as passed and continue to next command
   - ❌ **FAIL:** Mark as failed and STOP immediately
4. **If FAIL:**
   - Analyze the failure
   - Fix the issue
   - Re-run the command
   - Repeat until PASS
5. **Continue only when ALL commands pass**

**Verification Summary:**

After all commands run, display summary:
```
VALIDATION SUMMARY:
- Command 1: ✅ PASS (output shown above)
- Command 2: ✅ PASS (output shown above)
- Command 3: ✅ PASS (output shown above)
...

Status: [ALL PASSED / FAILURES DETECTED]
```

**If ANY command shows ❌ FAIL, execution is INCOMPLETE - fix and re-validate.**

### 3.5. MANDATORY: Debug Trace Cleanup

**CRITICAL:** Remove ALL debug traces added during implementation, debugging, and validation.

**What to remove:**
- ❌ `console.log()`, `console.debug()`, `console.info()` (JavaScript/TypeScript)
- ❌ `print()`, `pprint()` statements (Python)
- ❌ `debugger;` statements
- ❌ Commented-out debug code
- ❌ Temporary logging added for troubleshooting
- ❌ Test output statements not in test files

**What to keep:**
- ✅ Pre-existing debug logs that were already in the codebase
- ✅ Debug logs explicitly requested in the plan or requirements
- ✅ Proper logging framework usage (logger.debug, logger.info, etc.)
- ✅ Production logging for errors and important events

**How to identify debug traces YOU added:**

1. **Review git diff** - Look for new console.log/print statements
2. **Search codebase:**
   ```bash
   # JavaScript/TypeScript
   grep -r "console.log\|console.debug\|debugger;" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx"

   # Python
   grep -r "print(" --include="*.py" | grep -v "# keep" | grep -v "test_"
   ```
3. **Check each match** - Remove only what YOU added during this execution

**Verification:**
```bash
# Run search again after cleanup - should find zero new debug traces
# Compare with git diff to ensure only debug traces removed
git diff --stat
```

**DO NOT proceed to Verification Gate until debug traces are cleaned up.**

---

### 4. MANDATORY VERIFICATION GATE - EXECUTION INCOMPLETE UNTIL ALL PASS

**CRITICAL:** You CANNOT proceed to "Output Report" until ALL items below pass.

**BLOCKING REQUIREMENTS:**

- ✅ All tasks from plan completed (list them)
- ✅ All tests created and passing (show test run output)
- ✅ All validation commands pass (show validation summary)
- ✅ Debug traces removed (Step 3.5 completed)
- ✅ Code follows project conventions
- ✅ Documentation added/updated as needed

**Verification Process:**

1. Review each checklist item
2. Provide evidence for each (test output, validation results, etc.)
3. If ANY item is ❌ INCOMPLETE:
   - DO NOT generate Output Report
   - DO NOT claim execution complete
   - Fix the incomplete item
   - Re-verify
   - ONLY proceed when all ✅ COMPLETE

**Self-Check Question:**
"Can I confidently claim this execution is production-ready?"
- If NO → execution is INCOMPLETE, continue fixing
- If YES → proceed to Output Report

**DO NOT claim execution complete with failing validations or missing tests.**

---

## Team-Based Parallel Execution

For complex plans (4+ tasks, parallel opportunities, or explicit parallel strategy):

### 1. Plan Analysis & Team Setup

#### a. Read and Parse Plan
- Read ENTIRE plan carefully
- If plan has "Parallel Execution Strategy" section, extract team structure and phases
- If no explicit team structure, analyze tasks to design team composition
- Identify task dependencies and blocking relationships
- Note validation commands and testing strategy

#### b. Create Team
Use TeamCreate tool:
- team_name: "execute-{plan-name}"
- description: "Executing {plan-name} with parallel agents"

### 1.25. MANDATORY: Baseline Test Run

Same rule as in Sequential Execution — run the full test suite once on the unmodified codebase before spawning any agent or writing any code. Record N passing / N failing and note any pre-existing failures so agents are not held responsible for them during validation.

### 1.5. MANDATORY: Enumerate Manual Prerequisites Before Creating Tasks

Same rule as in Sequential Execution — scan the plan for all manual prerequisites before spawning any teammates or writing any code.

**Runtime-critical prerequisites** (secrets, `.env` files, credentials, migrations): ask the user to complete them now and wait for confirmation before proceeding.

Reason: spawned agents that start without real config will write tests that mock-inject env vars, masking wiring bugs that only appear at real startup.

---

### 2. Task Breakdown & Assignment

#### a. Create Tasks from Plan
For each task in the plan, create using TaskCreate

#### b. Map Tasks to Agents

**Common Team Structures:**

**3-Agent Team (Frontend/Backend split):**
- Agent 1 (Backend-API): API endpoints, routers, configuration
- Agent 2 (Backend-Core): Core services, business logic
- Agent 3 (Frontend): UI components, hooks, types

**4-Agent Team (Full-stack + Database):**
- Agent 1 (Database): Migrations, schema changes
- Agent 2 (Backend-Processing): Core services and processing
- Agent 3 (Backend-API): API layer
- Agent 4 (Frontend): UI and integration

### 3. Spawn Teammates & Execute in Waves

Create general-purpose agents for each role and execute tasks in dependency-based waves.

**During Execution:**
- Monitor teammate progress via messages
- Address blockers immediately
- Ensure agents mark tasks complete when done
- Coordinate integration points between agents

**Code Remarks — required for all agents:**

Each spawned agent MUST follow these commenting rules when implementing their tasks:

- **File-level comment** at the top of every file they create or significantly modify: briefly state what the file does and why it exists in the system.
- **Inline remarks** above non-obvious logic: explain the *why* (not the *what*) for algorithms, workarounds, critical business decisions, and async/concurrency patterns.
- Keep all comments short (1–3 lines). Skip comments for self-explanatory code.

Include this requirement explicitly in the prompt given to each spawned agent.

### 4. MANDATORY: Integration & Testing Verification

**REQUIRED BEFORE PROCEEDING:**

After all teammates complete their assigned tasks:

1. **Verify Integration:**
   - Check all file changes are compatible
   - Verify imports/exports between modules work
   - Test integration points manually if needed

2. **Run Test Suite:**
   - Execute ALL tests specified in plan
   - Capture complete output
   - If failures detected:
     - Fix issues
     - Re-run tests
     - Continue until all pass

3. **Display Test Results:**
```
TEST EXECUTION RESULTS:
[Show full test output]

Status: ✅ All tests passing
```

### 4.5. MANDATORY: Pre-Validation User Action Check

**CRITICAL:** Before running validation commands, check if the plan requires user actions that must be completed BEFORE tests can pass.

**Check the plan for these blocking prerequisites:**

1. **Database migrations** (explicitly mentioned example)
   - Search for "migration", "SQL", "schema changes", "CREATE TABLE", "ALTER TABLE"
   - If found: User must apply migration before tests will pass

2. **External service setup**
   - API key configuration (beyond .env.example updates)
   - Third-party account creation
   - Service deployments

3. **Infrastructure changes**
   - DNS updates
   - Environment provisioning
   - Deployment prerequisites

4. **Manual installations**
   - System-level dependencies (beyond pip/npm)
   - CLI tools
   - Database setup

5. **Env-loading wiring** — when `python-dotenv`, `dotenv`, or any config-loading library appears in requirements or the plan:
   - Search the codebase for the actual `load_dotenv()` call (or equivalent)
   - Verify it is in the app entry point (`main.py`, `app.py`, etc.) — not just in `requirements.txt` or `pyproject.toml`
   - If the call is missing: add it before running validation

**If ANY blocking user actions are required:**

1. **STOP execution** - Do NOT run validation commands yet
2. **List all required actions:**
   ```
   ⚠️ USER ACTIONS REQUIRED BEFORE VALIDATION

   The following actions must be completed before tests can pass:

   1. [Action description]
      - Why needed: [Brief explanation]
      - How to do it: [Clear instructions or reference to plan section]

   2. [Next action...]
   ```

3. **Ask user to notify when complete:**
   ```
   Please complete these actions and reply "done" or "ready" when finished.
   I will then continue with validation testing.
   ```

4. **WAIT for user confirmation** - Do NOT proceed until user responds

5. **After user confirms** - Continue to Step 5 (Run Validation Commands)

**If you did NOT block on manual prerequisites at Step 1.5** (missed them during planning):
- This is the same situation — STOP now, enumerate all uncompleted steps, ask the user to complete them, and wait before running validation.

**If NO blocking user actions found:**
- Proceed directly to Step 5

**Example blocking action (database migration):**
```
⚠️ USER ACTIONS REQUIRED BEFORE VALIDATION

1. Apply Database Migration
   - Why needed: Tests require new RPC functions (hybrid_search_chunks, keyword_search_chunks)
   - How to do it:
     * Open Supabase Dashboard → SQL Editor
     * Copy contents of supabase/migrations/013_hybrid_search.sql
     * Paste and execute in SQL Editor

Please complete this action and reply "done" when finished.
I will then run the full test suite to verify everything works.
```

**DO NOT claim tests "can't run" or mark execution complete without running tests after user completes required actions.**

### 5. MANDATORY: Run Validation Commands

**CRITICAL:** Execute EVERY validation command listed in the plan.

For EACH validation command:

1. **Run the command**
2. **Capture and display full output**
3. **Evaluate result:**
   - ✅ **PASS:** Continue to next
   - ❌ **FAIL:** STOP, fix, and re-run

**Validation Summary:**
```
VALIDATION SUMMARY:
- Command 1: ✅ PASS
- Command 2: ✅ PASS
- Command 3: ✅ PASS
...

Status: [ALL PASSED / FAILURES DETECTED]
```

### 5.5. MANDATORY: Debug Trace Cleanup

**CRITICAL:** Remove ALL debug traces added during implementation, debugging, and validation.

**What to remove:**
- ❌ `console.log()`, `console.debug()`, `console.info()` (JavaScript/TypeScript)
- ❌ `print()`, `pprint()` statements (Python)
- ❌ `debugger;` statements
- ❌ Commented-out debug code
- ❌ Temporary logging added for troubleshooting
- ❌ Test output statements not in test files

**What to keep:**
- ✅ Pre-existing debug logs that were already in the codebase
- ✅ Debug logs explicitly requested in the plan or requirements
- ✅ Proper logging framework usage (logger.debug, logger.info, etc.)
- ✅ Production logging for errors and important events

**How to identify debug traces added by team:**

1. **Review git diff** - Look for new console.log/print statements
2. **Search codebase:**
   ```bash
   # JavaScript/TypeScript
   grep -r "console.log\|console.debug\|debugger;" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx"

   # Python
   grep -r "print(" --include="*.py" | grep -v "# keep" | grep -v "test_"
   ```
3. **Check each match** - Remove only what was added during this execution

**Verification:**
```bash
# Run search again after cleanup - should find zero new debug traces
# Compare with git diff to ensure only debug traces removed
git diff --stat
```

**Coordinate cleanup across team** - Ensure all teammates remove their debug traces before proceeding.

**DO NOT proceed to Pre-Shutdown Verification Gate until debug traces are cleaned up.**

---

### 6. MANDATORY: Pre-Shutdown Verification Gate

**BLOCKING REQUIREMENTS - Cannot shutdown team until ALL pass:**

- ✅ All tasks complete (verify via TaskList)
- ✅ All tests passing (output shown)
- ✅ All validation commands pass (summary shown)
- ✅ Debug traces removed (Step 5.5 completed)
- ✅ Integration verified
- ✅ No blocking issues remain

**Only after ALL items ✅ COMPLETE:**

### 7. Team Shutdown

Gracefully shut down all teammates:
- Send shutdown requests to each agent
- Wait for acknowledgment
- Delete team using TeamDelete

---

## Best Practices

### Parsing Plan for Execution Guidance

**Always check for explicit parallel execution sections first:**

1. **Read plan header** - Look for metadata like complexity markers and parallel execution flags
2. **Search for section headers** - "Parallel Execution Strategy", "Team Structure", "Execution Order"
3. **Extract team definitions** - If plan defines agents, use those exact role names
4. **Follow plan's phase structure** - If plan defines Phase 1/2/3, use those as waves
5. **Respect plan dependencies** - If plan says "Agent 2 depends on Agent 1", enforce blocking

**Example: Plan with Explicit Strategy**

If plan contains "Parallel Execution Strategy" section with 3 agents defined, you MUST:
1. Create team with 3 agents using exact roles from plan
2. Assign tasks according to plan's agent mapping
3. Follow plan's execution order (phases)

### When to Use Parallel Execution

**Use team-based parallel execution when:**
- ✅ Plan explicitly defines parallel execution strategy
- ✅ 4+ tasks with clear domain separation
- ✅ Frontend and backend work can proceed independently
- ✅ Multiple long-running test suites can run concurrently

**Use sequential execution when:**
- ✅ 1-3 simple, fast tasks
- ✅ Tasks have tight sequential dependencies
- ✅ All work affects the same files (high conflict risk)

---

## Decision Examples

### Example 1: Plan with Explicit Parallel Strategy

**Plan Structure:**
- Has "Parallel Execution Strategy" section ✅
- Defines 3 agents with specific roles ✅
- Shows phase-based execution order ✅

**Decision:**
TEAM-BASED PARALLEL - Plan explicitly defines 3-agent team structure. Must use team-based execution as plan author designed for parallelism.

### Example 2: Simple Sequential Plan

**Plan Structure:**
- No "Parallel Execution Strategy" section ❌
- 2 tasks with sequential dependency
- Complexity: Simple

**Decision:**
SEQUENTIAL - No parallel signals, only 2 tightly coupled tasks. Team overhead not justified.

### Example 3: Complex Plan (Design Team Yourself)

**Plan Structure:**
- No explicit parallel strategy ❌
- 8 tasks: 4 frontend + 4 backend
- Complexity: Complex
- Clear domain separation

**Decision:**
TEAM-BASED PARALLEL - Clear frontend/backend separation justifies team execution. Design 3-agent team to parallelize work.

---

## Output Report

**ONLY generate this report after passing Step 4 Mandatory Verification Gate.**

After execution completes and all validations pass, provide summary:

### Completed Tasks
- List all tasks completed with checkmarks
- Files created/modified with paths

### Test Results

**Tests Created/Updated:**
- [List test files created]
- [List test files updated]

**Test Suite Execution:**
```
[Show full test suite output]
```

**Status:** ✅ All tests passing

### Validation Results

**Validation Commands Executed:**

| Level | Command | Status | Output |
|-------|---------|--------|--------|
| 1 | [command] | ✅ PASS | [summary] |
| 2 | [command] | ✅ PASS | [summary] |
| 3 | [command] | ✅ PASS | [summary] |
| ... | ... | ... | ... |

**Validation Summary:** ✅ ALL VALIDATIONS PASSED

### Code Quality

- ✅ Code follows project conventions
- ✅ Documentation added/updated
- ✅ Types properly defined
- ✅ Error handling implemented

### Execution Metrics (if team-based)
- Number of agents used
- Estimated time saved vs sequential
- Coordination overhead
- Task distribution across agents

### Final Status

✅ **EXECUTION COMPLETE** - All implementations, tests, and validations passed successfully.

**Ready for commit:** Yes - all changes verified and production-ready.

---

## Invoke Post-Execution Skills

After generating the Output Report above, launch the following skills as **parallel subagents** using the Agent tool. Start all available skills simultaneously — do NOT wait for one to finish before starting the others.

For each skill, check whether it is available in this system. If it is, spawn it as an Agent subagent. If it is not available, skip it silently.

---

### Subagent 1 — Execution Report (always run if available)

**Skill:** `execution-report`

Pass this context to the subagent:

**Coverage gap context — required for execution-report:**

Compare planned test coverage (from the plan file) against what was actually executed:

1. **Planned coverage** — from the plan's "Test Automation Summary" / "Coverage Summary":
   - Each planned test: automation status (✅/⚠️), tool, file path
   - Planned automated % and total code-path coverage %

2. **Actual coverage** — from this execution:
   - Which planned tests were created and passed (✅)
   - Which planned tests were skipped, deferred, or left failing (⚠️/❌)
   - Which VALIDATION COMMANDS levels were not executed or produced failures

3. **Gaps** — explicitly identify:
   - Tests planned but not implemented
   - Validation levels that were skipped or failed without resolution
   - Code paths introduced during implementation that were not in the original plan and have no test coverage

Use this to populate the "Test Results" and "Validation Results" sections of the execution report, and add a **"Coverage Gaps"** subsection that lists each gap with its severity (blocking / non-blocking) and a recommended follow-up action.

---

### Subagent 2 — Acceptance Criteria Validation (run if available)

**Skill:** `acceptance-criteria-validate`

Pass the plan file path and the execution output summary as context. The skill will locate acceptance criteria in the plan (or in `acceptance_criteria.md`) and validate whether each was met. It will produce a ACCEPTED / REJECTED / NEEDS REVIEW verdict and surface any unmet criteria.

**If this skill produces a REJECTED or NEEDS REVIEW verdict:** surface its output prominently to the user before declaring execution complete. Do not silently discard a failing validation result.

---

### Subagent 3 — Code Review (run if available)

**Skill:** `code-review`

Pass the list of files modified during this execution and the plan file path as context. The skill will perform a technical review of all changed files for bugs, security issues, and standards compliance.

---

**Note:** These skills are installed via the marketplace. Do NOT use a bash file-existence check — just attempt to invoke each via the Agent tool and it will fail gracefully if the skill is not installed.
