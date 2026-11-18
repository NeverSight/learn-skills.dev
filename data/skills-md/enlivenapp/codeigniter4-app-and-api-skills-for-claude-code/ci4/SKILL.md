---
name: ci4
description: Comprehensive CodeIgniter 4 framework skill. Use when working with any CodeIgniter 4 project — routing, controllers, models, views, query builder, migrations, filters, services, Spark CLI, and Shield auth. Activates on mentions of "CodeIgniter", "CI4", "spark", "CI4 model", "CI4 controller", "CI4 route", or any CI4-specific pattern.
version: 2.0.0
---

# CodeIgniter 4 — Framework Reference

CodeIgniter 4 is a full-stack PHP 8+ MVC framework. It is **not Laravel**. Do not apply Laravel APIs, method names, or conventions here. When in doubt, check this skill and its references — not memory of another framework.

> **Related skills**: `ci4-api` for REST API patterns, `ci4-shield` for authentication/authorization.

## Reference Documents

For deep dives, read the relevant reference from `references/`:

| Reference | When to read |
|---|---|
| `references/routing.md` | Route groups, placeholders, named routes, resource routes |
| `references/controllers.md` | ResourceController, request data, validation, redirects, flash data |
| `references/models.md` | CRUD, soft deletes, timestamps, validation, pagination, scopes, callbacks, entities |
| `references/query-builder.md` | SELECT, WHERE, JOIN, GROUP BY, batch ops, subqueries, transactions, debugging |
| `references/views.md` | Layouts, sections, partials, escaping, view cells |
| `references/filters.md` | Creating, registering, applying, global filters, filter arguments |
| `references/database.md` | Migrations, seeds, forge, field types, adding/dropping columns |
| `references/validation.md` | All validation rules, custom rules, file upload validation |
| `references/services-helpers.md` | Services, helpers, caching, email, sessions, encryption |
| `references/spark-cli.md` | All spark commands, generators, custom commands |
| `references/testing.md` | PHPUnit, feature tests, database tests, mocking |
| `references/gotchas.md` | Critical pitfalls, CI4 vs Laravel comparison table |

---

## Directory Structure

```
app/
  Config/         # All configuration classes (Routes, Database, Filters, Auth, etc.)
  Controllers/    # HTTP controllers
  Database/
    Migrations/   # Migration files (timestamped)
    Seeds/        # Seeder classes
  Filters/        # Before/after request filters
  Libraries/      # Custom libraries
  Models/         # Model classes
  Services/       # Custom service classes
  Views/          # View templates (.php)
    layouts/      # Layout templates
    partials/     # Reusable partials
public/           # Web root — index.php entry point lives here
writable/         # Cache, logs, sessions (must be writable)
tests/
vendor/
.env              # Environment config (copy from `env`)
spark             # CLI entry point
```

---

## MVC Conventions — Hard Rules

1. **Controllers handle HTTP** — receive request, call model/service, return response. No business logic.
2. **Models handle data** — all database interaction lives here. No HTTP concerns.
3. **Views handle display** — no DB calls, no business logic. Only presentation.
4. **Never call models from views.** Ever.
5. Web controllers call models directly — that is standard CI4.
6. One controller = one resource. Name them descriptively (`UserController`, `EventController`).

---

## Configuration

All config lives in `app/Config/` as PHP classes (not arrays, not .ini files).

```php
// app/Config/Database.php — DB connection
// app/Config/Routes.php   — route definitions
// app/Config/Filters.php  — filter aliases + global filters
// app/Config/App.php      — base URL, timezone, etc.
```

`.env` overrides any config value using dot-notation:
```
database.default.hostname = localhost
database.default.database = mydb
app.baseURL = 'http://example.com/'
CI_ENVIRONMENT = development
```

---

## Routing

Defined in `app/Config/Routes.php`. See `references/routing.md` for complete reference.

```php
$routes->get('users', 'UserController::index');
$routes->post('users', 'UserController::create');
$routes->get('users/(:num)', 'UserController::show/$1');
$routes->put('users/(:num)', 'UserController::update/$1');
$routes->delete('users/(:num)', 'UserController::delete/$1');

// Route groups
$routes->group('admin', ['namespace' => 'App\Controllers\Admin'], function ($routes) {
    $routes->get('users', 'UsersController::index');
});

// Apply filter to a route
$routes->get('dashboard', 'DashboardController::index', ['filter' => 'session']);

// Resource routes — generates full CRUD
$routes->resource('photos');
```

### Route Placeholders
| Placeholder | Matches |
|---|---|
| `(:num)` | Digits only |
| `(:alpha)` | Alphabetic only |
| `(:alphanum)` | Alphanumeric |
| `(:segment)` | URL segment (no slashes) |
| `(:any)` | Anything (use sparingly) |

---

## Controllers

See `references/controllers.md` for complete reference.

```php
<?php
namespace App\Controllers;

use App\Controllers\BaseController;

class UserController extends BaseController
{
    public function index()
    {
        $model = new \App\Models\UserModel();
        return view('users/index', ['users' => $model->findAll()]);
    }
}
```

### Request Data
```php
$this->request->getGet('name');       // GET param
$this->request->getPost('email');     // POST param
$this->request->getJSON(true);        // JSON body as array
$this->request->getVar('key');        // GET + POST
$this->request->getFile('avatar');    // File upload
```

### Validation
```php
$rules = [
    'email' => 'required|valid_email',
    'name'  => 'required|min_length[2]|max_length[100]',
];

if (!$this->validate($rules)) {
    return redirect()->back()->withInput()->with('errors', $this->validator->getErrors());
}
```

### Redirects
```php
return redirect()->to('/dashboard');
return redirect()->back();
return redirect()->back()->withInput()->with('error', 'Something went wrong.');
```

**GOTCHA**: Never add PHP type hints (`int $id`) to overridden ResourceController methods like `show($id = null)`. The parent signature uses `$id = null` — a type hint breaks the override.

---

## Models

See `references/models.md` for complete reference.

```php
<?php
namespace App\Models;

use CodeIgniter\Model;

class UserModel extends Model
{
    protected $table            = 'users';
    protected $primaryKey       = 'id';
    protected $useAutoIncrement = true;
    protected $returnType       = 'object';   // Always use 'object' (not 'array')
    protected $useSoftDeletes   = false;
    protected $protectFields    = true;
    protected $allowedFields    = ['name', 'email', 'role'];

    protected $useTimestamps = true;
    protected $createdField  = 'created_at';
    protected $updatedField  = 'updated_at';
}
```

### CRUD
```php
$model = new UserModel();
$user  = $model->find(1);                          // by ID
$users = $model->findAll();                         // all
$user  = $model->where('email', 'a@b.com')->first(); // where
$id    = $model->insert(['name' => 'Rob', 'email' => 'r@b.com']);
$model->update(1, ['name' => 'Robert']);
$model->delete(1);
$users = $model->paginate(20);                      // pagination
$pager = $model->pager;                             // pager for view
```

---

## Query Builder

See `references/query-builder.md` for complete reference.

```php
$db = \Config\Database::connect();
$builder = $db->table('users');

$builder->select('id, name, email')
    ->where('active', 1)
    ->orderBy('created_at', 'DESC')
    ->limit(10);

$rows = $builder->get()->getResult();     // array of objects
$row  = $builder->get()->getRow();        // single object
```

**CRITICAL GOTCHAS**:
- `whereNull()` does **not exist** in CI4. Use `->where('col IS NULL')`.
- `->select('DISTINCT col')` returns wrong results. Use `->select('col')->distinct()`.

---

## Views

See `references/views.md` for complete reference.

```php
// Controller
return view('users/index', ['users' => $users, 'title' => 'Users']);
```

```php
<!-- app/Views/users/index.php -->
<?= $this->extend('layouts/main') ?>

<?= $this->section('content') ?>
<h1><?= esc($title) ?></h1>
<?php foreach ($users as $user): ?>
    <p><?= esc($user->name) ?></p>
<?php endforeach; ?>
<?= $this->endSection() ?>
```

**Always use `esc()` for output.** Never use `return` inside a view that uses `$this->extend()`.

---

## Filters

See `references/filters.md` for complete reference.

```php
<?php
namespace App\Filters;

use CodeIgniter\Filters\FilterInterface;
use CodeIgniter\HTTP\RequestInterface;
use CodeIgniter\HTTP\ResponseInterface;

class AuthFilter implements FilterInterface
{
    public function before(RequestInterface $request, $arguments = null)
    {
        if (!auth()->loggedIn()) {
            return redirect()->to('/login');
        }
    }

    public function after(RequestInterface $request, ResponseInterface $response, $arguments = null) {}
}
```

Register in `app/Config/Filters.php`, apply via routes:
```php
$routes->get('admin', 'AdminController::index', ['filter' => ['session', 'group:admin']]);
```

---

## Migrations

See `references/database.md` for complete reference.

```bash
php spark make:migration CreateUsersTable
php spark migrate
```

```php
public function up(): void
{
    $this->forge->addField([
        'id'         => ['type' => 'INT', 'constraint' => 11, 'unsigned' => true, 'auto_increment' => true],
        'name'       => ['type' => 'VARCHAR', 'constraint' => 150],
        'email'      => ['type' => 'VARCHAR', 'constraint' => 255, 'unique' => true],
        'created_at' => ['type' => 'DATETIME', 'null' => true],
        'updated_at' => ['type' => 'DATETIME', 'null' => true],
    ]);
    $this->forge->addPrimaryKey('id');
    $this->forge->createTable('users');
}
```

---

## Spark CLI Quick Reference

See `references/spark-cli.md` for complete reference.

```bash
php spark serve                          # dev server
php spark routes                         # list routes
php spark migrate                        # run migrations
php spark migrate:rollback               # rollback last batch
php spark db:seed DatabaseSeeder         # run seeder
php spark make:controller UserController # scaffold
php spark make:model UserModel           # scaffold
php spark make:migration CreateUsersTable
php spark make:filter AuthFilter
php spark cache:clear
```

---

## Key Gotchas

See `references/gotchas.md` for the complete list and CI4 vs Laravel comparison.

1. `whereNull()` does not exist — use `->where('col IS NULL')`
2. `->select('DISTINCT col')` fails silently — use `->select('col')->distinct()`
3. Never type-hint overridden ResourceController params
4. `redirect()` must be `return`ed — without `return` it does nothing
5. `insertBatch()` bypasses `$allowedFields` — be deliberate about what you pass
6. Never use `return` inside a view using `$this->extend()`
7. View sections cannot be nested — close one before opening another
8. `orLike()` after `where()` needs `groupStart()`/`groupEnd()`
9. Model `save()` decides insert vs update by whether primary key is present
10. `$returnType` should always be `'object'` — `'array'` is inconsistent
