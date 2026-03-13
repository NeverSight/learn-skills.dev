---
name: drupal-tooling
description: Drupal development tooling skill for DDEV local environments and Drush command-line operations (Drupal 8-11+). Use when working with Docker-based development environments, Drush commands, deployment workflows, or site management tasks.
---

# Drupal Development Tooling

## Overview

Enable expert-level Drupal development tooling capabilities with comprehensive guidance for DDEV Docker-based local development environments and Drush command-line operations for Drupal 8, 9, 10, and 11+.

## When to Use This Skill

Invoke this skill when working with:
- **DDEV operations**: Starting, managing, or configuring local development environments
- **Drush commands**: Site management, configuration, cache operations
- **Database management**: Import/export, snapshots, migrations
- **Deployment workflows**: Configuration sync, database updates
- **Development setup**: Project initialization, environment configuration
- **Troubleshooting**: Debugging environment or command-line issues

## Core Capabilities

### 1. DDEV Local Development

Manage Docker-based local Drupal environments efficiently:

**Project initialization:**
```bash
# Initialize new Drupal project
ddev config --project-type=drupal10 --docroot=web --create-docroot

# Start containers
ddev start

# Install Drupal via Composer
ddev composer create drupal/recommended-project

# Install Drupal site
ddev drush site:install standard --account-name=admin --account-pass=admin
```

**Daily operations:**
```bash
# Start/stop project
ddev start
ddev stop
ddev restart

# SSH into container
ddev ssh

# Launch site in browser
ddev launch

# View logs
ddev logs
ddev logs -f  # Follow logs
```

**Database operations:**
```bash
# Import database
ddev import-db --src=database.sql.gz

# Export database
ddev export-db --file=backup.sql.gz --gzip

# Create snapshot
ddev snapshot

# Restore snapshot
ddev snapshot restore

# Access MySQL CLI
ddev mysql
```

**Reference documentation:**
- `references/ddev.md` - Complete DDEV reference

### 2. Drush Command-Line Management

Execute site management tasks efficiently:

**Cache management:**
```bash
# Rebuild cache (most common)
ddev drush cr

# Clear specific cache
ddev drush cache:clear css-js
ddev drush cache:clear render
```

**Configuration management:**
```bash
# Export configuration
ddev drush config:export
ddev drush cex

# Import configuration
ddev drush config:import
ddev drush cim

# View configuration
ddev drush config:get system.site
ddev drush cget system.site

# Set configuration
ddev drush config:set system.site name "My Site"
ddev drush cset system.site name "My Site"
```

**Module management:**
```bash
# Enable module
ddev drush pm:enable mymodule -y
ddev drush en mymodule -y

# Uninstall module
ddev drush pm:uninstall mymodule -y
ddev drush pmu mymodule -y

# List modules
ddev drush pm:list
ddev drush pml

# Download module
ddev drush pm:download webform
```

**Database updates:**
```bash
# Run pending database updates
ddev drush updatedb -y
ddev drush updb -y
```

**User management:**
```bash
# One-time login URL
ddev drush user:login
ddev drush uli

# Login as specific user
ddev drush uli admin

# Create user
ddev drush user:create newuser --mail="user@example.com" --password="pass"

# Change password
ddev drush user:password admin "newpassword"
```

**Reference documentation:**
- `references/drush.md` - Complete Drush reference

### 3. Development Workflows

Common development and deployment workflows:

**Standard deployment:**
```bash
# Run database updates
ddev drush updb -y

# Import configuration
ddev drush cim -y

# Clear cache
ddev drush cr

# One-liner version
ddev drush updb -y && ddev drush cim -y && ddev drush cr
```

**Fresh site setup:**
```bash
# Clone repository
git clone <repo> myproject
cd myproject

# Start DDEV
ddev start

# Install dependencies
ddev composer install

# Import database and files
ddev import-db --src=database.sql.gz
ddev import-files --src=files.tar.gz

# Clear cache
ddev drush cr

# Launch site
ddev launch
```

**Theme/module development:**
```bash
# Start work
ddev start

# Clear cache frequently
ddev drush cr

# Watch for changes (if using build tools)
ddev exec npm run watch

# View logs
ddev drush watchdog:tail
```

### 4. Code Generation

Use Drush generators to scaffold code:

```bash
# Generate module
ddev drush generate module

# Generate controller
ddev drush generate controller

# Generate form
ddev drush generate form

# Generate plugin block
ddev drush generate plugin:block

# Generate service
ddev drush generate service

# Generate theme
ddev drush generate theme

# Generate hook
ddev drush generate hook

# List all generators
ddev drush generate --help
```

### 5. Debugging & Troubleshooting

Debug and monitor your Drupal site:

**Enable Xdebug:**
```bash
# Enable Xdebug
ddev xdebug on

# Disable Xdebug (improves performance)
ddev xdebug off

# Check status
ddev xdebug status
```

**View logs:**
```bash
# Recent watchdog messages
ddev drush watchdog:show

# Follow watchdog logs
ddev drush watchdog:tail

# Container logs
ddev logs -s web
ddev logs -s db
```

**Project information:**
```bash
# Show project details
ddev describe

# Drupal status
ddev drush status
ddev drush st

# List all DDEV projects
ddev list
```

## Best Practices

### DDEV Best Practices
1. **Run tools through DDEV**: Always use `ddev drush`, `ddev composer`, `ddev npm`
2. **Snapshots**: Create before risky operations
3. **Performance**: Enable Mutagen (Mac) or NFS for better file sync
4. **Xdebug**: Only enable when debugging
5. **Version control**: Commit `.ddev/config.yaml` to share configuration
6. **Clean shutdown**: Use `ddev stop` before system shutdown

### Drush Best Practices
1. **Aliases**: Use short aliases (`cr`, `cex`, `cim`, `uli`)
2. **Automation**: Add `-y` flag to skip confirmations
3. **Custom commands**: Create for repetitive tasks
4. **Site aliases**: Configure for multi-environment management
5. **Chaining**: Use `&&` for sequential operations
6. **Error handling**: Check exit codes in scripts

### Deployment Best Practices
1. **Order**: Run updates (`updb`) before config import (`cim`)
2. **Testing**: Test deployment workflow in staging first
3. **Backups**: Always backup before major changes
4. **Rollback plan**: Have a way to revert changes
5. **Monitoring**: Check logs after deployment

## Common Operations

### Initialize DDEV for Existing Project

```bash
cd existing-project

# Configure DDEV
ddev config

# Start containers
ddev start

# Install dependencies
ddev composer install

# Import database (if available)
ddev import-db --src=backup.sql.gz

# Clear cache
ddev drush cr
```

### Pull From Remote Environment

```bash
# Configure Drush alias for remote site
# Then pull database and files
ddev pull @production

# Or pull separately
ddev drush sql:sync @production @self
ddev rsync @production:%files @self:%files
```

### Update Drupal Core

```bash
# Backup first
ddev snapshot

# Update with Composer
ddev composer update drupal/core "drupal/core-*" --with-all-dependencies

# Run database updates
ddev drush updb -y

# Clear cache
ddev drush cr
```

### Enable Development Settings

```bash
# Copy development settings
cp sites/example.settings.local.php sites/default/settings.local.php

# Disable CSS/JS aggregation via Drush
ddev drush config:set system.performance css.preprocess 0 -y
ddev drush config:set system.performance js.preprocess 0 -y

# Enable Twig debugging
# Edit sites/default/services.yml:
# twig.config:
#   debug: true
#   auto_reload: true
#   cache: false

# Clear cache
ddev drush cr
```

## Troubleshooting

### DDEV Issues

**Containers won't start:**
```bash
# Check Docker is running
docker ps

# Restart DDEV
ddev restart

# Power off and restart
ddev poweroff
ddev start

# Clean restart
ddev restart --clean
```

**Port conflicts:**
```bash
# Check what's using ports
ddev describe

# Change ports in .ddev/config.yaml:
# router_http_port: "8080"
# router_https_port: "8443"

# Restart
ddev restart
```

**Permission issues:**
```bash
# Fix file permissions
ddev exec chmod -R 755 web/sites/default/files
ddev exec chown -R www-data:www-data web/sites/default/files
```

### Drush Issues

**Drush not found:**
```bash
# Always run through DDEV
ddev drush status

# Not just: drush status
```

**Configuration sync failures:**
```bash
# Check for overridden configuration
ddev drush config:status

# Force import
ddev drush cim -y --partial

# Check specific config
ddev drush config:get system.site
```

**Database update failures:**
```bash
# Run with verbose output
ddev drush updb -v

# Check specific module updates
ddev drush updatedb:status

# Check logs
ddev drush watchdog:show
```

## Performance Optimization

### DDEV Performance (Mac)

**Enable Mutagen:**
```bash
# In .ddev/config.yaml
ddev config --mutagen-enabled

# Restart
ddev restart
```

**Enable NFS:**
```bash
# In .ddev/config.yaml
ddev config --nfs-mount-enabled

# Restart
ddev restart
```

### Drush Performance

**Disable Xdebug when not debugging:**
```bash
ddev xdebug off
```

**Use specific commands instead of aliases:**
```bash
# Faster (loads less)
ddev drush cache:rebuild

# vs
ddev drush cr
```

## Resources

### Reference Documentation

- **`references/ddev.md`** - Complete DDEV reference
  - Project initialization and configuration
  - Database and file operations
  - Add-ons and services (Redis, Elasticsearch, etc.)
  - Performance optimization
  - Troubleshooting

- **`references/drush.md`** - Complete Drush reference
  - Cache management commands
  - Configuration management
  - Module and theme operations
  - Database operations
  - User management
  - Custom command development

### Searching References

```bash
# Find DDEV command
grep -r "ddev snapshot" references/

# Find Drush command
grep -r "config:import" references/

# Find deployment info
grep -r "deployment" references/
```

## Common Use Cases

### Local Development Setup

1. Clone project: `git clone <repo>`
2. Configure DDEV: `ddev config`
3. Start: `ddev start`
4. Install dependencies: `ddev composer install`
5. Import DB: `ddev import-db --src=db.sql.gz`
6. Clear cache: `ddev drush cr`
7. Launch: `ddev launch`

### Deploying Configuration Changes

1. Export config: `ddev drush cex -y`
2. Commit to git: `git add config/ && git commit`
3. Push: `git push`
4. On server: `drush cim -y && drush cr`

### Debugging Performance Issues

1. Enable Xdebug: `ddev xdebug on`
2. Set breakpoints in IDE
3. Trigger request: `ddev launch`
4. Step through code
5. Disable Xdebug: `ddev xdebug off`

## Version Compatibility

### DDEV Versions
- DDEV v1.21+ recommended
- Supports all Drupal versions (8-11+)
- Update with: `brew upgrade ddev` (Mac) or platform equivalent

### Drush Versions
- Drush 10+ for Drupal 8.4+
- Drush 11+ for Drupal 9.0+
- Drush 12+ for Drupal 10.0+
- Install via Composer (project-specific)

## See Also

- **drupal-frontend** - Theme development and Twig templates
- **drupal-backend** - Module development and APIs
- [DDEV Documentation](https://ddev.readthedocs.io/) - Official DDEV docs
- [Drush Documentation](https://www.drush.org/) - Official Drush docs
- [DDEV Discord](https://discord.gg/hCZFfAMc5k) - Community support
