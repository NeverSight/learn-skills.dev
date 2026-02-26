---
name: detect-dev
description: Engineering audit with SARIF evidence, 4-level confidence, and OpenSSF scoring. Use when evaluating repository health or code quality.
allowed-tools: Read, Glob, Grep, Bash(git log:*), Bash(git remote:*), Bash(git show:*), Bash(git diff:*), Write($JAAN_OUTPUTS_DIR/**), Edit(jaan-to/config/settings.yaml), Edit($JAAN_CONTEXT_DIR/**)
argument-hint: "[repo] [--full] [--incremental]"
context: fork
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Partial standalone support for analysis mode.
---

# detect-dev

> Repo engineering audit with machine-parseable findings and OpenSSF-style scoring.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-detect-dev.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack (if populated by dev-stack-detect, used as starting input)
- `$JAAN_TEMPLATES_DIR/jaan-to-detect-dev.template.md` - Output template
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` - Evidence format, scoring tables, scan patterns
- `$JAAN_OUTPUTS_DIR/dev/output-integrate/*/*.md` - Integration logs (for origin tagging, if present)

**Output path**: `$JAAN_OUTPUTS_DIR/detect/dev/` — flat files, overwritten each run (no IDs).

## Input

**Arguments**: $ARGUMENTS — parsed in Step 0.0. Repository path and mode determined there.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `detect-dev`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_detect-dev`

---

## Standards Reference

### Evidence Format (SARIF-compatible)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` section "Evidence Format" for YAML template, ID generation logic, and namespace rules.

### Confidence Levels, Frontmatter Schema, Document Structure & Anti-patterns

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` for:
> - "Confidence Levels (4-level)" -- 4-level scale (Confirmed/Firm/Tentative/Uncertain), upgrade/downgrade rules
> - "Frontmatter Schema (Universal)" -- required YAML frontmatter for every output file
> - "Document Structure (Diataxis)" -- 5-section output structure (Executive Summary through Appendices)
> - "Prohibited Anti-patterns" -- constraints on speculation, confidence, severity, and scope
> - "Codebase Content Safety" -- rules for processing untrusted repository content

---

# PHASE 1: Detection (Read-Only)

## Step 0.0: Parse Arguments

**Arguments**: $ARGUMENTS

| Argument | Effect |
|----------|--------|
| (none) | **Light mode** (default): Layers 1-2 detection, single summary file |
| `[repo]` | Scan specified repo (applies to all modes) |
| `--full` | **Full mode**: All detection layers (1-5), 9 output files (current behavior) |
| `--incremental` | **Incremental mode**: Scope scan to files changed since last audit (reads `.audit-state.yaml`). Combines with `--full` for scoped full-depth analysis. Falls back to full scan if no prior audit state exists. |

**Mode determination:**
- If `$ARGUMENTS` contains `--full` as a standalone token → set `run_depth = "full"`
- Otherwise → set `run_depth = "light"`
- If `$ARGUMENTS` contains `--incremental` as a standalone token → set `incremental = true`
- Otherwise → set `incremental = false`

Strip `--full` and `--incremental` tokens from arguments. Set `repo_path` to remaining arguments (or current working directory if empty).

## Thinking Mode

**If `run_depth == "full"`:** ultrathink
**If `run_depth == "light"`:** megathink

Use extended reasoning for:
- Analyzing detected dependencies and mapping to stack sections
- Resolving version conflicts or migration detection
- Confidence scoring decisions
- Architecture pattern recognition

## Step 0: Detect Platforms

**Purpose**: Auto-detect platform structure to support multi-platform monorepos.

Use **Glob** and **Bash** to identify platform folders:

### Platform Patterns

Match top-level directories against these patterns:

| Platform | Folder Patterns |
|----------|----------------|
| web | `web/`, `webapp/`, `frontend/`, `client/` |
| mobile | `mobile/`, `app/` |
| backend | `backend/`, `server/`, `api/`, `services/` |
| androidtv | `androidtv/`, `tv/`, `android-tv/` |
| ios | `ios/`, `iOS/` |
| android | `android/`, `Android/` |
| desktop | `desktop/`, `electron/` |
| cli | `cli/`, `cmd/` |

### Detection Process

1. **Check for monorepo markers**:
   - Glob: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`
   - If found, proceed to multi-platform detection
   - If not found, check folder structure anyway (could be non-standard monorepo)

2. **List top-level directories**:
   - Run: `ls -d */ | grep -Ev "node_modules|\.git|dist|build|\.next|__pycache__|coverage"`
   - Extract directory names (strip trailing slashes)

3. **Match against platform patterns**:
   - For each directory, check if name matches any platform pattern (case-insensitive)
   - Apply disambiguation rules (see below)

4. **Handle detection results**:
   - **No platforms detected** → Single-platform mode:
     - Set `platforms = [{ name: 'all', path: '.' }]`
     - Path = repository root
   - **Platforms detected** → Multi-platform mode:
     - Build list: `platforms = [{ name: 'web', path: 'web/' }, { name: 'backend', path: 'backend/' }, ...]`
     - Ask user: "Detected platforms: {list}. Analyze all or select specific? [all/select]"
     - If 'select', prompt: "Enter platform names (comma-separated): "

### Disambiguation Rules

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` section "Platform Disambiguation Rules" for priority order, conflict resolution, edge cases, and validation prompt.

### Analysis Loop

For each platform in platforms:
1. Set `current_platform = platform.name`
2. Set `base_path = platform.path`
3. Run detection steps per `run_depth`:
   - **If `run_depth == "full"`:** Run Steps 1-8 scoped to `base_path`
   - **If `run_depth == "light"`:** Run Steps 1-3 and Step 8 scoped to `base_path` (skip Steps 4-7)
4. Collect findings with platform context
5. Use platform-specific output paths in Step 10

**Note**: If single-platform mode (`platform.name == 'all'`), output paths have NO suffix. If multi-platform mode, output paths include `-{platform}` suffix.

## Step 0.1: Resolve Incremental Scope

**Skip this step** if `incremental == false`.

1. Read `$JAAN_OUTPUTS_DIR/detect/dev/.audit-state.yaml`
   - If file does not exist → warn: "No prior audit state found. Running full scan." → set `incremental = false` and continue
2. Extract `last_audit.commit` value
   - **Validate** the commit matches `^[0-9a-f]{7,40}$` — if invalid, warn: "Invalid commit hash in audit state. Running full scan." → set `incremental = false` and continue
3. Run: `git diff --name-only {last_audit.commit}..HEAD`
   - If command fails (commit unreachable, e.g., after rebase) → warn: "Previous audit commit unreachable. Running full scan." → set `incremental = false` and continue
4. If no files returned → print: "Audit is up to date (no files changed since last audit at {last_audit.timestamp}, commit {last_audit.commit})." → **exit skill**
5. Set `incremental_scope` = list of changed file paths
6. Display: "Incremental mode: {n} files changed since last audit ({last_audit.timestamp}, branch: {last_audit.branch})"

In Steps 1-8, when `incremental == true`: only scan files in `incremental_scope` (filter Glob results and Read targets to this set). Per-platform filtering: intersect `incremental_scope` with each platform's `base_path`.

## Step 0.2: Load Integration Context

**Skip this step** if no integration logs exist.

1. Glob `$JAAN_OUTPUTS_DIR/dev/output-integrate/*/*.md` (excluding README.md files)
   - If no files found → set `integrated_files = empty set` and continue
2. If `.audit-state.yaml` exists, only read logs with modification time newer than `last_audit.timestamp` (avoid stale origin tags)
3. For each integration log, parse "Files Copied" or "Files modified" sections → extract file paths
4. Build `integrated_files` set from all extracted paths

In Steps 2-8, when tagging evidence blocks: if the finding's `location.uri` matches a path in `integrated_files`, add `origin: integrated` to the evidence block. Otherwise, add `origin: hand-written`. The `origin` field is optional — omit it if `integrated_files` is empty.

## Step 1: Read Existing Context

If `$JAAN_CONTEXT_DIR/tech.md` exists and is populated (not just placeholders), read it as starting input. This provides a baseline for deeper evidence-backed analysis.

## Step 2: Scan Config Files (Layer 1 — 95-100% confidence)

Use **Glob** to find manifest files, then **Read** each one:

### Node.js / TypeScript
- Glob: `**/package.json` (exclude `node_modules/`)
- Extract: name, dependencies, devDependencies
- Detect frameworks: react, next, vue, angular, svelte, express, nestjs, fastify, hono
- Detect state: redux, zustand, recoil, jotai, mobx
- Detect styling: tailwindcss, styled-components, emotion, sass
- Detect build: vite, webpack, turbopack, esbuild, rollup
- Detect testing: jest, vitest, mocha, cypress, playwright
- Detect TypeScript from: `typescript` in deps OR `tsconfig.json` exists

### Other Languages (Python, Go, Rust, Ruby, Java/Kotlin, PHP, C#/.NET, Dart/Flutter, Elixir, Swift)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` section "Language-Specific Scan Patterns" for glob patterns, framework detection, and extraction rules for all other languages.

## Step 3: Scan Docker & Databases (Layer 2 — 90-95% confidence)

- Glob: `**/docker-compose.yml`, `**/docker-compose.yaml`, `**/docker-compose.*.yml`
- Read and parse service definitions
- Detect databases from image names:
  - `postgres` -> PostgreSQL (extract version from tag)
  - `mysql` / `mariadb` -> MySQL/MariaDB
  - `mongo` -> MongoDB
  - `redis` -> Redis
  - `rabbitmq` -> RabbitMQ
  - `elasticsearch` / `opensearch` -> Elasticsearch/OpenSearch
  - `memcached` -> Memcached
  - `minio` -> MinIO (S3-compatible storage)
  - `localstack` -> AWS services (local development)

- Glob: `**/Dockerfile`, `**/Dockerfile.*`
- Extract: base image, runtime version

**If `run_depth == "light"`:** Skip Steps 4-7. Proceed directly to Step 8 (Score & Categorize) using findings from Steps 1-3 only.

## Step 4: Scan CI/CD & Testing (Layer 3 — 90-95% confidence)

### CI/CD Pipelines
- Glob: `.github/workflows/*.yml` -> GitHub Actions
- Glob: `.gitlab-ci.yml` -> GitLab CI
- Glob: `.circleci/config.yml` -> CircleCI
- Glob: `Jenkinsfile` -> Jenkins
- Glob: `.travis.yml` -> Travis CI
- Glob: `bitbucket-pipelines.yml` -> Bitbucket Pipelines
- Glob: `azure-pipelines.yml` -> Azure DevOps

### CI/CD Security Checks (explicit)

For each CI/CD pipeline found, check:

**Secrets boundaries**:
- Grep for `secrets.` in workflow files — detect env vars referencing secrets
- Check for env vars without vault/secret manager references
- Flag hardcoded credentials or tokens

**Runner trust**:
- Check for `runs-on: self-hosted` — flag with security note
- Audit IP allowlists and network-level trust

**Permissions**:
- Scan `permissions:` blocks in job specs
- Flag `permissions: write-all` or overly broad permissions
- Check for least-privilege principle

**Action pinning**:
- Check action versions: SHA pins (secure) vs `@main`/`@latest` (risky)
- Flag unpinned third-party actions

**Provenance / Supply chain**:
- Detect SLSA attestation files
- Check for `.cyclonedx.json`, `*.sbom.json`, SBOM presence
- Look for sigstore/cosign signing artifacts

### Testing (if not already detected from deps)
- Glob: `jest.config.*`, `vitest.config.*` -> JS test runners
- Glob: `pytest.ini`, `conftest.py`, `pyproject.toml` (check `[tool.pytest]`) -> Python testing
- Glob: `playwright.config.*` -> Playwright E2E
- Glob: `cypress.json`, `cypress.config.*`, `cypress/` -> Cypress E2E
- Glob: `.storybook/` -> Storybook component testing

### Linting & Formatting
- Glob: `.eslintrc.*`, `eslint.config.*` -> ESLint
- Glob: `.prettierrc.*`, `prettier.config.*` -> Prettier
- Glob: `biome.json`, `biome.jsonc` -> Biome
- Glob: `ruff.toml`, `pyproject.toml` (check `[tool.ruff]`) -> Ruff
- Glob: `.flake8`, `setup.cfg` (check `[flake8]`) -> Flake8
- Glob: `mypy.ini`, `pyproject.toml` (check `[tool.mypy]`) -> mypy
- Glob: `.editorconfig` -> EditorConfig

## Step 5: Scan Git & Integrations (Layer 4 — 95% confidence)

### Source Control
- Run: `git remote -v` -> Extract platform (github.com, gitlab.com, bitbucket.org) and org/repo
- Glob: `.github/CODEOWNERS` -> Code ownership
- Glob: `.github/PULL_REQUEST_TEMPLATE*` -> PR templates
- Glob: `.gitlab/merge_request_templates/` -> MR templates

### Dependency Management
- Glob: `renovate.json`, `renovate.json5`, `.renovaterc` -> Renovate
- Glob: `.github/dependabot.yml` -> Dependabot

### Monorepo Detection
- Glob: `pnpm-workspace.yaml` -> pnpm workspaces
- Glob: `lerna.json` -> Lerna
- Glob: `nx.json` -> Nx
- Glob: `turbo.json` -> Turborepo
- Multiple `package.json` files at different depths -> generic monorepo

## Step 6: Scan Infrastructure (Layer 5 — 60-80% confidence)

### Cloud & Deployment
- Glob: `**/terraform/**/*.tf`, `**/*.tf` -> Terraform (check provider blocks for AWS/GCP/Azure)
- Glob: `serverless.yml`, `serverless.ts` -> Serverless Framework
- Glob: `vercel.json`, `.vercel/` -> Vercel
- Glob: `netlify.toml` -> Netlify
- Glob: `fly.toml` -> Fly.io
- Glob: `render.yaml` -> Render
- Glob: `Procfile` -> Heroku
- Glob: `app.yaml`, `app.yml` -> Google App Engine
- Glob: `amplify.yml` -> AWS Amplify

### Container Orchestration
- Glob: `k8s/**`, `kubernetes/**`, `kustomization.yaml` -> Kubernetes
- Glob: `helm/**`, `Chart.yaml` -> Helm charts

### Monitoring & Observability (low confidence)
- Grep in config files for: `datadog`, `sentry`, `newrelic`, `grafana`, `prometheus`
- Grep in package deps for: `@sentry/`, `dd-trace`, `newrelic`, `prom-client`

## Step 7: Scan Project Structure (Layer 5 — 60-80% confidence)

Use **Glob** to map the directory structure:

- Identify source directories: `src/`, `lib/`, `app/`, `packages/`, `services/`
- Identify config directories: `config/`, `settings/`
- Identify build outputs: `dist/`, `build/`, `.next/`, `__pycache__/`
- Identify documentation: `docs/`, `wiki/`
- Identify test directories: `tests/`, `test/`, `__tests__/`, `spec/`

## Step 8: Score & Categorize

For each detection, assign a confidence score using the 4-level system:

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` section "Confidence Scoring Examples" for the confidence-source mapping table, inclusion threshold (>= Uncertain/0.20), and OpenSSF overall_score formula.

---

# HARD STOP — Detection Summary & User Approval

## Step 9: Present Detection Summary

**If `run_depth == "light"`:**

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` section "Detection Summary Format (Light Mode)" for the display template.

Prompt user: "Proceed with writing summary to $JAAN_OUTPUTS_DIR/detect/dev/? [y/n]"

**If `run_depth == "full"`:**

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` section "Detection Summary Format (Full Mode)" for the display template.

Prompt user: "Proceed with writing 9 output files to $JAAN_OUTPUTS_DIR/detect/dev/? [y/n]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Write Output Files

## Step 10: Write to $JAAN_OUTPUTS_DIR/detect/dev/

Create directory `$JAAN_OUTPUTS_DIR/detect/dev/` if it does not exist.

**Platform-specific output path logic**:

```python
# Determine filename suffix
if current_platform == 'all' or current_platform is None:  # Single-platform
  suffix = ""                                               # No suffix
else:  # Multi-platform
  suffix = f"-{current_platform}"                          # e.g., "-web", "-backend"
```

### Stale File Cleanup

- **If `run_depth == "full"`:** Delete any existing `summary{suffix}.md` in the output directory (stale light-mode output).
- **If `run_depth == "light"`:** Do NOT delete existing full-mode files (they may be from a previous `--full` run).

### If `run_depth == "light"`: Write Single Summary File

Write one file: `$JAAN_OUTPUTS_DIR/detect/dev/summary{suffix}.md`

Contents:
1. Universal YAML frontmatter with `platform` field, `findings_summary`, and `overall_score`
2. **Executive Summary** — BLUF of tech stack findings
3. **Tech Stack Table** — languages, frameworks, versions, confidence levels (from Step 2)
4. **Database & Container Table** — detected databases, Docker images (from Step 3)
5. **Top Findings** — up to 5 highest-severity findings with evidence blocks
6. **Score Disclaimer** — "Score based on config + container layers only (Layers 1-2). Run with `--full` for complete engineering audit including CI/CD, security, infrastructure, observability, and risk assessment."

### If `run_depth == "full"`: Write 9 Output Files

For each of the 9 output files, use the template from `$JAAN_TEMPLATES_DIR/jaan-to-detect-dev.template.md` and fill with findings:

| File | Content |
|------|---------|
| `$JAAN_OUTPUTS_DIR/detect/dev/stack{suffix}.md` | Tech stack with version evidence |
| `$JAAN_OUTPUTS_DIR/detect/dev/architecture{suffix}.md` | Architecture patterns and data flow |
| `$JAAN_OUTPUTS_DIR/detect/dev/standards{suffix}.md` | Coding standards and conventions |
| `$JAAN_OUTPUTS_DIR/detect/dev/testing{suffix}.md` | Test coverage and strategy |
| `$JAAN_OUTPUTS_DIR/detect/dev/cicd{suffix}.md` | CI/CD pipelines and security |
| `$JAAN_OUTPUTS_DIR/detect/dev/deployment{suffix}.md` | Deployment patterns |
| `$JAAN_OUTPUTS_DIR/detect/dev/security{suffix}.md` | Security posture and findings (OWASP mapping) |
| `$JAAN_OUTPUTS_DIR/detect/dev/observability{suffix}.md` | Logging, metrics, tracing |
| `$JAAN_OUTPUTS_DIR/detect/dev/risks{suffix}.md` | Technical risks and debt |

**Note**: `{suffix}` is empty for single-platform mode, or `-{platform}` for multi-platform mode.

Each file MUST include:
1. Universal YAML frontmatter with `platform` field and findings_summary/overall_score
2. Executive Summary
3. Scope and Methodology
4. Findings with evidence blocks (using E-DEV-{PLATFORM}-NNN or E-DEV-NNN IDs)
5. Recommendations
6. Appendices (if applicable)

## Step 10a: Seed Reconciliation

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/seed-reconciliation-reference.md` for comparison rules, discrepancy format, and auto-update protocol.

1. Read domain-relevant seed files: `$JAAN_CONTEXT_DIR/tech.md`
2. Compare detection results against seed content (versions, frameworks, patterns, infrastructure, CI/CD, constraints, tech debt)
3. If discrepancies found:
   - Display discrepancy table to user
   - Offer auto-updates for non-destructive changes (version bumps, new entries): `[y/n]`
   - Suggest `/jaan-to:learn-add` commands for patterns worth documenting
4. If no discrepancies: display "Seed files are aligned with detection results."

## Step 10b: Record Audit State

Write audit state to `$JAAN_OUTPUTS_DIR/detect/dev/.audit-state.yaml`:

```yaml
last_audit:
  timestamp: "{ISO 8601 UTC}"
  commit: "{git HEAD short hash}"
  branch: "{current branch name}"
  mode: "{light|full}"
  incremental: {true|false}
  platforms: ["{platform_name}"]
  findings_count:
    critical: 0
    high: 0
    medium: 0
    low: 0
    informational: 0
  overall_score: 0.0
  files_written: ["summary.md"]
```

This file enables `--incremental` mode on subsequent runs.

---

## Step 11: Quality Check & Definition of Done

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-dev-reference.md` section "Quality Check & Definition of Done" for the complete checklists (light mode and full mode).

---

## Step 12: Capture Feedback

> "Any feedback on the engineering audit? Anything missed or incorrect? [y/n]"

If yes:
- Run `/jaan-to:learn-add detect-dev "{feedback}"`

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Evidence-based findings with confidence scoring
- Fork-isolated execution (`context: fork`)
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] Repository scanned with all applicable checkers
- [ ] Findings reported with SARIF-compatible evidence and 4-level confidence
- [ ] OpenSSF-style score calculated
- [ ] DORA metrics extracted from git log (deployment frequency, lead time) if git history available
- [ ] ISO 25010 quality characteristics mapped to OpenSSF scoring dimensions
- [ ] Mutation testing presence detected (stryker.config.*, infection.json5, mutmut, go-mutesting)
- [ ] Output written to `$JAAN_OUTPUTS_DIR/detect/dev/`
- [ ] User approved final report
