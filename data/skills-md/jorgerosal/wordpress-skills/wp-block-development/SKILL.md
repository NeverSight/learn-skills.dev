---
name: wp-block-development
description: WordPress block editor code review and Gutenberg block development patterns for WordPress 6.x+. Use when reviewing block code, auditing block.json schema, checking editor components, validating render callbacks, analyzing block attributes, verifying InnerBlocks usage, detecting block validation errors, reviewing Interactivity API directives, or when user mentions "block review", "Gutenberg", "block development", "block editor", "block.json", "useBlockProps", "InnerBlocks", "Interactivity API", "data-wp-bind", "render_callback", "dynamic block", "static block", "block deprecation", "block attributes", "block supports", "@wordpress/scripts", "wp-scripts", "block validation error", "save function", "RichText", "InspectorControls", "BlockControls". Detects issues in block.json schema, React/JSX editor patterns, server-side rendering, attribute handling, and frontend interactions.
---

# WordPress Block Development Review Skill

## Overview

Systematic block development review for WordPress 6.x+ block editor (Gutenberg). **Core principle:** WordPress blocks follow a dual-architecture pattern—React components for the editor (edit function) and either static HTML (save function) or server-side PHP (render_callback/render file) for the frontend. block.json is the single source of truth. Review validates block.json schema, editor patterns (React/JSX), server-side rendering (PHP), attribute handling, deprecation management, and Interactivity API usage. Report findings grouped by file (PHP and JS/JSX files intermixed by actual path) with line numbers, severity labels (CRITICAL/WARNING/INFO), and BAD/GOOD code pairs.

**Note:** This skill reviews BOTH PHP and JavaScript/React code. PHP follows WordPress PHP Coding Standards (spaces in parentheses, `array()` not `[]`, Yoda conditions). JavaScript/JSX follows WordPress JS coding standards (tab indentation, JSDoc comments, camelCase for variables/functions, PascalCase for components).

## When to Use

**Use when:**
- Block plugin code review (single block, multi-block, or block library)
- block.json schema validation and field verification
- Editor component review (edit/save functions, React/JSX patterns)
- Render callback or render file audit (server-side PHP)
- InnerBlocks pattern review (nested blocks, template, templateLock)
- Block deprecation check (save function migrations)
- Interactivity API directive review (WP 6.5+ frontend interactions)
- Block attribute schema validation (type, source, selector, default)
- @wordpress/scripts build configuration check
- Block validation error investigation
- useBlockProps, RichText, InspectorControls, BlockControls usage

**Don't use for:**
- theme.json configuration (use wp-theme-development when available)
- General React application review (this is block-editor-specific)
- WooCommerce block extensions (use wp-woocommerce-dev when available)
- Security-only audits (use wp-security-review for comprehensive security analysis)
- Plugin architecture audits (use wp-plugin-development for plugin structure)
- Performance-only audits (use wp-performance-review)

## Code Review Workflow

Follow this seven-step workflow for systematic block reviews:

1. **Identify block type and context**
   - Single block plugin → One block.json, simple structure
   - Multi-block plugin → Multiple blocks in src/block-one/, src/block-two/
   - Block library/collection → Published as package, namespacing critical
   - Theme blocks → Registered in functions.php, different loading context

2. **Validate block.json schema (BLK-02, BLK-06, BLK-08, BLK-10)**
   - apiVersion must be 3 (WP 6.3+). Flag 1 or 2 as WARNING with upgrade guidance.
   - name must be "namespace/block-name" format (lowercase, letters, numbers, dashes)
   - title, category required
   - attributes: validate type, source, selector, default values. Flag type mismatches.
   - supports: color, spacing, typography, align, anchor, html
   - editorScript, script, viewScript, viewScriptModule: validate "file:./path" format
   - style, editorStyle: validate paths
   - render: "file:./render.php" for dynamic blocks
   - $schema field recommended for validation

3. **Check edit function (BLK-05, BLK-20)**
   - useBlockProps() MUST be called and spread on wrapper element
   - Import pattern: @wordpress/* packages (GOOD) vs window.wp.* (BAD - legacy)
   - InspectorControls for sidebar settings, BlockControls for toolbar
   - RichText proper usage (tagName, value, onChange, allowedFormats)
   - InnerBlocks with allowedBlocks and template props
   - useSelect/useDispatch from @wordpress/data (combine selectors in single useSelect call)
   - i18n: all user-facing strings wrapped in __() from @wordpress/i18n with text domain

4. **Check save function or render callback**
   - **Static blocks:** useBlockProps.save() MUST be called, RichText.Content for rich text, InnerBlocks.Content for nested blocks
   - **Dynamic blocks:** save returns null (or InnerBlocks.Content if nested blocks used - BLK-14 CRITICAL)
   - Save function must be DETERMINISTIC - no random values, no Date.now(), no side effects
   - **Render callback/render.php:** get_block_wrapper_attributes() for wrapper, escape all output (esc_html, esc_attr, esc_url, wp_kses_post but NOT on $content from InnerBlocks - BLK-21), defined( 'ABSPATH' ) || exit; at top

5. **Scan for CRITICAL patterns**
   - Missing apiVersion or using 1/2 instead of 3
   - window.wp.* instead of @wordpress/* imports in JS/JSX
   - save function without useBlockProps.save() (apiVersion 3)
   - render callback using wp_kses_post() on $content parameter (breaks embeds)
   - Dynamic block with InnerBlocks but save returns null (no InnerBlocks.Content)
   - Attribute with source: 'meta' (deprecated - use useEntityProp)
   - Invalid attribute type/source combination
   - Missing register_block_type() call in PHP

6. **Check WARNING patterns**
   - block.json missing supports field
   - edit function without useBlockProps()
   - Hardcoded strings not wrapped in __() in JS/JSX or PHP
   - render.php without get_block_wrapper_attributes()
   - PHP render files without defined( 'ABSPATH' ) check
   - save function with side effects (Math.random, Date.now)
   - Missing block.json $schema field
   - useSelect with multiple separate calls (performance anti-pattern)

7. **Note INFO improvements**
   - Using render_callback in PHP instead of render file in block.json
   - Missing viewScript/viewScriptModule in block.json (no frontend JS)
   - apiVersion 2 (suggest upgrade to 3)
   - Missing keywords in block.json
   - Not using block hooks for auto-insertion opportunities

Report using output format below. If security concerns found (unescaped render output, user input in Interactivity API state), add note: "Security issues detected. Run `/wp-sec-review` for comprehensive security analysis." If plugin architecture issues found (init hook registration, ABSPATH check missing), add note: "Plugin architecture issues detected. Run `/wp-plugin-review` for comprehensive plugin review."

**Source vs Build Review:** Review src/ files for code patterns (developer intent). Flag if build/ directory is missing or stale (check index.asset.php timestamp vs src/ modification times). Do NOT review build/ files for code quality - they are compiled output.

## File-Type Specific Checks

### block.json (BLK-02, BLK-06, BLK-08, BLK-10)

**apiVersion field:**
- CRITICAL: Missing apiVersion → Block won't register correctly
- WARNING: apiVersion 1 or 2 → Upgrade to 3 for iframe isolation (WP 6.3+)
- Pattern: `"apiVersion": 3`

**name field:**
- CRITICAL: Missing name → Block won't register
- CRITICAL: Invalid format (not "namespace/block-name") → Registration fails
- Pattern: `"name": "my-plugin/my-block"` (lowercase, dashes, letters, numbers)

**attributes field:**
- CRITICAL: Invalid type (not string/number/boolean/object/array/integer/null) → Validation fails
- CRITICAL: source:'meta' → Deprecated, use useEntityProp hook instead
- WARNING: type doesn't match source data type → Attribute won't populate correctly
- Pattern: Validate type, source, selector, default combinations
- Sources: attribute, text, html, query (meta deprecated)

**supports field:**
- WARNING: Missing supports → Users can't customize color/spacing/typography
- INFO: Could add common supports (color, spacing, typography, align, anchor)
- Pattern: Object with nested configuration for each support type

**editorScript/script/viewScript/viewScriptModule fields:**
- WARNING: Invalid path format → Assets won't load
- Pattern: `"file:./index.js"` relative to block.json location
- Note: viewScriptModule for Interactivity API (WP 6.5+)

**render field:**
- INFO: Dynamic blocks can use render file instead of render_callback
- Pattern: `"file:./render.php"` relative to block.json location

**$schema field:**
- INFO: Missing $schema → Can't validate schema in IDE
- Pattern: `"$schema": "https://schemas.wp.org/trunk/block.json"`

### Edit function / edit.js (BLK-05, BLK-20)

**useBlockProps usage:**
- CRITICAL: useBlockProps() not called → Block won't render properly in editor
- CRITICAL: useBlockProps result not spread on wrapper → Missing block classes/attributes
- Pattern: `const blockProps = useBlockProps();` then `<div { ...blockProps }>`

**Import patterns:**
- WARNING: window.wp.* global access → Legacy pattern, breaks modern builds
- Pattern: GOOD: `import { useBlockProps } from '@wordpress/block-editor';` BAD: `const { useBlockProps } = window.wp.blockEditor;`

**InspectorControls and BlockControls:**
- INFO: Could add settings sidebar with InspectorControls
- INFO: Could add toolbar controls with BlockControls
- Pattern: InspectorControls for PanelBody/ToggleControl/SelectControl, BlockControls for AlignmentToolbar/ToolbarGroup

**RichText usage:**
- WARNING: RichText without tagName → May render incorrectly
- WARNING: RichText without value/onChange → Not controlled component
- Pattern: `<RichText tagName="p" value={ attributes.content } onChange={ ( content ) => setAttributes( { content } ) } />`

**InnerBlocks usage:**
- INFO: Consider allowedBlocks to restrict nesting
- INFO: Consider template for default block structure
- Pattern: `<InnerBlocks allowedBlocks={ [ 'core/paragraph' ] } template={ [ [ 'core/heading' ] ] } />`

**useSelect/useDispatch performance:**
- WARNING: Multiple separate useSelect calls → Performance degradation with many blocks
- Pattern: Combine selectors in single useSelect when reading multiple values

**Internationalization:**
- WARNING: Hardcoded strings without __() → Not translatable
- Pattern: `__( 'Text', 'text-domain' )` for all user-facing strings

### Save function / save.js (BLK-05, BLK-07)

**Static blocks (save returns JSX):**
- CRITICAL: Missing useBlockProps.save() → Block validation error (apiVersion 3)
- WARNING: RichText without RichText.Content → Won't save rich text correctly
- WARNING: InnerBlocks without InnerBlocks.Content → Nested blocks won't save
- Pattern: `const blockProps = useBlockProps.save();` then `<div { ...blockProps }>`

**Dynamic blocks (save returns null or InnerBlocks.Content):**
- CRITICAL: Dynamic block with InnerBlocks but save returns null → Nested blocks lost (BLK-14)
- Pattern: If block uses InnerBlocks, save MUST return `<InnerBlocks.Content />` even for dynamic blocks

**Deterministic save:**
- WARNING: Math.random() or Date.now() in save → Block validation errors on re-save
- WARNING: Side effects in save → Unpredictable behavior
- Pattern: Save must return identical markup for identical attributes

### Render callback / render.php (BLK-11)

**ABSPATH check:**
- WARNING: Missing defined( 'ABSPATH' ) || exit; → Direct file access possible
- Pattern: First line after <?php should be ABSPATH check
- Cross-reference: See wp-security-review for security depth

**get_block_wrapper_attributes():**
- WARNING: Manual class concatenation instead of get_block_wrapper_attributes() → Missing block supports
- Pattern: `$wrapper_attributes = get_block_wrapper_attributes();` then `<div <?php echo $wrapper_attributes; ?>>`

**Output escaping:**
- CRITICAL: Unescaped output → XSS vulnerability (CWE-79)
- CRITICAL: wp_kses_post() on $content from InnerBlocks → Breaks embeds (BLK-21)
- Pattern: esc_html() for text, esc_attr() for attributes, esc_url() for URLs, wp_kses_post() for trusted HTML (but NOT InnerBlocks $content)
- Cross-reference: See wp-security-review for comprehensive escaping patterns

**Function parameters:**
- $attributes: Array of block attributes
- $content: InnerBlocks HTML (if InnerBlocks used)
- $block: WP_Block instance with context and other metadata
- Pattern: Use all three parameters for full dynamic block functionality

### Plugin main file / plugin.php

**register_block_type():**
- CRITICAL: Missing register_block_type() → Block won't register
- WARNING: Not hooked to 'init' → May register too early
- Pattern: `add_action( 'init', 'callback' );` then `register_block_type( __DIR__ . '/build/block-name' );`

**Multi-block registration:**
- WARNING: Single register_block_type() for multi-block plugin → Other blocks won't register
- Pattern: Call register_block_type() for each block's build directory

**Plugin header and ABSPATH:**
- Cross-reference: See wp-plugin-development for plugin header requirements and ABSPATH check

### Block deprecation (BLK-09)

**deprecated array:**
- CRITICAL: Save function changed without deprecation → Block validation errors for existing content
- WARNING: Missing apiVersion in deprecation entry → Deprecation may not match
- Pattern: deprecated array with save + attributes for each version

**migrate function:**
- INFO: Could add migrate function for attribute schema changes
- Pattern: `migrate( attributes ) { return { ...attributes, newField: 'default' }; }`

**Ordering:**
- WARNING: Deprecations ordered oldest first → WordPress checks newest first, performance issue
- Pattern: Newest deprecation listed FIRST in array

### Interactivity API files (BLK-12)

**WP 6.5+ version marker:**
- INFO: Interactivity API requires WordPress 6.5+ → Add version check or plugin requirement
- Pattern: Check `Requires at least: 6.5` in plugin header

**render.php directives:**
- data-wp-interactive="namespace" → REQUIRED for Interactivity API scope
- wp_interactivity_state() → Server-side state initialization
- wp_interactivity_config() → Server-side configuration
- data-wp-context → Context provider for nested elements
- Directives: data-wp-bind, data-wp-on, data-wp-class, data-wp-style, data-wp-text, data-wp-watch, data-wp-init, data-wp-each

**view.js (frontend store):**
- WARNING: Import from window.wp.interactivity → Legacy pattern, use @wordpress/interactivity
- Pattern: `import { store } from '@wordpress/interactivity';` then `store( 'namespace', { actions, state } );`

**Key distinction:**
- Interactivity API = FRONTEND ONLY (view.js, render.php directives)
- Editor still uses React (edit.js)
- Don't confuse frontend state management with editor component state

**Security crossover:**
- WARNING: User input in wp_interactivity_state() without sanitization → XSS risk
- Cross-reference: See wp-security-review for input sanitization patterns

### Block context (BLK-16)

**providesContext (parent block):**
- Pattern: In parent block.json: `"providesContext": { "myPlugin/keyName": "attributeName" }`
- Namespace context keys: Use "myPlugin/keyName" format

**usesContext (child block):**
- Pattern: In child block.json: `"usesContext": [ "myPlugin/keyName" ]`
- Access in edit: `function Edit( { context } ) { const value = context['myPlugin/keyName']; }`

### Surface-level checks

**Block transforms (BLK-13 partial):**
- INFO: Could add transforms for conversion from/to other blocks
- Pattern: from/to array in block registration

**Block variations (BLK-13):**
- INFO: Could add variations for preset configurations
- Pattern: variation picker, isDefault, scope properties

**Block styles:**
- INFO: Could register style variations in block.json or PHP
- Pattern: styles array in block.json or register_block_style() in PHP

**Block patterns (BLK-18):**
- Pattern: register_block_pattern() structure, categories, keywords
- Note: Patterns are multi-block layouts, different from variations (single block presets)

**Block hooks (BLK-19):**
- INFO: Could use blockHooks for auto-insertion (WP 6.4+)
- CRITICAL: Block hooks only work with dynamic blocks (save returns null)
- Pattern: blockHooks property in block.json

**Block Bindings API (BLK-17):**
- INFO: Could use bindings for dynamic attribute connections (WP 6.5+)
- Pattern: Surface-level detection only

**@wordpress/scripts build config:**
- WARNING: Missing @wordpress/scripts → No build toolchain
- WARNING: package.json missing build/start scripts → Can't compile blocks
- Pattern: Check package.json for "scripts": { "build": "wp-scripts build", "start": "wp-scripts start" }

**Template lock:**
- INFO: Could use templateLock on InnerBlocks for fixed layouts
- Pattern: `<InnerBlocks templateLock="all" />` prevents block addition/removal/reordering

## Search Patterns for Quick Detection (BLK-22)

Use these `rg` commands for quick block scanning. Organized by severity. Cover BOTH PHP and JS/JSX files.

### CRITICAL Patterns

```bash
# block.json without apiVersion 3
rg -l --iglob 'block.json' . | xargs -I{} sh -c "rg -q '\"apiVersion\"\\s*:\\s*3' '{}' || echo '{}'"

# JS/JSX files with window.wp.* instead of @wordpress/* imports
rg -n "window\.wp\." . -g '*.{js,jsx}'

# save function without useBlockProps.save() in JSX files (manual candidate list)
rg -n "function save|const save\s*=|save:\s*\(" . -g '*.{js,jsx}'

# render callback using wp_kses_post on $content parameter (breaks embeds)
rg -n "wp_kses_post\s*\(\s*\$content\s*\)" . -g '*.php'

# Dynamic block with InnerBlocks but save returns null
# Manual check: if edit.js uses InnerBlocks, save.js should include InnerBlocks.Content.
rg -n "InnerBlocks" . -g '*.{js,jsx}'
rg -n "return\s+null" . -g '*.{js,jsx}'

# Attribute with source: 'meta' (deprecated)
rg -n "\"source\"\s*:\s*\"meta\"" . -g 'block.json'

# Missing register_block_type() call in plugin bootstrap files
rg -n "register_block_type\s*\(" . -g '*.php'
```

### WARNING Patterns

```bash
# block.json missing supports field
rg -l --iglob 'block.json' . | xargs -I{} sh -c "rg -q '\"supports\"' '{}' || echo '{}'"

# edit function without useBlockProps() in JS/JSX files (manual candidate list)
rg -n "function Edit|export default function Edit|const Edit\s*=" . -g '*.{js,jsx}'

# Hardcoded strings not wrapped in __() in JS/JSX files
rg -n "title\s*:\s*['\"][A-Z]" . -g '*.{js,jsx}'

# render.php without get_block_wrapper_attributes()
rg -l --iglob 'render.php' . | xargs -I{} sh -c "rg -q 'get_block_wrapper_attributes' '{}' || echo '{}'"

# PHP render files without defined( 'ABSPATH' ) check
rg -l --iglob 'render.php' . | xargs -I{} sh -c "rg -q 'defined.*ABSPATH' '{}' || echo '{}'"

# save function with side effects (Math.random, Date.now)
rg -n "Math\.random|Date\.now|new Date\(" . -g 'save.js'

# Missing block.json $schema field
rg -l --iglob 'block.json' . | xargs -I{} sh -c "rg -q '\"\\$schema\"' '{}' || echo '{}'"

# useSelect with multiple separate calls (performance anti-pattern)
# Manual check: inspect files with repeated useSelect() calls.
rg -n "useSelect\s*\(" . -g '*.{js,jsx}'
```

### INFO Patterns

```bash
# Using render_callback in PHP instead of render file in block.json
grep -rn "render_callback" --include="*.php" .

# Missing viewScript/viewScriptModule in block.json (no frontend JS)
grep -L "viewScript\|viewScriptModule" --include="block.json" .

# apiVersion 2 (suggest upgrade to 3)
grep -rn "\"apiVersion\": 2" --include="block.json" .

# Missing keywords in block.json
grep -L "\"keywords\"" --include="block.json" .

# Not using block hooks for auto-insertion opportunities
# (Manual check: Review block purpose for auto-insertion potential)
```

**Note:** Grep patterns for JavaScript require different regex than PHP patterns. Use `--include="*.js" --include="*.jsx"` for JS files, `--include="*.php"` for PHP files.

## Block Context Detection

Context-aware review notes based on block distribution and loading context:

### Single block plugin
**Structure:** One block.json at root or src/, single build output
**Review adjustments:** Standard review, no special considerations
**Pattern:** Plugin folder contains single src/ directory with index.js, edit.js, save.js

### Multi-block plugin
**Structure:** Multiple blocks in src/block-one/, src/block-two/, each with block.json
**Review adjustments:**
- Check shared components in src/shared/ or src/components/
- Verify consistent naming conventions across all blocks
- Ensure build config handles all blocks (multiple entry points or wildcard)
- Verify register_block_type() called for each block's build directory
**Pattern:** Plugin folder contains multiple src/*/block.json files

### Block library/collection
**Structure:** Published as npm package or WordPress.org plugin with multiple blocks
**Review adjustments:**
- Namespacing CRITICAL (all blocks must use consistent namespace)
- Check for consistent naming: "namespace/block-one", "namespace/block-two"
- Verify all blocks in same namespace
- Package.json should have "main" field pointing to build entry
**Pattern:** package.json has "name" field, published to npm or WordPress.org

### Theme blocks
**Structure:** Registered in functions.php, block files in /blocks/ or /inc/blocks/
**Review adjustments:**
- Different loading context (theme activation vs plugin activation)
- Block may depend on theme.json settings (colors, spacing, typography)
- Brief note on theme.json integration, defer depth to Phase 4 (Theme Development)
- Verify blocks registered on 'init' or 'after_setup_theme' hook
**Pattern:** register_block_type() in functions.php, blocks in theme subdirectory

## Quick Reference: Block Development Patterns (BLK-23)

Common block patterns organized by concern. All examples use WordPress coding standards (PHP: spaces in parentheses, `array()` not `[]`, Yoda conditions; JS: tab indentation, camelCase, PascalCase for components).

### block.json Schema

Complete schema with all fields annotated (apiVersion 3):

```json
{
	"$schema": "https://schemas.wp.org/trunk/block.json",
	"apiVersion": 3,
	"name": "my-plugin/my-block",
	"title": "My Block",
	"category": "widgets",
	"icon": "smiley",
	"description": "A custom block example",
	"keywords": [ "custom", "example" ],
	"version": "1.0.0",
	"textdomain": "my-plugin",
	"attributes": {
		"content": {
			"type": "string",
			"source": "html",
			"selector": "p",
			"default": ""
		},
		"showImage": {
			"type": "boolean",
			"default": false
		}
	},
	"supports": {
		"html": false,
		"color": {
			"background": true,
			"text": true
		},
		"spacing": {
			"margin": true,
			"padding": true
		},
		"typography": {
			"fontSize": true,
			"lineHeight": true
		},
		"align": [ "wide", "full" ],
		"anchor": true
	},
	"editorScript": "file:./index.js",
	"editorStyle": "file:./index.css",
	"style": "file:./style-index.css",
	"viewScriptModule": "file:./view.js"
}
```

### Block Registration

PHP + JS registration pattern:

**❌ BAD: Missing ABSPATH check, not hooked to init**
```php
<?php
function my_plugin_register_block() {
	register_block_type( __DIR__ . '/build/my-block' );
}
my_plugin_register_block(); // Runs immediately, not on init
```

**✅ GOOD: Complete registration with ABSPATH and init hook**
```php
<?php
defined( 'ABSPATH' ) || exit;

function my_plugin_register_blocks() {
	register_block_type( __DIR__ . '/build/my-block' );
}
add_action( 'init', 'my_plugin_register_blocks' );
```

**✅ GOOD: Multi-block registration**
```php
<?php
defined( 'ABSPATH' ) || exit;

function my_plugin_register_blocks() {
	register_block_type( __DIR__ . '/build/block-one' );
	register_block_type( __DIR__ . '/build/block-two' );
	register_block_type( __DIR__ . '/build/block-three' );
}
add_action( 'init', 'my_plugin_register_blocks' );
```

### Static Block Pattern

Edit with useBlockProps, save with useBlockProps.save, RichText + RichText.Content:

**❌ BAD: Missing useBlockProps in edit and save**
```javascript
// edit.js
export default function Edit( { attributes, setAttributes } ) {
	return (
		<div className="my-block">
			<input
				value={ attributes.content }
				onChange={ ( e ) => setAttributes( { content: e.target.value } ) }
			/>
		</div>
	);
}

// save.js
export default function save( { attributes } ) {
	return (
		<div className="my-block">
			<p>{ attributes.content }</p>
		</div>
	);
}
```

**✅ GOOD: Complete static block with useBlockProps and RichText**
```javascript
// edit.js
import { useBlockProps, RichText } from '@wordpress/block-editor';

export default function Edit( { attributes, setAttributes } ) {
	const blockProps = useBlockProps();

	return (
		<div { ...blockProps }>
			<RichText
				tagName="p"
				value={ attributes.content }
				onChange={ ( content ) => setAttributes( { content } ) }
				placeholder="Enter content..."
			/>
		</div>
	);
}

// save.js
import { useBlockProps, RichText } from '@wordpress/block-editor';

export default function save( { attributes } ) {
	const blockProps = useBlockProps.save();

	return (
		<div { ...blockProps }>
			<RichText.Content tagName="p" value={ attributes.content } />
		</div>
	);
}
```

### Dynamic Block Pattern

Edit with useBlockProps, save returns null (or InnerBlocks.Content), render.php with get_block_wrapper_attributes and escaping:

**❌ BAD: render callback without wrapper attributes, unescaped output**
```php
<?php
function my_plugin_render_callback( $attributes ) {
	return '<div><p>' . $attributes['content'] . '</p></div>';
}
```

**✅ GOOD: Complete dynamic block with proper escaping**
```php
<?php
// render.php
defined( 'ABSPATH' ) || exit;

$wrapper_attributes = get_block_wrapper_attributes();
?>
<div <?php echo $wrapper_attributes; ?>>
	<p><?php echo esc_html( $attributes['content'] ); ?></p>
</div>
```

```javascript
// save.js - Dynamic blocks return null
export default function save() {
	return null;
}
```

**✅ GOOD: Dynamic block registered with render file**
```php
<?php
// plugin.php
defined( 'ABSPATH' ) || exit;

function my_plugin_register_blocks() {
	register_block_type( __DIR__ . '/build/my-block' );
	// render file specified in block.json "render": "file:./render.php"
}
add_action( 'init', 'my_plugin_register_blocks' );
```

### InnerBlocks Pattern

allowedBlocks, template, templateLock, InnerBlocks.Content in save (even for dynamic blocks):

**❌ BAD: Dynamic block with InnerBlocks but save returns null**
```javascript
// edit.js
import { useBlockProps, InnerBlocks } from '@wordpress/block-editor';

export default function Edit() {
	const blockProps = useBlockProps();
	return (
		<div { ...blockProps }>
			<InnerBlocks />
		</div>
	);
}

// save.js - CRITICAL: Nested blocks will be lost!
export default function save() {
	return null;
}
```

**✅ GOOD: Dynamic block with InnerBlocks saves nested content**
```javascript
// edit.js
import { useBlockProps, InnerBlocks } from '@wordpress/block-editor';

export default function Edit() {
	const blockProps = useBlockProps();
	const ALLOWED_BLOCKS = [ 'core/paragraph', 'core/image', 'core/heading' ];
	const TEMPLATE = [
		[ 'core/heading', { placeholder: 'Card Title' } ],
		[ 'core/paragraph', { placeholder: 'Card content...' } ],
	];

	return (
		<div { ...blockProps }>
			<InnerBlocks
				allowedBlocks={ ALLOWED_BLOCKS }
				template={ TEMPLATE }
				templateLock={ false }
			/>
		</div>
	);
}

// save.js - MUST save InnerBlocks.Content even for dynamic blocks
import { InnerBlocks } from '@wordpress/block-editor';

export default function save() {
	return <InnerBlocks.Content />;
}
```

**✅ GOOD: render.php uses $content parameter for InnerBlocks HTML**
```php
<?php
// render.php
defined( 'ABSPATH' ) || exit;

$wrapper_attributes = get_block_wrapper_attributes();
?>
<div <?php echo $wrapper_attributes; ?>>
	<h3><?php echo esc_html( $attributes['title'] ); ?></h3>
	<?php echo $content; // InnerBlocks HTML - DO NOT use wp_kses_post() ?>
</div>
```

### useBlockProps

edit (useBlockProps()) and save (useBlockProps.save()), merging custom props:

**❌ BAD: Missing useBlockProps**
```javascript
export default function Edit() {
	return <div className="my-block">Content</div>;
}

function save() {
	return <div className="my-block">Content</div>;
}
```

**✅ GOOD: useBlockProps with custom props merged**
```javascript
import { useBlockProps } from '@wordpress/block-editor';

export default function Edit( { attributes } ) {
	const blockProps = useBlockProps( {
		className: 'my-custom-class',
		style: { backgroundColor: attributes.bgColor },
	} );

	return <div { ...blockProps }>Content</div>;
}

function save( { attributes } ) {
	const blockProps = useBlockProps.save( {
		className: 'my-custom-class',
		style: { backgroundColor: attributes.bgColor },
	} );

	return <div { ...blockProps }>Content</div>;
}
```

### Attributes

type/source/selector/default patterns, attribute type matching:

**❌ BAD: Type mismatch, no default, deprecated source**
```json
{
	"attributes": {
		"count": {
			"type": "number",
			"source": "text",
			"selector": ".count"
		},
		"metaValue": {
			"type": "string",
			"source": "meta",
			"meta": "my_meta_key"
		}
	}
}
```

**✅ GOOD: Correct type/source matching, defaults, modern patterns**
```json
{
	"attributes": {
		"content": {
			"type": "string",
			"source": "html",
			"selector": "p",
			"default": ""
		},
		"count": {
			"type": "number",
			"source": "attribute",
			"selector": ".count",
			"attribute": "data-count",
			"default": 0
		},
		"url": {
			"type": "string",
			"source": "attribute",
			"selector": "a",
			"attribute": "href",
			"default": ""
		},
		"items": {
			"type": "array",
			"source": "query",
			"selector": "li",
			"query": {
				"text": {
					"type": "string",
					"source": "text"
				}
			},
			"default": []
		}
	}
}
```

**✅ GOOD: Meta attribute using useEntityProp (not deprecated source)**
```javascript
import { useEntityProp } from '@wordpress/core-data';

export default function Edit() {
	const [ meta, setMeta ] = useEntityProp( 'postType', 'post', 'meta' );
	const value = meta.my_meta_key;

	const updateMeta = ( newValue ) => {
		setMeta( { ...meta, my_meta_key: newValue } );
	};

	// Use value and updateMeta in component
}
```

### Block Controls

InspectorControls for sidebar, BlockControls for toolbar, PanelBody, ToggleControl, SelectControl:

**❌ BAD: Settings hardcoded in block markup, no sidebar controls**
```javascript
export default function Edit( { attributes, setAttributes } ) {
	return (
		<div>
			<label>
				Show Image:
				<input
					type="checkbox"
					checked={ attributes.showImage }
					onChange={ ( e ) => setAttributes( { showImage: e.target.checked } ) }
				/>
			</label>
		</div>
	);
}
```

**✅ GOOD: InspectorControls for sidebar, BlockControls for toolbar**
```javascript
import { useBlockProps, InspectorControls, BlockControls, AlignmentToolbar } from '@wordpress/block-editor';
import { PanelBody, ToggleControl, SelectControl } from '@wordpress/components';
import { __ } from '@wordpress/i18n';

export default function Edit( { attributes, setAttributes } ) {
	const blockProps = useBlockProps();

	return (
		<>
			<BlockControls>
				<AlignmentToolbar
					value={ attributes.align }
					onChange={ ( align ) => setAttributes( { align } ) }
				/>
			</BlockControls>

			<InspectorControls>
				<PanelBody title={ __( 'Settings', 'my-plugin' ) }>
					<ToggleControl
						label={ __( 'Show featured image', 'my-plugin' ) }
						checked={ attributes.showImage }
						onChange={ ( showImage ) => setAttributes( { showImage } ) }
					/>
					<SelectControl
						label={ __( 'Display style', 'my-plugin' ) }
						value={ attributes.style }
						options={ [
							{ label: 'Default', value: 'default' },
							{ label: 'Card', value: 'card' },
							{ label: 'List', value: 'list' },
						] }
						onChange={ ( style ) => setAttributes( { style } ) }
					/>
				</PanelBody>
			</InspectorControls>

			<div { ...blockProps }>
				{/* Block content */}
			</div>
		</>
	);
}
```

### Block Deprecation

deprecated array, save + attributes + migrate, apiVersion in entries, newest first:

**❌ BAD: Save function changed without deprecation**
```javascript
// Changed save markup - existing blocks will show validation error
function save( { attributes } ) {
	const blockProps = useBlockProps.save();
	return <div { ...blockProps }>{ attributes.content }</div>;
}
```

**✅ GOOD: Deprecation entry for old save function**
```javascript
import { useBlockProps } from '@wordpress/block-editor';

const deprecated = [
	{
		// Version 2: Added useBlockProps (newest deprecation first)
		apiVersion: 2,
		attributes: {
			content: { type: 'string' },
		},
		save( { attributes } ) {
			return <div className="my-block">{ attributes.content }</div>;
		},
	},
	{
		// Version 1: Original block
		apiVersion: 2,
		attributes: {
			content: { type: 'string' },
		},
		save( { attributes } ) {
			return <p>{ attributes.content }</p>;
		},
		migrate( attributes ) {
			// Transform old attributes to new schema
			return {
				...attributes,
				newField: 'default',
			};
		},
	},
];

// Current version
function save( { attributes } ) {
	const blockProps = useBlockProps.save();
	return <div { ...blockProps }>{ attributes.content }</div>;
}

export default {
	edit: Edit,
	save,
	deprecated,
};
```

### Interactivity API

data-wp-interactive, data-wp-bind, data-wp-on, store(), wp_interactivity_state(), frontend-only emphasis:

**❌ BAD: Custom JavaScript for frontend interaction**
```php
<?php
// render.php
?>
<div class="my-block">
	<button id="toggle-button">Toggle</button>
	<div id="content" style="display: none;">Hidden content</div>
</div>
<script>
	document.getElementById('toggle-button').addEventListener('click', function() {
		var content = document.getElementById('content');
		content.style.display = content.style.display === 'none' ? 'block' : 'none';
	});
</script>
```

**✅ GOOD: Interactivity API with directives (WP 6.5+)**
```php
<?php
// render.php
defined( 'ABSPATH' ) || exit;

wp_interactivity_state( 'myPlugin', array(
	'isOpen' => false,
) );

$wrapper_attributes = get_block_wrapper_attributes();
?>
<div
	<?php echo $wrapper_attributes; ?>
	data-wp-interactive="myPlugin"
	data-wp-context='{ "id": "<?php echo esc_attr( uniqid() ); ?>" }'
>
	<button data-wp-on--click="actions.toggle">
		<?php esc_html_e( 'Toggle', 'my-plugin' ); ?>
	</button>
	<div data-wp-bind--hidden="!state.isOpen">
		<p><?php esc_html_e( 'Hidden content', 'my-plugin' ); ?></p>
	</div>
</div>
```

```javascript
// view.js - Frontend store (NOT editor code)
import { store } from '@wordpress/interactivity';

store( 'myPlugin', {
	state: {
		isOpen: false,
	},
	actions: {
		toggle: ( { state } ) => {
			state.isOpen = ! state.isOpen;
		},
	},
} );
```

**block.json configuration:**
```json
{
	"viewScriptModule": "file:./view.js"
}
```

**Note:** Interactivity API is for FRONTEND only. Editor still uses React (edit.js).

### Import Patterns

@wordpress/* package imports vs window.wp.* legacy access:

**❌ BAD: window.wp.* global access (legacy)**
```javascript
const { registerBlockType } = window.wp.blocks;
const { useBlockProps } = window.wp.blockEditor;
const { __ } = window.wp.i18n;
```

**✅ GOOD: @wordpress/* package imports (modern)**
```javascript
import { registerBlockType } from '@wordpress/blocks';
import { useBlockProps } from '@wordpress/block-editor';
import { __ } from '@wordpress/i18n';
```

### Block Supports

color, spacing, typography, align, anchor in block.json:

**❌ BAD: Missing supports field**
```json
{
	"name": "my-plugin/my-block",
	"title": "My Block"
}
```

**✅ GOOD: Complete supports configuration**
```json
{
	"name": "my-plugin/my-block",
	"title": "My Block",
	"supports": {
		"html": false,
		"color": {
			"background": true,
			"text": true,
			"gradients": true,
			"link": true
		},
		"spacing": {
			"margin": true,
			"padding": true,
			"blockGap": true
		},
		"typography": {
			"fontSize": true,
			"lineHeight": true,
			"fontFamily": true,
			"fontWeight": true
		},
		"align": [ "wide", "full" ],
		"anchor": true
	}
}
```

### Block Variations

variation objects with attributes and innerBlocks:

```javascript
import { registerBlockVariation } from '@wordpress/blocks';

registerBlockVariation( 'core/columns', {
	name: 'three-columns-equal',
	title: 'Three Columns (Equal)',
	description: 'Three columns with equal width',
	icon: 'columns',
	isDefault: false,
	scope: [ 'block' ],
	attributes: {
		columns: 3,
	},
	innerBlocks: [
		[ 'core/column' ],
		[ 'core/column' ],
		[ 'core/column' ],
	],
} );
```

### Block Transforms

from/to patterns:

```javascript
import { createBlock } from '@wordpress/blocks';

export default {
	edit: Edit,
	save,
	transforms: {
		from: [
			{
				type: 'block',
				blocks: [ 'core/paragraph' ],
				transform: ( { content } ) => {
					return createBlock( 'my-plugin/my-block', {
						content,
					} );
				},
			},
		],
		to: [
			{
				type: 'block',
				blocks: [ 'core/paragraph' ],
				transform: ( { content } ) => {
					return createBlock( 'core/paragraph', {
						content,
					} );
				},
			},
		],
	},
};
```

### Block Context

providesContext/usesContext:

```json
// Parent block.json
{
	"providesContext": {
		"myPlugin/userId": "userId",
		"myPlugin/userName": "userName"
	},
	"attributes": {
		"userId": { "type": "number" },
		"userName": { "type": "string" }
	}
}
```

```json
// Child block.json
{
	"usesContext": [ "myPlugin/userId", "myPlugin/userName" ]
}
```

```javascript
// Child edit.js
export default function Edit( { context } ) {
	const userId = context['myPlugin/userId'];
	const userName = context['myPlugin/userName'];

	return (
		<div>
			<p>User: { userName } ({ userId })</p>
		</div>
	);
}
```

### Block Hooks

blockHooks with dynamic blocks only:

**❌ BAD: Block hooks with static block**
```json
{
	"blockHooks": {
		"core/post-content": "after"
	}
}
```

```javascript
// save.js - Static save = block hooks won't work
function save() {
	return <div>Content</div>;
}
```

**✅ GOOD: Block hooks with dynamic block**
```json
{
	"blockHooks": {
		"core/post-content": "after"
	},
	"render": "file:./render.php"
}
```

```javascript
// save.js - Dynamic block (null save) = block hooks work
function save() {
	return null;
}
```

### @wordpress/scripts

package.json scripts configuration:

**❌ BAD: Missing build scripts**
```json
{
	"scripts": {
		"test": "echo \"No build toolchain configured\""
	}
}
```

**✅ GOOD: Complete @wordpress/scripts configuration**
```json
{
	"scripts": {
		"build": "wp-scripts build",
		"start": "wp-scripts start",
		"lint:js": "wp-scripts lint-js",
		"format": "wp-scripts format",
		"packages-update": "wp-scripts packages-update"
	},
	"devDependencies": {
		"@wordpress/scripts": "^27.0.0"
	}
}
```

## Severity Definitions (BLK-24)

| Severity | Definition | Examples |
|----------|------------|----------|
| **CRITICAL** | Block won't render OR crashes editor OR causes block validation error | Missing apiVersion or using apiVersion 1/2 without migration path, invalid attribute type causing save validation error, save function mismatch without deprecation entry, missing useBlockProps.save() in apiVersion 3 block, InnerBlocks in edit but save returns null (not InnerBlocks.Content), wp_kses_post() on InnerBlocks $content parameter, window.wp.* access breaking modern build, missing register_block_type() call, deprecated source:'meta' attribute pattern |
| **WARNING** | Block works but has quality/compatibility issues OR non-standard patterns | Deprecated API usage (apiVersion 1/2 without critical issues), missing block supports (color, spacing, typography), no deprecation handler for changed save function, hardcoded strings without i18n in JS/JSX or PHP, multiple separate useSelect calls (performance issue), missing get_block_wrapper_attributes() in render.php, missing defined( 'ABSPATH' ) in PHP files, save function with side effects (Math.random, Date.now) |
| **INFO** | Best practice improvements OR optimization opportunities | Could use render PHP file instead of render_callback function, missing viewScript/viewScriptModule for frontend interactions, not using block.json $schema field, apiVersion 2 (upgrade to 3 available), missing keywords in block.json, block hooks opportunity for auto-insertion, could add block variations for common presets, missing template lock on fixed InnerBlocks layouts |

## Output Format (BLK-24)

Report findings grouped by FILE (PHP and JS/JSX files intermixed by actual file path), with line numbers and severity labels. Use BAD/GOOD code pairs for each finding.

```markdown
# WordPress Block Review: my-block-plugin

## FILE: src/index.js

### Line 3: WARNING - Legacy global access
window.wp.* access is legacy pattern. Use @wordpress/* package imports for modern build toolchain.

❌ **BAD:**
```javascript
const { registerBlockType } = window.wp.blocks;
```

✅ **GOOD:**
```javascript
import { registerBlockType } from '@wordpress/blocks';
```

## FILE: src/edit.js

### Line 12: CRITICAL - Missing useBlockProps
useBlockProps() not called in edit function. Block won't render correctly in editor.

❌ **BAD:**
```javascript
export default function Edit() {
	return <div className="my-block">Content</div>;
}
```

✅ **GOOD:**
```javascript
import { useBlockProps } from '@wordpress/block-editor';

export default function Edit() {
	const blockProps = useBlockProps();
	return <div { ...blockProps }>Content</div>;
}
```

## FILE: src/save.js

### Line 5: CRITICAL - Missing useBlockProps.save()
apiVersion 3 blocks require useBlockProps.save(). Block validation errors will occur.

❌ **BAD:**
```javascript
function save() {
	return <div className="my-block">Content</div>;
}
```

✅ **GOOD:**
```javascript
import { useBlockProps } from '@wordpress/block-editor';

function save() {
	const blockProps = useBlockProps.save();
	return <div { ...blockProps }>Content</div>;
}
```

## FILE: render.php

### Line 15: CRITICAL - wp_kses_post on InnerBlocks content
Using wp_kses_post() on $content breaks embed blocks and oEmbed processing. InnerBlocks content is already sanitized.

❌ **BAD:**
```php
<?php echo wp_kses_post( $content ); ?>
```

✅ **GOOD:**
```php
<?php echo $content; // InnerBlocks already sanitized ?>
```

### Line 1: WARNING - Missing ABSPATH check
Add ABSPATH check at top of file to prevent direct access.

❌ **BAD:**
```php
<?php
$wrapper_attributes = get_block_wrapper_attributes();
```

✅ **GOOD:**
```php
<?php
defined( 'ABSPATH' ) || exit;

$wrapper_attributes = get_block_wrapper_attributes();
```

## FILE: block.json

### Line 2: WARNING - apiVersion 2 (upgrade available)
apiVersion 2 still works but upgrade to 3 recommended for iframe editor isolation (WP 6.3+).

❌ **BAD:**
```json
{
	"apiVersion": 2
}
```

✅ **GOOD:**
```json
{
	"apiVersion": 3
}
```

### Line 10: INFO - Missing $schema field
Add $schema field for IDE validation support.

```json
{
	"$schema": "https://schemas.wp.org/trunk/block.json",
	"apiVersion": 3,
	...
}
```

## SUMMARY

**Total issues: 7**
- CRITICAL: 3 (must fix - block won't render correctly)
- WARNING: 3 (quality/compatibility issues)
- INFO: 1 (best practice improvement)

**Block validation risk:** HIGH - Missing useBlockProps.save() will cause validation errors
**Security note:** Missing ABSPATH check detected. Run `/wp-sec-review` for comprehensive security analysis.
**Plugin note:** Block registration detected. Run `/wp-plugin-review` for plugin architecture review.
```

## Common Mistakes (BLK-25)

Patterns that look like issues but are NOT problems:

| Pattern | Why It's NOT a Problem | Context |
|---------|------------------------|---------|
| **Dynamic block save() returning null** | Server-side PHP renders output. save() doesn't need to return markup. | Correct for render_callback or render file usage |
| **InnerBlocks.Content without useBlockProps wrapper** | Valid for dynamic blocks that only need to persist nested blocks. | Dynamic blocks can return bare InnerBlocks.Content in save() |
| **viewScript not needed** | Block has no frontend JavaScript behavior. | Editor-only blocks or static HTML blocks don't need viewScript |
| **render_callback without return** | Valid if callback echoes output (though return is preferred). | WordPress handles both echo and return patterns |
| **Missing style/editorStyle in block.json** | Block uses theme defaults or has no custom styling. | Not all blocks need custom styles |
| **apiVersion 2 blocks** | Still work in WordPress 6.x+, just missing iframe isolation features. | Upgrade recommended but not critical |
| **Block without supports** | Valid for simple blocks that don't need color/spacing/typography. | Intentional for minimal blocks |
| **save() function with className in wrapper** | apiVersion 2 auto-injects classes. apiVersion 3 requires useBlockProps. | apiVersion-dependent behavior, not a bug |
| **window.wp.* in browser console** | Expected for debugging. Only @wordpress/* imports in source code matter. | Console access fine, source imports should use packages |
| **Interactivity API not used** | Blocks with no frontend interaction don't need Interactivity API. | Editor-only or static blocks work without frontend JS |
| **No block.json deprecation for attribute additions** | Adding new optional attributes doesn't break existing blocks. | Only save() markup changes need deprecation |
| **InnerBlocks without template** | Free-form nesting is valid. Template is optional. | Intentional when users should choose any blocks |

## Version Compatibility Reference

Quick reference for WordPress version requirements:

| Feature | WordPress Version | Notes |
|---------|-------------------|-------|
| block.json metadata support | 5.8+ | Single source of truth for block registration |
| apiVersion 2 | 5.6+ | Automatic wrapper class injection in save() |
| apiVersion 3 | 6.3+ | Iframe editor isolation, manual wrapper handling required |
| InspectorControls group prop | 6.2+ | Settings/Appearance tabs in sidebar |
| Block Hooks API | 6.4+ | Auto-insertion, dynamic blocks only |
| Interactivity API | 6.5+ | data-wp-* directives, viewScriptModule |
| viewScriptModule field | 6.5+ | ES module support for Interactivity API |
| Block Bindings API | 6.5+ | Dynamic attribute connections |
| useEntityProp hook | 5.9+ | Replacement for deprecated source:'meta' |

## Deep-Dive References

For advanced block development patterns, load these companion reference documents:

| Task | Reference to Load |
|------|-------------------|
| block.json schema validation, field-by-field reference, attribute type/source/selector patterns | `references/block-json-guide.md` |
| React/JSX editor component patterns, useBlockProps, RichText, InspectorControls, BlockControls, useSelect/useDispatch | `references/editor-patterns.md` |
| Server-side rendering, render_callback vs render file, get_block_wrapper_attributes, output escaping, $attributes/$content/$block parameters | `references/dynamic-blocks-guide.md` |
| Interactivity API directives (data-wp-*), wp_interactivity_state(), store() patterns, frontend state management | `references/interactivity-api-guide.md` |

**Note:** Reference docs provide deep-dive content. This SKILL.md is self-sufficient for standard block reviews.

**Security crossover:** When encountering security-relevant patterns (unescaped render output, user input in Interactivity API state, missing ABSPATH checks), this skill provides brief reminders but defers to wp-security-review for comprehensive security analysis. For detailed security patterns, use `/wp-sec-review` command.

**Plugin crossover:** When encountering plugin-level patterns (register_block_type() on init hook, ABSPATH checks, plugin headers), this skill provides brief mentions but defers to wp-plugin-development for plugin architecture depth. For detailed plugin architecture review, use `/wp-plugin-review` command.
