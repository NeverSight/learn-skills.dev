---
name: modular-saas-architecture
description: "Build SAAS platforms with pluggable business modules (Advanced Inventory, Restaurant, Pharmacy, etc.) that can be enabled/disabled per tenant without breaking the system. Use when designing modular SAAS features, implementing module toggles, ensuring module independence, and building scalable multi-tenant platforms with optional features."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Modular SAAS Architecture

## Overview

Architecture pattern for building SAAS platforms where business modules (Advanced Inventory, Restaurant, Pharmacy, Retail, etc.) can be independently enabled, disabled, or added without affecting other parts of the system.

**Core Principles:**

- **Module Independence**: Each module is self-contained with minimal dependencies
- **Graceful Degradation**: Disabling a module doesn't break dependent features
- **Per-Tenant Control**: Each tenant can enable only the modules they need
- **Zero Breaking Changes**: Adding/removing modules preserves existing functionality
- **Clean Interfaces**: Modules communicate through well-defined contracts

**Security Baseline (Required):** Always load and apply the **Vibe Security Skill** for any web app, API, or module implementation work.

**Key Benefits:**

- Customers pay only for modules they use
- Faster feature development (independent teams per module)
- Easier testing (modules tested in isolation)
- Better scaling (resource-intensive modules can scale independently)
- Reduced complexity (tenants see only their enabled modules)

## When to Use

✅ **Use for:**

- Multi-tenant SAAS platforms with diverse customer needs
- Systems serving different industries (retail, healthcare, hospitality, etc.)
- Platforms with optional premium features
- Applications requiring vertical-specific functionality
- Systems with varying compliance requirements per industry

❌ **Don't use for:**

- Single-tenant applications
- Simple CRUD apps without feature variations
- Tightly coupled monolithic systems
- Systems where all features are always required

## Module Architecture Pattern

### System Structure

```
┌────────────────────────────────────────────────────────────┐
│                  SAAS Platform (Maduuka)                   │
├────────────────────────────────────────────────────────────┤
│                     CORE SYSTEM                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │ • Authentication & Authorization                  │     │
│  │ • Multi-tenant Isolation                         │     │
│  │ • User Management                                │     │
│  │ • Billing & Subscriptions                        │     │
│  │ • Audit Logs                                     │     │
│  │ • Module Registry & Feature Flags                │     │
│  └──────────────────────────────────────────────────┘     │
│                           ▲                                │
│                           │                                │
│          ┌────────────────┴────────────────┐              │
│          │                                  │              │
├──────────▼──────────┬──────────▼────────────┬─────────────┤
│  BUSINESS MODULES   │   BUSINESS MODULES    │   MODULES   │
├─────────────────────┼───────────────────────┼─────────────┤
│ 🏪 Retail Module    │ 🍽️  Restaurant Module │ 💊 Pharmacy │
│   • POS Sales       │   • Table Management  │   • Rx Mgmt │
│   • Inventory       │   • Order Management  │   • Drug DB │
│   • Invoicing       │   • Kitchen Display   │   • Scripts │
│                     │   • Reservations      │             │
├─────────────────────┼───────────────────────┼─────────────┤
│ 📦 Adv. Inventory   │ 🏨 Hospitality Module │ 📚 Library  │
│   • Stock Items     │   • Room Booking      │   • Catalog │
│   • UOM Conversion  │   • Housekeeping      │   • Lending │
│   • Multi-location  │   • Guest Management  │   • Fines   │
│   • Transfers       │                       │             │
└─────────────────────┴───────────────────────┴─────────────┘

Per-Tenant Configuration:
Tenant A: Retail + Adv. Inventory (enabled)
Tenant B: Restaurant + Hospitality (enabled)
Tenant C: Pharmacy only (enabled)
```

### Module Anatomy

Each module consists of:

```
modules/
├── advanced-inventory/
│   ├── module.config.php         # Module metadata
│   ├── permissions.php           # Module-specific permissions
│   ├── routes.php               # API endpoints
│   ├── database/
│   │   ├── schema.sql           # Module tables (tenant-scoped)
│   │   └── migrations/          # Database changes
│   ├── api/                     # Module API handlers
│   ├── views/                   # UI pages (optional)
│   ├── services/                # Business logic
│   ├── models/                  # Data models
│   └── tests/                   # Module tests
```

## Module Definition Pattern

### 1. Module Configuration

```php
// modules/advanced-inventory/module.config.php
return [
    'module_code' => 'ADV_INV',
    'name' => 'Advanced Inventory',
    'description' => 'Multi-location inventory with UOM conversions and transfers',
    'version' => '1.0.0',
    'icon' => 'bi-boxes',

    // Module dependencies (optional)
    'requires' => [],  // Empty = no dependencies
    // 'requires' => ['CORE', 'RETAIL'],  // Requires these modules

    // Module provides these features
    'features' => [
        'stock_items',
        'uom_conversions',
        'stock_transfers',
        'multi_location_inventory',
        'stock_adjustments',
    ],

    // Permissions defined by this module
    'permissions' => [
        'VIEW_INVENTORY',
        'MANAGE_STOCK',
        'APPROVE_TRANSFERS',
        'VIEW_REPORTS',
    ],

    // Database tables owned by this module
    'tables' => [
        'tbl_stock_items',
        'tbl_stock_item_uoms',
        'tbl_stock_transfers',
        'tbl_stock_adjustments',
        'tbl_inventory_transactions',
    ],

    // Navigation menu items
    'menu' => [
        [
            'label' => 'Inventory',
            'icon' => 'bi-boxes',
            'items' => [
                ['label' => 'Stock Items', 'url' => '/stock-items-catalog.php'],
                ['label' => 'UOM Conversions', 'url' => '/advanced-inventory-uom.php'],
                ['label' => 'Stock Transfers', 'url' => '/stock-transfers.php'],
            ]
        ]
    ],

    // Billing information
    'pricing' => [
        'type' => 'addon',  // 'core', 'addon', 'enterprise'
        'price_monthly' => 29.99,
        'trial_days' => 14,
    ]
];
```

### 2. Module Registry

```php
// src/ModuleRegistry.php
class ModuleRegistry {
    private $db;
    private $cacheFile = __DIR__ . '/../cache/modules.json';

    public function getAvailableModules(): array {
        // Scan modules directory
        $modules = [];
        $moduleDirs = glob(__DIR__ . '/../modules/*', GLOB_ONLYDIR);

        foreach ($moduleDirs as $dir) {
            $configFile = $dir . '/module.config.php';
            if (file_exists($configFile)) {
                $config = require $configFile;
                $modules[$config['module_code']] = $config;
            }
        }

        return $modules;
    }

    public function getEnabledModules(int $franchiseId): array {
        $stmt = $this->db->prepare('
            SELECT module_code, config
            FROM tbl_franchise_modules
            WHERE franchise_id = ? AND is_enabled = 1
        ');
        $stmt->execute([$franchiseId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function isModuleEnabled(int $franchiseId, string $moduleCode): bool {
        $stmt = $this->db->prepare('
            SELECT is_enabled
            FROM tbl_franchise_modules
            WHERE franchise_id = ? AND module_code = ?
        ');
        $stmt->execute([$franchiseId, $moduleCode]);
        return (bool) $stmt->fetchColumn();
    }
}
```

### 3. Module Access Control

```php
// src/config/auth.php

/**
 * Require module access (fails gracefully if module disabled)
 */
function requireModuleAccess(string $moduleCode): void {
    if (!isLoggedIn()) {
        header('Location: ./sign-in.php');
        exit();
    }

    $franchiseId = (int) $_SESSION['franchise_id'];

    $db = (new \App\Config\Database())->getConnection();
    $stmt = $db->prepare('
        SELECT is_enabled
        FROM tbl_franchise_modules
        WHERE franchise_id = ? AND module_code = ?
    ');
    $stmt->execute([$franchiseId, $moduleCode]);
    $enabled = $stmt->fetchColumn();

    if (!$enabled) {
        // Module not enabled for this tenant
        header('Location: ./module-not-available.php?module=' . urlencode($moduleCode));
        exit();
    }
}

/**
 * Check if module is enabled (non-blocking)
 */
function hasModuleAccess(string $moduleCode): bool {
    if (!isLoggedIn()) {
        return false;
    }

    $franchiseId = (int) $_SESSION['franchise_id'];

    $db = (new \App\Config\Database())->getConnection();
    $stmt = $db->prepare('
        SELECT is_enabled
        FROM tbl_franchise_modules
        WHERE franchise_id = ? AND module_code = ?
    ');
    $stmt->execute([$franchiseId, $moduleCode]);
    return (bool) $stmt->fetchColumn();
}
```

### 4. Page-Level Module Protection

```php
// advanced-inventory-uom.php
<?php
require_once 'src/config/auth.php';

if (!isLoggedIn()) {
    header('Location: ./sign-in.php');
    exit();
}

// CRITICAL: Require module access
requireModuleAccess('ADV_INV');
requirePermissionGlobal('VIEW_INVENTORY');

// Page continues only if module is enabled
?>
```

### Minimal Module Registry Stub (Template Mode)

Use this when scaffolding a template so UI and menu logic are already module-aware,
even before real module tables exist.

```php
// src/Modules/ModuleRegistry.php
class ModuleRegistry {
    public function getAvailableModules(): array {
        return [
            'INVENTORY' => ['label' => 'Inventory', 'menu' => '/inventory.php'],
            'SALES' => ['label' => 'Sales', 'menu' => '/sales.php'],
        ];
    }
}

// src/config/modules.php
function hasModuleAccess(string $moduleCode, int $tenantId): bool {
    return true;
}

function requireModuleAccess(string $moduleCode, int $tenantId): void {
    if (!hasModuleAccess($moduleCode, $tenantId)) {
        header('Location: /module-not-available.php');
        exit();
    }
}
```

## Module Independence Patterns

### 1. Optional Dependencies

**Problem:** Module A wants to use Module B, but Module B might be disabled.

**Solution:** Check module availability before using.

```php
// In Restaurant Module
class OrderService {
    public function createOrder(array $data) {
        // Core order creation (always works)
        $order = $this->saveOrder($data);

        // Optional: Use Advanced Inventory if enabled
        if (hasModuleAccess('ADV_INV')) {
            $this->updateInventory($order);
        } else {
            // Fallback: Use simple inventory
            $this->updateBasicStock($order);
        }

        // Optional: Send to Kitchen Display if enabled
        if (hasModuleAccess('KITCHEN_DISPLAY')) {
            $this->sendToKitchen($order);
        }

        return $order;
    }
}
```

### 2. Interface-Based Integration

**Problem:** Module A needs functionality that might come from different modules.

**Solution:** Define interfaces, modules implement them.

```php
// Core interface
interface InventoryProvider {
    public function checkStock(int $itemId, float $quantity): bool;
    public function decrementStock(int $itemId, float $quantity): void;
}

// Basic implementation (always available)
class BasicInventory implements InventoryProvider {
    public function checkStock(int $itemId, float $quantity): bool {
        // Simple stock check
    }

    public function decrementStock(int $itemId, float $quantity): void {
        // Simple decrement
    }
}

// Advanced module implementation (optional)
class AdvancedInventory implements InventoryProvider {
    public function checkStock(int $itemId, float $quantity): bool {
        // Multi-location, UOM-aware check
    }

    public function decrementStock(int $itemId, float $quantity): void {
        // Multi-location, UOM-aware decrement with audit trail
    }
}

// Factory selects implementation based on enabled modules
class InventoryFactory {
    public static function create(): InventoryProvider {
        if (hasModuleAccess('ADV_INV')) {
            return new AdvancedInventory();
        }
        return new BasicInventory();
    }
}
```

### 3. Event-Driven Communication

**Problem:** Module A wants to notify Module B when something happens, but Module B might not exist.

**Solution:** Use event system with optional listeners.

```php
// Event system (core)
class EventDispatcher {
    private static $listeners = [];

    public static function listen(string $event, callable $handler): void {
        self::$listeners[$event][] = $handler;
    }

    public static function dispatch(string $event, array $data = []): void {
        if (!isset(self::$listeners[$event])) {
            return; // No listeners, no problem
        }

        foreach (self::$listeners[$event] as $handler) {
            try {
                $handler($data);
            } catch (\Exception $e) {
                // Log error but don't break other listeners
                error_log("Event handler failed: " . $e->getMessage());
            }
        }
    }
}

// Module A (always enabled)
class SalesModule {
    public function completeSale(Sale $sale) {
        // Complete sale logic
        $this->saveSale($sale);

        // Notify anyone listening (optional)
        EventDispatcher::dispatch('sale.completed', ['sale' => $sale]);
    }
}

// Module B (optional - Advanced Inventory)
// modules/advanced-inventory/bootstrap.php
if (hasModuleAccess('ADV_INV')) {
    EventDispatcher::listen('sale.completed', function($data) {
        $inventoryService = new InventoryService();
        $inventoryService->decrementStock($data['sale']);
    });
}

// Module C (optional - Loyalty)
// modules/loyalty/bootstrap.php
if (hasModuleAccess('LOYALTY')) {
    EventDispatcher::listen('sale.completed', function($data) {
        $loyaltyService = new LoyaltyService();
        $loyaltyService->awardPoints($data['sale']);
    });
}
```

## Database Design for Modular SAAS

### 1. Module Tables

**Each module owns its tables:**

```sql
-- Core tables (always present)
CREATE TABLE tbl_users (...);
CREATE TABLE tbl_franchises (...);
CREATE TABLE tbl_permissions (...);

-- Advanced Inventory module tables
CREATE TABLE tbl_stock_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    franchise_id BIGINT NOT NULL,  -- Tenant isolation
    name VARCHAR(255) NOT NULL,
    -- ... other fields
    FOREIGN KEY (franchise_id) REFERENCES tbl_franchises(id)
);

CREATE TABLE tbl_stock_item_uoms (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    stock_item_id BIGINT NOT NULL,
    -- ... other fields
    FOREIGN KEY (stock_item_id) REFERENCES tbl_stock_items(id) ON DELETE CASCADE
);

-- Restaurant module tables
CREATE TABLE tbl_restaurant_tables (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    franchise_id BIGINT NOT NULL,
    table_number VARCHAR(50) NOT NULL,
    -- ... other fields
    FOREIGN KEY (franchise_id) REFERENCES tbl_franchises(id)
);
```

### 2. Module Registry Table

```sql
-- Track available modules
CREATE TABLE tbl_modules (
    module_code VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(20),
    is_core BOOLEAN DEFAULT 0,  -- Core modules cannot be disabled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Track which modules are enabled per tenant
CREATE TABLE tbl_franchise_modules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    franchise_id BIGINT NOT NULL,
    module_code VARCHAR(50) NOT NULL,
    is_enabled BOOLEAN DEFAULT 1,
    enabled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    disabled_at TIMESTAMP NULL,
    config JSON,  -- Module-specific settings
    UNIQUE KEY (franchise_id, module_code),
    FOREIGN KEY (franchise_id) REFERENCES tbl_franchises(id),
    FOREIGN KEY (module_code) REFERENCES tbl_modules(module_code)
);

-- Billing for modules
CREATE TABLE tbl_franchise_module_subscriptions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    franchise_id BIGINT NOT NULL,
    module_code VARCHAR(50) NOT NULL,
    status ENUM('trial', 'active', 'cancelled', 'expired') DEFAULT 'trial',
    trial_ends_at TIMESTAMP NULL,
    next_billing_date DATE,
    price_monthly DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (franchise_id) REFERENCES tbl_franchises(id),
    FOREIGN KEY (module_code) REFERENCES tbl_modules(module_code)
);
```

### 3. Cross-Module References (Safe Pattern)

**Problem:** Module A table references Module B table, but Module B might be disabled.

**Solution:** Use nullable foreign keys with soft references.

```sql
-- Sales table (core/retail module)
CREATE TABLE tbl_sales (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    franchise_id BIGINT NOT NULL,

    -- Safe reference to optional module
    restaurant_table_id BIGINT NULL,  -- Nullable!

    -- Don't use FK if target module is optional
    -- FOREIGN KEY (restaurant_table_id) REFERENCES tbl_restaurant_tables(id)

    -- Instead, check at application level:
    -- if (hasModuleAccess('RESTAURANT') && $tableId) { validate($tableId); }
);
```

## UI/UX for Modular Systems

### 1. Dynamic Navigation

**Menu constraints (Required):**

- Keep navigation minimal and job-focused.
- Each menu may have **max 5 submenus**.
- Each submenu may have **max 6 items**.
- If more items are needed, add **one** extra submenu level (no deeper).
- Use Bootstrap Icons on **all** headings and entries (`bi-*`).
- Prefer fewer pages: group related features into one screen with permissioned sections.

```php
// includes/topbar.php
<?php
$enabledModules = getEnabledModules($_SESSION['franchise_id']);
?>

<nav>
    <!-- Core navigation always visible -->
    <a href="/dashboard.php">Dashboard</a>
    <a href="/settings.php">Settings</a>

    <!-- Module-specific navigation -->
    <?php if (hasModuleAccess('RETAIL')): ?>
        <a href="/pos-sales.php">POS</a>
        <a href="/invoices.php">Invoices</a>
    <?php endif; ?>

    <?php if (hasModuleAccess('ADV_INV')): ?>
        <div class="dropdown">
            <a href="#">Inventory</a>
            <ul>
                <li><a href="/stock-items-catalog.php">Stock Items</a></li>
                <li><a href="/advanced-inventory-uom.php">UOM Conversions</a></li>
                <li><a href="/stock-transfers.php">Transfers</a></li>
            </ul>
        </div>
    <?php endif; ?>

    <?php if (hasModuleAccess('RESTAURANT')): ?>
        <a href="/restaurant-orders.php">Orders</a>
        <a href="/tables.php">Tables</a>
    <?php endif; ?>
</nav>
```

### 2. Module Marketplace UI

```php
// modules-marketplace.php
<?php
requirePermissionGlobal('MANAGE_BILLING');  // Only owners can enable modules

$availableModules = getAvailableModules();
$enabledModules = getEnabledModules($_SESSION['franchise_id']);
?>

<h2>Available Modules</h2>

<?php foreach ($availableModules as $code => $module): ?>
    <?php $isEnabled = in_array($code, array_column($enabledModules, 'module_code')); ?>

    <div class="module-card <?= $isEnabled ? 'enabled' : '' ?>">
        <i class="<?= $module['icon'] ?>"></i>
        <h3><?= $module['name'] ?></h3>
        <p><?= $module['description'] ?></p>

        <?php if ($module['pricing']['type'] === 'core'): ?>
            <span class="badge bg-blue">Included</span>
        <?php else: ?>
            <p class="price">$<?= $module['pricing']['price_monthly'] ?>/month</p>
        <?php endif; ?>

        <?php if (!$isEnabled): ?>
            <button onclick="enableModule('<?= $code ?>')">
                Enable (<?= $module['pricing']['trial_days'] ?> day trial)
            </button>
        <?php else: ?>
            <button disabled>Enabled</button>
            <button onclick="disableModule('<?= $code ?>')" class="btn-danger">
                Disable
            </button>
        <?php endif; ?>
    </div>
<?php endforeach; ?>
```

### 3. Feature Not Available Page

```php
// module-not-available.php
<?php
$moduleCode = $_GET['module'] ?? 'UNKNOWN';
$moduleName = getModuleName($moduleCode);
?>

<div class="text-center py-5">
    <i class="bi bi-lock-fill" style="font-size: 4rem; color: #ccc;"></i>
    <h2>Module Not Available</h2>
    <p>The <strong><?= $moduleName ?></strong> module is not enabled for your account.</p>

    <a href="/modules-marketplace.php" class="btn btn-primary">
        View Available Modules
    </a>
    <a href="/dashboard.php" class="btn btn-secondary">
        Back to Dashboard
    </a>
</div>
```

## Module Lifecycle Management

### 1. Enabling a Module

```php
// api/modules.php?action=enable
public function enableModule(int $franchiseId, string $moduleCode): array {
    // 1. Validate module exists
    $moduleConfig = $this->moduleRegistry->getModule($moduleCode);
    if (!$moduleConfig) {
        return ['success' => false, 'message' => 'Module not found'];
    }

    // 2. Check dependencies
    foreach ($moduleConfig['requires'] as $requiredModule) {
        if (!$this->isModuleEnabled($franchiseId, $requiredModule)) {
            return [
                'success' => false,
                'message' => "Requires {$requiredModule} module to be enabled first"
            ];
        }
    }

    // 3. Run module migrations (create tables)
    $this->runModuleMigrations($moduleCode);

    // 4. Enable module
    $stmt = $this->db->prepare('
        INSERT INTO tbl_franchise_modules
        (franchise_id, module_code, is_enabled)
        VALUES (?, ?, 1)
        ON DUPLICATE KEY UPDATE
            is_enabled = 1,
            enabled_at = CURRENT_TIMESTAMP
    ');
    $stmt->execute([$franchiseId, $moduleCode]);

    // 5. Create trial subscription
    $this->createTrialSubscription($franchiseId, $moduleCode);

    // 6. Audit log
    auditLog('MODULE_ENABLED', [
        'franchise_id' => $franchiseId,
        'module_code' => $moduleCode
    ]);

    return ['success' => true, 'message' => 'Module enabled'];
}
```

### 2. Disabling a Module

```php
public function disableModule(int $franchiseId, string $moduleCode): array {
    // 1. Check if other modules depend on this
    $dependentModules = $this->getDependentModules($franchiseId, $moduleCode);
    if (!empty($dependentModules)) {
        return [
            'success' => false,
            'message' => 'Cannot disable. Required by: ' . implode(', ', $dependentModules)
        ];
    }

    // 2. Don't delete data, just disable access
    $stmt = $this->db->prepare('
        UPDATE tbl_franchise_modules
        SET is_enabled = 0, disabled_at = CURRENT_TIMESTAMP
        WHERE franchise_id = ? AND module_code = ?
    ');
    $stmt->execute([$franchiseId, $moduleCode]);

    // 3. Cancel subscription
    $this->cancelSubscription($franchiseId, $moduleCode);

    // 4. Audit log
    auditLog('MODULE_DISABLED', [
        'franchise_id' => $franchiseId,
        'module_code' => $moduleCode
    ]);

    return ['success' => true, 'message' => 'Module disabled'];
}
```

### 3. Data Retention After Disable

**Important:** Never delete module data when module is disabled!

```php
// When module is disabled:
// ✅ GOOD: Keep data, disable access
UPDATE tbl_franchise_modules SET is_enabled = 0 WHERE ...;
// User can re-enable and data is still there

// ❌ BAD: Delete data
DELETE FROM tbl_stock_items WHERE franchise_id = ?;
// User loses all data if they re-enable!
```

## Testing Modular Systems

### 1. Module Isolation Tests

```php
class AdvancedInventoryModuleTest extends TestCase {
    public function testModuleWorksIndependently() {
        // Enable only Advanced Inventory
        $this->enableModule('ADV_INV');
        $this->disableModule('RESTAURANT');
        $this->disableModule('PHARMACY');

        // Should work without other modules
        $stockItem = $this->createStockItem(['name' => 'Test Item']);
        $this->assertNotNull($stockItem);

        $uom = $this->createUOMConversion($stockItem->id, 'Gram', 0.001);
        $this->assertNotNull($uom);
    }

    public function testModuleAccessControl() {
        // Disable module
        $this->disableModule('ADV_INV');

        // Accessing module page should redirect
        $response = $this->get('/advanced-inventory-uom.php');
        $this->assertRedirect('/module-not-available.php');
    }
}
```

### 2. Cross-Module Integration Tests

```php
public function testRestaurantWithInventoryIntegration() {
    // Enable both modules
    $this->enableModule('RESTAURANT');
    $this->enableModule('ADV_INV');

    // Create stock item
    $stockItem = $this->createStockItem(['name' => 'Tomato']);

    // Create restaurant order using stock item
    $order = $this->createRestaurantOrder([
        'items' => [['stock_item_id' => $stockItem->id, 'qty' => 2]]
    ]);

    // Verify inventory was decremented
    $this->assertEquals($stockItem->quantity - 2, $this->getStockQuantity($stockItem->id));
}

public function testRestaurantWithoutInventory() {
    // Enable only Restaurant
    $this->enableModule('RESTAURANT');
    $this->disableModule('ADV_INV');

    // Create order (should use basic inventory)
    $order = $this->createRestaurantOrder([
        'items' => [['product_id' => 1, 'qty' => 2]]
    ]);

    // Should work without Advanced Inventory
    $this->assertNotNull($order);
}
```

## Best Practices

### DO ✅

**Module Design:**

- Keep modules self-contained (own tables, own logic)
- Use feature flags for module checks (`hasModuleAccess()`)
- Provide fallback when optional modules are disabled
- Version module APIs for backward compatibility
- Document module dependencies clearly

**Database:**

- Always include `franchise_id` for tenant isolation
- Use migrations for module schema changes
- Keep data when module is disabled (soft delete)
- Use nullable FKs for cross-module references

**Testing:**

- Test module works independently
- Test graceful degradation when dependencies missing
- Test re-enabling after disable (data preserved)
- Test billing/subscription flow

### DON'T ❌

**Module Design:**

- Don't hard-code module dependencies (check at runtime)
- Don't break core features when module disabled
- Don't expose module internals to other modules
- Don't assume module is always enabled

**Database:**

- Don't delete module data on disable (user may re-enable)
- Don't use hard FK constraints for optional modules
- Don't share tables between modules (coupling)
- Don't skip tenant_id in module tables

**UI/UX:**

- Don't show disabled module navigation
- Don't let users access disabled module pages
- Don't display cryptic errors (show upgrade CTA)

## Anti-Patterns

### ❌ Hard Dependencies

```php
// BAD: Assumes Advanced Inventory is always enabled
class RestaurantOrderService {
    public function createOrder($data) {
        $inventory = new AdvancedInventoryService();  // Crashes if disabled!
        $inventory->decrementStock($data['items']);
    }
}
```

```php
// GOOD: Check if module is enabled
class RestaurantOrderService {
    public function createOrder($data) {
        if (hasModuleAccess('ADV_INV')) {
            $inventory = new AdvancedInventoryService();
            $inventory->decrementStock($data['items']);
        } else {
            $this->decrementBasicStock($data['items']);
        }
    }
}
```

### ❌ Circular Dependencies

```php
// BAD: Restaurant depends on Inventory, Inventory depends on Restaurant
// Restaurant Module
class OrderService {
    public function createOrder() {
        $inventory = new InventoryService();  // Restaurant → Inventory
    }
}

// Inventory Module
class InventoryService {
    public function transferStock() {
        $orders = new OrderService();  // Inventory → Restaurant
    }
}
```

```php
// GOOD: Use events to decouple
// Restaurant Module
class OrderService {
    public function createOrder() {
        EventDispatcher::dispatch('order.created', $order);
    }
}

// Inventory Module (listens to event)
EventDispatcher::listen('order.created', function($order) {
    $inventory = new InventoryService();
    $inventory->decrementStock($order);
});
```

### ❌ Deleting Data on Disable

```php
// BAD: User loses data if they disable and re-enable
public function disableModule($franchiseId, $moduleCode) {
    if ($moduleCode === 'ADV_INV') {
        $this->db->exec("DELETE FROM tbl_stock_items WHERE franchise_id = $franchiseId");
    }
}
```

```php
// GOOD: Keep data, just disable access
public function disableModule($franchiseId, $moduleCode) {
    $this->db->prepare('
        UPDATE tbl_franchise_modules
        SET is_enabled = 0
        WHERE franchise_id = ? AND module_code = ?
    ')->execute([$franchiseId, $moduleCode]);
}
```

## Summary

**Core Principles:**

1. **Module Independence**: Each module is self-contained and optional
2. **Graceful Degradation**: System works when modules are disabled
3. **Per-Tenant Control**: Each tenant enables only needed modules
4. **Zero Breaking Changes**: Adding/removing modules preserves functionality
5. **Clean Interfaces**: Modules communicate through contracts

**Implementation Checklist:**

- [ ] Module config file with metadata
- [ ] Module access control (`requireModuleAccess()`)
- [ ] Optional dependency checks (`hasModuleAccess()`)
- [ ] Module registry in database
- [ ] Per-tenant module subscriptions
- [ ] Dynamic navigation based on enabled modules
- [ ] Fallback logic when modules disabled
- [ ] Migration system for module schemas
- [ ] Billing integration for module pricing
- [ ] Tests for module isolation and integration

**Key Insight:** Build modules like Lego blocks—each piece works independently, but they snap together perfectly to create more powerful features.
