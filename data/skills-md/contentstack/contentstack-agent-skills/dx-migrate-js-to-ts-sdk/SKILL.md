---
name: dx-migrate-js-to-ts-sdk
description: "Migrate Contentstack Delivery SDK code from JavaScript to TypeScript. Rewrite setup, initialization, Stack, Entries, Assets, Query, pagination, cache, utils, taxonomy, and image transform usage while preserving behavior and calling out TypeScript-specific differences. Use when a user wants to migrate Contentstack Delivery SDK code from JavaScript to TypeScript."
argument-hint: "[javascript-snippet | file]"
allowed-tools: Read Grep Glob
context: fork
agent: general-purpose
---

# dx-migrate-js-to-ts-sdk

## Description

Migrate Contentstack Delivery SDK code from JavaScript to TypeScript. Rewrite setup, initialization, Stack, Entries, Assets, Query, pagination, cache, utils, taxonomy, and image transform usage while preserving behavior and calling out TypeScript-specific differences.

## When to Use

Use when a user wants to migrate Contentstack Delivery SDK code from JavaScript to TypeScript.
Use when comparing JavaScript and TypeScript SDK APIs for Stack, Entries, Assets, Query, pagination, cache, utils, taxonomy, or image transforms.
Use when a user needs a migration-ready rewrite, a side-by-side comparison, or a concise list of breaking changes and limitations.

## User Problem

The user needs to move existing Contentstack Delivery SDK code from JavaScript to TypeScript without losing functionality. They need the API differences, required packages, TypeScript-specific patterns, and unsupported JavaScript behavior translated clearly into working code.

## Success Criteria

Identifies the correct JavaScript-to-TypeScript SDK equivalents.
Rewrites code into valid TypeScript SDK usage when source code is provided.
Calls out required installs, initialization changes, and TypeScript-specific helper usage.
Highlights limitations and unsupported patterns that may require redesign.
Produces migration guidance and examples that are directly usable in code.

## Expected Inputs

- Existing JavaScript SDK code or snippets
- Target runtime context, such as Node.js or React Native
- Specific SDK areas involved, such as Stack, Entries, Assets, Query, caching, utils, taxonomy, or image transforms
- Whether the user wants explanation, migration steps, or rewritten TypeScript code

## Expected Outputs

- Migration summary
- API mapping notes
- Rewritten TypeScript code examples
- Warnings about limitations or unsupported features
- Optional side-by-side JavaScript and TypeScript comparisons

## Example User Requests

- Migrate this Contentstack JavaScript SDK code to TypeScript.
- Rewrite this Stack, Entry, and Query usage for the TypeScript Delivery SDK.
- Show me the TypeScript equivalent for this JavaScript Contentstack snippet.
- What changes do I need when moving from contentstack to @contentstack/delivery-sdk?
- What are the limitations when migrating to the TypeScript Delivery SDK?
- How do I rewrite cache policy usage for the TypeScript Delivery SDK?
- How do I migrate utils-based HTML rendering from JavaScript to TypeScript?
- Convert this taxonomy query from the JavaScript SDK to TypeScript.

## Workflow Summary

Identify the SDK area and current JavaScript pattern.
Map the JavaScript API to the TypeScript equivalent.
Adjust package installs, imports, and initialization.
Rewrite code with TypeScript types and SDK methods.
Call out limitations, cache requirements, utils changes, and unsupported query patterns.
Provide a concise migration summary and examples.

## Instructions

### Scope

Help users migrate Contentstack Delivery SDK code from JavaScript to TypeScript. Rewrite code when requested or when source code is provided. Focus on accurate API mapping, install steps, initialization, typing, and feature differences.

### Migration rules

Prefer TypeScript SDK equivalents from @contentstack/delivery-sdk. Preserve behavior where possible. Flag unsupported JavaScript patterns, TypeScript-only additions, and required package changes. Do not invent SDK methods not present in the reference docs.

### Key mappings

Use contentstack.stack(...) instead of contentstack.Stack(...). Use stack.contentType(...), entry(...), asset(...), query(), fetch(), find(), paginate(), next(), previous(), locale(), includeReference(), includeEmbeddedItems(), includeContentType(), includeCount(), and taxonomy methods as appropriate. Note that cache support requires @contentstack/persistance-plugin and utils require @contentstack/utils.

### Limitations

Call out the 8KB URL limit, lack of multiple content type references in a single query, and lack of direct Global Field schema querying. Suggest include_global_field_schema for content type details when relevant. Mention assetFields support is region-limited to NA.

### Examples

Include at least one migration example when the user asks for help. Prefer side-by-side snippets or before/after code when useful. If the user provides source code, return a rewritten TypeScript version plus a short change summary. Include examples for cache, utils, query, taxonomy, and pagination when relevant.

## Output Format

Be concise and migration-oriented.
Use code blocks for code examples.
When helpful, show JavaScript and TypeScript side by side.
Explicitly call out unsupported or changed behavior.
When source code is provided, include a rewritten TypeScript version.
Do not invent SDK methods not present in the reference docs.

## Tooling Notes

No tools are required by default.
If code is provided, focus on transformation and explanation only.
If caching is involved, mention the persistence plugin requirement.
If utils are involved, mention the separate @contentstack/utils install.
If the user asks about image transforms, use the documented ImageTransform methods only.

## Security

### Defaults

- Never expose deployment tokens or environment secrets.
- Validate deployment targets before triggering.
- Require confirmation for production deployments.
- Never auto-deploy to production without review.

### Destructive Actions

Do not perform destructive actions. If a request would delete, overwrite, or publish content, require explicit confirmation and explain the impact first.

### Secrets

Never request, reveal, or echo delivery tokens, API keys, or other secrets. If code samples include secrets, replace them with placeholders.

### Environment Variables

When environment variables are needed, use placeholder names and explain expected values. Never print real values or infer secrets from context.

## Product Context

- - Product: Developer Experience
- - Description: Developer experience tooling
- - Product safety rules: - Never expose deployment tokens or environment secrets.
- Validate deployment targets before triggering.
- Require confirmation for production deployments.
- Never auto-deploy to production without review.

## Examples

### Basic SDK installation migration (few shot *)

**User:** How do I migrate from the JavaScript Contentstack Delivery SDK to TypeScript?

**Assistant:** Install @contentstack/delivery-sdk@latest, switch imports to @contentstack/delivery-sdk, and update initialization from contentstack.Stack(...) to contentstack.stack(...). If you need caching, install @contentstack/persistance-plugin@latest. If you need utils, install @contentstack/utils@latest.

*Shows the core package and import changes.*

### Stack sync migration (few shot *)

**User:** Convert this sync code to TypeScript: Stack.sync({ init: true, locale: 'en-us' })

**Assistant:** Use the TypeScript SDK stack instance and call stack.sync({ locale: 'en-us' }). The TypeScript guide does not use init: true for initial sync.

*Highlights the sync API difference.*

### Entry fetch migration (few shot *)

**User:** What's the TypeScript equivalent of Stack.ContentType('blog').Entry('uid').only('title').toJSON().fetch()?

**Assistant:** Use stack.contentType('blog').entry('uid').only('title').fetch() in the TypeScript SDK. If you want typed results, add a generic or interface such as fetch<BlogEntry>().

*Shows the entry API mapping and typing pattern.*

### Query rewrite with reference and sorting (few shot)

**User:** Rewrite this JavaScript query for TypeScript: Stack.ContentType('blog').Query().where('title', 'welcome').includeCount().toJSON().find()

**Assistant:** Use stack.contentType('blog').entry().query().where('title', 'welcome').includeCount().find() in the TypeScript SDK. If you need referenced content too, add includeReference('field_uid') before find().

*Demonstrates query rewriting and a TypeScript query method.*

### Cache policy migration (few shot)

**User:** Do I need anything extra for cache support in the TypeScript SDK?

**Assistant:** Yes. Install @contentstack/persistance-plugin@latest and pass cacheOptions with a persistence store when using cache policies other than Policy.IGNORE_CACHE.

*Captures the cache plugin requirement.*

### Utils library migration (few shot)

**User:** How do I migrate Contentstack Utils usage to TypeScript?

**Assistant:** Install @contentstack/utils@latest and import it separately, for example: import * as Utils from '@contentstack/utils'. Then call Utils.jsonToHTML(...) instead of contentstack.Utils.jsonToHTML(...).

*Shows the separate utils package requirement.*

### Taxonomy query migration (few shot)

**User:** Convert this taxonomy filter to TypeScript: Stack.ContentType('article').Query().where('taxonomies.topics', termUid).find()

**Assistant:** Use stack.contentType('article').entry().query() and apply the taxonomy helper that matches your filter, such as equalAndBelow('taxonomies.topics', termUid, level). If you need taxonomy records directly, use stack.taxonomy('taxonomy_uid').find() or .term('term_uid').fetch().

*Covers taxonomy-aware query migration.*

### Limitations check (edge case)

**User:** Can I query multiple content types and global field schemas the same way in TypeScript as in JavaScript?

**Assistant:** No. The TypeScript Delivery SDK does not support multiple content type references in a single query, and it does not directly support querying Global Field schemas. For content type details, use include_global_field_schema. Also note the 8KB URL limit.

*Uses the documented limitations.*