---
name: run-automated-tests
description: Analyze a target repository's automated testing approach and run the most appropriate test command(s) safely.
tags: [automation, devops, eng-standards]
version: 0.1.0
license: MIT
related_skills: [review-codebase, generate-github-workflow]
recommended_scope: both
metadata:
  author: ai-cortex
compatibility: Requires git (optional), a shell, and the repo's language toolchain(s) (e.g., node, python, go, dotnet, java).
---

# Skill: Run Automated Tests

## Purpose

Determine how a target repository expects automated tests to be executed (commands, frameworks, prerequisites, and scope), then run the best matching test suite(s) with a safety-first interaction policy.

## Use Cases

- You cloned a repo and want the correct test command without guessing.
- A repo has multiple test layers (unit/integration/e2e) and you need a safe default run plan.
- CI is failing and you want to reproduce locally by running the same commands used in workflows.

## Behavior

1. **Establish scope and constraints (ask if ambiguous)**
   - If the user did not specify, default to a **fast, local, non-destructive** run:
     - Unit tests only, no external services, no Docker, no network-dependent setup.
   - Ask the user to choose a mode if needed:
     - `fast`: unit tests only, minimal setup.
     - `ci`: mirror CI workflow commands as closely as possible.
     - `full`: include integration/e2e tests and service dependencies.
   - Ask whether Docker is allowed, whether network access is allowed, and whether installing dependencies is allowed.

2. **Discover the test plan (evidence-based)**
   - Read these sources in order; stop early if a clear, explicit test command is found:
     - `README.md`, `CONTRIBUTING.md`, `TESTING.md`, `docs/testing*`, `Makefile`
     - CI configs: `.github/workflows/*.yml`, `.gitlab-ci.yml`, `azure-pipelines.yml`, `Jenkinsfile`
     - Build manifests: `package.json`, `pyproject.toml`, `setup.cfg`, `tox.ini`, `go.mod`, `pom.xml`, `build.gradle*`, `*.csproj`, `Cargo.toml`
   - Identify:
     - Primary test entrypoints (`npm test`, `pnpm test`, `yarn test`, `pytest`, `tox`, `go test`, `dotnet test`, `mvn test`, `gradle test`, `cargo test`, etc.)
     - Test layers and markers (unit vs integration vs e2e)
     - Environment prerequisites (DB, Redis, Docker Compose, required env vars, secrets)
     - How CI sets up dependencies (services, caches, artifacts)
   - Prefer **explicit instructions** found in docs or CI over heuristics.

3. **Select an execution plan**
   - If `ci` mode: derive the run sequence from the repo's CI workflow steps (closest match).
   - If `fast` mode: pick the most direct unit-test command with the least prerequisites.
   - If multiple stacks exist (e.g., backend + frontend), propose running each stack separately in a deterministic order.
   - If the plan requires dependency installation or service startup, request confirmation before proceeding.

4. **Execute with guardrails**
   - Always print the exact commands you will run before running them.
   - Use a working directory rooted at the target repo (default `.`).
   - Capture and summarize failures:
     - First failing command and exit code
     - The most relevant error excerpt
     - Next actions (missing toolchain, missing env var, service not running, etc.)
   - Avoid destructive operations:
     - Do not run `rm -rf`, `git clean -fdx`, `docker system prune`, or database drop/migrate commands without explicit user approval.
   - If the repo requires secrets, do not ask the user to paste secrets into chat. Prefer `.env` files, secret managers, or documented local dev flows.

## Input & Output

**Input**

- Target repository path (default `.`).
- Mode: `fast` (default), `ci`, or `full`.
- Constraints: allow dependency install (yes/no), allow network (yes/no), allow Docker (yes/no).

**Output**

- A short "Test Plan Summary" containing:
  - Evidence: which files/paths informed the plan
  - Chosen commands (in order)
  - Assumptions and prerequisites
  - What was executed and what was skipped (and why)
- Command transcript snippets sufficient to debug failures (do not dump extremely long logs unless asked).

## Restrictions

- Do not invent test commands when evidence exists (prefer docs/CI).
- Do not install dependencies, run Docker, or start external services without confirmation.
- Do not modify repository files unless the user explicitly requests it (exception: generating a report file if the user asked for artifacts).
- Do not exfiltrate secrets; do not request sensitive credentials in chat.

## Self-Check

Before you finish:

1. Confirm you identified at least one authoritative test instruction source:
   - A doc file (README/CONTRIBUTING/TESTING), or
   - A CI workflow step, or
   - A build manifest script target (e.g., `package.json` scripts).
2. Confirm you asked for confirmation before any action that:
   - Installs dependencies, uses network, starts Docker/services, or changes state outside the repo.
3. Confirm the final output includes:
   - Evidence paths, selected commands, execution results, and any missing prerequisites.
4. If tests failed, confirm you provided:
   - The first failing command, exit code, and the likely root cause category (toolchain/env/service/test failure).

## Examples

**Example 1: JavaScript repo with package.json**

User: "Run tests for this repo."

Agent:

1. Inspect `package.json` scripts and `.github/workflows/*`.
2. Decide mode `fast` and propose:
   - `npm test` (or `pnpm test` / `yarn test` if the repo standardizes on it)
3. Ask: "Install dependencies (`npm ci`) and allow network?"
4. Run:
   - `npm ci`
   - `npm test`
5. Summarize results and point to failing test output if any.

**Example 2 (Edge case): Monorepo with integration tests requiring Docker**

User: "Mirror CI locally."

Agent:

1. Parse `.github/workflows/ci.yml` and identify separate jobs:
   - backend unit tests
   - frontend tests
   - integration tests with `docker compose`
2. Ask for confirmation:
   - allow Docker
   - allow network
   - which jobs to run (all vs only failing job)
3. Execute in a controlled order:
   - install deps per job
   - run unit tests first
   - bring up services for integration tests
4. If integration tests fail, summarize:
   - service health / port conflicts
   - missing env vars
    - how CI config differs from local

---

## Appendix: Output contract

Each skill execution MUST produce a **Test Plan Summary** in this exact JSON format:

```json
{
  "test_plan_summary": {
    "mode": "fast | ci | full",
    "evidence": ["path/to/source1", "path/to/source2"],
    "commands": [
      {"command": "npm test", "purpose": "run unit tests", "order": 1}
    ],
    "prerequisites": ["npm ci", "Docker running"],
    "executed": ["npm ci", "npm test"],
    "skipped": ["integration tests - require Docker"],
    "result": {
      "status": "passed | failed | blocked",
      "exit_code": 0,
      "first_failure": {
        "command": "npm test",
        "exit_code": 1,
        "error_excerpt": "FAIL src/utils.test.js"
      }
    }
  }
}
```

| Element | Type | Description |
| :--- | :--- | :--- |
| `mode` | string | Selected mode: `fast`, `ci`, or `full` |
| `evidence` | array | Source files that informed the test plan |
| `commands` | array | Selected test commands with purpose and order |
| `prerequisites` | array | Required setup steps |
| `executed` | array | Commands actually run |
| `skipped` | array | Commands skipped and reason |
| `result.status` | string | `passed`, `failed`, or `blocked` |
| `result.exit_code` | number | Exit code of test command |
| `result.first_failure` | object | First failure details (if any) |

This schema enables Agent consumption without prose parsing.
