---
name: atdd
description: >-
  This skill should be used when the user asks to "build a feature",
  "implement a feature", "add functionality", "start development",
  "write acceptance tests", "write specs", "use ATDD", "use TDD with
  acceptance tests", or begins any feature implementation work. Also
  triggered by the /atdd command. Enforces the Acceptance Test Driven
  Development workflow: write Given/When/Then specs before code, generate
  a project-specific test pipeline, and maintain two test streams.
version: 0.4.0
---

# Acceptance Test Driven Development

Enforce the ATDD workflow for feature development. This methodology is
adapted from Robert C. Martin's acceptance test approach.

## Core Principle

> "The two different streams of tests cause Claude to think much more
> deeply about the structure of the code."
> — Robert C. Martin

Two test streams constrain development:
- **Acceptance tests** define WHAT the system does (external observables)
- **Unit tests** define HOW the system does it (internal structure)

Both must pass. Neither alone is sufficient.

## Workflow

Follow these steps strictly, in order. Do not skip steps.

### Step 1: Understand the Feature

Before writing anything, understand what is being built:

- Ask clarifying questions about the feature's purpose
- Identify the domain language (what terms do users/stakeholders use?)
- Determine success criteria: what observable behavior proves it works?
- Scope it: "just enough specs for this sprint" — do not design the whole system

### Step 2: Write GWT Acceptance Specs

Create spec files in the project's `specs/` directory using this format:

```
;===============================================================
; Description of the behavior being specified.
;===============================================================
GIVEN [precondition in domain language].
GIVEN [another precondition if needed].

WHEN [action the user/system takes].

THEN [observable outcome].
THEN [another observable outcome if needed].
```

**Format rules:**
- Semicolon comments with `===` separators delimit test cases
- GIVEN sets up preconditions (state before the action)
- WHEN describes the action (one action per test, ideally)
- THEN describes observable outcomes (external behavior only)
- Use periods at the end of each statement
- Use natural domain language, never implementation language

**The spec-leakage rule — CRITICAL:**

Specs must describe **external observables only**. Never reference:
- Class names, function names, method names
- Database tables, columns, queries
- API endpoints, HTTP methods, status codes
- Framework-specific terms (controllers, services, repositories)
- Internal state, variables, data structures
- File paths or module names

```
BAD:  GIVEN the UserService has an empty userRepository.
GOOD: GIVEN there are no registered users.

BAD:  WHEN a POST request is sent to /api/users.
GOOD: WHEN a new user registers with email "bob@example.com".

BAD:  THEN the database contains 1 row in the users table.
GOOD: THEN there is 1 registered user.
```

**Present specs to the user for approval before proceeding.**
Specs are co-authored, but the human has final approval — ferociously defended.

### Step 3: Generate the Test Pipeline

Invoke the `pipeline-builder` agent to analyze the project and generate
(or update) the three-stage pipeline:

1. **Parser** — reads `.txt` spec files from `specs/`, produces structured IR
2. **IR format** — intermediate representation (JSON, YAML, or native format
   depending on the project's language/ecosystem)
3. **Generator** — reads IR, produces executable test files for the project's
   test framework (pytest, Jest, JUnit, Go testing, RSpec, etc.)

The pipeline must have **deep knowledge of the system internals**.
This is NOT Cucumber. The generator produces complete, runnable tests
that call into the system's internals — not stubs requiring manual fixtures.

A runner script/command should be generated so the user can run:
```
# Full pipeline: parse specs → generate tests → run tests
./run-acceptance-tests.sh
```

### Step 4: Run Acceptance Tests (Red)

Run the generated acceptance tests. They should **fail** — this confirms
the specs describe behavior that doesn't exist yet.

If they pass, either:
- The behavior already exists (specs are redundant — revise or remove)
- The generator is not testing the right thing (fix the pipeline)

### Step 5: Implement with TDD

Now implement the feature using standard TDD:

1. Write a failing unit test for the smallest piece of the feature
2. Write minimal code to make it pass
3. Refactor
4. Repeat until the acceptance tests pass

**Both streams must pass:**
- Unit tests verify internal correctness
- Acceptance tests verify external behavior matches specs

### Step 6: Review Specs for Leakage

After implementation, invoke the `spec-guardian` agent to review all
spec files for implementation details that may have crept in during
development.

If leakage is found, clean the specs back to domain language.

### Step 7: Iterate

Return to Step 1 for the next feature. Each iteration adds specs only
for the current feature — never design the whole system upfront.

## Rules

These rules govern how spec files and the pipeline are handled.
They are non-negotiable.

### Spec file discipline
- **Never modify a spec `.txt` file without explicit user permission.**
  Specs are the user's contract. Always ask before changing them.
- If a directive in a spec is ambiguous, **report the ambiguity rather
  than guessing**. Let the user clarify.

### Pipeline discipline
- **Never modify generated test files** in `generated-acceptance-tests/`.
  Only delete and regenerate them by running the pipeline from the `.txt`
  source.
- **Generated files are gitignored.** Add `generated-acceptance-tests/`
  and `acceptance-pipeline/ir/` to `.gitignore`. Never commit generated
  artifacts.
- Before running the pipeline, **check modification dates**: if a `.txt`
  spec file is newer than its IR or generated test, re-parse and
  regenerate before running.
- **Clear state before each test.** Generated tests must reset all
  application state before each test case to ensure isolation.

### Failure handling
- On test failure, **report the source spec file name and line number**
  of the first GIVEN line for the failing test. Traceability back to
  the spec is critical.
- If a spec cannot be translated into a test, **still generate it as a
  failing test** that documents the desired behavior. Report to the user
  which spec and why it could not be fully translated.
- Mock non-deterministic behavior (random numbers, timestamps, etc.) in
  generated tests to ensure reproducibility.

### Before pushing
- Before a git push, **ask the user whether acceptance tests should be
  run**. Do not push without confirming both test streams pass.

## Anti-Patterns to Watch For

### "Let me just write the code first"
No. Specs first, always. The spec-before-code hook will warn about this.

### "The specs are too high-level to test"
Then the specs need to be more specific. Break the feature into smaller
observable behaviors. Each spec should describe one concrete scenario.

### "Let me add implementation details so the generator is easier to write"
This is the perverse incentive. Fight it. The generator should be smart
enough to map domain language to system internals. If it can't, improve
the generator — don't pollute the specs.

### "We only need acceptance tests, unit tests are redundant"
No. Two streams constrain development differently. Acceptance tests alone
leave internal structure unchecked. Unit tests alone miss integration.

## File Organization

```
project-root/
├── specs/                       # Acceptance test specs (.txt files)
│   ├── authentication.txt       #   — committed to git
│   ├── shopping-cart.txt        #   — committed to git
│   └── ...
├── acceptance-pipeline/         # Pipeline code (parser + generator)
│   ├── parser.*                 #   — committed to git
│   ├── generator.*              #   — committed to git
│   └── ir/                      #   — GITIGNORED (generated)
├── generated-acceptance-tests/  # Executable test files
│   └── ...                      #   — GITIGNORED (generated)
└── run-acceptance-tests.sh      # Pipeline runner — committed to git
```

### What to commit vs. gitignore

**Commit these (source of truth):**
- `specs/*.txt` — the acceptance test specs
- `acceptance-pipeline/parser.*` — the parser code
- `acceptance-pipeline/generator.*` — the generator code
- `run-acceptance-tests.sh` — the pipeline runner script

**Gitignore these (regenerated from source):**
- `acceptance-pipeline/ir/` — intermediate representations
- `generated-acceptance-tests/` — generated test files

Add to the project's `.gitignore`:
```
acceptance-pipeline/ir/
generated-acceptance-tests/
```

### Project CLAUDE.md integration

After setting up the pipeline, add an **Acceptance Tests** section to
the project's `CLAUDE.md` (or create one if it doesn't exist). This
ensures Claude Code understands the ATDD setup in every session:

```markdown
## Acceptance Tests

Acceptance tests are `.txt` files in `specs/` in Given/When/Then format.

### Pipeline

```
.txt → Parser → IR → Generator → executable tests
```

1. **Parse:** [parse command] — reads `specs/*.txt`, produces IR in `acceptance-pipeline/ir/`
2. **Generate:** [generate command] — reads IR, produces test files in `generated-acceptance-tests/`
3. **Run:** [test command] — executes the generated tests

Full pipeline: `./run-acceptance-tests.sh`

### Rules

- Never modify a spec `.txt` file without explicit permission.
- Never modify generated tests — only delete and regenerate via the pipeline.
- Generated tests and IR files are gitignored — do not commit them.
- Before a push, run the full acceptance test pipeline.
- On failure, report the spec file name and line number.
```

Adapt the commands and paths to match the project's language and
test framework. The pipeline-builder agent generates this CLAUDE.md
section automatically when creating the pipeline.
