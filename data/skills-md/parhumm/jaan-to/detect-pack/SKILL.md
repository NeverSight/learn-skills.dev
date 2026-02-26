---
name: detect-pack
description: Consolidate all detect outputs into unified index with risk heatmap and unknowns backlog. Use when combining audit results.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/**), Edit(jaan-to/config/settings.yaml), Edit($JAAN_CONTEXT_DIR/**), Write($JAAN_CONTEXT_DIR/**)
argument-hint: "[repo] [--full]"
context: fork
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Partial standalone support for analysis mode.
---

# detect-pack

> Consolidate all detect outputs into a scored index with risk heatmap and unknowns backlog.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-detect-pack.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_TEMPLATES_DIR/jaan-to-detect-pack.template.md` - Output template
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` - Evidence formats, consolidation logic, output templates
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-shared-reference.md` - Shared standards: Evidence Format, Confidence Levels, Codebase Content Safety

**Output path**: `$JAAN_OUTPUTS_DIR/detect/` — flat files, overwritten each run (no IDs).

**Important**: This skill does NOT scan the repository directly. It reads and consolidates outputs from the 5 detect skills.

## Input

**Arguments**: $ARGUMENTS — parsed in Step 0.0. Repository path and mode determined there.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `detect-pack`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_detect-pack`

---

# PHASE 1: Consolidation (Read-Only)

## Step 0.0: Parse Arguments

**Arguments**: $ARGUMENTS

| Argument | Effect |
|----------|--------|
| (none) | **Light mode** (default): Heatmap + domain scores, single summary file |
| `[repo]` | Read detect outputs from specified repo (applies to both modes) |
| `--full` | **Full mode**: Full consolidation with evidence index and unknowns backlog (current behavior) |

**Mode determination:**
- If `$ARGUMENTS` contains `--full` as a standalone token → set `run_depth = "full"`
- Otherwise → set `run_depth = "light"`

Strip `--full` token from arguments. Set `repo_path` to remaining arguments (or current working directory if empty).

## Thinking Mode

**If `run_depth == "full"`:** ultrathink
**If `run_depth == "light"`:** megathink

Use extended reasoning for:
- Cross-domain pattern recognition
- Risk correlation across domains
- Evidence ID validation and deduplication
- Overall score calculation

## Step 0: Check Detect Outputs & Detect Platforms

### Check for Detect Outputs

Glob `$JAAN_OUTPUTS_DIR/detect/{dev,design,writing,product,ux}/` to see which detect skills have run.

**If NO detect outputs exist**:

Display:
> "No detect outputs found. Is this a multi-platform project? [y/n]"

If YES:
  Ask: "Enter platform names (comma-separated, e.g., web,backend,mobile): "
  Display orchestration guide:

  "To analyze all platforms, run detect skills for each:

  Platform: {platform1}
    1. /jaan-to:detect-dev
    2. /jaan-to:detect-design
    3. /jaan-to:detect-writing
    4. /jaan-to:detect-product
    5. /jaan-to:detect-ux

  Platform: {platform2}
    ... (repeat for each platform)

  After all platforms analyzed:
    /jaan-to:detect-pack"

  **Stop execution** (orchestration mode)

If NO (single-platform):
  Display standard workflow list:
  > "To generate a full knowledge pack, run the detect skills first:
  >
  > 1. `/jaan-to:detect-dev` — Engineering audit
  > 2. `/jaan-to:detect-design` — Design system detection
  > 3. `/jaan-to:detect-writing` — Writing system extraction
  > 4. `/jaan-to:detect-product` — Product reality extraction
  > 5. `/jaan-to:detect-ux` — UX audit
  >
  > Then run `/jaan-to:detect-pack` to consolidate."

  **Stop execution**

### Detect Platform Structure

**If outputs exist**, scan for platform suffixes to determine single vs multi-platform:

```python
# Detect platforms by scanning for filename suffixes
platforms = set()
for domain in ['dev', 'design', 'writing', 'product', 'ux']:
  files = Glob(f"$JAAN_OUTPUTS_DIR/detect/{domain}/*-*.md")  # Files with dash suffix
  for file in files:
    # Extract platform from filename: "stack-web.md" → "web"
    # Pattern: {aspect}-{platform}.md where platform is everything after last dash
    filename = os.path.basename(file)
    if filename.count('-') >= 1:  # Has platform suffix
      platform = filename.split('-')[-1].replace('.md', '')
      platforms.add(platform)

# Also check for files WITHOUT suffix (single-platform)
for domain in ['dev', 'design', 'writing', 'product', 'ux']:
  files_no_suffix = Glob(f"$JAAN_OUTPUTS_DIR/detect/{domain}/*.md")
  for file in files_no_suffix:
    filename = os.path.basename(file)
    # Check if filename has NO platform suffix (e.g., "stack.md" not "stack-web.md")
    if '-' not in filename.replace('.md', ''):  # No dash in base name
      platforms.add('all')  # Single-platform marker
      break

platforms = list(platforms)
```

**Handle detection results**:

- **No platforms detected** → Something is wrong, no valid outputs found
- **Only 'all' platform detected** → **Single-platform mode**: consolidate all files into single pack
- **Multiple platforms detected** (excluding 'all') → **Multi-platform mode**: create per-platform packs + merged pack
- **Mix of 'all' and platforms** → **Hybrid mode**: treat 'all' as legacy single-platform alongside new multi-platform outputs

**Display detection result**:
```
PLATFORM DETECTION
------------------
Mode: {Single-platform / Multi-platform / Hybrid}
Platforms detected: {list}
```

**If SOME but not all detect outputs exist**:

Display:
> "Found outputs for: {list of domains with outputs}.
> Missing: {list of domains without outputs}.
>
> Continue with available outputs? (Results will be marked as partial) [y/n]"

If user declines, stop execution.

## Step 1: Read All Detect Outputs

For each domain that has outputs, detect input mode and read accordingly:

### Input Mode Detection

For each domain directory (`detect/dev/`, `detect/design/`, etc.):

1. **Glob for individual aspect files** (e.g., `stack*.md`, `architecture*.md`, `tokens*.md`)
2. **If individual files found** → `input_mode = "full"` — read all individual files (current behavior)
3. **If only `summary{suffix}.md` found** → `input_mode = "light"` — read summary file, extract `findings_summary` and `overall_score` from frontmatter
4. **Track input mode per domain** for use in subsequent steps:

| Domain | Input Mode | Files Read |
|---------|-----------|------------|
| dev     | full / light | {count} files or summary.md |
| design  | full / light | {count} files or summary.md |
| writing | full / light | {count} files or summary.md |
| product | full / light | {count} files or summary.md |
| ux      | full / light | {count} files or summary.md |

### Full-Mode Input: Expected Files

| Domain | Directory | Expected Files |
|--------|-----------|---------------|
| dev | `$JAAN_OUTPUTS_DIR/detect/dev/` | stack, architecture, standards, testing, cicd, deployment, security, observability, risks |
| design | `$JAAN_OUTPUTS_DIR/detect/design/` | brand, tokens, components, patterns, accessibility, governance |
| writing | `$JAAN_OUTPUTS_DIR/detect/writing/` | writing-system, glossary, ui-copy, error-messages, localization, samples |
| product | `$JAAN_OUTPUTS_DIR/detect/product/` | overview, features, value-prop, monetization, entitlements, metrics, constraints |
| ux | `$JAAN_OUTPUTS_DIR/detect/ux/` | personas, jtbd, flows, pain-points, heuristics, accessibility, gaps |

### Light-Mode Input: Summary Files

For domains with `input_mode = "light"`, read `summary{suffix}.md` and extract:
- YAML frontmatter: `findings_summary`, `overall_score`, `platform`, `target`
- Executive summary text (for domain summary in consolidated output)

## Step 2: Validate Universal Frontmatter

For each output file, validate required frontmatter fields:

- `target.commit` — MUST match current git HEAD (flag stale if mismatched)
- `tool.rules_version` — record for version compatibility
- `confidence_scheme` — MUST be "four-level"
- `findings_summary` — MUST have severity buckets (critical/high/medium/low/informational)
- `overall_score` — MUST be 0-10 numeric
- `lifecycle_phase` — MUST use CycloneDX vocabulary

**Validation failures** become findings in the consolidated output (severity: Medium, confidence: Confirmed).

**Light-mode input handling**: For domains with `input_mode = "light"`, validate only the summary file frontmatter. Skip per-file validation (individual files don't exist).

## Step 3: Aggregate Findings

### Severity Buckets

Collect all findings_summary from each output file and aggregate into repo-wide totals:

```
Total Critical:      sum of all critical findings
Total High:          sum of all high findings
Total Medium:        sum of all medium findings
Total Low:           sum of all low findings
Total Informational: sum of all informational findings
```

### Overall Score Formula

```
overall_score = 10 - (critical * 2.0 + high * 1.0 + medium * 0.4 + low * 0.1) / max(total_findings, 1)
```

Clamp result to 0-10 range.

If partial run (not all 5 domains), append "(partial)" to the score label.

### Confidence Distribution

Count findings by confidence level across all domains:
- Confirmed: {n}
- Firm: {n}
- Tentative: {n}
- Uncertain: {n}

## Step 4: Build Risk Heatmap

Create a domain x severity markdown table:

```markdown
| Domain | Critical | High | Medium | Low | Info | Score |
|--------|----------|------|--------|-----|------|-------|
| Dev    | {n}      | {n}  | {n}    | {n} | {n}  | {s}   |
| Design | {n}      | {n}  | {n}    | {n} | {n}  | {s}   |
| Writing| {n}      | {n}  | {n}    | {n} | {n}  | {s}   |
| Product| {n}      | {n}  | {n}    | {n} | {n}  | {s}   |
| UX     | {n}      | {n}  | {n}    | {n} | {n}  | {s}   |
| **Total** | **{n}** | **{n}** | **{n}** | **{n}** | **{n}** | **{s}** |
```

For missing domains, show "not analyzed" in all cells.

**If `run_depth == "light"`:** Skip Steps 5, 6, and 6a. Proceed directly to Step 7 (Present Consolidation Summary).

**Note**: For domains with `input_mode = "light"`, Steps 2-4 use summary-level data (frontmatter scores and finding counts) instead of per-file data. Validation is limited to frontmatter presence check.

## Step 5: Build Evidence Index (Source Map)

Collect ALL evidence IDs from all detect outputs and build a resolution index.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` sections "Evidence Index Table Format", "Evidence ID Parsing", "Evidence Validation Rules", and "Cross-Platform Evidence Linking" for table format, regex patterns, validation rules, and linking logic.

## Step 6: Build Unknowns Backlog

Collect all findings with confidence <= Tentative (0.79 or below) and all "absence" evidence items.

For each unknown:
- Finding ID and title
- Current confidence level
- Domain
- "How to confirm" steps (what investigation would resolve the uncertainty)
- Explicit scope boundary (what this finding can and cannot claim)

## Step 6a: Multi-Platform Consolidation (if applicable)

**Only run this step if Step 0 detected multiple platforms.**

If single-platform mode, skip to Step 7.

### 1. Aggregate Per-Platform Findings

For each detected platform, aggregate findings across all domains and calculate per-platform scores using the standard score formula.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "Per-Platform Aggregation Logic" for implementation details.

### 2. Build Cross-Platform Risk Heatmap

Build a platform x domain severity table with totals row.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "Cross-Platform Risk Heatmap Logic" for implementation and example table.

### 3. Identify Cross-Platform Findings

Extract findings with `related_evidence` field that link across platforms.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "Cross-Platform Findings Extraction" for implementation.

### 4. Deduplicate Shared Findings

Group cross-platform findings by canonical group ID and deduplicate. Store consolidated data (`platform_findings`, `heatmap_table`, `deduplicated`) for use in Step 8.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "Cross-Platform Deduplication Logic" for implementation.

---

# HARD STOP — Consolidation Summary & User Approval

## Step 7: Present Consolidation Summary

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "Consolidation Summary Templates" for light mode, full single-platform, and full multi-platform display formats.

Present the consolidation summary using the appropriate template for current `run_depth` and platform mode.

> "Proceed with writing consolidation files to $JAAN_OUTPUTS_DIR/detect/? [y/n]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Write Output Files

## Step 8: Write Output Files

**Output directory logic:**

```python
# Determine output directory
if len(platforms) == 1 and 'all' in platforms:  # Single-platform
  output_dir = "$JAAN_OUTPUTS_DIR/detect/"
else:  # Multi-platform
  output_dir = "$JAAN_OUTPUTS_DIR/detect/pack/"

# Create directory if needed
os.makedirs(output_dir, exist_ok=True)
```

### Stale File Cleanup

- **If `run_depth == "full"`:** Delete any existing `summary.md` in `$JAAN_OUTPUTS_DIR/detect/` (stale light-mode output).
- **If `run_depth == "light"`:** Do NOT delete existing full-mode files.

### If `run_depth == "light"`: Write Single Summary File

Write one file: `$JAAN_OUTPUTS_DIR/detect/summary.md`

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "Light Mode Summary File Structure" for required contents.

### If `run_depth == "full"`: Write Full Output Files

### Single-Platform Mode

Write 4 output files to `$JAAN_OUTPUTS_DIR/detect/`:

| File | Content |
|------|---------|
| `README.md` | Knowledge index: metadata, domain summaries, overall score, links to all detect outputs |
| `risk-heatmap.md` | Risk heatmap table (domain x severity), top risks per domain |
| `unknowns-backlog.md` | Prioritized unknowns with "how to confirm" steps and scope boundaries |
| `source-map.md` | Evidence index: all E-IDs mapped to file locations |

### Multi-Platform Mode

Write to `$JAAN_OUTPUTS_DIR/detect/pack/`:

**Per-Platform Packs** (one per platform):

| File | Content |
|------|---------|
| `README-{platform}.md` | Platform-specific index with domain summaries for that platform only |

**Merged Pack** (all platforms combined):

| File | Content |
|------|---------|
| `README.md` | Merged knowledge index with platform summary table and overall aggregated score |
| `risk-heatmap.md` | Cross-platform risk heatmap (platform x domain table) + cross-platform findings section |
| `unknowns-backlog.md` | All Tentative/Uncertain findings across all platforms, grouped by platform then domain |
| `source-map.md` | All evidence IDs from all platforms with platform column |

### README.md Structure (Single-Platform)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "README.md Structure (Single-Platform)" for full template. Includes: Overview, Domain Summaries (per-domain score + executive summary), Quick Links.

### README.md Structure (Multi-Platform Merged Pack)

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-pack-reference.md` section "README.md Structure (Multi-Platform Merged Pack)" for full template. Includes: Overview, Platform Summary table, Cross-Platform Findings, Per-Platform Details, Quick Links.

Each file MUST include universal YAML frontmatter.

---

## Step 8a: Seed Update from Detection Data

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/seed-reconciliation-reference.md` for mapping tables, change categories, approval options, preservation rules, and report format.

Use consolidated detection results as source of truth to update all project seed files.

1. **Read** all seed files in `$JAAN_CONTEXT_DIR/` (tech.md, team.md, integrations.md, boundaries.md, tone-of-voice.template.md, localization.template.md) — skip any that don't exist
2. **Build proposed updates** by cross-referencing detect outputs against each seed file using the mapping table and section anchors from the reference doc
3. **Present diff-style summary** per seed file using [UPDATE] / [ADD] / [STALE] categories — **HARD STOP**: require explicit approval (`[y/all/n/pick]`)
4. **Apply approved updates** — edit seed files preserving section anchors, custom sections, and `<!-- keep -->` markers
5. **Suggest `/jaan-to:learn-add`** commands for detection findings that don't map to any seed file
6. **Write reconciliation report** to `$JAAN_OUTPUTS_DIR/detect/seed-reconciliation.md`

---

## Step 9: Capture Feedback

> "Any feedback on the knowledge pack? [y/n]"

If yes:
- Run `/jaan-to:learn-add detect-pack "{feedback}"`

---

## ISO 25010 Quality Compliance

When aggregating detect outputs, map findings to ISO 25010 quality characteristics:

| ISO 25010 Characteristic | Detect Sources | Signal |
|--------------------------|---------------|--------|
| Functional Suitability | detect-dev (test coverage) | Test pass rate, coverage % |
| Performance Efficiency | detect-dev (architecture) | N+1 queries, connection pools |
| Compatibility | detect-dev (CI/CD) | Multi-platform support |
| Usability | detect-ux (UX audit) | Heuristic scores |
| Reliability | detect-dev (error handling) | Error handler coverage |
| Security | detect-dev (security scan) | Vulnerability counts |
| Maintainability | detect-dev (code quality) | Complexity, duplication |
| Portability | detect-dev (infrastructure) | Container, cloud-agnostic |

Add "Quality Gate Readiness" section to consolidated output:
- Map aggregate scores to 4-tier gating model (auto-approve / lightweight / full / block)
- Reference `/jaan-to:qa-quality-gate` for detailed composite scoring

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Evidence-based findings with confidence scoring
- Fork-isolated execution (`context: fork`)
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

**If `run_depth == "light"`:**

- [ ] Single `summary.md` written to `$JAAN_OUTPUTS_DIR/detect/`
- [ ] Universal YAML frontmatter with `findings_summary` and `overall_score`
- [ ] Risk heatmap table included (domain x severity)
- [ ] Per-domain executive summary (1-2 sentences each)
- [ ] Input mode table shows which domains provided full vs summary data
- [ ] Overall score calculated with formula
- [ ] Partial runs clearly labeled with coverage %
- [ ] "--full" upsell note included
- [ ] User approved output

**If `run_depth == "full"`:**

**Single-Platform Mode:**

- [ ] All 4 output files written to `$JAAN_OUTPUTS_DIR/detect/`
- [ ] Universal YAML frontmatter in every file
- [ ] Risk heatmap shows domain x severity table
- [ ] Evidence index resolves all E-IDs to file locations
- [ ] No duplicate evidence IDs
- [ ] Unknowns backlog has "how to confirm" steps
- [ ] Overall score calculated with formula
- [ ] Partial runs clearly labeled with coverage %
- [ ] Frontmatter validation issues flagged
- [ ] User approved output
- [ ] Seed files updated from detection data (or user declined updates)
- [ ] Seed reconciliation report written to `$JAAN_OUTPUTS_DIR/detect/seed-reconciliation.md`

**Multi-Platform Mode:**

- [ ] Output files written to `$JAAN_OUTPUTS_DIR/detect/pack/`
- [ ] Per-platform packs created (README-{platform}.md for each platform)
- [ ] Merged pack created (README.md with platform summary table)
- [ ] Cross-platform risk heatmap shows platform x domain table
- [ ] Cross-platform findings section in heatmap (deduplicated via related_evidence)
- [ ] Evidence index includes platform column and handles both ID formats
- [ ] Evidence ID regex correctly parses E-DEV-001 and E-DEV-WEB-001 formats
- [ ] No duplicate evidence IDs (checked with platform awareness)
- [ ] Cross-platform evidence links validated (all related_evidence IDs exist)
- [ ] Unknowns backlog groups findings by platform, then domain
- [ ] Per-platform scores calculated correctly
- [ ] Overall weighted average score calculated from platform scores
- [ ] Platform detection logic executed in Step 0
- [ ] User approved output
- [ ] Seed files updated from detection data (or user declined updates)
- [ ] Seed reconciliation report written to `$JAAN_OUTPUTS_DIR/detect/seed-reconciliation.md`
