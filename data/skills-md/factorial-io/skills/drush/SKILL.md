---
name: drush
description: Use when working with Drush CLI for Drupal site management - running cache rebuilds, config imports/exports, database queries, PHP evaluation, module management, user operations, or troubleshooting Drush commands that no longer exist
---

# Drush CLI Reference

Command-line interface for Drupal site management. Drush runs in the Drupal bootstrap context, giving full access to the Drupal API.

## Command Structure

**All commands follow: `drush <command> [arguments] [--options]`**

Most commands have short aliases. Use `drush list` to see all available commands, `drush <command> --help` for details.

**In DDEV:** Prefix with `ddev` (e.g., `ddev drush cr`).

## Quick Reference

| Task | Command | Alias |
|------|---------|-------|
| Cache rebuild | `drush cache:rebuild` | `drush cr` |
| Config export | `drush config:export` | `drush cex` |
| Config import | `drush config:import` | `drush cim` |
| Config get | `drush config:get <name>` | `drush cget <name>` |
| Config set | `drush config:set <name> <key> <value>` | `drush cset <name> <key> <value>` |
| Database update | `drush updatedb` | `drush updb` |
| Module install | `drush pm:install <module>` | `drush en <module>` |
| Module uninstall | `drush pm:uninstall <module>` | `drush pmu <module>` |
| List modules | `drush pm:list` | `drush pml` |
| User login link | `drush user:login` | `drush uli` |
| User info | `drush user:information <name>` | |
| Watchdog logs | `drush watchdog:show` | `drush ws` (requires dblog module) |
| Status overview | `drush status` | `drush st` |
| Run cron | `drush cron` | |
| State get | `drush state:get <key>` | `drush sget <key>` |
| State set | `drush state:set <key> <value>` | `drush sset <key> <value>` |
| Deploy (updb+cim+cr) | `drush deploy` | |
| Code generation | `drush generate` | `drush gen` |
| Site requirements | `drush core:requirements` | `drush rq` |
| Watchdog tail | `drush watchdog:tail` | `drush wt` (requires dblog module) |
| Queue list | `drush queue:list` | |
| Queue run | `drush queue:run <name>` | |

## Running PHP Code

Drush can evaluate arbitrary PHP within full Drupal bootstrap context.

### Inline PHP with eval

```bash
# Simple expression
drush php:eval "echo \Drupal::VERSION;"

# Load and inspect an entity
drush php:eval "\$node = \Drupal\node\Entity\Node::load(1); echo \$node->getTitle();"

# Query entities
drush php:eval "\$ids = \Drupal::entityTypeManager()->getStorage('node')->getQuery()->accessCheck(FALSE)->condition('type', 'article')->range(0, 5)->execute(); print_r(\$ids);"

# Access a service
drush php:eval "echo \Drupal::service('extension.list.module')->getPath('node');"

# Get current user
drush php:eval "echo \Drupal::currentUser()->getAccountName();"
```

**Shell escaping:** Use single quotes around the PHP string in fish/zsh to avoid `$` expansion, or escape `\$` in double quotes.

### Interactive PHP shell

```bash
# Opens interactive REPL with Drupal bootstrapped
drush php:cli
```

Useful for exploring APIs interactively. Tab completion available for classes/functions.

### Running PHP scripts

```bash
# Execute a PHP file with full Drupal bootstrap
drush php:script path/to/script.php

# Pass arguments (available as $extra in the script)
drush php:script path/to/script.php -- arg1 arg2
```

## Executing SQL Commands

### Direct SQL queries

```bash
# Run a SQL query directly
drush sql:query "SELECT nid, title FROM node_field_data LIMIT 10"

# Count content by type
drush sql:query "SELECT type, COUNT(*) as count FROM node_field_data GROUP BY type"

# Check a specific table (MySQL-specific syntax)
drush sql:query "DESCRIBE users_field_data"

# Show tables matching a pattern (MySQL-specific)
drush sql:query "SHOW TABLES LIKE '%node%'"
```

**Note:** `DESCRIBE` and `SHOW TABLES` are MySQL-specific. For PostgreSQL use `\d table_name` in `sql:cli`.

### Database shell and dumps

```bash
# Open interactive database client (mysql/psql)
drush sql:cli

# Create database dump
drush sql:dump > dump.sql
drush sql:dump --result-file=/tmp/dump.sql
drush sql:dump --gzip --result-file=/tmp/dump.sql  # produces dump.sql.gz

# Import SQL file
drush sql:cli < dump.sql

# Show database connection info
drush sql:conf

# Sanitize user data (emails, passwords) for safe copies
drush sql:sanitize

# Drop all tables (use with caution)
drush sql:drop
```

## Retrieving Configuration

### Get configuration values

```bash
# Get entire config object (YAML output)
drush config:get system.site
drush cget system.site

# Get a specific key
drush config:get system.site name
drush cget system.site page.front

# List all config names (no config:list command in Drush 13+)
drush php:eval 'foreach (\Drupal::service("config.storage")->listAll("system") as $name) echo "$name\n";'

# Get active vs sync diff
drush config:status
```

### Edit and set configuration

```bash
# Set a single value
drush config:set system.site name "My Site"
drush cset system.site name "My Site"

# Set nested value
drush config:set system.site page.front "/node"

# Edit full config object in editor
drush config:edit system.site

# Delete a config object
drush config:delete <config-name>
```

### Config export/import workflow

```bash
# Export active config to sync directory
drush cex

# Show pending changes (what would be imported)
drush config:status

# Import config from sync directory
drush cim

# Import partial (only imports items in sync dir, does not delete active-only config)
drush cim --partial

# Import from a non-default directory
drush cim --source=/path/to/config

# Export single config item to stdout
drush config:get system.site --format=yaml
```

## Module Management

```bash
# List all modules with status
drush pml
drush pml --status=enabled
drush pml --type=module --status="not installed"

# Install module(s)
drush en module_name
drush en module_one module_two

# Uninstall module(s)
drush pmu module_name

# Check if module is enabled
drush pml --filter=module_name
```

## User Management

```bash
# Generate one-time login link
drush uli
drush uli --uid=1
drush uli admin

# Create user
drush user:create username --mail="user@example.com" --password="pass"

# Add role to user
drush user:role:add editor admin

# Remove role
drush user:role:remove editor admin

# Block/unblock user
drush user:block username
drush user:unblock username

# Reset password
drush user:password admin "newpassword"
```

## Roles and Permissions

### Inspecting roles

```bash
# List all roles with their permissions
drush role:list
drush role:list --format=table
drush role:list --format=json

# Get permissions for a specific role via config
drush cget user.role.editor

# Check a user's roles
drush user:information admin --format=json
```

### Checking permissions

```bash
# List all available permissions (grep to search)
drush php:eval 'echo implode("\n", array_keys(\Drupal::service("user.permissions")->getPermissions()));'

# Search for specific permissions
drush php:eval 'echo implode("\n", array_keys(\Drupal::service("user.permissions")->getPermissions()));' | grep administer
```

### Managing permissions

```bash
# Grant permission to a role
drush role:perm:add anonymous 'access content'

# Grant multiple permissions
drush role:perm:add editor 'access content,administer nodes'

# Remove permission from a role
drush role:perm:remove anonymous 'access content'

# Create / delete a role
drush role:create editor Editor
drush role:delete editor
```

## Code Generation

Drush includes scaffolding for modules, plugins, forms, entities, and more via `drush generate` (powered by [drupal-code-generator](https://github.com/Chi-teck/drupal-code-generator)).

```bash
# Interactive: pick a generator from the list
drush generate

# Generate a specific component
drush generate module
drush generate controller
drush generate form:config
drush generate plugin:block
drush generate entity:content
drush generate hook

# Preview what would be generated (no files written)
drush generate controller --dry-run

# Pre-fill answers to skip interactive prompts
drush generate controller --answer=Example --answer=example

# See all available generators
drush generate --dry-run
```

Common generators: `module`, `controller`, `field`, `hook`, `form:simple`, `form:config`, `form:confirm`, `plugin:block`, `plugin:action`, `entity:content`, `entity:configuration`, `service-provider`, `drush:command`.

Run `drush generate <name> --help` for details on a specific generator.

## Useful Options

| Option | Description |
|--------|-------------|
| `--format=json` | JSON output (useful for scripting/parsing) |
| `--format=yaml` | YAML output |
| `--format=table` | Table output (default for many commands) |
| `-y` | Auto-confirm prompts |
| `-v` | Verbose output |
| `--debug` | Debug output |
| `--uri=http://example.com` | Set base URI for commands |
| `--root=/path/to/drupal` | Set Drupal root |

## Deprecated and Removed Commands

Commands that NO LONGER EXIST in modern Drush (12+). Do NOT suggest these:

| Removed Command | What to Use Instead |
|-----------------|---------------------|
| `drush entity-updates` / `drush entup` | Removed entirely. Entity schema updates are handled by `drush updatedb` (`drush updb`). If hook_update_N does not cover your change, write a custom update hook. |
| `drush pm-download` / `drush dl` | Use `composer require drupal/<module>` |
| `drush pm-update` / `drush up` | Use `composer update` then `drush updb` |
| `drush pm-enable` (old syntax) | Use `drush pm:install` / `drush en` |
| `drush pm-disable` / `drush dis` | Use `drush pm:uninstall` / `drush pmu` (no "disable" concept in modern Drupal) |
| `drush features-*` | Features module commands; use config management instead |
| `drush sql-sync` | Still exists as `sql:sync` but requires site aliases. Without aliases, use `drush sql:dump` + transfer, or tools like phabalicious `copy-from` |
| `drush core-rsync` | Still exists as `core:rsync` but requires site aliases. Without aliases, use `rsync` directly or deployment tools |
| `drush registry-rebuild` / `drush rr` | Removed. Use `drush cr` instead |
| `drush variable-get/set` | Variables replaced by State API (`drush sget`/`drush sset`) or Config API (`drush cget`/`drush cset`) |

**General rule:** If a command uses a hyphen (e.g., `entity-updates`), it is likely old Drush syntax. Modern Drush uses colons (e.g., `cache:rebuild`).

## Common Mistakes

| Wrong | Right | Why |
|-------|-------|-----|
| `drush entity-updates` | `drush updb` | `entity-updates` removed in Drush 11+ |
| `drush dl module` | `composer require drupal/module` | Package management via Composer now |
| `drush up` | `composer update && drush updb` | Updates via Composer, then run DB updates |
| `drush dis module` | `drush pmu module` | No disable concept; uninstall instead |
| `drush cim` without `drush cr` after issues | `drush cr && drush cim` | Cache rebuild can resolve import errors |
| `drush variable-get x` | `drush sget x` or `drush cget x` | Variables removed; use State or Config API |
| Running `drush cim` before `drush updb` | `drush updb && drush cim` or `drush deploy` | Update hooks may add schemas needed by config import |
| Manual `drush updb && drush cim && drush cr` | `drush deploy` | `deploy` handles correct order and error handling |
| `drush cim`/`drush updb` in scripts without `-y` | Add `-y` flag | These commands prompt for confirmation and hang without it |
| Forgetting `accessCheck(FALSE)` in entity queries via `php:eval` | Always add `->accessCheck(FALSE)` | Required since Drupal 9.2, throws deprecation without it |
