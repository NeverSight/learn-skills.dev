---
name: agents-md-optimizer
description: "Optimize agent context files (AGENTS.md, CLAUDE.md, .cursorrules, .windsurfrules, .github/copilot-instructions.md, codex.md, etc.) using Addy Osmani's agents-md methodology. Triggers: 'optimize CLAUDE.md', 'streamline CLAUDE.md', 'agents-md', 'discoverability filter', 'add gotchas', 'optimize AGENTS.md', 'optimize context file', 'CLAUDE.md 최적화', 'CLAUDE.md 줄이기', 'CLAUDE.md 다이어트', 'optimize .cursorrules', 'optimize .windsurfrules', 'optimize copilot-instructions', 'optimize codex.md'."
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion]
---

# Agents-MD Optimizer

Optimize agent context files (CLAUDE.md, AGENTS.md, .cursorrules, etc.) by applying the discoverability filter: remove information agents can discover from code, keep only non-discoverable operational knowledge (gotchas, landmines, non-standard conventions), and mine source code for undocumented gotchas.

Research shows redundant context (directory trees, data flow diagrams) degrades agent performance by 15-20%, while human-authored operational knowledge reduces runtime by ~28%.

## Flag Parsing

Parse `$ARGUMENTS` for optional flags:

| Flag | Effect |
|------|--------|
| `--dry-run` | Analyze and show diff without modifying the file |
| `--report-only` | Output statistics and classification table only |
| `--path <path>` | Target file path (see auto-detection below) |
| `--help` | Display usage and exit |

If `--help` is present, display available flags and a brief description of the workflow, then stop.

## Workflow

### Phase 0: Setup

**Language Detection**: Detect the user's language from conversation history. Present all analysis results and messages in the user's language.

**Target File Resolution** (when `--path` is not specified):

Search for the first existing file in this priority order:
1. `AGENTS.md`
2. `CLAUDE.md`
3. `.cursorrules`
4. `CURSOR.md`
5. `.github/copilot-instructions.md`
6. `.windsurfrules`
7. `codex.md`

If none found, ask the user to specify the target file path.

**Small File Check**: If the target file has fewer than 20 lines, inform the user that the file is already minimal and optimization is unnecessary. Stop unless the user explicitly requests to proceed.

### Step 1: Baseline Analysis

Read the target file. Collect line statistics.

**Script Location**: Find the line-count script by searching for it:

```bash
# Search in common skill installation paths
SCRIPT_PATH=$(find ~/.claude/skills ~/.codex/skills ~/.cursor/skills ~/skills 2>/dev/null -path "*/agents-md-optimizer/scripts/line-count.mjs" | head -1)
if [ -z "$SCRIPT_PATH" ]; then
  # Fallback: search in current directory
  SCRIPT_PATH=$(find . -path "*/agents-md-optimizer/scripts/line-count.mjs" 2>/dev/null | head -1)
fi
```

Run the script if found:

```bash
node "$SCRIPT_PATH" '<TARGET_PATH>'
```

**Fallback** (if script not found): Count lines manually using Bash:

```bash
wc -l '<TARGET_PATH>'
grep -c '^##' '<TARGET_PATH>'
```

Then classify each `##`/`###` section into one of three categories:

| Category | Meaning | Action |
|----------|---------|--------|
| `discoverable` | Agent can find this via Glob/Grep/Read within 10 seconds | Remove |
| `operational` | Non-discoverable, operationally significant | Keep |
| `verbose` | Operational knowledge but overly detailed | Compress |

To classify, **actually read the source files** referenced in each section. Verify whether the information is truly discoverable. Detailed classification criteria are in [`references/methodology.md`](references/methodology.md).

Present results as a table:

```
## Baseline Analysis — <filename>

Total: XXX lines (YY sections)

| Section | Lines | Category | Rationale |
|---------|-------|----------|-----------|
| Directory Structure | 63 | discoverable | Glob **/* reveals this instantly |
| Design Rules | 8 | operational | Non-standard constraints, not in code |
| Config & State | 24 | verbose | Operational but compressible to ~6 lines |

Removal candidates: XX lines (XX%)
```

If `--report-only`, stop here.

### Step 2: Gotcha Mining

Scan project source code to find non-obvious operational knowledge missing from the target file. Use the systematic checklist in [`references/gotcha-mining.md`](references/gotcha-mining.md).

Key Grep patterns to run on the codebase:

```
MUST|WARNING|HACK|TODO|FIXME          → developer-flagged gotchas
catch.*exit\(0\)|process\.exit        → error exit policies
setTimeout|setInterval|deadline       → timing constraints
=== null|== null|delete result        → implicit semantics
process\.platform|/proc/version       → platform detection quirks
cooldown|throttle|lastNotified        → rate limiting scope
```

Present findings:

```
## Discovered Gotchas

| # | Category | Description | Source | Already documented? |
|---|----------|-------------|--------|---------------------|
| 1 | Timing | 5s→4s→2s budget | _common.mjs:21,52 | No → Add |
| 2 | Implicit | null = key deletion | config.mjs:157 | No → Add |
```

### Step 3: Generate Optimized File

Use AskUserQuestion to confirm before modifying:

> Based on the analysis:
> - **Remove**: X lines of discoverable content (Y sections)
> - **Compress**: X lines → ~Y lines (Z sections)
> - **Add**: X new gotcha items
>
> Options:
> 1. **Apply all** — Remove discoverable, compress verbose, add gotchas
> 2. **Item by item** — Review each change individually
> 3. **Cancel** — No changes

Apply the selected changes using Edit (prefer surgical edits over full rewrite).

If `--dry-run`, show the diff but do not write.

**Structure for optimized file** (recommended section order):
1. Project description (1-2 lines)
2. Development Commands
3. Design Rules (non-negotiable constraints)
4. Gotchas & Landmines (categorized subsections)
5. Conventions (non-standard project patterns)
6. Version/Release Management
7. Testing

Detailed anti-pattern examples with before/after are in [`references/anti-patterns.md`](references/anti-patterns.md).

### Step 4: Verification

Re-run statistics (using the same script or fallback method from Step 1) and present before/after comparison:

```
## Optimization Results

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total lines | 182 | 90 | -51% |
| Discoverable lines | 80 | 0 | Removed |
| Operational lines | 60 | 55 | Kept |
| Gotcha items | 0 | 25 | Added |

Discoverability filter: all remaining lines pass "not discoverable from code" check.
```

## Reference Files

- **[`references/methodology.md`](references/methodology.md)** — Discoverability filter decision tree, category classification criteria, compression techniques, efficiency research data
- **[`references/anti-patterns.md`](references/anti-patterns.md)** — 6 anti-pattern catalog with real before/after examples
- **[`references/gotcha-mining.md`](references/gotcha-mining.md)** — 8-category mining checklist with Grep patterns and source code analysis techniques
