---
name: apache-lamp-config
description: Configuration for Virtual Hosts, .htaccess, and PHP-FPM in LAMP stacks.
---

# Apache & LAMP Config

## When to use this skill
- Configuring local development environments (MAMP, XAMPP, Docker + Apache).
- Managing `.htaccess` files.
- Troubleshooting rewrite rules.

## 1. Virtual Hosts
- **Structure**: One file per site in `sites-available`, symlinked to `sites-enabled`.
- **DocumentRoot**: Point to the `public/` directory, not the project root (security).
- **Directory**: Allow overrides:
  ```apache
  <Directory "/var/www/site/public">
      AllowOverride All
      Require all granted
  </Directory>
  ```

## 2. .htaccess Best Practices
- **Rewrites**: Standard pattern for front controllers (Laravel/Symfony):
  ```apache
  RewriteEngine On
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteRule ^ index.php [L]
  ```
- **HTTPS**: Force HTTPS if not handled by a reverse proxy.

## 3. PHP-FPM
- **Timeouts**: Increase `max_execution_time` and `memory_limit` only for specific heavy jobs, not globally.
- **Opcache**: Enable Opcache in production for performance.
