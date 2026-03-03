---
name: docs-management
description: Single source of truth and librarian for ALL Claude official documentation. Manages local documentation storage, scraping, discovery, and resolution. Use when finding, locating, searching, or resolving Claude documentation; discovering docs by keywords, category, tags, or natural language queries; scraping from sitemaps or docs maps; managing index metadata (keywords, tags, aliases); or rebuilding index from filesystem. Run scripts to scrape, find, and resolve documentation. Handles doc_id resolution, keyword search, natural language queries, category/tag filtering, alias resolution, sitemap.xml parsing, docs map processing, markdown subsection extraction for internal use, hash-based drift detection, and comprehensive index maintenance.
allowed-tools: Read, Glob, Grep, Bash, Skill
---

# Claude Docs Management

## 🚨🚨🚨 MANDATORY: Hybrid Parallel Pattern 🚨🚨🚨

> **STOP - Before using this skill for ANY Claude Code documentation query:**
>
> **IF YOU ARE THE MAIN AGENT**, you MUST invoke BOTH sources **in the same message**:
>
> 1. **This skill** (`docs-management`) - local cache, token-efficient
> 2. **`claude-code-guide` subagent** - live web search
>
> ```text
> [Skill tool: docs-management]
> "Find documentation about {topic}"
>
> [Task tool: claude-code-guide] (SAME MESSAGE - USE THIS EXACT PROMPT)
> "First WebFetch https://code.claude.com/docs/en/claude_code_docs_map.md to find
> relevant doc pages about {topic}. Then WebFetch those specific pages. Use WebSearch
> only if needed for additional context. Do NOT use Skill tool (not available).
> Return key findings with source URLs."
> ```
>
> **⚠️ CRITICAL:** claude-code-guide does NOT have Skill tool access. Always prompt it
> to use **WebSearch/WebFetch explicitly**. If you see "No such tool: Skill" error,
> you prompted it wrong.
>
> **This is AUTOMATIC. Do NOT wait for user to ask for it.**
>
> **IF YOU ARE A SUBAGENT**: Note in your response that main agent should also query `claude-code-guide`.

---

## 🚨 CRITICAL: Path Doubling Prevention - MANDATORY

**ABSOLUTE PROHIBITION: NEVER use `cd` with `&&` in PowerShell when running scripts from this skill.**

**The Problem:** If your current working directory is already inside the skill directory, using relative paths causes PowerShell to resolve paths relative to the current directory instead of the repository root, resulting in path doubling.

**REQUIRED Solutions (choose one):**

1. **✅ ALWAYS use helper scripts** (recommended - they handle path resolution automatically)
2. **✅ Use absolute path resolution** (if not using helper script)
3. **✅ Use separate commands** (never `cd` with `&&`)

**NEVER DO THIS:**

- ❌ Chain `cd` with `&&`: `cd <relative-path> && python <script>` causes path doubling
- ❌ Assume current directory
- ❌ Use relative paths when current dir is inside skill directory

**For all scripts:** Always run from repository root using relative paths, OR use helper scripts that handle path resolution automatically.

## 🚨 CRITICAL: Large File Handling - MANDATORY SCRIPT USAGE

### ⚠️ ABSOLUTE PROHIBITION: NEVER use read_file tool on the index.yaml file

The file exceeds 25,000 tokens and will ALWAYS fail. You MUST use scripts.

**✅ REQUIRED: ALWAYS use manage_index.py scripts for ANY index.yaml access:**

```bash
python scripts/management/manage_index.py count
python scripts/management/manage_index.py list
python scripts/management/manage_index.py get <doc_id>
python scripts/management/manage_index.py verify
```

All scripts automatically handle large files via `index_manager.py`.

## Available Slash Commands

Use the consolidated `docs-ops` skill for common workflows:

- **`/claude-ecosystem:docs-ops scrape`** - Scrape all configured Claude documentation sources, then refresh index and validate
- **`/claude-ecosystem:docs-ops refresh`** - Refresh the local index and metadata without scraping from remote sources
- **`/claude-ecosystem:docs-ops validate`** - Validate the index and references for consistency and drift without scraping
- **`/claude-ecosystem:docs-ops rebuild-index`** - Force rebuild the search index from filesystem
- **`/claude-ecosystem:docs-ops clear-cache`** - Clear the documentation search cache

## Overview

This skill provides automation tooling for documentation management. It manages:

- **Canonical storage** (encapsulated in skill) - Single source of truth for official docs
- **Subsection extraction** - Token-optimized extracts for skills (60-90% savings)
- **Drift detection** - Hash-based validation against upstream sources
- **Sync workflows** - Quarterly maintenance automation
- **Documentation discovery** - Keyword-based search and doc_id resolution
- **Index management** - Metadata, keywords, tags, aliases for resilient references

**Core value:** Prevents link rot, enables offline access, optimizes token costs, automates maintenance, and provides resilient doc_id-based references.

## Quick Reference: Which Command to Use

| I want to... | Command | Example |
|--------------|---------|---------|
| Find docs by keywords | `search` | `search skills progressive` |
| Find docs by natural language | `query` | `query "how to create skills"` |
| Get full document content | `content` | `content code-claude-com-docs-en-skills` |
| Get specific section | `content --section` | `content <doc_id> --section "metadata"` |
| Resolve doc_id to path | `resolve` | `resolve code-claude-com-docs-en-skills` |
| Find related docs | `related` | `related code-claude-com-docs-en-skills` |
| List docs by category | `category` | `category api` |
| List docs by tag | `tag` | `tag skills` |

**Key Workflow:** `search` by keywords → Get `doc_id` from results → `content` by doc_id

**Important distinctions:**

- `search` and `query` accept **flexible keywords** (no full doc_id needed)
- `content`, `resolve`, and `related` require **full doc_id** (e.g., `code-claude-com-docs-en-skills`)

## When to Use This Skill

This skill should be used when:

- **Scraping documentation** - Fetching docs from sitemaps or docs maps
- **Finding documentation** - Searching for docs by keywords, category, or natural language
- **Resolving doc references** - Converting doc_id to file paths
- **Managing index metadata** - Adding keywords, tags, aliases, updating metadata
- **Rebuilding index** - Regenerating index from filesystem (handles renames/moves)

## Hybrid Parallel Documentation Strategy

> **CRITICAL: This section is the authoritative source for Claude Code documentation access patterns.**

### Architecture Constraint

**Skills cannot spawn subagents.** Only the main conversation thread can use the Task tool.

This means:

- When **main agent** loads this skill → Main agent must also invoke `claude-code-guide` in parallel
- When **subagent** loads this skill → Subagent should note in response that main agent should invoke `claude-code-guide` for live coverage
- When **command** invokes this skill → Same as main agent (commands run in main context)

### Caller-Aware Guidance

**If you are the main agent:**

- You MUST invoke both this skill AND `claude-code-guide` subagent in the SAME message
- This is the only way to get comprehensive Claude Code documentation coverage

**If you are a subagent:**

- You CANNOT invoke `claude-code-guide` yourself (architectural constraint)
- Include in your response: "For comprehensive coverage, main agent should also query claude-code-guide subagent"
- Proceed with local cache results

### Always-Parallel Pattern (Main Agent Only)

**⚠️ MANDATORY DEFAULT BEHAVIOR - NOT OPTIONAL:**

When ANY Claude Code documentation query is detected, the main agent MUST automatically:

1. Invoke `docs-management` skill (local cache)
2. Spawn `claude-code-guide` subagent (live web) **in the same message**

**This is automatic. The user does NOT need to ask for it.**

#### Detection Triggers

Use both sources automatically when user asks about:

- Claude Code features (hooks, skills, memory, MCP, plugins, settings, etc.)
- How to do something in Claude Code
- Claude Code configuration or troubleshooting
- Any topic in the Claude Code documentation

#### Same-Message Parallel Invocation

```text
# Main agent sends BOTH in a single message (AUTOMATIC):

[Skill tool: docs-management]
"Find documentation about {topic}"

[Task tool: claude-code-guide] (same message = parallel execution)
"First WebFetch https://code.claude.com/docs/en/claude_code_docs_map.md to find
relevant doc pages about {topic}. Then WebFetch those specific pages. Use WebSearch
only if needed for additional context. Do NOT use Skill tool (not available).
Return key findings with source URLs."
```

**IMPORTANT:** `claude-code-guide` is a built-in subagent with tools: `Glob, Grep, Read, WebFetch, WebSearch`.
It does NOT have the `Skill` tool - it's designed for **web search**, not local skill invocation.
Always prompt it to use WebSearch/WebFetch explicitly.

#### Synthesis Step

After both complete:

- Combine results from both sources
- Local cache provides category context and token efficiency
- Live search provides currency and gap-filling
- Note any discrepancies between sources

### Two Documentation Sources

| Source | Invoke Via | Strengths |
| ------ | ---------- | --------- |
| `docs-management` (this skill) | `Skill` tool | Fast, token-efficient (60-90% savings), hierarchical categories, offline |
| `claude-code-guide` | `Task` tool | Always current, web search, fetches live URLs |

### Fallback Behavior

- **Plugin not installed**: Use `claude-code-guide` only
- **Live search unavailable**: This skill provides complete local cache
- **Both sources disagree**: Flag discrepancy, prefer official docs, investigate

### Automatic Behavior Summary

| User Query | What Happens (Automatic) |
|------------|--------------------------|
| "How do hooks work?" | Both sources invoked automatically |
| "What's the CLAUDE.md syntax?" | Both sources invoked automatically |
| "Help me set up MCP" | Both sources invoked automatically |
| Any Claude Code topic | Both sources invoked automatically |

**There is no manual trigger.** This is default behavior for Claude Code documentation queries.

### Three-Source Troubleshooting Pattern

When troubleshooting errors, bugs, or unexpected behavior, use **three sources** in parallel:

| Source | Agent/Skill | Purpose |
| ------ | ----------- | ------- |
| Official Docs | `docs-management` skill | Correct usage, configuration |
| GitHub Issues | `claude-code-issue-researcher` agent | Known bugs, workarounds |
| Live Web | `claude-code-guide` subagent | Current discussions |

**Troubleshooting triggers** (automatically detected by hook):

- "error", "bug", "broken", "not working", "fails", "crash"
- "debug", "troubleshoot", "workaround", "issue", "problem"
- "doesn't work", "won't work", "can't", "isn't firing"

**Example prompt for claude-code-issue-researcher:**

```text
Search GitHub issues in anthropics/claude-code for: [ERROR/PROBLEM DESCRIPTION].
Check both open and closed issues. Report issue numbers, status, and any workarounds.
```

### Correct Subagent Pattern

When spawning docs-researcher (or any subagent that uses this skill), the main agent should ALSO spawn claude-code-guide in the same message for comprehensive coverage:

```text
# Main agent spawns BOTH in a single message:

[Task tool: docs-researcher subagent]
"Research Claude Code memory/CLAUDE.md files"

[Task tool: claude-code-guide subagent] (same message = parallel)
"Use WebSearch to find current Claude Code documentation about memory and
CLAUDE.md files on code.claude.com. Return key findings with URLs."

# After both complete, synthesize results
```

**Why both?** The docs-researcher uses local cache (fast, token-efficient), while claude-code-guide searches live web (always current). Together they provide comprehensive coverage.

### Hierarchical Categories (from docs_map.md)

The index includes category hierarchy from the official Claude Code docs map:

| Category | Topics |
| --- | --- |
| **Getting started** | overview, quickstart, common-workflows |
| **Build with Claude Code** | sub-agents, plugins, skills, hooks, mcp, output-styles |
| **Deployment** | amazon-bedrock, google-vertex-ai, sandboxing |
| **Administration** | setup, iam, security, costs |
| **Configuration** | settings, vs-code, jetbrains, memory |
| **Reference** | cli-reference, slash-commands, hooks |
| **Resources** | troubleshooting, legal-and-compliance |

Categories are stored in `doc_map_category` field. Query by category:

```python
resolver.get_by_category("Build with Claude Code")  # Returns all docs in category
resolver.list_categories()  # Returns all categories with counts
```

### Category Enrichment

After scraping, update categories from the official docs map:

```bash
python scripts/core/enrich_categories.py           # Update categories
python scripts/core/enrich_categories.py --dry-run # Preview changes
```

## Workflow Execution Pattern

**CRITICAL: This section defines HOW to execute operations in this skill.**

### Delegation Strategy

#### Default approach: Delegate to Task agent

For ALL scraping, validation, and index operations, delegate execution to a general-purpose Task agent.

**How to invoke:**

Use the Task tool with:

- `subagent_type`: "general-purpose"
- `description`: Short 3-5 word description
- `prompt`: Full task description with execution instructions

### Execution Pattern

**Scripts run in FOREGROUND by default. Do NOT background them.**

When Task agents execute scripts:

- ✅ **Run directly**: `python .claude/skills/docs-management/scripts/core/scrape_all_sources.py --parallel --skip-existing`
- ✅ **Streaming logs**: Scripts emit progress naturally via stdout
- ✅ **Wait for completion**: Scripts exit when done with exit code
- ❌ **NEVER use `run_in_background=true`**: Scripts are designed for foreground execution
- ❌ **NEVER poll output**: Streaming logs appear automatically, no BashOutput polling needed
- ❌ **NEVER use background jobs**: No `&`, no `nohup`, no background process management

### Anti-Pattern Detection

**Red flags indicating incorrect execution:**

🚩 Using `run_in_background=true` in Bash tool
🚩 Repeated BashOutput calls in a loop
🚩 Checking process status with `ps` or `pgrep`
🚩 Manual polling of script output
🚩 Background job management (`&`, `nohup`, `jobs`)
🚩 **Using BashOutput AFTER Task agent completes** ← CRITICAL RED FLAG

**If you recognize these patterns, STOP and correct immediately.**

### After Task Agent Completes

**CRITICAL: When the Task agent reports "Done", READ its report and summarize to the user. DO NOT use BashOutput.**

**Correct workflow:**

1. Task agent reports "Done (X tool uses · Y tokens · Z time)"
2. ✅ READ the agent's message containing its final report
3. ✅ SUMMARIZE the agent's findings to the user
4. ❌ NEVER use BashOutput to "check the real results"
5. ❌ NEVER poll or verify what the agent already reported

### Error and Warning Reporting

**CRITICAL: Report ALL errors, warnings, and issues - never suppress or ignore them.**

When executing scripts via Task agents:

- ✅ **Report script errors**: Exit codes, exceptions, error messages
- ✅ **Report warnings**: Deprecation warnings, import issues, configuration problems
- ✅ **Report unexpected output**: 404s, timeouts, validation failures
- ✅ **Include context**: What was being executed when the error occurred

**Red flags that indicate issues:**

🚩 Non-zero exit code
🚩 Lines containing "ERROR", "FAILED", "Exception", "Traceback"
🚩 "WARNING" or "WARN" messages
🚩 "404 Not Found", "500 Internal Server Error"

### Domain-Specific Reporting for Scraping

**CRITICAL**: When reporting scraping results, distinguish behavior by domain.

**Domain-Specific .md URL Behavior:**

1. **docs.claude.com** and **code.claude.com**: These domains serve .md URLs successfully
2. **anthropic.com**: These domains do NOT serve .md URLs (404 expected, configured with `try_markdown: false`)

**Accurate Reporting:**

✅ **Good (Domain-Specific)**: "docs.claude.com: 97 URLs using direct .md (97 skipped/unchanged). anthropic.com: 164 URLs using HTML conversion (158 skipped/unchanged)."

❌ **Bad (Misleading)**: "All .md URL attempts returned 404 (expected - these are HTML pages)" ← This is misleading because Claude domains successfully use .md URLs

## Quick Start

### Refresh Index End-to-End (No Scraping)

Use this when you want to rebuild and validate the local index/metadata **without scraping**:

**⚠️ IMPORTANT: Use Python 3.13 for validation** - spaCy/Pydantic have compatibility issues with Python 3.14+

```bash
# Use Python 3.13 for full compatibility with spaCy
py -3.13 .claude/skills/docs-management/scripts/management/refresh_index.py
```

Optional flags:

```bash
# Check for missing files before rebuilding
py -3.13 .claude/skills/docs-management/scripts/management/refresh_index.py --check-missing-files

# Detect drift (404s, missing files) after rebuilding
py -3.13 .claude/skills/docs-management/scripts/management/refresh_index.py --check-drift

# Detect and automatically cleanup drift
py -3.13 .claude/skills/docs-management/scripts/management/refresh_index.py --check-drift --cleanup-drift
```

This script runs the full pipeline:

- ✅ Checks dependencies
- ✅ (Optional) Checks for missing files
- ✅ Rebuilds the index from the filesystem
- ✅ Extracts keywords & metadata for all documents
- ✅ Validates metadata coverage
- ✅ Generates a summary report
- ✅ (Optional) Detects and cleans up drift

Expected runtime: ~20-30 seconds for ~500 documents

### Scrape All Sources (Used by `/scrape-official-docs`)

Use this when the user explicitly wants to **hit the network and scrape docs**:

#### Python Version Requirement

- **Python 3.14 works by default** for scraping
- **Python 3.13 required for spaCy operations** (keyword extraction, metadata extraction)

```bash
# Step 1: Scrape documentation (Python 3.14+ works)
python .claude/skills/docs-management/scripts/core/scrape_all_sources.py \
  --parallel \
  --skip-existing

# Step 2: IMMEDIATELY run validation after scraping completes
# ⚠️ Use Python 3.13 for validation (spaCy compatibility)
py -3.13 .claude/skills/docs-management/scripts/management/refresh_index.py

# Step 3: Clean up aged-out Anthropic articles (reads max_age from sources.json)
python .claude/skills/docs-management/scripts/maintenance/cleanup_old_anthropic_docs.py --execute
```

#### Validation and Cleanup Are Required After Scraping

Since `--auto-validate` is now default: False (for speed), you **MUST run validation and cleanup separately** immediately after scraping.

Optional: Detect and cleanup drift after scraping:

```bash
# Auto-cleanup workflow (detect and cleanup in one flag)
python .claude/skills/docs-management/scripts/core/scrape_all_sources.py \
  --parallel \
  --skip-existing \
  --auto-cleanup

# Then validate (use Python 3.13)
py -3.13 .claude/skills/docs-management/scripts/management/refresh_index.py
```

### Find Documentation

**⚠️ CRITICAL: Global flags MUST come BEFORE the subcommand:**

```bash
# ✅ CORRECT - global flags before subcommand
python find_docs.py --json --limit 10 search skills frontmatter

# ❌ WRONG - global flags after subcommand (will fail with "unrecognized arguments")
python find_docs.py search skills frontmatter --json
```

**Examples:**

```bash
# Resolve doc_id to file path
python .claude/skills/docs-management/scripts/core/find_docs.py resolve <doc_id>

# Search by keywords (default: 25 results)
python .claude/skills/docs-management/scripts/core/find_docs.py search skills progressive-disclosure

# Search with custom limit (global options come before subcommand)
python .claude/skills/docs-management/scripts/core/find_docs.py --limit 10 search skills

# Search without limit (returns all matching results)
python .claude/skills/docs-management/scripts/core/find_docs.py --no-limit search skills

# Search with minimum score threshold (filters low-relevance results)
python .claude/skills/docs-management/scripts/core/find_docs.py --min-score 20 search skills

# Natural language search
python .claude/skills/docs-management/scripts/core/find_docs.py query "how to create skills"

# List by category
python .claude/skills/docs-management/scripts/core/find_docs.py category api

# List by tag
python .claude/skills/docs-management/scripts/core/find_docs.py tag skills
```

**Search Accepts Flexible Keywords** (no full doc_ids needed):

- Single keyword: `search skills`
- Multiple keywords: `search skills progressive disclosure`
- Partial words work via token matching: `search skill` matches "skills"
- Singular/plural auto-handled: "skill" matches "skills"
- Stop words removed automatically from queries: "how", "to", "the", etc.

**Search Options:**

| Option | Default | Description |
| --- | --- | --- |
| `--limit N` | 25 | Maximum number of results to return |
| `--no-limit` | - | Return all matching results (no limit) |
| `--min-score N` | - | Only return results with relevance score >= N |
| `--fast` | - | Index-only search (skip content grep) |
| `--separate` | - | Show index matches and content matches separately |
| `--no-context` | - | Hide grep context lines in content matches |
| `--clear-cache` | - | Rebuild search cache before operation |
| `--category` | - | Filter results by category |
| `--tags` | - | Filter results by tags |
| `--json` | - | Output results as JSON |
| `--verbose` | - | Show relevance scores for debugging |

When results are truncated, output shows "showing X of Y total" to indicate more results are available.

### Hybrid Search (Default Behavior)

By default, `search` performs **both** index and content search:

1. **Index search** - Fast keyword matching against document metadata (title, description, keywords, tags)
2. **Content search** - Grep through actual file contents for matches not in index

**Result markers:**

- `[SUBSECTION]` - Match found in a specific document section (click to extract)
- `[CONTENT]` - Match found in file content (not in metadata index)
- No marker - Standard index match

**Performance options:**

- Use `--fast` for index-only search (faster, but may miss content-only matches)
- Use `--separate` to display index and content matches in separate sections

### Search Scoring

Results are ranked by a multi-factor scoring system:

- **Title matches** (highest weight, 14 points)
- **Description matches** (10 points)
- **Keyword field matches** (8-10 points, with variant detection)
- **Tag matches** (5-7 points)
- **Coverage multipliers** (1.5-2.0x for multi-term matches)
- **Domain weighting** (Claude Code docs prioritized over general Anthropic docs)

Use `--verbose` to see scores for debugging relevance issues.

### find_docs.py Command Reference

| Command | Purpose | Subsection Support |
|---------|---------|-------------------|
| `resolve <doc_id>` | Resolve doc_id to file path | ❌ No |
| `content <doc_id>` | Get document content | ✅ Yes (`--section`) |
| `search <keywords>` | Keyword search | ❌ No |
| `query "<text>"` | Natural language search | ❌ No |
| `category <name>` | List docs in category | ❌ No |
| `tag <name>` | List docs with tag | ❌ No |
| `related <doc_id>` | Find related documents | ❌ No |

**Related Documents Example:**

```bash
# Find documents related to skills documentation
python .claude/skills/docs-management/scripts/core/find_docs.py related code-claude-com-docs-en-skills

# Limit results
python .claude/skills/docs-management/scripts/core/find_docs.py --limit 5 related code-claude-com-docs-en-skills
```

Related documents are scored by shared tags (3x weight) and shared keywords (2x weight).

### Subsection Extraction (Token-Optimized)

To extract a specific section from a document (60-90% token savings):

**Option 1: Using find_docs.py content command:**

```bash
python scripts/core/find_docs.py content code-claude-com-docs-en-skills --section "Available metadata fields"
```

**Option 2: Using get_subsection_content.py (dedicated script):**

```bash
python scripts/core/get_subsection_content.py code-claude-com-docs-en-skills \
  --section "Available metadata fields"
```

**Discover Available Sections (`--list-sections`):**

```bash
# List all sections in a document
python scripts/core/get_subsection_content.py code-claude-com-docs-en-skills --list-sections

# Output shows hierarchical structure with heading levels
#   # Agent Skills
#     ## Create your first Skill
#     ## How Skills work
#       ### Where Skills live
```

**Fuzzy Section Matching:**

Section names support fuzzy matching - partial or word-overlap matches work:

```bash
# Exact: "Available metadata fields"
# Fuzzy: "metadata fields" -> matches "Available metadata fields"
# Fuzzy: "tool access" -> matches "Restrict tool access with allowed-tools"

python scripts/core/get_subsection_content.py code-claude-com-docs-en-skills   --section "metadata fields"
# Output: Fuzzy match: 'metadata fields' -> 'Available metadata fields'
```

**Note:** The `resolve` command ONLY returns file paths. Use `content` to get actual document content with optional section extraction.

## Configuration System

The docs-management skill uses a unified configuration system with a single source of truth.

**Configuration Files:**

- **`config/defaults.yaml`** - Central configuration file with all default values
- **`config/config_registry.py`** - Canonical configuration system with environment variable support
- **`references/sources.json`** - Documentation sources configuration (required for scraping)

**Path Configuration:**

All paths configured in `config/defaults.yaml` under the `paths` section.

**Environment Variable Overrides:**

All configuration values can be overridden using environment variables: `CLAUDE_DOCS_<SECTION>_<KEY>`

**Full details:** [references/technical-details.md#configuration](references/technical-details.md)

## Dependencies & Environment

**Required:** `pyyaml`, `requests`, `beautifulsoup4`, `markdownify`
**Optional (recommended):** `spacy`, `yake` (for enhanced keyword extraction)

**Quick setup:**

```bash
python .claude/skills/docs-management/scripts/setup/setup_dependencies.py --install-required
```

**Auto-installation:** The `extract-keywords` command automatically installs optional dependencies if missing.

**Full details:** [references/technical-details.md#dependencies](references/technical-details.md)

## Core Capabilities

### 1. Scraping Documentation

Fetch documentation from official sources and store in canonical storage. Features: sitemap/docs map parsing, HTML→Markdown conversion, direct .md URL fetching (30-40% token savings), automatic metadata tracking, domain-based folder organization.

**Guide:** [references/capabilities/scraping-guide.md](references/capabilities/scraping-guide.md)

### 2. Extracting Subsections (Internal Use)

Extract specific markdown sections for internal skill operations. Features: ATX-style heading structure parsing, section boundaries detection, provenance frontmatter, token economics (60-90% savings typical).

**Guide:** [references/capabilities/extraction-guide.md](references/capabilities/extraction-guide.md)

### 3. Change Detection

Detect new and removed documentation pages from sitemaps, and detect content changes via hash comparison. Features: new/removed page detection, content hash comparison, automatic stale marking, change reporting and audit logs.

**Guide:** [references/capabilities/change-detection-guide.md](references/capabilities/change-detection-guide.md)

### 4. Finding and Resolving Documentation

Discover and resolve documentation references using doc_id, keywords, or natural language queries. Features: doc_id resolution, keyword-based search, natural language query processing, subsection discovery and extraction, category and tag filtering, alias resolution.

### 5. Index Management and Maintenance

Maintain index metadata, keywords, tags, and rebuild index from filesystem. Scripts: `manage_index.py`, `rebuild_index.py`, `generate_report.py`, `verify_index.py`.

### 6. Age-Based Cleanup

Remove documentation that has aged out based on `published_at` dates. Anthropic sources (engineering, news, research) have a `max_age_days` threshold configured in `references/sources.json`. Articles older than this threshold are skipped during scraping; this cleanup removes any previously-scraped articles that have since aged out.

```bash
# Clean up aged-out Anthropic articles (dry-run by default)
# Reads max_age_days from sources.json automatically
python scripts/maintenance/cleanup_old_anthropic_docs.py

# Execute cleanup (actually delete files)
python scripts/maintenance/cleanup_old_anthropic_docs.py --execute

# Override with custom age threshold if needed
python scripts/maintenance/cleanup_old_anthropic_docs.py --max-age 90 --execute
```

This should be run after scraping and validation to ensure the canonical directory stays clean.

## Workflows

Common maintenance and operational workflows for documentation management:

- **Adding New Documentation Source** - Onboarding new docs from sitemaps or docs maps
- **Scraping Multiple Sources** - Validation checkpoints to prevent wasted time/tokens
- **Token-Optimized Subsection Retrieval** - Workflow for extracting subsections instead of full documents

**Detailed Workflows:** [references/workflows.md](references/workflows.md)

## Metadata & Keyword Audit Workflows

**Lightweight audit:**

```bash
py -3.13 .claude/skills/docs-management/scripts/validation/validate_index_vs_docs.py --summary-only
```

**Tag configuration audit:**

```bash
py -3.13 .claude/skills/docs-management/scripts/validation/audit_tag_config.py --summary-only
```

**Full details:** [references/workflows.md#metadata--keyword-audit](references/workflows.md)

## Platform-Specific Requirements

### Windows Users

**MUST use PowerShell (recommended) or prefix Git Bash commands with `MSYS_NO_PATHCONV=1`**

Git Bash on Windows converts Unix paths to Windows paths, breaking filter patterns.

**See:** [Troubleshooting Guide](references/troubleshooting.md#git-bash-path-conversion)

## Troubleshooting

### spaCy Installation Issues

**Problem:** spaCy installation fails with Python 3.14+.

**Solution:** The script automatically detects and uses Python 3.13 if available. No manual intervention needed!

**If Python 3.13 not available:** Install Python 3.13:

- Windows: `winget install --id Python.Python.3.13 -e --source winget`
- macOS: `brew install python@3.13`
- Linux: `sudo apt install python3.13`

**Full troubleshooting:** [references/troubleshooting.md](references/troubleshooting.md)

## Public API

The docs-management skill provides a clean public API for external tools:

```python
from official_docs_api import (
    find_document,
    resolve_doc_id,
    get_docs_by_tag,
    get_docs_by_category,
    search_by_keywords,
    detect_drift,
    cleanup_drift,
    refresh_index
)
```

**Full API documentation:** See Public API section in original SKILL.md

## Plugin Maintenance

For plugin-specific maintenance workflows (versioning, publishing updates, changelog):

**See:** [references/plugin-maintenance.md](references/plugin-maintenance.md)

Quick reference:

- **Update workflow**: Scrape → Validate → Review → Commit → Version bump → Push
- **Version bumps**: Patch for doc refresh, Minor for new sources/features, Major for breaking changes
- **Testing**: Run `manage_index.py verify` and test search before pushing

## Development Mode

When developing this plugin locally, you may want changes to go to your dev repo instead of the installed plugin location. This skill supports explicit dev/prod mode separation via environment variable.

### How It Works

By default, scripts write to wherever the plugin is installed (typically `~/.claude/plugins/marketplaces/...`). When `OFFICIAL_DOCS_DEV_ROOT` is set to a valid skill directory, all paths resolve to that location instead.

### Enabling Dev Mode

**One-time setup:**

```bash
# Navigate to your dev repo skill directory
cd /path/to/your/claude-code-plugins/plugins/claude-ecosystem/skills/docs-management

# Generate shell commands for your shell
python scripts/setup/enable_dev_mode.py
```

**PowerShell:**

```powershell
$env:OFFICIAL_DOCS_DEV_ROOT = "D:\repos\gh\claude-code-plugins\plugins\claude-ecosystem\skills\docs-management"
```

**Bash/Zsh:**

```bash
export OFFICIAL_DOCS_DEV_ROOT="/path/to/claude-code-plugins/plugins/claude-ecosystem/skills/docs-management"
```

### Verifying Mode

When you run any major script (scrape, refresh, rebuild), a mode banner will display:

**Dev mode:**

```text
[DEV MODE] Using development skill directory:
  D:\repos\gh\claude-code-plugins\plugins\claude-ecosystem\skills\docs-management
  Set via: OFFICIAL_DOCS_DEV_ROOT
Canonical dir: D:\...\canonical
```

**Prod mode:**

```text
[PROD MODE] Using installed skill directory
  (Set OFFICIAL_DOCS_DEV_ROOT to enable dev mode)
```

### Development Workflow

1. Set `OFFICIAL_DOCS_DEV_ROOT` in your terminal
2. Run scripts - output goes to dev repo
3. Track changes: `git diff canonical/`
4. Commit and push when ready

### Disabling Dev Mode

**PowerShell:**

```powershell
Remove-Item Env:OFFICIAL_DOCS_DEV_ROOT
```

**Bash/Zsh:**

```bash
unset OFFICIAL_DOCS_DEV_ROOT
```

## Related Documentation

- **index.yaml** (in canonical storage) - Complete registry of docs and extracts
- **[references/parallelization-strategy.md](references/parallelization-strategy.md)** - Parallelization decision trees
- **[references/plugin-maintenance.md](references/plugin-maintenance.md)** - Plugin update and publishing workflows
- **[DEPENDENCIES.md](DEPENDENCIES.md)** - Script dependency graph and execution order

## Version History

- v1.19.0 (2025-11-25): Determinism fixes and observability enhancements
- v1.18.0 (2025-11-18): CRITICAL FIX: Enforce foreground execution pattern
- v1.17.1 (2025-11-18): Fix Task tool invocation syntax
- v1.17.0 (2025-11-18): Critical workflow execution guidance + error reporting
- v1.16.0 (2025-11-17): Comprehensive search quality audit & fixes (100% pass rate)
- v1.15.0 (2025-11-17): Critical bug fix + domain prioritization
- v1.14.0 (2025-11-17): Comprehensive skill audit & validation (A+ grade)

Full history: See original SKILL.md

## Last Updated

**Date:** 2025-12-29
**Model:** claude-opus-4-5-20251101

**Audit Result:** ✅ **EXCEPTIONAL PASS (A+)** - Score: 50/50 (100%)

**Audit Type:** Type B (Meta-Skill - Delegation Pattern Compliance)

**Status:** Production-ready. Serves as the canonical reference implementation for Type B meta-skills.
