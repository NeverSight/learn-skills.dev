---
name: pelican-panel-plugins
description: Write, scaffold, explain, and debug plugins for the Pelican gaming panel. Use this skill whenever the user wants to create a Pelican plugin, add functionality to the Pelican panel, build a FilamentPHP resource or page for Pelican, register custom permissions, add plugin settings, write plugin routes, or asks anything about Pelican plugin development — even if they just say "I want to add something to Pelican" or "how do I extend Pelican".
---

# Pelican Panel Plugins

Pelican is an open-source game server management panel built on Laravel + FilamentPHP. Plugins let you add functionality without touching core files.

> ⚠️ The plugin system is still in active development — some features may change.

## Quick Reference

📖 **Detailed Guides:**
- [FilamentPHP Patterns](references/filament-patterns.md) - Resources, pages, widgets, actions, relation managers
- [Advanced Patterns](references/advanced-patterns.md) - Models, services, routes, commands, events
- [Complete Plugin Walkthrough](examples/complete-plugin-walkthrough.md) - Step-by-step example

## Scaffolding a New Plugin

Run inside the panel directory (`/var/www/pelican` by default):

```bash
php artisan p:plugin:make
```

This creates the basic structure with `plugin.json`, main plugin class, service provider, and config file.

> **Critical:** The plugin folder name must exactly match the `id` field in `plugin.json`.

## Plugin Structure

```
plugins/my-plugin/
├── plugin.json              # Metadata and configuration
├── config/
│   └── my-plugin.php       # Config values (use env vars)
├── database/
│   └── migrations/         # Auto-discovered migrations
├── lang/                   # Translations (namespaced: my-plugin::strings.key)
├── resources/
│   └── views/              # Blade views (namespaced: my-plugin::view-name)
├── routes/                 # Optional route files
└── src/                    # App logic (PSR-4 autoloaded)
    ├── MyPlugin.php        # Main plugin class
    ├── Filament/
    │   ├── Admin/          # Admin panel components
    │   │   ├── Pages/
    │   │   ├── Resources/
    │   │   └── Widgets/
    │   ├── App/            # Server list panel
    │   └── Server/         # Server management panel
    ├── Models/
    ├── Policies/           # Auto-discovered
    ├── Providers/          # Auto-discovered service providers
    ├── Console/Commands/   # Auto-discovered artisan commands
    └── Http/
        └── Controllers/
```

Everything in standard Laravel locations is **auto-discovered**: migrations, providers, commands, policies.

## plugin.json

```json
{
    "id": "my-plugin",
    "name": "My Plugin",
    "author": "Your Name",
    "version": "1.0.0",
    "description": "Short description",
    "category": "plugin",
    "namespace": "MyName\\MyPlugin",
    "class": "MyPlugin",
    "panels": ["admin", "server"],
    "panel_version": "^1.2.0",
    "composer_packages": {
        "vendor/package": "^1.0"
    }
}
```

| Field | Required | Notes |
|---|---|---|
| `id` | ✅ | Must match folder name |
| `namespace` | ✅ | PHP namespace root (use `\\` for backslashes) |
| `class` | ✅ | Main class name (in `src/`) |
| `category` | ✅ | `plugin`, `theme`, or `language` |
| `panels` | No | Array of panel IDs or omit for all panels |
| `panel_version` | No | Minimum panel version (e.g., `^1.2.0`) |
| `composer_packages` | No | External dependencies |

## Main Plugin Class

Located in `src/{ClassName}.php`:

```php
namespace MyName\MyPlugin;

use Filament\Contracts\Plugin;
use Filament\Panel;

class MyPlugin implements Plugin
{
    public function getId(): string
    {
        return 'my-plugin';
    }

    public function register(Panel $panel): void
    {
        $id = str($panel->getId())->title(); // "Admin", "App", "Server"

        // Auto-discover Filament components
        $panel->discoverPages(
            plugin_path($this->getId(), "src/Filament/$id/Pages"),
            "MyName\\MyPlugin\\Filament\\$id\\Pages"
        );
        $panel->discoverResources(
            plugin_path($this->getId(), "src/Filament/$id/Resources"),
            "MyName\\MyPlugin\\Filament\\$id\\Resources"
        );
        $panel->discoverWidgets(
            plugin_path($this->getId(), "src/Filament/$id/Widgets"),
            "MyName\\MyPlugin\\Filament\\$id\\Widgets"
        );
    }

    public function boot(Panel $panel): void
    {
        //
    }
}
```

## The Three Filament Panels

| Panel ID | Area | Use Case |
|---|---|---|
| `admin` | Admin area | Full CRUD for resources, settings, management |
| `app` | Server list | Minimal UI (no nav by default) |
| `server` | Server management | Tenant-scoped (current server context) |

### Enabling Navigation on `app` Panel

```php
use App\Filament\App\Resources\Servers\ServerResource;
use App\Enums\CustomizationKey;

public function register(Panel $panel): void
{
    parent::register($panel);

    if ($panel->getId() === 'app') {
        ServerResource::embedServerList();
        $panel->navigation(true);
        $panel->topbar(function () {
            $nav = user()?->getCustomization(CustomizationKey::TopNavigation);
            return in_array($nav, ['topbar', 'mixed', true], true);
        });
        $panel->clearCachedComponents();
    }
}
```

## Extending Core Resources

Call static methods on core classes inside a **service provider's `register()`**:

```php
use App\Filament\Admin\Resources\Users\UserResource;
use App\Filament\Admin\Resources\Servers\ServerResource;
use App\Models\Role;

public function register(): void
{
    // Add a relation manager tab
    ServerResource::registerCustomRelations(MyRelationManager::class);
    
    // Register permissions
    Role::registerCustomDefaultPermissions('myModel');
    Role::registerCustomModelIcon('myModel', 'tabler-star');
}
```

**Available customization traits** (check `app/Traits/Filament/` for all):
- `CanModifyResource` - Relation managers, custom actions
- `CanCustomizePage` - Widgets, header actions
- `CanModifyForm` / `CanModifyTable` - Form/table hooks

## Plugin Settings

Implement `HasPluginSettings` on your main class:

```php
use App\Contracts\Plugins\HasPluginSettings;
use App\Traits\EnvironmentWriterTrait;
use Filament\Forms\Components\TextInput;
use Filament\Notifications\Notification;

class MyPlugin implements Plugin, HasPluginSettings
{
    use EnvironmentWriterTrait;

    public function getSettingsForm(): array
    {
        return [
            TextInput::make('api_key')
                ->required()
                ->default(fn () => config('my-plugin.api_key')),
        ];
    }

    public function saveSettings(array $data): void
    {
        $this->writeToEnvironment([
            'MY_PLUGIN_API_KEY' => $data['api_key'],
        ]);

        Notification::make()->title('Settings saved')->success()->send();
    }
}
```

> Always prefix env vars with your plugin ID to avoid conflicts.

## Permissions

### Admin Role Permissions

In your service provider's `register()`:

```php
use App\Models\Role;

// Shorthand: registers viewList, view, create, update, delete
Role::registerCustomDefaultPermissions('myModel');

// Custom permissions
Role::registerCustomPermissions([
    'myModel' => ['export', 'approve'],
    'server'  => ['customAction'], // extend existing model
]);

// Optional: icon for permission group
Role::registerCustomModelIcon('myModel', 'tabler-star');
```

### Subuser Permissions

```php
use App\Models\Subuser;

// New permission group
Subuser::registerCustomPermissions('myFeature', ['read', 'write'], 'tabler-bolt', false);

// Append to existing group
Subuser::registerCustomPermissions('console', ['myCustomAction']);
```

## Routes

Create a `RouteServiceProvider` in `src/Providers/`:

```php
use Illuminate\Foundation\Support\Providers\RouteServiceProvider;
use Illuminate\Support\Facades\Route;

class MyPluginRoutesProvider extends RouteServiceProvider
{
    public function boot(): void
    {
        $this->routes(function () {
            // Simple route
            Route::get('/my-plugin/test', [TestController::class, 'index'])
                ->name('my-plugin.test');

            // Load from file
            Route::prefix('/my-plugin')
                ->group(plugin_path('my-plugin', 'routes/web.php'));

            // Append to client API
            Route::middleware(['api', 'client-api', 'throttle:api.client'])
                ->prefix('/api/client/servers/{server}')
                ->scopeBindings()
                ->group(plugin_path('my-plugin', 'routes/api-client.php'));
        });
    }
}
```

## Models & Relationships

### Add Relationship to Core Models

In your service provider's `boot()`:

```php
use App\Models\Server;
use MyPlugin\Models\Ticket;

public function boot(): void
{
    Server::resolveRelationUsing('tickets', fn (Server $server) => 
        $server->hasMany(Ticket::class, 'server_id', 'id')
    );
}
```

Now `$server->tickets` works everywhere.

### Policies

```php
use App\Policies\DefaultAdminPolicies;

class MyModelPolicy
{
    use DefaultAdminPolicies;
    
    protected string $modelName = 'myModel';
}
```

This automatically checks admin role permissions based on the registered model name.

## Translations

Place in `lang/{locale}/` (e.g., `lang/en/strings.php`):

```php
return [
    'welcome' => 'Welcome',
    'item' => 'Item|Items', // Pluralization
];
```

Usage:
```php
trans('my-plugin::strings.welcome')
trans_choice('my-plugin::strings.item', 2) // "Items"
```

## Views

Place in `resources/views/`:

```php
view('my-plugin::my-view')
// → plugins/my-plugin/resources/views/my-view.blade.php
```

## Common Patterns

### FilamentPHP Components

See [FilamentPHP Patterns](references/filament-patterns.md) for:
- Resources (CRUD interfaces)
- Pages (custom pages)
- Widgets (dashboard components)
- Relation Managers (manage related records)
- Custom Actions (reusable buttons)
- Form components (inputs, selects, toggles)
- Table columns and filters

### Advanced Patterns

See [Advanced Patterns](references/advanced-patterns.md) for:
- Model events and hooks
- Enums with Filament interfaces
- Service classes
- HTTP controllers and API routes
- Artisan commands and scheduling
- HTTP macros for external APIs
- Database migrations
- Error handling

### Complete Example

See [Complete Plugin Walkthrough](examples/complete-plugin-walkthrough.md) for a step-by-step guide building a "Server Notes" plugin.

## Publishing a Plugin

1. Open `plugin.json` and **remove** the `meta` block (internal use only)
2. Zip the entire plugin folder
3. Share the zip — users install via panel UI Import button or manually drop into `plugins/`

Publish to the community:
- GitHub: [pelican-dev/plugins](https://github.com/pelican-dev/plugins)
- Discord: `#plugins` channel at [discord.gg/pelican-panel](https://discord.gg/pelican-panel)

## Tips & Gotchas

- **Namespace in plugin.json**: Use `\\` (double backslash) for namespace separators
- **Migration naming**: Use numeric prefixes (`001_`, `002_`) to control execution order
- **Environment variables**: Always prefix with your plugin ID (e.g., `MY_PLUGIN_*`)
- **Panel context**: Use `Filament::getTenant()` to get current server in server panel
- **Auto-discovery**: Service providers, commands, migrations, and policies are auto-discovered
- **Relation managers**: Must be registered on core resources via `registerCustomRelations()` in service provider's `register()` method
- **Testing**: Use `php artisan migrate:fresh --seed` to reset and test migrations
- **Permissions**: Register in service provider's `register()`, not `boot()`

## Getting Help

- **Documentation**: [pelican.dev/docs/panel](https://pelican.dev/docs/panel)
- **Discord**: [discord.gg/pelican-panel](https://discord.gg/pelican-panel)
- **GitHub**: [github.com/pelican-dev/panel](https://github.com/pelican-dev/panel)
- **Example Plugins**: [github.com/pelican-dev/plugins](https://github.com/pelican-dev/plugins)
