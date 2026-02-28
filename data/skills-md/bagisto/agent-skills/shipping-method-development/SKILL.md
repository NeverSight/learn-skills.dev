---
name: shipping-method-development
description: "Shipping method development in Bagisto. Activates when creating shipping methods, integrating shipping carriers like FedEx, UPS, DHL, or any third-party shipping provider; or when the user mentions shipping, shipping method, shipping carrier, delivery, or needs to add a new shipping option to checkout."
license: MIT
metadata:
  author: bagisto
---

# Shipping Method Development

## Overview

Creating custom shipping methods in Bagisto allows you to tailor delivery options to meet your specific business needs. Whether you need special handling for fragile items, express delivery options, or region-specific shipping rules, custom shipping methods provide the flexibility your e-commerce store requires.

For our tutorial, we'll create a **Custom Express Shipping** method that demonstrates all the essential concepts you need to build any type of shipping solution.

## When to Apply

Activate this skill when:
- Creating new shipping methods
- Integrating shipping carriers (FedEx, UPS, DHL, USPS, etc.)
- Adding shipping options to checkout
- Modifying existing shipping configurations
- Creating admin configuration for shipping methods
- Implementing rate calculation logic

## Bagisto Shipping Architecture

Bagisto's shipping system is built around a flexible carrier-based architecture that separates configuration from business logic.

### Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Carriers Configuration** | Defines shipping method properties | `Config/carriers.php` |
| **Carrier Classes** | Contains rate calculation logic | `Carriers/ClassName.php` |
| **System Configuration** | Admin interface forms | `Config/system.php` |
| **Service Provider** | Registers shipping method | `Providers/ServiceProvider.php` |
| **Shipping Facade** | Collects and manages rates | `Webkul\Shipping\Shipping` |

### Key Features

- **Flexible Rate Calculation**: Support for per-unit, per-order, weight-based, or custom pricing.
- **Configuration Management**: Admin-friendly settings interface.
- **Multi-channel Support**: Different rates and settings per sales channel.
- **Localization Ready**: Full translation support.
- **Extensible Architecture**: Easy integration with third-party APIs.

## Step-by-Step Guide

### Step 1: Create Package Directory Structure

```bash
mkdir -p packages/Webkul/CustomExpressShipping/src/{Carriers,Config,Providers}
```

### Step 2: Create Carrier Configuration

**File:** `packages/Webkul/CustomExpressShipping/src/Config/carriers.php`

```php
<?php

return [
    'custom_express_shipping' => [
        'code'         => 'custom_express_shipping',
        'title'        => 'Express Delivery (1-2 Days)',
        'description'  => 'Premium express shipping with tracking',
        'active'       => true,
        'default_rate' => '19.99',
        'type'         => 'per_order',
        'class'        => 'Webkul\CustomExpressShipping\Carriers\CustomExpressShipping',
    ],
];
```

#### Configuration Properties Explained

| Property | Type | Purpose | Description |
|----------|------|---------|-------------|
| **`code`** | String | Unique identifier | Must match the array key and `$code` property in carrier class. |
| **`title`** | String | Default display name | Shown to customers during checkout (can be overridden in admin). |
| **`description`** | String | Method description | Brief explanation of the shipping service. |
| **`active`** | Boolean | Default status | Whether the shipping method is enabled by default. |
| **`default_rate`** | String/Float | Base shipping cost | Base shipping cost before calculations. |
| **`type`** | String | Pricing model | `per_order` (flat rate) or `per_unit` (per item). |
| **`class`** | String | Carrier class namespace | Full path to your carrier class. |

> **Note:** The array key (`custom_express_shipping`) must match the `code` property in your carrier class, system configuration key path, and should be consistent throughout.

### Step 3: Create Carrier Class

**File:** `packages/Webkul/CustomExpressShipping/src/Carriers/CustomExpressShipping.php`

```php
<?php

namespace Webkul\CustomExpressShipping\Carriers;

use Webkul\Shipping\Carriers\AbstractShipping;
use Webkul\Checkout\Models\CartShippingRate;
use Webkul\Checkout\Facades\Cart;

class CustomExpressShipping extends AbstractShipping
{
    /**
     * Shipping method code - must match carriers.php key.
     *
     * @var string
     */
    protected $code = 'custom_express_shipping';

    /**
     * Shipping method code.
     *
     * @var string
     */
    protected $method = 'custom_express_shipping_custom_express_shipping';

    /**
     * Calculate shipping rate for the current cart.
     *
     * @return \Webkul\Checkout\Models\CartShippingRate|false
     */
    public function calculate()
    {
        if (! $this->isAvailable()) {
            return false;
        }

        return $this->getRate();
    }

    /**
     * Get shipping rate.
     *
     * @return \Webkul\Checkout\Models\CartShippingRate
     */
    public function getRate(): CartShippingRate
    {
        $cart = Cart::getCart();

        $cartShippingRate = new CartShippingRate;

        $cartShippingRate->carrier = $this->getCode();
        $cartShippingRate->carrier_title = $this->getConfigData('title');
        $cartShippingRate->method = $this->getMethod();
        $cartShippingRate->method_title = $this->getConfigData('title');
        $cartShippingRate->method_description = $this->getConfigData('description');
        $cartShippingRate->price = 0;
        $cartShippingRate->base_price = 0;

        $baseRate = (float) $this->getConfigData('default_rate');

        if ($this->getConfigData('type') == 'per_unit') {
            foreach ($cart->items as $item) {
                if ($item->getTypeInstance()->isStockable()) {
                    $cartShippingRate->price += core()->convertPrice($baseRate) * $item->quantity;
                    $cartShippingRate->base_price += $baseRate * $item->quantity;
                }
            }
        } else {
            $cartShippingRate->price = core()->convertPrice($baseRate);
            $cartShippingRate->base_price = $baseRate;
        }

        return $cartShippingRate;
    }
}
```

### Step 4: Create System Configuration

**File:** `packages/Webkul/CustomExpressShipping/src/Config/system.php`

```php
<?php

return [
    [
        'key'    => 'sales.carriers.custom_express_shipping',
        'name'   => 'Custom Express Shipping',
        'info'   => 'Configure the Custom Express Shipping method settings.',
        'sort'   => 1,
        'fields' => [
            [
                'name'          => 'title',
                'title'         => 'Method Title',
                'type'          => 'text',
                'validation'    => 'required',
                'channel_based' => true,
                'locale_based'  => true,
            ],
            [
                'name'          => 'description',
                'title'         => 'Description',
                'type'          => 'textarea',
                'channel_based' => true,
                'locale_based'  => false,
            ],
            [
                'name'          => 'default_rate',
                'title'         => 'Base Rate',
                'type'          => 'text',
                'validation'    => 'required|numeric|min:0',
                'channel_based' => true,
                'locale_based'  => false,
            ],
            [
                'name'          => 'type',
                'title'         => 'Pricing Type',
                'type'          => 'select',
                'options'       => [
                    [
                        'title' => 'Per Order (Flat Rate)',
                        'value' => 'per_order',
                    ],
                    [
                        'title' => 'Per Item',
                        'value' => 'per_unit',
                    ],
                ],
                'channel_based' => true,
                'locale_based'  => false,
            ],
            [
                'name'          => 'active',
                'title'         => 'Enabled',
                'type'          => 'boolean',
                'validation'    => 'required',
                'channel_based' => true,
                'locale_based'  => false,
            ],
        ],
    ],
];
```

#### System Configuration Field Properties

| Property | Purpose | Description |
|----------|---------|-------------|
| **`name`** | Field identifier | Used to store and retrieve configuration values. |
| **`title`** | Field label | Label displayed in the admin form. |
| **`type`** | Input type | `text`, `textarea`, `boolean`, `select`, `password`, etc. |
| **`default_value`** | Default setting | Initial value when first configured. |
| **`channel_based`** | Multi-store support | Different values per sales channel. |
| **`locale_based`** | Multi-language support | Translatable content per language. |
| **`validation`** | Field validation | Rules like `required`, `numeric`, `email`. |

### Step 5: Create Service Provider

**File:** `packages/Webkul/CustomExpressShipping/src/Providers/CustomExpressShippingServiceProvider.php`

```php
<?php

namespace Webkul\CustomExpressShipping\Providers;

use Illuminate\Support\ServiceProvider;

class CustomExpressShippingServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     *
     * @return void
     */
    public function register(): void
    {
        $this->mergeConfigFrom(
            dirname(__DIR__) . '/Config/carriers.php',
            'carriers'
        );

        $this->mergeConfigFrom(
            dirname(__DIR__) . '/Config/system.php',
            'core'
        );
    }

    /**
     * Bootstrap services.
     *
     * @return void
     */
    public function boot(): void
    {
        //
    }
}
```

### Step 6: Register Your Package

1. **Add to composer.json** (in Bagisto root directory):

```json
{
    "autoload": {
        "psr-4": {
            "Webkul\\CustomExpressShipping\\": "packages/Webkul/CustomExpressShipping/src"
        }
    }
}
```

2. **Update autoloader:**

```bash
composer dump-autoload
```

3. **Register service provider** in `bootstrap/providers.php`:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,

    // ... other providers ...

    Webkul\CustomExpressShipping\Providers\CustomExpressShippingServiceProvider::class,
];
```

4. **Clear caches:**

```bash
php artisan optimize:clear
```

## Base Carrier Class Reference

**Location:** `packages/Webkul/Shipping/src/Carriers/AbstractShipping.php`

All shipping methods extend `Webkul\Shipping\Carriers\AbstractShipping`:

```php
<?php

namespace Webkul\Shipping\Carriers;

use Webkul\Shipping\Exceptions\CarrierCodeException;

abstract class AbstractShipping
{
    /**
     * Shipping method carrier code.
     *
     * @var string
     */
    protected $code;

    /**
     * Shipping method code.
     *
     * @var string
     */
    protected $method;

    abstract public function calculate();

    /**
     * Checks if shipping method is available.
     *
     * @return array
     */
    public function isAvailable()
    {
        return $this->getConfigData('active');
    }

    /**
     * Returns shipping method carrier code.
     *
     * @return string
     */
    public function getCode()
    {
        if (empty($this->code)) {
            throw new CarrierCodeException('Carrier code should be initialized.');
        }

        return $this->code;
    }

    /**
     * Return shipping method code.
     *
     * @return string
     */
    public function getMethod()
    {
        if (empty($this->method)) {
            $code = $this->getCode();

            return $code . '_' . $code;
        }

        return $this->method;
    }

    /**
     * Returns shipping method title.
     *
     * @return array
     */
    public function getTitle()
    {
        return $this->getConfigData('title');
    }

    /**
     * Returns shipping method description.
     *
     * @return array
     */
    public function getDescription()
    {
        return $this->getConfigData('description');
    }

    /**
     * Retrieve information from shipping configuration.
     *
     * @param  string  $field
     * @return mixed
     */
    public function getConfigData($field)
    {
        return core()->getConfigData('sales.carriers.' . $this->getCode() . '.' . $field);
    }
}
```

## CartShippingRate Model

**Location:** `packages/Webkul/Checkout/src/Models/CartShippingRate.php`

```php
<?php

namespace Webkul\Checkout\Models;

use Illuminate\Database\Eloquent\Model;
use Webkul\Checkout\Contracts\CartShippingRate as CartShippingRateContract;

class CartShippingRate extends Model implements CartShippingRateContract
{
    protected $fillable = [
        'carrier',
        'carrier_title',
        'method',
        'method_title',
        'method_description',
        'price',
        'base_price',
        'discount_amount',
        'base_discount_amount',
        'tax_percent',
        'tax_amount',
        'base_tax_amount',
        'price_incl_tax',
        'base_price_incl_tax',
        'applied_tax_rate',
    ];
}
```

## Key Methods to Implement

| Method | Purpose | Required |
|--------|---------|----------|
| `calculate()` | Calculate and return shipping rate | Yes (abstract) |
| `getRate()` | Build CartShippingRate object | No (can be inline) |
| `isAvailable()` | Override for custom availability | No (uses default) |

## Built-in Shipping Methods

- **FlatRate**: `packages/Webkul/Shipping/src/Carriers/FlatRate.php`
- **Free**: `packages/Webkul/Shipping/src/Carriers/Free.php`

## Pricing Examples

### Fixed Rate Shipping

```php
public function calculate()
{
    if (! $this->isAvailable()) {
        return false;
    }

    $cartShippingRate = new CartShippingRate;
    $cartShippingRate->carrier = $this->getCode();
    $cartShippingRate->carrier_title = $this->getConfigData('title');
    $cartShippingRate->method = $this->getMethod();
    $cartShippingRate->method_title = $this->getConfigData('title');
    $cartShippingRate->method_description = $this->getConfigData('description');
    $cartShippingRate->price = 15.99;
    $cartShippingRate->base_price = 15.99;

    return $cartShippingRate;
}
```

### Weight-Based Pricing

```php
public function calculate()
{
    if (! $this->isAvailable()) {
        return false;
    }

    $cart = Cart::getCart();
    $baseRate = 5.00;
    $perKg = 2.50;

    $price = $baseRate + ($cart->weight * $perKg);

    $cartShippingRate = new CartShippingRate;
    $cartShippingRate->carrier = $this->getCode();
    $cartShippingRate->carrier_title = $this->getConfigData('title');
    $cartShippingRate->method = $this->getMethod();
    $cartShippingRate->method_title = $this->getConfigData('title');
    $cartShippingRate->price = core()->convertPrice($price);
    $cartShippingRate->base_price = $price;

    return $cartShippingRate;
}
```

### Free Shipping Above Threshold

```php
public function calculate()
{
    if (! $this->isAvailable()) {
        return false;
    }

    $cart = Cart::getCart();
    $threshold = (float) $this->getConfigData('free_shipping_threshold');
    $price = $cart->sub_total >= $threshold ? 0 : (float) $this->getConfigData('default_rate');

    $cartShippingRate = new CartShippingRate;
    $cartShippingRate->carrier = $this->getCode();
    $cartShippingRate->carrier_title = $this->getConfigData('title');
    $cartShippingRate->method = $this->getMethod();
    $cartShippingRate->method_title = $this->getConfigData('title');
    $cartShippingRate->price = core()->convertPrice($price);
    $cartShippingRate->base_price = $price;

    return $cartShippingRate;
}
```

## Shipping Facade

**Location:** `packages/Webkul/Shipping/src/Shipping.php`

The Shipping facade manages rate collection and processing:

```php
class Shipping
{
    public function collectRates()
    {
        // Iterates through all carriers and calls calculate()
        // Returns grouped shipping methods with rates
    }

    public function getGroupedAllShippingRates()
    {
        // Returns rates grouped by carrier
    }

    public function getShippingMethods()
    {
        // Returns available shipping methods
    }
}
```

## Package Structure

```
packages
└── Webkul
    └── CustomExpressShipping
        └── src
            ├── Carriers
            │   └── CustomExpressShipping.php         # Rate calculation logic
            ├── Config
            │   ├── carriers.php                     # Shipping method definition
            │   └── system.php                        # Admin configuration
            └── Providers
                └── CustomExpressShippingServiceProvider.php  # Registration
```

## Testing

Shipping methods can be tested through the checkout flow. Test:
- Method appears in checkout when enabled
- Rate calculation is correct
- Admin configuration saves properly
- Method respects enabled/disabled status

## Key Files Reference

| File | Purpose |
|------|---------|
| `packages/Webkul/Shipping/src/Carriers/AbstractShipping.php` | Base abstract class |
| `packages/Webkul/Shipping/src/Carriers/FlatRate.php` | Flat rate shipping example |
| `packages/Webkul/Shipping/src/Carriers/Free.php` | Free shipping example |
| `packages/Webkul/Shipping/src/Config/carriers.php` | Default carriers config |
| `packages/Webkul/Shipping/src/Shipping.php` | Shipping facade |
| `packages/Webkul/Checkout/src/Models/CartShippingRate.php` | Shipping rate model |
| `packages/Webkul/Admin/src/Config/system.php` | Admin config (carrier sections) |

## Common Pitfalls

- Forgetting to merge config in service provider
- Not matching `$code` property with config array key
- Not registering service provider in `bootstrap/providers.php`
- Forgetting to run `composer dump-autoload` after adding package
- Not clearing cache after configuration changes
- Not using `core()->convertPrice()` for multi-currency support
- Not checking `isStockable()` for per-item calculations
- Not following PHPDoc conventions with proper punctuation
