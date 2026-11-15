---
name: wp-woocommerce-dev
description: WooCommerce extension code review for HPOS compatibility, payment gateway security, cart optimization, and template overrides. Use when reviewing WooCommerce extension code, payment gateway development, shipping methods, custom product types, cart operations, checkout customization, or when user mentions "WooCommerce review", "WooCommerce extension", "WooCommerce plugin", "payment gateway", "shipping method", "HPOS", "High-Performance Order Storage", "wc_get_orders", "WC_Payment_Gateway", "WC_Shipping_Method", "cart fragments", "WooCommerce hooks", "WooCommerce template", "shop_order", "WooCommerce performance", "Action Scheduler", "WooCommerce REST API", "WooCommerce Blocks", "checkout block", "woocommerce_checkout". Detects HPOS issues, CRUD violations, payment security anti-patterns, performance problems, and template override mistakes in WooCommerce 8.2+ through 10.x code.
---

# WooCommerce Development Review Skill

## Overview

Systematic WooCommerce development review for WooCommerce 8.2+ through current 10.x. **Core principle:** WooCommerce has undergone a fundamental architectural shift—HPOS (High-Performance Order Storage) is default for new stores since WC 8.2 (October 2023), requiring all extensions to use CRUD APIs exclusively. Direct post access for orders is broken on modern WooCommerce installations.

Extensions must use WC_Data CRUD pattern (wc_get_order(), wc_get_orders(), WC_Order methods), Action Scheduler for background processing, and hooks-over-template-overrides for maintainability. Payment gateways must never store/log raw card data. Cart fragments must be conditionally loaded. Template overrides must preserve all action hooks.

Review validates HPOS compatibility, payment gateway security (code-level only, NOT PCI compliance audit), WooCommerce hook usage, template override quality, and performance patterns. Auto-detects WooCommerce context (extension, theme integration, payment gateway, shipping method, custom product type, WC Blocks integration) and adjusts review guidance. Report findings grouped by file with line numbers, severity labels (CRITICAL/WARNING/INFO), and BAD/GOOD code pairs.

**Note:** This skill touches all prior skills—security (payment data handling), plugin architecture (WC as extension), blocks (WC Blocks), themes (template overrides), and performance (cart fragments, queries). Cross-references provided throughout.

## When to Use

**Use when:**
- WooCommerce extension architecture review
- HPOS compatibility audit (declare_compatibility check, CRUD-only validation)
- Payment gateway code review (WC_Payment_Gateway patterns, security anti-patterns)
- Shipping method review (WC_Shipping_Method, calculate_shipping)
- Custom product type review (WC_Product extension, data stores)
- WooCommerce hook usage analysis (order lifecycle, product data, cart/checkout)
- Template override assessment (hooks preservation, version tracking)
- Cart fragments performance analysis (site-wide loading detection)
- Action Scheduler pattern review (vs wp_cron anti-patterns)
- WooCommerce REST API extension review
- WC Blocks integration check (Store API, Additional Checkout Fields API)
- Webhook security review (signature verification)

**Don't use for:**
- Generic plugin architecture (use wp-plugin-development)
- Security-only audits (use wp-security-review for comprehensive analysis)
- Block development outside WC (use wp-block-development)
- Theme-only review without WC integration (use wp-theme-development)
- Performance-only review (use wp-performance-review)
- PCI compliance auditing (out of scope—infrastructure-level)
- Store setup or hosting configuration (out of scope)

## Code Review Workflow

Follow this eight-step workflow for systematic WooCommerce reviews:

### 1. Detect WooCommerce context from file structure

**Extension/plugin:**
- Main plugin file with WC dependency check (`WooCommerce` in plugin header)
- HPOS declaration via `before_woocommerce_init` hook
- Most common context—full HPOS + CRUD + hook audit

**Theme integration:**
- woocommerce/ directory in theme with template overrides
- Template override focus with hooks-first guidance
- Cross-reference wp-theme-development for theme patterns

**Payment gateway:**
- Class extending `WC_Payment_Gateway`
- Heightened security review (never store raw cards, HTTPS check)
- Webhook verification if applicable

**Shipping method:**
- Class extending `WC_Shipping_Method`
- calculate_shipping() review, zone support, rate calculation

**Custom product type:**
- Class extending `WC_Product`
- Data store review, product type registration, class hierarchy

**WC Blocks integration:**
- Store API usage, checkout block extension points
- Additional Checkout Fields API (WC 8.6+)
- Surface-level review, suggest wp-block-development for deep block patterns

### 2. Check HPOS compatibility (WOO-16)

**CRITICAL if missing:**
- `declare_compatibility()` call in `before_woocommerce_init` hook
- Pattern to find: `add_action( 'before_woocommerce_init', ... )` with `FeaturesUtil::declare_compatibility( 'custom_order_tables', __FILE__, true )`

**CRITICAL violations:**
- `get_posts()` or `WP_Query` with `post_type='shop_order'`
- `get_post_meta()` / `update_post_meta()` for order data
- Direct `$wpdb` queries against `wp_posts` / `wp_postmeta` for orders

**WARNING violations:**
- `WP_Query` with `post_type='product'` (future-breaking—custom product tables planned)

**GOOD patterns:**
- `wc_get_order( $order_id )`
- `wc_get_orders( array( 'status' => 'completed', 'limit' => 10 ) )`
- `$order->get_meta( 'key' )`, `$order->update_meta_data( 'key', $value )`, `$order->save()`

**Compatibility mode awareness:**
- Code should work in both HPOS and legacy modes
- Use CRUD APIs exclusively—they handle both storage modes

### 3. Check data access patterns (WOO-02, WOO-17)

**Product access:**
- GOOD: `wc_get_product( $id )`, `WC_Product_Query`
- WARNING: `WP_Query` with `post_type='product'` (use `wc_get_products()` instead)
- CRITICAL: Direct `$wpdb` queries against product tables

**Order access:**
- GOOD: `wc_get_order( $id )`, `wc_get_orders()`
- CRITICAL: `get_posts()` with `post_type='shop_order'`
- CRITICAL: Direct `$wpdb` queries for order data

**WC_Data pattern:**
- Base class for all WooCommerce CRUD objects
- Data stores handle persistence (post-based vs HPOS tables)
- Always call `->save()` after modifications

### 4. If payment gateway detected (WOO-03, WOO-19, WOO-20)

**CRITICAL violations:**
- Storing raw card numbers/CVV in database or sessions
- Logging card data in `error_log()` or `debug.log`
- Transmitting card data over HTTP (non-SSL)

**WARNING violations:**
- Hardcoded API credentials in code (should use settings)
- Missing `is_ssl()` check before payment processing
- Missing webhook signature verification

**process_payment() validation:**
- Must return array with 'result' and 'redirect' keys
- Use `$order->payment_complete( $transaction_id )` not manual status change
- Never access raw `$_POST` card data—use tokenization

**Cross-reference:**
- See wp-security-review for general security patterns
- This skill focuses on WC-specific payment anti-patterns only

### 5. Check WooCommerce hook usage (WOO-05, WOO-06, WOO-07, WOO-08)

**Lifecycle hooks:**
- `woocommerce_before_cart`, `woocommerce_after_cart`
- `woocommerce_checkout_process`, `woocommerce_checkout_create_order`
- `woocommerce_thankyou`
- `woocommerce_order_status_changed`

**Product data hooks:**
- `woocommerce_product_options_*` for admin fields
- `woocommerce_process_product_meta` for saving

**Checkout field hooks:**
- `woocommerce_checkout_fields` for adding fields
- `woocommerce_checkout_update_order_meta` for saving

**Cart hooks:**
- `woocommerce_add_cart_item_data` for custom cart data
- `woocommerce_cart_calculate_fees` for fees
- `woocommerce_check_cart_items` for validation

**Order status transitions:**
- `woocommerce_order_status_{status}` for specific status changes
- Use `$order->set_status()` with note, not direct post status change

### 6. Check template overrides (WOO-10, WOO-11, WOO-12, WOO-13)

**CRITICAL violations:**
- Template overrides with deleted `do_action()` hooks
- Breaks plugin integration—other extensions can't hook in

**WARNING violations:**
- Outdated template versions (@version comment mismatch)
- May miss WC updates, cause display issues

**INFO suggestions:**
- Template override where a hook exists—suggest using hook instead

**Hooks-first philosophy:**
- Key teaching point: hooks are strongly preferred over template overrides
- Template overrides should be last resort
- Always preserve ALL `do_action()` calls from original template

**Cross-reference:**
- See wp-theme-development for general template patterns

### 7. Check performance patterns (WOO-15, WOO-17, WOO-18)

**Cart fragments (wc-cart-fragments.js):**
- CRITICAL: Site-wide loading with no conditional dequeue
- WARNING: Loading on non-WC pages without justification
- GOOD: Conditional dequeuing to cart/checkout/product pages only
- BETTER: Migrate to Mini-Cart Block (built-in optimization)

**Product queries:**
- CRITICAL: Direct SQL queries against `wp_posts` for products
- WARNING: `WP_Query` with `post_type='product'`
- INFO: Missing object caching for repeated product loads

**Action Scheduler:**
- WARNING: `wp_cron()` for bulk WC operations (unreliable, traffic-dependent)
- GOOD: `as_enqueue_async_action()`, `as_schedule_single_action()`
- Ships with WooCommerce—no separate installation

**Session handling:**
- WARNING: Custom session filters exceeding 30-day cap (WC 10.1+)
- INFO: Custom session implementations bypassing `WC_Session_Handler`

**Cross-reference:**
- See wp-performance-review for comprehensive performance analysis

### 8. Report using output format below

Suggest cross-referencing skills as appropriate:
- Security concerns → `/wp-sec-review`
- Plugin architecture → `/wp-plugin-review`
- Block issues → `/wp-block-review`
- Theme issues → `/wp-theme-review`
- Performance issues → `/wp-perf-review`

## File-Type Specific Checks

### HPOS Compatibility (WOO-16)

**Compatibility declaration (CRITICAL if missing):**
```php
// GOOD: Declare HPOS compatibility
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables',
            __FILE__,
            true
        );
    }
} );

// BAD: Missing declaration
// Extension silently breaks on HPOS-enabled stores
```

**Direct post access (CRITICAL):**
- `get_posts()` with `'post_type' => 'shop_order'`
- `new WP_Query( array( 'post_type' => 'shop_order' ) )`
- `get_post_meta( $order_id, ... )` for order data
- `update_post_meta( $order_id, ... )` for order data
- Direct `$wpdb->prepare()` against `wp_posts` for orders

**CRUD patterns (GOOD):**
```php
// GOOD: HPOS-compatible order access
$order = wc_get_order( $order_id );
$order->update_meta_data( 'custom_field', $value );
$order->save();

// GOOD: Query orders
$orders = wc_get_orders( array(
    'status' => 'completed',
    'limit' => 10,
    'date_created' => '>=' . strtotime( '-30 days' )
) );

// BAD: Direct post access (breaks HPOS)
$orders = get_posts( array(
    'post_type' => 'shop_order',
    'post_status' => 'wc-completed'
) );
update_post_meta( $order_id, 'custom_field', $value );
```

### WooCommerce CRUD Pattern (WOO-02, WOO-07)

**WC_Data base class:**
- All WooCommerce objects extend `WC_Data`
- Data stores handle persistence (HPOS tables vs post tables)
- Changes buffered until `->save()` called

**Order CRUD:**
```php
// GOOD: Complete order manipulation
$order = wc_get_order( $order_id );
$order->set_status( 'processing', 'Payment received' );
$order->update_meta_data( 'gift_message', $message );
$order->add_order_note( 'Custom note' );
$order->save(); // Single save after all changes

// BAD: Manual post status change
wp_update_post( array(
    'ID' => $order_id,
    'post_status' => 'wc-processing'
) );
```

**Product CRUD:**
```php
// GOOD: WC_Product_Query for product lists
$query = new WC_Product_Query( array(
    'status' => 'publish',
    'limit' => 10,
    'category' => array( 'clothing' ),
    'orderby' => 'date',
    'order' => 'DESC'
) );
$products = $query->get_products();

// WARNING: WP_Query for products (future-breaking)
$products = new WP_Query( array(
    'post_type' => 'product',
    'posts_per_page' => 10
) );
```

**Custom data store registration:**
```php
// GOOD: Register custom data store
add_filter( 'woocommerce_data_stores', 'register_custom_data_store' );
function register_custom_data_store( $data_stores ) {
    $data_stores['custom-order-type'] = 'Custom_Order_Data_Store';
    return $data_stores;
}
```

### Payment Gateway Development (WOO-03, WOO-19)

**WC_Payment_Gateway class structure:**
```php
// GOOD: Complete payment gateway implementation
class WC_Gateway_Custom extends WC_Payment_Gateway {

    public function __construct() {
        $this->id = 'custom_gateway';
        $this->has_fields = true;
        $this->method_title = __( 'Custom Gateway', 'text-domain' );
        $this->method_description = __( 'Description', 'text-domain' );

        $this->init_form_fields();
        $this->init_settings();

        add_action( 'woocommerce_update_options_payment_gateways_' . $this->id,
            array( $this, 'process_admin_options' ) );
    }

    public function process_payment( $order_id ) {
        $order = wc_get_order( $order_id );

        // CRITICAL: Always check HTTPS in production
        if ( ! is_ssl() && 'yes' !== $this->get_option( 'testmode' ) ) {
            wc_add_notice( __( 'SSL required', 'text-domain' ), 'error' );
            return array( 'result' => 'failure' );
        }

        // GOOD: Use payment_complete() not manual status change
        $order->payment_complete( $transaction_id );

        return array(
            'result' => 'success',
            'redirect' => $this->get_return_url( $order )
        );
    }
}
```

**CRITICAL security anti-patterns:**
```php
// CRITICAL: Never store raw card data
// BAD:
update_post_meta( $order_id, 'card_number', $_POST['card_number'] );
$wpdb->insert( 'payment_tokens', array( 'card' => $_POST['card_number'] ) );

// CRITICAL: Never log card data
// BAD:
error_log( 'Card: ' . $_POST['card_number'] );
wc_get_logger()->debug( 'CVV: ' . $_POST['cvv'] );

// GOOD: Use tokenization
$token = new WC_Payment_Token_CC();
$token->set_token( $gateway_token );
$token->set_gateway_id( $this->id );
$token->set_last4( substr( $card_number, -4 ) );
$token->set_card_type( $card_type );
$token->save();
```

**Refund handling:**
```php
// GOOD: Implement refund support
public function process_refund( $order_id, $amount = null, $reason = '' ) {
    $order = wc_get_order( $order_id );

    // Process refund via API
    $result = $this->api_refund( $order, $amount );

    if ( $result->success ) {
        $order->add_order_note(
            sprintf( __( 'Refunded %s', 'text-domain' ), $amount )
        );
        return true;
    }

    return false;
}
```

**Cross-reference:**
- See wp-security-review for comprehensive security patterns
- This focuses on WC payment-specific anti-patterns only

### Shipping Methods (WOO-04)

**WC_Shipping_Method class structure:**
```php
// GOOD: Complete shipping method implementation
class WC_Shipping_Custom extends WC_Shipping_Method {

    public function __construct( $instance_id = 0 ) {
        $this->id = 'custom_shipping';
        $this->instance_id = absint( $instance_id );
        $this->method_title = __( 'Custom Shipping', 'text-domain' );
        $this->method_description = __( 'Description', 'text-domain' );
        $this->supports = array( 'shipping-zones', 'instance-settings' );

        $this->init();
    }

    public function calculate_shipping( $package = array() ) {
        $rate = array(
            'id' => $this->id . $this->instance_id,
            'label' => $this->title,
            'cost' => 10.00,
            'calc_tax' => 'per_order'
        );

        $this->add_rate( $rate );
    }
}
```

### Custom Product Types (WOO-02)

**Product type registration:**
```php
// GOOD: Register custom product type
add_filter( 'product_type_selector', 'add_custom_product_type' );
function add_custom_product_type( $types ) {
    $types['custom-product'] = __( 'Custom Product', 'text-domain' );
    return $types;
}

// GOOD: Product class extending WC_Product
class WC_Product_Custom extends WC_Product {

    public function __construct( $product = 0 ) {
        $this->product_type = 'custom-product';
        parent::__construct( $product );
    }

    public function get_type() {
        return 'custom-product';
    }
}

// GOOD: Register product class
add_filter( 'woocommerce_product_class', 'load_custom_product_class', 10, 2 );
function load_custom_product_class( $classname, $product_type ) {
    if ( 'custom-product' === $product_type ) {
        $classname = 'WC_Product_Custom';
    }
    return $classname;
}
```

### WooCommerce Hooks Catalog (WOO-05, WOO-06)

**Lifecycle hooks:**
```php
// GOOD: Order lifecycle hooks
add_action( 'woocommerce_checkout_process', 'validate_custom_checkout_field' );
add_action( 'woocommerce_checkout_create_order', 'save_custom_order_data', 10, 2 );
add_action( 'woocommerce_thankyou', 'custom_thankyou_action' );
add_action( 'woocommerce_order_status_changed', 'handle_status_change', 10, 4 );
```

**Product data hooks:**
```php
// GOOD: Product admin hooks
add_action( 'woocommerce_product_options_general_product_data', 'add_custom_field' );
add_action( 'woocommerce_process_product_meta', 'save_custom_field' );
```

**Checkout field hooks:**
```php
// GOOD: Add checkout field
add_filter( 'woocommerce_checkout_fields', 'add_gift_message_field' );
function add_gift_message_field( $fields ) {
    $fields['order']['gift_message'] = array(
        'type' => 'textarea',
        'label' => __( 'Gift message', 'text-domain' ),
        'required' => false
    );
    return $fields;
}

add_action( 'woocommerce_checkout_update_order_meta', 'save_gift_message' );
function save_gift_message( $order_id ) {
    if ( ! empty( $_POST['gift_message'] ) ) {
        $order = wc_get_order( $order_id );
        $order->update_meta_data( 'gift_message', sanitize_textarea_field( $_POST['gift_message'] ) );
        $order->save();
    }
}
```

### Cart Operations (WOO-08)

**Cart item data:**
```php
// GOOD: Add custom cart item data
add_filter( 'woocommerce_add_cart_item_data', 'add_custom_cart_data', 10, 2 );
function add_custom_cart_data( $cart_item_data, $product_id ) {
    if ( isset( $_POST['custom_field'] ) ) {
        $cart_item_data['custom_field'] = sanitize_text_field( $_POST['custom_field'] );
    }
    return $cart_item_data;
}
```

**Cart fees:**
```php
// GOOD: Add custom fee
add_action( 'woocommerce_cart_calculate_fees', 'add_custom_fee' );
function add_custom_fee() {
    if ( WC()->cart->get_subtotal() > 100 ) {
        WC()->cart->add_fee( __( 'Handling fee', 'text-domain' ), 5 );
    }
}
```

**Cart validation:**
```php
// GOOD: Validate cart contents
add_action( 'woocommerce_check_cart_items', 'validate_cart_items' );
function validate_cart_items() {
    if ( WC()->cart->get_cart_contents_count() < 3 ) {
        wc_add_notice( __( 'Minimum 3 items required', 'text-domain' ), 'error' );
    }
}
```

### Order Status Transitions (WOO-07)

**Custom order status:**
```php
// GOOD: Register custom order status
add_action( 'init', 'register_awaiting_shipment_status' );
function register_awaiting_shipment_status() {
    register_post_status( 'wc-awaiting-shipment', array(
        'label' => __( 'Awaiting Shipment', 'text-domain' ),
        'public' => true,
        'show_in_admin_status_list' => true,
        'label_count' => _n_noop(
            'Awaiting shipment <span class="count">(%s)</span>',
            'Awaiting shipment <span class="count">(%s)</span>',
            'text-domain'
        )
    ) );
}

add_filter( 'wc_order_statuses', 'add_awaiting_shipment_to_order_statuses' );
function add_awaiting_shipment_to_order_statuses( $order_statuses ) {
    $order_statuses['wc-awaiting-shipment'] = __( 'Awaiting Shipment', 'text-domain' );
    return $order_statuses;
}

// GOOD: Set order status
$order = wc_get_order( $order_id );
$order->set_status( 'awaiting-shipment', 'Order ready for shipment' );
```

### Cart Fragments Performance (WOO-15)

**Conditional dequeuing:**
```php
// GOOD: Conditional cart fragments loading
add_filter( 'woocommerce_get_script_data', 'conditional_cart_fragments', 10, 2 );
function conditional_cart_fragments( $data, $handle ) {
    if ( 'wc-cart-fragments' === $handle ) {
        // Only load on WC pages
        if ( ! is_woocommerce() && ! is_cart() && ! is_checkout() ) {
            return null;
        }
    }
    return $data;
}

// CRITICAL: Site-wide cart fragments loading
// BAD: No conditional dequeue - loads on every page
```

**Mini-Cart Block alternative:**
```php
// INFO: Recommend Mini-Cart Block migration
// Mini-Cart Block has built-in performance optimizations
// No cart fragments needed
```

### Action Scheduler Patterns

**Background processing:**
```php
// GOOD: Action Scheduler for bulk operations
function schedule_order_export() {
    as_enqueue_async_action(
        'process_order_export',
        array( 'batch_id' => 123 ),
        'wc-exports'
    );
}

add_action( 'process_order_export', 'do_order_export', 10, 1 );
function do_order_export( $batch_id ) {
    $orders = wc_get_orders( array(
        'limit' => 100,
        'offset' => $batch_id * 100
    ) );

    foreach ( $orders as $order ) {
        // Export logic
    }

    // Schedule next batch if needed
    if ( count( $orders ) === 100 ) {
        as_enqueue_async_action(
            'process_order_export',
            array( 'batch_id' => $batch_id + 1 ),
            'wc-exports'
        );
    }
}

// WARNING: wp_cron for heavy WC tasks
// BAD:
wp_schedule_event( time(), 'hourly', 'process_order_export' );
```

### Webhook Security (WOO-20)

**Signature verification:**
```php
// GOOD: Verify webhook signature
function verify_wc_webhook( $payload, $signature, $secret ) {
    $expected = base64_encode( hash_hmac( 'sha256', $payload, $secret, true ) );

    // CRITICAL: Use hash_equals to prevent timing attacks
    return hash_equals( $expected, $signature );
}

// Webhook handler
$payload = file_get_contents( 'php://input' );
$signature = $_SERVER['HTTP_X_WC_WEBHOOK_SIGNATURE'] ?? '';
$delivery_id = $_SERVER['HTTP_X_WC_WEBHOOK_DELIVERY_ID'] ?? '';

// WARNING: Missing signature verification
if ( ! verify_wc_webhook( $payload, $signature, $secret ) ) {
    http_response_code( 401 );
    exit;
}

// GOOD: Check for duplicate delivery
if ( get_transient( 'wc_webhook_' . $delivery_id ) ) {
    http_response_code( 200 );
    exit;
}
set_transient( 'wc_webhook_' . $delivery_id, true, DAY_IN_SECONDS );

// GOOD: Process async via Action Scheduler
as_enqueue_async_action( 'process_wc_webhook', array( 'payload' => $payload ) );
```

### Template Override Anti-Patterns (WOO-10, WOO-11, WOO-12)

**Preserving hooks:**
```php
// In child-theme/woocommerce/content-product.php

// GOOD: Preserve all action hooks from original template
do_action( 'woocommerce_before_shop_loop_item' );
do_action( 'woocommerce_before_shop_loop_item_title' );
// Custom content here
do_action( 'woocommerce_shop_loop_item_title' );
do_action( 'woocommerce_after_shop_loop_item_title' );
do_action( 'woocommerce_after_shop_loop_item' );

// CRITICAL: Deleted hooks in template override
// BAD: No do_action() calls - breaks plugin integration
```

**Version tracking:**
```php
// GOOD: Template with version comment
/**
 * Product loop template
 *
 * @version 8.9.0
 */

// WARNING: Outdated version
// Template version 3.6.0 when WC is 10.5 - may miss updates
```

**Hooks-first philosophy:**
```php
// BETTER: Use hooks instead of template override
add_action( 'woocommerce_shop_loop_item_title', 'add_custom_content', 15 );
function add_custom_content() {
    // Custom content via hook - no template override needed
}

// INFO: Template override where hook exists
// Suggest using hook instead of copying entire template
```

**Cross-reference:**
- See wp-theme-development for general template patterns

### Surface-Level Checks

**WooCommerce Blocks checkout integration (WOO-14):**
```php
// GOOD: Add checkout field via Additional Checkout Fields API (WC 8.6+)
add_action( 'woocommerce_init', 'register_custom_checkout_field' );
function register_custom_checkout_field() {
    woocommerce_register_additional_checkout_field( array(
        'id' => 'namespace/gift-message',
        'label' => __( 'Gift message', 'text-domain' ),
        'location' => 'order',
        'type' => 'text'
    ) );
}
```

**WooCommerce REST API extensions (WOO-09):**
```php
// INFO: Custom REST endpoint registration
add_action( 'rest_api_init', 'register_custom_endpoint' );
function register_custom_endpoint() {
    register_rest_route( 'wc/v3', '/custom-endpoint', array(
        'methods' => 'GET',
        'callback' => 'custom_endpoint_callback',
        'permission_callback' => function() {
            return current_user_can( 'manage_woocommerce' );
        }
    ) );
}
```

**Coupon validation (WOO-21):**
```php
// GOOD: Custom coupon validation
add_filter( 'woocommerce_coupon_is_valid', 'validate_custom_coupon', 10, 3 );
function validate_custom_coupon( $valid, $coupon, $discount ) {
    if ( WC()->cart->get_cart_contents_count() < 3 ) {
        throw new Exception(
            __( 'Coupon requires at least 3 items', 'text-domain' ),
            109
        );
    }
    return $valid;
}
```

**Session handling (WOO-18):**
```php
// WARNING: Custom session filter exceeding 30-day cap (WC 10.1+)
// BAD:
add_filter( 'wc_session_expiration', function() {
    return 60 * DAY_IN_SECONDS; // Exceeds 30-day cap
} );

// GOOD: Respect 30-day cap
add_filter( 'wc_session_expiration', function() {
    return 30 * DAY_IN_SECONDS; // Maximum allowed
} );
```

## Search Patterns for Quick Detection (WOO-22)

Use these `rg` commands and shell checks for quick WooCommerce scanning. Organized by severity.

### CRITICAL Patterns

```bash
# HPOS declaration candidates
# If this returns nothing in a WooCommerce extension, the plugin likely lacks HPOS declaration.
rg -n "declare_compatibility\s*\(\s*['\"]custom_order_tables['\"]" . -g '*.php'

# get_posts/WP_Query with shop_order
rg -n "post_type.*shop_order|shop_order.*post_type" . -g '*.php'

# Direct $wpdb queries against wp_posts for orders
rg -n "\$wpdb.*wp_posts.*shop_order" . -g '*.php'

# Raw card data storage/logging
rg -n "card_number|card_cvv|cvv.*meta|card.*error_log" . -g '*.php'

# Template overrides without do_action() calls
find . -path "*/woocommerce/*.php" -exec rg -L "do_action|apply_filters" {} \;

# Webhook signature handling candidates (manually confirm verification logic)
rg -n "X-WC-Webhook-Signature|hash_hmac|verify" . -g '*.php'
```

### WARNING Patterns

```bash
# WP_Query with post_type=product (compare these result sets manually)
rg -n "WP_Query|get_posts" . -g '*.php'
rg -n "post_type.*product|product.*post_type" . -g '*.php'

# Site-wide cart-fragments loading without conditional dequeue (manual context check)
rg -n "wc-cart-fragments|woocommerce_get_script_data|is_woocommerce|is_cart" . -g '*.php'

# wp_cron for bulk WC operations (manual context check)
rg -n "wp_schedule_event|wp_cron|wc_|order|product" . -g '*.php'

# Hardcoded API credentials
rg -n "api_key.*=.*['\"][A-Za-z0-9]{20,}" . -g '*.php'

# get_post_meta/update_post_meta for order fields
rg -n "get_post_meta.*order_id|update_post_meta.*order_id" . -g '*.php'

# Session filters exceeding 30-day cap (manual follow-up on returned values)
rg -n "wc_session_expiration|wc_session_expiring" . -g '*.php'
```

### INFO Patterns

```bash
# Template overrides where hooks exist
find . -path "*/woocommerce/*.php" -type f

# Missing object caching for repeated product loads
rg -n "wc_get_product" . -g '*.php'

# Action Scheduler candidates
rg -n "foreach.*wc_get_orders|foreach.*wc_get_products" . -g '*.php'

# WC Blocks integration opportunities
rg -n "woocommerce_register_additional_checkout_field|Store API" . -g '*.php'
```

**Note:** WC-specific patterns need different context than generic WP. `get_posts()` for non-order post types is valid. `WP_Query` for standard posts/pages is valid. Only flag when combined with WC-specific post types.

## WooCommerce Context Detection

Context-aware review notes based on file structure and patterns:

### Extension/plugin
**Detection:** Main plugin file with WC dependency check, HPOS declaration
**Review focus:** Full HPOS + CRUD + hook audit
**Most common context**

### Theme integration
**Detection:** woocommerce/ directory in theme with template overrides
**Review focus:** Template override quality, hooks preservation
**Cross-reference:** wp-theme-development for theme patterns

### Payment gateway
**Detection:** Class extending `WC_Payment_Gateway`
**Review focus:** Heightened security review (never store raw cards, HTTPS check, webhook verification)
**Cross-reference:** wp-security-review for general security

### Shipping method
**Detection:** Class extending `WC_Shipping_Method`
**Review focus:** calculate_shipping() review, zone support, rate calculation

### Custom product type
**Detection:** Class extending `WC_Product`
**Review focus:** Data store review, product type registration, class hierarchy

### WC Blocks integration
**Detection:** Store API usage, checkout block extension points
**Review focus:** Surface-level review, Additional Checkout Fields API
**Cross-reference:** wp-block-development for deep block patterns

## Quick Reference: WooCommerce Development Patterns (WOO-23)

Common WooCommerce patterns organized by concern. All examples follow WordPress PHP Coding Standards (spaces in parentheses, `array()` not `[]`, Yoda conditions).

### HPOS Compatibility Declaration

**❌ BAD: Missing HPOS declaration**
```php
<?php
// Extension silently breaks on HPOS-enabled stores
```

**✅ GOOD: Declare compatibility in before_woocommerce_init hook**
```php
<?php
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables',
            __FILE__,
            true
        );
    }
} );
```

### Order Data Access

**❌ BAD: Direct post access (breaks HPOS)**
```php
<?php
$orders = get_posts( array(
    'post_type' => 'shop_order',
    'post_status' => 'wc-completed'
) );
update_post_meta( $order_id, 'custom_field', $value );
```

**✅ GOOD: HPOS-compatible CRUD**
```php
<?php
$orders = wc_get_orders( array(
    'status' => 'completed',
    'limit' => 10
) );

$order = wc_get_order( $order_id );
$order->update_meta_data( 'custom_field', $value );
$order->save();
```

### Order Meta Operations

**❌ BAD: Direct meta functions**
```php
<?php
update_post_meta( $order_id, 'delivery_date', '2026-02-15' );
$date = get_post_meta( $order_id, 'delivery_date', true );
```

**✅ GOOD: WC_Order methods**
```php
<?php
$order = wc_get_order( $order_id );
$order->update_meta_data( 'delivery_date', '2026-02-15' );
$order->save();

$date = $order->get_meta( 'delivery_date', true );
```

### Product Data Access

**❌ BAD: WP_Query for products (future-breaking)**
```php
<?php
$products = new WP_Query( array(
    'post_type' => 'product',
    'posts_per_page' => 10
) );
```

**✅ GOOD: WC_Product_Query**
```php
<?php
$query = new WC_Product_Query( array(
    'status' => 'publish',
    'limit' => 10,
    'category' => array( 'clothing' ),
    'orderby' => 'date',
    'order' => 'DESC'
) );
$products = $query->get_products();
```

### Payment Gateway

**❌ BAD: Raw card data storage, missing HTTPS check**
```php
<?php
public function process_payment( $order_id ) {
    // CRITICAL: Never store raw card data
    update_post_meta( $order_id, 'card_number', $_POST['card_number'] );

    // Process payment
    $order = wc_get_order( $order_id );
    $order->update_status( 'processing' ); // Manual status change

    return array(
        'result' => 'success',
        'redirect' => $this->get_return_url( $order )
    );
}
```

**✅ GOOD: Tokenization, HTTPS check, payment_complete()**
```php
<?php
public function process_payment( $order_id ) {
    $order = wc_get_order( $order_id );

    // Check HTTPS in production
    if ( ! is_ssl() && 'yes' !== $this->get_option( 'testmode' ) ) {
        wc_add_notice( __( 'SSL required', 'text-domain' ), 'error' );
        return array( 'result' => 'failure' );
    }

    // Process via API (use tokenization, never store raw cards)
    $result = $this->api_charge( $order );

    if ( $result->success ) {
        // Use payment_complete() not manual status change
        $order->payment_complete( $result->transaction_id );

        return array(
            'result' => 'success',
            'redirect' => $this->get_return_url( $order )
        );
    }

    return array( 'result' => 'failure' );
}
```

### Shipping Method

**✅ GOOD: Complete shipping method**
```php
<?php
class WC_Shipping_Custom extends WC_Shipping_Method {

    public function __construct( $instance_id = 0 ) {
        $this->id = 'custom_shipping';
        $this->instance_id = absint( $instance_id );
        $this->method_title = __( 'Custom Shipping', 'text-domain' );
        $this->supports = array( 'shipping-zones', 'instance-settings' );

        $this->init();
    }

    public function calculate_shipping( $package = array() ) {
        $rate = array(
            'id' => $this->id . $this->instance_id,
            'label' => $this->title,
            'cost' => 10.00,
            'calc_tax' => 'per_order'
        );

        $this->add_rate( $rate );
    }
}
```

### Custom Product Type

**✅ GOOD: Register and implement custom product type**
```php
<?php
// Register product type
add_filter( 'product_type_selector', 'add_custom_product_type' );
function add_custom_product_type( $types ) {
    $types['custom-product'] = __( 'Custom Product', 'text-domain' );
    return $types;
}

// Product class
class WC_Product_Custom extends WC_Product {

    public function __construct( $product = 0 ) {
        $this->product_type = 'custom-product';
        parent::__construct( $product );
    }

    public function get_type() {
        return 'custom-product';
    }
}

// Register product class
add_filter( 'woocommerce_product_class', 'load_custom_product_class', 10, 2 );
function load_custom_product_class( $classname, $product_type ) {
    if ( 'custom-product' === $product_type ) {
        $classname = 'WC_Product_Custom';
    }
    return $classname;
}
```

### Cart Operations

**✅ GOOD: Add cart item data**
```php
<?php
add_filter( 'woocommerce_add_cart_item_data', 'add_custom_cart_data', 10, 2 );
function add_custom_cart_data( $cart_item_data, $product_id ) {
    if ( isset( $_POST['custom_field'] ) ) {
        $cart_item_data['custom_field'] = sanitize_text_field( $_POST['custom_field'] );
    }
    return $cart_item_data;
}
```

**✅ GOOD: Add cart fee**
```php
<?php
add_action( 'woocommerce_cart_calculate_fees', 'add_custom_fee' );
function add_custom_fee() {
    if ( WC()->cart->get_subtotal() > 100 ) {
        WC()->cart->add_fee( __( 'Handling fee', 'text-domain' ), 5 );
    }
}
```

### Order Status Transitions

**❌ BAD: Manual post status change**
```php
<?php
wp_update_post( array(
    'ID' => $order_id,
    'post_status' => 'wc-processing'
) );
```

**✅ GOOD: Use WC_Order::set_status()**
```php
<?php
$order = wc_get_order( $order_id );
$order->set_status( 'processing', 'Payment received' );
// Automatically saved
```

**✅ GOOD: Use payment_complete() for payment flow**
```php
<?php
$order = wc_get_order( $order_id );
$order->payment_complete( $transaction_id );
```

### Template Override with Hook Preservation

**❌ BAD: Deleted hooks in template override**
```php
<?php
// In child-theme/woocommerce/content-product.php
// CRITICAL: No do_action() calls - breaks plugin integration
?>
<li class="product">
    <h2><?php the_title(); ?></h2>
    <div class="price"><?php echo $product->get_price_html(); ?></div>
</li>
```

**✅ GOOD: Preserve all action hooks**
```php
<?php
// In child-theme/woocommerce/content-product.php
do_action( 'woocommerce_before_shop_loop_item' );
do_action( 'woocommerce_before_shop_loop_item_title' );
?>
<h2><?php the_title(); ?></h2>
<?php
do_action( 'woocommerce_shop_loop_item_title' );
do_action( 'woocommerce_after_shop_loop_item_title' );
do_action( 'woocommerce_after_shop_loop_item' );
```

**✅ BETTER: Use hooks instead of template override**
```php
<?php
add_action( 'woocommerce_shop_loop_item_title', 'add_custom_content', 15 );
function add_custom_content() {
    // Custom content via hook - no template override needed
}
```

### Cart Fragments Optimization

**❌ BAD: Site-wide cart fragments loading**
```php
<?php
// No conditional dequeue - loads on every page
// CRITICAL performance issue
```

**✅ GOOD: Conditional dequeuing**
```php
<?php
add_filter( 'woocommerce_get_script_data', 'conditional_cart_fragments', 10, 2 );
function conditional_cart_fragments( $data, $handle ) {
    if ( 'wc-cart-fragments' === $handle ) {
        if ( ! is_woocommerce() && ! is_cart() && ! is_checkout() ) {
            return null;
        }
    }
    return $data;
}
```

**✅ BETTER: Migrate to Mini-Cart Block**
```php
// Mini-Cart Block has built-in performance optimizations
// No cart fragments needed
```

### Action Scheduler

**❌ BAD: wp_cron for bulk WC operations**
```php
<?php
wp_schedule_event( time(), 'hourly', 'process_order_export' );

add_action( 'process_order_export', 'do_export' );
function do_export() {
    // Unreliable, traffic-dependent, no retry
}
```

**✅ GOOD: Action Scheduler for bulk operations**
```php
<?php
function schedule_order_export() {
    as_enqueue_async_action(
        'process_order_export',
        array( 'batch_id' => 0 ),
        'wc-exports'
    );
}

add_action( 'process_order_export', 'do_order_export', 10, 1 );
function do_order_export( $batch_id ) {
    $orders = wc_get_orders( array(
        'limit' => 100,
        'offset' => $batch_id * 100
    ) );

    foreach ( $orders as $order ) {
        // Export logic
    }

    // Schedule next batch if needed
    if ( 100 === count( $orders ) ) {
        as_enqueue_async_action(
            'process_order_export',
            array( 'batch_id' => $batch_id + 1 ),
            'wc-exports'
        );
    }
}
```

### Webhook Security

**❌ BAD: Missing signature verification**
```php
<?php
// Webhook handler
$payload = file_get_contents( 'php://input' );
$data = json_decode( $payload );

// WARNING: No signature verification - allows forged webhooks
process_webhook( $data );
```

**✅ GOOD: HMAC-SHA256 verification with hash_equals()**
```php
<?php
function verify_wc_webhook( $payload, $signature, $secret ) {
    $expected = base64_encode( hash_hmac( 'sha256', $payload, $secret, true ) );
    return hash_equals( $expected, $signature );
}

// Webhook handler
$payload = file_get_contents( 'php://input' );
$signature = $_SERVER['HTTP_X_WC_WEBHOOK_SIGNATURE'] ?? '';
$delivery_id = $_SERVER['HTTP_X_WC_WEBHOOK_DELIVERY_ID'] ?? '';

if ( ! verify_wc_webhook( $payload, $signature, $secret ) ) {
    http_response_code( 401 );
    exit;
}

// Check for duplicate delivery
if ( get_transient( 'wc_webhook_' . $delivery_id ) ) {
    http_response_code( 200 );
    exit;
}
set_transient( 'wc_webhook_' . $delivery_id, true, DAY_IN_SECONDS );

// Process async
as_enqueue_async_action( 'process_wc_webhook', array( 'payload' => $payload ) );
```

### WooCommerce Blocks Checkout

**✅ GOOD: Additional Checkout Fields API (WC 8.6+)**
```php
<?php
add_action( 'woocommerce_init', 'register_custom_checkout_field' );
function register_custom_checkout_field() {
    woocommerce_register_additional_checkout_field( array(
        'id' => 'namespace/gift-message',
        'label' => __( 'Gift message', 'text-domain' ),
        'location' => 'order',
        'type' => 'text',
        'attributes' => array(
            'maxLength' => 200
        )
    ) );
}

// Access field value
$order = wc_get_order( $order_id );
$gift_message = $order->get_meta( 'namespace/gift-message' );
```

### REST API Extension

**✅ GOOD: Custom REST endpoint with authentication**
```php
<?php
add_action( 'rest_api_init', 'register_custom_endpoint' );
function register_custom_endpoint() {
    register_rest_route( 'wc/v3', '/custom-endpoint', array(
        'methods' => 'GET',
        'callback' => 'custom_endpoint_callback',
        'permission_callback' => function() {
            return current_user_can( 'manage_woocommerce' );
        }
    ) );
}
```

### Coupon Validation

**✅ GOOD: Custom coupon validation**
```php
<?php
add_filter( 'woocommerce_coupon_is_valid', 'validate_custom_coupon', 10, 3 );
function validate_custom_coupon( $valid, $coupon, $discount ) {
    if ( WC()->cart->get_cart_contents_count() < 3 ) {
        throw new Exception(
            __( 'Coupon requires at least 3 items', 'text-domain' ),
            109
        );
    }
    return $valid;
}
```

### Session Handling

**❌ BAD: Exceeding 30-day cap**
```php
<?php
add_filter( 'wc_session_expiration', function() {
    return 60 * DAY_IN_SECONDS; // Exceeds cap
} );
```

**✅ GOOD: Respect 30-day cap (WC 10.1+)**
```php
<?php
add_filter( 'wc_session_expiration', function() {
    return 30 * DAY_IN_SECONDS; // Maximum allowed
} );
```

### Email Customization

**✅ GOOD: Extend WC_Email class**
```php
<?php
class WC_Email_Custom extends WC_Email {

    public function __construct() {
        $this->id = 'custom_email';
        $this->title = __( 'Custom Email', 'text-domain' );
        $this->description = __( 'Email description', 'text-domain' );

        $this->template_html = 'emails/custom-email.php';
        $this->template_plain = 'emails/plain/custom-email.php';

        parent::__construct();
    }

    public function trigger( $order_id ) {
        $this->object = wc_get_order( $order_id );

        if ( ! $this->is_enabled() || ! $this->get_recipient() ) {
            return;
        }

        $this->send( $this->get_recipient(), $this->get_subject(), $this->get_content(), $this->get_headers(), $this->get_attachments() );
    }
}
```

## Severity Definitions (WOO-24)

| Severity | Definition | Examples |
|----------|------------|----------|
| **CRITICAL** | Extension will break on modern WC stores OR has security vulnerabilities | Missing HPOS compatibility declaration, direct post access for orders (get_posts/WP_Query with shop_order), direct database queries for orders/products, raw card data storage/logging (card_number in DB or error_log), template overrides with deleted action hooks, missing webhook signature verification, transmitting card data over HTTP |
| **WARNING** | Extension works but has quality/compatibility/performance issues | WP_Query for products (future-breaking), cart fragments site-wide loading, outdated template overrides (version mismatch), hardcoded API credentials in code, wp_cron() for bulk WC operations, session duration exceeding 30 days, get_post_meta/update_post_meta for order fields, missing HTTPS check in payment processing |
| **INFO** | Best practice improvements OR optimization opportunities | Template override where hook exists (suggest hook instead), Action Scheduler instead of wp_cron for light tasks, object caching for repeated product loads, WC Blocks integration opportunity, Additional Checkout Fields API usage, product object caching (WC 10.5+ experimental) |

## Output Format (WOO-24)

Report findings grouped by FILE (PHP files organized by actual file path), with line numbers and severity labels. Use BAD/GOOD code pairs for each finding.

```markdown
# WooCommerce Review: my-wc-extension

## FILE: includes/class-order-handler.php

### Line 45: CRITICAL - Direct post access for orders
get_posts() with post_type='shop_order' breaks on HPOS-enabled stores. Use wc_get_orders() instead.

❌ **BAD:**
```php
$orders = get_posts( array(
    'post_type' => 'shop_order',
    'post_status' => 'wc-completed'
) );
```

✅ **GOOD:**
```php
$orders = wc_get_orders( array(
    'status' => 'completed',
    'limit' => 10
) );
```

### Line 67: CRITICAL - Direct meta functions for order data
update_post_meta() for order data breaks HPOS compatibility. Use WC_Order methods.

❌ **BAD:**
```php
update_post_meta( $order_id, 'custom_field', $value );
```

✅ **GOOD:**
```php
$order = wc_get_order( $order_id );
$order->update_meta_data( 'custom_field', $value );
$order->save();
```

## FILE: my-wc-extension.php

### Line 1: CRITICAL - Missing HPOS declaration
Extension must declare HPOS compatibility status. Add before_woocommerce_init hook.

❌ **BAD:**
```php
<?php
// No HPOS declaration - extension silently incompatible
```

✅ **GOOD:**
```php
<?php
add_action( 'before_woocommerce_init', function() {
    if ( class_exists( \Automattic\WooCommerce\Utilities\FeaturesUtil::class ) ) {
        \Automattic\WooCommerce\Utilities\FeaturesUtil::declare_compatibility(
            'custom_order_tables',
            __FILE__,
            true
        );
    }
} );
```

## FILE: includes/class-gateway.php

### Line 89: CRITICAL - Raw card data logging
Logging card data is a PCI violation and security breach. Never log payment information.

❌ **BAD:**
```php
error_log( 'Processing card: ' . $_POST['card_number'] );
```

✅ **GOOD:**
```php
// Never log card data
// Use tokenization, log transaction IDs only
$this->log( 'Processing transaction: ' . $transaction_id );
```

### Line 102: WARNING - Missing HTTPS check
Check is_ssl() before processing payments in production mode.

❌ **BAD:**
```php
public function process_payment( $order_id ) {
    // Process payment without SSL check
}
```

✅ **GOOD:**
```php
public function process_payment( $order_id ) {
    if ( ! is_ssl() && 'yes' !== $this->get_option( 'testmode' ) ) {
        wc_add_notice( __( 'SSL required', 'text-domain' ), 'error' );
        return array( 'result' => 'failure' );
    }
    // Process payment
}
```

## FILE: includes/class-cart-fragments.php

### Line 23: WARNING - Site-wide cart fragments loading
Cart fragments loading on every page causes performance issues. Add conditional dequeuing.

❌ **BAD:**
```php
// No conditional dequeue - loads on all pages
```

✅ **GOOD:**
```php
add_filter( 'woocommerce_get_script_data', 'conditional_cart_fragments', 10, 2 );
function conditional_cart_fragments( $data, $handle ) {
    if ( 'wc-cart-fragments' === $handle ) {
        if ( ! is_woocommerce() && ! is_cart() && ! is_checkout() ) {
            return null;
        }
    }
    return $data;
}
```

## SUMMARY

**Total issues: 7**
- CRITICAL: 4 (must fix - extension broken on HPOS stores or security violations)
- WARNING: 2 (quality/performance issues)
- INFO: 1 (best practice improvement)

**HPOS compatibility risk:** HIGH - Extension will break on modern WooCommerce stores
**Security note:** Payment security issues detected. Run `/wp-sec-review` for comprehensive security analysis.
**Performance note:** Cart fragments performance issue detected. Run `/wp-perf-review` for comprehensive performance analysis.
```

## Common Mistakes (WOO-25)

Patterns that look like issues but are NOT problems:

| Pattern | Why It's NOT a Problem | Context |
|---------|------------------------|---------|
| **get_posts() for custom post types (not orders)** | Valid when post type is not 'shop_order'. Only shop_order queries break HPOS. | Extensions can use get_posts() for their own post types |
| **WP_Query for standard posts/pages** | Valid for non-product queries. Only product queries flagged as WARNING. | Blog posts, custom post types are fine with WP_Query |
| **get_post_meta() for custom post types (not orders)** | Valid when not accessing order data. Only order meta breaks HPOS. | Custom post type meta operations work normally |
| **Template overrides in child themes** | Legitimate when hooks are preserved. Only flag if do_action() calls deleted. | Intentional customization with proper hook preservation |
| **wc-cart-fragments.js on cart/checkout/product pages** | Expected on WC pages. Only flag site-wide loading. | Conditional loading to WC pages is correct |
| **wp_cron() for lightweight non-WC tasks** | Acceptable for simple scheduled tasks. Only flag for heavy WC operations. | Daily cleanup, simple notifications are fine |
| **WC_Session usage within 30-day window** | Normal behavior. Only flag custom filters exceeding cap. | Standard session handling works correctly |
| **error_log() in non-payment code** | Acceptable debugging. Only flag in payment processing context. | General logging is fine, just not card data |
| **Direct $wpdb for custom tables (NOT WC core tables)** | Valid for extension's own tables. Only flag queries against wp_posts/wp_postmeta for WC data. | Custom table queries don't affect HPOS |
| **process_payment() accessing $_POST for custom fields** | Valid for non-card data (shipping notes, gift messages). Only flag raw card data access. | Custom checkout field handling is expected |
| **Template overrides without @version comment** | Missing metadata, not necessarily outdated. Only flag significant version mismatches. | Version tracking helps but absence isn't critical |
| **apiVersion 2 in WC Blocks integration** | Block-related, not WC-specific. Defer to wp-block-development. | Block patterns handled by block skill |

## Version Compatibility Reference

Quick reference for WooCommerce version requirements:

| Feature | WooCommerce Version | Notes |
|---------|---------------------|-------|
| WC_Data CRUD API | 3.0+ | Base class for all CRUD objects |
| wc_get_order(), wc_get_product() | 3.0+ | Preferred data access methods |
| Product attribute lookup table | 6.3+ | Indexed product attributes for filtering |
| Cart fragments no longer global by default | 7.8+ | Requires opt-in for site-wide loading |
| HPOS (Custom Order Tables) default | 8.2+ | New stores use HPOS by default |
| HPOS compatibility declaration required | 8.2+ | declare_compatibility() mandatory |
| Additional Checkout Fields API | 8.6+ | Block checkout field registration |
| Session 30-day cap enforced | 10.1+ | Maximum session duration limit |
| wc_enqueue_js() deprecated | 10.4+ | Use wp_add_inline_script() instead |
| Product object caching (experimental) | 10.5+ | Opt-in performance feature |
| Variation price caching improvements | 10.5+ | Automatic performance optimization |
| Batch analytics imports (100/12hrs) | 10.5+ | Background processing improvements |

## Deep-Dive References

For advanced WooCommerce development patterns, load these companion reference documents:

| Task | Reference to Load |
|------|-------------------|
| HPOS compatibility migration, payment gateway development (WC_Payment_Gateway lifecycle, process_payment flow, refund handling, security patterns), shipping methods (WC_Shipping_Method, calculate_shipping, zones), custom product types (register_product_type, data stores), order handling (WC_Order CRUD, status transitions), cart operations (cart item data, fees, validation), REST API extensions, Action Scheduler patterns, webhook security | `references/wc-extension-guide.md` |
| Template hierarchy (archive-product, content-product, single-product, cart, checkout, myaccount), override procedures (child theme woocommerce/ directory, version tracking), hooks-first philosophy (when to use hooks vs overrides, preserving action hooks), shop/product/cart/checkout theming, WooCommerce Blocks compatibility notes, email templates | `references/wc-template-guide.md` |
| Cart fragments analysis (problem, solutions, Mini-Cart Block), WC_Product_Query optimization, HPOS performance benefits, session handling (30-day cap, cleanup), Action Scheduler for background processing, transient and object caching strategies, variation price caching, product attribute lookup table, database optimization | `references/wc-performance-guide.md` |

**Note:** Reference docs provide deep-dive content. This SKILL.md is self-sufficient for standard WooCommerce reviews.

**Security crossover:** When encountering security-relevant patterns (payment data handling, REST API authentication, AJAX nonce verification, capability checks), this skill provides brief reminders but defers to wp-security-review for comprehensive security analysis. For detailed security patterns, use `/wp-sec-review` command.

**Plugin crossover:** When encountering plugin-level patterns (WC dependency checking, activation/deactivation, hooks architecture, REST API registration), this skill provides brief mentions but defers to wp-plugin-development for plugin architecture depth. For detailed plugin review, use `/wp-plugin-review` command.

**Block crossover:** When encountering WooCommerce Blocks integration (Store API, checkout block extension points, Additional Checkout Fields API), this skill provides brief mentions but defers to wp-block-development for block development depth. For detailed block patterns, use `/wp-block-review` command.

**Theme crossover:** When encountering template overrides in themes (woocommerce/ directory, template hierarchy, version tracking), this skill provides brief mentions but defers to wp-theme-development for theme development depth. For detailed theme review, use `/wp-theme-review` command.

**Performance crossover:** When encountering cart fragments, query optimization, caching strategies, this skill provides brief mentions but defers to wp-performance-review for comprehensive performance analysis. For detailed performance patterns, use `/wp-perf-review` command.
