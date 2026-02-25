---
name: spec-workflow-init
description: |
  Development workflow generator — Generate issue-to-pr-workflow.md for your project.

  Creates a project-specific development workflow through interactive dialogue,
  covering branch strategy, quality gates, development style, and optional sub-agent definitions.

  English triggers: "Generate workflow", "Create development workflow", "Setup issue-to-PR flow"
  日本語トリガー: 「ワークフローを生成」「開発フローを作成」「Issue-to-PRフローを設定」
license: MIT
---

# spec-workflow-init — Development Workflow Generator

Generate a project-specific `issue-to-pr-workflow.md` through interactive dialogue. The workflow serves as a playbook for spec-implement and development agents.

## Language Rules

1. **Auto-detect input language** → output in the same language
2. Japanese input → Japanese output, use `references/workflow-template.ja.md`
3. English input → English output, use `references/workflow-template.md`
4. Explicit override takes priority (e.g., "in English", "日本語で")

**Sub-agent template selection** (when generating agent definitions):
- English → `references/agents/claude/workflow-*.md`
- Japanese → `references/agents/claude/workflow-*.ja.md`
- Codex templates: English → `references/agents/codex/workflow-*.toml`, Japanese → `references/agents/codex/workflow-*.ja.toml`

## Execution Flow

### Step 1: Initial Checks

1. **Verify Git repository**:
   ```bash
   git rev-parse --is-inside-work-tree 2>/dev/null
   ```
   If not a Git repo, warn and skip branch detection. Continue with other checks.

2. **Check current directory**:
   ```bash
   pwd
   ls -la
   ```

3. **Detect existing workflow file**:
   ```bash
   find . -name "issue-to-pr-workflow.md" -maxdepth 3 2>/dev/null
   ```
   If found and `--force` is not set, show the existing file path and proceed to Step 7 (idempotency handling).

### Step 2: Environment Detection

Run the following checks to auto-detect the project environment:

**Package manager**:
```bash
ls pnpm-lock.yaml yarn.lock package-lock.json bun.lockb 2>/dev/null
```

**Container usage**:
```bash
ls docker-compose.yml docker-compose.yaml Dockerfile 2>/dev/null
```

**CI/CD service**:
```bash
ls -d .github/workflows .gitlab-ci.yml .circleci 2>/dev/null
```

**Branch information**:
```bash
git branch -r 2>/dev/null | head -10
```

**Language, framework, and scripts**:
```bash
cat package.json 2>/dev/null | grep -A 50 '"scripts"'
cat package.json 2>/dev/null | grep -A 30 '"dependencies"'
ls go.mod requirements.txt pyproject.toml 2>/dev/null
```

**Database**:
```bash
ls prisma/schema.prisma 2>/dev/null
grep -l "postgres\|mysql\|mongo" docker-compose.yml 2>/dev/null
```

**Lint tools**:
```bash
ls .eslintrc* biome.json 2>/dev/null
```

**Coding rules file**:
```bash
find . -name "coding-rules.md" -maxdepth 3 2>/dev/null
```

**Present the detection results** to the user in a summary table:

```
Detected project environment:
  Language/FW:       {detected}
  Package Manager:   {detected}
  Container:         {detected}
  Test:              {detected}
  CI/CD:             {detected}
  Branch:            {detected}
  Database:          {detected}
  Lint:              {detected}
  Coding Rules:      {detected or "Not found"}
```

Ask the user to confirm or correct the detection results before proceeding.

### Step 3: Interactive Dialogue

Gather workflow configuration through AskUserQuestion rounds.

**Round 1: Output Path**

```
question: "Where to save issue-to-pr-workflow.md?" / "issue-to-pr-workflow.md の出力先は？"
header: "Output"
options:
  - "docs/issue-to-pr-workflow.md (Recommended)" / "docs ディレクトリ直下（推奨）"
  - "docs/development/issue-to-pr-workflow.md" / "docs/development 配下"
```

**Round 2: Branch Strategy**

```
Q1:
question: "Base branch (PR target)?" / "ベースブランチ（PRターゲット）は？"
header: "Branch"
options:
  - "develop (Recommended)" / "feature → develop → main（Git Flow）"
  - "main" / "feature → main（GitHub Flow）"
  - "trunk" / "Short-lived branches → main（Trunk-based）"

Q2:
question: "Feature branch naming convention?" / "featureブランチの命名規則は？"
header: "Naming"
options:
  - "feature/{issue}-{slug} (Recommended)" / "e.g. feature/42-add-auth"
  - "{issue}-{slug}" / "e.g. 42-add-auth"
  - "{type}/{issue}-{slug}" / "e.g. fix/42-login-bug, feat/43-dashboard"
```

**Round 3: Quality Gates**

```
question: "Quality gates before PR creation?" / "PR作成前の品質ゲートは？"
header: "Gates"
multiSelect: true
options:
  - "All tests must pass (Recommended)" / "テスト全パス（推奨）"
  - "Lint and type check must pass" / "Lint / Typecheckパス"
  - "Coverage threshold" / "カバレッジ基準"
```

**Round 4: Development Style**

```
question: "Select your development style" / "開発スタイルを選択してください"
header: "Style"
options:
  - "Implementation First (Recommended)" / "実装 → レビュー → テスト → テストレビュー → 品質ゲート → PR"
  - "TDD" / "テスト(RED) → 実装(GREEN) → リファクタ → レビュー → 品質ゲート → PR"
  - "BDD" / "E2Eシナリオ → テスト(RED) → 実装(GREEN) → レビュー → 品質ゲート → PR"
```

**Round 5: E2E Test Level**

```
question: "E2E test scope?" / "E2Eテストの範囲は？"
header: "E2E"
options:
  - "API level only (Recommended)" / "supertest等でリクエスト→レスポンスを検証"
  - "API + Browser E2E" / "上記 + Playwrightでクリティカルパスを検証"
```

**Round 6: Parallel Execution**

```
question: "Use parallel execution for implementation and tests?" / "実装とテストの並列実行を使いますか？"
header: "Parallel"
options:
  - "Sequential (Recommended)" / "メインエージェントが全工程を順番に実行（安全・シンプル）"
  - "Parallel" / "実装とテストコード生成を並行して実行（高速・要エージェント分離）"
```

**Round 7: Agent Targets (only if Parallel selected)**

Ask which agent definitions to generate. Do NOT decide targets based on `.claude/` / `.codex/` directory detection.

```
question: "Which agent definitions should be generated?" / "どのエージェント定義を生成しますか？"
header: "Agents"
options:
  - "Both Claude + Codex (Recommended)" / "Claude と Codex の両方を生成"
  - "Claude only" / "Claude のみ生成"
  - "Codex only" / "Codex のみ生成"
  - "Skip generation" / "生成しない"
```

**Additional Questions (project-type specific)**:

- **Docker project**: "Run all commands inside Docker?" / "Docker内で全コマンドを実行しますか？"
- **Next.js project**: "Include build check in workflow?" / "ビルド確認をワークフローに含めますか？"

### Step 4: Workflow Generation

1. **Select template** based on Language Rules:
   - English → `references/workflow-template.md`
   - Japanese → `references/workflow-template.ja.md`

2. **Read the template** and replace placeholders with collected values:
   - `{package_manager}`, `{container_tool}`, `{database}`, `{test_framework}`, etc.
   - `{pr_target}`, `{branch_naming}`, `{dev_style}`
   - `{test_command}`, `{lint_command}`, `{typecheck_command}`, `{build_command}`
   - `{e2e_test_command}`, `{browser_e2e_command}`, `{coverage_command}`
   - `{timestamp}` → current date/time

3. **Select development style sections**:
   - Implementation First → keep `{if_implementation_first}...{end_implementation_first}`, remove TDD/BDD blocks
   - TDD → keep `{if_tdd}...{end_tdd}`, remove others
   - BDD → keep `{if_bdd}...{end_bdd}`, remove others

4. **Handle conditional sections**:
   - Browser E2E not selected → remove `{if_browser_e2e}...{end_browser_e2e}` blocks
   - Parallel not selected → remove `{if_parallel}...{end_parallel}` blocks
   - If agent targets include Claude → keep `{if_claude_agents}...{end_claude_agents}`, otherwise remove
   - If agent targets include Codex → keep `{if_codex_agents}...{end_codex_agents}`, otherwise remove
   - If agent generation is skipped → keep `{if_no_agent_files}...{end_no_agent_files}`, otherwise remove
   - No typecheck command → remove `{if_typecheck}...{end_typecheck}`
   - No build command → remove `{if_build}...{end_build}`

5. **Clean up** remaining placeholders and conditional markers

6. **Create output directory** if needed:
   ```bash
   mkdir -p {output_directory}
   ```

7. **Write the file** to the specified output path

### Step 5: Idempotency Handling

If an existing workflow file is detected (from Step 1 or during generation):

1. **Without `--force`**: Show a warning with the existing file path
   ```
   question: "Existing workflow found at {path}. Overwrite?" / "既存のワークフローが {path} に見つかりました。上書きしますか？"
   header: "Overwrite"
   options:
     - "Yes, overwrite" / "はい、上書きする"
     - "No, cancel" / "いいえ、キャンセル"
   ```

2. **With `--force`**: Overwrite without confirmation

### Step 6: Sub-Agent Generation

**Skip this step** if the user did not select parallel execution or selected "Skip generation" in Round 7.

**Step 6a: Claude Code agents** (when Round 7 selection includes Claude):

1. Select template language based on Language Rules:
   - English → `references/agents/claude/workflow-*.md`
   - Japanese → `references/agents/claude/workflow-*.ja.md`

2. Read each template and replace placeholders:
   - `{coding_rules_path}` → detected path (e.g., `docs/coding-rules.md`)
   - `{workflow_path}` → output path from Step 3 (e.g., `docs/issue-to-pr-workflow.md`)
   - `{test_command}`, `{lint_command}`, `{typecheck_command}`, `{build_command}`
   - `{e2e_test_command}`, `{browser_e2e_command}`, `{coverage_command}`
   - `{dev_style}` → selected development style
   - `{branch_naming}` → selected naming convention

3. Create directory and write files:
   ```bash
   mkdir -p .claude/agents
   ```
   - `.claude/agents/workflow-implementer.md`
   - `.claude/agents/workflow-reviewer.md`
   - `.claude/agents/workflow-tester.md`

4. If files already exist, ask for overwrite confirmation (same as Step 5)

**Step 6b: Codex agents** (when Round 7 selection includes Codex):

1. Select template language based on Language Rules:
   - English → `references/agents/codex/workflow-*.toml`
   - Japanese → `references/agents/codex/workflow-*.ja.toml`

2. Read each TOML template and replace placeholders in `developer_instructions`:
   - Same variables as Claude Code agents

3. Create directory and write files:
   ```bash
   mkdir -p .codex/agents
   ```
   - `.codex/agents/workflow-implementer.toml`
   - `.codex/agents/workflow-reviewer.toml`
   - `.codex/agents/workflow-tester.toml`

4. Update `.codex/config.toml`:
   - Create file if it doesn't exist
   - Add or update agent sections in config.toml:
     ```toml
     [agents.workflow-implementer]
     config_file = "agents/workflow-implementer.toml"

     [agents.workflow-reviewer]
     config_file = "agents/workflow-reviewer.toml"

     [agents.workflow-tester]
     config_file = "agents/workflow-tester.toml"
     ```
   - Add `[features] multi_agent = true` if not present

5. If files already exist, ask for overwrite confirmation

### Step 7: AGENTS.md / CLAUDE.md Reference Update

1. Check for convention files:
   ```bash
   ls AGENTS.md CLAUDE.md 2>/dev/null
   ```

2. If CLAUDE.md is a symlink to AGENTS.md, update only AGENTS.md:
   ```bash
   readlink CLAUDE.md 2>/dev/null
   ```

3. If at least one file exists, ask for confirmation:
   ```
   question: "Add workflow reference to AGENTS.md / CLAUDE.md?" / "AGENTS.md / CLAUDE.md にワークフローの参照を追記しますか？"
   header: "Update"
   options:
     - "Yes, add reference (Recommended)" / "はい、参照を追記する（推奨）"
     - "No, skip" / "いいえ、スキップ"
   ```

4. If approved, append the following section (adapt language to match output):

   English:
   ```markdown
   ## Development Workflow

   Follow the development workflow for Issue → Implementation → PR:
   - [{workflow_path}]({workflow_path}) — Development workflow generated by spec-workflow-init
   ```

   Japanese:
   ```markdown
   ## Development Workflow

   開発フロー（Issue → 実装 → PR）は以下のファイルに従ってください:
   - [{workflow_path}]({workflow_path}) — spec-workflow-init で生成された開発ワークフロー
   ```

5. If neither file exists, output a warning:
   ```
   "Warning: Neither AGENTS.md nor CLAUDE.md found. Skipping reference update."
   / "警告: AGENTS.md も CLAUDE.md も見つかりません。参照追記をスキップします。"
   ```

## Options

| Option | Description |
|--------|-------------|
| `--force` | Overwrite existing files without confirmation |

## Error Handling

| Error | Detection | Response |
|-------|-----------|----------|
| Not a Git repository | `git rev-parse` fails | Warn and skip branch detection. Continue with other checks |
| No package.json | `ls package.json` fails | Skip package manager / test / lint detection. Gather via dialogue |
| Write permission error | `mkdir -p` or file write fails | Show error and re-ask output path via AskUserQuestion |
| Network error (git branch -r) | Command timeout or non-zero exit | Skip remote branches. Use local branches only. Gather via dialogue |
| Existing file conflict | File found at output path | Without `--force`: show warning and ask to overwrite. With `--force`: overwrite |

## Usage Examples

```
# Generate workflow with dialogue
"Generate development workflow"
「開発ワークフローを生成」

# Generate with force overwrite
"Create workflow --force"
「ワークフロー生成 --force」

# After spec-rules-init
"Now create the development workflow"
「次に開発フローを作って」
```

## Post-Completion Actions

After generating the workflow:

```
question: "Workflow generated. What's next?" / "ワークフローを生成しました。次のアクションは？"
options:
  - "Run spec-implement" / "spec-implement を実行する"
    description: "Start implementing with the generated workflow" / "生成したワークフローで実装を開始"
  - "Review and customize" / "レビューしてカスタマイズ"
    description: "Open the generated file and make adjustments" / "生成されたファイルを開いて調整"
  - "Done for now" / "完了"
    description: "Finish without further action" / "追加アクションなしで完了"
```
