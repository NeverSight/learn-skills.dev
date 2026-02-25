---
name: dataverse-web-resources
description: >
  Use when creating, deploying, or managing Dataverse web resources for model-driven apps.
  Covers JavaScript form scripts (OnLoad, OnSave, OnChange events), HTML dashboard pages,
  CSS styling, image resources, navigation/side panes, ribbon/command bar customization,
  business process flow client API, and deployment via the Web API. Triggers on: "web resource",
  "javascript form", "form script", "html dashboard", "ribbon command", "onload event",
  "onchange event", "onsave event", "formContext", "Xrm.WebApi", "web resource deployment",
  "dashboard page", "form event handler", "side pane", "command bar", "ribbon", "modal dialog",
  "navigation", "Xrm.App", "Xrm.Navigation", "business process flow", "bpf", "stage change".
license: MIT
compatibility: "Dataverse Web API v9.2, Model-Driven Apps"
metadata:
  author: custom
  version: "1.0.0"
  platform: "Microsoft Power Platform / Dataverse"
---

# Dataverse Web Resources Skill

You are an expert in creating, deploying, and using Dataverse web resources within
model-driven apps. Web resources are virtual files stored in Dataverse that can contain
JavaScript, HTML, CSS, images, and other web content used to extend the application.

## CRITICAL RULES

1. **Always use a publisher prefix namespace** for web resource names (e.g., `cnt_/js/formscript.js`).
   The forward slash creates a virtual folder structure.

2. **JavaScript must use the namespace pattern.** Define all functions inside a namespace object
   to avoid global scope pollution:
   ```javascript
   var MyApp = MyApp || {};
   MyApp.FormScripts = { onLoad: function(executionContext) { ... } };
   ```

3. **Always pass `executionContext`** to form event handlers. Enable "Pass execution context
   as first parameter" when registering. Then: `var formContext = executionContext.getFormContext();`

4. **Content must be base64-encoded** when creating via the API. Use PowerShell's
   `[Convert]::ToBase64String()` or equivalent.

5. **Always publish after creating/updating** web resources. They remain in draft until published.

6. **5MB size limit** per web resource (configurable by org admin). Minify large JS/CSS.

7. **Always consult `resources/ux-decision-guide.md` when choosing controls** — before
   selecting a control type, field format, navigation pattern, or page layout, check the
   decision guide for the recommended approach.

8. **`Xrm` is NOT available in web resources loaded via MDA sitemap.** Web resources loaded
   as sitemap SubAreas run in an iframe where `Xrm` is not injected directly. Use this
   fallback chain: (1) `Xrm.Utility.getGlobalContext()`, (2) `parent.Xrm.Utility.getGlobalContext()`,
   (3) `WhoAmI` API call (`GET /api/data/v9.2/WhoAmI`) for user identity. Cache the result.

9. **Sitemap web resource URL format:** Use `Url="/WebResources/{name}"` (NOT `$webresource:`
   prefix) on `<SubArea>` elements to embed HTML web resources as navigation items.

## Quick Reference

| Operation | Method | Endpoint |
|---|---|---|
| Create web resource | POST | `/webresourceset` |
| Update web resource | PATCH | `/webresourceset({id})` |
| Delete web resource | DELETE | `/webresourceset({id})` |
| Add to solution | Action | `AddSolutionComponent` (ComponentType=61) |
| Publish | Action | `PublishXml` |

## Xrm Client API Quick Reference

| API | Purpose | Target |
|---|---|---|
| `Xrm.App.sidePanes.createPane()` | Open persistent side panel | Web resource, custom page, entity form |
| `Xrm.Navigation.navigateTo()` | Open inline dialog (modal/modeless) | Web resource, custom page |
| `Xrm.Navigation.openWebResource()` | Open web resource in new window/dialog | Web resource |
| `Xrm.Navigation.openForm()` | Open entity form programmatically | Entity form |
| `Xrm.Navigation.openAlertDialog()` | Show alert message | System dialog |
| `Xrm.Navigation.openConfirmDialog()` | Show confirm/cancel prompt | System dialog |
| `Xrm.WebApi.retrieveMultipleRecords()` | Query records from form JS | Dataverse table |
| `Xrm.WebApi.createRecord()` | Create record from form JS | Dataverse table |
| `Xrm.WebApi.updateRecord()` | Update record from form JS | Dataverse table |
| `Xrm.WebApi.deleteRecord()` | Delete record from form JS | Dataverse table |
| `formContext.data.process.getActiveProcess()` | Get active BPF | Form process |
| `formContext.data.process.setActiveProcess(id)` | Switch BPF | Form process |
| `formContext.data.process.moveNext()` / `movePrevious()` | Navigate BPF stages | Form process |
| `formContext.data.process.addOnStageChange(handler)` | Listen for BPF stage changes | Form process |
| `Xrm.Utility.getResourceString(webresource, key)` | Get localized string from RESX | Web resource |

## Resource Files

- `resources/types-reference.md` -- All 12 web resource types with Type IDs and use cases
- `resources/js-form-scripts.md` -- JavaScript for form event handling, field validation, UI manipulation
- `resources/html-dashboards.md` -- HTML pages for dashboards, charts, and KPI displays
- `resources/deployment.md` -- Creating and deploying web resources via the API
- `resources/navigation-side-panes.md` -- Side panes, dialogs, navigation APIs (Xrm.App, Xrm.Navigation)
- `resources/ribbon-command-bar.md` -- Ribbon/command bar customization (modern + classic RibbonDiffXml)
- `resources/ux-decision-guide.md` -- Decision trees for control, layout, and navigation pattern selection
- `resources/bpf-client-api.md` -- Business Process Flow JavaScript API, events, stage navigation, common patterns
