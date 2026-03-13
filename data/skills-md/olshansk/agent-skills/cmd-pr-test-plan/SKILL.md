---
name: cmd-pr-test-plan
description: Generate manual test plans for PR changes with verified commands and pass/fail criteria
disable-model-invocation: true
context: fork
agent: general-purpose
---

# PR Test Plan

Generate a manual test plan for the changes in the current branch. The plan should give a reviewer everything they need to verify the PR -- copy-paste commands, clear pass/fail criteria, and logical grouping by change area.

## Instructions

### Step 1: Detect base branch

Try these methods in order:

```bash
BASE_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null)
```

```bash
BASE_BRANCH=$(git remote show origin 2>/dev/null | grep "HEAD branch" | cut -d: -f2 | xargs)
```

If both fail, ask the user.

### Step 2: Gather change context

Run all of these and capture the results:

```bash
git diff $BASE_BRANCH...HEAD --name-only
git diff $BASE_BRANCH...HEAD --stat
git log $BASE_BRANCH..HEAD --oneline
```

### Step 3: Detect project tooling

Check what's available in the project so you can reference real commands (not generic guesses):

- **Makefile targets**: `make help 2>/dev/null || grep -E '^[a-z_-]+:.*##' Makefile makefiles/*.mk 2>/dev/null`
- **Package manager**: Look for `pyproject.toml` (uv/pip), `package.json` (npm/pnpm), `Cargo.toml` (cargo), `go.mod` (go)
- **Test runners**: Look for `pytest.ini`, `pyproject.toml [tool.pytest]`, `jest.config.*`, `.mocharc.*`
- **Project docs**: Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or `README.md` for project-specific test/build instructions
- **CI config**: Check `.github/workflows/`, `Makefile`, or `Taskfile.yml` for existing test commands

**Prefer project Makefile targets and documented commands over raw tool invocations.** If the project has `make test_unit`, use that instead of `uv run pytest tests/unit/`.

### Step 4: Categorize changes and confirm with user

Group changed files into categories. Common categories (adapt based on actual changes):

- **Feature code** -- new commands, API routes, services, UI components
- **Configuration / docs** -- config files, markdown, schemas, manifests
- **Tests** -- new or modified test files
- **Build / deploy** -- Makefiles, CI, Dockerfiles, scripts
- **Deletions** -- removed files or deprecated code

Present the detected categories to the user with a summary of what changed in each. Ask them to confirm or adjust before generating the full plan.

Example confirmation format:

```
I found 3 change areas in this branch:

1. CLI agent mode -- new --agent flag on setup command (cli/commands/setup.py, cli/cli.py)
2. Skills restructuring -- SKILL.md rewrite, new reference docs, deleted shell scripts
3. Test fixes -- E2E test stability improvements (4 test files)

Should I generate the test plan for all 3, or would you like to adjust?
```

### Step 5: Generate the test plan

For each confirmed category, generate a test section following these rules:

#### Formatting rules

- **Numbered sections** with separator lines (`---`) between them
- **Numbered sub-steps** within each section (1a, 1b, 1c...)
- Each sub-step has a **bold title** describing what to test
- Each sub-step has a **copy-paste command** in a fenced code block
- Each sub-step has a **"Verify:"** line stating what success looks like
- **One command per code block** -- never stack multiple commands in one block with comments between them
- Use **Makefile targets** when available instead of raw tool commands
- For commands requiring env vars, put them inline: `GROVE_API_URL=http://localhost:8000 make test_e2e_suite`

#### What to include per category

**Feature code:**
- Happy path: the main thing the feature does, verified end-to-end
- Edge cases: invalid inputs, missing arguments, boundary values
- Help text / discoverability: `--help` output shows new flags/options
- Error messages: meaningful output on failure, correct exit codes

**Configuration / docs:**
- Validate file format (JSON parse, YAML lint, markdown render)
- Verify expected files exist and unexpected files are gone
- If publishable: serve locally and fetch to verify

**Tests:**
- Run the relevant test suite(s) with the project's standard commands
- Call out expected pass counts if known from prior runs
- List individual test commands for spot-checking specific fixes

**Build / deploy:**
- Dry-run build or deploy commands
- Verify targets still work after changes

**Deletions:**
- Confirm removed files are actually gone
- Verify nothing references the deleted files (grep for imports/includes)

#### Quick smoke test section

Always end with a "Quick Smoke Test" section -- the 2-3 commands a reviewer would run if they only have 60 seconds.

### Step 6: Write output

1. **Write the plan** to `TEST_PLAN.md` in the repo root
2. **Print a summary** to the terminal showing the section count and a one-liner per section

Terminal summary format:

```
Wrote TEST_PLAN.md with 4 sections:

  1. CLI Agent Mode -- 7 test steps (happy path, errors, help text)
  2. Skills Restructuring -- 6 test steps (validation, file checks, local serve)
  3. Automated Tests -- 4 test steps (unit, CLI, SDK, E2E suite)
  4. Quick Smoke Test -- 3 commands

Run `cat TEST_PLAN.md` to view the full plan.
```

## Style Reference

Follow the same style used in `cmd-pr-description`:
- **Bold the what**, plain text the how
- No fluff -- every step must verify something
- Copy-paste ready -- a reviewer should never need to edit a command
- Separate code blocks -- one command per block, bold header above it
