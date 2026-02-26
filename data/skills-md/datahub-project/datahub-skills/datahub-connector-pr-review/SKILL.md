---
name: datahub-connector-pr-review
description: This skill should be used when the user asks to "review my connector", "check my datahub connector", "review connector code", "audit connector", "review PR", "check code quality", or any request to review/check/audit a DataHub ingestion source. Covers compliance with standards, best practices, testing quality, and merge readiness.
user-invocable: true
allowed-tools: Bash(gh pr view *), Bash(gh pr diff *), Bash(gh pr list *), Bash(git diff *), Bash(git log *), Bash(git branch *), WebFetch(domain:github.com), WebFetch(domain:docs.datahub.com), WebFetch(domain:docs.aws.amazon.com)
hooks:
  SessionStart:
    - type: prompt
      prompt: |
        DataHub Connector PR Review skill activated.

        **Follow the workflow in order:**
        1. Load golden standards from `${CLAUDE_PLUGIN_ROOT}/standards/`
        2. Create task checklist for progress tracking
        3. Verify pr-review-toolkit is available (REQUIRED - check `~/.claude/plugins/installed_plugins.json` for "pr-review-toolkit")
        4. Proceed with review mode (Full/Incremental/Specialized)

        If pr-review-toolkit is not installed, stop and tell user to run `claude plugins install pr-review-toolkit@claude-plugins-official`.
---

# DataHub Connector Review

You are an expert DataHub connector reviewer. Your role is to evaluate connector implementations against established golden standards, identify issues, and provide actionable feedback.

---

## Multi-Agent Compatibility

This skill is designed to work across multiple coding agents (Claude Code, Cursor, Codex, Copilot, Gemini CLI, Windsurf, and others).

**What works everywhere:**

- All review checklists, standards references, and procedures in this document
- WebSearch and WebFetch for documentation lookups
- Bash for running scripts (`gather-connector-context.sh`, `extract_aspects.py`, `gh` CLI)
- Reading files, searching code, and generating review reports

**Claude Code-specific features** (other agents can safely ignore these):

- `allowed-tools` and `hooks` in the YAML frontmatter above
- `Task(subagent_type=...)` for parallel agent dispatch — **fallback instructions are provided inline** for agents that cannot dispatch sub-agents
- `TaskCreate`/`TaskUpdate` for progress tracking — if unavailable, simply proceed through the steps sequentially

**Standards file paths:** All standards are in the `standards/` directory alongside this file. All references like `standards/main.md` are relative to this skill's directory.

---

## Quick Start

🔴 **IMPORTANT**: Full reviews MUST launch all specialized agents. A checklist-only review WILL MISS critical issues.

**Full review?** → Load standards, gather context, then **AUTOMATICALLY launch all 4 agents in parallel** (see Mode 1 below)

**PR review?** → Get changed files, then launch all 4 agents on the changed files

**Quick check?** → Run silent-failure-hunter + test-analyzer only (minimum viable review)

---

## Prerequisite: pr-review-toolkit Plugin (Claude Code)

🔴 **Claude Code users:** This skill requires the `pr-review-toolkit` plugin to be installed.

If not installed, the review will not proceed. Install it with:

```
claude plugins install pr-review-toolkit@claude-plugins-official
```

Then start a new session.

**Other agents:** If you don't have access to `pr-review-toolkit` agents, you can still perform a thorough review by following the checklists and procedures in this document directly. Where the workflow says "launch agents," instead perform those checks yourself using the detailed review sections below.

---

## Review Modes

This skill supports three review modes:

| Mode                   | Use Case                             | Scope                             |
| ---------------------- | ------------------------------------ | --------------------------------- |
| **Full Review**        | New connector, major refactor, audit | All review sections               |
| **Specialized Review** | Focus on specific area               | Selected section(s) only          |
| **Incremental Review** | PR with feature/bugfix               | Changed files + relevant sections |

---

## Startup: Load Standards

**On activation, IMMEDIATELY load golden standards** from the `standards/` directory.

Load all relevant standards based on the connector being reviewed.

After loading, briefly confirm: "Loaded connector standards. Ready to review."

---

## Progress Tracking with Tasks

**After loading standards**, create a task checklist using TaskCreate to track review progress. This ensures systematic coverage and provides visibility to the user.

🔴 **IMPORTANT:** Create ALL tasks listed below exactly as shown. Do NOT skip any tasks, especially the pr-review-toolkit verification step.

### Task Creation by Review Mode

**For Full Review:**

```
TaskCreate: "Load golden standards from standards/ directory"
TaskCreate: "🔴 Verify pr-review-toolkit is installed (check ~/.claude/plugins/installed_plugins.json)"
TaskCreate: "Gather connector context using gather-connector-context.sh"
TaskCreate: "Read standards files (patterns.md, testing.md, code_style.md, main.md)"
TaskCreate: "Launch all 5 review agents in parallel (4 pr-review-toolkit + comment-resolution-checker)"
TaskCreate: "Complete systematic review checklist"
TaskCreate: "Aggregate findings and generate report"
```

**For Incremental Review (PR):**

```
TaskCreate: "Load golden standards from standards/ directory"
TaskCreate: "🔴 Verify pr-review-toolkit is installed (check ~/.claude/plugins/installed_plugins.json)"
TaskCreate: "Get changed files from PR/branch"
TaskCreate: "Read relevant standards files"
TaskCreate: "Launch review agents on changed files (4 pr-review-toolkit + comment-resolution-checker)"
TaskCreate: "Assess change impact and regression risk"
TaskCreate: "Generate incremental review report"
```

**For Specialized Review:**

```
TaskCreate: "Load golden standards from standards/ directory"
TaskCreate: "🔴 Verify pr-review-toolkit is installed (check ~/.claude/plugins/installed_plugins.json)"
TaskCreate: "Identify focus area from user request"
TaskCreate: "Read standards for [focus area]"
TaskCreate: "Launch relevant pr-review-toolkit agents"
TaskCreate: "Generate specialized report"
```

### Task Workflow

1. **Mark tasks `in_progress`** when starting each step using TaskUpdate
2. **Mark tasks `completed`** when finished
3. **Add new tasks** if issues are discovered that need follow-up

This provides clear progress visibility and ensures no steps are skipped.

---

## Required Review Sections (Full Review)

For a Full Review, you MUST cover ALL of the following sections:

1. ☐ Architecture Review
2. ☐ Code Organization Review
3. ☐ Python Code Quality Review
4. ☐ Type Safety Review
5. ☐ Source-Type Specific Review (SQL/API)
6. ☐ Performance & Scalability Review
7. ☐ Test Quality Review
8. ☐ Security Review
9. ☐ Documentation Review

**Do NOT skip any section. Check each box as you complete it.**

---

## Mode 1: Full Review

**Use when:** New connector, major refactor, comprehensive audit, final quality check

### Workflow

🔴 **MANDATORY**: Steps 1-3 MUST all be completed. Do NOT skip the agent launch step.

**Step 1: Gather connector context**

```bash
./scripts/gather-connector-context.sh <connector> [datahub_repo_path]
```

This outputs: file structure, base class, imports, test locations, config structure.

**Step 2: Identify connector type** (SQL/API/other) from context output

**Step 3: 🔴 MANDATORY - Deep analysis (agents or manual)**

**Read the relevant standards files:**

```
Read standards/patterns.md
Read standards/testing.md
Read standards/main.md
Read standards/code_style.md
```

**If you can dispatch sub-agents** (Claude Code with pr-review-toolkit), launch all 5 agents in a SINGLE message:

```
Task(subagent_type="pr-review-toolkit:silent-failure-hunter",
     prompt="""Review error handling in src/datahub/ingestion/source/<connector>/.

<datahub-standards>
[Include relevant sections from patterns.md - error handling, logging patterns]
</datahub-standards>

Find silent failures, swallowed exceptions, missing error logging, empty catch blocks.""")

Task(subagent_type="pr-review-toolkit:pr-test-analyzer",
     prompt="""Analyze test coverage for <connector>. Check tests/unit/<connector>/ and tests/integration/<connector>/.

<datahub-standards>
[Include full content from testing.md]
</datahub-standards>

Find missing tests, trivial tests, coverage gaps, untested error paths.""")

Task(subagent_type="pr-review-toolkit:type-design-analyzer",
     prompt="""Review type design in src/datahub/ingestion/source/<connector>/.

<datahub-standards>
[Include type safety section from code_style.md and patterns.md]
</datahub-standards>

Check Pydantic models, type hints, Any usage, config classes, validators.""")

Task(subagent_type="pr-review-toolkit:code-simplifier",
     prompt="""Find complexity and refactoring opportunities in src/datahub/ingestion/source/<connector>/.

<datahub-standards>
[Include relevant sections from code_style.md, main.md and patterns.md]
</datahub-standards>

Check for DRY violations, deep nesting, overly complex functions.""")

Task(subagent_type="datahub-skills:comment-resolution-checker",
     prompt="""Check whether all previous review comments on PR #<pr_number> in <owner>/<repo> have been substantively addressed.

Verify code changes actually match what reviewers requested — don't just trust resolved checkboxes.
Distinguish between code change requests, questions, discussions, and informational comments.
Flag any threads marked resolved without corresponding code changes.""")
```

**If you cannot dispatch sub-agents**, perform these 5 checks sequentially yourself:

1. **Error handling review** — Scan all source files in `src/datahub/ingestion/source/<connector>/` for: empty `except` blocks, exceptions caught but not logged with `report.warning()` or `report.failure()`, bare `except:` clauses, `pass` in error handlers, and missing error propagation. Reference `patterns.md` error handling section.

2. **Test coverage analysis** — Examine `tests/unit/<connector>/` and `tests/integration/<connector>/`. Check: do unit tests exist and cover meaningful logic (not just imports)? Are golden files >5KB with >20 events? Do golden files contain `schemaMetadata` for datasets? Are error paths tested? Reference `testing.md`.

3. **Type design review** — Check all Pydantic models, config classes, and type hints. Look for: `Any` types without justification, missing validators on config fields, weak typing on API response models, missing `Optional` annotations. Reference `code_style.md` type safety section.

4. **Code simplification review** — Look for: DRY violations (duplicated code blocks), functions over 50 lines, deeply nested conditionals (>3 levels), overly complex list comprehensions, and opportunities to use existing DataHub utilities. Reference `code_style.md` and `patterns.md`.

5. **Comment resolution check** (for PR reviews) — Use `gh pr view <PR_NUMBER> --comments` or `gh api repos/<owner>/<repo>/pulls/<pr_number>/comments` to check whether previous review comments have been substantively addressed in the code. Don't trust resolved checkboxes — verify actual code changes match reviewer requests.

**Why this is mandatory**: Each agent catches different issues:

| Agent                                       | Catches Issues That Checklists Miss                                              |
| ------------------------------------------- | -------------------------------------------------------------------------------- |
| `pr-review-toolkit:silent-failure-hunter`   | Empty except blocks, missing report.warning(), swallowed errors                  |
| `pr-review-toolkit:pr-test-analyzer`        | Missing edge case tests, trivial golden files, untested error paths              |
| `pr-review-toolkit:type-design-analyzer`    | `Any` types without justification, weak Pydantic config models                   |
| `pr-review-toolkit:code-simplifier`         | Duplicated code, unnecessary complexity                                          |
| `datahub-skills:comment-resolution-checker` | Review comments marked resolved but not actually addressed, unaddressed feedback |

**Step 4: Apply systematic review checklist** (see Systematic Review section below)

**Step 5: Aggregate all findings** into unified report using template: `templates/full-review-report.md`

🛑 **NEVER declare "no issues found" based only on the checklist.** The agents find issues the checklist cannot detect.

### Full Review Checklist

```
Architecture:
[ ] Correct base class (see standards/main.md)
[ ] SDK V2 usage
[ ] Proper config structure
[ ] File organization per standards/patterns.md

Code Quality:
[ ] Passes all checks in standards/code_style.md

Testing:
[ ] Unit tests exist and meaningful
[ ] Integration tests with golden files
[ ] Golden file >5KB, >20 events (use extract_aspects.py to analyze)
[ ] Golden file has schemaMetadata for datasets (may be in MCE format)
[ ] Tests are non-trivial (standards/testing.md)
[ ] No fabricated test data

Source-Specific:
[ ] SQL: Follows standards/sql.md
[ ] API: Follows standards/api.md
[ ] Lineage: Uses SqlParsingAggregator
[ ] Containers: Proper hierarchy

Performance:
[ ] Uses generators (yield) for workunit emission
[ ] No N+1 query patterns (batch fetching per schema, not per table)
[ ] Pagination implemented for API calls
[ ] HTTP session reuse (API sources)
[ ] No unbounded in-memory collections
[ ] Scalable extraction approach (estimate: 1000 tables = X queries)

Documentation:
[ ] Config options documented
[ ] Example recipes provided
[ ] Known limitations noted
```

---

## Mode 2: Specialized Review

**Use when:** Focus on specific area (security, architecture, tests only, etc.)

### Specialized Review Types

| User Request                          | Focus Area                                      |
| ------------------------------------- | ----------------------------------------------- |
| "Review architecture"                 | Architecture Review section only                |
| "Review code quality"                 | Code Organization + Type Safety sections        |
| "Review tests" / "Check test quality" | Test Quality Review section only                |
| "Review documentation"                | Documentation Review section only               |
| "Security review"                     | Security Review section only                    |
| "Type safety review"                  | Type Safety Review section only                 |
| "Check for blockers only"             | All sections, but report only 🔴 BLOCKER issues |

### Workflow

1. **Identify focus area** from user request
2. **Apply only relevant section(s)** from Systematic Review
3. **Generate Specialized Review Report** (focused on requested area)

### Example: Architecture-Only Review

```markdown
## Architecture Review: [Connector Name]

**Focus:** Architecture and design patterns only

### Findings

[Architecture-specific findings only]

### Checklist

[ ] Correct base class
[ ] Proper separation of concerns
[ ] No circular dependencies
[ ] SOLID principles followed
```

---

## Mode 3: Incremental Review

**Use when:** PR with additional feature, bugfix, small changes

### Workflow

**Step 1: Get changed files:**

```bash
# For PR
gh pr diff <PR_NUMBER> --name-only

# For local changes
git diff --name-only main
```

**Step 2: 🔴 MANDATORY - Deep analysis of changed files (agents or manual)**

**Read the relevant standards files:**

```
Read standards/patterns.md
Read standards/testing.md
```

**If you can dispatch sub-agents** (Claude Code with pr-review-toolkit), launch agents focused on the changed files:

```
Task(subagent_type="pr-review-toolkit:silent-failure-hunter",
     prompt="""Review error handling in these changed files: <list_changed_source_files>.

<datahub-standards>
[Include relevant sections from patterns.md]
</datahub-standards>

Find silent failures, swallowed exceptions.""")

Task(subagent_type="pr-review-toolkit:pr-test-analyzer",
     prompt="""Analyze test coverage for changes in: <list_changed_files>.

<datahub-standards>
[Include content from testing.md]
</datahub-standards>

Check if new code paths have tests, find coverage gaps.""")

Task(subagent_type="pr-review-toolkit:type-design-analyzer",
     prompt="""Review type design in changed files: <list_changed_source_files>.

<datahub-standards>
[Include type safety section from code_style.md and patterns.md]
</datahub-standards>

Check type hints, Any usage, Pydantic models.""")

Task(subagent_type="pr-review-toolkit:code-simplifier",
     prompt="""Find complexity in changed files: <list_changed_source_files>.

<datahub-standards>
[Include relevant sections from code_style.md and patterns.md]
</datahub-standards>

Check for DRY violations, unnecessary complexity.""")

Task(subagent_type="datahub-skills:comment-resolution-checker",
     prompt="""Check whether all previous review comments on PR #<pr_number> in <owner>/<repo> have been substantively addressed.

Verify code changes actually match what reviewers requested — don't just trust resolved checkboxes.
Distinguish between code change requests, questions, discussions, and informational comments.
Flag any threads marked resolved without corresponding code changes.""")
```

**If you cannot dispatch sub-agents**, perform these checks yourself on the changed files only:

1. **Error handling** — In the changed source files, check for: empty `except` blocks, swallowed exceptions, missing `report.warning()`/`report.failure()` calls. Reference `patterns.md`.
2. **Test coverage** — For each changed source file, verify corresponding tests exist and cover the changed logic. Check golden file completeness per `testing.md`.
3. **Type design** — In changed files, check Pydantic models, type hints, `Any` usage, config validators.
4. **Code simplification** — Look for DRY violations, unnecessary complexity, and deep nesting in the diff.
5. **Comment resolution** — Use `gh` CLI to review PR comments and verify they've been addressed in the code.

**Step 3: Categorize changes and apply relevant review sections:**

- Source files changed → Architecture + Code Organization + Type Safety
- Test files changed → Test Quality Review
- Doc files changed → Documentation Review
- Config files changed → Code Organization

**Step 4: Focus review on:**

- Changed files primarily
- Impact on existing functionality
- Backward compatibility
- Regression risk

**Step 5: Generate Incremental Review Report**

### Incremental Review Checklist

```
Change Assessment:
[ ] Scope of changes understood
[ ] Breaking changes identified (if any)
[ ] Backward compatibility maintained

For Bug Fixes:
[ ] Root cause identified
[ ] Fix addresses root cause
[ ] Regression test added
[ ] No unrelated changes

For New Features:
[ ] Feature aligns with existing patterns
[ ] Tests cover new functionality
[ ] Documentation updated
[ ] Config changes are additive

General:
[ ] Existing tests still pass
[ ] No new type errors introduced
[ ] Code quality maintained or improved
```

---

## Systematic Review (All Modes)

Apply these checks based on connector type. Reference standards files for details.

### Architecture Review

**Detailed procedures in `references/architecture-review.md`**

Quick checklist:

- [ ] Correct base class for source type (see `standards/main.md`)
- [ ] SDK V2 usage throughout
- [ ] Separate config, client, source classes
- [ ] No circular dependencies
- [ ] Clear data flow: config -> client -> extraction -> emission

Use context gathering script: `./scripts/gather-connector-context.sh <connector>`

---

### Code Organization Review

Check against `standards/patterns.md`:

- [ ] File organization matches standards
- [ ] Proper imports and dependencies
- [ ] Config classes in separate file
- [ ] No circular dependencies

---

### Python Code Quality Review

**Detailed procedures in `references/python-quality-review.md`**

Check against `standards/code_style.md`.

---

### Type Safety Review

Check against `standards/code_style.md` type safety section.

### Source-Type Specific Review

**For SQL sources** (check `standards/sql.md`):

- [ ] Proper SQLAlchemy usage
- [ ] Query patterns follow standards
- [ ] Schema introspection approach
- [ ] Connection handling

**For API sources** (check `standards/api.md`):

- [ ] Separate API client class
- [ ] Pydantic models for responses
- [ ] Error handling and retries
- [ ] Pagination handling

### Lineage Review (if applicable)

Check against `standards/lineage.md`:

- [ ] Uses SqlParsingAggregator (not custom parsing)
- [ ] Proper lineage entity construction
- [ ] Column-level lineage (if supported)

### Container Review (if applicable)

Check against `standards/containers.md`:

- [ ] Correct container hierarchy
- [ ] Proper parent-child relationships
- [ ] Correct subtypes (Database, Schema, etc.)

---

### Performance & Scalability Review

**Detailed procedures in `references/performance-review.md`**

Quick checklist:

- [ ] Uses generators (`yield`) for workunit emission
- [ ] No N+1 query patterns (batch per schema, not per table)
- [ ] HTTP session reuse (API sources)
- [ ] Pagination implemented for large results
- [ ] No unbounded in-memory collections

Key question: "How many API calls/queries for 1,000 tables?"

---

### Test Quality Review

Check against `standards/testing.md`:

- [ ] Unit tests exist and are meaningful
- [ ] Integration tests with golden files
- [ ] Golden file is non-trivial (>5KB, >20 events)
- [ ] Tests are NOT trivial (see anti-patterns)
- [ ] No fabricated test data

**Use `extract_aspects.py` to analyze golden files:**

```bash
python ./scripts/extract_aspects.py <golden_file.json>
```

Verify the golden file contains expected aspects:

- [ ] `schemaMetadata` present for all datasets (may be in MCE/proposedSnapshot format)
- [ ] `container` aspect linking datasets to parent containers
- [ ] `subTypes` distinguishing Tables from Views
- [ ] `upstreamLineage` for views (if lineage is implemented)
- [ ] `viewProperties` with view definitions (for views)

### Security Review

- [ ] No hardcoded credentials
- [ ] No secrets in test files (except Docker test containers)
- [ ] Proper credential handling
- [ ] No SQL injection vulnerabilities

### Documentation Review

- [ ] Docstrings on public classes/methods
- [ ] Config options documented
- [ ] Example recipes provided

---

## Report Templates

Report templates are in the `templates/` directory.

**How to use:**

1. Read the appropriate template
2. Replace all `{{PLACEHOLDER}}` values with actual findings
3. Output the completed report to the user

### Available Templates

| Template           | File                                                                        | Use Case                               |
| ------------------ | --------------------------------------------------------------------------- | -------------------------------------- |
| Full Review        | `skills/datahub-connector-pr-review/templates/full-review-report.md`        | New connector, comprehensive audit     |
| Incremental Review | `skills/datahub-connector-pr-review/templates/incremental-review-report.md` | PR changes, bug fixes                  |
| Specialized Review | `skills/datahub-connector-pr-review/templates/specialized-review-report.md` | Focused review (tests, security, etc.) |

### Quick Reference

**Full Review Report** includes:

- Summary table with status per category
- Critical issues (blockers)
- Important issues (should fix)
- Suggestions (nice to have)
- Quality score (X/10)
- Verdict: APPROVED / NEEDS CHANGES / BLOCKED

**Incremental Review Report** includes:

- Change summary
- Impact assessment (breaking changes, regression risk)
- Change-specific checklist
- Verdict: APPROVED / NEEDS CHANGES

**Specialized Review Report** includes:

- Focus area identification
- Area-specific checklist
- Targeted findings and recommendations

---

## Utility Scripts

This skill includes utility scripts in `scripts/` directory:

**`gather-connector-context.sh`** - Comprehensive connector information:

```bash
./scripts/gather-connector-context.sh <connector> [datahub_repo_path]
```

- File structure and sizes
- Base class identification
- Key imports and dependencies
- Config structure
- Test locations and golden files
- Lineage implementation detection
- **Golden file aspect analysis** (via extract_aspects.py)

**`extract_aspects.py`** - Golden file aspect extraction and analysis:

```bash
# Summary of all aspects in a golden file
python ./scripts/extract_aspects.py <golden_file.json>

# Check if specific aspect exists (e.g., schemaMetadata)
python ./scripts/extract_aspects.py golden.json --aspect schemaMetadata

# Filter by entity type
python ./scripts/extract_aspects.py golden.json --entity-type dataset

# Show aspect data as JSON
python ./scripts/extract_aspects.py golden.json --aspect schemaMetadata --show-data --json

# Machine-readable summary (for scripts)
python ./scripts/extract_aspects.py golden.json --summary-json
```

**Supports both formats:**

- **MCP format** (newer): `aspectName` + `aspect.json` at top level
- **MCE format** (older): `proposedSnapshot` with nested aspects array

**Output includes:**

- Entity type breakdown (dataset, container, query, etc.)
- Aspect counts per entity type
- Dataset aspect checklist (schemaMetadata, container, subTypes, lineage, etc.)

**Use this script to verify golden files contain expected aspects** - especially `schemaMetadata` which may be embedded in MCE snapshots rather than MCP format.

---

## Severity Levels

Use consistent severity in findings:

| Level             | Meaning                               | Action     |
| ----------------- | ------------------------------------- | ---------- |
| 🔴 **BLOCKER**    | Violates standards, will cause issues | Must fix   |
| 🟡 **WARNING**    | Significant issue, should address     | Should fix |
| ℹ️ **SUGGESTION** | Would improve quality                 | Optional   |

---

## Standards Reference

All standards are in the `standards/` directory. Key files:

- `main.md` - Base classes, SDK V2, config patterns
- `code_style.md` - Python code quality, type safety, naming conventions
- `patterns.md` - File organization, connector-specific patterns
- `testing.md` - Test requirements, golden files
- `sql.md` / `api.md` - Source-type specific patterns
- `lineage.md` - SqlParsingAggregator usage

---

## Remember

1. **Match review mode to context** - Full for new/major, Specialized for focus, Incremental for PRs
2. **Be specific** - Cite file:line, reference exact standard section
3. **Be actionable** - Every issue should have a clear fix
4. **Be fair** - Acknowledge good work, not just problems
5. **Reference, don't duplicate** - Point to standards, don't copy them

---

## Specialized Agent Architecture

> **Note for non-Claude-Code agents:** This section describes the Claude Code multi-agent dispatch system. If your agent does not support `Task(subagent_type=...)`, skip this section — use the sequential fallback checks described in Mode 1 Step 3 and Mode 3 Step 2 above instead.

This skill uses **pr-review-toolkit** agents with DataHub-specific context injected via prompts. This approach avoids duplicating agents while providing domain expertise.

### Available Agents

| Agent (subagent_type)                       | Focus                        | Output                           |
| ------------------------------------------- | ---------------------------- | -------------------------------- |
| `pr-review-toolkit:silent-failure-hunter`   | Error handling, logging gaps | Confidence scores (0-100)        |
| `pr-review-toolkit:pr-test-analyzer`        | Test coverage, trivial tests | Priority scores (1-10)           |
| `pr-review-toolkit:type-design-analyzer`    | Pydantic models, type safety | Dimension scores (1-10 x4)       |
| `pr-review-toolkit:code-simplifier`         | Complexity, refactoring      | Complexity metrics               |
| `datahub-skills:comment-resolution-checker` | Review comment resolution    | Addressed/Unaddressed/Suspicious |

### When to Use Agents

| Scenario                | Recommended Agents                              |
| ----------------------- | ----------------------------------------------- |
| PR Review               | All agents in parallel                          |
| Re-review readiness     | comment-resolution-checker (+ others as needed) |
| Error handling concerns | pr-review-toolkit:silent-failure-hunter         |
| Test quality audit      | pr-review-toolkit:pr-test-analyzer              |
| Config/model review     | pr-review-toolkit:type-design-analyzer          |
| Code cleanup            | pr-review-toolkit:code-simplifier               |
| Quick pre-merge check   | silent-failure-hunter + pr-test-analyzer        |

### Agent Execution Modes

**Parallel Mode (default):** Launch all agents simultaneously for faster results. Use when agents don't need to share context.

**Sequential Mode:** Run agents one at a time. Use when you want findings from one agent to inform another (e.g., silent-failure-hunter finds error paths → test-analyzer checks if they're tested).

### Launching Agents with DataHub Context

**IMPORTANT:** Always include DataHub standards as context when invoking pr-review-toolkit agents.

**Before launching agents:**

1. Read the relevant standards files from `standards/`
2. Include the standards content in the agent prompt

### Standards to Include Per Agent

| Agent                        | Standards Files to Include                                                        |
| ---------------------------- | --------------------------------------------------------------------------------- |
| `silent-failure-hunter`      | `patterns.md` (error handling section)                                            |
| `pr-test-analyzer`           | `testing.md`                                                                      |
| `type-design-analyzer`       | `code_style.md` (type safety section), `patterns.md`, `api.md` (Pydantic section) |
| `code-simplifier`            | `code_style.md` (code quality rules), `patterns.md`, `main.md` (SDK patterns)     |
| `comment-resolution-checker` | None (self-contained — uses GitHub API data, not standards files)                 |

### Example: Launching with Standards Context

```
# Step 1: Read relevant standards
Read standards/testing.md

# Step 2: Launch agent with standards content
Task(subagent_type="pr-review-toolkit:pr-test-analyzer",
     prompt="""Analyze test coverage for postgres connector.

**Apply these DataHub connector testing standards:**

<standards>
[Paste content from testing.md here]
</standards>

**Files to analyze:**
- tests/unit/postgres/
- tests/integration/postgres/

Find missing tests, trivial tests, coverage gaps, untested error paths.""")
```

### Parallel Launch Pattern

For full reviews, read all needed standards first, then launch agents in parallel:

```
# 1. Read all standards upfront
patterns_content = Read(standards/patterns.md)
testing_content = Read(standards/testing.md)
main_content = Read(standards/main.md)
code_style_content = Read(standards/code_style.md)

# 2. Launch all agents with standards context (single message, parallel execution)
Task(subagent_type="pr-review-toolkit:silent-failure-hunter",
     prompt=f"""Review error handling in src/datahub/ingestion/source/<connector>/

<datahub-standards>
{patterns_content}
</datahub-standards>

Find silent failures, swallowed exceptions, missing error logging.""")

Task(subagent_type="pr-review-toolkit:pr-test-analyzer",
     prompt=f"""Analyze test coverage for <connector>.

<datahub-standards>
{testing_content}
</datahub-standards>

Check tests/unit/<connector>/ and tests/integration/<connector>/.""")

Task(subagent_type="pr-review-toolkit:type-design-analyzer",
     prompt=f"""Review type design in src/datahub/ingestion/source/<connector>/

<datahub-standards>
{code_style_content}
{patterns_content}
</datahub-standards>

Check Pydantic models, type hints, config classes.""")

Task(subagent_type="pr-review-toolkit:code-simplifier",
     prompt=f"""Find complexity in src/datahub/ingestion/source/<connector>/

<datahub-standards>
{code_style_content}
{main_content}
{patterns_content}
</datahub-standards>

Check for DRY violations, unnecessary complexity.""")

Task(subagent_type="datahub-skills:comment-resolution-checker",
     prompt="""Check whether all previous review comments on PR #<pr_number> in <owner>/<repo>
have been substantively addressed. Verify code changes match what reviewers requested.""")
```

---

## Confidence Scoring System

All findings use a confidence scoring system to reduce false positives and prioritize issues.

### Confidence Score Interpretation

| Score      | Meaning           | Action              | Report?                       |
| ---------- | ----------------- | ------------------- | ----------------------------- |
| **90-100** | Definite issue    | Must fix            | Yes, as 🔴 CRITICAL           |
| **80-89**  | Very likely issue | Should fix          | Yes, as 🟡 HIGH               |
| **70-79**  | Probably an issue | Consider fixing     | Yes, as 🟠 MEDIUM             |
| **60-69**  | Possible issue    | Optional            | Yes, as ℹ️ SUGGESTION         |
| **<60**    | Uncertain         | Investigate if time | No (too many false positives) |

### Priority Score Alignment (Test Analyzer)

Test gaps use priority scores (1-10) mapped to severity:

| Priority | Severity    | Description                               |
| -------- | ----------- | ----------------------------------------- |
| **9-10** | 🔴 Critical | Data loss, security, system failure risks |
| **7-8**  | 🟡 High     | Business logic bugs, user-facing errors   |
| **5-6**  | 🟠 Medium   | Edge cases, minor issues                  |
| **3-4**  | ⚪ Low      | Completeness improvements                 |
| **1-2**  | Optional    | Nice to have                              |

### Type Design Scores (Type Analyzer)

Types are scored on 4 dimensions (1-10 each):

1. **Encapsulation** - Are internals hidden?
2. **Invariant Expression** - Are constraints in types vs comments?
3. **Usefulness** - Do types prevent real bugs?
4. **Enforcement** - Are invariants validated?

**Overall type quality:**

- All dimensions ≥8 → Good
- Any dimension <5 → Critical issue
- Average <7 → Needs improvement

---

## Comprehensive Review Command

For the most thorough analysis, use the comprehensive review command:

```
/comprehensive-review <connector> [mode] [--agents=list]
```

### Examples

```bash
# Full parallel review of postgres connector
/comprehensive-review postgres

# Sequential review for deeper analysis
/comprehensive-review snowflake sequential

# Only check error handling and tests
/comprehensive-review --agents=silent-failures,tests

# Review current PR changes
/comprehensive-review
```

### Comprehensive Review Output

The comprehensive review produces a unified report with:

- Executive summary table
- Critical issues from all agents
- High priority issues
- Medium priority suggestions
- Positive observations
- Detailed individual agent reports (collapsible)

---

## Agent-Enhanced Workflow

### For PR Reviews (Recommended)

1. **Get changed files:**

   ```bash
   git diff --name-only main
   ```

2. **Launch comprehensive review:**

   ```
   /comprehensive-review
   ```

   OR launch agents manually in parallel

3. **Aggregate findings** into unified report

4. **Prioritize fixes:**
   - 🔴 Critical (90%+ confidence, priority 9-10) → Must fix
   - 🟡 High (80%+ confidence, priority 7-8) → Should fix
   - 🟠 Medium → Consider for follow-up

### For Full Connector Audit

1. **Gather context:**

   ```bash
   ./scripts/gather-connector-context.sh <connector>
   ```

2. **Run systematic review** (existing sections above)

3. **Launch specialized agents** for deep analysis

4. **Combine reports** into comprehensive assessment

---

## Quick Commands

| User Says                              | Mode            | Action                                                       |
| -------------------------------------- | --------------- | ------------------------------------------------------------ |
| "Review connector X"                   | Full            | Full systematic review                                       |
| "Full review of X" / "Audit X"         | Full            | Full review of connector X                                   |
| "Deep review" / "Comprehensive review" | Full + Agents   | Launch all 4 agents in parallel                              |
| "Review architecture of X"             | Specialized     | Architecture section only                                    |
| "Check tests for X"                    | Specialized     | Test quality section only                                    |
| "Review PR #123"                       | Incremental     | Changed files in PR                                          |
| "Review my changes"                    | Incremental     | Uncommitted changes                                          |
| "Quick review" / "Blockers only"       | Full (filtered) | All sections, blockers only                                  |
| "Check for silent failures"            | Agent           | Run pr-review-toolkit:silent-failure-hunter with patterns.md |
| "Analyze test coverage"                | Agent           | Run pr-review-toolkit:pr-test-analyzer with testing.md       |
| "Review types/models"                  | Agent           | Run pr-review-toolkit:type-design-analyzer with patterns.md  |
| "Simplify code"                        | Agent           | Run pr-review-toolkit:code-simplifier with patterns.md       |
| "Check if comments addressed"          | Agent           | Run datahub-skills:comment-resolution-checker                |
| "Quick PR check"                       | Agent           | silent-failure-hunter + pr-test-analyzer                     |

---

## Integration with Existing Review

The pr-review-toolkit agents **complement** the systematic review sections:

| Systematic Section  | Enhanced By Agent          | Standards to Pass                   |
| ------------------- | -------------------------- | ----------------------------------- |
| Test Quality Review | pr-test-analyzer           | testing.md                          |
| Python Code Quality | code-simplifier            | code_style.md, patterns.md, main.md |
| Type Safety Review  | type-design-analyzer       | code_style.md, patterns.md          |
| Security Review     | silent-failure-hunter      | patterns.md                         |
| Re-review Readiness | comment-resolution-checker | N/A (GitHub API-based)              |

**Best practice:** Run systematic review first for structure, then agents for deep dives into problem areas. Always pass relevant standards as context.
