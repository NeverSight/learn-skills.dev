---
name: drupal-backend
description: Drupal Back End Specialist skill for custom module development, hooks, APIs, and PHP programming (Drupal 8-11+). Use when building custom modules, implementing hooks, working with entities, forms, plugins, or services.
---

# Drupal Back End Development

## Overview

Enable expert-level Drupal back end development capabilities. Provide comprehensive guidance for custom module development, PHP programming, API usage, hooks, plugins, services, and database operations for Drupal 8, 9, 10, and 11+.

## When to Use This Skill

Invoke this skill when working with:
- **Custom module development**: Creating new Drupal modules
- **Hooks**: Implementing Drupal hooks to alter system behavior
- **Controllers & routing**: Building custom pages and routes
- **Forms**: Creating configuration or custom forms
- **Entities**: Working with content entities or config entities
- **Plugins**: Building blocks, field types, formatters, or other plugins
- **Services**: Creating reusable business logic services
- **Database operations**: Custom queries and schema definitions
- **APIs**: Entity API, Form API, Database API, Plugin API

## Core Capabilities

### 1. Custom Module Development

Create complete, standards-compliant Drupal modules:

**Quick start workflow:**
1. Use module template from `assets/module-template/`
2. Replace `MODULENAME` with machine name (lowercase, underscores)
3. Replace `MODULELABEL` with human-readable name
4. Implement functionality using Drupal APIs
5. Enable module and test: `ddev drush en mymodule -y`

**Module structure:**
- `.info.yml` - Module metadata and dependencies
- `.module` - Hook implementations
- `.routing.yml` - Route definitions
- `.services.yml` - Service definitions
- `.permissions.yml` - Custom permissions
- `src/` - PHP classes (PSR-4 autoloading)
- `config/` - Configuration files

**Reference documentation:**
- `references/module_structure.md` - Complete module patterns
- `references/hooks.md` - Hook implementations

### 2. Hooks System

Implement hooks to alter Drupal behavior:

**Common hooks:**
- `hook_entity_presave()` - Modify entities before saving
- `hook_entity_insert/update/delete()` - React to entity changes
- `hook_form_alter()` - Modify any form
- `hook_node_access()` - Control node access
- `hook_cron()` - Perform periodic tasks
- `hook_install/uninstall()` - Module installation tasks

**Hook pattern:**
```php
function MODULENAME_hook_name($param1, &$param2) {
  // Implementation
}
```

**Best practices:**
- Implement hooks in `.module` file only
- Use proper type hints
- Document with PHPDoc blocks
- Check for entity types before processing
- Be mindful of performance

### 3. Controllers & Routing

Create custom pages and endpoints:

**Route definition** (`.routing.yml`):
```yaml
mymodule.example:
  path: '/example/{param}'
  defaults:
    _controller: '\Drupal\mymodule\Controller\ExampleController::content'
    _title: 'Example Page'
  requirements:
    _permission: 'access content'
    param: \d+
```

**Controller pattern:**
```php
namespace Drupal\mymodule\Controller;

use Drupal\Core\Controller\ControllerBase;

class ExampleController extends ControllerBase {
  public function content() {
    return ['#markup' => $this->t('Hello!')];
  }
}
```

**With dependency injection:**
```php
public function __construct(EntityTypeManagerInterface $entity_type_manager) {
  $this->entityTypeManager = $entity_type_manager;
}

public static function create(ContainerInterface $container) {
  return new static($container->get('entity_type.manager'));
}
```

### 4. Forms API

Build configuration and custom forms:

**Configuration form:**
```php
class SettingsForm extends ConfigFormBase {
  protected function getEditableConfigNames() {
    return ['mymodule.settings'];
  }

  public function buildForm(array $form, FormStateInterface $form_state) {
    $config = $this->config('mymodule.settings');
    
    $form['api_key'] = [
      '#type' => 'textfield',
      '#title' => $this->t('API Key'),
      '#default_value' => $config->get('api_key'),
    ];
    
    return parent::buildForm($form, $form_state);
  }

  public function submitForm(array &$form, FormStateInterface $form_state) {
    $this->config('mymodule.settings')
      ->set('api_key', $form_state->getValue('api_key'))
      ->save();
    parent::submitForm($form, $form_state);
  }
}
```

**Form validation:**
```php
public function validateForm(array &$form, FormStateInterface $form_state) {
  if (strlen($form_state->getValue('field')) < 5) {
    $form_state->setErrorByName('field', $this->t('Too short.'));
  }
}
```

### 5. Entity API

Work with content and configuration entities:

**Loading entities:**
```php
// Load single entity
$node = \Drupal::entityTypeManager()->getStorage('node')->load($nid);

// Load multiple entities
$nodes = \Drupal::entityTypeManager()->getStorage('node')->loadMultiple([1, 2, 3]);

// Load by properties
$nodes = \Drupal::entityTypeManager()->getStorage('node')->loadByProperties([
  'type' => 'article',
  'status' => 1,
]);
```

**Creating/saving entities:**
```php
$node = \Drupal::entityTypeManager()->getStorage('node')->create([
  'type' => 'article',
  'title' => 'My Article',
  'body' => ['value' => 'Content', 'format' => 'basic_html'],
]);
$node->save();
```

**Entity queries:**
```php
$query = \Drupal::entityQuery('node')
  ->condition('type', 'article')
  ->condition('status', 1)
  ->accessCheck(TRUE)
  ->sort('created', 'DESC')
  ->range(0, 10);
$nids = $query->execute();
```

### 6. Plugin System

Create custom plugins (blocks, fields, etc.):

**Block plugin:**
```php
/**
 * @Block(
 *   id = "mymodule_custom_block",
 *   admin_label = @Translation("Custom Block"),
 * )
 */
class CustomBlock extends BlockBase {
  public function build() {
    return ['#markup' => 'Block content'];
  }
  
  public function blockForm($form, FormStateInterface $form_state) {
    $form['setting'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Setting'),
      '#default_value' => $this->configuration['setting'] ?? '',
    ];
    return $form;
  }
  
  public function blockSubmit($form, FormStateInterface $form_state) {
    $this->configuration['setting'] = $form_state->getValue('setting');
  }
}
```

### 7. Services & Dependency Injection

Create reusable services:

**Service definition** (`.services.yml`):
```yaml
services:
  mymodule.custom_service:
    class: Drupal\mymodule\Service\CustomService
    arguments: ['@entity_type.manager', '@current_user']
```

**Service class:**
```php
namespace Drupal\mymodule\Service;

class CustomService {
  protected $entityTypeManager;
  protected $currentUser;

  public function __construct(EntityTypeManagerInterface $entity_type_manager, AccountProxyInterface $current_user) {
    $this->entityTypeManager = $entity_type_manager;
    $this->currentUser = $current_user;
  }

  public function doSomething() {
    // Business logic
  }
}
```

### 8. Database Operations

Execute custom queries:

**Using Database API:**
```php
$database = \Drupal::database();

// Select query
$query = $database->select('node_field_data', 'n')
  ->fields('n', ['nid', 'title'])
  ->condition('type', 'article')
  ->condition('status', 1)
  ->range(0, 10);
$results = $query->execute()->fetchAll();

// Insert
$database->insert('mymodule_table')
  ->fields(['name' => 'Example', 'value' => 123])
  ->execute();

// Update
$database->update('mymodule_table')
  ->fields(['value' => 456])
  ->condition('name', 'Example')
  ->execute();
```

**Schema definition** (`.install` file):
```php
function mymodule_schema() {
  $schema['mymodule_table'] = [
    'fields' => [
      'id' => ['type' => 'serial', 'not null' => TRUE],
      'name' => ['type' => 'varchar', 'length' => 255, 'not null' => TRUE],
      'value' => ['type' => 'int', 'not null' => TRUE, 'default' => 0],
    ],
    'primary key' => ['id'],
    'indexes' => ['name' => ['name']],
  ];
  return $schema;
}
```

## Development Workflow

### Creating a Custom Module

1. **Scaffold the module:**
   ```bash
   cp -r assets/module-template/ /path/to/drupal/modules/custom/mymodule/
   cd /path/to/drupal/modules/custom/mymodule/
   mv MODULENAME.info.yml mymodule.info.yml
   mv MODULENAME.module mymodule.module
   mv MODULENAME.routing.yml mymodule.routing.yml
   ```

2. **Update module files:**
   - Replace `MODULENAME` with machine name
   - Replace `MODULELABEL` with readable name
   - Update `.info.yml` dependencies
   - Customize controller, routes, logic

3. **Enable and test:**
   ```bash
   ddev drush en mymodule -y
   ddev drush cr
   ```

4. **Develop iteratively:**
   - Implement functionality
   - Clear cache: `ddev drush cr`
   - Test thoroughly
   - Check logs: `ddev drush watchdog:tail`

### Standard Development Workflow

1. **Plan**: Identify what APIs/hooks you need
2. **Code**: Implement using Drupal APIs
3. **Test**: Enable module, clear cache, test functionality
4. **Debug**: Check logs, use Xdebug if needed
5. **Refine**: Optimize, add tests, improve code quality

## Best Practices

### Module Development
1. **PSR-4 autoloading**: Follow namespace conventions
2. **Dependency injection**: Use DI in classes
3. **Hooks**: Implement only in `.module` files
4. **Type hints**: Use proper PHP type declarations
5. **Documentation**: Add PHPDoc blocks
6. **Testing**: Write automated tests

### Code Quality
1. **Drupal coding standards**: Follow PHPCS rules
2. **Security**: Validate input, sanitize output, check permissions
3. **Performance**: Cache when possible, optimize queries
4. **Accessibility**: Ensure forms and pages are accessible
5. **Internationalization**: Use `$this->t()` for all strings

### API Usage
1. **Entity API**: Prefer entity operations over direct DB queries
2. **Configuration**: Use Config API for settings
3. **State API**: Use for temporary/non-exportable data
4. **Cache API**: Implement caching for expensive operations
5. **Queue API**: Use for long-running tasks

## Common Patterns

### Event Subscriber

```php
class MyModuleSubscriber implements EventSubscriberInterface {
  public static function getSubscribedEvents() {
    return [KernelEvents::REQUEST => ['onRequest', 0]];
  }

  public function onRequest(RequestEvent $event) {
    // Handle event
  }
}
```

### Custom Permission

```yaml
# mymodule.permissions.yml
administer mymodule:
  title: 'Administer My Module'
  restrict access: true
```

### Custom Access Check

```php
class CustomAccessCheck implements AccessInterface {
  public function access(AccountInterface $account) {
    return AccessResult::allowedIf($account->hasPermission('access content'));
  }
}
```

## Troubleshooting

### Module Not Appearing
- Check `.info.yml` syntax
- Verify `core_version_requirement`
- Clear cache: `ddev drush cr`

### Hooks Not Working
- Verify hook name is correct
- Clear cache after adding hooks
- Check module weight if hook order matters

### Class Not Found
- Verify PSR-4 namespace matches directory
- Clear cache to rebuild class registry
- Check autoloading with `composer dump-autoload`

### Database Errors
- Check schema definition syntax
- Run `ddev drush updb` after schema changes
- Verify table/column names in queries

## Resources

### Reference Documentation

- **`references/hooks.md`** - Common hooks with examples
  - Entity hooks
  - Form hooks
  - Node hooks
  - Installation hooks
  - Token hooks

- **`references/module_structure.md`** - Module patterns
  - Controllers and routing
  - Forms (config and custom)
  - Plugins (blocks, fields, etc.)
  - Services and DI
  - Event subscribers

### Asset Templates

- **`assets/module-template/`** - Module scaffold
  - `.info.yml` metadata
  - `.module` hook file
  - `.routing.yml` routes
  - Example controller

## Version Compatibility

### Drupal 8 vs 9 vs 10 vs 11
- **Core APIs**: Largely consistent across versions
- **PHP requirements**: 8.x (7.0+), 9.x (7.3+), 10.x (8.1+), 11.x (8.3+)
- **Deprecations**: Check change records when upgrading
- **Symfony**: Different Symfony versions in each Drupal version

## See Also

- **drupal-frontend** - Theme development, Twig templates
- **drupal-tooling** - DDEV and Drush development tools
- [Drupal API](https://api.drupal.org/) - Official API documentation
