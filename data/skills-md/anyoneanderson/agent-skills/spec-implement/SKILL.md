---
name: spec-implement
description: |
  Specification-driven implementation — Execute implementation from specs to PR.

  Reads issue-to-pr-workflow.md as playbook, enforces coding-rules.md as quality gates,
  tracks progress via tasks.md checkboxes with resume capability.

  English triggers: "Implement from spec", "Start implementation", "Execute spec tasks"
  日本語トリガー: 「仕様書から実装」「実装を開始」「specタスクを実行」
license: MIT
---

# spec-implement — Spec-Driven Implementation to PR

Execute implementation from specifications to pull request, following project-specific workflows and enforcing coding rules.

## Language Rules

1. **Auto-detect input language** → output in the same language
2. Japanese input → Japanese output, use `references/implement-guide.ja.md`
3. English input → English output, use `references/implement-guide.md`
4. Explicit override takes priority (e.g., "in English", "日本語で")

## Critical First Steps

**BEFORE any implementation, execute these checks in order:**

1. **Verify environment**:
   - Run `pwd` to confirm working directory
   - Run `git status` to confirm inside a git repository
   - Run `gh auth status` to confirm GitHub CLI access

2. **Parse user input for options**:
   - `--resume` → resume from last uncompleted task
   - `--issue {N}` → specify GitHub Issue number
   - `--spec {path}` → specify `.specs/` directory path
   - `--dry-run` → show execution plan without making changes
   - `--parallel` → force parallel execution if environment is ready
   - `--no-parallel` → force sequential execution

3. **Locate spec directory**:
   - If `--spec` provided → use that path
   - If issue body contains `.specs/` path → use that
   - Otherwise → scan `.specs/` and ask user to select:
     ```
     AskUserQuestion:
       question: "Which spec to implement?" / "どの仕様書を実装しますか？"
       options: [list discovered .specs/ directories]
     ```

4. **Locate and read project files** (in this order):

   **Workflow playbook** — search in order, use first found:
   1. `docs/development/issue-to-pr-workflow.md`
   2. `docs/issue-to-pr-workflow.md`
   3. Fallback: `find . -name "issue-to-pr-workflow.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" -not -path "*/dist/*" -not -path "*/build/*" | head -1`
   4. If not found → trigger fallback (see Phase 1)

   **Coding rules** — search in order, use first found:
   1. `docs/development/coding-rules.md`
   2. `docs/coding-rules.md`
   3. Fallback: `find . -name "coding-rules.md" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/vendor/*" -not -path "*/dist/*" -not -path "*/build/*" | head -1`
   4. If not found → trigger fallback (see Phase 2)

   **Project instruction files** — read all that exist:
   - `CLAUDE.md` (project root)
   - `src/CLAUDE.md` (source-level rules)
   - `test/CLAUDE.md` (test-level rules)
   - `AGENTS.md` (agent definitions)

   **Spec files**:
   - `.specs/{feature}/requirement.md` → what to build
   - `.specs/{feature}/design.md` → how to build it
   - `.specs/{feature}/tasks.md` → task breakdown with checkboxes

5. **Detect parallel-capable agent environment (runtime-aware)**:
   - Determine active runtime from the current execution environment (do NOT infer runtime solely from repository directories)
   - Use repository files only for runtime setup validation:
     - Codex validation: `.codex/config.toml`
     - Claude Code validation: `.claude/agents/workflow-*.md`
   - If runtime cannot be determined, ask user to choose runtime
   - Check whether workflow contains a parallel section (`Parallel Execution Strategy` / `Agent Roles`)
   - Parse optional workflow section for explicit agent file paths:
     - `Agent definition files:` / `エージェント定義ファイル:`
     - Extract paths for implementer / reviewer / tester from list items
     - Use extracted paths as first priority for validation and dispatch context
     - If section is absent, fallback to runtime defaults
   - Validate runtime-specific sub-agent setup:
     - Codex: `.codex/config.toml` has `[features] multi_agent = true` and `agents.workflow-*`
     - Claude Code: agent files from workflow section exist; if absent, use defaults (`.claude/agents/workflow-implementer.md`, `.claude/agents/workflow-reviewer.md`, `.claude/agents/workflow-tester.md`)
   - If any required condition is missing, continue in sequential mode

## Execution Flow

### Phase 1: Workflow Loading

Read the workflow file (located in Step 4) and interpret each section as instructions to follow:

| Workflow Section | Action |
|-----------------|--------|
| Development Environment | Extract setup commands, environment variables |
| Issue Analysis and Setup | Follow branch naming convention, issue reading steps |
| Branch Strategy / PR Target | **Extract base branch** (e.g., `develop`, `main`) and PR target branch |
| Phased Implementation | Follow implementation order and guidelines |
| Agent Roles / Sub-agents | Extract agent role definitions (if present) |
| Agent Definition Files (Optional) | Extract explicit sub-agent definition file paths |
| Testing | Extract test commands and coverage thresholds |
| PR Creation and Quality Gates | Extract pre-PR checks and PR template |
| CI/CD Monitoring | Extract CI verification commands |
| Commit Message Rules | Extract commit message format and language requirements |

**Follow sections top-to-bottom.** Replace `{variable}` placeholders with actual values (issue number, branch name, etc.). Treat "MUST" and "required" keywords as mandatory; treat "optional" and "if applicable" as conditional.

**Base branch detection** — determine `{base_branch}` from the workflow:
1. Look for "branch strategy", "base branch", "PR target", "develop", "main" in the workflow
2. If the workflow specifies a branch (e.g., `develop`), use it as `{base_branch}`
3. Default fallback: `main`

**Fallback (no workflow file):**
If no workflow file is found:
```
AskUserQuestion:
  question: "Workflow file not found. Generate it?" / "ワークフローファイルが見つかりません。生成しますか？"
  options:
    - "Run spec-workflow-init" / "spec-workflow-initを実行"
    - "Continue without workflow" / "ワークフローなしで続行"
```
If continuing without workflow, use minimal flow: Issue analysis → branch → implement → test → PR. Use `main` as `{base_branch}`.

### Phase 1.5: Parallel Mode Resolution (Runtime-Aware)

Enable parallel mode only when ALL are true:

1. Workflow includes a parallel section with role assignment
2. Runtime-specific sub-agent configuration is valid
3. User did not pass `--no-parallel` (or explicitly passed `--parallel`)

If runtime cannot be determined from execution context, confirm runtime before dispatch:
```
AskUserQuestion:
  question: "Which runtime should execute sub-agents?" / "どのランタイムでサブエージェント実行しますか？"
  options:
    - "Codex runtime" / "Codexで実行"
    - "Claude Code runtime" / "Claude Codeで実行"
```

If enabled:
- Run implementer and tester in parallel, then run reviewer after both complete.
- Use explicit runtime-specific dispatch instructions, not narrative role assignment only.

Codex path:
- Required config: `.codex/config.toml` with `multi_agent = true` and `agents.workflow-*`
- Agent definition file paths:
  - First priority: paths declared in workflow `Agent definition files` section
  - Fallback: runtime defaults (from `.codex/agents/` conventions)
- Dispatch format (example):
```text
Task:
  subagent_type: workflow-implementer
  prompt: "Implement task T001 using design section 2.3. Edit implementation files only."

Task:
  subagent_type: workflow-tester
  prompt: "Create tests for task T001. Edit test files only."
```

Claude Code path:
- Required files:
  - First priority: paths declared in workflow `Agent definition files` section
  - Fallback defaults: `.claude/agents/workflow-implementer.md`, `.claude/agents/workflow-reviewer.md`, `.claude/agents/workflow-tester.md`
- Dispatch format: use Claude Code sub-agent call format with `subagent_type` set to workflow agent names (`workflow-implementer`, `workflow-tester`, `workflow-reviewer`).
- Example (pseudocode):
```text
SubAgent:
  subagent_type: workflow-implementer
  prompt: "Implement task T001 using design section 2.3. Edit implementation files only."
```

If disabled:
- Continue with the existing single-agent sequential loop.

### Phase 2: Quality Rules Loading

Read the coding rules file (located in Step 4) and parse rule structure:

```
## {Category}
### [{Severity}] {Rule Name}
- {Rule detail}
```

Apply rules by severity:

| Severity | On Violation | Action |
|----------|-------------|--------|
| `[MUST]` | Error | Stop → fix → recheck before continuing |
| `[SHOULD]` | Warning | Log warning → continue |
| `[MAY]` | Info | Log info only |

**Check timing:**
- **Before task**: Review rules relevant to the task's category
- **During code generation**: Self-check against `[MUST]` rules
- **After task**: Verify completion criteria + rule compliance
- **Final gate**: Check all `[MUST]` rules across all changes

**Fallback (no rules file):**
If no coding rules file is found:
```
AskUserQuestion:
  question: "Coding rules not found. Generate them?" / "コーディングルールが見つかりません。生成しますか？"
  options:
    - "Run spec-rules-init" / "spec-rules-initを実行"
    - "Continue without rules" / "ルールなしで続行"
```
If continuing without rules, use CLAUDE.md or AGENTS.md as fallback reference if available.

### Phase 3: Project Instruction Loading

Read all project instruction files found in Step 4 (`CLAUDE.md`, `src/CLAUDE.md`, `test/CLAUDE.md`, `AGENTS.md`).

These files contain project-specific conditional rules, environment constraints, and coding conventions. Apply them with the same enforcement level as `[MUST]` rules from coding-rules.md:

- **Extract conditional rules**: IF-THEN patterns, conditional instructions, and environment-specific constraints (e.g., "when using Docker...", "if the project has...") are mandatory action triggers
- **Extract environment constraints**: Docker requirements, package manager restrictions, etc.
- **Extract commit conventions**: Commit message language, format, co-author requirements
- **Extract test patterns**: Required test helpers, test structure conventions
- **Merge with coding-rules.md**: These rules supplement (not replace) coding-rules.md

If neither coding-rules.md nor any CLAUDE.md files exist, proceed with framework defaults only.

### Phase 4: Issue Analysis

If `--issue {N}` is provided or an issue number is found in context:
```bash
gh issue view {N} --json title,body,labels,assignees
```

Extract from the issue:
- Feature overview and requirements
- Spec directory path (if referenced)
- Phase/task checklists
- Assignees and labels

### Phase 5: Branch Creation

> **🚨 BLOCKING GATE — Feature branch is MANDATORY**
>
> Implementation MUST NOT proceed on `main`, `master`, or `develop` branches.
> This gate cannot be skipped. Violation = immediate stop.

Follow the workflow's branch naming convention:
```bash
git checkout {base_branch} && git pull origin {base_branch}
git checkout -b feature/issue-{N}-{brief-description}
```

Where `{base_branch}` is the branch detected in Phase 1 (default: `main`).

**Protected branch list** — by default: `main`, `master`, `develop`.
If the workflow file defines a "protected branches" or "branch protection" section, use that list instead.

If `--resume` is active and the branch already exists, switch to it instead.

**Post-creation verification:**
```bash
current_branch=$(git branch --show-current)
if [ "$current_branch" = "main" ] || [ "$current_branch" = "master" ] || [ "$current_branch" = "develop" ]; then
  echo "🚨 ERROR: Cannot implement on protected branch: $current_branch"
  echo "Create a feature branch first."
  exit 1
fi
```

This check MUST pass before proceeding to Phase 6. If it fails, stop and ask the user for guidance.

### Phase 6: Spec-Driven Task Loop

**Pre-loop: Agent role detection**

If the workflow file contains an "Agent Roles", "Sub-agents", or "エージェントロール" section:

0. **Parse explicit agent file paths** (if present):
   - Read workflow section `Agent definition files:` / `エージェント定義ファイル:`
   - Build a map of role → definition file path (implementer/reviewer/tester)
   - If no section exists, use runtime defaults

1. **Parse the Role Assignment Table** — find the Markdown table with columns like `Role | Agent | Responsibility`:
   - Extract each row's `Agent` column value → use as runtime sub-agent identifier (`subagent_type`)
   - Extract each row's `Responsibility` column value → use as context in the task prompt
2. **Parse the Parallel Execution Strategy Table** (if present) — find the table with phase rows and role columns:
   - Each row = a phase (execute sequentially, top to bottom)
   - Cells with `-` = role is idle in that phase
   - Non-`-` cells = role's action (roles active in the same row run in parallel)
3. Present options to the user:
   ```
   AskUserQuestion:
     question: "Workflow defines agent roles. Use sub-agents for parallel execution?" /
               "ワークフローにエージェントロールが定義されています。サブエージェントで並列実行しますか？"
     options:
       - "Use sub-agents (parallel)" / "サブエージェント使用（並列）"
       - "Single agent (sequential)" / "シングルエージェント（順次）"
   ```
4. If sub-agents selected, branch by runtime:
   - Codex runtime: spawn agents via Codex Task dispatch using parsed `Agent` names as `subagent_type`
   - Claude Code runtime: spawn agents via Claude Code sub-agent dispatch using parsed `Agent` names as `subagent_type`
   - Execute phases per strategy table (same-row roles run in parallel)
5. If single agent selected: proceed with sequential execution below

See reference guide for table format examples and runtime-specific sub-agent invocation patterns.

**Read specs in order:** `requirement.md` → `design.md` → `tasks.md`

For each unchecked task in `tasks.md`:

```
1. Read task details (requirements ID, design reference, target files, completion criteria)
2. Reference the corresponding design.md section
3. Implement: create or modify target files
4. 🔍 Implementation Review:
   a. Self-review generated code against design.md specifications
   b. Verify coding-rules.md [MUST] rules for generated code
   c. Verify CLAUDE.md conditional rules for generated code
   d. If review finds issues → fix before proceeding
5. If task includes test implementation:
   a. Write tests following project test patterns (from CLAUDE.md / coding-rules.md)
   b. Run tests to verify they pass
   c. 🔍 Test Review:
      - Verify test coverage matches completion criteria
      - Verify test patterns match project conventions
      - If review finds issues → fix before proceeding
6. Update tasks.md: mark completion criteria (- [ ] → - [x])
7. When all criteria pass: mark top-level task checkbox (- [x])
8. Commit progress:
   git add .specs/{feature}/tasks.md [+ implementation files]
   git commit -m "{commit message following project conventions}"
```

**Commit messages:** Follow format/language from coding-rules.md or CLAUDE.md. Default: `feat: {task-id} complete — {brief description}`. See reference guide for details.

**No specs fallback:** If `.specs/` is missing, use Issue body as guide and generate a simple checklist. See reference guide for details.

### Phase 7: Final Quality Gate

After all tasks are complete:

1. Run test commands from the workflow (or language-appropriate default)
2. Run lint/typecheck commands from the workflow (if specified)
3. Verify all `[MUST]` rules from coding-rules.md pass
4. Verify all CLAUDE.md conditional rules pass
5. If any check fails → fix → recheck
6. All checks pass → proceed to PR creation

### Phase 8: PR Creation

Follow the workflow's PR template. Use `{base_branch}` detected in Phase 1:

```bash
gh pr create \
  --title "{type}: {description} (closes #{N})" \
  --body "{PR body following workflow template}" \
  --base {base_branch}
```

Where `{base_branch}` comes from Phase 1 workflow detection (default: `main`).

Verify `--base {base_branch}` matches the workflow's branch strategy before creating the PR.

**Safety guards:**
- Do NOT create PR if tests are failing
- Do NOT force push
- Do NOT push directly to main/master
- Do NOT target wrong base branch (verify against workflow)
- Ask for user confirmation before large-scale code deletions

After PR creation, monitor CI status if the workflow specifies CI verification commands.

## Options

| Option | Description |
|--------|-------------|
| `--resume` | Resume from last uncompleted task in tasks.md |
| `--issue {N}` | Specify GitHub Issue number for context |
| `--spec {path}` | Specify .specs/ directory path (default: auto-detect) |
| `--dry-run` | Show execution plan without making any changes (output format: see reference guide) |
| `--parallel` | Force parallel mode (requires valid runtime sub-agent setup for Codex or Claude Code) |
| `--no-parallel` | Disable parallel mode and run sequentially |

## Error Handling

| Situation | Response |
|-----------|----------|
| Not a git repository | Error: "Must be in a git repository" / "gitリポジトリ内で実行してください" |
| `gh` CLI not available | Error: guide user to install/authenticate gh CLI |
| `.specs/` not found | Warning: switch to Issue-only minimal mode |
| Parallel requested but runtime sub-agent config missing/invalid | Warning: explain missing setup, fallback to sequential mode |
| Workflow-declared agent definition file path does not exist | Warning: explain missing file path, fallback to sequential mode |
| Workflow references sub-agent names that are not configured in selected runtime | Warning: explain missing agent definitions, fallback to sequential mode |
| Parallel file edit collision | Warning: stop parallel for current task, continue sequentially |
| `requirement.md` missing | Warning: use Issue body as requirements source |
| `tasks.md` missing | Warning: generate simple checklist from Issue |
| `[MUST]` rule violation | Error: stop, fix, recheck before continuing |
| Tests failing before PR | Block PR creation, report failures |
| Branch already exists | Ask: switch to it or create new |
| On protected branch (main/master/develop) | 🚨 BLOCKING: stop immediately, require feature branch |
| Workflow/rules file not at expected path | Search alternate paths before declaring missing |

## Usage Examples

```
# Full implementation from spec
"Implement from spec for auth-feature"
「auth-featureの仕様書から実装して」

# With issue number
"Implement spec --issue 42"
「Issue #42の仕様を実装して」

# Resume after interruption
"Resume implementation --resume --spec .specs/auth-feature/"
「実装を再開 --resume」

# Dry run to preview plan
"Show implementation plan --dry-run --spec .specs/auth-feature/"
「実装計画を表示 --dry-run」

# Force parallel mode (runtime-aware)
"Implement from spec --spec .specs/auth-feature/ --parallel"
「仕様書から並列実行で実装 --parallel」

# Minimal mode (no specs)
"Implement issue 42"
「Issue 42を実装して」
```

## Post-Completion Actions

After PR is created:

```
AskUserQuestion:
  question: "PR created. What's next?" / "PRを作成しました。次は？"
  options:
    - "Monitor CI status" / "CIステータスを監視"
    - "Review the PR diff" / "PR差分を確認"
    - "Done" / "完了"
```
