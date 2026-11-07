---
name: agent-ready
description: Make a codebase agent-ready by scaffolding AGENTS.md, ARCHITECTURE.md, and docs/ structure, installing regression-aware quality gates, and recommending project-local, stack-specific skills. Analyzes codebase structure, generates documentation artifacts following progressive disclosure patterns, installs report/check/baseline quality-gate commands with merge-base-aware CI and a human-reviewed baseline, and audits existing artifacts for staleness and coherence. Use when improving a codebase for AI agent work.
---

# Agent-Ready

Scaffold the documentation and structural artifacts that make a codebase legible to AI agents. This skill is the **remediation companion** to codebase-readiness -- it does not score, it builds.

---

## Startup: Check for Prior Assessment

Before entering any mode, check if `AGENT_READY_ASSESSMENT.md` exists in the project root.

If it exists:
1. Read it and extract dimension scores
2. Auto-suggest a mode based on the weakest dimensions:
   - Documentation & Context < 50 -> suggest **agents-md** first
   - Architecture Clarity < 50 -> suggest **architecture** first
   - Both < 50 -> suggest **scaffold** (full setup)
   - Quality gates at L0-L2 in the snapshot (or Code Clarity / Change Safety < 50 with no debt gate in the evidence) -> suggest **quality-gates**
3. Tell the user: "I found an existing assessment. Based on your scores, I recommend starting with [mode]. Want to proceed, or choose a different mode?"

If it does not exist, proceed with mode detection.

---

## Mode Detection

Determine which mode to run based on user intent:

| User Intent | Mode | Trigger Phrases |
|-------------|------|-----------------|
| Full documentation setup | **scaffold** | "make this agent-ready", "full setup", "scaffold docs" |
| Generate architecture doc | **architecture** | "create ARCHITECTURE.md", "architecture doc", "codemap" |
| Create/refactor AGENTS.md | **agents-md** | "set up AGENTS.md", "create AGENTS.md", "refactor AGENTS.md" |
| Install regression-aware quality gates | **quality-gates** | "set up quality gates", "block new complexity", "baseline our tech debt", "stop agents adding dead code", "regression gate" |
| Upgrade a prior agent-ready scaffold | **migrate** | "migrate agent-ready", "upgrade our agent docs", "modernize agent-ready" |
| Check existing artifacts | **audit** | "audit docs", "are my docs up to date", "check agent readiness" |

If intent is ambiguous, ask the user which mode they want.

---

## Startup: Recommend Project Skills

After selecting a mode and before making project changes, read `references/recommended-skills.md` and inspect the repository for its documented framework signals.

When one or more catalog entries match:
1. Check project-local skills and exclude any that are already installed
2. Present core matches under **Recommended** and qualifying UI matches under **Optional**, with the detected signal, skill, source, and short rationale
3. Ask once whether to install recommended skills only, recommended plus optional skills, a selected subset, or none; do not select optional skills by default
4. Wait for explicit confirmation; never install a skill based only on detection
5. Install confirmed skills from the repository root with the catalog commands, which omit `--global` to preserve project scope
6. Report install results and continue the selected agent-ready mode even if an install fails

When nothing matches or all matching skills are installed, continue without prompting. Do not recommend uncataloged skills merely because they seem related.

---

## Mode: scaffold

Full documentation setup. This is the comprehensive mode that creates everything a codebase needs for agent legibility.

### Step 1: Reconnaissance

Gather project metadata:

```bash
# Language and framework detection
ls package.json Gemfile requirements*.txt pyproject.toml go.mod Cargo.toml build.sbt pom.xml *.csproj 2>/dev/null

# Directory structure
find . -maxdepth 3 -type d 2>/dev/null | grep -v node_modules | grep -v .git | grep -v vendor | grep -v ".bundle" | grep -v __pycache__ | sort | head -50

# Existing documentation
find . -maxdepth 2 -name "AGENTS.md" -o -name "CLAUDE.md" -o -name "ARCHITECTURE.md" -o -name "README.md" -o -name "CONTRIBUTING.md" 2>/dev/null | grep -v node_modules | grep -v .git
ls -la docs/ doc/ 2>/dev/null
find docs/ doc/ -name "*.md" 2>/dev/null | head -20

# Build/test/lint commands
cat package.json 2>/dev/null | grep -A5 '"scripts"'
cat Makefile 2>/dev/null | grep -E "^[a-zA-Z_-]+:" | head -10
cat Rakefile 2>/dev/null | head -20
ls .eslintrc* .rubocop.yml .prettierrc* pyproject.toml ruff.toml .golangci.yml 2>/dev/null

# CI configuration
ls .github/workflows/*.yml .circleci/config.yml .buildkite/*.yml Jenkinsfile 2>/dev/null

# Domain documentation and ADRs
find . -maxdepth 3 \( -name "CONTEXT.md" -o -name "CONTEXT-MAP.md" -o -name "DOMAIN.md" \) 2>/dev/null | grep -v node_modules | grep -v .git
find . -type d \( -name "decisions" -o -name "adr" -o -name "adrs" \) 2>/dev/null | grep -v node_modules | grep -v .git

# Compatibility signals for the Matt Pocock design workflow
find .agents .claude -maxdepth 3 -type d \( -name "grill-with-docs" -o -name "domain-modeling" -o -name "grilling" \) 2>/dev/null
```

### Step 2: Report Inventory

Present a clear inventory to the user:

```
## Documentation Inventory

### Exists
- [List each existing artifact with path and line count]

### Missing
- [List each missing artifact that will be created]

### Will Create
- docs/ directory structure
- docs/README.md (documentation index)
- ARCHITECTURE.md (codemap, invariants, and dependency rules)
- docs/DOMAIN.md (business workflows, relationships, and compliance context)
- AGENTS.md (progressive disclosure entry point)
- AGENTS.md (also recognized by Claude Code 2.1.277+; no CLAUDE.md alias needed)
- docs/adr/ (only when a qualifying decision is made; no starter ADR)
- Documentation check: scripts/docs-check.py, CI job, and a Definition of Done directive
- Quality gate: scripts/quality-gate.py, .quality-gate.json, CI job, docs/guides/quality-gates.md, gate self-test (baseline created only after review -- see Step 7)
```

### Step 3: Create docs/ Structure

Read `assets/docs-structure-template.md` for the recommended layout.

Create only the directories needed now:
```bash
mkdir -p docs/architecture docs/guides docs/references scripts .github/workflows
cp "<skill-dir>/assets/docs-check.py" scripts/docs-check.py
cp "<skill-dir>/assets/docs-check-ci-template.yml" .github/workflows/docs-check.yml
chmod +x scripts/docs-check.py
```

Create `docs/README.md` as an index. Populate it based on what documentation exists and what will be created. Link `CONTEXT.md` only if it already exists. Do not create `docs/adr/` or `CONTEXT.md` until they have content.

Before generating domain or architecture documentation, present a **documentation design checkpoint**. Separate facts discovered in reconnaissance from the decisions only the team can make: whether domain terminology is already settled, whether a multi-context map is needed, and whether any durable architectural decision is being made. If compatible `grill-with-docs`, `grilling`, or `domain-modeling` skills are installed and terminology or trade-offs remain unsettled, recommend that workflow. Do not invoke it automatically or block scaffolding that does not need it.

### Step 4: Generate ARCHITECTURE.md

Execute the **architecture** mode logic (see below) inline. Do not launch a separate agent.

### Step 5: Generate docs/DOMAIN.md

Read `assets/domain-knowledge-template.md` for the template.

Seed the template by scanning the codebase:

```bash
# Find model/entity/type names
find . -type f \( -name "*.rb" -o -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.java" \) 2>/dev/null \
  | grep -v node_modules | grep -v .git | grep -v vendor \
  | xargs grep -lE "class |model |entity |type |interface |struct " 2>/dev/null | head -20

# Look for model directories
find . -type d \( -name "models" -o -name "entities" -o -name "types" -o -name "schemas" -o -name "domain" \) 2>/dev/null \
  | grep -v node_modules | grep -v .git | grep -v vendor

# Read README for business context
cat README.md 2>/dev/null | head -80
```

Using the discovered model/entity names and README context:
1. Do not create or infer glossary entries. If `CONTEXT.md` or `CONTEXT-MAP.md` exists, read the relevant context and use its vocabulary.
2. Sketch relationships only where code associations or existing documentation supports them; mark inferences for review.
3. Leave workflow and regulatory sections as template placeholders if not enough context exists.

Write the result to `docs/DOMAIN.md`. Link `CONTEXT.md` if it exists, but do not create it speculatively. Recommend a domain-modeling workflow when the team needs to resolve new canonical terms.

### Step 6: Generate AGENTS.md

Execute the **agents-md** mode logic (see below) inline. Do not launch a separate agent.

### Step 7: Install Quality Gates

Execute the **quality-gates** mode logic (see below) inline. The Definition of Done written in Step 6 must reference the gate's `check` command, so if Step 6 ran before the command name was known, update AGENTS.md now.

Do not skip the baseline review protocol to keep scaffold moving: if the user is not ready to review the baseline, install the engine, config, CI, docs, and tests, leave the baseline uncreated, and record in the summary that `check` will fail until a baseline is created and approved.

### Step 8: Summary

Present everything created with file paths, and suggest next steps:
- Review `docs/DOMAIN.md` and verify every inferred workflow or relationship
- Resolve domain terminology through `CONTEXT.md` only when terms are actually decided
- Create an ADR only when the decision is hard to reverse, surprising without context, and the result of a real trade-off
- Run `python3 scripts/docs-check.py` after changing Markdown links or documentation paths
- Review and approve the quality-gate baseline PR, then add `.quality-baseline.json` to CODEOWNERS
- Run `agent-ready audit` periodically to check for drift

---

## Mode: architecture

Generate an ARCHITECTURE.md from actual codebase analysis.

### Step 1: Map the Codebase

```bash
# Top-level structure
find . -maxdepth 2 -type d 2>/dev/null | grep -v node_modules | grep -v .git | grep -v vendor | grep -v ".bundle" | grep -v __pycache__ | sort

# Identify major modules and entry points
find . -maxdepth 2 -type f -name "*.ts" -o -name "*.js" -o -name "*.rb" -o -name "*.py" -o -name "*.go" -o -name "*.java" -o -name "*.scala" 2>/dev/null | grep -v node_modules | grep -v .git | grep -v vendor | head -50

# Entry points
ls src/index.* src/main.* app/main.* main.* cmd/ 2>/dev/null
ls config/ 2>/dev/null

# Largest files (potential god objects)
find . -name "*.ts" -o -name "*.js" -o -name "*.rb" -o -name "*.py" -o -name "*.go" -o -name "*.java" 2>/dev/null \
  | grep -v node_modules | grep -v .git | grep -v vendor | grep -v spec | grep -v test \
  | xargs wc -l 2>/dev/null | sort -rn | head -15
```

### Step 2: Detect Patterns

Read source files to identify:
- **Layers:** controllers/handlers, services, repositories/models, utilities
- **Domains:** distinct business domains grouped in the filesystem
- **Entry points:** where the application starts, what the main interfaces are
- **Configuration:** how the app is configured, environment handling
- **Cross-cutting:** logging, auth, error handling, middleware

### Step 3: Read Existing Context

Read README.md and any existing documentation for project context. Before mapping a domain, read the relevant `CONTEXT.md`, or resolve it through `CONTEXT-MAP.md` when present. Read ADRs that affect the area from `docs/adr/`, `docs/decisions/`, or the project's established ADR location. Use canonical domain vocabulary and explicitly surface an ADR conflict rather than silently overriding it. Do not duplicate what README already covers -- ARCHITECTURE.md complements it.

### Step 4: Load References

Read `references/architecture-guide.md` for matklad's principles.
Read `assets/architecture-md-template.md` for the output template.

### Step 5: Generate ARCHITECTURE.md

Using the template and principles, generate an ARCHITECTURE.md with:
- **Overview:** One paragraph describing the problem domain (not the tech stack)
- **Codemap:** Every significant top-level directory with one-line descriptions. Name important files and types.
- **Invariants:** Rules that hold across the codebase. **Always include absences** -- things that deliberately do not exist.
- **Boundaries:** Public vs internal APIs. Layer dependency rules. Which modules can import which.
- **Cross-cutting concerns:** How logging, auth, errors, and config work across the system.
- **Domain terminology:** Use the applicable `CONTEXT.md` vocabulary when one exists. Do not invent a competing glossary.

### Step 6: Present and Confirm

Show the draft to the user. Write to `ARCHITECTURE.md` in the project root on confirmation.

---

## Mode: agents-md

Create a new AGENTS.md or refactor an existing one for progressive disclosure. Claude Code 2.1.277+ reads AGENTS.md directly, so do not create or require a CLAUDE.md symlink.

### Step 1: Assess Current State

Check if AGENTS.md or CLAUDE.md exists:

```bash
find . -name "AGENTS.md" -o -name "CLAUDE.md" 2>/dev/null | grep -v node_modules | grep -v .git
```

**If AGENTS.md exists**, analyze it:
```bash
wc -l AGENTS.md
# Code block percentage
echo "Code block lines: $(sed -n '/^```/,/^```/p' AGENTS.md | wc -l)"
# Directive density
echo "Directive keywords: $(grep -ci 'must\|never\|always\|avoid\|prefer' AGENTS.md)"
# Doc links
echo "Doc links: $(grep -coE '\[.*\]\([^)]+\.md\)' AGENTS.md)"
# Section count
echo "Sections: $(grep -c '^##' AGENTS.md)"
```

Read the existing AGENTS.md fully. Identify:
- Sections that are bloated (>30 lines on one topic)
- Code examples that are too long (>10 lines)
- Content that belongs in topic docs, not AGENTS.md
- Missing directives (build, test, lint commands)
- Missing links to supporting docs

**If CLAUDE.md exists but not AGENTS.md**, analyze CLAUDE.md the same way and plan to migrate it to AGENTS.md.

**If neither exists**, proceed to generation.

### Step 2: Load References

Read `references/progressive-disclosure.md` for Harness Engineering principles.
Read `assets/agent-ready-template.md` for the output template that generates AGENTS.md content.

### Step 3: Detect Project Signals

Gather the information needed to populate AGENTS.md:

```bash
# Build/test/lint commands
cat package.json 2>/dev/null | grep -A10 '"scripts"'
cat Makefile 2>/dev/null | grep -E "^[a-zA-Z_-]+:" | head -10
ls .eslintrc* .rubocop.yml .prettierrc* ruff.toml .golangci.yml 2>/dev/null

# CI config (for workflow hints)
ls .github/workflows/*.yml 2>/dev/null

# Existing docs to link
find docs/ doc/ -name "*.md" 2>/dev/null | head -20
ls ARCHITECTURE.md CONTRIBUTING.md 2>/dev/null

# Domain context and ADRs
find . -maxdepth 4 \( -name "CONTEXT.md" -o -name "CONTEXT-MAP.md" \) 2>/dev/null | grep -v node_modules | grep -v .git
find . -path "*/decisions/*.md" -o -path "*/adr/*.md" -o -path "*/adrs/*.md" 2>/dev/null | grep -v node_modules | grep -v .git | head -5
```

### Step 4: Generate or Refactor

**New AGENTS.md:**
Using the template, generate an AGENTS.md that:
- Stays under ~120 lines
- Leads with project identity and build/test/lint one-liners
- Includes a **Session Startup** section with the bearing-getting ritual (pwd, git log, fetch origin, sync with the upstream default branch using the repo's merge/rebase strategy, smoke test) -- fill in the smoke-test command from detected scripts, or leave a `[TODO: add smoke-test command]` placeholder if nothing is detected
- Uses directives (must/never/always/avoid/prefer) for conventions
- Includes a **Definition of Done** section codifying end-to-end verification before marking work complete -- fill in lint/test commands from detected tooling, and the quality-gate `check` command if `.quality-gate.json` (or a native gate such as `golangci-lint` with `new-from-merge-base`, `detekt --baseline`, or a PHPStan baseline) exists or is about to be installed by scaffold
- Includes three quality-gate directives (run `check` before finishing; never edit, extend, or approve the baseline; run `baseline --prune` when `check` reports stale entries) under Key Conventions or Definition of Done, not as a new section
- If the repo already uses machine-updated ledgers such as `tasks.json`, status queues, or work trackers, include a directive that names exactly which fields agents may edit
- Markdown links to existing docs or docs that should be created
- Links `CONTEXT.md` or `CONTEXT-MAP.md` when one exists, without duplicating its glossary
- Includes an ADR section that states the three-part eligibility rule: hard to reverse, surprising without context, and a real trade-off
- Adds a documentation-check directive when `scripts/docs-check.py` exists or scaffold is about to install it
- Lists max 5 known gotchas
- Avoids code examples longer than 5 lines

**Refactoring existing AGENTS.md or migrating from CLAUDE.md:**
1. Identify bloated sections
2. Extract content to appropriate docs/ files (create them)
3. Replace extracted content with markdown links
4. Tighten language to directives
5. Present before/after comparison showing:
   - Line count reduction
   - Content moved to which files
   - New doc links added

### Step 5: Handle Legacy CLAUDE.md (only if present)

Claude Code supports AGENTS.md directly starting with version 2.1.277 ([announcement](https://x.com/trq212/status/2101009392611278961)). Do not create a CLAUDE.md symlink, replace an existing CLAUDE.md, or require AGENTS.md and CLAUDE.md to be aliases. If CLAUDE.md is the only instruction file, use it as source material for AGENTS.md; preserve the original unless the user explicitly asks to remove or consolidate it. If both files exist independently, leave them intact and mention that their instructions may need reconciliation if they conflict.

### Step 6: Present and Confirm

Show the draft (or before/after diff for refactoring). Write AGENTS.md on confirmation.

---

## Mode: quality-gates

Install a regression-aware quality gate: the project's native complexity, duplication, and dead-code checks, a baseline that lets legacy debt stay while new or worsened debt fails, merge-base-aware PR CI, reproducible local commands, docs, and tests of the gate. Read `references/quality-gates-pattern.md` first; it defines the contract and the per-language adapters.

Never run this mode to make a failing gate pass. If a gate exists and `check` is red, fix the code or prune stale entries; do not extend the baseline.

### Step 1: Detect Tools and Existing Gates

```bash
# Language and existing analyzers
ls package.json Gemfile pyproject.toml requirements*.txt go.mod Cargo.toml composer.json pom.xml build.gradle* build.sbt 2>/dev/null
ls .eslintrc* eslint.config.* biome.json .rubocop.yml .rubocop_todo.yml ruff.toml pyproject.toml .pylintrc .golangci.yml phpstan.neon* phpmd*.xml detekt*.yml pmd*.xml knip.json* .jscpd.json 2>/dev/null
grep -E '"(lint|typecheck|test|quality|gate)"' package.json 2>/dev/null

# Existing gate artifacts
ls .quality-gate.json .quality-baseline.json scripts/quality-gate.py scripts/quality-gate-test.sh docs/guides/quality-gates.md 2>/dev/null
grep -E "new-from-rev|new-from-merge-base|reportUnmatchedIgnoredErrors|baseline" .golangci.yml phpstan.neon* detekt*.yml 2>/dev/null
grep -rlE "complexity|jscpd|flay|knip|vulture|debride|gocyclo|dupl|phpmd|detekt|quality-gate" .github/workflows .gitlab-ci.yml .circleci 2>/dev/null

# Hook frameworks and CODEOWNERS
ls .husky lefthook.yml .pre-commit-config.yaml .github/CODEOWNERS CODEOWNERS 2>/dev/null
python3 --version
```

Decide the route from `references/quality-gates-pattern.md`:
- **Option A** when the native tool has a baseline or diff mode (golangci-lint, detekt, PHPStan, RuboCop todo). Prefer it; no custom engine needed.
- **Option B** otherwise: install `assets/quality-gate.py` and write adapters that emit the contract format.

If a partial gate already exists, extend it toward the contract rather than replacing it. Report what exists and what is missing before changing anything.

### Step 2: Choose Checks

Pick three checks -- complexity, duplication, dead code -- from the language's recipes. Use the thresholds the project already configures where they exist; otherwise use the tool's defaults. Do not introduce a new analyzer when the project already runs one that covers the property. Skip a property only when no reliable tool exists for the stack, and say so.

**Run every candidate command by hand** and confirm it emits the contract format (one finding per line, `unix` or `jsonl`). Fix the adapter until it does.

### Step 3: Install Commands

**Option B:**

```bash
mkdir -p scripts
cp "<skill-dir>/assets/quality-gate.py" scripts/quality-gate.py
chmod +x scripts/quality-gate.py
```

Write `.quality-gate.json` with the confirmed checks, `base_ref` set to the repository's default branch (`origin/main` or `origin/master`), and `baseline` at `.quality-baseline.json`. Add `__pycache__/` to `.gitignore` if it is not already ignored.

Adapters that need more than a shell one-liner (JSON reshaping, temp dirs for a reporter) belong in one small script in the project's own language -- for example `scripts/quality-gate-adapter.mjs complexity|duplication|dead-code` -- rather than in the JSON config.

**Both options:** expose `report`, `check`, and `baseline --prune` through the project's task runner so the commands read naturally for the stack -- `make quality-report` / `quality-check`, `npm run quality:check`, `bundle exec rake quality:check`, `just quality-check`. The task-runner entry must call exactly what CI calls.

### Step 4: Report, Then Baseline With Review

```bash
python3 scripts/quality-gate.py report
```

Present the findings grouped by rule and top files. Ask which are cheap enough to fix now -- fixing before baselining is always preferred. Then:

```bash
python3 scripts/quality-gate.py baseline --reason "<user's reason>" --dry-run
```

Show the candidate summary. Only on the user's explicit confirmation run it without `--dry-run`. State clearly that the baseline is written **unreviewed**, that `check` fails until a reviewer runs `baseline --approve --reviewed-by "<name>"`, and that this is by design. Do not run `--approve` on the user's behalf. For Option A tools, the equivalent is committing the generated baseline/todo file in a PR that a named reviewer approves.

If the user declines to baseline now, skip this step; everything else still gets installed and `check` will report the legacy findings as new until a baseline exists.

### Step 5: Wire CI, Hooks, and Protection

- **CI (required):** read `assets/quality-gate-ci-template.yml`; copy to `.github/workflows/quality-gate.yml` (or add the equivalent steps to the existing pipeline for other CI systems). Keep `fetch-depth: 0` and the base-branch fetch so the merge-base resolves. No `continue-on-error`.
- **Hooks (recommended):** if lefthook, husky, or pre-commit exists, add `check --changed-only` as a pre-push step.
- **CODEOWNERS (required):** add `.quality-baseline.json` (or the native baseline file) with a named owner so extending it always needs a human.

### Step 6: Docs and AGENTS.md

- Read `assets/quality-gates-guide-template.md`, fill in the commands, tools, and thresholds, and write `docs/guides/quality-gates.md`. Add it to `docs/README.md`.
- In AGENTS.md: add the `check` command to **Definition of Done**, and add three directives (run `check` before finishing; never edit, extend, or approve the baseline; run `baseline --prune` when `check` reports stale entries). Link the guide from **Common Workflows**. If AGENTS.md does not exist, run agents-md mode.

### Step 7: Tests of the Gate

Copy `assets/quality-gate-test-template.sh` to `scripts/quality-gate-test.sh`. Fill in `FIXTURE_PATH` (a file the complexity check scans that does not exist yet) and `FIXTURE_BODY` (a function over the threshold in the project's language; snippets are in the pattern reference). Run it and confirm all five assertions pass -- the self-test marks its temporary baseline copy as reviewed, so it passes before the real baseline is approved while `check` stays red. Wire it into the project's test command and the CI job.

For Option A, write the equivalent three assertions against the native tool: a clean tree passes, a fixture over the threshold fails, and a regenerated baseline drops a fixed finding.

### Step 8: Summary

```
## Quality Gate Installed

| Check | Tool | Threshold | Findings baselined |
|-------|------|-----------|--------------------|

- Route: [Option A: native <tool> mode / Option B: scripts/quality-gate.py]
- Commands: [report / check / prune, as exposed in the task runner]
- Baseline: [N entries, UNREVIEWED -- approve with ... / not created]
- CI: .github/workflows/quality-gate.yml (merge-base aware, annotates PRs)
- CODEOWNERS: [entry added / TODO]
- Docs: docs/guides/quality-gates.md; AGENTS.md Definition of Done updated
- Tests: scripts/quality-gate-test.sh (5 assertions passing)

Next steps:
- Open a PR with these files; the reviewer inspects the baseline and runs `baseline --approve --reviewed-by "<name>"`
- Fix the cheap findings identified in Step 4 and run `baseline --prune` to lock in the gain
```

---

## Mode: migrate

Upgrade a repository scaffolded by an older agent-ready version to the current documentation contract. This mode is conservative: preserve content and history, present a migration plan, and wait for explicit confirmation before changing files.

### Step 1: Detect Legacy Artifacts

Inventory the root agent entrypoints, `docs/DOMAIN.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, ADR directories, documentation indexes, documentation-check scripts and CI jobs. Flag these legacy patterns:
- `docs/DOMAIN.md` contains a glossary but no `CONTEXT.md`
- ADRs live in `docs/decisions/` rather than the current `docs/adr/` layout
- A starter `001-agent-ready-documentation.md` exists
- AGENTS.md lacks Session Startup, Definition of Done, the ADR eligibility rule, or a documentation-check directive
- Documentation links and context-map targets are not checked in CI

Read every affected file. Do not infer synonym preferences, rewrite a glossary, or classify a document as disposable based only on its filename.

### Step 2: Present the Migration Plan

Show a file-by-file plan with source, destination, and whether content will be copied, moved with `git mv`, or edited in place. The recommended plan is:
1. Keep `AGENTS.md` as the shared agent-instructions file; Claude Code 2.1.277+ reads it natively. Do not create or require a `CLAUDE.md` symlink; preserve any existing CLAUDE.md unless explicitly asked to consolidate.
2. Promote confirmed entries from `docs/DOMAIN.md`'s glossary into root `CONTEXT.md`. Preserve definitions verbatim; ask the team to resolve `_Avoid_` synonyms rather than guessing. Remove the migrated glossary from DOMAIN.md and add a link to CONTEXT.md.
3. Move ADRs to `docs/adr/` with `git mv`, preserve their contents and numbering, and update every in-repo link. Do not delete the old starter ADR; retain it as historical context and exclude it from ADR-quality credit if it is boilerplate.
4. Update `docs/README.md`, AGENTS.md, and ARCHITECTURE.md links to the new topology.
5. Install `scripts/docs-check.py` and `.github/workflows/docs-check.yml`; add the scoped Definition of Done directive.

If the project deliberately uses a different ADR directory or maintains multiple bounded contexts, present that as an alternative and preserve it on explicit request. Never run the recommended plan without confirmation.

### Step 3: Migrate and Verify

After confirmation:
- use `git mv` for tracked ADR paths;
- update links in the same change;
- generate CONTEXT.md only from reviewed, existing glossary entries;
- leave unresolved or duplicate terminology for a domain-modeling session;
- run `python3 scripts/docs-check.py` and the project's normal documentation or test checks;
- finish with `agent-ready audit` and report remaining manual decisions.

---

## Mode: audit

Check health of existing agent-readiness artifacts.

### Step 1: Inventory

Find all agent-readiness artifacts:

```bash
# AGENTS.md and CLAUDE.md files (root and nested)
find . -name "AGENTS.md" -o -name "CLAUDE.md" 2>/dev/null | grep -v node_modules | grep -v .git

# Note any legacy CLAUDE.md independently; it is not required to alias AGENTS.md
if [ -f CLAUDE.md ]; then
  echo "CLAUDE.md exists independently (not required for Claude Code 2.1.277+)"
fi

# ARCHITECTURE.md and domain context
find . -name "ARCHITECTURE.md" 2>/dev/null | grep -v node_modules | grep -v .git
find . -maxdepth 4 \( -name "CONTEXT.md" -o -name "CONTEXT-MAP.md" -o -name "DOMAIN.md" \) 2>/dev/null | grep -v node_modules | grep -v .git

# docs/ contents
find docs/ doc/ -type f 2>/dev/null | grep -v node_modules | grep -v .git

# ADRs
find . -path "*/decisions/*.md" -o -path "*/adr/*.md" -o -path "*/adrs/*.md" 2>/dev/null | grep -v node_modules | grep -v .git
```

### Step 2: Staleness Checks

**ARCHITECTURE.md vs actual structure:**
- Read ARCHITECTURE.md and extract mentioned directories/modules
- Compare against actual directory tree
- Flag directories mentioned in ARCHITECTURE.md that no longer exist
- Flag significant directories that exist but are not mentioned

**Linked doc resolution:**
```bash
# Check both AGENTS.md and CLAUDE.md for broken links
for doc in AGENTS.md CLAUDE.md; do
  if [ -f "$doc" ]; then
    grep -oE '\[.*\]\([^)]+\.md\)' "$doc" 2>/dev/null | grep -oE '\([^)]+\)' | tr -d '()' | while read -r ref; do
      if [ ! -f "$ref" ]; then
        echo "BROKEN in $doc: $ref not found"
      fi
    done
  fi
done
```

**ADR recency and context-map resolution:**
```bash
find . -path "*/decisions/*.md" -o -path "*/adr/*.md" 2>/dev/null | grep -v node_modules | xargs ls -lt 2>/dev/null | head -5
if [ -f CONTEXT-MAP.md ]; then
  grep -oE '\]\([^)]+CONTEXT\.md\)' CONTEXT-MAP.md | tr -d '[]()' | while read -r ref; do
    [ -f "$ref" ] || echo "BROKEN context-map target: $ref"
  done
fi
```

### Step 3: Coherence Checks

Run the coherence analysis from the codebase-readiness documentation dimension:

```bash
# AGENTS.md content type analysis (use AGENTS.md as primary, fall back to legacy CLAUDE.md only when AGENTS.md is absent)
DOC="AGENTS.md"
if [ ! -f "$DOC" ] && [ -f "CLAUDE.md" ] && [ ! -L "CLAUDE.md" ]; then
  DOC="CLAUDE.md"
fi

if [ -f "$DOC" ]; then
  echo "Analyzing: $DOC"
  echo "Total lines: $(wc -l < "$DOC")"
  echo "Code block lines: $(sed -n '/^```/,/^```/p' "$DOC" | wc -l)"
  echo "Directive keywords (must/never/always/avoid/prefer): $(grep -ci 'must\|never\|always\|avoid\|prefer' "$DOC")"
  TOTAL=$(wc -l < "$DOC")
  CODE=$(sed -n '/^```/,/^```/p' "$DOC" | wc -l)
  if [ "$TOTAL" -gt 0 ]; then
    PCT=$(( CODE * 100 / TOTAL ))
    echo "Code example percentage: ${PCT}%"
  fi

  # Session Startup section -- bearing-getting ritual for fresh contexts
  if grep -qiE '^##+ .*(session startup|getting (started|up to speed)|orient)' "$DOC"; then
    echo "✓ Session Startup section present"
  else
    echo "⚠ MISSING: Session Startup section -- agents have no prescribed orientation sequence on fresh contexts"
  fi

  # Definition of Done section -- end-to-end verification protocol
  if grep -qiE '^##+ .*(definition of done|verification|done criteria)' "$DOC"; then
    DOD_SECTION=$(awk '
      BEGIN { capture=0 }
      /^##+[[:space:]]/ {
        if (capture) exit
      }
      /^##+[[:space:]].*(Definition of Done|Verification|Done Criteria)/ {
        capture=1
      }
      capture { print }
    ' "$DOC")

    if printf "%s\n" "$DOD_SECTION" | grep -qiE 'end-to-end|end to end|browser|exercise'; then
      echo "✓ Definition of Done section present (mentions end-to-end verification)"
    else
      echo "⚠ Definition of Done section present but does not mention end-to-end verification"
    fi
  else
    echo "⚠ MISSING: Definition of Done section -- no codified end-to-end verification protocol"
  fi
fi

# CLAUDE.md is optional; do not enforce aliasing. Flag only potential instruction duplication/conflict for manual review.
if [ -f CLAUDE.md ] && [ -f AGENTS.md ]; then
  echo "ℹ Both AGENTS.md and CLAUDE.md exist; review for conflicting instructions if needed. Claude Code 2.1.277+ reads AGENTS.md directly."
fi

# Topic overlap
DOC="AGENTS.md"
if [ ! -f "$DOC" ] && [ -f "CLAUDE.md" ] && [ ! -L "CLAUDE.md" ]; then
  DOC="CLAUDE.md"
fi

for doc in $(find docs/ doc/ -name "*.md" -maxdepth 2 2>/dev/null | grep -v node_modules); do
  TOPIC=$(basename "$doc" .md | tr '[:upper:]' '[:lower:]' | sed 's/_/ /g')
  if [ -f "$DOC" ] && grep -qi "$TOPIC" "$DOC" 2>/dev/null; then
    DOC_MENTIONS=$(grep -ci "$TOPIC" "$DOC" 2>/dev/null)
    DOC_LINES=$(wc -l < "$doc" 2>/dev/null | tr -d ' ')
    echo "Overlap: '$TOPIC' -- $DOC mentions ${DOC_MENTIONS}x, dedicated doc is ${DOC_LINES} lines"
  fi
done

# Broken references
if [ -f "$DOC" ]; then
  grep -oE '\[.*\]\(\./[^)]+\)' "$DOC" 2>/dev/null | grep -oE '\./[^)]+' | while read -r ref; do
    if [ ! -f "$ref" ]; then
      echo "BROKEN link in $DOC: $ref not found"
    fi
  done
fi

# Source of truth declarations and documentation checks
find AGENTS.md CLAUDE.md CONTEXT.md CONTEXT-MAP.md docs/ -type f 2>/dev/null | xargs grep -rn "source of truth\|authoritative\|canonical\|definitive" 2>/dev/null | grep -v node_modules | grep -v .git
if [ -f scripts/docs-check.py ]; then
  python3 scripts/docs-check.py
else
  echo "⚠ MISSING: scripts/docs-check.py"
fi
grep -rl "scripts/docs-check.py" .github/workflows .gitlab-ci.yml .circleci .buildkite 2>/dev/null || echo "⚠ MISSING: documentation-check CI job"
```

### Step 4: Coverage Checks

- **Domain documentation:** Check whether `docs/DOMAIN.md` documents supported workflows and relationships, and whether `CONTEXT.md` or `CONTEXT-MAP.md` is the sole canonical glossary when domain terms have been settled. Do not flag a missing CONTEXT.md when no terms are resolved yet.
- **Domain directories without scoped instructions:** Recommend nested AGENTS.md only where a domain has local rules or gotchas, not merely because a directory exists.
- **Unlisted directories in ARCHITECTURE.md:** Find top-level source directories not mentioned in the codemap.
- **ADR discipline:** Flag boilerplate or routine ADRs, missing rationale, and ADRs that duplicate implementation notes. A small set of consequential ADRs is healthy.
- **Missing docs/ categories:** Check if guides/ and references/ are needed and populated. Do not require `docs/adr/` until a qualifying decision exists.
- **Documentation verification:** Classify link and context-map checks as CI-enforced, local-only, or absent. CLAUDE.md aliasing is not checked or required.
- **Quality gate:** Run the detection commands from `references/quality-gates-pattern.md` (`.quality-gate.json`, native baseline/diff modes, CI job, `docs/guides/quality-gates.md`, gate self-test, CODEOWNERS entry, DoD mention). Classify as: **installed and governed** (check in CI, baseline reviewed, self-test present, DoD references it), **installed but ungoverned** (missing review, tests, CODEOWNERS, or DoD mention), **report-only** (tooling runs but cannot fail CI), or **absent**. If `.quality-baseline.json` exists, run `check` and report stale entries and unreviewed status

### Step 5: Report

Present an actionable report:

```
## Agent-Readiness Audit

### Artifact Inventory
| Artifact | Status | Location | Lines |
|----------|--------|----------|-------|
| AGENTS.md (root) | [Present/Missing] | ./AGENTS.md | [N] |
| CLAUDE.md (optional legacy file) | [Present/Absent] | ./CLAUDE.md | [N/—] |
| ARCHITECTURE.md | [Present/Missing] | ./ARCHITECTURE.md | [N] |
| DOMAIN.md | [Present/Stub/Missing] | ./docs/DOMAIN.md | [N] |
| CONTEXT.md / CONTEXT-MAP.md | [Present/Absent/Not yet needed] | [path] | [N] |
| docs/ index | [Present/Missing] | ./docs/README.md | [N] |
| ADRs | [N found, consequential/boilerplate] | [path] | — |
| Nested AGENTS.md | [N found] | [locations] | — |

### Staleness Issues
- [List stale items with specific file paths and what's wrong]

### Coherence Issues
- Primary doc (AGENTS.md or CLAUDE.md) line count: [N] [OK if <150 / WARNING if >150 / CRITICAL if >300]
- Code example %: [N]% [OK if <20% / WARNING if >20%]
- Directive density: [N] directives in [M] lines
- AGENTS.md compatibility: [Claude Code 2.1.277+ reads it directly / note older-tooling constraints if relevant]
- Domain glossary authority: [CONTEXT.md / CONTEXT-MAP.md / duplicated / not yet needed]
- Documentation checks: [CI-enforced / local-only / absent]
- Session Startup section: [Present/Missing]
- Definition of Done section: [Present/Missing/Present-without-E2E]
- Topic overlaps: [list]
- Broken references: [list]
- Cross-document conflicts: [list]

### Coverage Gaps
- Directories needing scoped instructions: [list, only when local rules exist]
- Directories not in ARCHITECTURE.md: [list]
- Missing docs/ categories: [list]

### Quality Gate
- Status: [installed and governed / installed but ungoverned / report-only / absent]
- Baseline: [N entries, reviewed by X on DATE / unreviewed / none] -- stale entries: [N]
- CI: [blocks on check / continue-on-error / no job]
- Self-test: [present at ... / absent]
- DoD references check command: [yes / no]

### Recommended Actions
1. [Highest priority fix -- specific, actionable]
2. [Second priority fix]
3. [Third priority fix]
```

After presenting the report, offer to auto-fix issues:
- Broken doc links: remove or create the missing file
- Primary doc bloat: offer to run agents-md mode to refactor
- Missing ARCHITECTURE.md entries: offer to run architecture mode to regenerate
- Missing scoped AGENTS.md where local rules exist: offer to create a starter file
- Legacy DOMAIN.md/decisions topology: offer to run migrate mode
- Both AGENTS.md and CLAUDE.md present: offer to review possible instruction conflicts; do not merge, replace, or symlink automatically
- Missing Session Startup section: offer to insert the bearing-getting ritual (pwd, git log, fetch origin, sync with the upstream default branch using the repo's merge/rebase strategy, smoke test) using detected commands
- Missing Definition of Done section: offer to insert a DoD checklist using detected lint/test commands
- Quality gate absent or report-only: offer to run quality-gates mode
- Quality gate installed but ungoverned: offer the missing piece only (self-test, CODEOWNERS entry, DoD line, or a reminder that the baseline awaits `--approve`)
- Stale baseline entries: offer to run `baseline --prune` and commit the result
