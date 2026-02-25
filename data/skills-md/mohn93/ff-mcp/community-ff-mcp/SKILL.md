---
name: community-ff-mcp
description: >
  Teaches AI assistants how to develop FlutterFlow apps using MCP tools.
  Use this skill when working with FlutterFlow projects, editing FF YAML,
  creating or inspecting pages and components, reading project configuration,
  or navigating FlutterFlow widget trees. It covers all 25 MCP tools for
  discovery, reading, editing, and settings. Triggers on: FlutterFlow,
  FF YAML, FF page, FF component, FF widget, FF theme, FF project.
license: MIT
compatibility: Requires the community-ff-mcp MCP server to be connected and a valid FLUTTERFLOW_API_TOKEN environment variable.
metadata:
  author: mohn93
  version: "1.0"
---

## Prerequisites

This skill requires the **community-ff-mcp** MCP server to be installed and connected. Before proceeding, check if the `list_projects` tool is available. If not, the user needs to set up the MCP server first:

1. Get a FlutterFlow API token from **FlutterFlow > Profile > Account Settings > API Token** (requires a paid FlutterFlow subscription)
2. Add the MCP server to your AI client:
   ```bash
   # Claude Code
   claude mcp add flutterflow -e FLUTTERFLOW_API_TOKEN=<token> -- npx -y community-ff-mcp

   # Other clients (Claude Desktop, Cursor, Windsurf) — add to MCP config:
   # { "command": "npx", "args": ["-y", "community-ff-mcp"], "env": { "FLUTTERFLOW_API_TOKEN": "<token>" } }
   ```
3. Restart your AI client, then verify by calling `list_projects`

## Overview

The FlutterFlow MCP provides 25 tools for reading, inspecting, and editing FlutterFlow projects through YAML. It connects AI assistants to the FlutterFlow Project API, enabling programmatic access to pages, components, themes, actions, data models, and settings. All project data is represented as YAML files that can be fetched, cached locally, validated, and pushed back.

## Tool Catalog

### Discovery & Exploration

| Tool | Purpose |
|------|---------|
| `list_projects` | List all FF projects accessible to your API token |
| `list_project_files` | List YAML file keys in a project (supports prefix filter) |
| `list_pages` | List pages with human-readable names, scaffold IDs, and folders |
| `search_project_files` | Search file keys by keyword, prefix, or regex |
| `sync_project` | Download all project YAML to local cache for fast reads |

### Reading & Understanding

| Tool | Purpose |
|------|---------|
| `get_page_by_name` | Fetch full page YAML by human-readable name |
| `get_project_yaml` | Fetch specific YAML file(s) by file key |
| `get_page_summary` | Quick page overview: widget tree, actions, params (cache-based) |
| `get_component_summary` | Quick component overview: widget tree, params (cache-based) |
| `find_component_usages` | Find all pages/components that use a given component |
| `find_page_navigations` | Find all actions that navigate to a given page |

### Configuration & Settings

| Tool | Purpose |
|------|---------|
| `get_theme` | Theme colors, typography, breakpoints, widget defaults |
| `get_app_state` | App state variables, constants, environment settings |
| `get_api_endpoints` | API endpoint definitions (method, URL, headers, response) |
| `get_data_models` | Data structs, enums, Firestore collections, Supabase tables |
| `get_custom_code` | Custom actions, functions, widgets, AI agents (read-only) |
| `get_general_settings` | App Details, App Assets, Nav Bar & App Bar |
| `get_project_setup` | Firebase, Languages, Platforms, Permissions, Dependencies |
| `get_app_settings` | Authentication, Push Notifications, Deployment settings |
| `get_in_app_purchases` | Stripe, Braintree, RevenueCat, Razorpay config |
| `get_integrations` | Supabase, SQLite, GitHub, Algolia, Google Maps, AdMob, etc. |

### Editing & Documentation

| Tool | Purpose |
|------|---------|
| `get_editing_guide` | Get recommended workflow and docs for a specific editing task |
| `get_yaml_docs` | Search/retrieve YAML reference docs by topic or file path |
| `validate_yaml` | Validate YAML content before pushing changes |
| `update_project_yaml` | Push validated YAML changes to the FF project |

## Core Workflows

### Discover & Explore a Project

Use this workflow when first connecting to a FlutterFlow project or when you need to understand its structure.

```
1. list_projects → pick the target projectId
2. sync_project(projectId) → cache all YAML locally for fast reads
3. list_pages(projectId) → see all pages with human-readable names, scaffold IDs, folders
4. get_page_summary(projectId, pageName) → widget tree overview for any page of interest
```

After syncing, all cache-based tools (`get_page_summary`, `get_component_summary`, `get_theme`, `get_app_state`, etc.) work without additional API calls.

### Read / Inspect a Page or Component

Use this workflow to understand what a page contains, how it is structured, and how it connects to the rest of the app.

```
1. get_page_summary(projectId, pageName) → quick overview of widget tree, actions, params
2. get_page_by_name(projectId, pageName) → full YAML if you need complete details
3. find_page_navigations(projectId, pageName) → discover what actions navigate here
4. find_component_usages(projectId, componentName) → find everywhere a component is used
```

For components, use `get_component_summary` instead of `get_page_summary`. Component summaries resolve nested component references so you can see the full hierarchy.

### Edit an Existing Widget

Use this workflow to modify a specific widget on a page without affecting the rest of the page.

```
1. get_page_by_name(projectId, pageName) → get the full page YAML
2. Identify the node file key for the target widget (format: page/id-Scaffold_XXX/page-widget-tree-outline/node/id-Widget_YYY)
3. get_project_yaml(projectId, fileName: "page/id-.../node/id-Widget_XXX") → fetch the individual node YAML
4. Modify the YAML — keep inputValue and mostRecentInputValue in sync
5. validate_yaml(projectId, fileKey, content) → check for errors before pushing
6. update_project_yaml(projectId, {fileKey: content}) → push changes
```

Always edit at the node level. Editing the full page YAML for a single widget change risks overwriting unrelated content and is more error-prone.

### Add a New Widget to a Page

Use this workflow when you need to add new widgets to an existing page.

```
1. get_page_by_name(projectId, pageName) → understand the current widget tree structure
2. get_yaml_docs(topic: "WidgetType") → look up the YAML schema for the widget you want to add
3. Update the page-widget-tree-outline to include a reference to the new widget key
4. Create individual node files for each new widget (one file per widget)
5. validate_yaml → validate the tree outline first, then each node file
6. update_project_yaml → push tree outline + all node files together in one call
```

Pushing the tree outline and node files in a single call is critical. The server strips inline widget children from the tree outline, so nodes must be separate files.

### Create a Reusable Component

Use this workflow to build a new component from scratch.

```
1. get_yaml_docs(topic: "create component") → get the full walkthrough and required file structure
2. Design component parameters: name, dataType, isNullable for each param
3. Create these files: component metadata, widget-tree-outline, root node (with isDummyRoot: true), child nodes
4. validate_yaml → validate all files before pushing
5. update_project_yaml → push all component files in one call
```

Remember: the root node of a component must have `isDummyRoot: true`. Callback triggers use `triggerType: CALLBACK` with a separate `parameterIdentifier` field. WidgetProperty params use `widgetProperty` in parameterPasses, not `inputValue`.

## Critical YAML Rules

1. **Sync inputValue and mostRecentInputValue** -- Both fields must always contain the same value when you set or update them. If you change one, change both. Exceptions: `fontWeightValue` and `fontSizeValue` only accept `inputValue` (they have no `mostRecentInputValue` field).

2. **Use node-level file keys for edits** -- Target `page/id-Scaffold_XXX/page-widget-tree-outline/node/id-Widget_YYY` for individual widget edits. Never edit the full page YAML (`page/id-Scaffold_XXX`) just to change a single widget. Full-page edits risk overwriting unrelated content and are harder to validate.

3. **Always validate before pushing** -- Call `validate_yaml` before every `update_project_yaml` call. Validation catches missing node files, unknown fields, invalid enum values, and structural problems. Skipping validation risks corrupting the project.

4. **Push tree outline and node files together** -- When adding new widgets, include the updated `page-widget-tree-outline` AND all individual node files in a single `update_project_yaml` call. Widget children embedded inline in the tree outline will be silently stripped by the FlutterFlow server.

5. **Column has no mainAxisSize field** -- To achieve shrink-to-content behavior (equivalent to `MainAxisSize.min` in Flutter), use `minSizeValue: { inputValue: true }` on the Column widget instead.

6. **AppBar templateType** -- Only `LARGE_HEADER` is a confirmed valid value. Do not use `STANDARD` as it may cause unexpected behavior. Control the AppBar height through the `toolbarHeight` property instead.

7. **Custom code is read-only** -- Custom actions, functions, widgets, and AI agents cannot be created or edited through the MCP API. Use `get_custom_code` to read their signatures and source code, but any modifications must be made directly in the FlutterFlow UI. Attempting to push custom code changes will silently corrupt or be ignored.

## Anti-Patterns

- **Don't use `list_project_files` to find pages** -- It returns raw file keys without human-readable names. Use `list_pages` instead, which gives you page names, scaffold IDs, and folder assignments.

- **Don't fetch pages one-by-one to browse a project** -- This is slow and wastes API calls. Use `sync_project` to cache everything locally first, then use `get_page_summary` for quick overviews of any page.

- **Don't edit full page YAML for a single widget change** -- Full-page edits can overwrite other widgets, actions, or parameters. Always use node-level file keys for targeted, safe edits.

- **Don't guess YAML field names or enum values** -- FlutterFlow YAML has specific field names and valid values that are not always intuitive. Use `get_yaml_docs(topic)` or `get_editing_guide(task)` to look up the correct schema before writing YAML.

- **Don't embed widget children inline in the tree outline** -- The FlutterFlow server silently strips inline children from the `page-widget-tree-outline` file. Always create separate node files for each widget.

- **Don't push custom code changes through the API** -- The API silently corrupts or ignores Dart code edits for custom actions, functions, and widgets. These must be edited in the FlutterFlow UI.

## Documentation Lookup

The MCP server ships with 21 built-in reference documents. Use these tools to look up schemas, patterns, and conventions **before** writing YAML:

| When you need... | Call |
|------------------|------|
| Widget schema (Button, Text, Container, etc.) | `get_yaml_docs(topic: "Button")` |
| Action chains, triggers, navigation | `get_yaml_docs(topic: "actions")` |
| Data binding, variable sources | `get_yaml_docs(topic: "variables")` |
| Colors, typography, dimensions | `get_yaml_docs(topic: "theming")` |
| Creating components from scratch | `get_yaml_docs(topic: "create component")` |
| Editing workflows and anti-patterns | `get_yaml_docs(topic: "editing")` |
| Data structs, enums, collections | `get_yaml_docs(topic: "data")` |
| Full docs index | `get_yaml_docs()` |
| Guided workflow for a specific task | `get_editing_guide(task: "change the button color")` |

Always consult the docs before writing YAML. They contain validated schemas, field references, enum values, and real examples.
