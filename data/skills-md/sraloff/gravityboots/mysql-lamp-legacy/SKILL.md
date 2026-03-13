---
name: mysql-lamp-legacy
description: Managing legacy MySQL/MariaDB schemas in LAMP stacks.
---

# MySQL / MariaDB (LAMP Legacy)

## When to use this skill
- Working on legacy LAMP (Linux, Apache, MySQL, PHP) projects.
- Maintaining WordPress, Drupal, or older custom PHP apps.
- Dealing with specific MySQL quirks (backticks, engine types).

## 1. Schema Management
- **Engine**: Ensure `InnoDB` is used (not MyISAM).
- **Encoding**: Convert/Ensure `utf8mb4` (collation `utf8mb4_unicode_ci` or `utf8mb4_0900_ai_ci`).
- **Dates**: Beware of `0000-00-00` dates; enable strict mode if possible (`NO_ZERO_DATE`).

## 2. Identifiers
- **Quoting**: Use backticks \` \` for identifiers (tables, columns) if they conflict with keywords.
- **Case Sensitivity**: Remember table names are case-sensitive on Linux but not Windows/macOS. Lowercase conventions prefered.

## 3. Optimization
- **Indexes**: Max key length limits might apply on older versions with `utf8mb4`.
- **Query Cache**: Deprecated/Removed in newer MySQL; do not rely on it.
- **Foreign Keys**: Often missing in legacy apps; add them if `InnoDB` allows, otherwise enforce in app logic (but add a comment `// Logic FK`).
