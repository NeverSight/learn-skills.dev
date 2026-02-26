---
name: detect-design
description: Design system detection with drift findings and evidence blocks. Use when auditing design system consistency.
allowed-tools: Read, Glob, Grep, Write($JAAN_OUTPUTS_DIR/**), Edit(jaan-to/config/settings.yaml), Edit($JAAN_CONTEXT_DIR/**)
argument-hint: "[repo] [--full]"
context: fork
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Partial standalone support for analysis mode.
---

# detect-design

> Detect real design system in code with drift findings and evidence blocks.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-detect-design.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_CONTEXT_DIR/tech.md` - Tech stack (if exists, for framework-aware scanning)
- `$JAAN_TEMPLATES_DIR/jaan-to-detect-design.template.md` - Output template
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

**Output path**: `$JAAN_OUTPUTS_DIR/detect/design/` — flat files, overwritten each run (no IDs).

## Input

**Arguments**: $ARGUMENTS — parsed in Step 0.0. Repository path and mode determined there.

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `detect-design`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_detect-design`

---

## Standards Reference

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-shared-reference.md` for Evidence Format (SARIF), Evidence ID Generation, Confidence Levels, Frontmatter Schema, Platform Detection, Document Structure, and Codebase Content Safety.

**This skill's namespace**: `E-DSN-*` (e.g., E-DSN-001, E-DSN-WEB-001)
**Tool name in frontmatter**: `detect-design`

### Drift Detection — Paired Evidence

"Drift" findings REQUIRE two evidence items showing the conflict:

```yaml
evidence:
  - id: E-DSN-001a
    type: token-definition
    confidence: 0.95
    location:
      uri: "src/tokens/colors.json"
      startLine: 15
    snippet: |
      "primary": "#3B82F6"
  - id: E-DSN-001b
    type: conflicting-usage
    confidence: 0.90
    location:
      uri: "src/components/Button.tsx"
      startLine: 42
    snippet: |
      color: "#2563EB"  // hardcoded, differs from token
```

---

# PHASE 1: Detection (Read-Only)

## Step 0.0: Parse Arguments

**Arguments**: $ARGUMENTS

| Argument | Effect |
|----------|--------|
| (none) | **Light mode** (default): Token + component scan, single summary file |
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
- Identifying design token hierarchies and naming conventions
- Detecting drift between definitions and usage
- Mapping component library patterns
- Accessibility scope assessment

## Step 0: Detect Platforms

**Purpose**: Auto-detect platform structure and check for UI presence before analysis.

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
   - Apply disambiguation rules (same as detect-dev)

4. **Handle detection results**:
   - **No platforms detected** → Single-platform mode:
     - Set `platforms = [{ name: 'all', path: '.' }]`
     - Path = repository root
   - **Platforms detected** → Multi-platform mode:
     - Build list: `platforms = [{ name: 'web', path: 'web/' }, { name: 'backend', path: 'backend/' }, ...]`
     - Ask user: "Detected platforms: {list}. Analyze all or select specific? [all/select]"
     - If 'select', prompt: "Enter platform names (comma-separated): "

### UI Presence Check (Design System Applicability)

For each platform, check for UI indicators:

```bash
# Check for UI component files
ui_files=$(find {platform.path} -type f \( -name "*.jsx" -o -name "*.tsx" -o -name "*.vue" -o -name "*.svelte" \) 2>/dev/null | head -n 1)

if [ -z "$ui_files" ]; then
  # No UI files detected - design system analysis not applicable
  # Will create minimal output files with "Not Applicable" findings
  platform_has_ui = false
else
  platform_has_ui = true
fi
```

**Platform applicability:**

| Platform Type | UI Expected | If No UI Found |
|---------------|-------------|----------------|
| web, mobile, androidtv, ios, android, desktop | Yes | Report as finding (unexpected) |
| backend, cli, services | Conditional | Report "Not Applicable" (expected) |

### Analysis Loop

For each platform in platforms:
1. Set `current_platform = platform.name`
2. Set `base_path = platform.path`
3. **Check UI presence** using the check above
4. If `platform_has_ui == false` and platform is backend/cli:
   - Skip Steps 1-7 (detection steps)
   - Go directly to Step 8 with "Not Applicable" findings
5. If `platform_has_ui == true` or platform is expected to have UI:
   - Run detection steps per `run_depth`:
     - **If `run_depth == "full"`:** Run Steps 1-7 scoped to `base_path`
     - **If `run_depth == "light"`:** Run Steps 1-2 only scoped to `base_path` (skip Steps 3-7)
6. Use platform-specific output paths in Step 9

**"Not Applicable" Findings Structure**:

When a platform has no UI files and design analysis is not applicable, create minimal output files with this finding:

```yaml
---
findings_summary:
  critical: 0
  high: 0
  medium: 0
  low: 0
  informational: 1
overall_score: 10.0  # Perfect score (nothing to assess)
---

## Executive Summary

No UI components detected for platform '{platform}'. Design system analysis is not applicable to this platform.

## Findings

### E-DSN-{PLATFORM}-001: No UI Components Detected

**Severity**: Informational
**Confidence**: Confirmed (1.0)

**Description**: Platform '{platform}' does not contain UI component files (.jsx, .tsx, .vue, .svelte). Design system detection, token analysis, and component inventory are not applicable to this platform type.

**Evidence**:
```yaml
evidence:
  id: E-DSN-{PLATFORM}-001
  type: absence
  confidence: 1.0
  method: glob-pattern-match
  description: "No UI files found in {platform.path}"
```
```

**Note**: If single-platform mode (`platform.name == 'all'`), output paths have NO suffix. If multi-platform mode, output paths include `-{platform}` suffix.

## Step 1: Scan Design Tokens

### Token Definition Files
- Glob: `**/tokens/**/*.{json,js,ts}` — design token packages
- Glob: `**/*.tokens.json` — token files by convention
- Glob: `tailwind.config.*` — Tailwind theme tokens
- Glob: `**/theme.{js,ts,json}`, `**/theme/**` — theme definitions

### CSS Variables
- Grep in `**/*.{css,scss,less}` for `--` prefixed custom properties
- Extract variable names, values, and categorize (color, spacing, typography, etc.)
- Detect naming conventions (BEM, kebab-case, camelCase)

### Token Categories
Map discovered tokens to categories:
- **Colors**: brand, semantic (success/warning/error/info), neutral/gray scales
- **Typography**: font families, sizes, weights, line heights
- **Spacing**: margins, paddings, gaps (detect scale: 4px/8px base)
- **Shadows**: elevation levels
- **Border radius**: shape tokens
- **Breakpoints**: responsive breakpoints
- **Animation**: timing, easing, duration tokens

## Step 2: Scan Component Library

### Component Files
- Glob: `**/components/**/*.{tsx,jsx,vue,svelte}` — component source
- Glob: `**/*.stories.{tsx,jsx,ts,js,mdx}` — Storybook stories
- Glob: `.storybook/**` — Storybook configuration

### Component Inventory
For each component directory, extract:
- Component name and file path
- Props interface (TypeScript types or PropTypes)
- Variant patterns (size, color, state)
- Composition patterns (compound components, slots)

### Component Categories
Classify components:
- **Primitives**: Button, Input, Text, Icon, Image
- **Layout**: Container, Grid, Stack, Flex, Spacer
- **Navigation**: Nav, Menu, Breadcrumb, Tabs, Pagination
- **Feedback**: Alert, Toast, Modal, Dialog, Progress
- **Data display**: Table, Card, List, Badge, Avatar
- **Form**: Select, Checkbox, Radio, Switch, DatePicker

**If `run_depth == "light"`:** Skip Steps 3-7. Proceed directly to Step 8 (Present Detection Summary).

**Precedence**: N/A handling (platform_has_ui checks) always takes priority over run_depth gates. If `platform_has_ui == false`, skip ALL detection steps regardless of run_depth.

## Step 3: Scan Brand Assets

- Glob: `**/assets/brand/**` — brand directory
- Glob: `**/assets/logo*`, `**/assets/icons/**` — logo and icon assets
- Glob: `**/fonts/**`, `**/*.woff2`, `**/*.ttf` — font files
- Detect font loading strategy (preload, font-display)
- Check for favicon and app icons

## Step 4: Scan UI Patterns

- Grep for layout patterns: grid systems, responsive utilities
- Detect spacing scale usage consistency
- Scan for color usage patterns outside token definitions
- Check for hardcoded values vs token references (drift signals)
- Detect dark mode / theme switching patterns (`prefers-color-scheme`, theme context)

## Step 5: Scan Accessibility Signals

**Scope**: Repo-level only. Cannot make claims about runtime behavior.

- Grep for ARIA attributes: `aria-label`, `aria-describedby`, `aria-live`, `role=`
- Check for semantic HTML usage: `<main>`, `<nav>`, `<article>`, `<section>`, `<header>`, `<footer>`
- Glob: `**/*.test.{ts,tsx,js,jsx}` and grep for a11y test patterns: `axe`, `jest-axe`, `@testing-library`, `getByRole`
- Check for skip links, focus management patterns
- Detect `alt` attribute usage on images

**Important**: Mark findings as "Unknown" when repo evidence is insufficient for runtime behavior claims.

## Step 6: Scan Governance Signals

- Glob: `CODEOWNERS` — check for design system file ownership
- Look for design system changelogs or versioning
- Detect Storybook configuration and deployment
- Check for visual regression testing (chromatic, percy, backstop)
- Look for design system documentation conventions
- Check for token versioning or release process

## Step 7: Detect Drift

For every token/variable definition found in Step 1, scan component files for:
- Hardcoded values that should reference tokens
- Inconsistent token usage (same semantic meaning, different tokens)
- Orphaned tokens (defined but never used)
- Undocumented overrides

Each drift finding MUST have paired evidence (definition + conflicting usage).

---

# HARD STOP — Detection Summary & User Approval

## Step 8: Present Detection Summary

**If `run_depth == "light"`:**

```
DESIGN SYSTEM DETECTION COMPLETE (Light Mode)
-----------------------------------------------

PLATFORM: {platform_name or 'all'}
UI PRESENCE: {Yes/No} {if No, show "(Not Applicable)"}

TOKEN INVENTORY
  Colors:      {n} tokens found    [Confidence: {level}]
  Typography:  {n} tokens found    [Confidence: {level}]
  Spacing:     {n} tokens found    [Confidence: {level}]
  Other:       {n} tokens found    [Confidence: {level}]

COMPONENTS: {n} components detected across {n} categories

SEVERITY SUMMARY
  Critical: {n}  |  High: {n}  |  Medium: {n}  |  Low: {n}  |  Info: {n}

OVERALL SCORE: {score}/10

OUTPUT FILE (1):
  $JAAN_OUTPUTS_DIR/detect/design/summary{-platform}.md

Note: Run with --full for brand assets, UI patterns, accessibility audit,
governance signals, and full drift analysis (6 output files).
```

> "Proceed with writing summary to $JAAN_OUTPUTS_DIR/detect/design/? [y/n]"

**If `run_depth == "full"`:**

```
DESIGN SYSTEM DETECTION COMPLETE
---------------------------------

PLATFORM: {platform_name or 'all'}
UI PRESENCE: {Yes/No} {if No, show "(Not Applicable)"}

TOKEN INVENTORY
  Colors:      {n} tokens found    [Confidence: {level}]
  Typography:  {n} tokens found    [Confidence: {level}]
  Spacing:     {n} tokens found    [Confidence: {level}]
  Other:       {n} tokens found    [Confidence: {level}]

COMPONENTS: {n} components detected across {n} categories
DRIFT FINDINGS: {n} drift issues found
ACCESSIBILITY: {n} a11y findings

SEVERITY SUMMARY
  Critical: {n}  |  High: {n}  |  Medium: {n}  |  Low: {n}  |  Info: {n}

OVERALL SCORE: {score}/10

OUTPUT FILES (6):
  $JAAN_OUTPUTS_DIR/detect/design/brand{-platform}.md          - Brand signals
  $JAAN_OUTPUTS_DIR/detect/design/tokens{-platform}.md         - Design token inventory
  $JAAN_OUTPUTS_DIR/detect/design/components{-platform}.md     - Component inventory
  $JAAN_OUTPUTS_DIR/detect/design/patterns{-platform}.md       - UI patterns and conventions
  $JAAN_OUTPUTS_DIR/detect/design/accessibility{-platform}.md  - A11y findings
  $JAAN_OUTPUTS_DIR/detect/design/governance{-platform}.md     - Governance signals

Note: {-platform} suffix only if multi-platform mode (e.g., -web, -mobile). Single-platform mode has no suffix.
      If UI presence = No, files contain "Not Applicable" findings.
```

> "Proceed with writing 6 output files to $JAAN_OUTPUTS_DIR/detect/design/? [y/n]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Write Output Files

## Step 9: Write to $JAAN_OUTPUTS_DIR/detect/design/

Create directory `$JAAN_OUTPUTS_DIR/detect/design/` if it does not exist.

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/detect-shared-reference.md` sections "Output Path Logic" and "Stale File Cleanup" for platform-specific suffix convention and run_depth cleanup rules.

### If `run_depth == "light"`: Write Single Summary File

Write one file: `$JAAN_OUTPUTS_DIR/detect/design/summary{suffix}.md`

Contents:
1. Universal YAML frontmatter with `platform` field, `findings_summary`, and `overall_score`
2. **Executive Summary** — BLUF of design system findings
3. **Token Inventory** — categories, count, naming convention, confidence levels (from Step 1)
4. **Component Inventory** — name, category, variant count (from Step 2)
5. **Token Coverage Gaps** — categories defined vs categories missing
6. **Top Findings** — up to 5 highest-severity findings with evidence blocks
7. "Run with `--full` for brand assets, UI patterns, accessibility audit, governance signals, and full drift analysis."

### If `run_depth == "full"`: Write 6 Output Files

Write 6 output files using the template:

| File | Content |
|------|---------|
| `$JAAN_OUTPUTS_DIR/detect/design/brand{suffix}.md` | Brand signals (colors, typography, logos) |
| `$JAAN_OUTPUTS_DIR/detect/design/tokens{suffix}.md` | Design token definitions and usage with drift findings |
| `$JAAN_OUTPUTS_DIR/detect/design/components{suffix}.md` | Component inventory and patterns |
| `$JAAN_OUTPUTS_DIR/detect/design/patterns{suffix}.md` | UI patterns and conventions |
| `$JAAN_OUTPUTS_DIR/detect/design/accessibility{suffix}.md` | A11y implementation findings (scoped to repo evidence) |
| `$JAAN_OUTPUTS_DIR/detect/design/governance{suffix}.md` | Design system governance signals |

**Note**: `{suffix}` is empty for single-platform mode, or `-{platform}` for multi-platform mode.

**If UI presence = No** (from Step 0 check), write minimal "Not Applicable" files with:
- Frontmatter: `findings_summary.informational: 1`, `overall_score: 10.0`
- Single finding: "E-DSN-{PLATFORM}-001: No UI Components Detected" (severity: informational)

Each file MUST include:
1. Universal YAML frontmatter with `platform` field and findings_summary/overall_score
2. Executive Summary
3. Scope and Methodology
4. Findings with evidence blocks (using E-DSN-{PLATFORM}-NNN or E-DSN-NNN IDs)
5. Recommendations

---

## Step 9a: Seed Reconciliation

> **Reference**: See `${CLAUDE_PLUGIN_ROOT}/docs/extending/seed-reconciliation-reference.md` for comparison rules, discrepancy format, and auto-update protocol.

1. Read domain-relevant seed files: `$JAAN_CONTEXT_DIR/tone-of-voice.template.md`
2. Compare detection results against seed content (brand colors, typography, voice characteristics if design tokens reference them)
3. If discrepancies found:
   - Display discrepancy table to user
   - Offer auto-updates for non-destructive changes: `[y/n]`
   - Suggest `/jaan-to:learn-add` commands for patterns worth documenting
4. If no discrepancies: display "Seed files are aligned with detection results."

---

## Step 10: Capture Feedback

> "Any feedback on the design system detection? [y/n]"

If yes:
- Run `/jaan-to:learn-add detect-design "{feedback}"`

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- Evidence-based findings with confidence scoring
- Fork-isolated execution (`context: fork`)
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

**If `run_depth == "light"`:**

- [ ] Single summary file written to `$JAAN_OUTPUTS_DIR/detect/design/summary{suffix}.md`
- [ ] Universal YAML frontmatter with `overall_score`
- [ ] Token and component findings have evidence blocks with E-DSN-NNN IDs
- [ ] Confidence scores assigned to all findings
- [ ] Detection summary shown to user before writing
- [ ] User approved output

**If `run_depth == "full"`:**

- [ ] All 6 output files written to `$JAAN_OUTPUTS_DIR/detect/design/`
- [ ] Universal YAML frontmatter with `platform` field in every file
- [ ] Every finding has evidence block with correct ID format (E-DSN-NNN for single-platform, E-DSN-{PLATFORM}-NNN for multi-platform)
- [ ] Drift findings have paired evidence (definition + conflicting usage)
- [ ] Accessibility findings scoped to repo evidence (no runtime claims)
- [ ] Confidence scores assigned to all findings
- [ ] Overall score calculated
- [ ] Output filenames match platform suffix convention (no suffix for single-platform, -{platform} suffix for multi-platform)
- [ ] If no UI files detected for platform, minimal "Not Applicable" files created with informational findings
- [ ] User approved output
- [ ] Seed reconciliation check performed (discrepancies reported or alignment confirmed)
