---
name: wp-theme-development
description: WordPress theme code review and block theme development patterns for WordPress 6.6+. Use when reviewing theme code, auditing theme.json schema, checking template hierarchy, validating block templates, analyzing global styles, verifying style variations, reviewing template parts, detecting hardcoded styles, checking classic-to-block migration, or when user mentions "theme review", "theme development", "theme.json", "block theme", "FSE", "Full Site Editing", "template parts", "template hierarchy", "global styles", "style variations", "classic theme", "child theme", "theme patterns", "theme.json validation", "hardcoded styles", "useRootPaddingAwareAlignments", "classic-to-block", "hybrid theme", "WordPress.org theme". Detects issues in theme.json structure, block templates, template parts, style systems, and classic theme migration patterns.
---

# WordPress Theme Development Review Skill

## Overview

Systematic theme development review for WordPress 6.6+ with primary focus on block themes (Full Site Editing) and secondary coverage of classic themes for migration guidance. **Core principle:** WordPress themes have undergone a paradigm shift—block themes use HTML templates with block markup and theme.json for global settings/styles, replacing PHP templates and add_theme_support() calls. theme.json v3 is the single source of truth for design configuration. Review validates theme.json structure, block template hierarchy (HTML files in templates/), template parts (parts/), global styles, style variations, block patterns in themes, child theme compatibility, and classic-to-block migration opportunities. Auto-detects theme type (block/classic/hybrid/child/WordPress.org) and adjusts guidance accordingly. Report findings grouped by file (PHP, HTML template, JSON files intermixed by actual path) with line numbers, severity labels (CRITICAL/WARNING/INFO), and BAD/GOOD code pairs.

**Note:** This skill reviews PHP files (functions.php, classic templates), HTML block template files (templates/, parts/), JSON files (theme.json, style variations), and PHP pattern files (patterns/). PHP follows WordPress PHP Coding Standards (spaces in parentheses, array() not [], Yoda conditions). HTML templates use valid block markup. JSON follows theme.json v3 schema.

## When to Use

**Use when:**
- Block theme code review (theme.json, HTML templates, template parts)
- theme.json v3 schema validation and structure check
- Template hierarchy audit (block themes with .html files, classic themes with .php files)
- Template parts review (parts/header.html, parts/footer.html, parts/sidebar.html)
- Global styles analysis (color palettes, typography, spacing, layout settings)
- Style variations validation (styles/ directory with alternate theme.json files)
- Block patterns in themes review (patterns/ directory with PHP files)
- Child theme compatibility check (block or classic child themes)
- Classic-to-block theme migration assessment
- WordPress.org theme submission readiness (Theme Check compliance)
- Hardcoded styles detection in block themes
- useRootPaddingAwareAlignments verification for full-width alignment

**Don't use for:**
- Block editor component review (use wp-block-development for React/JSX blocks)
- Plugin architecture audits (use wp-plugin-development for plugin structure)
- Security-only audits (use wp-security-review for comprehensive security)
- Performance-only audits (use wp-performance-review for performance analysis)
- WooCommerce theme integration (use wp-woocommerce-dev when available)
- Visual design assessment (this is code review only, not UI/UX review)

## Code Review Workflow

Follow this seven-step workflow for systematic theme reviews:

1. **Identify theme type and context (THM-01)**
   - Block theme → Has templates/index.html + theme.json + style.css
   - Classic theme → Has index.php + style.css + functions.php (no templates/ directory)
   - Hybrid theme → Has both index.php AND theme.json (classic with block editor support)
   - Child theme → style.css has "Template:" header pointing to parent theme
   - WordPress.org submission → Stricter standards (Theme Check compliance required)

   Auto-detection pattern:
   ```bash
   # Block theme detection
   [ -f templates/index.html ] && [ -f theme.json ] && echo "Block theme"

   # Classic theme detection
   [ -f index.php ] && [ ! -d templates ] && echo "Classic theme"

   # Hybrid theme detection
   [ -f index.php ] && [ -f theme.json ] && [ ! -d templates ] && echo "Hybrid theme"

   # Child theme detection
   grep -q "^Template:" style.css && echo "Child theme"
   ```

2. **Validate theme.json schema (THM-02, THM-03, THM-04, THM-05)**
   - Version field MUST be 3 (WP 6.6+). Flag v1 as CRITICAL (deprecated), v2 as WARNING (upgrade available)
   - Required sections: settings, styles
   - Validate settings structure: color, typography, spacing, layout, border, shadow
   - Check for v3 breaking changes: defaultFontSizes and defaultSpacingSizes both default to true (must explicitly set false if theme defines custom sizes)
   - Verify templateParts array: name, title, area (header/footer/uncategorized)
   - Verify customTemplates array: name, title, postTypes
   - Check for $schema field (INFO if missing, enhances IDE autocomplete)
   - Validate useRootPaddingAwareAlignments when root padding present

3. **Check template hierarchy (THM-06, THM-07)**
   - Block themes: templates/index.html required, others optional (home.html, front-page.html, single.html, page.html, archive.html, 404.html, search.html)
   - Classic themes: index.php required, standard hierarchy (header.php, footer.php, single.php, page.php, archive.php)
   - Verify template files use correct markup: HTML block markup for block themes, PHP template tags for classic themes
   - Check for hardcoded styles in block templates (CRITICAL anti-pattern)
   - Validate template part references in templates

4. **Check template parts (THM-08)**
   - parts/ directory structure: header.html, footer.html, sidebar.html
   - Verify templateParts registration in theme.json matches files
   - Check area designation (header/footer/uncategorized)
   - Validate block markup in template parts
   - Verify template part usage in templates via <!-- wp:template-part --> blocks

5. **Scan for CRITICAL/WARNING/INFO patterns**
   - **CRITICAL:** Missing required files (templates/index.html for block themes, index.php for classic themes, style.css), invalid theme.json version/structure, missing style.css header fields, template hierarchy violations, block theme with hardcoded inline styles defeating theme.json purpose
   - **WARNING:** theme.json v2 (should upgrade to v3), hardcoded color/font values in style.css instead of CSS variables, missing useRootPaddingAwareAlignments with root padding, classic patterns where block patterns preferred, deprecated add_theme_support() in block theme
   - **INFO:** Missing style variations, could use theme.json instead of add_theme_support(), font could use local hosting, missing custom template registration

6. **Apply context-aware severity adjustments**
   - Block theme context: Hardcoded styles = WARNING, missing theme.json sections = WARNING
   - Classic theme context: Migration opportunities = INFO, theme.json missing = INFO
   - Hybrid theme context: Incremental adoption guidance, validate both classic and theme.json patterns
   - Child theme context: Parent compatibility, override validation
   - WordPress.org context: Theme Check failures = CRITICAL

7. **Report with cross-references**
   - Group by FILE (PHP, HTML, JSON intermixed by path)
   - Include line numbers, severity, BAD/GOOD pairs
   - If security issues found (template escaping): "Security issues detected. Run `/wp-sec-review` for comprehensive security analysis."
   - If plugin-like patterns found (functions.php hooks): "Plugin architecture patterns detected. Run `/wp-plugin-review` for plugin development guidance."
   - If block markup issues found: "Block markup issues detected. Run `/wp-block-review` for block development guidance."

## File-Type Specific Checks

### theme.json (THM-02, THM-03, THM-04, THM-05)

**version field:**
- CRITICAL: Missing version field → Theme won't load correctly
- CRITICAL: version 1 → Deprecated, must upgrade to v3
- WARNING: version 2 → Upgrade to v3 recommended (breaking changes in defaultFontSizes and defaultSpacingSizes)
- Pattern: `"version": 3`

**$schema field:**
- INFO: Missing $schema → Can't validate in IDE
- Pattern: `"$schema": "https://schemas.wp.org/trunk/theme.json"`

**settings.color:**
- WARNING: Missing palette → Users can't customize colors via Site Editor
- WARNING: Hardcoded color hex values without palette definitions
- Pattern: color.palette array with slug, color, name
- Available properties: palette, gradients, duotone, custom, defaultPalette, link, heading, button, caption

**settings.typography:**
- WARNING: Missing fontSizes → Users can't customize font sizes
- CRITICAL (v3): theme defines fontSizes but missing `"defaultFontSizes": false` → WordPress defaults override theme sizes
- WARNING: Using Google Fonts CDN instead of local font files (GDPR, performance)
- Pattern: typography.fontSizes array, fontFamilies with fontFace for local fonts
- Available properties: fontSizes, fontFamilies, fluid, lineHeight, fontWeight, letterSpacing, textDecoration, textTransform, defaultFontSizes

**settings.spacing:**
- WARNING: Missing spacingSizes → Users can't customize spacing via Site Editor
- CRITICAL (v3): theme defines spacingSizes but missing `"defaultSpacingSizes": false` → WordPress defaults override theme sizes
- Pattern: spacing.spacingSizes array with slug, size, name
- Available properties: spacingSizes, padding, margin, blockGap, units, customSpacingSize, spacingScale, defaultSpacingSizes

**settings.layout:**
- WARNING: Missing contentSize and wideSize → Full-width blocks may not work correctly
- Pattern: `"contentSize": "640px", "wideSize": "1200px"`

**settings.useRootPaddingAwareAlignments:**
- WARNING: Missing useRootPaddingAwareAlignments with root-level padding → Full-width blocks won't reach viewport edges
- CRITICAL: useRootPaddingAwareAlignments true but padding uses CSS shorthand → Must use object notation
- Pattern: Set to true when styles.spacing.padding present

**styles section:**
- WARNING: Hardcoded values instead of CSS variables → Defeats theme.json purpose
- Pattern: Use `var(--wp--preset--color--primary)` not `"#0073aa"`
- Available properties: color, typography, spacing, border, shadow, elements, blocks

**templateParts array:**
- INFO: Missing templateParts registration → Template parts work but won't show in UI with proper labels
- Pattern: Array with name, title, area (header/footer/uncategorized)

**customTemplates array:**
- INFO: Missing customTemplates → Users can't select custom templates in editor
- Pattern: Array with name, title, postTypes

### style.css (THM-09, THM-10)

**Required header fields:**
- CRITICAL: Missing "Theme Name" → WordPress won't recognize theme
- WARNING: Missing "Text Domain" → Internationalization won't work
- WARNING: Missing "Version" → Updates won't work correctly
- INFO: Missing "Requires at least", "Tested up to", "Requires PHP" → Can't enforce version requirements
- WordPress.org required: Theme Name, Theme URI, Author, Author URI, Description, Version, Requires at least, Tested up to, Requires PHP, License, License URI, Text Domain

**Block theme style patterns:**
- WARNING: Block theme with extensive CSS instead of theme.json → Defeats FSE purpose
- INFO: Could move hardcoded color/font values to theme.json presets
- Pattern: Block themes should have minimal style.css (metadata + critical CSS only), styling comes from theme.json

**Classic theme style patterns:**
- INFO: Classic theme could adopt theme.json for block editor support (hybrid approach)

**Child theme patterns:**
- CRITICAL: Child theme missing "Template:" header → Won't inherit from parent
- WARNING: Child theme template not matching parent directory name → Won't find parent

### Block templates (templates/*.html) (THM-06, THM-11, THM-14)

**Required template:**
- CRITICAL: Missing templates/index.html in block theme → Theme won't work

**Template file naming:**
- INFO: Could add specific templates (single.html, page.html, archive.html, 404.html, search.html, home.html, front-page.html) for better hierarchy coverage

**Block markup validation:**
- CRITICAL: Invalid block comment syntax → Template won't parse
- WARNING: Hardcoded inline style attributes → Defeats theme.json, users can't customize
- WARNING: Hardcoded color hex values instead of theme.json presets
- WARNING: Hardcoded pixel font sizes instead of theme.json fluid typography
- Pattern: Use block attributes with theme.json preset references, not inline styles

**Template part usage:**
- WARNING: Missing template part references (header/footer) → Users expect standard structure
- Pattern: `<!-- wp:template-part {"slug":"header","area":"header"} /-->`

**useBlockProps equivalent:**
- INFO: Block templates don't need wrapper attributes like dynamic blocks (static HTML)

### Template parts (parts/*.html) (THM-08)

**Template part files:**
- WARNING: templateParts registered in theme.json but files missing → 404 in Site Editor
- WARNING: Template part files exist but not registered in theme.json → Won't show in UI with proper labels
- Pattern: parts/header.html, parts/footer.html, parts/sidebar.html

**Area designation:**
- WARNING: Template part area mismatch between theme.json and usage → May not render in correct location
- Available areas: header, footer, uncategorized (or custom areas in WP 6.0+)

**Block markup:**
- Same validation as block templates: no hardcoded styles, use theme.json presets

### functions.php (THM-12, THM-13)

**ABSPATH check:**
- WARNING: Missing `defined( 'ABSPATH' ) || exit;` → Direct file access possible
- Cross-reference: See wp-security-review for security depth

**Block theme setup:**
- WARNING: add_theme_support() calls that should be in theme.json → Deprecated pattern
- Acceptable add_theme_support() in block themes: wp-block-styles, responsive-embeds, editor-styles (theme.json can't replace these)
- Pattern: Most add_theme_support() calls migrate to theme.json settings

**Classic theme setup:**
- INFO: Classic theme could migrate add_theme_support() to theme.json for hybrid approach
- Pattern: Color palette, font sizes, line height, spacing → theme.json settings

**Theme hooks:**
- Pattern: after_setup_theme for theme setup, wp_enqueue_scripts for assets, init for custom post types
- Cross-reference: See wp-plugin-development for hooks system patterns

**Asset enqueuing:**
- WARNING: Enqueuing assets on every page without conditional checks → Performance issue
- Pattern: Use conditional tags (is_front_page, is_singular) or admin checks

### Block patterns (patterns/*.php) (THM-15, THM-16)

**Pattern file headers:**
- CRITICAL: Pattern file missing Title or Slug header → Won't register
- WARNING: Pattern slug not namespaced (themename/pattern-slug) → Collision risk
- Pattern: PHP file with comment block containing Title, Slug, Categories, Description, Keywords, Block Types, Viewport Width

**Pattern file structure:**
- WARNING: Pattern file without PHP tags → Won't process dynamic values
- Pattern: `<?php ?>` tags for PHP code, then block markup

**Block markup in patterns:**
- Same validation as templates: use theme.json presets, no hardcoded styles
- Use PHP functions for dynamic values: `get_theme_file_uri()`, `esc_url()`, `esc_html()`, translation functions

**Pattern registration:**
- INFO: Patterns in patterns/ directory auto-register, no manual register_block_pattern() needed (themes only, not plugins)

### Style variations (styles/*.json) (THM-17, THM-18, THM-19)

**Variation file structure:**
- WARNING: Style variation missing version field → May not load correctly
- WARNING: Style variation missing title → Shows filename in UI
- Pattern: JSON file with version, title, settings, styles

**Variation naming:**
- INFO: Variation filename becomes variation slug (dark.json → "dark"), title overrides display name
- Pattern: Use descriptive filenames (dark.json, minimal.json, high-contrast.json)

**Variation schema:**
- WARNING: Variation with invalid theme.json structure → Won't apply
- Pattern: Same schema as theme.json (settings, styles sections), version should match main theme.json

### Child themes (THM-20)

**Child theme detection:**
- Pattern: style.css with "Template:" header

**Template overrides:**
- WARNING: Child block theme parts/header.html doesn't override parent → Filename must match exactly
- WARNING: Child theme.json doesn't override parent templateParts → Must copy and modify templateParts array
- Pattern: Child theme files override parent by exact filename match

**Child theme compatibility:**
- WARNING: Child theme depends on parent template parts that might change → Fragile override
- INFO: Child theme could use unregister_block_pattern() to remove parent patterns

## Search Patterns for Quick Detection (THM-21)

Use these `rg` commands and shell checks for quick theme scanning. Organized by severity. Cover PHP, HTML template, and JSON files.

### CRITICAL Patterns

```bash
# Missing required files for block theme
[ ! -f templates/index.html ] && [ -f theme.json ] && echo "CRITICAL: Block theme missing templates/index.html"
[ ! -f theme.json ] && [ -d templates ] && echo "CRITICAL: templates/ exists but theme.json missing"

# Missing required files for classic theme
[ ! -f index.php ] && [ ! -d templates ] && echo "CRITICAL: Classic theme missing index.php"

# theme.json with invalid or missing version
test -f theme.json && ! rg -q "\"version\"" theme.json && echo "CRITICAL: theme.json missing version"
rg -n "\"version\": 1" theme.json  # Deprecated
rg -n "\"version\": [^23]" theme.json  # Invalid version

# Missing style.css required header
test -f style.css && ! rg -q "Theme Name:" style.css && echo "CRITICAL: style.css missing Theme Name header"

# v3 theme.json with custom fontSizes but missing defaultFontSizes: false
rg -n "\"fontSizes\"" theme.json
# Manual follow-up: if custom fontSizes are defined, confirm defaultFontSizes is explicitly false.

# v3 theme.json with custom spacingSizes but missing defaultSpacingSizes: false
rg -n "\"spacingSizes\"" theme.json
# Manual follow-up: if custom spacingSizes are defined, confirm defaultSpacingSizes is explicitly false.

# Child theme missing Template header
test -f style.css && ! rg -q "Template:" style.css && echo "CRITICAL: If this is a child theme, style.css is missing Template header"
```

### WARNING Patterns

```bash
# theme.json version 2 (should upgrade to v3)
rg -n "\"version\": 2" theme.json

# Hardcoded inline styles in block templates
rg -n "style=\"" templates/ parts/ -g '*.html'

# Hardcoded color hex values in templates
rg -n "#[0-9a-fA-F]{6}" templates/ parts/ -g '*.html'

# Hardcoded pixel font sizes in templates
rg -n "font-size:\s*[0-9]+px" templates/ parts/ -g '*.html'

# Root padding without useRootPaddingAwareAlignments
rg -n "\"padding\"" theme.json
# Manual follow-up: if root padding is present, confirm useRootPaddingAwareAlignments is enabled.

# useRootPaddingAwareAlignments with CSS shorthand padding (won't work)
rg -n "useRootPaddingAwareAlignments.*true" theme.json
rg -n "\"padding\":\s*\"" theme.json

# Block theme with add_theme_support() that should be in theme.json
rg -n "add_theme_support.*editor-color-palette" functions.php
rg -n "add_theme_support.*editor-font-sizes" functions.php
rg -n "add_theme_support.*custom-line-height" functions.php
rg -n "add_theme_support.*custom-spacing" functions.php

# Missing ABSPATH check in functions.php
test -f functions.php && ! sed -n '1,10p' functions.php | rg -q "defined.*ABSPATH" && echo "WARNING: functions.php missing ABSPATH check in first 10 lines"

# Pattern file without required headers
rg -L "Title:" patterns -g '*.php'
rg -L "Slug:" patterns -g '*.php'
```

### INFO Patterns

```bash
# Missing $schema in theme.json
test -f theme.json && ! rg -q "\"\\$schema\"" theme.json && echo "INFO: theme.json missing \$schema"

# Missing style variations directory
[ ! -d styles ] && echo "INFO: Could add style variations in styles/"

# Missing block patterns directory
[ ! -d patterns ] && echo "INFO: Could add block patterns in patterns/"

# Missing templateParts registration in theme.json
test -f theme.json && ! rg -q "\"templateParts\"" theme.json && echo "INFO: theme.json missing templateParts registration"

# Missing customTemplates registration in theme.json
test -f theme.json && ! rg -q "\"customTemplates\"" theme.json && echo "INFO: theme.json missing customTemplates registration"

# Google Fonts CDN usage (could use local fonts)
rg -n "fonts.googleapis.com" .

# Classic theme without theme.json (could be hybrid)
[ -f index.php ] && [ ! -f theme.json ] && echo "INFO: Classic theme could add theme.json for block editor support"
```

**Note:** HTML template patterns require different regex than PHP. Use `--include="*.html"` for templates, `--include="*.php"` for PHP files, `--include="*.json"` for theme.json and variations.

## Theme Context Detection

Context-aware review notes based on detected theme type:

### Block theme
**Structure:** templates/index.html + theme.json + style.css, optional parts/, patterns/, styles/
**Review focus:**
- theme.json v3 validation primary concern
- Hardcoded styles in templates = WARNING (defeats FSE purpose)
- Template hierarchy completeness
- useRootPaddingAwareAlignments when padding present
- Style variations and patterns as enhancement opportunities
**Common mistakes:** Missing useRootPaddingAwareAlignments, hardcoded inline styles, theme.json v2 without migration to v3

### Classic theme
**Structure:** index.php + style.css + functions.php, header.php, footer.php, template files
**Review focus:**
- Template escaping (cross-reference wp-security-review)
- Classic template hierarchy
- Migration opportunities to block theme or hybrid approach
- Suggest theme.json adoption for block editor support
**Common mistakes:** Missing escaping, deprecated template tags, no theme.json for modern editor features

### Hybrid theme
**Structure:** index.php + theme.json + functions.php (classic templates with theme.json)
**Review focus:**
- Validate both classic and theme.json patterns
- Check CSS variable usage in classic templates
- Verify theme.json applies to block content
- Suggest incremental migration to block templates
**Common mistakes:** theme.json settings don't affect classic template output, expecting theme.json to style PHP templates

### Child theme (block or classic)
**Structure:** style.css with "Template:" header, optional template overrides
**Review focus:**
- Parent compatibility (template filenames must match exactly)
- theme.json override patterns (child must copy + modify parent templateParts)
- Template part overrides
- Pattern removal with unregister_block_pattern()
**Common mistakes:** Template part doesn't override (wrong filename), theme.json doesn't override parent settings

### WordPress.org theme submission
**Structure:** Any theme type but stricter standards
**Review focus:**
- Theme Check plugin compliance (all errors = CRITICAL)
- Required files: style.css with complete header, readme.txt, screenshot.png
- License compatibility (GPL or GPL-compatible)
- No obfuscated code, no phone-home, no upsells in free theme
- Prefix all functions/classes
**Common mistakes:** Missing readme.txt, incomplete style.css header, Theme Check errors

## Quick Reference: Theme Development Patterns (THM-22, THM-23)

Common theme patterns organized by concern. PHP examples use WordPress PHP Coding Standards (spaces in parentheses, array() not [], Yoda conditions). HTML templates use valid block markup. JSON examples use valid theme.json v3 syntax.

### theme.json v3 Complete Structure

```json
{
	"$schema": "https://schemas.wp.org/trunk/theme.json",
	"version": 3,
	"settings": {
		"appearanceTools": true,
		"useRootPaddingAwareAlignments": true,
		"color": {
			"defaultPalette": false,
			"palette": [
				{
					"slug": "primary",
					"color": "#0073aa",
					"name": "Primary"
				},
				{
					"slug": "secondary",
					"color": "#005177",
					"name": "Secondary"
				},
				{
					"slug": "foreground",
					"color": "#333333",
					"name": "Foreground"
				},
				{
					"slug": "background",
					"color": "#ffffff",
					"name": "Background"
				}
			]
		},
		"typography": {
			"defaultFontSizes": false,
			"fluid": true,
			"fontFamilies": [
				{
					"fontFamily": "\"Inter\", -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif",
					"name": "Inter",
					"slug": "inter",
					"fontFace": [
						{
							"fontFamily": "Inter",
							"fontWeight": "400",
							"fontStyle": "normal",
							"src": [ "file:./assets/fonts/inter-regular.woff2" ]
						},
						{
							"fontFamily": "Inter",
							"fontWeight": "700",
							"fontStyle": "normal",
							"src": [ "file:./assets/fonts/inter-bold.woff2" ]
						}
					]
				}
			],
			"fontSizes": [
				{
					"slug": "small",
					"size": "0.875rem",
					"name": "Small"
				},
				{
					"slug": "medium",
					"size": "1rem",
					"name": "Medium"
				},
				{
					"slug": "large",
					"size": "1.5rem",
					"name": "Large"
				}
			]
		},
		"spacing": {
			"defaultSpacingSizes": false,
			"spacingSizes": [
				{
					"slug": "30",
					"size": "1rem",
					"name": "Small"
				},
				{
					"slug": "40",
					"size": "1.5rem",
					"name": "Medium"
				},
				{
					"slug": "50",
					"size": "2rem",
					"name": "Large"
				}
			],
			"units": [ "px", "rem", "vh", "vw", "%" ]
		},
		"layout": {
			"contentSize": "640px",
			"wideSize": "1200px"
		},
		"border": {
			"radius": true,
			"color": true,
			"style": true,
			"width": true
		}
	},
	"styles": {
		"color": {
			"background": "var(--wp--preset--color--background)",
			"text": "var(--wp--preset--color--foreground)"
		},
		"typography": {
			"fontFamily": "var(--wp--preset--font-family--inter)",
			"fontSize": "var(--wp--preset--font-size--medium)",
			"lineHeight": "1.6"
		},
		"spacing": {
			"padding": {
				"top": "var(--wp--preset--spacing--50)",
				"right": "var(--wp--preset--spacing--50)",
				"bottom": "var(--wp--preset--spacing--50)",
				"left": "var(--wp--preset--spacing--50)"
			}
		},
		"elements": {
			"link": {
				"color": {
					"text": "var(--wp--preset--color--primary)"
				}
			},
			"heading": {
				"typography": {
					"fontWeight": "700",
					"lineHeight": "1.2"
				}
			}
		},
		"blocks": {
			"core/button": {
				"color": {
					"background": "var(--wp--preset--color--primary)",
					"text": "var(--wp--preset--color--background)"
				}
			}
		}
	},
	"customTemplates": [
		{
			"name": "page-no-title",
			"title": "Page Without Title",
			"postTypes": [ "page" ]
		}
	],
	"templateParts": [
		{
			"name": "header",
			"title": "Header",
			"area": "header"
		},
		{
			"name": "footer",
			"title": "Footer",
			"area": "footer"
		}
	]
}
```

### Block Template Structure (templates/single.html)

**❌ BAD: Hardcoded inline styles defeat theme.json**
```html
<!-- wp:template-part {"slug":"header"} /-->

<main style="max-width: 1200px; margin: 0 auto; padding: 2rem; color: #333;">
	<h1 style="font-size: 32px; color: #0073aa;">Post Title</h1>
	<div style="font-size: 16px; line-height: 1.6;">
		<!-- wp:post-content /-->
	</div>
</main>

<!-- wp:template-part {"slug":"footer"} /-->
```

**✅ GOOD: Use block attributes and theme.json presets**
```html
<!-- wp:template-part {"slug":"header","area":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
	<!-- wp:post-title {"level":1} /-->

	<!-- wp:group {"layout":{"type":"flex","flexWrap":"nowrap"}} -->
	<div class="wp-block-group">
		<!-- wp:post-author {"showAvatar":true} /-->
		<!-- wp:post-date /-->
	</div>
	<!-- /wp:group -->

	<!-- wp:post-content {"layout":{"type":"constrained"}} /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","area":"footer"} /-->
```

### Template Part Structure (parts/header.html)

**❌ BAD: Hardcoded colors and spacing**
```html
<div style="background: #ffffff; padding: 20px; border-bottom: 1px solid #cccccc;">
	<div style="max-width: 1200px; margin: 0 auto; display: flex; justify-content: space-between;">
		<h1 style="font-size: 24px; color: #0073aa;">Site Title</h1>
		<nav>Navigation</nav>
	</div>
</div>
```

**✅ GOOD: Use block attributes with theme.json preset references**
```html
<!-- wp:group {"align":"full","style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|40"}}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull">
	<!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between","flexWrap":"nowrap"}} -->
	<div class="wp-block-group">
		<!-- wp:site-logo {"width":60} /-->
		<!-- wp:site-title {"level":0} /-->

		<!-- wp:navigation {"layout":{"type":"flex","orientation":"horizontal"}} /-->
	</div>
	<!-- /wp:group -->
</div>
<!-- /wp:group -->
```

### useRootPaddingAwareAlignments

**❌ BAD: Root padding without useRootPaddingAwareAlignments**
```json
{
	"version": 3,
	"styles": {
		"spacing": {
			"padding": {
				"left": "2rem",
				"right": "2rem"
			}
		}
	}
}
```
Result: Full-width blocks have white space on left/right edges

**❌ BAD: useRootPaddingAwareAlignments with CSS shorthand**
```json
{
	"version": 3,
	"settings": {
		"useRootPaddingAwareAlignments": true
	},
	"styles": {
		"spacing": {
			"padding": "2rem"
		}
	}
}
```
Result: Won't work, must use object notation

**✅ GOOD: useRootPaddingAwareAlignments with object notation**
```json
{
	"version": 3,
	"settings": {
		"useRootPaddingAwareAlignments": true
	},
	"styles": {
		"spacing": {
			"padding": {
				"top": "var(--wp--preset--spacing--50)",
				"right": "var(--wp--preset--spacing--50)",
				"bottom": "var(--wp--preset--spacing--50)",
				"left": "var(--wp--preset--spacing--50)"
			}
		}
	}
}
```

### theme.json v2 to v3 Migration

**❌ BAD: Upgrading version without adjusting defaults**
```json
{
	"version": 3,
	"settings": {
		"typography": {
			"fontSizes": [
				{ "slug": "small", "size": "14px" },
				{ "slug": "medium", "size": "16px" }
			]
		}
	}
}
```
Result: WordPress default font sizes also appear, theme sizes don't override

**✅ GOOD: v3 with explicit defaultFontSizes: false**
```json
{
	"version": 3,
	"settings": {
		"typography": {
			"defaultFontSizes": false,
			"fontSizes": [
				{ "slug": "small", "size": "0.875rem", "name": "Small" },
				{ "slug": "medium", "size": "1rem", "name": "Medium" }
			]
		},
		"spacing": {
			"defaultSpacingSizes": false,
			"spacingSizes": [
				{ "slug": "30", "size": "1rem", "name": "Small" }
			]
		}
	}
}
```

### Block Pattern in Theme (patterns/hero.php)

**❌ BAD: Pattern without required headers**
```php
<?php
// Missing Title and Slug headers
?>
<!-- wp:cover -->
<div class="wp-block-cover">
	<h1>Welcome</h1>
</div>
<!-- /wp:cover -->
```

**✅ GOOD: Complete pattern with headers and dynamic values**
```php
<?php
/**
 * Title: Hero Section
 * Slug: mytheme/hero
 * Categories: featured, banner
 * Keywords: hero, banner, header
 * Block Types: core/cover
 * Viewport Width: 1400
 * Description: Full-width hero section with heading and CTA
 */
?>
<!-- wp:cover {"url":"<?php echo esc_url( get_theme_file_uri( 'assets/images/hero.jpg' ) ); ?>","dimRatio":50,"align":"full","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|60"}}}} -->
<div class="wp-block-cover alignfull">
	<span aria-hidden="true" class="wp-block-cover__background has-background-dim"></span>
	<img class="wp-block-cover__image-background" alt="" src="<?php echo esc_url( get_theme_file_uri( 'assets/images/hero.jpg' ) ); ?>" data-object-fit="cover" />

	<div class="wp-block-cover__inner-container">
		<!-- wp:heading {"textAlign":"center","level":1} -->
		<h1 class="has-text-align-center"><?php echo esc_html_x( 'Welcome to Our Site', 'Pattern placeholder', 'mytheme' ); ?></h1>
		<!-- /wp:heading -->

		<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
		<div class="wp-block-buttons">
			<!-- wp:button -->
			<div class="wp-block-button">
				<a class="wp-block-button__link wp-element-button"><?php echo esc_html_x( 'Get Started', 'Pattern placeholder', 'mytheme' ); ?></a>
			</div>
			<!-- /wp:button -->
		</div>
		<!-- /wp:buttons -->
	</div>
</div>
<!-- /wp:cover -->
```

### Style Variation (styles/dark.json)

**❌ BAD: Variation missing version or title**
```json
{
	"settings": {
		"color": {
			"palette": [
				{ "slug": "background", "color": "#1a1a1a" }
			]
		}
	}
}
```

**✅ GOOD: Complete variation with version and title**
```json
{
	"version": 3,
	"title": "Dark Mode",
	"settings": {
		"color": {
			"palette": [
				{
					"slug": "foreground",
					"color": "#ffffff",
					"name": "Foreground"
				},
				{
					"slug": "background",
					"color": "#1a1a1a",
					"name": "Background"
				},
				{
					"slug": "primary",
					"color": "#3dadff",
					"name": "Primary"
				}
			]
		}
	},
	"styles": {
		"color": {
			"background": "var(--wp--preset--color--background)",
			"text": "var(--wp--preset--color--foreground)"
		}
	}
}
```

### functions.php for Block Themes

**❌ BAD: Using add_theme_support() instead of theme.json**
```php
<?php
function mytheme_setup() {
	add_theme_support( 'align-wide' );
	add_theme_support( 'custom-line-height' );
	add_theme_support( 'custom-spacing' );
	add_theme_support( 'editor-color-palette', array(
		array(
			'name'  => 'Primary',
			'slug'  => 'primary',
			'color' => '#0073aa',
		),
	) );
}
add_action( 'after_setup_theme', 'mytheme_setup' );
```

**✅ GOOD: Minimal functions.php, settings in theme.json**
```php
<?php
/**
 * Theme setup and initialization
 */

defined( 'ABSPATH' ) || exit;

/**
 * Theme setup
 */
function mytheme_setup() {
	// Still valid in block themes
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'editor-styles' );

	// Load editor stylesheet
	add_editor_style( 'style.css' );

	// Internationalization
	load_theme_textdomain( 'mytheme', get_template_directory() . '/languages' );
}
add_action( 'after_setup_theme', 'mytheme_setup' );

/**
 * Enqueue additional scripts (if needed)
 */
function mytheme_enqueue_assets() {
	// Only if theme needs custom JS
	if ( is_front_page() ) {
		wp_enqueue_script(
			'mytheme-interactions',
			get_theme_file_uri( '/assets/js/interactions.js' ),
			array(),
			wp_get_theme()->get( 'Version' ),
			true
		);
	}
}
add_action( 'wp_enqueue_scripts', 'mytheme_enqueue_assets' );
```

### Classic to Block Theme Migration

**❌ BAD: Classic approach (deprecated for block themes)**
```php
<?php
// functions.php in classic theme
function classictheme_setup() {
	add_theme_support( 'custom-logo' );
	add_theme_support( 'custom-header' );
	add_theme_support( 'custom-background' );
	add_theme_support( 'editor-color-palette', array(
		array( 'name' => 'Primary', 'slug' => 'primary', 'color' => '#0073aa' ),
	) );
	add_theme_support( 'editor-font-sizes', array(
		array( 'name' => 'Small', 'size' => 14, 'slug' => 'small' ),
	) );
}
add_action( 'after_setup_theme', 'classictheme_setup' );
```

**✅ GOOD: Block theme approach via theme.json**
```json
{
	"version": 3,
	"settings": {
		"layout": {
			"contentSize": "640px",
			"wideSize": "1200px"
		},
		"typography": {
			"defaultFontSizes": false,
			"fontSizes": [
				{
					"slug": "small",
					"size": "0.875rem",
					"name": "Small"
				}
			]
		},
		"color": {
			"defaultPalette": false,
			"palette": [
				{
					"slug": "primary",
					"color": "#0073aa",
					"name": "Primary"
				}
			]
		}
	}
}
```

### Child Theme Pattern

**❌ BAD: Child theme style.css missing Template header**
```css
/*
Theme Name: My Child Theme
Description: A child theme
Author: Author Name
*/
```
Result: WordPress won't recognize parent theme

**✅ GOOD: Complete child theme style.css**
```css
/*
Theme Name: My Child Theme
Template: parent-theme-folder
Description: A child theme extending Parent Theme
Author: Author Name
Author URI: https://example.com
Version: 1.0.0
License: GNU General Public License v2 or later
License URI: http://www.gnu.org/licenses/gpl-2.0.html
Text Domain: my-child-theme
*/
```

**Child theme template part override:**
```
parent-theme/
├── parts/
│   └── header.html

child-theme/
├── style.css (with Template: parent-theme)
└── parts/
    └── header.html  ← Must match filename exactly to override
```

## Severity Definitions (THM-23)

| Severity | Definition | Examples |
|----------|------------|----------|
| **CRITICAL** | Theme won't work OR WordPress.org rejection | Missing required files (templates/index.html for block themes, index.php for classic themes, style.css for all themes), invalid theme.json version (v1 deprecated), missing style.css "Theme Name" header, template hierarchy violations, child theme missing "Template:" header, theme.json v3 with custom fontSizes/spacingSizes but missing defaultFontSizes/defaultSpacingSizes: false (WordPress defaults override theme), useRootPaddingAwareAlignments with CSS shorthand padding (must use object notation), pattern file missing Title or Slug header |
| **WARNING** | Theme works but has quality/compatibility issues | theme.json v2 (should upgrade to v3 for breaking changes), hardcoded styles in block theme templates (inline style attributes, hardcoded hex colors, pixel font sizes), missing useRootPaddingAwareAlignments with root padding (full-width blocks won't reach edges), classic patterns where block patterns preferred, deprecated add_theme_support() calls in block theme (editor-color-palette, editor-font-sizes, custom-line-height, custom-spacing should be in theme.json), missing ABSPATH check in functions.php, template part files without theme.json registration, hardcoded WordPress paths (/wp-content/themes/) |
| **INFO** | Best practice improvements OR optimization opportunities | Missing $schema in theme.json (IDE validation), missing style variations directory, missing block patterns directory, missing templateParts or customTemplates registration, Google Fonts CDN instead of local fonts (GDPR, performance), classic theme without theme.json (could be hybrid), could add specific templates (single.html, page.html) for better hierarchy, child theme could use unregister_block_pattern() to remove parent patterns, missing version requirements in style.css (Requires at least, Tested up to, Requires PHP) |

## Output Format (THM-24)

Report findings grouped by FILE (PHP, HTML template, JSON files intermixed by actual file path), with line numbers and severity labels. Use BAD/GOOD code pairs for each finding.

```markdown
# WordPress Theme Review: my-theme

## Theme Type: Block Theme
**Detected:** templates/index.html + theme.json + style.css

## FILE: theme.json

### Line 2: WARNING - theme.json version 2 (upgrade to v3)
theme.json v2 still works but v3 is recommended for WP 6.6+. Breaking changes: defaultFontSizes and defaultSpacingSizes now default to true.

❌ **BAD:**
```json
{
	"version": 2
}
```

✅ **GOOD:**
```json
{
	"version": 3,
	"settings": {
		"typography": {
			"defaultFontSizes": false,
			"fontSizes": [ /* custom sizes */ ]
		}
	}
}
```

### Line 45: WARNING - Missing useRootPaddingAwareAlignments
Root-level padding present but useRootPaddingAwareAlignments not set. Full-width blocks won't reach viewport edges.

❌ **BAD:**
```json
{
	"styles": {
		"spacing": {
			"padding": { "left": "2rem", "right": "2rem" }
		}
	}
}
```

✅ **GOOD:**
```json
{
	"settings": {
		"useRootPaddingAwareAlignments": true
	},
	"styles": {
		"spacing": {
			"padding": {
				"top": "2rem",
				"right": "2rem",
				"bottom": "2rem",
				"left": "2rem"
			}
		}
	}
}
```

## FILE: templates/single.html

### Line 8: WARNING - Hardcoded inline style
Inline style attribute defeats theme.json purpose. Users can't customize via Site Editor.

❌ **BAD:**
```html
<div style="max-width: 1200px; padding: 2rem;">
```

✅ **GOOD:**
```html
<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
```

## FILE: functions.php

### Line 1: WARNING - Missing ABSPATH check
Add ABSPATH check at top of file to prevent direct access.

❌ **BAD:**
```php
<?php
function mytheme_setup() {
```

✅ **GOOD:**
```php
<?php
defined( 'ABSPATH' ) || exit;

function mytheme_setup() {
```

### Line 15: WARNING - add_theme_support() deprecated in block themes
editor-color-palette should be in theme.json for block themes.

❌ **BAD:**
```php
add_theme_support( 'editor-color-palette', array(
	array( 'name' => 'Primary', 'slug' => 'primary', 'color' => '#0073aa' ),
) );
```

✅ **GOOD:**
```json
// In theme.json:
{
	"settings": {
		"color": {
			"palette": [
				{ "slug": "primary", "color": "#0073aa", "name": "Primary" }
			]
		}
	}
}
```

## FILE: style.css

### Line 1: INFO - Missing version requirements
Add Requires at least, Tested up to, Requires PHP for version enforcement.

```css
/*
Theme Name: My Theme
Version: 1.0.0
Requires at least: 6.6
Tested up to: 6.7
Requires PHP: 7.4
*/
```

## SUMMARY

**Total issues: 6**
- CRITICAL: 0
- WARNING: 4 (quality/compatibility improvements needed)
- INFO: 2 (best practice enhancements)

**Upgrade recommendation:** Update theme.json to v3 with explicit defaultFontSizes and defaultSpacingSizes settings.
**Hardcoded styles:** Found in templates - migrate to theme.json presets for user customization.
**Security note:** Missing ABSPATH check. Run `/wp-sec-review` for comprehensive security analysis.
**Plugin note:** functions.php hooks detected. Run `/wp-plugin-review` for plugin development patterns.
```

## Common Mistakes (THM-25)

Patterns that look like issues but are NOT problems:

| Pattern | Why It's NOT a Problem | Context |
|---------|------------------------|---------|
| **Block theme with minimal style.css** | Block themes use theme.json for styling, style.css is primarily metadata | Correct for block themes - style.css contains theme header, minimal CSS |
| **Classic theme without theme.json** | Classic themes work without theme.json, optional for block editor support | Valid classic theme - theme.json is optional for hybrid approach |
| **Hybrid theme with both index.php and theme.json** | Intentional pattern for incremental block editor adoption | Valid hybrid approach - theme.json enhances block editor, classic templates still work |
| **Template part without theme.json registration** | Template parts work by filename, registration is for UI labels only | Works correctly - registration enhances Site Editor UI but not required |
| **Style variation missing some settings sections** | Variations only need to override specific settings, not full schema | Intentional - variations merge with main theme.json |
| **Block template without template-part blocks** | Not all templates need header/footer, valid for custom layouts | Intentional for special templates (404, search results without chrome) |
| **functions.php with add_theme_support() in block theme** | Some add_theme_support() calls are still valid (wp-block-styles, responsive-embeds, editor-styles) | Valid - these can't be replaced by theme.json |
| **Pattern file with only static markup (no PHP)** | If pattern doesn't need dynamic values, static HTML is fine | Valid - PHP optional for static patterns |
| **Child theme without functions.php** | Child themes don't need functions.php if only overriding styles/templates | Valid minimal child theme - functions.php is optional |
| **Block theme without patterns/ directory** | Patterns are optional, not all themes need bundled patterns | Valid - themes can rely on WordPress.org pattern directory |
| **Missing viewScript in theme** | Themes typically don't need frontend JavaScript, unlike blocks | Expected - most themes are HTML/CSS only |
| **CSS variables in style.css referencing theme.json** | Correct usage - theme.json generates CSS variables that style.css can reference | Intentional integration between theme.json and style.css |

## Version Compatibility Reference

Quick reference for WordPress version requirements:

| Feature | WordPress Version | Notes |
|---------|-------------------|-------|
| Block themes (FSE) | 5.9+ | Full Site Editing stable release |
| theme.json v1 | 5.8+ | Initial theme.json support |
| theme.json v2 | 5.9+ | Expanded settings and styles options |
| theme.json v3 | 6.6+ | Breaking changes: defaultFontSizes and defaultSpacingSizes defaults |
| useRootPaddingAwareAlignments | 6.1+ | Full-width alignment with root padding |
| Template parts areas | 6.0+ | header, footer, uncategorized areas |
| fontFace support in theme.json | 6.0+ | Local font hosting via theme.json |
| Block theme patterns (patterns/) | 6.3+ | Auto-registration of PHP pattern files |
| Navigation block | 5.9+ | Replaces wp_nav_menu() in block themes |
| Site Editor | 5.9+ | Full Site Editing interface |
| Global Styles | 5.9+ | User customization of theme.json via UI |
| Style variations | 6.0+ | Alternate theme.json files in styles/ |

## Deep-Dive References

For advanced theme development patterns, load these companion reference documents:

| Task | Reference to Load |
|------|-------------------|
| theme.json v3 complete schema, all sections explained (settings, styles, templateParts, customTemplates, patterns), property catalog with valid values, v2→v3 migration notes, common mistakes, WordPress.org requirements | `references/theme-json-guide.md` |
| Template hierarchy for both classic and block themes side-by-side, template parts and areas, conditional tags, get_template_part() for classic, block markup in HTML templates, custom templates registration | `references/template-patterns.md` |
| Full Site Editing comprehensive guide: site editor workflow, global styles UI mapping to theme.json, style variations creation, block patterns in themes (patterns/ directory), navigation configuration, font management, layout system (contentSize, wideSize, root padding) | `references/fse-guide.md` |
| Step-by-step classic-to-block migration: functions.php → theme.json mapping table, template.php → template.html conversion, sidebar widgets → template parts, Customizer → global styles, add_theme_support → theme.json equivalents, incremental hybrid adoption path | `references/classic-to-block-guide.md` |

**Note:** Reference docs provide deep-dive content. This SKILL.md is self-sufficient for standard theme reviews.

**Security crossover:** When encountering security-relevant patterns (template escaping in classic themes, child theme security, sanitization in theme customizer), this skill provides brief reminders but defers to wp-security-review for comprehensive security analysis. For detailed security patterns, use `/wp-sec-review` command.

**Plugin crossover:** When encountering plugin-level patterns (functions.php hooks like after_setup_theme, wp_enqueue_scripts, init for CPT registration), this skill provides brief mentions but defers to wp-plugin-development for plugin architecture depth. For detailed plugin patterns, use `/wp-plugin-review` command.

**Block crossover:** When encountering block development patterns (block patterns registration in themes vs plugins, block markup in templates, block supports defined in theme.json), this skill provides brief context but defers to wp-block-development for block-specific depth. For detailed block patterns, use `/wp-block-review` command.
