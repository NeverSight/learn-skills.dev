---
name: elementor-widget-create
description: Scaffold a custom Elementor widget (classic Widget_Base or 4.0 Atomic_Widget_Base, free or Pro base). Use when the user wants to create, register, or extend an Elementor widget, add controls, or write render/content_template.
---

# elementor-widget-create

Decide which base first. Ask the user (or infer from their Elementor version):

- Classic editor (3.x or 4.x non-atomic): extend `Elementor\Widget_Base`.
- Atomic 4.0 widget (`e-*` element type): extend `Elementor\Modules\AtomicWidgets\Elements\Base\Atomic_Widget_Base`.
- Pro widget: typically extends `ElementorPro\Base\Base_Widget` or a module-specific base (e.g. `Posts_Base`, `Theme_Elements_Widget_Base`, `Carousel_Base`, `Products_Base`).

For non-obvious patterns (multi-skin widget, repeater controls, Pro Posts/Carousel/WooCommerce base, atomic prop schema), Read `resources/widget-create-examples.md`.

## Classic Widget_Base — required overrides

Source: `elementor-free/elementor/includes/base/widget-base.php` (abstract class + render_content at line 617, render_plain_content at line 696).

- `get_name()` — unique slug, used in `_elementor_data` JSON.
- `get_title()`, `get_icon()`, `get_keywords()`, `get_categories()` (defaults to `['basic']`).
- `protected function register_controls()` — call `start_controls_section` / `add_control` / `add_responsive_control` / `add_group_control` / `end_controls_section`. Control type constants in `Elementor\Controls_Manager`.
- `protected function render()` — server-side HTML for frontend + editor preview. Use `$this->get_settings_for_display()`, not `get_settings()`, so dynamic tags resolve.
- `protected function content_template()` — Underscore.js template (`<# #>` / `{{ }}` / `{{{ }}}`) for live editor preview. Skip only if you set `$_has_template_content = false`.

## Registration

Hook `elementor/widgets/register` (deprecated alias `elementor/widgets/widgets_registered` since 3.5). See `elementor-free/elementor/includes/managers/widgets.php:147-159`.

```php
add_action( 'elementor/widgets/register', function( $widgets_manager ) {
    require_once __DIR__ . '/widgets/my-widget.php';
    $widgets_manager->register( new \My_Plugin\My_Widget() );
} );
```

If you need a custom category, hook `elementor/elements/categories_registered`.

Enqueue widget-specific JS/CSS via `get_script_depends()` / `get_style_depends()` (registered separately on `wp_enqueue_scripts` / `elementor/frontend/after_register_scripts`).

## Atomic 4.0 widget — required overrides

Anchor file: `elementor-free/elementor/modules/atomic-widgets/elements/atomic-button/atomic-button.php`.

- `public static function get_element_type(): string` — must start with `e-`.
- `get_title()`, `get_icon()`, `get_keywords()`.
- `protected static function define_props_schema(): array` — typed prop schema using `*_Prop_Type::make()` from `modules/atomic-widgets/PropTypes/`.
- `define_atomic_controls()` — array of `Section::make()` containing typed controls from `modules/atomic-widgets/controls/types/`.
- Template: use `Has_Template` trait + a `.twig` file in the same dir, OR override `render()`.
- Register through `Widgets_Manager::register()` on `elementor/widgets/register` like classic — atomic dispatches itself; see `atomic-widgets/module.php:161` and `:267-276`.

Atomic widgets don't use `register_controls` / `content_template` — those are classic-only.

## Pro widget bases

- `ElementorPro\Base\Base_Widget` — adds promo handling, common Pro categories.
- `Posts_Base` (`modules/posts/widgets/posts-base.php`) — query controls, pagination, skins.
- `ElementorPro\Modules\Carousel\Widgets\Base` (`modules/carousel/widgets/base.php:15`) — Swiper config. Note the class is literally named `Base`; use the FQN, not `Carousel_Base`.
- `ElementorPro\Modules\ThemeElements\Widgets\Base` (`modules/theme-elements/widgets/base.php:10`) — Pro "Theme Elements" category. Also literally `Base`; alias it on import to avoid clashing with the carousel `Base`.
- `Products_Base` / `WooCommerce\Base_Widget` — WC integration helpers.

Pro widgets register on the same `elementor/widgets/register` hook from within their module.

## Deploy & verify

To install the widget on a live/staging site and confirm it registered and renders, use `elementor-deploy-verify` (writes the file, activates, asserts `get_widget_types('<name>')`, render-checks, flushes CSS).
