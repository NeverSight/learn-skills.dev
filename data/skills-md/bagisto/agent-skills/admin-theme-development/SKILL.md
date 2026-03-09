---
name: admin-theme-development
description: "Admin theme development in Bagisto. Activates when creating custom admin themes, modifying admin layouts, building admin theme packages, or working with admin panel styling and interface customization."
license: MIT
metadata:
  author: bagisto
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

## Creating Admin Theme Package

### Goal: Complete Self-Contained Package

The end result should be a complete package with:
- All views inside the package
- All assets inside the package
- Service provider for publishing
- Vite configuration for asset compilation

### Step 1: Create Package Structure

```bash
mkdir -p packages/Webkul/CustomAdminTheme/src/{Providers,Resources/views}
```

### Step 2: Copy Complete Admin Assets

Copy all admin assets to your package to have full control:

```bash
# Copy complete admin assets folder
cp -r packages/Webkul/Admin/src/Resources/assets/* packages/Webkul/CustomAdminTheme/src/Resources/assets/

# Copy complete admin views folder
cp -r packages/Webkul/Admin/src/Resources/views/* packages/Webkul/CustomAdminTheme/src/Resources/views/

# Copy admin package.json for dependencies
cp packages/Webkul/Admin/package.json packages/Webkul/CustomAdminTheme/
```

This gives you:
- Complete CSS foundation with Tailwind
- All JavaScript functionality
- Admin components and layouts
- Images, fonts, and static assets
- Complete Blade template structure
- Dependencies for asset compilation

### Step 3: Add Custom Dashboard Page (Boilerplate)

After copying, create a custom dashboard page to show it's a new theme:

**File:** `packages/Webkul/CustomAdminTheme/src/Resources/views/dashboard/index.blade.php`

```blade
<x-admin::layouts>
    <x-slot:title>
        Custom Admin Dashboard
    </x-slot>

    <div class="flex gap-4 justify-between max-sm:flex-wrap">
        <h1 class="py-[11px] text-xl text-gray-800 dark:text-white font-bold">
            Custom Theme Dashboard
        </h1>

        <div class="flex gap-x-2.5 items-center">
            <button class="secondary-button">
                Reset to Defaults
            </button>
            
            <button class="primary-button">
                Save Settings
            </button>
        </div>
    </div>

    {{-- Dashboard Content --}}
    <div class="mt-8 bg-white dark:bg-gray-900 rounded-lg shadow p-6">
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white mb-6">
            Welcome to Custom Admin Theme
        </h1>
        
        <p class="text-lg text-gray-600 dark:text-gray-300 mb-8">
            Your customized Bagisto admin panel!
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <h3 class="text-xl font-semibold text-blue-800 mb-2">
                    Analytics
                </h3>
                <p class="text-blue-600">
                    Enhanced dashboard analytics and reporting
                </p>
            </div>
            
            <div class="bg-green-50 p-4 rounded-lg border border-green-200">
                <h3 class="text-xl font-semibold text-green-800 mb-2">
                    Orders
                </h3>
                <p class="text-green-600">
                    Streamlined order management interface
                </p>
            </div>
            
            <div class="bg-purple-50 p-4 rounded-lg border border-purple-200">
                <h3 class="text-xl font-semibold text-purple-800 mb-2">
                    Customers
                </h3>
                <p class="text-purple-600">
                    Enhanced customer management tools
                </p>
            </div>
        </div>
    </div>
</x-admin::layouts>
```

### Step 4: Create Custom Layout (Optional)

Create your own master layout for complete control:

**File:** `packages/Webkul/CustomAdminTheme/src/Resources/views/layouts/master.blade.php`

```blade
<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? config('app.name') }}</title>
    
    {{-- Load assets manually for custom layouts --}}
    @bagistoVite([
        'src/Resources/assets/css/app.css',
        'src/Resources/assets/js/app.js'
    ])
</head>
<body class="dark:bg-gray-900">
    {{-- Custom sidebar --}}
    @include('custom-admin-theme::layouts.sidebar')
    
    <div class="flex">
        {{-- Main content area --}}
        <main class="flex-1 p-6">
            {{ $slot }}
        </main>
    </div>
</body>
</html>
```

### Step 5: Create Service Provider

**File:** `packages/Webkul/CustomAdminTheme/src/Providers/CustomAdminThemeServiceProvider.php`

```php
<?php

namespace Webkul\CustomAdminTheme\Providers;

use Illuminate\Support\ServiceProvider;

class CustomAdminThemeServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap services.
     */
    public function boot(): void
    {
        // Publish views to resources/admin-themes/custom-admin-theme/views
        $this->publishes([
            __DIR__ . '/../Resources/views' => resource_path('admin-themes/custom-admin-theme/views'),
        ], 'custom-admin-theme-views');
    }
}
```

### Step 6: Configure Autoloading

Update `composer.json`:

```json
"autoload": {
    "psr-4": {
        "Webkul\\CustomAdminTheme\\": "packages/Webkul/CustomAdminTheme/src"
    }
}
```

Run: `composer dump-autoload`

### Step 7: Register Service Provider

Add to `bootstrap/providers.php`:

```php
Webkul\CustomAdminTheme\Providers\CustomAdminThemeServiceProvider::class,
```

### Step 8: Update Theme Configuration

**File:** `config/themes.php`

```php
'admin-default' => 'custom-admin-theme',

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
    'custom-admin-theme' => [
        'name' => 'Custom Admin Theme',
        'assets_path' => 'public/themes/admin/custom-admin-theme',
        'views_path' => 'resources/admin-themes/custom-admin-theme/views',
        'vite' => [
            'hot_file' => 'admin-custom-vite.hot',
            'build_directory' => 'themes/admin/custom-admin/build',
            'package_assets_directory' => 'src/Resources/assets',
        ],
    ],
],
```

### Step 9: Publish Views

```bash
php artisan vendor:publish --provider="Webkul\CustomAdminTheme\Providers\CustomAdminThemeServiceProvider"
```

### Step 10: Clear Cache

```bash
php artisan optimize:clear
```

### Step 11: Build Assets

```bash
# Navigate to package
cd packages/Webkul/CustomAdminTheme

# Install dependencies
npm install

# Build assets for production
npm run build
```

This will compile your admin theme assets and create the build directory. After building, your custom admin theme will be ready to use with the custom dashboard you created.

## Vite-Powered Assets

### Step 1: Create Asset Configuration Files

Create in your package root:

**File:** `package.json`

```json
{
    "name": "custom-admin-theme",
    "private": true,
    "description": "Custom Admin Theme Package for Bagisto",
    "scripts": {
        "dev": "vite",
        "build": "vite build"
    },
    "devDependencies": {
        "autoprefixer": "^10.4.14",
        "axios": "^1.1.2",
        "laravel-vite-plugin": "^0.7.2",
        "postcss": "^8.4.23",
        "tailwindcss": "^3.3.2",
        "vite": "^4.0.0"
    }
}
```

**File:** `vite.config.js`

```javascript
import { defineConfig, loadEnv } from "vite";
import laravel from "laravel-vite-plugin";
import path from "path";

export default defineConfig(({ mode }) => {
    const envDir = "../../../";

    Object.assign(process.env, loadEnv(mode, envDir));

    return {
        build: {
            emptyOutDir: true,
        },
        envDir,
        server: {
            host: process.env.VITE_HOST || "localhost",
            port: process.env.VITE_ADMIN_PORT || 5174,
            cors: true,
        },
        plugins: [
            laravel({
                hotFile: "../../../public/admin-custom-vite.hot",
                publicDirectory: "../../../public",
                buildDirectory: "themes/admin/custom-admin/build",
                input: [
                    "src/Resources/assets/css/app.css",
                    "src/Resources/assets/js/app.js",
                ],
                refresh: true,
            }),
        ],
    };
});
```

**File:** `tailwind.config.js`

```javascript
module.exports = {
    content: [
        "./src/Resources/**/*.blade.php",
        "../../../resources/admin-themes/custom-admin-theme/**/*.blade.php"
    ],
    theme: {
        extend: {
            colors: {
                navyBlue: "#060C3B",
            },
        },
    },
    plugins: [],
};
```

**File:** `postcss.config.js`

```javascript
module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
}
```

### Step 2: Add to Bagisto Vite Config

**File:** `config/bagisto-vite.php`

```php
'admin-custom-theme' => [
    'hot_file' => 'admin-custom-vite.hot',
    'build_directory' => 'themes/admin/custom-admin/build',
    'package_assets_directory' => 'src/Resources/assets',
],
```

### Development Commands

```bash
# Navigate to package
cd packages/Webkul/CustomAdminTheme

# Install dependencies
npm install

# Start dev server with hot reload
npm run dev

# Build for production
npm run build
```

## Development Workflow

### Option A: Symlink (Recommended)

Create symlink for real-time development without republishing:

```bash
# Remove published views
rm -rf resources/admin-themes/custom-admin-theme/views

# Create symlink from package to resources
ln -s $(pwd)/packages/Webkul/CustomAdminTheme/src/Resources/views resources/admin-themes/custom-admin-theme/views
```

### Option B: Direct Package Development

Work directly in package and republish when needed:

```bash
# After making changes
php artisan vendor:publish --provider="Webkul\CustomAdminTheme\Providers\CustomAdminThemeServiceProvider" --force
```

## Admin Layouts

### Using Admin Layout

```blade
<x-admin::layouts>
    <x-slot:title>
        Page Title
    </x-slot>

    {{-- Page Header --}}
    <div class="flex gap-4 justify-between max-sm:flex-wrap">
        <p class="py-[11px] text-xl text-gray-800 dark:text-white font-bold">
            Page Heading
        </p>
        <div class="flex gap-x-2.5 items-center">
            <button class="primary-button">
                Action Button
            </button>
        </div>
    </div>

    {{-- Page content --}}
    <div class="mt-8">
        Content goes here
    </div>
</x-admin::layouts>
```

### Layout Features

The admin layout automatically provides:
- **Sidebar Navigation**: Admin menu with collapsible sections
- **Header**: Top navigation with user menu and notifications
- **Responsive Design**: Mobile-friendly layout
- **Dark Mode**: Built-in dark mode support
- **Breadcrumbs**: Automatic breadcrumb generation

### Admin Layout Best Practices

- Always use the title slot for SEO and user experience
- Follow Bagisto's admin design patterns
- Use provided CSS classes (e.g., `primary-button`, `secondary-button`)
- Keep layout structure clean and semantic

## Admin Blade Components

### Available Components

| Component | Usage | Description |
|-----------|-------|-------------|
| `<x-admin::accordion>` | Collapsible sections | Toggle content visibility |
| `<x-admin::button>` | Action buttons | Loading states supported |
| `<x-admin::charts.bar>` | Bar charts | Based on Chart.js |
| `<x-admin::charts.line>` | Line charts | Based on Chart.js |
| `<x-admin::datagrid>` | Data tables | Sorting, filtering, pagination |
| `<x-admin::drawer>` | Slide-out panels | Position: top/bottom/left/right |
| `<x-admin::dropdown>` | Dropdown menus | Position options available |
| `<x-admin::flat-picker.date>` | Date picker | Based on Flatpickr |
| `<x-admin::flat-picker.datetime>` | Date-time picker | Based on Flatpickr |
| `<x-admin::media.images>` | Image upload | Multiple images support |
| `<x-admin::media.videos>` | Video upload | Video support |
| `<x-admin::modal>` | Dialog boxes | Header, content, footer slots |
| `<x-admin::quantity-changer>` | Quantity input | +/- buttons |
| `<x-admin::seo>` | SEO metadata | Meta title and description |
| `<x-admin::table>` | Data tables | Customizable thead/tbody |
| `<x-admin::tabs>` | Tab navigation | Position: left/right/center |
| `<x-admin::shimmer.*>` | Loading effects | Skeleton loaders |

## Custom Layouts

### Creating Custom Layout

**File:** `packages/Webkul/CustomAdminTheme/src/Resources/views/layouts/master.blade.php`

```blade
<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? config('app.name') }}</title>
    
    {{-- Load assets manually for custom layouts --}}
    @bagistoVite([
        'src/Resources/assets/css/app.css',
        'src/Resources/assets/js/app.js'
    ])
</head>
<body class="dark:bg-gray-900">
    {{-- Custom sidebar --}}
    @include('custom-admin-theme::layouts.sidebar')
    
    <div class="flex">
        {{-- Main content area --}}
        <main class="flex-1 p-6">
            {{ $slot }}
        </main>
    </div>
</body>
</html>
```

## Complete Package Structure

```
packages/Webkul/CustomAdminTheme/
├── src/
│   ├── Providers/
│   │   └── CustomAdminThemeServiceProvider.php
│   └── Resources/
│       ├── assets/
│       │   ├── css/
│       │   │   └── app.css
│       │   ├── js/
│       │   │   └── app.js
│       │   ├── images/
│       │   └── fonts/
│       └── views/
│           ├── layouts/
│           │   └── master.blade.php
│           ├── dashboard/
│           │   └── index.blade.php
│           ├── components/
│           └── ...
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `config/themes.php` | Theme configuration |
| `config/bagisto-vite.php` | Vite asset configuration |
| `packages/Webkul/Admin/src/Providers/AdminServiceProvider.php` | Admin package registration |
| `packages/Webkul/Admin/src/Resources/views/components/*` | Admin components |
| `packages/Webkul/Theme/src/Themes.php` | Theme facade |

## Common Pitfalls

- Not clearing cache after theme config changes
- Forgetting to run composer dump-autoload after package registration
- Not copying complete admin assets (views and assets)
- Using custom layouts without manually loading @bagistoVite assets
- Working in published files instead of package source files
- Missing symlink setup for development workflow

## Testing

Test your admin theme by:
1. Setting admin-default in config/themes.php
2. Logging into admin panel
3. Checking dashboard and various admin pages
4. Verifying responsive design
5. Verifying all admin functionality works
6. Testing hot reload during development
