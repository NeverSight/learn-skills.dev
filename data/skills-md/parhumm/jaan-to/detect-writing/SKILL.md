---
name: detect-writing
description: Writing system extraction with NNg tone dimensions, UI copy classification, and i18n maturity. Use when auditing content systems.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/**), Edit(jaan-to/config/settings.yaml), Edit($JAAN_CONTEXT_DIR/**)
argument-hint: "[repo] [--full]"
context: fork
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Partial standalone support for analysis mode.
---

# detect-writing

> Detect the current writing system using multi-signal extraction and output a canonical writing-system spec.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-detect-writing.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack (for framework-aware i18n scanning)
- `$JAAN_TEMPLATES_DIR/jaan-to-detect-writing.template.md` - Output template
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

**Output path**: `$JAAN_OUTPUTS_DIR/detect/writing/` — flat files, overwritten each run (no IDs).

## Input

**Arguments**: $ARGUMENTS — parsed in Step 0.0. Repository path and mode determined there.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `detect-writing`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_detect-writing`

---

## Standards Reference

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-shared-reference.md` for Evidence Format (SARIF), Evidence ID Generation, Confidence Levels, Frontmatter Schema, Platform Detection, Document Structure, and Codebase Content Safety.

**This skill's namespace**: `E-WRT-*` (e.g., E-WRT-001, E-WRT-WEB-001)
**Tool name in frontmatter**: `detect-writing`

---

# PHASE 1: Detection (Read-Only)

## Step 0.0: Parse Arguments

**Arguments**: $ARGUMENTS

| Argument | Effect |
|----------|--------|
| (none) | **Light mode** (default): String inventory + i18n maturity, single summary file |
| `[repo]` | Scan specified repo (applies to both modes) |
| `--full` | **Full mode**: All detection steps, 6 output files (current behavior) |

**Mode determination:**
- If `$ARGUMENTS` contains `--full` as a standalone token → set `run_depth = "full"`
- Otherwise → set `run_depth = "light"`

Strip `--full` token from arguments. Set `repo_path` to remaining arguments (or current working directory if empty).

## Thinking Mode

**If `run_depth == "full"`:** ultrathink
**If `run_depth == "light"`:** megathink

Use extended reasoning for:
- NNg tone dimension scoring across string corpus
- UI copy classification and quality assessment
- i18n maturity level determination
- Terminology consistency analysis

## Step 0: Detect Platforms

**Purpose**: Auto-detect platform structure and determine analysis scope (full vs partial).

Use **Glob** and **Bash** to identify platform folders:

### Platform Patterns

(Same as detect-dev - see detect-dev Step 0 for full patterns table)

### Detection Process

1. **Check for monorepo markers**: `pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`
2. **List top-level directories**: `ls -d */ | grep -Ev "node_modules|\.git|dist|build|\.next"`
3. **Match against platform patterns**: Apply disambiguation rules
4. **Handle detection results**:
   - No platforms → Single-platform: `platforms = [{ name: 'all', path: '.' }]`
   - Platforms detected → Multi-platform: Ask user to select all or specific platforms

### Writing System Applicability

For each platform, determine analysis scope:

| Platform Type | Analysis Scope | Rationale |
|---------------|---------------|-----------|
| web, mobile, androidtv, ios, android, desktop | **Full** | UI copy, error messages, tone, localization |
| backend, api, services | **Partial** | Error messages only (API errors, logs, validation messages) |
| cli, cmd | **Partial** | Error messages + CLI help text only |

**Partial analysis** includes:
- Error message detection and scoring (Step 4)
- Glossary extraction from error messages (Step 5 - partial)
- Localization detection for error messages (Step 6 - partial)
- **Skips**: UI copy classification (Step 2), full tone analysis (Step 3 reduced to error messages only)

### UI Presence Check

```bash
# Check for UI component files
ui_files=$(find {platform.path} -type f \( -name "*.jsx" -o -name "*.tsx" -o -name "*.vue" -o -name "*.svelte" \) 2>/dev/null | head -n 1)

if [ -z "$ui_files" ]; then
  # No UI files - partial analysis mode
  analysis_mode = "partial"  # Error messages only
else
  analysis_mode = "full"     # Full writing system analysis
fi
```

### Analysis Loop

For each platform in platforms:
1. Set `current_platform = platform.name`
2. Set `base_path = platform.path`
3. **Determine analysis mode** based on platform type and UI presence
4. Run detection steps per `run_depth` and `analysis_mode`:
   - **If `run_depth == "full"` AND `analysis_mode == "full"`:** Run Steps 1-7
   - **If `run_depth == "full"` AND `analysis_mode == "partial"`:** Run Steps 1, 3 (reduced), 4, 5, 6 (reduced). Skip Step 2, 7 unless content linting detected.
   - **If `run_depth == "light"` AND `analysis_mode == "full"`:** Run Steps 1, 5 only (skip Steps 2, 3, 4, 6, 7)
   - **If `run_depth == "light"` AND `analysis_mode == "partial"`:** Run Steps 1, 4, 5 only (skip Steps 2, 3, 6, 7)
5. Use platform-specific output paths in Step 9

**Partial Analysis Output Notes**:
- `writing-system.md`: Tone dimensions based on error messages only, with note about scope limitation
- `ui-copy.md`: Minimal "Not Applicable" file with informational finding
- `samples.md`: Minimal "Not Applicable" file or error message samples only

**Note**: If single-platform mode (`platform.name == 'all'`), output paths have NO suffix. If multi-platform mode, output paths include `-{platform}` suffix.

## Step 1: String Inventory

### i18n / Locale Files
Use framework-specific glob patterns:

| Framework | Glob Patterns |
|-----------|--------------|
| React i18next | `**/locales/**/*.json`, `**/i18n/**/*.json`, `**/public/locales/**/*.json` |
| Vue i18n | `**/locales/*.json`, `**/i18n/**/*.json`, `**/lang/**/*.{json,yml}` |
| Angular | `**/src/locale/messages.*.xlf` |
| Next.js | `**/public/locales/**/*.json`, `**/messages/*.json` |
| Flutter/Dart | `**/lib/l10n/*.arb`, `**/l10n/app_*.arb` |
| Android | `**/res/values/strings.xml`, `**/res/values-*/strings.xml` |
| iOS/macOS | `**/*.lproj/Localizable.strings` |
| Rails | `**/config/locales/**/*.yml` |
| Django | `**/locale/*/LC_MESSAGES/django.po` |
| Java | `**/resources/messages*.properties` |
| .NET | `**/Resources/*.resx` |
| PHP/Laravel | `**/resources/lang/**/*.php`, `**/lang/**/*.php` |
| GNU gettext | `**/po/*.po`, `**/po/*.pot` |

### Component Inline Text
- Grep for text in component props: `label`, `title`, `message`, `description`, `placeholder`, `helperText`, `errorMessage`
- Grep for JSX/TSX inline text between tags

**If `run_depth == "light"` AND `analysis_mode == "full"`:** Skip Steps 2-4, 6-7. Proceed directly to Step 5 (i18n Maturity Assessment).

**If `run_depth == "light"` AND `analysis_mode == "partial"`:** Skip Steps 2-3. Proceed directly to Step 4 (Error Message Quality Scoring), then Step 5, then skip Steps 6-7.

## Step 2: UI Copy Classification

Classify discovered strings into 8 categories (Buttons/CTAs, Error messages, Empty states, Confirmation dialogs, Notifications/toasts, Onboarding, Form labels/helper, Loading states) using component-name glob patterns and variant/severity props.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-writing-reference.md` — "UI Copy Classification" for category detection patterns and props to extract.

## Step 3: NNg Tone Dimension Scoring

Score strings across 4 primary dimensions (Formality, Humor, Respectfulness, Enthusiasm) and 5 extended dimensions (Technical complexity, Verbosity, Directness, Empathy, Confidence), each on a 1-5 scale. Calculate consistency scores via standard deviation per dimension; flag outliers deviating >1.5 standard deviations.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-writing-reference.md` — "NNg Tone Dimension Scoring" for dimension scales, detection signals, and consistency calculation.

## Step 4: Error Message Quality Scoring

Apply 5-dimension weighted rubric (Clarity 25%, Specificity 20%, Actionability 25%, Tone 15%, Accessibility 15%) to each error message found. Flag messages matching automated heuristic thresholds (complexity, length, passive voice, blame language, visible error codes, missing action verbs).

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-writing-reference.md` — "Error Message Quality Scoring" for rubric details and heuristic flag criteria.

## Step 5: i18n Maturity Assessment

Use the glob patterns from Step 1 to identify which i18n framework is in use. Assess ICU MessageFormat usage, RTL support, hardcoded string prevalence, string interpolation quality, and centralization. Rate maturity on a 0-5 scale (None through Excellence).

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-writing-reference.md` — "i18n Maturity Assessment" for ICU regex patterns, RTL detection methods, hardcoded string grep patterns, interpolation quality levels, centralization scoring rules, and the 0-5 maturity scale.

**If `run_depth == "light"`:** Skip Steps 6-7. Proceed directly to Step 8 (Present Detection Summary).

## Step 6: Terminology Extraction

Build a glossary using ISO-704-inspired methodology. Discover terms via TF-IDF and C-value analysis, detect semantic/syntactic/frequency-based inconsistencies, and output entries with preferred/admitted/deprecated statuses.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-writing-reference.md` — "Terminology Extraction" for term discovery methods, inconsistency detection rules, and glossary entry YAML format.

## Step 7: Content Governance Detection

Check for content governance signals: CODEOWNERS locale ownership, content linting tools, i18n keywords in PR templates, and CI translation checks.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-writing-reference.md` — "Content Governance Detection" for specific tools and patterns to check.

---

# HARD STOP — Detection Summary & User Approval

## Step 8: Present Detection Summary

**If `run_depth == "light"`:**

```
WRITING SYSTEM DETECTION COMPLETE (Light Mode)
-------------------------------------------------

PLATFORM: {platform_name or 'all'}
ANALYSIS MODE: {Full/Partial (error messages only)}

STRING CORPUS: {n} strings analyzed across {n} files
LOCALES DETECTED: {list}

i18n MATURITY: Level {0-5} ({name})
{if analysis_mode == "partial":}
ERROR MESSAGE SCORE: {avg_score}/10

SEVERITY SUMMARY
  Critical: {n}  |  High: {n}  |  Medium: {n}  |  Low: {n}  |  Info: {n}

OVERALL SCORE: {score}/10

OUTPUT FILE (1):
  $JAAN_OUTPUTS_DIR/detect/writing/summary{-platform}.md

Note: Run with --full for NNg tone dimensions, UI copy classification,
glossary, and governance analysis (6 output files).
```

> "Proceed with writing summary to $JAAN_OUTPUTS_DIR/detect/writing/? [y/n]"

**If `run_depth == "full"`:**

```
WRITING SYSTEM DETECTION COMPLETE
-----------------------------------

PLATFORM: {platform_name or 'all'}
ANALYSIS MODE: {Full/Partial (error messages only)}

STRING CORPUS: {n} strings analyzed across {n} files
LOCALES DETECTED: {list}

TONE DIMENSIONS (NNg) {scope note if partial: "based on error messages only"}
  Formality:      {score}/5    Consistency: {stddev}
  Humor:          {score}/5    Consistency: {stddev}
  Respectfulness: {score}/5    Consistency: {stddev}
  Enthusiasm:     {score}/5    Consistency: {stddev}

UI COPY COVERAGE {show "N/A" if partial analysis}
  Buttons:      {n} strings    Error messages: {n} strings
  Empty states: {n} strings    Dialogs:        {n} strings
  Toasts:       {n} strings    Onboarding:     {n} strings
  Form labels:  {n} strings    Loading:        {n} strings

i18n MATURITY: Level {0-5} ({name})
ERROR MESSAGE SCORE: {avg_score}/10

SEVERITY SUMMARY
  Critical: {n}  |  High: {n}  |  Medium: {n}  |  Low: {n}  |  Info: {n}

OVERALL SCORE: {score}/10

OUTPUT FILES (6):
  $JAAN_OUTPUTS_DIR/detect/writing/writing-system{-platform}.md  - Voice + tone + consistency
  $JAAN_OUTPUTS_DIR/detect/writing/glossary{-platform}.md        - Terminology glossary
  $JAAN_OUTPUTS_DIR/detect/writing/ui-copy{-platform}.md         - UI copy classification {or "N/A" if partial}
  $JAAN_OUTPUTS_DIR/detect/writing/error-messages{-platform}.md  - Error message audit
  $JAAN_OUTPUTS_DIR/detect/writing/localization{-platform}.md    - i18n maturity assessment
  $JAAN_OUTPUTS_DIR/detect/writing/samples{-platform}.md         - Representative samples {or "N/A" if partial}

Note: {-platform} suffix only if multi-platform mode (e.g., -web, -backend). Single-platform mode has no suffix.
      Partial analysis mode (backend/cli) produces minimal "Not Applicable" files for ui-copy.md and samples.md.
```

> "Proceed with writing 6 output files to $JAAN_OUTPUTS_DIR/detect/writing/? [y/n]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Write Output Files

## Step 9: Write to $JAAN_OUTPUTS_DIR/detect/writing/

Create directory `$JAAN_OUTPUTS_DIR/detect/writing/` if it does not exist.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-shared-reference.md` sections "Output Path Logic" and "Stale File Cleanup" for platform-specific suffix convention and run_depth cleanup rules.

### If `run_depth == "light"`: Write Single Summary File

Write one file: `$JAAN_OUTPUTS_DIR/detect/writing/summary{suffix}.md`

Contents:
1. Universal YAML frontmatter with `platform` field, `findings_summary`, and `overall_score`
2. **Executive Summary** — BLUF of writing system findings
3. **String Corpus Overview** — total strings, file count, categories found (from Step 1)
4. **i18n Maturity** — level (0-5), locales detected, evidence (from Step 5)
5. **If `analysis_mode == "partial"`:** **Error Message Quality Scores** — rubric scoring results (from Step 4)
6. **Top Findings** — up to 5 highest-severity findings with evidence blocks
7. "Run with `--full` for NNg tone dimensions, UI copy classification, glossary, and governance analysis (6 output files)."

### If `run_depth == "full"`: Write 6 Output Files

Write 6 output files:

| File | Content | Partial Analysis Handling |
|------|---------|---------------------------|
| `$JAAN_OUTPUTS_DIR/detect/writing/writing-system{suffix}.md` | Voice definition, tone spectrum (NNg dimensions), consistency score | If partial: Note scope limitation ("based on error messages only") |
| `$JAAN_OUTPUTS_DIR/detect/writing/glossary{suffix}.md` | Terminology glossary with ISO-704 statuses | If partial: Error terminology only |
| `$JAAN_OUTPUTS_DIR/detect/writing/ui-copy{suffix}.md` | UI copy classification across 8 categories | If partial: **Minimal "Not Applicable" file** |
| `$JAAN_OUTPUTS_DIR/detect/writing/error-messages{suffix}.md` | Error message quality audit with rubric scoring | Always included (core finding) |
| `$JAAN_OUTPUTS_DIR/detect/writing/localization{suffix}.md` | i18n maturity assessment (0-5) with evidence | If partial: Error message i18n only |
| `$JAAN_OUTPUTS_DIR/detect/writing/samples{suffix}.md` | Representative string samples per category | If partial: **Minimal "Not Applicable" or error samples only** |

**Note**: `{suffix}` is empty for single-platform mode, or `-{platform}` for multi-platform mode.

**Partial Analysis "Not Applicable" Files**:

For platforms with `analysis_mode == "partial"` (backend/cli), create minimal files for `ui-copy.md` and `samples.md`:

```yaml
---
findings_summary:
  informational: 1
overall_score: 10.0  # Nothing to assess
---

## Executive Summary

Platform '{platform}' does not contain UI components. Full writing system analysis is not applicable. This audit focuses on error messages only.

## Findings

### E-WRT-{PLATFORM}-001: UI Copy Analysis Not Applicable

**Severity**: Informational
**Confidence**: Confirmed (1.0)

**Description**: Platform type '{platform}' (backend/CLI) does not have UI copy. Writing system analysis is limited to error messages, validation strings, and API responses.
```

Each file MUST include:
1. Universal YAML frontmatter with `platform` field and findings_summary/overall_score
2. Executive Summary (with scope note if partial analysis)
3. Scope and Methodology (clearly state "Partial Analysis" if applicable)
4. Findings with evidence blocks (using E-WRT-{PLATFORM}-NNN or E-WRT-NNN IDs)
5. Recommendations

---

## Step 9a: Seed Reconciliation

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/seed-reconciliation-reference.md` for comparison rules, discrepancy format, and auto-update protocol.

1. Read domain-relevant seed files: `$JAAN_CONTEXT_DIR/tone-of-voice.template.md`, `$JAAN_CONTEXT_DIR/localization.template.md`
2. Compare detection results against seed content (tone dimensions, voice characteristics, error message guidelines, i18n maturity, supported languages)
3. If discrepancies found:
   - Display discrepancy table to user
   - Offer auto-updates for non-destructive changes: `[y/n]`
   - Suggest `/jaan-to:learn-add` commands for patterns worth documenting
4. If no discrepancies: display "Seed files are aligned with detection results."

---

## Step 10: Capture Feedback

> "Any feedback on the writing system detection? [y/n]"

If yes:
- Run `/jaan-to:learn-add detect-writing "{feedback}"`

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Evidence-based findings with confidence scoring
- Fork-isolated execution (`context: fork`)
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

**If `run_depth == "light"`:**

- [ ] Single summary file written to `$JAAN_OUTPUTS_DIR/detect/writing/summary{suffix}.md`
- [ ] Universal YAML frontmatter with `overall_score`
- [ ] String corpus overview and i18n maturity included
- [ ] If partial analysis: error message quality scores included
- [ ] "--full" upsell note included
- [ ] User approved output

**If `run_depth == "full"`:**

- [ ] All 6 output files written to `$JAAN_OUTPUTS_DIR/detect/writing/`
- [ ] Universal YAML frontmatter with `platform` field in every file
- [ ] Every finding has evidence block with correct ID format (E-WRT-NNN for single-platform, E-WRT-{PLATFORM}-NNN for multi-platform)
- [ ] NNg tone dimensions scored with consistency analysis (note scope if partial)
- [ ] UI copy classified into 8 categories (or "Not Applicable" if partial analysis)
- [ ] Error messages scored with weighted rubric (always included)
- [ ] i18n maturity rated 0-5 with evidence (scoped to error messages if partial)
- [ ] Glossary uses ISO-704 statuses (error terminology if partial)
- [ ] Output filenames match platform suffix convention (no suffix for single-platform, -{platform} suffix for multi-platform)
- [ ] If partial analysis mode (backend/cli), minimal "Not Applicable" files created for ui-copy.md and samples.md
- [ ] Confidence scores assigned to all findings
- [ ] User approved output
- [ ] Seed reconciliation check performed (discrepancies reported or alignment confirmed)
