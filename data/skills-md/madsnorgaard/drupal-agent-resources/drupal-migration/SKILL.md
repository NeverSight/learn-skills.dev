---
name: drupal-migration
description: Drupal migration expertise. Use when working with D7-to-D10 migrations, CSV imports, JSON API imports, or custom migration plugins.
---

# Drupal Migration Expert

You are an expert in Drupal's Migrate API, helping with D7 to D10/D11 migrations, CSV imports, and custom data migrations.

## Essential Modules

```bash
# Core migration modules
drush en migrate migrate_drupal migrate_drupal_ui

# Contrib essentials
composer require drupal/migrate_plus drupal/migrate_tools drupal/migrate_file
drush en migrate_plus migrate_tools migrate_file
```

| Module | Purpose |
|--------|---------|
| `migrate` | Core migration framework |
| `migrate_drupal` | D6/D7 migration support |
| `migrate_drupal_ui` | Browser-based migration wizard |
| `migrate_plus` | Config-based migrations, extra source plugins |
| `migrate_tools` | Drush commands for migrations |
| `migrate_file` | File migration handling |

## Migration Architecture

### Migration YAML Structure

```yaml
# migrations/migrate_plus.migration.my_migration.yml
id: my_migration
label: 'My Migration'
migration_group: my_group

source:
  plugin: source_plugin_name
  # Source configuration

process:
  # Field mappings
  destination_field: source_field

destination:
  plugin: 'entity:node'
  default_bundle: article

migration_dependencies:
  required:
    - other_migration
```

### Key Components

1. **Source** - Where data comes from (D7 database, CSV, JSON API)
2. **Process** - Transform data between source and destination
3. **Destination** - Where data goes (nodes, users, taxonomy terms)

## D7 to D10 Migration

### Setup Database Connection

```php
// settings.php
$databases['migrate']['default'] = [
  'driver' => 'mysql',
  'database' => 'drupal7_db',
  'username' => 'db_user',
  'password' => 'db_pass',
  'host' => 'localhost',
  'prefix' => '',
];
```

### Using the UI

```bash
drush en migrate_drupal_ui
# Visit /upgrade to use wizard
```

### Using Drush (Recommended)

```bash
# Generate migrations from D7
drush migrate:upgrade --legacy-db-key=migrate --configure-only

# List generated migrations
drush migrate:status

# Run all migrations
drush migrate:import --all

# Run specific migration
drush migrate:import upgrade_d7_node_article

# Rollback
drush migrate:rollback upgrade_d7_node_article
```

### Common D7 Migration Customizations

Override generated migrations with custom YAML:

```yaml
# migrations/migrate_plus.migration.upgrade_d7_node_article.yml
id: upgrade_d7_node_article
label: 'Article nodes from D7'
migration_group: migrate_drupal_7

source:
  plugin: d7_node
  node_type: article

process:
  type:
    plugin: default_value
    default_value: article
  title: title
  uid:
    plugin: migration_lookup
    migration: upgrade_d7_user
    source: uid
  body:
    plugin: sub_process
    source: body
    process:
      value: value
      format:
        plugin: static_map
        source: format
        map:
          full_html: full_html
          filtered_html: basic_html
        default_value: basic_html
  field_image:
    plugin: migration_lookup
    migration: upgrade_d7_file
    source: field_image/0/fid

destination:
  plugin: 'entity:node'
  default_bundle: article

migration_dependencies:
  required:
    - upgrade_d7_user
    - upgrade_d7_file
```

## CSV Migrations

### Source Plugin Configuration

```yaml
# migrations/migrate_plus.migration.import_products.yml
id: import_products
label: 'Import products from CSV'
migration_group: imports

source:
  plugin: csv
  path: 'modules/custom/my_module/data/products.csv'
  ids:
    - sku
  header_row_count: 1
  # Optionally define columns explicitly
  column_names:
    0:
      sku: 'Product SKU'
    1:
      name: 'Product Name'
    2:
      price: 'Price'
    3:
      category: 'Category'

process:
  type:
    plugin: default_value
    default_value: product
  title: name
  field_sku: sku
  field_price: price
  field_category:
    plugin: entity_lookup
    source: category
    entity_type: taxonomy_term
    bundle: product_categories
    bundle_key: vid
    value_key: name

destination:
  plugin: 'entity:node'
  default_bundle: product
```

### Running CSV Migrations

```bash
# Import
drush migrate:import import_products

# Update existing records
drush migrate:import import_products --update

# Reset status if stuck
drush migrate:reset-status import_products
```

## JSON/API Migrations

### HTTP JSON Source

```yaml
id: import_api_users
label: 'Import users from API'

source:
  plugin: url
  data_fetcher_plugin: http
  data_parser_plugin: json
  urls:
    - 'https://api.example.com/users'
  item_selector: data
  ids:
    id:
      type: integer
  fields:
    - name: id
      selector: id
    - name: email
      selector: email
    - name: full_name
      selector: attributes/name

process:
  name: full_name
  mail: email
  init: email
  status:
    plugin: default_value
    default_value: 1

destination:
  plugin: 'entity:user'
```

## Common Process Plugins

### Basic Transformations

```yaml
process:
  # Direct mapping
  title: source_title

  # Default value
  status:
    plugin: default_value
    default_value: 1

  # Static mapping
  field_type:
    plugin: static_map
    source: type
    map:
      old_type_1: new_type_1
      old_type_2: new_type_2
    default_value: default_type

  # Concatenate
  title:
    plugin: concat
    source:
      - first_name
      - last_name
    delimiter: ' '

  # Substring
  field_summary:
    plugin: substr
    source: body
    start: 0
    length: 200
```

### Entity References

```yaml
process:
  # Migration lookup (referenced entity was migrated)
  uid:
    plugin: migration_lookup
    migration: users
    source: author_id

  # Entity lookup (entity already exists)
  field_category:
    plugin: entity_lookup
    source: category_name
    entity_type: taxonomy_term
    bundle: categories
    bundle_key: vid
    value_key: name

  # Entity generate (create if not exists)
  field_tags:
    plugin: entity_generate
    source: tags
    entity_type: taxonomy_term
    bundle: tags
    bundle_key: vid
    value_key: name
```

### Multiple Values

```yaml
process:
  # Handle multiple values
  field_tags:
    plugin: sub_process
    source: tags
    process:
      target_id:
        plugin: entity_generate
        source: name
        entity_type: taxonomy_term
        bundle: tags
        value_key: name

  # Explode string to array
  field_keywords:
    - plugin: explode
      source: keywords
      delimiter: ','
    - plugin: entity_generate
      entity_type: taxonomy_term
      bundle: keywords
      value_key: name
```

### Conditional Processing

```yaml
process:
  # Skip if empty
  field_image:
    plugin: skip_on_empty
    method: process
    source: image_url

  # Skip row if condition
  pseudo_skip:
    plugin: skip_on_value
    source: status
    method: row
    value: 'draft'
```

## Custom Source Plugin

```php
<?php

declare(strict_types=1);

namespace Drupal\my_module\Plugin\migrate\source;

use Drupal\migrate\Attribute\MigrateSource;
use Drupal\migrate\Plugin\migrate\source\SqlBase;
use Drupal\migrate\Row;

/**
 * Custom source for legacy products.
 */
#[MigrateSource(
  id: 'legacy_products',
  source_module: 'my_module',
)]
class LegacyProducts extends SqlBase {

  /**
   * {@inheritdoc}
   */
  public function query() {
    $query = $this->select('legacy_products', 'p');
    $query->fields('p', ['id', 'name', 'price', 'description']);
    $query->condition('p.status', 'active');
    $query->orderBy('p.id');
    return $query;
  }

  /**
   * {@inheritdoc}
   */
  public function fields() {
    return [
      'id' => $this->t('Product ID'),
      'name' => $this->t('Product name'),
      'price' => $this->t('Price'),
      'description' => $this->t('Description'),
    ];
  }

  /**
   * {@inheritdoc}
   */
  public function getIds() {
    return [
      'id' => [
        'type' => 'integer',
        'alias' => 'p',
      ],
    ];
  }

  /**
   * {@inheritdoc}
   */
  public function prepareRow(Row $row) {
    // Add computed fields or modify data
    $price = $row->getSourceProperty('price');
    $row->setSourceProperty('price_with_tax', $price * 1.21);

    return parent::prepareRow($row);
  }

}
```

## Custom Process Plugin

```php
<?php

declare(strict_types=1);

namespace Drupal\my_module\Plugin\migrate\process;

use Drupal\migrate\Attribute\MigrateProcess;
use Drupal\migrate\MigrateExecutableInterface;
use Drupal\migrate\ProcessPluginBase;
use Drupal\migrate\Row;

/**
 * Converts price from cents to decimal.
 *
 * Example usage:
 * @code
 * process:
 *   field_price:
 *     plugin: cents_to_decimal
 *     source: price_cents
 * @endcode
 */
#[MigrateProcess(id: 'cents_to_decimal')]
class CentsToDecimal extends ProcessPluginBase {

  /**
   * {@inheritdoc}
   */
  public function transform($value, MigrateExecutableInterface $migrate_executable, Row $row, $destination_property) {
    if (empty($value) || !is_numeric($value)) {
      return NULL;
    }

    return number_format((float) $value / 100, 2, '.', '');
  }

}
```

## Drush Commands Reference

```bash
# List all migrations
drush migrate:status

# Run migration
drush migrate:import migration_id

# Run with options
drush migrate:import migration_id --limit=100
drush migrate:import migration_id --update
drush migrate:import migration_id --sync

# Rollback
drush migrate:rollback migration_id

# Reset stuck migration
drush migrate:reset-status migration_id

# Stop running migration
drush migrate:stop migration_id

# Show messages/errors
drush migrate:messages migration_id
```

## Debugging Migrations

### Enable Verbose Output

```bash
drush migrate:import migration_id -vvv
```

### Check Migration Status

```yaml
# Add to migration YAML
migration_tags:
  - debug
```

### Log Process Results

```php
// In custom process plugin
\Drupal::logger('my_migration')->notice('Processing: @value', ['@value' => $value]);
```

### Common Issues

**"Migration is busy":**
```bash
drush migrate:reset-status migration_id
```

**Memory errors:**
```bash
drush migrate:import migration_id --limit=500
# Process in batches
```

**Missing dependencies:**
Check `migration_dependencies` in YAML matches actual migration IDs.

## Best Practices

1. **Always use migration groups** to organize related migrations
2. **Set migration_dependencies** to ensure correct order
3. **Test with `--limit=10`** before full import
4. **Use `--update`** for re-running updated migrations
5. **Keep source data** until migration is verified
6. **Document field mappings** in migration YAML comments
7. **Create rollback plan** before production migration
8. **Monitor memory usage** for large migrations

## Migration Module Structure

```
my_migration/
├── my_migration.info.yml
├── my_migration.module
├── config/
│   └── install/
│       ├── migrate_plus.migration_group.my_group.yml
│       ├── migrate_plus.migration.users.yml
│       └── migrate_plus.migration.content.yml
├── src/
│   └── Plugin/
│       └── migrate/
│           ├── source/
│           │   └── LegacyProducts.php
│           └── process/
│               └── CentsToDecimal.php
└── data/
    └── import.csv
```

## Sources

- [Migrate API Documentation](https://www.drupal.org/docs/drupal-apis/migrate-api)
- [Migrate Plus](https://www.drupal.org/project/migrate_plus)
- [Migrate Tools](https://www.drupal.org/project/migrate_tools)
- [D7 to D10 Migration Guide](https://www.drupal.org/docs/upgrading-drupal/upgrading-from-drupal-7)
