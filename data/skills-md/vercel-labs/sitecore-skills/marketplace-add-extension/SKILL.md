---
name: marketplace-add-extension
description: Adds a new extension point route to a Sitecore Marketplace app. Use when the user wants to add a custom field, dashboard widget, context panel, fullscreen page, or standalone route.
argument-hint: "[extension-type]"
---

# Add an Extension Point Route

You are helping the user add a new extension point to their Sitecore Marketplace app.

## Step 1: Determine Extension Type

Ask the user which type (or infer from $ARGUMENTS):

| Type | Slug | Description | Typical Size |
|------|------|-------------|-------------|
| **Custom Field** | `custom-field` | Inline field in content editor | ~300px wide |
| **Dashboard Widget** | `dashboard-widget` | Widget on the dashboard | ~400x300px |
| **Pages Context Panel** | `pages-context-panel` | Side panel in Pages editor | ~350px wide, full height |
| **Fullscreen** | `fullscreen` | Full-page within Sitecore shell | Full viewport |
| **Standalone** | `standalone` | Independent page | Full viewport |

## Step 2: Generate the Route

Create the route at `app/<extension-type>/page.tsx` (or a custom path the user prefers).

See [extension-types.md](references/extension-types.md) for complete boilerplate templates for each extension type.

## Step 3: Register in Developer Portal

Remind the user to register the extension point in the Sitecore Developer Portal:
1. Go to Developer Portal → Your App → Extension Points
2. Click "Add Extension Point"
3. Select the type and set the route path (e.g., `/custom-field`)

## Step 4: Suggest Next Steps

- Use `/marketplace-build-component` to build out the UI
- Use `/marketplace-sdk-reference` to look up available queries/mutations for this extension type
- Use `/marketplace-add-xmc` if the extension needs XM Cloud data

## Reference Files
- [Extension Types](references/extension-types.md) — Boilerplate templates for each extension type
