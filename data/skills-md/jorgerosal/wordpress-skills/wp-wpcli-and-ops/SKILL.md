---
name: wp-wpcli-and-ops
description: WordPress WP-CLI and operations review guidance. Use when reviewing WP-CLI commands, search-replace plans, multisite operations, cron or cache maintenance, deployment scripts, operational runbooks, CLI automation, or when user mentions "WP-CLI", "search-replace", "multisite ops", "wp cron", "wp db", "deployment script", "maintenance task", "CLI command", or "ops review". Helps review command safety, environment targeting, multisite scope, automation reliability, and operational blast radius in WordPress codebases and runbooks.
---

# WordPress WP-CLI and Ops Skill

## Overview

Systematic review guidance for WordPress operational workflows centered on WP-CLI. **Core principle:** operational commands should be explicit about scope, environment, and side effects before they touch data or execute production work. Review covers custom CLI commands, search-replace plans, multisite targeting, cron and cache operations, maintenance scripts, and deployment-time automation.

## When to Use

**Use when:**
- Reviewing custom WP-CLI commands or command classes
- Auditing shell scripts or docs that run `wp` commands
- Planning safe search-replace or migration operations
- Checking multisite or network-wide operational steps
- Reviewing cron, cache, export, import, or maintenance workflows

**Don't use for:**
- General plugin architecture with no operational surface
- Performance tuning without an ops workflow
- Playground-only setup flows (use wp-playground-development)
- Static analysis configuration (use wp-phpstan-review)

## Code Review Workflow

1. **Identify the operational surface**
   - Custom `WP_CLI::add_command()` registrations
   - Project docs with `wp` command examples
   - Deployment scripts, CI jobs, or maintenance scripts
   - Multisite runbooks or migration plans

2. **Check scope and targeting first**
   - Is the command site-specific, network-wide, or environment-dependent?
   - Are `--url`, `--path`, or explicit table targets needed?
   - Does the workflow rely on assumptions about the current install?

3. **Review safety and reversibility**
   - Dry-run support where possible
   - Confirmation or logging for destructive steps
   - Backup/export step before high-risk mutations
   - Clear distinction between inspection and mutation commands

4. **Review command implementation**
   - Input validation and argument handling
   - Reasonable defaults
   - Useful success/error output
   - No hidden writes during read-only commands

5. **Classify findings**
   - **CRITICAL:** destructive operation without safeguards, wrong multisite scope, production-hostile search-replace, unvalidated CLI input causing data loss
   - **WARNING:** ambiguous environment targeting, brittle shell examples, missing dry run, weak logging, long-running tasks without chunking
   - **INFO:** could document aliases, improve command UX, or separate read vs write commands

## File-Type Specific Checks

### Custom WP-CLI Commands

- CRITICAL: Write commands with no argument validation or capability/context checks
- WARNING: Command names or synopsis do not communicate side effects
- WARNING: Command mixes read-only inspection with mutation
- INFO: Could return structured output or clearer status messages

### Search-Replace and DB Operations

- CRITICAL: `wp search-replace` examples without `--dry-run` or scope limits
- CRITICAL: Network-wide replace with no explicit `--network` review or table targeting
- WARNING: No `--skip-columns=guid` when replacing URLs
- WARNING: Regex search-replace used casually without performance warning

### Multisite Ops

- CRITICAL: Commands assume current site while touching network-wide state
- WARNING: Missing `--url` for site-specific tasks in multisite
- WARNING: Site creation/deletion workflows without rollback notes
- INFO: Could document `wp site` / `wp super-admin` implications more clearly

### Automation and Maintenance Scripts

- WARNING: Uses `wp eval`/`wp eval-file` where a custom command would be safer
- WARNING: Long maintenance job with no batching or progress output
- INFO: Could split inspection, export, and mutation into separate steps

## Search Patterns for Quick Detection (OPS-21)

Use these `rg` commands to locate WP-CLI and ops workflows fast.

### Command Discovery

```bash
rg -n "WP_CLI::add_command|class .* extends WP_CLI_Command" . -g '*.php'
rg -n "\bwp [a-z0-9:-]+" . -g '*.{md,sh,yml,yaml,json}'
```

### High-Risk Mutations

```bash
rg -n "wp search-replace|wp db reset|wp db drop|wp site delete|wp plugin deactivate" . -g '*.{md,sh,yml,yaml}'
rg -n "wp eval|wp eval-file" . -g '*.{md,sh,yml,yaml}'
```

### Multisite and Scheduling

```bash
rg -n "wp site|wp super-admin|--network|--url=" . -g '*.{md,sh,php,yml,yaml}'
rg -n "wp cron|wp cache|wp transient" . -g '*.{md,sh,php,yml,yaml}'
```

## Reference Files

- `references/command-patterns.md` - Custom command design, argument handling, and operational UX
- `references/multisite-and-search-replace.md` - Multisite scope, `wp site`, and safe `wp search-replace` usage
- `references/automation-and-safety.md` - Deployment scripts, maintenance jobs, batching, and rollback thinking
- `references/sample-wp-cli-command.php` - Sample custom command with validation, dry run, and batching
- `references/sample-maintenance-runbook.md` - Sample runbook with inspect, dry run, execute, and verify stages

## Output Format (OPS-23)

For each finding include:

1. Severity: `CRITICAL`, `WARNING`, or `INFO`
2. File and line number
3. Operational risk summary
4. Why it matters for WP-CLI or runtime operations
5. Recommended safer pattern

If no issues are found, say so clearly and mention any residual operational gaps such as missing dry runs, weak logging, or limited rollback documentation.
