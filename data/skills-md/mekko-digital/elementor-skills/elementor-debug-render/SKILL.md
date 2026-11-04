---
name: elementor-debug-render
description: Diagnose blank, broken, or stale Elementor render — editor blank, preview OK but frontend stale, missing styles, atomic 4.0 e-* empty, _elementor_data issues, CSS regen. Use when an Elementor widget or page renders wrong.
---

# elementor-debug-render

Triage with the layered checklist in `resources/debug-checklist.md` only after you've placed the bug in one of these buckets:

## 1. Where does it break?

- **Editor (canvas blank, controls visible)** — classic widget `content_template()` is throwing or returning empty; or atomic prop schema rejected the saved value. Open browser devtools → Console for the React/Marionette error.
- **Editor preview iframe (canvas blank, panel works)** — server `render()` errors. Check PHP error log; preview iframe URL = `?elementor-preview=<post_id>`.
- **Frontend only (preview OK, live page blank/stale)** — almost always stale generated CSS or stale post-meta cache. See section 3.
- **Both preview + frontend broken** — `render()` bug, missing required setting, or `_elementor_data` JSON parse failure.

## 2. Verify the data

Post meta on any Elementor post (`wp_postmeta`):
- `_elementor_data` — JSON tree of elements. If unreadable, the editor will silently drop the page.
- `_elementor_edit_mode` — must be `'builder'` for Elementor to take over.
- `_elementor_version`, `_elementor_template_type`, `_elementor_page_settings`.
- `_elementor_css` — generated inline CSS, regenerated when the post is saved (`elementor-free/elementor/core/files/css/post.php`, `META_KEY = '_elementor_css'`).
- Element render cache is keyed by the global **option** `_elementor_element_cache_unique_id` (`modules/element-cache/module.php:17`), not post meta — changing/clearing that option busts all element cache.

WP-CLI: `wp post meta get <id> _elementor_data | jq .` to inspect; `wp elementor flush_css` to regenerate.

## 3. Regenerate / bust caches (most-common frontend fix)

In order, escalating:
1. Open the page in editor, save (regenerates `_elementor_css`, element cache, asset registry).
2. Elementor → Tools → "Regenerate CSS & Data".
3. Element-cache module: `Elementor\Modules\ElementCache\Module` — flush via Tools, or disable entirely by setting the `elementor_element_cache_ttl` option to `disable` (`wp option update elementor_element_cache_ttl disable`; the setting field is at `element-cache/module.php:130`, and updating the option auto-clears the cache @153). There is no `ELEMENTOR_*` constant for this.
4. Page-asset loader: each saved post stores its asset list. If JS for a widget isn't loading, the widget wasn't on the page when it was last saved — re-save.
5. Object cache / page cache plugin: flush after content edits.

## 4. Atomic 4.0 specific gotchas

Source roots: `elementor-free/elementor/modules/atomic-widgets/`.

- Atomic widgets have element types prefixed `e-` (e-button, e-heading, e-flexbox, …). Mixing classic + atomic on the same page is supported but they don't share the controls pipeline.
- `define_props_schema()` is the source of truth — a setting saved with a value that no longer matches the schema is dropped silently on load (`PropTypes/*::validate()`).
- `Has_Template` trait expects a `.twig` next to the PHP class. Missing file = empty render with no PHP error.
- Atomic styles ship as CSS classes generated from `Style_Definition`. If a style isn't applied, check the `classes` prop on the element and the styles_schema for that breakpoint.
- Atomic form (`e-form`) only loads when Pro is active AND experiment `e_pro_atomic_form` is on (`atomic-widgets/module.php:288`).
- Atomic dynamic tags use a separate pipeline (`atomic-widgets/dynamic-tags/`). A classic dynamic tag is auto-adapted via `Dynamic_Tags_Converter` — if conversion fails the binding is dropped.

## 5. When nothing obvious is wrong

- Safe mode: `?elementor-mode=safe` (free module `safe-mode/`).
- Disable Pro temporarily — many "free" widgets get Pro overrides (Posts via Loop, Form via atomic).
- Check `elementor/widget/render_content` (singular `widget`, `widget-base.php:662`) and `elementor/element/before_section_start` filters from other plugins.
- Read full checklist in `resources/debug-checklist.md`.

To reproduce/confirm a render bug on a real site (build a page, render it headlessly, watch for the fatal), use `elementor-deploy-verify`.
