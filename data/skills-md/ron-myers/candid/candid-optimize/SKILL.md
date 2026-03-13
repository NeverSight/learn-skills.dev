---
name: candid-optimize
description: Audit and optimize the context candid loads during reviews — Technical.md efficiency, exclude patterns, decision register, and config tuning
---

# Context Optimizer

You are a context efficiency analyst for the Candid code review plugin. Your job is to audit everything that gets loaded into the LLM context during reviews and provide actionable optimizations to reduce waste and improve review quality.

## Token Estimation

Throughout this skill, estimate tokens using: `characters / 4` (approximate for English text). This is a rough estimate — label all numbers with `~` prefix.

## Workflow

### Step 1: Parse CLI Arguments

Check for flags:

| Flag | Behavior |
|------|----------|
| `--dry-run` | Show recommendations without applying. Skip Step 7 apply phase. |
| `--apply-all` | Apply all optimizations without prompting. Skip Step 7 selection prompt. |
| `--section <name>` | Only run the named section. Valid: `technical-md`, `excludes`, `register`, `config` |

If `--section` is provided with an unrecognized value, output an error and exit:
```
❌ Unknown section "[value]". Valid sections: technical-md, excludes, register, config
```

If `--section` is valid, skip sections not matching the name. The token budget (Step 2) always runs regardless of `--section` since other sections reference it.

### Step 2: Locate Context Files & Estimate Token Budget

Find all context files that candid loads during reviews.

#### 2.1 Find Technical.md

```
1. Check ./Technical.md
2. If not found, check ./.candid/Technical.md
3. Store path or null
```

If found: Read the file, count characters, estimate tokens.
If not found: Note as missing, set tokens to 0.

#### 2.2 Find Config Files

```
1. Read .candid/config.json (project config)
2. Read ~/.candid/config.json (user config)
3. Store contents and token estimates for each
```

For each file: if exists, count characters and estimate tokens. If not, note as missing.

#### 2.3 Find Decision Register

From project config, extract `decisionRegister.path` (default: `.candid/register`).
Strip any trailing slash from the path before constructing the file path.
Check for `${registerPath}/review-decision-register.md`.

If found: Read the file, count characters, estimate tokens, note the mode (`load` vs `lookup`).
If not found or disabled: Note as not present, set tokens to 0.

#### 2.4 Display Token Budget

Present the context budget breakdown:

```
Context Budget Estimate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source                    Tokens     Budget
──────────────────────────────────────────────
Technical.md              ~[N]       [bar]  [%]
Decision register         ~[N]       [bar]  [%]
Config files              ~[N]       [bar]  [%]
──────────────────────────────────────────────
Fixed context total       ~[N]

Note: Code diffs, full file reads, and import graphs
are loaded dynamically and vary per review.
```

**Bar chart:** Use `█` for filled and `░` for empty, 10 characters wide, proportional to percentage of total.

**Thresholds to flag:**
- Technical.md over 500 lines → `⚠️  Technical.md exceeds recommended 500-line limit ([N] lines)`
- Fixed context total over 8,000 tokens → `⚠️  Fixed context is high (~[N] tokens). Consider optimizations below.`
- Decision register in "load" mode over 2,000 tokens → `⚠️  Decision register in "load" mode is consuming ~[N] tokens. Consider "lookup" mode.`

If no Technical.md, no config, and no register exist:
```
ℹ️  No candid context files found.
```
Note: Do NOT exit early in this case. Steps 4 (exclude pattern scanning) and 6 (config tuning) can still produce valuable recommendations for projects without existing candid setup. Continue to subsequent steps.

### Step 3: Analyze Technical.md Efficiency

**Skip if:** Technical.md not found, or `--section` is set and not `technical-md`.

Read Technical.md and analyze each rule for optimization potential.

#### 3.1 Parse Rules

Extract rules from Technical.md using the same approach as candid-validate-standards:
- Lines starting with `-` or `*` (list items)
- Lines starting with numbers (numbered lists)
- Lines following a `##` heading
- Skip code blocks, empty lines, heading lines themselves

Store each rule with: line number, section heading, full text, character count.

#### 3.2 Identify Verbose Rules

Flag rules where the text exceeds 200 characters and could be condensed without losing meaning.

Look for:
- Rules with lengthy explanations that could be split into rule + example
- Rules with redundant qualifiers ("make sure to always", "it is important that")
- Rules that repeat the section heading in the rule text

For each verbose rule, draft a condensed version and calculate token savings.

#### 3.3 Identify Near-Duplicate Rules

Compare rules within the same section for redundancy. Cap output at 5 duplicate pairs maximum to avoid overwhelming the user.

For each pair of rules within the same section:
1. Normalize both rules: lowercase, remove punctuation, split into words
2. Remove common stop words (the, a, an, is, are, must, should, in, for, to, of, and, or, with, that, this, be, not, all, from, by, at, on, it, as, do, no, if, use)
3. Count remaining words shared between both rules
4. Calculate overlap: `shared words / min(words in rule A, words in rule B)`
5. If overlap > 0.7, flag as likely duplicate

For each flagged pair, suggest keeping the more specific rule (the one with file paths, numbers, or examples) and removing the other. Estimate token savings from the removed rule's character count / 4.

Do NOT compare across sections — rules in different sections serve different purposes even if they share terminology.

#### 3.4 Identify Low-Signal Rules

Flag rules that meet ALL THREE of these criteria simultaneously:
1. No file paths or directory references (no `/`, no `.ts`, no `.py`, no specific filenames)
2. No concrete numbers or thresholds
3. No domain-specific technical terms (e.g., "JWT", "SQL injection", "PII" are domain-specific and valuable even without file paths)

Rules like "All async functions must have try/catch" or "Never log PII" are valuable despite lacking file paths — they contain specific, verifiable technical requirements. Only flag rules that are truly generic platitudes.

For flagged rules, suggest making them project-specific by adding file paths or examples. Do not suggest removal — the user should decide.

#### 3.5 Present Technical.md Findings

```
Technical.md Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: [path]
Total rules: [N]
Total tokens: ~[N]

Verbose Rules ([N] found, est. savings: ~[N] tokens)
  Line [L]: "[first 60 chars]..."
    → Condensed: "[shorter version]"
    → Saves ~[N] tokens

Near-Duplicate Rules ([N] pairs, est. savings: ~[N] tokens)
  Lines [L1] & [L2]: Both say "[summary]"
    → Keep line [L1], remove line [L2]
    → Saves ~[N] tokens

Low-Signal Rules ([N] found, est. savings: ~[N] tokens)
  Line [L]: "[rule text]"
    → Generic rule with no project-specific references
    → Suggest: add file paths/examples or remove

Total potential savings: ~[N] tokens ([P]% of Technical.md)
```

### Step 4: Scan for Missing Exclude Patterns

**Skip if:** `--section` is set and not `excludes`.

Scan the repository for common file types that waste context when reviewed.

#### 4.1 Load Current Exclusions

Read `.candid/config.json` and extract the `exclude` array.
If no config or no exclude field, treat as empty array.

#### 4.2 Scan for Excludable Files

Run these checks:

```bash
# Generated files
find . -maxdepth 4 -type f \( -name "*.generated.*" -o -name "*.g.dart" -o -name "*.g.ts" -o -name "*.g.go" \) 2>/dev/null | grep -v node_modules | grep -v .git | head -5

# Build output directories
ls -d dist/ build/ .next/ out/ .nuxt/ .svelte-kit/ 2>/dev/null

# Vendored code
ls -d vendor/ third_party/ 2>/dev/null

# Minified files
find . -maxdepth 4 -type f \( -name "*.min.js" -o -name "*.min.css" \) 2>/dev/null | grep -v node_modules | grep -v .git | head -5

# Lock files
ls package-lock.json yarn.lock pnpm-lock.yaml Gemfile.lock poetry.lock composer.lock go.sum 2>/dev/null

# Protocol buffer / code-gen output
find . -maxdepth 4 -type f \( -name "*.pb.go" -o -name "*.pb.ts" -o -name "*_pb2.py" \) 2>/dev/null | grep -v node_modules | grep -v .git | head -5

# Source maps
find . -maxdepth 4 -type f -name "*.map" 2>/dev/null | grep -v node_modules | grep -v .git | head -5
```

#### 4.3 Compare Against Current Exclusions

For each detected file/directory, check if any existing exclude pattern would match it.

Simple glob matching:
- `dist/*` matches files in `dist/`
- `*.min.js` matches any `.min.js` file
- `**/*.generated.*` matches generated files at any depth

#### 4.4 Present Exclude Findings

```
Exclude Pattern Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current patterns: [list or "none configured"]

Missing Patterns ([N] found)

  [type]  [suggested pattern]
    Found: [example file(s)]
    Impact: These files would be skipped during review

  [type]  [suggested pattern]
    Found: [example file(s)]
    Impact: These files would be skipped during review
```

If all detected files are already excluded:
```
✅ Exclude patterns look good. No unexcluded generated/vendor/build files detected.
```

### Step 5: Analyze Decision Register

**Skip if:** Decision register is not enabled or file doesn't exist, or `--section` is set and not `register`.

#### 5.1 Parse Register

Read the register markdown file and parse:
- Count rows in Open Questions table → `openCount`
- Count rows in Resolved Questions table → `resolvedCount`
- Total entries = `openCount + resolvedCount`
- Estimate total tokens from file size

#### 5.2 Analyze

Check for optimization opportunities:

**Mode optimization:**
- If register mode is `"load"` and total tokens > 2,000: recommend switching to `"lookup"` mode
  - Note: In `"lookup"` mode, the register file is still read and parsed at review start, but entries are checked per-question rather than loaded into the prompt as full context. The savings come from not injecting the entire register text into the LLM context. Estimate savings as ~80% of register tokens (the file is read but not surfaced in full).

**Pruning:**
- If resolved entries > 100: recommend pruning oldest resolved entries beyond 100
  - Calculate tokens from entries that would be removed

**Duplicate detection:**
- Compare open questions by file path + normalized question text
- Flag pairs where same file + >70% keyword overlap

#### 5.3 Present Register Findings

```
Decision Register Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Path: [register path]
Mode: [load/lookup]
Entries: [N] open, [M] resolved ([total] total)
Tokens: ~[N]

Recommendations:
  [icon] [recommendation description]
    → [action to take]
    → Saves ~[N] tokens
```

If no issues found:
```
✅ Decision register looks healthy. [N] entries, ~[N] tokens.
```

### Step 6: Config Tuning Recommendations

**Skip if:** `--section` is set and not `config`.

Check for configuration improvements that enhance review quality.

#### 6.1 Missing Config

If Technical.md exists but no `.candid/config.json`:
```
📋 No project config found. Create .candid/config.json to persist tone, exclude patterns, and other settings.
   → Run /candid-init to generate both Technical.md and config.json
```

#### 6.2 Missing Exclude Patterns

If Step 4 found unexcluded files and config has no `exclude` field:
```
📋 Config has no exclude patterns. Add detected patterns to skip generated/vendor files during review.
```

#### 6.3 Merge Target Branches

Check if `mergeTargetBranches` is configured in `.candid/config.json`. If already set, skip.

If not configured, detect branching strategy:

```bash
git branch -a 2>/dev/null
```

Map detected branches to a suggestion:

| Detection | Strategy | Suggested value |
|-----------|----------|-----------------|
| `develop` branch exists (local or remote) | Git Flow | `["develop", "main"]` |
| `trunk` branch exists | Trunk-based | `["trunk"]` |
| `main` and `master` both exist | Migration | `["main"]` |
| `main` exists (no develop/trunk) | GitHub Flow | `["main"]` |
| `master` exists (no main) | Legacy | `["master"]` |

If a suggestion can be made:
```
📋 Detected [strategy] branching. Consider adding to config:
   "mergeTargetBranches": [suggested value]
   Candid defaults to ["main", "stable", "master"] without this setting.
```

#### 6.4 Focus Mode Suggestion

If Technical.md exceeds 300 lines:
```
📋 Technical.md is [N] lines. For routine reviews, consider using --focus to limit scope:
   /candid-review --focus security      # Security-focused
   /candid-review --focus performance   # Performance-focused
   This reduces the categories checked, making reviews faster and more targeted.
```

#### 6.5 Register Mode

If decision register is enabled with `"load"` mode and register tokens > 2,000:
```
📋 Decision register in "load" mode adds ~[N] tokens per review. Switch to "lookup" mode for large registers.
```

#### 6.6 Present Config Findings

```
Config Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[list each recommendation with icon and description]
```

If no issues:
```
✅ Config looks well-tuned. No recommendations.
```

### Step 7: Present Summary & Apply Optimizations

#### 7.1 Collect All Recommendations

Number each recommendation sequentially across all sections. Store:
- `id`: Sequential number
- `section`: Which section (technical-md, excludes, register, config)
- `type`: Specific type (verbose, duplicate, low-signal, missing-pattern, mode, prune, etc.)
- `description`: Human-readable description
- `tokenSavings`: Estimated token savings (0 for config-only changes)
- `action`: What to do (edit Technical.md, update config, rewrite register, etc.)
- `details`: Specifics needed to apply (line numbers, patterns, etc.)

#### 7.2 Display Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Optimization Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Section Name] (est. savings: ~[N] tokens)
  [#]. [[type]] [description]
  [#]. [[type]] [description]

[Section Name] (est. savings: ~[N] tokens)
  [#]. [[type]] [description]

[Section Name] (improves review quality)
  [#]. [[type]] [description]

──────────────────────────────────────────────
Total potential savings: ~[N] tokens
──────────────────────────────────────────────
```

If no recommendations in any section:
```
✅ Your candid context is well-optimized. No changes recommended.

Current budget: ~[N] tokens fixed context per review.
```
Exit — nothing to apply.

#### 7.3 Apply Phase

**If `--dry-run`:**
```
Dry run complete. No changes applied.
To apply: run /candid-optimize or /candid-optimize --apply-all
```
Exit.

**If `--apply-all`:**
Apply all recommendations (proceed to 7.4 for each).

**Otherwise (interactive):**

Use AskUserQuestion:

**Question:** "Which optimizations would you like to apply?"

**Options:**
1. "Apply all ([N] optimizations)" — Apply everything
2. "Review each one" — Go through each recommendation individually
3. "None — I'll handle manually" — Exit without applying

If "Review each one": Loop through each recommendation with AskUserQuestion:
- Show the recommendation number and total count (e.g., "[1/8]"), type, description
- Options: "Apply", "Skip", "Apply all remaining"
- Track which were selected
- If "Apply all remaining" is chosen, add all remaining recommendations to the selected list and exit the loop

If "None": Exit with message:
```
No changes applied. Recommendations saved above for manual review.
```

#### 7.4 Apply Selected Optimizations

**Important ordering rules:**
- Apply Technical.md edits in **reverse line-number order** (highest line first) to prevent line shifts from invalidating subsequent edits
- Batch all config.json changes into a single write (collect exclude patterns, mode changes, and new config creation into one operation)
- Apply register changes last

For each selected recommendation, apply based on type:

**Technical.md verbose/duplicate/low-signal:**
- Sort edits by line number descending
- Use Edit tool to modify Technical.md for each edit
- For verbose rules: replace with condensed version
- For duplicates: remove the less specific rule
- For low-signal: add a comment `<!-- candid-optimize: consider adding project-specific paths -->` above the rule (do not delete — let the user decide)

**Config file changes (exclude patterns, register mode, missing config):**
- Ensure `.candid/` directory exists:
  ```bash
  mkdir -p .candid
  ```
- If `.candid/config.json` exists, read it and validate JSON:
  ```bash
  jq empty .candid/config.json 2>&1
  ```
  If invalid JSON, warn the user and skip config changes:
  ```
  ⚠️  Cannot update .candid/config.json: malformed JSON. Fix the file manually.
  ```
- If valid (or creating new), merge all config changes into one write:
  - Add new `exclude` patterns to the existing array (or create new array)
  - Update `decisionRegister.mode` if recommended
  - For new config: start with `{"version": 1}` and include all applicable changes
- Write the merged config using Write tool

**Decision register pruning:**
- Read the register markdown file
- If file doesn't parse correctly (missing table headers, truncated), warn and skip:
  ```
  ⚠️  Decision register appears malformed. Skipping pruning.
  ```
- Parse resolved entries
- Keep most recent 100 resolved entries, remove older ones
- Rewrite the file with Write tool

#### 7.5 Show Before/After

After applying all changes, re-read any modified context files (Technical.md, config.json, decision register) and re-estimate their token counts using chars/4. Use the Step 2 estimates as "Before" and the fresh estimates as "After".

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Changes Applied
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ [description of change 1]
  ✓ [description of change 2]
  ✗ [skipped recommendation]

Before: ~[N] tokens fixed context
After:  ~[N] tokens fixed context
Saved:  ~[N] tokens ([P]% reduction)

Files modified:
  - [file path 1]
  - [file path 2]
```

## Edge Cases

### No Technical.md and no config
Output the token budget (all zeros), note that no context files exist. Continue to Steps 4 and 6 — exclude pattern scanning and config tuning recommendations are still valuable for fresh projects. Suggest running `/candid-init` as one of the config recommendations in Step 6.

### Technical.md exists but is already optimal
If no verbose, duplicate, or low-signal rules found, skip Section 3 findings and note:
```
✅ Technical.md is efficient. [N] rules, ~[N] tokens. No optimizations found.
```

### Config exists but is empty (`{}`)
Treat as valid config with no preferences. Recommend adding settings based on detected patterns.

### Decision register disabled
Skip Section 5 entirely. Note in summary:
```
Decision register: disabled (no analysis needed)
```

### --section with non-existent context
If `--section technical-md` but no Technical.md exists:
```
❌ No Technical.md found. Cannot analyze.
   Create one with: /candid-init
```

If `--section register` but decision register is disabled or file doesn't exist:
```
ℹ️  Decision register is not enabled or has no file. Nothing to analyze.
   Enable it in .candid/config.json: {"decisionRegister": {"enabled": true}}
```

If `--section excludes` or `--section config`: these always produce output (scanning the repo or checking config state), so no special handling needed.

## Quality Checklist

Before presenting results, verify:

- [ ] Token estimates use `~` prefix (never claim exact counts)
- [ ] Every recommendation includes an estimated token savings or states "improves quality"
- [ ] Technical.md edits are applied in reverse line-number order
- [ ] Config changes are batched into a single write
- [ ] `mkdir -p .candid` runs before any config file creation
- [ ] Invalid JSON in existing config is detected and warned about, not silently overwritten
- [ ] Low-signal rule detection does not flag rules with domain-specific technical terms
- [ ] Duplicate detection is capped at 5 pairs maximum
- [ ] The before/after summary re-reads modified files for accurate "After" estimates
