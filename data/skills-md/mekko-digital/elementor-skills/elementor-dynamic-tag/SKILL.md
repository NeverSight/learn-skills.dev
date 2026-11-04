---
name: elementor-dynamic-tag
description: Register a custom Elementor dynamic tag — text, image, URL, color, gallery, etc. — so users can bind it from any control's dynamic picker. Use when the user wants a new dynamic tag, an ACF/CPT field source, or a Pro-style data tag.
---

# elementor-dynamic-tag

Two flavors. Pick by output shape:

- **Tag** (`Elementor\Core\DynamicTags\Tag`) — returns rendered HTML/string via `render()`. Use for free-form text-like output.
- **Data_Tag** (`Elementor\Core\DynamicTags\Data_Tag`) — returns structured data via `get_value()`. Required for IMAGE / URL / COLOR / GALLERY categories where the consuming control expects a value array, not HTML.

Pro adds two extra bases for license gating:
- `ElementorPro\Modules\DynamicTags\Tags\Base\Tag` (extends free Tag).
- `ElementorPro\Modules\DynamicTags\Tags\Base\Data_Tag` (extends free Data_Tag).
- Both use `License_Meta_Trait` — only needed if you ship behind Pro license features.

## Required overrides (free Tag)

Source: `elementor-free/elementor/core/dynamic-tags/base-tag.php`.

- `get_name()` — slug stored in `__dynamic__` map.
- `get_title()`, `get_group()`, `get_categories()` — categories array from `\Elementor\Modules\DynamicTags\Module::*_CATEGORY` constants (TEXT, URL, COLOR, IMAGE, GALLERY, MEDIA, POST_META, NUMBER, KEY_VALUE_ARRAY, etc.).
- `get_content_type()` — `final` on free `Tag`/`Data_Tag` (`tag.php:64`, `data-tag.php:31`), so you don't (and can't) override it there; it's abstract only on a direct `Base_Tag` subclass.
- `render()` (Tag) — echo a string.
- `get_value( array $options = [] )` (Data_Tag) — return value matching the category's shape (e.g. IMAGE = `[ 'id' => ..., 'url' => ... ]`).
- `protected function register_controls()` — settings shown in the dynamic-tag popover.

## Register a group (optional)

```php
add_action( 'elementor/dynamic_tags/register', function( $dynamic_tags ) {
    $dynamic_tags->register_group( 'my-group', [ 'title' => __( 'My Group', 'td' ) ] );
} );
```

## Register the tag

Hook `elementor/dynamic_tags/register` (replaces deprecated `elementor/dynamic_tags/register_tags` — `core/dynamic-tags/manager.php:280-302`).

```php
add_action( 'elementor/dynamic_tags/register', function( $dynamic_tags ) {
    require_once __DIR__ . '/tags/my-tag.php';
    $dynamic_tags->register( new \My_Plugin\Tags\My_Tag() );
} );
```

## Gotchas

- Categories listed in `get_categories()` determine which controls accept your tag. A TEXT tag won't appear on a media control.
- Atomic 4.0 widgets use a separate dynamic-tags pipeline (`modules/atomic-widgets/dynamic-tags/`). Classic tags still work but get adapted via `Dynamic_Tags_Converter`. For new atomic-only tags, see `dynamic-prop-type.php` and `dynamic-tags-schemas.php`.
- Pro tag groups: AUTHOR, POST, COMMENTS, SITE, ARCHIVE, MEDIA, ACTION, WOOCOMMERCE (`elementor-pro/modules/dynamic-tags/module.php:17-31`). ACF / Pods / Toolset components register conditionally on plugin presence + license feature.
- For meta-driven tags use `Data_Tag` + POST_META category; do not echo the meta in `render()` of a plain Tag.

## Deploy & verify

Once registered on `elementor/dynamic_tags/register`, the tag becomes settable on controls and visible to MCP tools (`list-dynamic-tags` / `set-dynamic-tag`). To install on a live site and assert `dynamic_tags->get_tag_info('<name>')`, use `elementor-deploy-verify`.
