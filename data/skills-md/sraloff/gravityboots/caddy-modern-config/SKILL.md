---
name: caddy-modern-config
description: Caddyfile configuration, auto-HTTPS, and FastCGI.
---

# Caddy Modern Config

## When to use this skill
- Configuring Caddy as a web server or reverse proxy.
- Setting up local HTTPS.
- Deploying PHP/Python apps with Caddy.

## 1. Caddyfile Basics
- **Syntax**: `domain { directives }`.
- **Auto-HTTPS**: Enabled by default for any host that looks like a domain.

## 2. Reverse Proxy
- **Python/Node**:
  ```caddy
  example.com {
      reverse_proxy localhost:3000
  }
  ```

## 3. PHP (FastCGI)
- **Directives**: Use `php_fastcgi` preset.
  ```caddy
  example.com {
      root * /var/www/site/public
      php_fastcgi unix//run/php/php8.3-fpm.sock
      file_server
  }
  ```

## 4. Security
- **Headers**: Add basic security headers easily.
  ```caddy
  header {
      Strict-Transport-Security "max-age=31536000;"
      X-Content-Type-Options "nosniff"
  }
  ```
