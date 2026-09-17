---
name: code-quality
description: >-
  Use when the user asks to review code, lint files, fix linting errors, audit a
  project, run static analysis, check types, inspect complexity, find circular
  dependencies, review architecture, scan for vulnerabilities or secrets, run
  pre-commit checks, or set up ESLint, Biome, ruff, pyright, tsc, madge,
  depcycle, Semgrep, or detect-secrets.
---

# Code Quality Skill

Analyze, verify, and fix code quality issues using the project's own tools. This
skill detects the project's linter and type checker, runs them with structured
output, normalizes findings into a consistent severity format, and presents
actionable results.

**Core principle**: Use what the project already has. No external services, no
server setup, no token overhead when not in use.

**Named workflows**:

1. **Lint** - review, check, lint, fix, or audit code quality
2. **Pre-commit Check** - changed-file lint and type check before commit
3. **Type Check** - pyright or tsc static type analysis
4. **Architecture Review** - full structural audit plus focused complexity/cycle checks
5. **Security Scan** - Semgrep SAST plus detect-secrets
6. **Comprehensive Review** - read-only maximum-coverage review across lint, complexity, types, architecture, and security
7. **Linter Setup** - configure a project-level linter

**Supported tools**:
- **JavaScript/TypeScript linting**: ESLint, Biome
- **Python linting**: ruff, pylint
- **Type checking**: pyright, tsc
- **Architecture**: madge, depcycle, knip, vulture, custom graph analysis
- **Security**: Semgrep, detect-secrets

## Step 1: Detect Project Tools

Before any analysis, determine the skill directory (the directory containing
this `SKILL.md`) and run detection.

```bash
bash <skill-dir>/scripts/detect-linter.sh [target-path]
```

Replace `<skill-dir>` with the absolute path to the directory containing this
file. For example, if this file is at
`/Users/alice/.claude/skills/code-quality/SKILL.md`, run:

```bash
bash /Users/alice/.claude/skills/code-quality/scripts/detect-linter.sh [target-path]
```

Detection outputs key=value pairs:

| Key | Use |
|-----|-----|
| `TOOL` | Linter: eslint, biome, ruff, pylint, npm-script, none |
| `COMMAND` | Analysis command with JSON output when available |
| `FIX_COMMAND` | Native auto-fix command, empty if unsupported |
| `CONFIG` | Config file path, empty when none was detected |
| `LANGUAGE` | javascript, python, or unknown |
| `TYPESCRIPT` | true when `tsconfig.json` exists |
| `FALLBACK` | true when built-in defaults are used |
| `PROJECT_ROOT` | Detected project root |
| `FRAMEWORK` | Framework hint for architecture analysis |
| `FILES` | Changed lintable files, only with `--changed-only` |
| `TYPE_CHECKER` | pyright, tsc, or none |
| `TYPE_CHECK_COMMAND` | Type-check command |
| `COGNITIVE_COMMAND` | Cognitive complexity command for the language |
| `ESLINT_DEFAULTS_CMD` | Bundled ESLint+sonarjs wrapper |
| `SEMGREP_AVAILABLE` | true when Semgrep can run through `uvx` |
| `SECRETS_TOOL` | detect-secrets, gitleaks, or none |

If `TOOL=none` and `LANGUAGE=unknown`, report that this project type is not
supported yet.

If `FALLBACK=true`, inform the user:

> No linter config found in your project. Running with the skill's built-in
> defaults. To customize, create your own config file.

If `TOOL=npm-script`, run `COMMAND` directly and parse human-readable output
best-effort. Look for `file:line:col: message` or ESLint/Biome-style output. If
the output is unstructured, present it verbatim.

If `TOOL=pylint`, there is no auto-fix. Map pylint JSON severities as:
`fatal` -> BLOCKER, `error` -> CRITICAL, `warning` -> MAJOR, `refactor` ->
MINOR, `convention` -> INFO.

Load reference files only as needed:
- `TOOL=eslint` -> `<skill-dir>/references/eslint.md`
- `TOOL=biome` -> `<skill-dir>/references/biome.md`
- `TOOL=ruff` -> `<skill-dir>/references/ruff.md`
- Load `<skill-dir>/references/severity-map.md` only when findings exist.

## Default Configs

The skill ships with built-in configs in `<skill-dir>/defaults/` so analysis can
run without project setup. Inspired by SonarQube's "Sonar way" quality profile.

### Python - `defaults/ruff.toml`

Rules enabled: `E`, `F`, `W`, `C90`, `I`, `N`, `UP`, `B`, `S`, `SIM`, `T20`.
Cyclomatic complexity threshold: 10. Fallback lint runs through `uvx ruff` with
`--config <skill-dir>/defaults/ruff.toml`.

### JavaScript/TypeScript - Biome fallback for general lint

When no JS/TS linter is configured, the skill uses Biome as the fallback for
general lint because Biome parses both JavaScript and TypeScript without parser
plugins. It runs through `npx --yes @biomejs/biome check --reporter=json`.

### JavaScript/TypeScript - Bundled ESLint + sonarjs for complexity

General JS/TS lint uses the project linter or Biome fallback. Cognitive
complexity uses the bundled ESLint wrapper because it needs
`eslint-plugin-sonarjs`:

```bash
bash <skill-dir>/scripts/eslint-defaults.sh
```

The wrapper lazily runs `npm ci --prefix defaults/` on first use, then execs
`defaults/node_modules/.bin/eslint`. First run costs about 10-20s and writes
`defaults/node_modules` (gitignored).

Lint and Architecture Review both use this wrapper for JS/TS complexity. It is
not the JS/TS fallback linter; Biome remains the fallback for regular linting.

**Security plugins are intentionally not bundled**. Security Scan owns that
surface through Semgrep and detect-secrets.

### When to suggest project-level config

After reporting results that used built-in defaults, add:

> These results use the skill's built-in rules. To customize severity, disable
> rules, or add plugins, create your own config.

Suggest:
- **ruff**: `ruff.toml` or `[tool.ruff]` in `pyproject.toml`
- **ESLint**: `npm init @eslint/config@latest`
- **Biome**: `npx @biomejs/biome init`

## Workflow: Lint

**Triggers**: "review", "check", "what's wrong with", "lint", "analyze",
"any issues in", "fix", "clean up", "auto-fix", "fix linting", "audit my
project", "project scan", "full analysis", "scan the whole project", "overall
code quality".

Use this workflow for file, directory, and project-level code quality checks.
Plain audit/project scan requests route here, not to Architecture Review.
Bare "full audit" routes to Comprehensive Review. Qualified architecture
requests such as "architecture full audit" and "structural audit" route to
Architecture Review.

### Scope and mode

- **Scope**: file(s), directory, or project root from the user request.
- **Mode**: `analyze` by default.
- **Fix mode**: use when the request says fix, clean up, auto-fix, or fix lint
  errors.
- **Project audit mode**: use when the target is the project root or the request
  says audit/project scan/full analysis.

### Analyze steps

1. Run detection:
   ```bash
   bash <skill-dir>/scripts/detect-linter.sh [project-path]
   ```
2. Determine the target files/directories from the user request.
3. Run the detected linter command with the target appended:
   ```bash
   npx eslint --format json src/index.ts
   npx @biomejs/biome check --reporter=json src/
   ruff check --output-format json src/main.py
   ```
4. Treat exit code 1 as findings found. Treat exit code 2+ as config/runtime
   failure and report it.
5. Parse findings into file, line, column, rule, message, severity, and
   fixability.
6. Run explicit complexity checks on the same target. Do not assume the project
   Ruff or ESLint config enables complexity.
7. Merge lint and complexity findings into one Code Quality Report.

### Complexity included by default

Lint includes both cyclomatic and cognitive complexity for review/check/lint and
audit requests. Complexity findings are manual-only; do not mark them
auto-fixable and do not offer `--fix` for them.

**Python**:

```bash
uvx ruff check --select C901 --output-format json [targets...]
uvx --with flake8-cognitive-complexity flake8 \
  --select=CCR001 --max-cognitive-complexity=15 [targets...]
```

If `uvx` is unavailable but `ruff` is installed, use `ruff check --select C901
--output-format json` for the cyclomatic half and warn that cognitive complexity
could not run.

**JavaScript/TypeScript** (run with `cwd` set to `PROJECT_ROOT`):

```bash
bash <skill-dir>/scripts/eslint-defaults.sh \
  --no-config-lookup \
  --config <skill-dir>/defaults/eslint.config.js \
  --rule '{"complexity":["warn",10],"sonarjs/cognitive-complexity":["warn",15]}' \
  --format json [targets...]
```

Thresholds:

| Metric | Max | Severity if exceeded |
|--------|-----|----------------------|
| Cognitive complexity | 15 | 16-25 -> `[MAJ]`, >= 26 -> `[CRT]` |
| Cyclomatic complexity | 10 | Any value over cap -> `[MAJ]` |

When both metrics exceed their cap for the same function, cognitive drives the
severity tag. Merge by `(file, line +/-2)`. Function names come from the
cyclomatic finding when available.

Load `<skill-dir>/references/cognitive-complexity.md` when complexity findings
exist so refactoring suggestions are concrete.

### Fix mode

1. Run the full lint analysis first, including complexity, to capture a baseline.
2. Count baseline issues by severity and auto-fixability.
3. If `FIX_COMMAND` is empty, explain that the detected tool has no auto-fix and
   provide manual suggestions.
4. Run the native fix command on the target:
   ```bash
   npx eslint --fix src/index.ts
   npx @biomejs/biome check --write src/
   ruff check --fix src/main.py
   ```
5. Re-run the linter and complexity checks.
6. Report the delta:
   - what the tool fixed in plain language
   - what remains
   - which remaining findings are manual-only complexity refactors

Do not say only "N issues fixed". Name the types of changes when the tool output
makes them knowable, for example "removed unused imports" or "replaced `var`
with `const`".

### Project audit mode

Run the linter and explicit complexity checks on the project root. Respect the
tool's normal ignore behavior for `node_modules/`, `dist/`, `build/`, `venv/`,
`__pycache__/`, and similar paths.

If more than 50 findings exist, show the top 50 sorted by severity and state the
total. Include:
- total issues by severity
- top 5 problematic files by issue count
- auto-fixable count
- manual-only complexity count

Offer concrete follow-ups: fix auto-fixable issues, drill into a file, run
focused complexity, or run Architecture Review for structure/coupling.

## Workflow: Pre-commit Check

**Triggers**: "check before commit", "pre-commit", "check my changes", "ready to
commit?", "lint changed files".

This workflow is intentionally fast. It runs changed-file lint and type checks.
It does not run cognitive complexity unless the user explicitly asks for
complexity.

### Steps

1. Run detection with changed files:
   ```bash
   bash <skill-dir>/scripts/detect-linter.sh [project-path] --changed-only
   ```
2. If `FILES` is empty, report "No lintable files in current changes."
3. Run the detected linter on changed files:
   ```bash
   npx eslint --format json file1.ts file2.ts
   npx @biomejs/biome check --reporter=json file1.ts file2.ts
   ruff check --output-format json file1.py file2.py
   ```
4. If `TYPE_CHECKER` is not `none`, run type checking:
   - **pyright**: `npx pyright --outputjson file1.py file2.py`
   - **tsc**: `npx tsc --noEmit`, then filter diagnostics to changed files
5. Present a pass/fail verdict:
   - **PASS**: "All changed files pass lint and type checks. Ready to commit."
   - **FAIL**: show changed-file issues with severity and suggested fixes.

If the user asks for pre-commit plus complexity, run Lint on the changed files
after the fast pre-commit checks and label complexity findings as manual-only.

## Workflow: Type Check

**Triggers**: "type check", "verify types", "run pyright", "run tsc", "type
errors", "check types", "verify code", "static type analysis".

Type checkers catch correctness issues that linters miss, such as missing
attributes, invalid function signatures, and unsafe `None`/`undefined` usage.

**Supported tools**:
- **Python**: pyright through `npx pyright`
- **TypeScript**: `tsc --noEmit`

### Steps

1. Run detection and read `LANGUAGE`, `PROJECT_ROOT`, `TYPE_CHECKER`, and
   `TYPE_CHECK_COMMAND`.
2. If `TYPE_CHECKER=none`, say type checking is available for Python and
   TypeScript projects. For plain JavaScript, suggest adding a `tsconfig.json`
   with `npx tsc --init` if they want type checking.
3. Load `<skill-dir>/references/pyright.md` when `TYPE_CHECKER=pyright`.
4. Run the type checker:
   ```bash
   npx pyright --outputjson [files-or-directory]
   npx tsc --noEmit
   ```
5. Treat exit code 1 as type errors found, not command failure.
6. Parse results:
   - Pyright JSON: `generalDiagnostics`; line numbers are 0-based, add 1 when
     displaying.
   - tsc text: `file(line,col): error TSxxxx: message`.
7. Normalize severity:
   - pyright `error` -> `[CRT]`
   - pyright `warning` -> `[MAJ]`
   - pyright `information` -> `[MIN]`
   - tsc errors -> `[CRT]`
   - tsc warnings -> `[MAJ]`
8. Present findings with concrete fixes.

Filtering:
- Group noisy `reportMissingTypeStubs` warnings into one summary line.
- If more than 50 diagnostics exist, show the top 50 by severity and state the
  total.

## Workflow: Architecture Review

**Triggers**: "architecture review", "review architecture", "arch audit",
"architecture full audit", "structural audit", "find god modules", "find hub
modules", "layering violations", "coupling metrics", "instability", "module
coupling", "show me the structure", "onboard me to this codebase", "check
complexity", "find complex functions", "cyclomatic complexity", "cognitive
complexity", "circular dependencies", "circular imports", "dependency graph",
"find cycles", "orphan modules".

Architecture Review has three modes:

| Request | Mode |
|---------|------|
| complexity only | focused complexity |
| cycles/dependencies only | focused cycles |
| architecture/audit/onboarding/coupling/layers | full structural audit |

### Full structural audit mode

Produces a structured report with cycles, layering violations, hub/god modules,
instability hotspots, deep import chains, oversized files, excessive exports,
dead code, and complex functions. It is for on-demand audits and onboarding, not
a pre-commit gate.

1. Run detection and read `LANGUAGE`, `PROJECT_ROOT`, and `FRAMEWORK`.
2. Run the orchestrator:
   ```bash
   bash <skill-dir>/scripts/arch-review.sh \
     --project-root "$PROJECT_ROOT" \
     --language "$LANGUAGE" \
     --framework "$FRAMEWORK"
   ```
3. Useful flags:
   - `--top N`
   - `--include-tests`
   - `--skip-section <name>` (repeatable)
   - `--max-file-loc`, `--max-exports`, `--max-ca`, `--max-ce`,
     `--max-chain-depth`
4. Load `<skill-dir>/references/architecture.md`.
5. Render the JSON report using the normal severity-table style.

If `LANGUAGE=unknown`, report that Architecture Review supports Python and
JS/TS projects. If `python3` is missing, report that the orchestrator requires
`python3`.

Findings are not necessarily errors. Always render clean, found, skipped, and
error sections clearly.

### Focused complexity mode

Use this mode for "check complexity", "find complex functions", "hard to test",
or "refactor candidates". It runs the same dual-metric complexity checks as
Lint, but reports a dedicated complexity table and refactoring guidance.

1. Run detection to get `LANGUAGE`, `PROJECT_ROOT`, and `COGNITIVE_COMMAND`.
2. Prefer the helper used by the architecture orchestrator:
   `arch_review.complexity.run_complexity_check(root, language, metric="both")`.
   If driving commands directly, use:

   **Python**:
   ```bash
   uvx ruff check --select C901 --output-format json [targets...]
   uvx --with flake8-cognitive-complexity flake8 \
     --select=CCR001 --max-cognitive-complexity=15 [targets...]
   ```

   **JS/TS** (run from `PROJECT_ROOT`):
   ```bash
   bash <skill-dir>/scripts/eslint-defaults.sh \
     --no-config-lookup \
     --config <skill-dir>/defaults/eslint.config.js \
     --rule '{"complexity":["warn",10],"sonarjs/cognitive-complexity":["warn",15]}' \
     --format json [targets...]
   ```
3. Merge by `(file, line +/-2)` and sort by cognitive complexity descending.
4. Use severity rules:
   - cognitive 16-25 -> `[MAJ]`
   - cognitive >= 26 -> `[CRT]`
   - cyclomatic-only over 10 -> `[MAJ]`
5. Load `<skill-dir>/references/cognitive-complexity.md` and include manual
   refactoring suggestions such as early returns, extract method, table
   dispatch, or polymorphism.

Complexity violations have no auto-fix. If cognitive tooling is unavailable,
fall back to cyclomatic-only and warn in the report.

### Focused cycles mode

Use this mode for circular dependencies, circular imports, dependency graph, find
cycles, or orphan modules.

1. Run detection and read `LANGUAGE`, `TYPESCRIPT`, `FRAMEWORK`, and
   `PROJECT_ROOT`.
2. Load:
   - JS/TS -> `<skill-dir>/references/madge.md`
   - Python -> `<skill-dir>/references/pydeps.md`
3. Determine entry point:
   - Node services/libraries: package `main`/`module`, then `src/index.ts`,
     `src/server.ts`, `src/main.ts`, or `src/app.ts`
   - Framework projects: scan source directories such as `app/`, `pages/`, or
     `src/`
   - Multi-root projects: scan each source root separately when one entry misses
     files
4. Run cycles:
   ```bash
   npx madge --circular --json src/
   npx madge --circular --json --ts-config tsconfig.json --extensions ts,tsx src/index.ts
   npx madge --circular --json --ts-config tsconfig.json --extensions ts,tsx app/
   uvx depcycle <package-path>
   ```
5. For JS/TS orphans when requested:
   ```bash
   npx madge --orphans [entry-point]
   ```
6. Normalize severity:
   - Circular dependency -> `[CRT]`
   - Orphan module -> `[INF]`
7. Provide actionable refactoring suggestions. The usual fix is to extract a
   shared dependency into a separate module that both sides can import.

If `npx madge` appears to become `npm run madge` or emits `Unknown cli config
"--circular"`, bypass aliases/hooks:

```bash
command npx madge --version
command npx madge --circular --json --ts-config tsconfig.json --extensions ts,tsx app/
```

Do not conclude madge is missing until `command npx madge --version` fails.

## Workflow: Security Scan

**Triggers**: "security scan", "find vulnerabilities", "SAST scan", "OWASP
scan", "CWE scan", "scan for security issues", "secret scan", "find secrets",
"find leaked credentials", "find API keys", "check for hardcoded passwords".

Security Scan combines Semgrep with detect-secrets through the orchestrator.
Both run through `uvx` when available.

### Steps

1. Run detection and read `SEMGREP_AVAILABLE`, `SECRETS_TOOL`, `PROJECT_ROOT`,
   and `LANGUAGE`. If both tools are unavailable, tell the user to install `uv`
   with `brew install uv` or `pip install uv`.
2. Run:
   ```bash
   bash <skill-dir>/scripts/security-scan.sh \
     --project-root "$PROJECT_ROOT" \
     --language "$LANGUAGE"
   ```
3. Useful flags:
   - `--skip-section semgrep`
   - `--skip-section secrets`
   - `--semgrep-config p/owasp-top-ten`
   - `--exclude <pattern>` (repeatable)
   - `--timeout-per-section 180`
   - `--max-findings 200`
4. Load references only when findings exist:
   - `<skill-dir>/references/semgrep.md`
   - `<skill-dir>/references/secrets.md`
5. Render the orchestrator JSON using the normal severity-table style.

Severity:
- Semgrep `ERROR` -> `[BLK]`
- Semgrep `WARNING` -> `[CRT]`
- Semgrep `INFO` -> `[MAJ]`
- Any secret -> `[BLK]`

Secrets are not optional. Tell the user to rotate credentials first, then remove
them from source or suppress documented false positives.

Security Scan does not modify the project. Suppression edits such as
`// nosemgrep` or `# pragma: allowlist secret` are user actions unless the user
explicitly asks for edits.

## Workflow: Comprehensive Review

**Triggers**: "comprehensive review", "full audit", "review with all features",
"maximum coverage review".

Comprehensive Review is the read-only, maximum-coverage workflow. Use it when
the user asks for a broad all-feature review. Do not use auto-fix, set up
linters, edit suppressions, or modify project files in this workflow.

Trigger precedence:
- Bare "full audit" routes here.
- "Architecture review", "architecture full audit", and "structural audit"
  route to Architecture Review.
- Existing lint-focused phrases such as "audit my project", "project scan",
  and "full analysis" stay in Lint project audit mode.

### Steps

1. Run detection:
   ```bash
   bash <skill-dir>/scripts/detect-linter.sh [project-path]
   ```
2. Run project-level Lint in analyze mode, including explicit cyclomatic and
   cognitive complexity checks. Do not run native fix commands.
3. If `TYPE_CHECKER` is not `none`, run Type Check. If unavailable, record a
   skipped status with the reason.
4. Run Architecture Review in full structural audit mode, including tests:
   ```bash
   bash <skill-dir>/scripts/arch-review.sh \
     --project-root "$PROJECT_ROOT" \
     --language "$LANGUAGE" \
     --framework "$FRAMEWORK" \
     --include-tests
   ```
5. Run Security Scan with the default Semgrep `p/security-audit` config plus
   detect-secrets:
   ```bash
   bash <skill-dir>/scripts/security-scan.sh \
     --project-root "$PROJECT_ROOT" \
     --language "$LANGUAGE" \
     --semgrep-config p/security-audit
   ```
6. Scan the full target, but cap displayed findings using the existing workflow
   limits: 50 lint/type findings, 50 architecture findings, and 200 security
   findings per security section. Always state total counts and whether output
   was truncated.

### Report format

Return one user-facing Comprehensive Review report with sections in this order:
- Summary: overall status, elapsed time, tools detected, files/targets scanned,
  total findings by severity, and section status counts.
- Lint and complexity: status, elapsed time, skipped/error reason if any, total
  counts, top findings, auto-fixable count, and manual-only complexity count.
- Type check: status, elapsed time, skipped/error reason if any, total counts,
  and top diagnostics.
- Architecture Review: status, elapsed time, skipped/error reason if any, total
  counts by section/severity, and top structural findings.
- Security Scan: status, elapsed time, skipped/error reason if any, Semgrep and
  detect-secrets counts, and top findings.
- Recommended next actions: prioritize blockers/secrets/security first, then
  type errors, cycles/architecture risks, high-complexity refactors, and
  auto-fixable lint.

Status values are `clean`, `found`, `skipped`, or `error`. Treat command exit
codes that mean "findings found" as `found`, not `error`. Include concrete
skip/error reasons so the user can distinguish unsupported language, missing
tooling, and runtime failures.

## Workflow: Linter Setup

**Triggers**: "set up linting", "configure eslint", "configure ruff", "add a
linter", "set up code quality", "init eslint", "init ruff", "set up biome".

This is the only workflow that modifies project files.

### Steps

1. Run detection and read `TOOL`, `LANGUAGE`, `FALLBACK`, and `CONFIG`.
2. If `FALLBACK=false`, the project already has a linter. Say which tool and
   config were found, then ask whether the user wants a review or config update.
3. Choose a setup:

   **Python - recommend ruff**:
   ```bash
   cp <skill-dir>/defaults/ruff.toml [project-root]/ruff.toml
   ```

   **JavaScript - recommend ESLint**:
   ```bash
   npm init @eslint/config@latest
   ```

   Non-interactive fallback:
   ```bash
   cp <skill-dir>/defaults/eslint.config.js [project-root]/eslint.config.js
   npm install --save-dev eslint
   ```

   **TypeScript - recommend ESLint with TypeScript support**:
   ```bash
   npm init @eslint/config@latest
   npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin typescript-eslint
   ```
   If using the non-interactive install path, also create `eslint.config.js`:
   ```js
   import tseslint from 'typescript-eslint';

   export default tseslint.config(
     ...tseslint.configs.recommended,
     {
       rules: {
         "complexity": ["warn", 10],
       },
     },
   );
   ```

   **Biome alternative**:
   ```bash
   npm install --save-dev @biomejs/biome
   npx @biomejs/biome init
   ```
4. Verify setup:
   ```bash
   bash <skill-dir>/scripts/detect-linter.sh [project-path]
   ```
   Confirm `FALLBACK=false`.
5. Offer to run Lint as the initial analysis.
6. Remind the user to commit the new config.

## Output Format

### Summary Header

```markdown
## Code Quality Report

**Tool**: ESLint | **Config**: eslint.config.js | **Files scanned**: 3

| Severity | Count |
|----------|-------|
| [CRT] CRITICAL | 2 |
| [MAJ] MAJOR | 5 |
| [MIN] MINOR | 3 |
| **Total** | **10** |
```

### Per-file Findings

```markdown
### src/index.ts

| Line | Severity | Rule | Message |
|------|----------|------|---------|
| 10 | [CRT] | no-unused-vars | 'foo' is defined but never used |
| 25 | [MAJ] | eqeqeq | Expected '===' but found '==' |
| 42 | [MIN] | prefer-const | 'x' is never reassigned; use 'const' |
```

For MAJOR and above, add a brief explanation after the table:

```markdown
**Line 10** (`no-unused-vars`): Unused variables indicate dead code. Remove
`foo` or use it.
**Line 25** (`eqeqeq`): `==` performs type coercion. Use `===`.
```

### Clean Result

```markdown
## Code Quality Report

**Tool**: ESLint | **Config**: eslint.config.js | **Files scanned**: 3

No issues found.
```

## Fix Strategy

1. Prefer native auto-fix first.
2. Re-analyze after fixing.
3. For ruff, `--fix` applies safe fixes only; mention `--unsafe-fixes` only if
   the user wants all fixes.
4. For Biome, `--write` is safe and `--write --unsafe` applies unsafe fixes.
5. Complexity, dependency cycles, and security findings are manual unless the
   user explicitly asks for source edits.
6. Report what changed, what remains, and the severity of remaining issues.

## Error Handling

### Tool not installed

If a tool command fails with "command not found":
- **ruff**: `uvx ruff` runs without permanent installation but requires `uv`;
  if `uv` is missing, use `pip install ruff`.
- **eslint**: `npm install --save-dev eslint`.
- **biome**: `npm install --save-dev @biomejs/biome && npx @biomejs/biome init`.
- **pyright**: `npx pyright`.

### Large output

If any command returns more than 50 findings, truncate to the top 50 by severity
and report:

> Showing top 50 of N total issues. Run analysis on specific files to see more.

### Parse errors / syntax errors

If a linter reports parsing errors, report them as BLOCKER severity. Syntax
errors must be fixed before the rest of the analysis is meaningful.

## Reference Files

Load references based on the detected tool or requested workflow:

| File | When to load |
|------|-------------|
| `<skill-dir>/references/severity-map.md` | Findings exist and need severity normalization |
| `<skill-dir>/references/eslint.md` | `TOOL=eslint` or JS/TS complexity wrapper details |
| `<skill-dir>/references/biome.md` | `TOOL=biome` |
| `<skill-dir>/references/ruff.md` | `TOOL=ruff` |
| `<skill-dir>/references/pyright.md` | Type Check with pyright |
| `<skill-dir>/references/madge.md` | Architecture Review focused cycles for JS/TS |
| `<skill-dir>/references/pydeps.md` | Architecture Review focused cycles for Python |
| `<skill-dir>/references/architecture.md` | Architecture Review full structural audit |
| `<skill-dir>/references/knip.md` | Architecture Review dead-code section for JS/TS |
| `<skill-dir>/references/vulture.md` | Architecture Review dead-code section for Python |
| `<skill-dir>/references/cognitive-complexity.md` | Lint or Architecture Review complexity findings |
| `<skill-dir>/references/semgrep.md` | Security Scan with Semgrep findings |
| `<skill-dir>/references/secrets.md` | Security Scan with secret findings |
