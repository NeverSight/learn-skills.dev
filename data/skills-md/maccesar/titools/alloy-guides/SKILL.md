---
name: alloy-guides
description: "Titanium Alloy MVC official framework reference. Use when working with, reviewing, analyzing, or examining Alloy models, views, controllers, Backbone.js data binding, TSS styling, widgets, Alloy CLI, sync adapters, migrations, or MVC compilation. Explains how Backbone.js models and collections work in Alloy."
argument-hint: "[concept]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(node *)
---

# Alloy MVC framework guide

Reference for building Titanium mobile applications with the Alloy MVC framework and Backbone.js.

## Project detection

:::info AUTO-DETECTS ALLOY PROJECTS
This skill automatically detects Alloy projects when invoked and provides framework-specific guidance.

**Detection occurs automatically** - no manual command needed.

**Alloy project indicators:**
- `app/` folder (MVC structure)
- `app/views/`, `app/controllers/` folders
- `app/models/` folder

**Behavior based on detection:**
- **Alloy detected** → Provides Alloy MVC documentation, Backbone.js patterns, TSS styling, widgets
- **Not detected** → Indicates this skill is for Alloy projects only, does not suggest Alloy-specific features
:::

## Quick reference

| Topic                                            | Reference File                                                          |
| ------------------------------------------------ | ----------------------------------------------------------------------- |
| Core concepts, MVC, Backbone.js, conventions     | [CONCEPTS.md](references/CONCEPTS.md)                                   |
| Controllers, events, conditional code, arguments | [CONTROLLERS.md](references/CONTROLLERS.md)                             |
| Models, collections, data binding, migrations    | [MODELS.md](references/MODELS.md)                                       |
| XML markup, elements, attributes, events         | [VIEWS_XML.md](references/VIEWS_XML.md)                                 |
| TSS styling, themes, platform-specific styles    | [VIEWS_STYLES.md](references/VIEWS_STYLES.md)                           |
| Dynamic styles, autostyle, runtime styling       | [VIEWS_DYNAMIC.md](references/VIEWS_DYNAMIC.md)                         |
| Controllers-less views, patterns                 | [VIEWS_WITHOUT_CONTROLLERS.md](references/VIEWS_WITHOUT_CONTROLLERS.md) |
| Creating and using widgets                       | [WIDGETS.md](references/WIDGETS.md)                                     |
| CLI commands, code generation                    | [CLI_TASKS.md](references/CLI_TASKS.md)                                 |
| PurgeTSS integration (optional addon)            | [PURGETSS.md](references/PURGETSS.md)                                   |

## Project structure

Standard Alloy project structure:

```
app/
├── alloy.js              # Initializer file
├── alloy.jmk             # Build configuration
├── config.json           # Project configuration
├── assets/               # Images, fonts, files (→ Resources/)
├── controllers/          # Controller files (.js)
├── i18n/                 # Localization strings (→ i18n/)
├── lib/                  # CommonJS modules
├── migrations/           # DB migrations (<DATETIME>_<name>.js)
├── models/               # Model definitions (.js)
├── platform/             # Platform-specific resources (→ platform/)
├── specs/                # Test-only files (dev/test only)
├── styles/               # TSS files (.tss)
├── themes/               # Theme folders
├── views/                # XML markup files (.xml)
└── widgets/              # Widget components
```

## MVC quick start

**Controller** (`app/controllers/index.js`):
```javascript
function doClick(e) {
    alert($.label.text);
}
$.index.open();
```

**View** (`app/views/index.xml`):
```xml
<Alloy>
    <Window class="container">
        <Label id="label" onClick="doClick">Hello, World</Label>
    </Window>
</Alloy>
```

**Style** (`app/styles/index.tss`):
```javascript
".container": { backgroundColor: "white" }
"Label": { color: "#000" }
```

## Key concepts

- **Models/Collections**: Backbone.js objects with sync adapters (sql, properties)
- **Views**: XML markup with TSS styling
- **Controllers**: JavaScript logic with `$` reference to view components
- **Data Binding**: Bind collections to UI components automatically
- **Widgets**: Reusable components with MVC structure
- **Conventions**: File naming and placement drive code generation

## Critical rules

### Platform-specific properties in TSS

:::danger CRITICAL: Platform-specific properties require modifiers
Using `Ti.UI.iOS.*` or `Ti.UI.Android.*` properties in TSS without platform modifiers causes cross-platform compilation failures.

Example of the failure:
```tss
// WRONG - Adds Ti.UI.iOS to Android project
"#mainWindow": {
  statusBarStyle: Ti.UI.iOS.StatusBar.LIGHT_CONTENT  // FAILS on Android!
}
```

Correct approach - use platform modifiers:
```tss
// CORRECT - Only adds to iOS
"#mainWindow[platform=ios]": {
  statusBarStyle: Ti.UI.iOS.StatusBar.LIGHT_CONTENT
}

// CORRECT - Only adds to Android
"#mainWindow[platform=android]": {
  actionBar: {
    displayHomeAsUp: true
  }
}
```

Properties that always require platform modifiers:
- iOS: `statusBarStyle`, `modalStyle`, `modalTransitionStyle`, any `Ti.UI.iOS.*`
- Android: `actionBar` config, any `Ti.UI.Android.*` constant

**Available modifiers:** `[platform=ios]`, `[platform=android]`, `[formFactor=handheld]`, `[formFactor=tablet]`, `[if=Alloy.Globals.customVar]`

For more platform-specific patterns, see [Code conventions (ti-expert)](skills/ti-expert/references/code-conventions.md#platform--device-modifiers) or [Platform UI guides (ti-ui)](skills/ti-ui/references/platform-ui-ios.md).
:::

## Common patterns

### Creating a model
```bash
alloy generate model book sql title:string author:string
```

### Data binding
```xml
<Collection src="book" />
<TableView dataCollection="book">
    <TableViewRow title="{title}" />
</TableView>
```

### Platform-specific code
```javascript
if (OS_IOS) {
    // iOS-only code
}
if (OS_ANDROID) {
    // Android-only code
}
```

### Widget usage
```xml
<Widget src="mywidget" id="foo" />
```

## Compilation process

1. Cleanup: Resources folder cleaned
2. Build Config: alloy.jmk loaded (pre:load task)
3. Framework Files: Backbone.js, Underscore.js, sync adapters copied
4. MVC Generation: Models, widgets, views, controllers compiled to JS
5. Main App: app.js generated from template
6. Optimization: UglifyJS optimization, platform-specific code removal

## References

Read detailed documentation from the reference files listed above based on your specific task.

## Related skills

For tasks beyond Alloy MVC basics, use these complementary skills:

| Task                                           | Use This Skill |
| ---------------------------------------------- | -------------- |
| Modern architecture, services, patterns        | `ti-expert`    |
| Alloy CLI, config files, debugging errors      | `alloy-howtos` |
| Utility-first styling with PurgeTSS (optional) | `purgetss`     |
| Native features (location, push, media)        | `ti-howtos`    |
