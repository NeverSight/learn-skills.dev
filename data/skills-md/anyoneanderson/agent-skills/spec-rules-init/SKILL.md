---
name: spec-rules-init
description: |
  Coding rules generator — Extract and generate coding-rules.md from project conventions.

  Scans CLAUDE.md, AGENTS.md, config files, existing source code, and installed skills to
  produce a unified coding-rules.md that spec-implement uses as a quality gate.

  English triggers: "Generate coding rules", "Create coding-rules.md", "Extract project rules"
  日本語トリガー: 「コーディングルールを生成」「coding-rules.mdを作成」「プロジェクトルールを抽出」
license: MIT
---

# spec-rules-init — Coding Rules Generator

Extract project conventions and generate a unified `coding-rules.md` for use as a quality gate during implementation.

## Language Rules

1. **Auto-detect input language** → output in the same language
2. Japanese input → Japanese output, use `references/rules-template.ja.md`
3. English input → English output, use `references/rules-template.md`
4. Explicit override takes priority (e.g., "in English", "日本語で")

## Execution Flow

### Step 0: Initial Context Check

**BEFORE any interaction, execute these checks:**

1. **Check current directory**:
   ```bash
   pwd
   ls -la
   ```

2. **Detect convention files** (parallel where possible):
   ```bash
   # Convention files
   ls CLAUDE.md src/CLAUDE.md AGENTS.md test/CLAUDE.md 2>/dev/null
   ls -d .claude/ 2>/dev/null

   # Config files
   ls package.json go.mod requirements.txt Cargo.toml 2>/dev/null
   ls .eslintrc* biome.json tsconfig.json .prettierrc* 2>/dev/null
   ```

3. **Detect existing source code**:
   ```bash
   find . -maxdepth 3 -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.java" -o -name "*.rs" \) 2>/dev/null | head -30
   ```

4. **Scan installed skills**:
   ```bash
   ls ~/.claude/skills/*/SKILL.md .claude/skills/*/SKILL.md 2>/dev/null
   ```

5. **Check for existing coding-rules.md**:
   ```bash
   find . -name "coding-rules.md" -type f 2>/dev/null
   ```

### Step 1: Rule Extraction from Convention Files

Read detected convention files and extract rules by category.

**Detection targets** (by priority):

| File | Content to Extract | Priority |
|------|-------------------|----------|
| `CLAUDE.md` (root) | Project-wide rules | High |
| `src/CLAUDE.md` | Source-specific rules | High |
| `AGENTS.md` | Agent-oriented rules | High |
| `.claude/` contents | Project settings | Medium |
| `package.json` | lint/test script presence | Medium |
| `test/CLAUDE.md` | Test-specific rules | Medium |
| `.eslintrc*` / `biome.json` | Lint rules | Low |
| `tsconfig.json` | TypeScript strict settings | Low |
| `.prettierrc*` | Format settings | Low |

**Extraction categories and keywords**:

- **Testing Standards**: "coverage", "test", "spec", "E2E", "カバレッジ", "テスト"
- **Code Quality**: "lint", "typecheck", "strict", "import", "naming", "命名"
- **Error Handling**: "try/catch", "Logger", "error", "throw", "例外"
- **Documentation**: "JSDoc", "TSDoc", "@ApiProperty", "comment", "コメント"
- **Security**: "secret", "password", "hash", "HTTPS", "ログに出力しない"
- **Git**: "commit", "branch", "コミットメッセージ", "feature branch"

**For each extracted rule, record**:
- Category (one of the 6 above)
- Content (the rule text)
- Severity: `[MUST]` (explicit requirement), `[SHOULD]` (recommended), `[MAY]` (optional)
- Source file and line reference

Rules from CLAUDE.md / AGENTS.md are **Priority 1** and default to `[MUST]`.

### Step 2: Codebase Analysis

If source code exists, analyze the codebase to detect implicit conventions.
Skip this step entirely if no source files are found (new project).

**2a. Directory structure analysis**:
- Scan directory tree (up to 3 levels deep)
- Detect patterns: feature-based (`modules/{feature}/`), layer-based (`controllers/`, `services/`), co-located tests vs separate `tests/` directory

**2b. File naming convention detection**:
1. Collect file names under `src/` (or primary source directory)
2. Classify each name: kebab-case, camelCase, PascalCase, snake_case
3. If one pattern is 60%+ of files → propose as `[MUST]`
4. Minority patterns → propose as `[SHOULD]` for unification

**2c. Library analysis**:
1. Read dependency file (`package.json`, `go.mod`, `requirements.txt`, etc.)
2. Identify major libraries:
   - Frameworks: NestJS, Next.js, Express, Fastify, Django, Flask, Gin, etc.
   - Testing: Jest, Vitest, Playwright, pytest, etc.
   - Validation: Zod, class-validator, Joi, etc.
   - ORM: Prisma, TypeORM, Drizzle, SQLAlchemy, GORM, etc.
   - Linters: ESLint, Biome, ruff, golint, etc.
3. Add library-specific best practice recommendations as `[SHOULD]` rules
   - Example: Prisma detected → `[SHOULD] Use Prisma Client for all DB access`
   - Example: Zod detected → `[SHOULD] Use Zod for runtime validation`

**2d. Code pattern analysis** (if code intelligence tools are available):
- Import style: relative (`./`) vs path alias (`@/`)
- Export style: named exports vs default exports
- Error handling patterns in use

**2e. Shared utility and library detection**:
1. Scan the codebase for shared utility modules, helper functions, and internal libraries:
   - Look for directories named `utils/`, `helpers/`, `lib/`, `shared/`, `common/`
   - Identify frequently imported internal modules
2. Cross-reference with dependency file to identify commonly used libraries
3. Present a summary of detected shared utilities and libraries to the user:
   ```
   Detected shared utilities and libraries:
     Internal: utils/logger.ts, lib/validation.ts, helpers/date.ts
     External: Zod (validation), Prisma (DB), date-fns (dates)
   ```
4. For each detected shared utility or library, generate a `[SHOULD]` rule:
   - Example: `[SHOULD] Use lib/validation.ts for input validation`
   - Example: `[SHOULD] Use Zod for runtime validation`
   - Example: `[SHOULD] Use utils/logger.ts instead of console.log`
5. Include the detected list in the generated coding-rules.md under a "Shared Utilities" section

Codebase analysis results are **Priority 2** and assigned `[MUST]` (for 60%+ majority patterns) or `[SHOULD]`.

### Step 3: Installed Skills Analysis

Scan installed skills for framework-specific best practices.

**3a. Skill detection**:
1. Scan `~/.claude/skills/` (global skills)
2. Scan `.claude/skills/` (project skills)
3. Read each `SKILL.md` frontmatter description and body

**3b. Framework match**:
Compare detected project tech stack (from Steps 1-2) with skill keywords:

| Project Tech | Matching Keywords |
|-------------|-------------------|
| Next.js | `next`, `next.js`, `vercel`, `react`, `RSC`, `server component` |
| NestJS | `nest`, `nestjs`, `express`, `fastify`, `typescript backend` |
| React | `react`, `hooks`, `component`, `jsx`, `tsx` |
| Go | `go`, `golang`, `goroutine` |
| Python | `python`, `django`, `flask`, `fastapi` |

**3c. User confirmation** (if matching skills found):

Use AskUserQuestion:
```
question: "The following installed skills were detected. Use them for rule extraction?" / "以下のインストール済みスキルが検出されました。ルール抽出に使用しますか？"
header: "Skills"
multiSelect: true
options:
  - "{skill-name} — {description} (Recommended)" / "{skill-name} — {説明}"
```

**3d. Priority mapping**:
- Skill-derived rules are **Priority 3** → `[SHOULD]` or `[MAY]`
- If a skill rule contradicts Priority 1 or 2 rules → keep higher priority, show warning
- Record source as `Source: skill/{skill-name}` in coding-rules.md

**3e. No matching skills**:
If no matching skills are installed, optionally inform the user:
```
"Matching skills may be available on skills.sh for your tech stack.
Install and re-run to incorporate best practices."
/ "技術スタックに適合するスキルが skills.sh にある可能性があります。
インストール後に再実行すると、ベストプラクティスを取り込めます。"
```

### Step 4: Interactive Dialogue

**4a. Present extraction results**:

Display detected rules summary by category:
```
Extraction Results:
  Testing Standards:    {n} rules
  Code Quality:         {n} rules
  Error Handling:       {n} rules
  Documentation:        {n} rules
  Security:             {n} rules
  Git:                  {n} rules
  Total:                {total} rules (Priority 1: {n}, Priority 2: {n}, Priority 3: {n})
```

If any category has 0 rules, highlight it for user attention.

**4b. Output path selection** (AskUserQuestion):

```
question: "Where to save coding-rules.md?" / "coding-rules.md の出力先は？"
header: "Output"
options:
  - "docs/coding-rules.md (Recommended)" / "docs/coding-rules.md（推奨）"
  - "docs/development/coding-rules.md"
```

If user selects "Other", accept any valid file path.

**4c. Rule supplementation** (AskUserQuestion):

For categories with missing or insufficient rules, ask targeted questions:

```
question: "Any additional testing rules?" / "テスト基準について追加ルールはありますか？"
header: "Testing"
options:
  - "Require 80%+ coverage (Recommended)" / "カバレッジ80%以上を必須にする"
  - "Specify E2E test patterns" / "E2Eテストパターンを指定する"
  - "No additions needed" / "追加不要"
```

```
question: "Commit message language?" / "コミットメッセージの言語は？"
header: "Git"
options:
  - "Japanese only" / "日本語のみ"
  - "English only" / "英語のみ"
  - "Conventional Commits (English)" / "Conventional Commits（英語）"
```

Suggest project-type-specific rules based on detected frameworks.
Refer to the Project-Type Recommendations section in the reference template.

### Step 5: Existing File Detection and Idempotency

If an existing `coding-rules.md` was found in Step 0:

1. Read the existing file
2. Compare with newly extracted rules (additions, changes, removals)
3. Use AskUserQuestion:
   ```
   question: "Existing coding-rules.md found. How to proceed?" / "既存の coding-rules.md が見つかりました。どうしますか？"
   header: "Existing File"
   options:
     - "Overwrite" / "上書きする"
     - "Merge differences" / "差分のみマージ"
     - "Cancel" / "キャンセル"
   ```
4. If "Cancel" → exit without changes

### Step 6: Generate coding-rules.md

1. Load the appropriate reference template (based on Language Rules)
2. Fill in extracted rules by category
3. Apply severity tags: `[MUST]`, `[SHOULD]`, `[MAY]`
4. Add source attribution for each rule
5. Include the Sources summary table at the end
6. Create output directory if it does not exist
7. Write the file

### Step 7: Update AGENTS.md / CLAUDE.md References

After generating coding-rules.md, append a reference to project convention files.

**Procedure**:
1. Check if `AGENTS.md` exists at project root
2. Check if `CLAUDE.md` exists (skip if it is a symlink to AGENTS.md)
3. Use AskUserQuestion:
   ```
   question: "Add reference to coding-rules.md in AGENTS.md / CLAUDE.md?" / "AGENTS.md / CLAUDE.md に coding-rules.md の参照を追記しますか？"
   header: "Update"
   options:
     - "Yes, add reference (Recommended)" / "はい、追記する（推奨）"
     - "No, skip" / "いいえ、スキップ"
   ```

4. If approved, append to the end of each file (or after an existing "Coding Rules" section):

   English version:
   ```markdown
   ## Coding Rules

   Follow the coding rules in this file during implementation:
   - [{output_path}]({output_path}) — Quality rules generated by spec-rules-init
   ```

   Japanese version:
   ```markdown
   ## コーディングルール

   実装時のコーディングルールは以下のファイルに従ってください:
   - [{output_path}]({output_path}) — spec-rules-init で生成された品質ルール集
   ```

5. If neither file exists → skip with a warning message:
   ```
   "Warning: No AGENTS.md or CLAUDE.md found. Skipping reference update."
   / "警告: AGENTS.md も CLAUDE.md も見つかりません。参照追記をスキップします。"
   ```

### Step 8: spec-series Integration Notice

After completing generation, inform the user about integration with other spec-series skills:

```
"coding-rules.md has been generated. The following spec-series skills now reference it:
- spec-generator: Uses coding-rules.md as design constraints during the design phase
- spec-inspect: Checks [MUST] rules in Check 13 (Project Rule Compliance)
- spec-implement: Uses coding-rules.md as a quality gate during implementation"
/ "coding-rules.md を生成しました。以下の spec-series スキルが参照するようになっています:
- spec-generator: design フェーズで coding-rules.md を設計制約として使用
- spec-inspect: Check 13（プロジェクトルール準拠）で [MUST] ルールをチェック
- spec-implement: 実装時の品質ゲートとして coding-rules.md を使用"
```

## Options

| Option | Description |
|--------|-------------|
| `--force` | Overwrite existing coding-rules.md without confirmation |
| `--category <name>` | Generate rules for a specific category only (e.g., `--category testing`) |

## Error Handling

- **Convention file unreadable**: Warn and skip the file, continue with remaining files
  ```
  "Warning: Could not read {filename}. Skipping."
  / "警告: {filename} を読み取れません。スキップします。"
  ```

- **Output directory does not exist**: Create it automatically
  ```bash
  mkdir -p {output_directory}
  ```

- **Write permission denied**: Show error and suggest an alternative path
  ```
  "Error: Cannot write to {path}. Try a different location."
  / "エラー: {path} に書き込めません。別のパスを指定してください。"
  ```

- **No convention files found**: Fall back to dialogue-only mode
  ```
  "No convention files (CLAUDE.md, AGENTS.md, etc.) found. Proceeding with dialogue-only mode."
  / "規約ファイル（CLAUDE.md, AGENTS.md等）が見つかりません。対話のみモードで進みます。"
  ```

## Usage Examples

```
# Generate coding rules from project conventions
"Generate coding rules"
「コーディングルールを生成して」

# Create coding-rules.md with forced overwrite
"Create coding-rules.md --force"
「coding-rules.md を作成 --force」

# Extract rules for a specific category
"Extract project rules --category testing"
「テストルールだけ抽出して」

# After generating, re-run to update
"Update coding-rules.md"
「coding-rules.md を更新して」
```

## Post-Completion Actions

After generating coding-rules.md, suggest next actions with AskUserQuestion:

```
question: "coding-rules.md generated. What's next?" / "coding-rules.md を生成しました。次のアクションは？"
header: "Next"
options:
  - "Generate specifications (spec-generator)" / "仕様書を生成する（spec-generator）"
  - "Set up development workflow (spec-workflow-init)" / "開発ワークフローを設定する（spec-workflow-init）"
  - "Done for now" / "完了"
```
