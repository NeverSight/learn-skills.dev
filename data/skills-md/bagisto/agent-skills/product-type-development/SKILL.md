---
name: product-type-development
description: "Product type development in Bagisto. Activates when creating custom product types, defining product behaviors, or implementing specialized product logic. Use references: @config (product type configuration), @abstract (AbstractType methods), @build (complete subscription implementation)."
license: MIT
metadata:
  author: bagisto
  references:
    - config: Product type configuration
    - abstract: AbstractType methods and properties
    - build: Complete subscription implementation
---

# Product Type Development in Bagisto

## Overview

Creating custom product types in Bagisto allows you to define specialized product behaviors that match your business needs. Whether you need subscription products, rental items, digital services, or complex product variations, custom product types provide the flexibility to create exactly what your store requires.

## When to Apply

Activate this skill when:
- Creating new product types in Bagisto
- Building subscription or service-based products
- Implementing custom product behaviors
- Adding type-specific validation and pricing
- Modifying inventory/stock handling

---

# @config: Product Type Configuration

## Basic Configuration Structure

The `Config/product-types.php` file is a simple PHP array that registers your product type:

```php
<?php

return [
    'subscription' => [
        'key'   => 'subscription',
        'name'  => 'Subscription',
        'class' => 'Webkul\SubscriptionProduct\Type\Subscription',
        'sort'  => 5,
    ],
];
```

## Required Configuration Properties

| Property | Description | Example |
|----------|-------------|---------|
| `key` | Unique identifier (matches array key) | `'subscription'` |
| `name` | Display name in admin dropdown | `'Subscription'` |
| `class` | Full namespace to your product type class | `'Webkul\SubscriptionProduct\Type\Subscription'` |
| `sort` | Order in dropdown (optional, default: 0) | `5` |

## How Bagisto Uses This Configuration

### 1. Admin Product Creation
- Reads all registered product types from configuration
- Shows them in the "Product Type" dropdown
- Uses the `name` for display and `sort` for ordering

### 2. Product Type Instantiation
- Looks up the product's type using the `key`
- Creates an instance of the `class`
- Calls methods on that instance for product behavior

### 3. Configuration Loading
Your service provider merges your configuration:

```php
public function register(): void
{
    $this->mergeConfigFrom(
        dirname(__DIR__) . '/Config/product-types.php',
        'product_types'
    );
}
```

## Multiple Product Types

```php
<?php

return [
    'subscription' => [
        'key'   => 'subscription',
        'name'  => 'Subscription',
        'class' => 'Webkul\SubscriptionProduct\Type\Subscription',
        'sort'  => 5,
    ],
    
    'rental' => [
        'key'   => 'rental',
        'name'  => 'Rental Product',
        'class' => 'Webkul\RentalProduct\Type\Rental',
        'sort'  => 6,
    ],
];
```

---

# @abstract: AbstractType Methods

## AbstractType Overview

Every product type in Bagisto extends the `AbstractType` class:

```php
<?php

namespace Webkul\Product\Type;

abstract class AbstractType
{
    protected $product;
    protected $isStockable = true;
    protected $showQuantityBox = false;
    protected $haveSufficientQuantity = true;
    protected $canBeMovedFromWishlistToCart = true;
    protected $additionalViews = [];
    protected $skipAttributes = [];
}
```

## Key Methods to Override

### Product Availability Control

#### `isSaleable(): bool`

Controls whether the product appears as purchasable:

```php
public function isSaleable(): bool
{
    if (! parent::isSaleable()) {
        return false;
    }
    
    // Add custom availability logic
    return true;
}
```

#### `haveSufficientQuantity(int $qty): bool`

Checks if enough quantity is available:

```php
public function haveSufficientQuantity(int $qty): bool
{
    return true; // Custom logic based on subscription slots
}
```

### Inventory and Stock Control

#### `isStockable(): bool`

Determines if the product uses inventory tracking:

```php
public function isStockable(): bool
{
    return false; // Subscriptions don't use traditional inventory
}
```

#### `totalQuantity(): int`

Returns total available quantity:

```php
public function totalQuantity(): int
{
    return $this->product->subscription_slots ?? 0;
}
```

### User Interface Control

#### `showQuantityBox(): bool`

Controls whether quantity input appears:

```php
public function showQuantityBox(): bool
{
    return true;
}
```

### Pricing Methods

#### `getProductPrices(): array`

Returns structured pricing data:

```php
public function getProductPrices(): array
{
    $basePrice = $this->product->price;
    $discount = $this->product->subscription_discount ?? 0;
    $finalPrice = $basePrice - ($basePrice * $discount / 100);
    
    return [
        'regular' => [
            'price' => core()->convertPrice($basePrice),
            'formatted_price' => core()->currency($basePrice),
        ],
        'final' => [
            'price' => core()->convertPrice($finalPrice),
            'formatted_price' => core()->currency($finalPrice),
        ],
    ];
}
```

#### `getPriceHtml(): string`

Generates price HTML for display:

```php
public function getPriceHtml(): string
{
    return view('subscription::products.prices.subscription', [
        'product' => $this->product,
        'prices' => $this->getProductPrices(),
    ])->render();
}
```

### Validation Methods

#### `getTypeValidationRules(): array`

Returns validation rules for product type specific fields:

```php
public function getTypeValidationRules(): array
{
    return [
        'subscription_frequency' => 'required|in:weekly,monthly,quarterly,yearly',
        'subscription_discount' => 'nullable|numeric|min:0|max:100',
        'subscription_duration' => 'nullable|integer|min:1',
        'subscription_slots' => 'required|integer|min:1',
    ];
}
```

### Admin Interface Customization

#### `$additionalViews` Property

Specifies additional blade views in product edit page:

```php
protected $additionalViews = [
    'subscription::admin.catalog.products.edit.subscription-settings',
    'subscription::admin.catalog.products.edit.subscription-pricing',
];
```

#### `$skipAttributes` Property

Specifies which attributes to skip:

```php
protected $skipAttributes = [
    'weight',
    'dimensions',
];
```

### Cart Integration

#### `prepareForCart(array $data): array`

Processes product data before adding to cart:

```php
public function prepareForCart(array $data): array
{
    if (empty($data['subscription_frequency'])) {
        return 'Please select subscription frequency.';
    }
    
    $cartData = parent::prepareForCart($data);
    
    $cartData[0]['additional']['subscription_frequency'] = $data['subscription_frequency'];
    $cartData[0]['additional']['subscription_start_date'] = $data['start_date'] ?? now()->addDays(1)->format('Y-m-d');
    
    return $cartData;
}
```

---

# @build: Complete Subscription Implementation

## Package Structure

```
packages/Webkul/SubscriptionProduct/
└── src/
    ├── Type/
    │   └── Subscription.php
    ├── Config/
    │   └── product-types.php
    └── Providers/
        └── SubscriptionServiceProvider.php
```

## Step 1: Create Package Structure

```bash
mkdir -p packages/Webkul/SubscriptionProduct/src/{Type,Config,Providers}
```

## Step 2: Configure Product Type

**File:** `packages/Webkul/SubscriptionProduct/src/Config/product-types.php`

```php
<?php

return [
    'subscription' => [
        'key'   => 'subscription',
        'name'  => 'Subscription',
        'class' => 'Webkul\SubscriptionProduct\Type\Subscription',
        'sort'  => 5,
    ],
];
```

## Step 3: Create Product Type Class

**File:** `packages/Webkul/SubscriptionProduct/src/Type/Subscription.php`

```php
<?php

namespace Webkul\SubscriptionProduct\Type;

use Webkul\Product\Helpers\Indexers\Price\Simple as SimpleIndexer;
use Webkul\Product\Type\AbstractType;

class Subscription extends AbstractType
{
    public function getPriceIndexer()
    {
        return app(SimpleIndexer::class);
    }
    
    public function isStockable(): bool
    {
        return false;
    }
    
    public function showQuantityBox(): bool
    {
        return true;
    }
    
    public function isSaleable(): bool
    {
        if (! parent::isSaleable()) {
            return false;
        }
        
        return true;
    }
    
    public function haveSufficientQuantity(int $qty): bool
    {
        return true;
    }
    
    public function totalQuantity(): int
    {
        return $this->product->subscription_slots ?? 0;
    }
    
    public function prepareForCart(array $data): array
    {
        if (empty($data['subscription_frequency'])) {
            return 'Please select subscription frequency.';
        }
        
        $cartData = parent::prepareForCart($data);
        
        $cartData[0]['additional']['subscription_frequency'] = $data['subscription_frequency'];
        $cartData[0]['additional']['subscription_start_date'] = $data['start_date'] ?? now()->addDays(1)->format('Y-m-d');
        
        return $cartData;
    }
}
```

## Step 4: Create Service Provider

**File:** `packages/Webkul/SubscriptionProduct/src/Providers/SubscriptionServiceProvider.php`

```php
<?php

namespace Webkul\SubscriptionProduct\Providers;

use Illuminate\Support\ServiceProvider;

class SubscriptionServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->mergeConfigFrom(
            dirname(__DIR__) . '/Config/product-types.php',
            'product_types'
        );
    }

    public function boot(): void
    {
        //
    }
}
```

## Step 5: Register Your Package

### Update composer.json

```json
{
    "autoload": {
        "psr-4": {
            "Webkul\\SubscriptionProduct\\": "packages/Webkul/SubscriptionProduct/src"
        }
    }
}
```

### Update autoloader

```bash
composer dump-autoload
```

### Register service provider

In `bootstrap/providers.php`:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    
    // ... other providers ...
    
    Webkul\SubscriptionProduct\Providers\SubscriptionServiceProvider::class,
];
```

### Clear cache

```bash
php artisan optimize:clear
```

## Testing

```bash
php artisan tinker

# Test product type
>>> $product = \Webkul\Product\Models\Product::where('type', 'subscription')->first()
>>> $subscription = $product->getTypeInstance()

# Test methods
>>> $subscription->isStockable()        // Should return false
>>> $subscription->showQuantityBox()    // Should return true
>>> $subscription->isSaleable()         // Should return true

# Test cart preparation
>>> $cartData = $subscription->prepareForCart(['quantity' => 2, 'subscription_frequency' => 'monthly'])
>>> $cartData[0]['additional']  // Should show subscription data
```

## Built-in Product Types Reference

| Type | Use Case | Key Features |
|------|----------|--------------|
| **Simple** | Basic products | Standard pricing, inventory tracking |
| **Configurable** | Products with variations | Variant management, attribute-based pricing |
| **Virtual** | Non-physical products | No shipping required |
| **Grouped** | Related products sold together | Bundle pricing, component selection |

## Key Files Reference

| File | Purpose |
|------|---------|
| `Config/product-types.php` | Product type registration |
| `Type/ProductType.php` | Product type class |
| `Providers/ServiceProvider.php` | Package registration |
| `packages/Webkul/Product/src/Type/AbstractType.php` | Base class |

## Common Pitfalls

- Forgetting to merge config in service provider
- Not matching `$key` with array key in configuration
- Not registering service provider in `bootstrap/providers.php`
- Forgetting to run `composer dump-autoload` after adding package
- Not clearing cache after configuration changes
- Forgetting to call `parent::isSaleable()` when overriding
- Not handling cart data correctly in `prepareForCart()`
