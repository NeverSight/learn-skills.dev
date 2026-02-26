---
name: wp-pr-review
description: Review WordPress plugin PRs for security, performance, WPCS standards, and backward compatibility. Use when reviewing WordPress PRs.
  WPCS standards violations, and backward compatibility. Use for WordPress PR review,
  plugin code review, WP security audit, WPCS check.
allowed-tools: Read, Glob, Grep, Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr comment:*), Bash(gh api:*), Bash(glab mr diff:*), Bash(glab mr comment:*), Bash(git diff:*), Bash(git log:*), Write($JAAN_OUTPUTS_DIR/wp/**), Edit(jaan-to/config/settings.yaml)
argument-hint: <pr-url | owner/repo#number | local>
disable-model-invocation: true
license: MIT
compatibility: Designed for Claude Code with jaan-to plugin. Requires jaan-init setup.
---

# wp-pr-review

> Review WordPress plugin pull requests for security, performance, standards, and compatibility.

## Context Files

- `$JAAN_LEARN_DIR/jaan-to-wp-pr-review.learn.md` - Past lessons (loaded in Pre-Execution)
- `$JAAN_TEMPLATES_DIR/jaan-to-wp-pr-review.template.md` - Report output template
- Research: `$JAAN_OUTPUTS_DIR/research/67-wp-pr-review.md` - Full research document
- `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md` - Language resolution protocol

**Reference files** (loaded on demand during review):
- `references/security-checklist.md` - Sanitization, escaping, nonce, capability, DB security
- `references/performance-checklist.md` - N+1 queries, autoload, unbounded queries, asset loading
- `references/standards-checklist.md` - WPCS naming, Yoda, i18n, prefix, WP API usage
- `references/vulnerability-patterns.md` - CVE patterns, grep commands, dangerous functions
- `references/addon-ecosystem.md` - Hook contracts, API stability, schema changes

**Output path**: `$JAAN_OUTPUTS_DIR/wp/pr/` — ID-based folder pattern.

## Input

**Arguments**: $ARGUMENTS

Input modes:
1. **PR URL**: `https://github.com/owner/repo/pull/123` or `https://gitlab.com/owner/repo/-/merge_requests/123`
2. **Shorthand**: `owner/repo#123` (GitHub) or `owner/repo!123` (GitLab)
3. **Local**: `local` or empty — uses `git diff main...HEAD` on current repo

---

## Pre-Execution Protocol
**MANDATORY** — Read and execute ALL steps in: `${CLAUDE_PLUGIN_ROOT}/docs/extending/pre-execution-protocol.md`
Skill name: `wp-pr-review`
Execute: Step 0 (Init Guard) → A (Load Lessons) → B (Resolve Template) → C (Offer Template Seeding)

### Language Settings
Read and apply language protocol: `${CLAUDE_PLUGIN_ROOT}/docs/extending/language-protocol.md`
Override field for this skill: `language_wp-pr-review`

---

# PHASE 1: Analysis

## Step 0: Parse Input and Detect Mode

Classify `$ARGUMENTS`:

| Pattern | Mode | Action |
|---------|------|--------|
| `https://github.com/.../pull/N` | GitHub URL | Extract owner, repo, PR number |
| `https://gitlab.com/.../-/merge_requests/N` | GitLab URL | Extract owner, repo, MR number |
| `owner/repo#N` | GitHub shorthand | Extract owner, repo, PR number |
| `owner/repo!N` | GitLab shorthand | Extract owner, repo, MR number |
| `local` or empty | Local diff | Use current repo, `git diff main...HEAD` |

Confirm to user:
> "Review mode: {mode} | Target: {owner}/{repo} #{number}"

## Step 1: Context Gathering

Read project configuration files to understand the plugin under review. For remote PRs, first fetch the PR metadata to understand the repo structure, then read available config files.

1. **Read `composer.json`** (if exists) — PHP version constraints, dependencies, autoload config
2. **Read `phpcs.xml.dist` or `.phpcs.xml`** (if exists) — WPCS config: text domain, prefix, minimum WP version
3. **Read `phpstan.neon` or `phpstan.neon.dist`** (if exists) — static analysis level
4. **Read main plugin file** — the file with `Plugin Name:` header. Extract: `Requires at least`, `Requires PHP`, `Text Domain`, `Version`, `Requires Plugins`

Store and display gathered context:

```
PROJECT CONTEXT
───────────────
Plugin Name: {name}
Text Domain: {text-domain}
Prefix: {prefix}
Min WP: {version}
Min PHP: {version}
PHPCS Standard: {standard} (or "none detected")
PHPStan Level: {level} (or "none detected")
```

## Step 2: Diff Acquisition

Based on input mode, fetch the diff using a fallback chain.

### 2.1: Primary — Full Diff

**GitHub:**
```bash
gh pr view {number} --repo {owner}/{repo} --json files,additions,deletions,title,body
gh pr diff {number} --repo {owner}/{repo}
```

**GitLab:**
```bash
glab mr diff {number} --repo {owner}/{repo}
```

**Local:**
```bash
git diff main...HEAD
git log main..HEAD --oneline
```

If `gh pr diff` succeeds, proceed to 2.3.

### 2.2: Fallback — Paginated File List (GitHub only)

If `gh pr diff` fails (HTTP 406 or diff too large), use the REST API:

```bash
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate --jq '.[].filename'
```

This returns filenames only. For each changed `.php` file, retrieve its patch:

```bash
gh api repos/{owner}/{repo}/pulls/{number}/files --paginate \
  --jq '.[] | select(.filename == "{file}") | .patch'
```

If individual patches are unavailable for a file, note it as "patch unavailable — grep-only review" and rely on Step 3 grep patterns against the file content.

**Large PR batching**: When a PR has more than 50 changed PHP files, process files in batches of 30 to reduce per-call context size. Complete analysis of each batch before loading the next.

### 2.3: Parse and Classify

Parse the diff (or file list from fallback) to identify:
- List of changed `.php` files (primary review targets)
- Other changed files (`.js`, `.css`, `.json` — note but don't deep-review)
- Lines added/removed per file (mark "N/A" for fallback-acquired files)
- Skip files in `vendor/`, `node_modules/`, `.git/`

Show summary:
> "Diff acquired: {N} PHP files changed (+{additions} / -{deletions} lines)"
> If fallback was used: "Note: Used paginated API fallback — {N} files retrieved via REST endpoint"
> If batching active: "Large PR detected ({N} PHP files) — processing in batches of 30"

## Step 3: Deterministic Security Scan

Read `references/vulnerability-patterns.md` for the grep pattern catalog.

Run grep patterns against **changed PHP files ONLY**. This is the high-signal, low-noise first pass.

**Batching for large diffs**: If the PR has more than 50 changed PHP files, split the file list into batches of 30 and run each grep pattern set per batch. Complete one batch fully before moving to the next. This prevents excessively large grep output from triggering connection resets.

**CRITICAL patterns** — run all of these:

1. **Superglobal access**: `$_GET`, `$_POST`, `$_REQUEST`, `$_SERVER`, `$_COOKIE`
2. **Database queries without prepare()**: `$wpdb->query`, `$wpdb->get_results`, `$wpdb->get_var`, `$wpdb->get_row`, `$wpdb->get_col` — grep and check if `prepare()` is used
3. **Dangerous functions**: `unserialize`, `eval(`, `assert(`, `create_function`, `extract(`, `shell_exec`, `exec(`, `system(`, `passthru`, `popen`
4. **REST routes**: `register_rest_route` — check for `permission_callback`
5. **REST permissive callback**: `permission_callback.*__return_true`
6. **AJAX handlers**: `wp_ajax_` — check for nonce and capability
7. **is_admin() misuse**: Used as authorization instead of capability check

**WARNING patterns** — run these next:

1. **Unbounded queries**: `posts_per_page.*-1`, `nopaging.*true`
2. **Hardcoded table prefix**: Literal `wp_options`, `wp_posts`, etc. instead of `$wpdb->prefix`
3. **PHP functions instead of WP**: `wp_redirect` without `wp_safe_redirect`, `json_encode` without `wp_json_encode`, `file_get_contents`, `curl_init`
4. **Direct header redirect**: `header(` with `Location`

Store all grep matches with file paths and line numbers for contextual analysis in Step 4.

## Step 4: Contextual LLM Analysis

For each grep match from Step 3, read the surrounding code context (5-10 lines before and after) and determine:

### 4.1: True/False Positive Filtering

- Is this `$_POST` access actually sanitized on the same or next line?
- Is this `$wpdb->get_results()` call using `prepare()` in the same statement?
- Is this `echo` output properly escaped with `esc_html()`, `esc_attr()`, or `wp_kses()`?
- Is this `file_get_contents()` for a local file (acceptable) or remote URL (not acceptable)?
- Is this `is_admin()` used alongside `current_user_can()` (acceptable) or alone as auth (not acceptable)?

### 4.2: Standards Review

Read `references/standards-checklist.md` on demand. Check changed code for:

- Naming convention violations (camelCase instead of snake_case)
- Missing Yoda conditions in comparisons
- Missing i18n on user-facing strings
- Incorrect or missing text domain
- Unprefixed public functions, classes, constants
- Use of PHP functions where WordPress equivalents exist

### 4.3: Backward Compatibility

Check changed code for:

- PHP 8.0+ syntax without version guards (named args, union types, match, nullsafe)
- PHP 8.1+ syntax (enums, readonly, fibers)
- PHP 8.2+ issues (dynamic properties, null to non-nullable params)
- Named arguments on WordPress core functions (prohibited)
- Use of deprecated WordPress functions

### 4.4: Performance Review

Read `references/performance-checklist.md` on demand. Check for:

- Database queries inside loops (N+1 pattern)
- `update_option()` without explicit `autoload` parameter for large data
- Assets enqueued globally without conditional checks
- Cron scheduling without duplicate check or deactivation cleanup
- Missing transient/cache for expensive operations

### 4.5: Add-on Ecosystem Impact

Read `references/addon-ecosystem.md` on demand. If the PR modifies hooks, public methods, database schema, or option keys:

- Are hook signatures preserved? (parameter count, order, types)
- Are removed hooks properly deprecated with `do_action_deprecated()` / `apply_filters_deprecated()`?
- Are public method visibility changes backward-compatible?
- Are database schema changes additive (safe) or destructive (breaking)?
- Is there a major version bump for breaking changes?

### 4.6: Assign Severity and Confidence

**Severity classification**:

| Condition | Severity |
|-----------|----------|
| Security vulnerability | CRITICAL |
| Data loss possible | CRITICAL |
| PHP fatal error | CRITICAL |
| Broken access control | CRITICAL |
| Significant performance degradation | WARNING |
| Standards violation with functional impact | WARNING |
| Backward compatibility break | WARNING |
| Missing i18n for user strings | WARNING |
| Style/formatting issue only | INFO |
| Improvement suggestion | INFO |

**Confidence scoring** (0-100):
- **90-100**: Definitive pattern match with clear vulnerability (e.g., `$wpdb->query()` with direct `$_POST` concatenation)
- **80-89**: Strong signal with minor contextual uncertainty (e.g., missing escaping where context is mostly clear)
- **60-79**: Possible issue needing human judgment (FILTERED — do not include)
- **Below 60**: Likely false positive (FILTERED — do not include)

**Only include findings with confidence >= 80.**

---

# HARD STOP — Human Review Gate

Present the review summary:

```
PR REVIEW ANALYSIS COMPLETE
────────────────────────────────────
PR: {title} (#{number})
Repository: {owner}/{repo}
Files reviewed: {count} PHP files (+{additions} / -{deletions})

FINDINGS SUMMARY
────────────────
CRITICAL: {count} issues
WARNING:  {count} issues
INFO:     {count} issues
Filtered: {count} findings below confidence threshold

VERDICT: {APPROVE | REQUEST_CHANGES | COMMENT}

TOP FINDINGS (Preview)
──────────────────────
1. [{severity}] {title} — {file}:{line} (confidence: {score})
2. [{severity}] {title} — {file}:{line} (confidence: {score})
3. [{severity}] {title} — {file}:{line} (confidence: {score})
...

OUTPUT WILL CREATE
──────────────────
- $JAAN_OUTPUTS_DIR/wp/pr/{id}-{slug}/{id}-pr-review-{slug}.md
- Update $JAAN_OUTPUTS_DIR/wp/pr/README.md index
```

**Verdict logic**:
- Any CRITICAL findings -> `REQUEST_CHANGES`
- Only WARNING + INFO -> `COMMENT`
- No findings above threshold -> `APPROVE`

> "Generate full review report? [y/n]"

**Do NOT proceed to Phase 2 without explicit approval.**

---

# PHASE 2: Generation

## Step 5: Generate ID and Folder Structure

```bash
source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/id-generator.sh"
SUBDOMAIN_DIR="$JAAN_OUTPUTS_DIR/wp/pr"
mkdir -p "$SUBDOMAIN_DIR"
NEXT_ID=$(generate_next_id "$SUBDOMAIN_DIR")
```

Generate slug from PR: `{pr-number}-{slugified-pr-title}` (max 50 chars, lowercase, hyphens).

```
OUTPUT_FOLDER="${SUBDOMAIN_DIR}/${NEXT_ID}-${slug}"
MAIN_FILE="${OUTPUT_FOLDER}/${NEXT_ID}-pr-review-${slug}.md"
```

Preview:
> **Output Configuration**
> - ID: {NEXT_ID}
> - Folder: `$JAAN_OUTPUTS_DIR/wp/pr/{NEXT_ID}-{slug}/`
> - Main file: `{NEXT_ID}-pr-review-{slug}.md`

## Step 6: Generate Review Report

Read template from `$JAAN_TEMPLATES_DIR/jaan-to-wp-pr-review.template.md` (if exists) or use the skill's built-in `template.md`.

Fill all sections:

1. **Executive Summary**: 2-3 sentences with verdict and key finding highlights
2. **PR Metadata table**: All gathered context from Step 1
3. **Findings by severity**: CRITICAL first, then WARNING, then INFO
   - Each finding includes: file path, line numbers, category, confidence score
   - CRITICAL findings MUST include both vulnerable code snippet AND fix suggestion
   - WARNING findings SHOULD include fix suggestion where applicable
4. **Review Categories**: Security, Performance, Standards, Backward Compatibility, Add-on Impact
5. **Checklist Summary**: Pass/Fail for each review subcategory
6. **Methodology**: Review approach and confidence scoring explanation

## Step 7: Quality Check

Before showing to user, verify:

- [ ] All CRITICAL findings include both vulnerable code and fix suggestion
- [ ] All included findings have confidence >= 80
- [ ] File paths and line numbers are accurate to the diff
- [ ] No findings from `vendor/` or `node_modules/` directories
- [ ] No formatting-only issues that PHPCS would catch (indentation, spacing, brace style)
- [ ] Verdict matches severity distribution (CRITICAL present = REQUEST_CHANGES)
- [ ] Executive summary is factual and actionable
- [ ] No generic PHP security advice — all recommendations use WordPress-specific functions

If any check fails, fix the report before preview.

## Step 8: Preview and Write

Show the complete review report to user.

> "Write review report? [y/n]"

If approved:

1. Create output folder:
   ```bash
   mkdir -p "$OUTPUT_FOLDER"
   ```

2. Write main output file to `$MAIN_FILE`

3. Update subdomain index:
   ```bash
   source "${CLAUDE_PLUGIN_ROOT}/scripts/lib/index-updater.sh"
   add_to_index \
     "$SUBDOMAIN_DIR/README.md" \
     "$NEXT_ID" \
     "${NEXT_ID}-${slug}" \
     "PR Review: {pr_title}" \
     "{executive_summary_one_line}"
   ```

4. Confirm:
   > "Report written to: `$JAAN_OUTPUTS_DIR/wp/pr/{NEXT_ID}-{slug}/{NEXT_ID}-pr-review-{slug}.md`"
   > "Index updated: `$JAAN_OUTPUTS_DIR/wp/pr/README.md`"

## Step 9: Optional PR Comment (Second Hard Stop)

> "Would you like to post this review as a comment on the PR?"
>
> **This will post a public comment visible to all PR participants.**
>
> [1] Post full review as PR comment
> [2] Post summary only (findings list without code snippets)
> [3] Skip — do not post

**Do NOT post without explicit approval.**

If user chooses option 1 or 2, format the review for the PR platform:

**GitHub:**
```bash
gh pr comment {number} --repo {owner}/{repo} --body "{formatted_review}"
```

**GitLab:**
```bash
glab mr comment {number} --repo {owner}/{repo} --message "{formatted_review}"
```

Confirm:
> "Review posted as comment on {platform} PR #{number}."

## Step 10: Capture Feedback

> "Any feedback on the review? [y/n]"

If yes, invoke `/jaan-to:learn-add wp-pr-review "{feedback}"` to capture the lesson.

---

## Skill Alignment

- Two-phase workflow with HARD STOP for human approval
- WordPress ecosystem-specific patterns
- Template-driven output structure
- Output to standardized `$JAAN_OUTPUTS_DIR` path

## Definition of Done

- [ ] Input parsed and mode detected
- [ ] Project context gathered (plugin header, PHPCS config)
- [ ] Diff acquired and changed files identified
- [ ] Deterministic grep scan completed
- [ ] LLM contextual analysis completed with confidence scores
- [ ] User approved report generation (HARD STOP passed)
- [ ] Report written to `$JAAN_OUTPUTS_DIR/wp/pr/`
- [ ] Index updated
- [ ] PR comment posted (if user opted in)
