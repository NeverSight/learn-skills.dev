---
name: docker-local
description: Custom Docker Compose local development patterns. Use when working with Docker-based local environments, container configuration, or troubleshooting Docker setups.
---

# Docker Compose Local Development

You are working with custom Docker Compose local development environments (non-DDEV).

## Environment Detection

When working on a project with Docker, first detect the setup:

```bash
# Check for compose files
ls -la docker-compose*.yml compose*.yml 2>/dev/null

# Check for environment files
ls -la .env* 2>/dev/null

# Check for Makefile or scripts
ls -la Makefile docker/ scripts/ 2>/dev/null
```

## Common Commands

### Project Lifecycle
```bash
docker compose up -d              # Start in background
docker compose up -d --build      # Start with rebuild
docker compose down               # Stop and remove containers
docker compose down -v            # Also remove volumes (DATA LOSS!)
docker compose restart            # Restart all services
```

### Running Commands
```bash
# In running container
docker compose exec <service> <command>

# Examples
docker compose exec php composer install
docker compose exec php ./vendor/bin/drush cr
docker compose exec php bash

# In new container (if service not running)
docker compose run --rm php composer install
```

### Debugging
```bash
docker compose ps                 # Show container status
docker compose logs -f            # Follow all logs
docker compose logs -f php        # Follow specific service
docker compose top                # Show processes
docker compose exec php env       # Show environment
```

## Drupal Docker Patterns

### Common Service Names

Projects vary, but common patterns:

| Service Type | Common Names |
|-------------|--------------|
| PHP/Web | `php`, `web`, `app`, `drupal`, `php-fpm` |
| Database | `db`, `mysql`, `mariadb`, `postgres` |
| Cache | `redis`, `memcached` |
| Search | `solr`, `elasticsearch` |

### Running Drush

```bash
# Find the PHP container
docker compose ps

# Run Drush (path may vary)
docker compose exec php drush cr
docker compose exec php ./vendor/bin/drush cr
docker compose exec web vendor/bin/drush cr
```

### Database Operations

```bash
# MySQL/MariaDB
docker compose exec db mysql -u root -p<password> <database>

# Import
docker compose exec -T db mysql -u root -p<password> <database> < dump.sql

# Export
docker compose exec db mysqldump -u root -p<password> <database> > dump.sql

# PostgreSQL
docker compose exec db psql -U <user> <database>
```

## Standard Docker Compose Template

For Drupal projects without DDEV:

```yaml
# docker-compose.yml
services:
  php:
    build:
      context: .
      dockerfile: docker/php/Dockerfile
    volumes:
      - .:/var/www/html:cached
    depends_on:
      - db
    environment:
      - PHP_MEMORY_LIMIT=512M

  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    volumes:
      - .:/var/www/html:ro
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - php

  db:
    image: mariadb:10.11
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: drupal
      MYSQL_USER: drupal
      MYSQL_PASSWORD: drupal
    volumes:
      - db-data:/var/lib/mysql
    ports:
      - "3306:3306"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  db-data:
```

### PHP Dockerfile

```dockerfile
# docker/php/Dockerfile
FROM php:8.2-fpm

RUN apt-get update && apt-get install -y \
    git unzip libpng-dev libjpeg-dev libfreetype6-dev \
    libzip-dev libicu-dev mariadb-client \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo_mysql zip intl opcache bcmath

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html
```

### Nginx Config

```nginx
# docker/nginx/default.conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html/web;
    index index.php;

    location / {
        try_files $uri /index.php$is_args$args;
    }

    location ~ \.php$ {
        fastcgi_pass php:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

## Makefile Wrapper

Simplify commands with a Makefile:

```makefile
# Makefile
.PHONY: up down restart shell drush composer logs

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

shell:
	docker compose exec php bash

drush:
	docker compose exec php ./vendor/bin/drush $(filter-out $@,$(MAKECMDGOALS))

composer:
	docker compose exec php composer $(filter-out $@,$(MAKECMDGOALS))

logs:
	docker compose logs -f

db-import:
	docker compose exec -T db mysql -u root -proot drupal < $(file)

db-export:
	docker compose exec db mysqldump -u root -proot drupal > dump.sql

%:
	@:
```

Usage:
```bash
make up
make drush cr
make composer require drupal/module
make db-import file=backup.sql
```

## Troubleshooting

### Port Conflicts

```bash
# Find what's using a port
sudo lsof -i :80
sudo lsof -i :3306

# Check all Docker ports
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### Container Won't Start

```bash
docker compose logs <service>           # Check logs
docker compose down && docker compose up -d --build  # Rebuild
docker compose down -v && docker compose up -d       # Fresh start (loses data!)
```

### Permission Issues

```bash
# Check container user
docker compose exec php id

# Fix web directory permissions
docker compose exec php chown -R www-data:www-data /var/www/html/web/sites/default/files
```

### Network Issues

```bash
# Containers reach each other by service name
# From PHP container: mysql -h db -u root -proot

# Inspect network
docker network ls
docker network inspect <project>_default
```

### Performance (macOS/Windows)

Slow file sync on macOS/Windows:
- Use `:cached` volume flag
- Exclude `vendor/` and `node_modules/` from sync
- Consider Docker Desktop's VirtioFS (macOS)

```yaml
volumes:
  - .:/var/www/html:cached
  - vendor:/var/www/html/vendor  # Named volume for vendor
```

## Environment Variables

### .env File

Docker Compose auto-loads `.env`:

```env
COMPOSE_PROJECT_NAME=myproject
PHP_VERSION=8.2
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=drupal
```

### Drupal settings.php

```php
// settings.php for Docker
$databases['default']['default'] = [
  'driver' => 'mysql',
  'database' => getenv('MYSQL_DATABASE') ?: 'drupal',
  'username' => getenv('MYSQL_USER') ?: 'drupal',
  'password' => getenv('MYSQL_PASSWORD') ?: 'drupal',
  'host' => getenv('DB_HOST') ?: 'db',
  'port' => getenv('DB_PORT') ?: 3306,
];

// Redis (if using)
if (getenv('REDIS_HOST')) {
  $settings['redis.connection']['host'] = getenv('REDIS_HOST') ?: 'redis';
  $settings['cache']['default'] = 'cache.backend.redis';
}
```

## Best Practices

1. **Version your docker-compose.yml** - Ensure consistent environments
2. **Use .env for secrets** - Never commit passwords
3. **Create a Makefile** - Simplify commands for the team
4. **Document in README** - How to start, stop, access services
5. **Use named volumes** - For database persistence
6. **Health checks** - Ensure services are ready before dependent services start
