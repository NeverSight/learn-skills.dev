---
name: wp-acf-and-content-modeling
description: WordPress ACF and content modeling review. Use when reviewing Advanced Custom Fields usage, field group architecture, CPT and taxonomy design, options pages, repeaters, flexible content, block-bound field groups, meta storage patterns, or when user mentions "ACF", "field groups", "flexible content", "repeater", "custom post type design", "taxonomy design", "content model", "relationship fields", "ACF JSON", "options page", or "meta query performance". Detects schema drift, weak content modeling, brittle field naming, and performance issues in meta-heavy WordPress builds.
---

# WordPress ACF and Content Modeling Skill

## Overview

Systematic review skill for WordPress projects that rely on Advanced Custom Fields and custom content architecture. **Core principle:** a healthy WordPress content model is durable, query-aware, editor-friendly, and predictable to migrate. Review focuses on CPT and taxonomy design, field-group boundaries, naming consistency, storage strategy, ACF JSON synchronization, and the long-term cost of meta-heavy patterns. Report findings grouped by file or subsystem with severity labels (`CRITICAL`, `WARNING`, `INFO`), line references where possible, and concrete remediation guidance.

## When to Use

**Use when:**
- Auditing a plugin or theme that registers custom post types, taxonomies, or ACF field groups
- Reviewing `acf_add_local_field_group()` or field group JSON exports
- Checking whether repeaters / flexible content are the right fit for the content problem
- Evaluating options pages, relationship fields, clone fields, or block field groups
- Investigating slow admin screens or expensive `meta_query` usage in content-heavy builds
- Planning a new content model for an editorial site, directory, landing-page builder, or headless setup
- Reviewing ACF JSON sync, field key drift, or environment-to-environment portability

**Don't use for:**
- Generic plugin architecture without meaningful ACF/content-model work (use `wp-plugin-development`)
- Pure REST route design (use `wp-rest-api-development`)
- Gutenberg block implementation details unrelated to field modeling (use `wp-block-development`)
- Performance audits not tied to content schema or metadata access (use `wp-performance-review`)
- WooCommerce domain modeling (use `wp-woocommerce-dev` unless the issue is truly generic ACF modeling)

## Review Workflow

Follow this seven-step workflow.

1. **Identify the model boundary**
   - What is the real domain: articles, locations, staff, products, events, landing pages, settings, or reusable content fragments?
   - Determine whether the model is single-site, multisite, or headless-facing.
   - Inventory CPTs, taxonomies, options pages, and field groups before evaluating implementation quality.

2. **Check core content entities first**
   - Validate each CPT has a clear purpose and does not merely duplicate posts/pages without a reason.
   - Check whether taxonomies model classification and relationships better than extra text/meta fields.
   - Flag overloaded post types used as catch-alls for unrelated content.

3. **Review field-group architecture**
   - Inspect location rules, naming conventions, instructions, conditional logic, defaults, and required flags.
   - Check whether field groups are split by editorial task instead of becoming giant monoliths.
   - Verify repeaters and flexible content are used intentionally, not as a substitute for missing entity design.

4. **Scan for CRITICAL patterns**
   - Field names or data shapes changed without a migration path.
   - Environment-specific field keys relied on directly in code.
   - Content that should be relational or taxonomic stored as plain text blobs.
   - Massive `meta_query` dependence for core archive/search behavior with no mitigation.
   - Flexible-content or repeater structures used where separate entities are clearly required.
   - Options-page values treated as request-specific content without cache or invalidation awareness.

5. **Check WARNING patterns**
   - Ambiguous field names (`title`, `image`, `link`) with no domain prefix or context.
   - Duplicate field groups or cloned definitions drifting across environments.
   - Relationship/post object fields with no return-format consistency.
   - Fields exposed to editors with weak instructions, no defaults, or unclear conditional logic.
   - ACF JSON enabled inconsistently or committed unreliably.
   - Repeater-heavy landing pages likely to become impossible to query, reuse, or migrate.

6. **Note INFO improvements**
   - Taxonomies could improve filtering, SEO, or editorial consistency.
   - An options page could replace duplicated per-page settings.
   - A custom table may be justified for high-volume structured data.
   - Shared components may benefit from clone fields or a reusable block strategy.
   - Field instructions, tabs, and groups could reduce editor error rates.

7. **Report with context-aware severity**
   - Enterprise/editorial site: prioritize governance, migration safety, query behavior, and authoring ergonomics.
   - Marketing/landing-page builder: prioritize maintainability and editorial constraints over abstract purity.
   - Headless site: prioritize schema stability, API exposure shape, and relationship modeling.
   - Add cross-skill notes when findings should be followed by `wp-rest-api-development`, `wp-performance-review`, or `wp-block-development`.

## Model-Level Checks

### Content Type Design (ACF-01)

**CRITICAL**
- Multiple unrelated business concepts forced into one CPT with flags like `type`, `layout`, or `kind` doing all the work
- A CPT exists only to simulate grouped fields that belong on an existing content type
- Important relational content stored in serialized arrays or long text fields instead of structured entities

**WARNING**
- CPT labels, supports, or archive behavior do not match editorial intent
- Post types rely on custom fields for primary titles or slugs when core title/slug should carry that job
- Content discoverability depends entirely on custom sorting/meta instead of taxonomy or date semantics

**INFO**
- A taxonomy may be better than another boolean/select field
- A small reusable post type may simplify repeated section content or shared landing-page fragments

### Taxonomy Design (ACF-02)

**CRITICAL**
- Taxonomy-worthy classification modeled as free-text fields, causing duplicate spellings and broken filters
- Relationship semantics forced into repeated text/select fields instead of terms or relationship fields

**WARNING**
- Taxonomies are too broad, mixing audience, topic, location, and workflow state in one structure
- A hierarchical taxonomy is used where flat tagging would be simpler, or vice versa
- Term metadata is added for core entity content that likely deserves its own entity instead

**INFO**
- Taxonomies can often replace fragile editor-entered labels and improve queryability

### Field Naming and Schema Stability (ACF-03)

**CRITICAL**
- Code depends on field keys like `field_123abc` instead of stable field names when not required
- Field names renamed with no migration or backward-compatibility handling
- Two unrelated fields share nearly identical names across contexts, leading to template confusion

**WARNING**
- Names are too generic (`title`, `cta`, `copy`, `image`) and lose meaning outside one template
- Prefixing is inconsistent across domains (`hero_`, `event_`, `team_` mixed unpredictably)
- Return formats vary silently between field groups for the same conceptual field

**INFO**
- Prefix related fields by domain or component to improve grepability and future migrations

### Repeater and Flexible Content Usage (ACF-04)

**CRITICAL**
- Flexible content is used as a full site-builder without governance, creating untestable content permutations
- Repeaters hold data that needs independent URLs, reuse, ownership, or filtering
- Huge nested repeaters are queried or transformed as if they were relational tables

**WARNING**
- Repeater rows have no min/max limits or editor guidance
- Flexible content layouts overlap heavily and indicate missing design-system discipline
- Deep nesting makes migrations, previews, and template maintenance brittle

**INFO**
- Consider dedicated entities, synced patterns, or block-based composition for reusable structures

### Relationship Fields and Return Formats (ACF-05)

**CRITICAL**
- Relationship/post-object fields used without a stable expected return format in code
- Bidirectional relationships are assumed but never maintained consistently

**WARNING**
- Templates call `get_field()` repeatedly inside loops when values could be normalized once
- Relationship field queries are not constrained, making editorial selection noisy and error-prone
- IDs vs objects vs arrays are mixed casually across code paths

**INFO**
- Normalize field access through view-model helpers or DTO-like mappers when templates become repetitive

### Options Pages and Global Settings (ACF-06)

**CRITICAL**
- Frequently changing request-level content is stored globally and expected to vary per page/user/context
- Critical runtime configuration is edited through ACF options with no validation or deployment discipline

**WARNING**
- Sitewide content is duplicated across pages instead of centralized in options/global entities
- Options pages mix marketing copy, integration secrets, and editorial settings in one screen
- Code assumes options always exist and never handles empty defaults

**INFO**
- Split options pages by responsibility and add defaults/instructions for resilience

### ACF JSON and Environment Sync (ACF-07)

**CRITICAL**
- Field-group changes exist only in the database with no committed JSON or export path
- Team workflow routinely overwrites field definitions because sync direction is unclear

**WARNING**
- `acf-json` is committed inconsistently or partially
- Field groups are edited in production without a promotion path
- Local JSON path configuration differs between environments without documentation

**INFO**
- Keep `acf-json` under version control and treat DB-only edits as temporary until exported

### Meta Query and Storage Performance (ACF-08)

**CRITICAL**
- Primary archive/search behavior depends on multiple unindexed `meta_query` clauses at scale
- Repeater/flexible content values are mined through `LIKE` queries for business-critical views
- Numeric/date filtering uses string comparison semantics or inconsistent storage formats

**WARNING**
- Content modeling encourages many joins against `postmeta` for every request
- Derived/aggregated values are recalculated from nested ACF data on each page load
- Query behavior assumes ACF fields are cheap just because the admin UI is convenient

**INFO**
- Promote high-volume query keys into taxonomies, dedicated lookup tables, or precomputed indexes when needed

## Review Heuristics

### Good ACF signs
- Field groups align with clear editorial tasks or components
- CPTs and taxonomies reflect real business entities
- Names are stable, descriptive, and domain-prefixed
- ACF JSON is committed and environment sync is intentional
- Relationship fields and return formats are normalized in code
- Meta usage supports the scale and query patterns of the site

### Common anti-patterns
- “Everything is a page with flexible content forever”
- “Everything is post meta even when it should be taxonomy or a dedicated entity”
- “Editors can build anything” without constraints or safe defaults
- “We query repeater internals directly”
- “We changed field names and hoped templates would keep working”

## Output Format

Use this structure:

```text
# ACF / Content Modeling Review

## Summary
- Scope: plugin/theme/app reviewed
- Modeling maturity: strong / mixed / fragile
- Primary risks: 2-5 bullets

## Critical Findings
- [ACF-XX] Title — file:line or subsystem
  Why it matters
  Recommended fix

## Warning Findings
- [ACF-XX] Title — file:line or subsystem
  Why it matters
  Recommended fix

## Info / Improvement Opportunities
- [ACF-XX] Title — file:line or subsystem
  Suggested improvement

## Modeling Notes
- Entity design observations
- Taxonomy vs meta observations
- Query/storage implications

## Cross-Skill Follow-Up
- Run `/wp-perf-review` if query behavior is the main risk
- Run `/wp-rest-review` if schema exposure or API contracts need review
- Run `/wp-block-review` if field groups power custom blocks heavily
```

## Reference Files

Load these only as needed:
- `references/content-modeling-guide.md`
- `references/acf-json-and-field-group-guide.md`
- `references/meta-query-and-performance.md`

## Final Reminder

This skill should not reward ACF usage merely because it works in the admin. Prefer models that stay understandable after the site doubles in content, editors, and integrations.
