---
name: ddev-expert
description: DDEV local development expertise. Use when working with DDEV projects, containers, configuration, or troubleshooting DDEV environments.
---

# DDEV Development Expert

You are an expert in DDEV, the Docker-based local development environment for PHP projects.

## Core Concepts

DDEV provides a consistent, containerized local development environment with:
- Pre-configured PHP, web server, database containers
- Automatic HTTPS with mkcert
- Built-in Composer and Node.js support
- Easy multi-project management

**Note:** Drush is NOT included by default - you must `composer require drush/drush` after creating a Drupal project.

## Essential Commands

### Project Management
```bash
ddev start          # Start project containers
ddev stop           # Stop project containers
ddev restart        # Restart containers
ddev poweroff       # Stop all DDEV projects
ddev delete         # Remove project (keeps files)
```

### Executing Commands
```bash
ddev drush <cmd>    # Run Drush commands
ddev composer <cmd> # Run Composer
ddev php <script>   # Run PHP scripts
ddev exec <cmd>     # Run any command in web container
ddev ssh            # SSH into web container
```

### Database
```bash
ddev mysql          # MySQL CLI
ddev export-db      # Export database
ddev import-db      # Import database (--file=dump.sql)
ddev snapshot       # Create database snapshot
ddev restore        # Restore from snapshot
```

### Utilities
```bash
ddev describe       # Show project info and URLs
ddev logs           # View container logs
ddev launch         # Open site in browser
ddev share          # Create public URL (ngrok)
```

## Configuration

### .ddev/config.yaml
```yaml
name: my-project
type: drupal           # Auto-detects Drupal version, or use drupal11/drupal10
docroot: web
php_version: "8.3"     # Use 8.3 for Drupal 11, 8.2 for Drupal 10
webserver_type: nginx-fpm
database:
  type: mariadb
  version: "10.11"

# Additional hostnames
additional_hostnames:
  - api.my-project.ddev.site

# Extra PHP packages
webimage_extra_packages: [php8.3-imagick]
```

### Common Customizations

**Custom services** (.ddev/docker-compose.*.yaml):
```yaml
version: '3.6'
services:
  redis:
    image: redis:7
    container_name: ddev-${DDEV_SITENAME}-redis
    labels:
      com.ddev.site-name: ${DDEV_SITENAME}
    expose:
      - "6379"
```

**PHP overrides** (.ddev/php/my-settings.ini):
```ini
memory_limit = 512M
upload_max_filesize = 64M
post_max_size = 64M
```

**Nginx config** (.ddev/nginx_full/nginx-site.conf):
Custom nginx configuration for special routing needs.

## Drupal-Specific Setup

### New Drupal 11 Project
```bash
mkdir my-drupal && cd my-drupal
ddev config --project-type=drupal --docroot=web --php-version=8.3
ddev start
ddev composer create-project drupal/recommended-project:^11
ddev composer require drush/drush
ddev drush site:install --account-name=admin --account-pass=admin -y
ddev launch
```

**Important notes:**
- `ddev composer create-project` requires a clean directory - move any existing files (like `.claude/`) out first, then move them back after
- Drush is NOT included in Drupal 11's recommended-project - always install it separately
- Use `--project-type=drupal` (auto-detects version) or explicitly `drupal11`

### New Drupal 10 Project
```bash
mkdir my-drupal && cd my-drupal
ddev config --project-type=drupal --docroot=web --php-version=8.2
ddev start
ddev composer create-project drupal/recommended-project:^10
ddev composer require drush/drush
ddev drush site:install --account-name=admin --account-pass=admin -y
ddev launch
```

### Existing Drupal Project
```bash
cd existing-project
ddev config --project-type=drupal --docroot=web
ddev start
ddev composer install
ddev import-db --file=database.sql.gz
ddev drush cr
```

## Troubleshooting

### Common Issues

**`ddev composer create-project` fails with "not allowed to be present":**
```bash
# This happens when extra directories exist (like .claude/, .git/, etc.)
# Solution: Move them out temporarily
mv .claude /tmp/claude-backup
mv .git /tmp/git-backup
ddev composer create-project drupal/recommended-project:^11
mv /tmp/claude-backup .claude
mv /tmp/git-backup .git
```

**Port conflicts:**
```bash
ddev poweroff
# Check what's using ports 80/443
sudo lsof -i :80
```

**Container issues:**
```bash
ddev restart
ddev debug refresh    # Rebuild containers
ddev delete && ddev start  # Nuclear option
```

**Database connection issues:**
- Host: `db` (inside container) or `127.0.0.1:PORT` (outside)
- Check port with `ddev describe`

**Permission issues:**
```bash
ddev exec chown -R $(id -u):$(id -g) .
```

### Useful Debug Commands
```bash
ddev debug capabilities  # Show DDEV capabilities
ddev debug router       # Show router status
ddev logs -f            # Follow logs
ddev exec env           # Show environment variables
```

## Multi-Environment Workflows

### Using ddev pull
Configure providers in .ddev/providers/:
```yaml
# .ddev/providers/platform.yaml
environment_variables:
  project: my-project
  environment: main

db_pull_command:
  command: platform db:dump -e ${environment}
```

Then: `ddev pull platform`

## Xdebug Configuration

### Enable Xdebug
```bash
ddev xdebug on           # Enable step debugging
ddev xdebug off          # Disable (faster performance)
ddev xdebug status       # Check current state
```

### IDE Configuration

**VS Code** (with PHP Debug extension):
```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Listen for Xdebug",
      "type": "php",
      "request": "launch",
      "port": 9003,
      "pathMappings": {
        "/var/www/html": "${workspaceFolder}"
      }
    }
  ]
}
```

**PHPStorm**:
1. Settings → PHP → Servers
2. Add server: name matches DDEV project name
3. Host: `<project>.ddev.site`, Port: 443, HTTPS
4. Path mappings: project root → `/var/www/html`

### Xdebug Modes
```bash
# .ddev/php/xdebug.ini
[xdebug]
xdebug.mode=debug,develop,coverage
```

Modes: `debug` (step debugging), `develop` (enhanced errors), `coverage` (code coverage), `profile` (profiling)

## Custom Services

### Redis
```yaml
# .ddev/docker-compose.redis.yaml
services:
  redis:
    image: redis:7-alpine
    container_name: ddev-${DDEV_SITENAME}-redis
    labels:
      com.ddev.site-name: ${DDEV_SITENAME}
      com.ddev.approot: $DDEV_APPROOT
    expose:
      - "6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

Drupal settings.php:
```php
$settings['redis.connection']['host'] = 'redis';
$settings['redis.connection']['port'] = 6379;
$settings['cache']['default'] = 'cache.backend.redis';
```

### Solr
```yaml
# .ddev/docker-compose.solr.yaml
services:
  solr:
    image: solr:9
    container_name: ddev-${DDEV_SITENAME}-solr
    labels:
      com.ddev.site-name: ${DDEV_SITENAME}
      com.ddev.approot: $DDEV_APPROOT
    expose:
      - "8983"
    volumes:
      - solr-data:/var/solr
    command: solr-precreate drupal

volumes:
  solr-data:
```

Access Solr: `ddev describe` shows URL, typically `https://<project>.ddev.site:8983`

### Elasticsearch
```yaml
# .ddev/docker-compose.elasticsearch.yaml
services:
  elasticsearch:
    image: elasticsearch:8.11.0
    container_name: ddev-${DDEV_SITENAME}-elasticsearch
    labels:
      com.ddev.site-name: ${DDEV_SITENAME}
      com.ddev.approot: $DDEV_APPROOT
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    expose:
      - "9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

volumes:
  elasticsearch-data:
```

### Mailpit (Email Testing)
DDEV includes Mailpit by default:
```bash
ddev launch -m           # Open Mailpit UI
```
All outgoing mail is captured at `https://<project>.ddev.site:8026`

## Performance Tuning

### Mutagen (macOS/Windows)
Mutagen provides fast file synchronization for better performance:

```bash
# Enable globally
ddev config global --mutagen-enabled

# Or per-project in .ddev/config.yaml
mutagen_enabled: true
```

**When to use Mutagen:**
- macOS with large codebases (vendor, node_modules)
- Windows with WSL2
- Projects with slow file I/O

**Mutagen commands:**
```bash
ddev mutagen status      # Check sync status
ddev mutagen sync        # Force sync
ddev mutagen reset       # Reset if issues
```

### NFS (macOS alternative)
For macOS without Mutagen:
```bash
ddev config global --nfs-mount-enabled
```

### Performance Tips

1. **Exclude unnecessary files** from sync:
   ```yaml
   # .ddev/config.yaml
   upload_dirs:
     - sites/default/files
   ```

2. **Use tmpfs for temp files**:
   ```yaml
   # .ddev/docker-compose.performance.yaml
   services:
     web:
       tmpfs:
         - /tmp
   ```

3. **Increase PHP memory for large operations**:
   ```ini
   # .ddev/php/performance.ini
   memory_limit = 1024M
   ```

## Custom DDEV Commands

Create project-specific commands in `.ddev/commands/`:

```bash
# .ddev/commands/web/refresh
#!/bin/bash

## Description: Full site refresh (db + config + cache)
## Usage: refresh
## Example: ddev refresh

set -e

echo "Importing database..."
drush sql:drop -y
drush sql:cli < /var/www/html/reference.sql

echo "Importing config..."
drush config:import -y

echo "Running updates..."
drush updatedb -y

echo "Clearing cache..."
drush cache:rebuild

echo "Done!"
```

Make executable: `chmod +x .ddev/commands/web/refresh`

Then run: `ddev refresh`

### Command Locations
- `.ddev/commands/web/` - Run in web container
- `.ddev/commands/host/` - Run on host machine
- `.ddev/commands/db/` - Run in database container

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup DDEV
        uses: ddev/github-action-setup-ddev@v1

      - name: Start DDEV
        run: ddev start

      - name: Install dependencies
        run: ddev composer install

      - name: Run tests
        run: ddev exec ./vendor/bin/phpunit
```

### GitLab CI
```yaml
# .gitlab-ci.yml
test:
  image: ddev/ddev-gitpod-base:latest
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2375
  script:
    - ddev start
    - ddev composer install
    - ddev exec ./vendor/bin/phpunit
```

## Best Practices

1. **Commit .ddev folder** (except .ddev/db_snapshots, .ddev/.gitignore handles this)
2. **Use .ddev/config.local.yaml** for personal overrides (gitignored)
3. **Document custom services** in project README
4. **Use snapshots** before risky database operations
5. **Keep DDEV updated**: `ddev self-upgrade`
6. **Use Mutagen on macOS/Windows** for better performance
7. **Create custom commands** for repetitive tasks
8. **Test DDEV config in CI** to catch issues early
