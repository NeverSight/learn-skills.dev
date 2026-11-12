---
name: bagisto-admin-theme-development
description: Use when creating or changing a Bagisto admin theme — a theme package, admin layouts, Blade component overrides, or the Vite asset pipeline for the admin panel. Trigger phrases include "admin theme", "admin layout", "admin panel styling", "theme package", "vite", "tailwind", "publish views", "custom layout".
requires: bagisto-coding-standards
license: MIT
---

# Admin Theme Development

## Overview

Admin theme development in Bagisto involves creating custom admin panel themes packaged as Laravel packages. The end result is a self-contained package that can be distributed and maintained independently.

## When to Apply

Activate this skill when:
- Creating custom admin themes as packages
- Building admin theme packages for distribution
- Customizing admin panel styling
- Overriding default admin templates

## Bagisto Admin Theme Architecture

### Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Theme Configuration** | Defines available admin themes | `config/themes.php` |
| **Views Path** | Blade template files | Defined in theme config |
| **Assets Path** | CSS, JS, images | Defined in theme config |
| **Admin Service Provider** | Loads views and components | `packages/Webkul/Admin/src/Providers/AdminServiceProvider.php` |

### Key Configuration Properties

```php
// config/themes.php
'admin-default' => 'default',

'admin' => [
    'default' => [
        'name' => 'Default',
        'assets_path' => 'public/themes/admin/default',
        'views_path' => 'resources/admin-themes/default/views',
        'vite' => [
            'hot_file' => 'admin-default-vite.hot',
            'build_directory' => 'themes/admin/default/build',
            'package_assets_directory' => 'src/Resources/assets',
        ],
    ],
],
```

## Reference files — load only what the current task needs

| File | Load when |
|---|---|
| [creating-a-theme.md](creating-a-theme.md) | Scaffolding the theme package and registering it |
| [assets.md](assets.md) | The Vite pipeline, the build, and the dev-server workflow |
| [layouts.md](layouts.md) | Admin layouts, Blade components, custom layouts |
| [reference.md](reference.md) | Package layout, key files, pitfalls, testing |

**REQUIRED SUB-SKILL:** Use bagisto-change-verification before calling any change done.
