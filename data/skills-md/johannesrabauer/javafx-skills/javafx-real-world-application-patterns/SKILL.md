---
name: javafx-real-world-application-patterns
description: Compose multiple JavaFX skills into realistic editor, dashboard, media, and developer-tool application blueprints.
triggers:
  - javafx app architecture example
  - javafx editor app pattern
  - javafx dashboard app pattern
  - javafx developer tool ui
compatibility:
  java: 17+
  javafx: 21+
category: app-patterns
tags:
  - blueprints
  - editors
  - dashboards
  - developer-tools
  - media-apps
metadata:
  scope: repository
  maturity: starter
allowed-tools:
  - view
  - rg
  - apply_patch
---

# JavaFX Real-World Application Patterns

Use this skill when the user is not asking for one isolated widget or API, but for a whole product
shape such as an editor, developer tool, dashboard, or media-oriented desktop application.

## Example blueprint

```text
Editor-style app
- Shell: BorderPane or workbench shell
- Navigation: tabbed documents + side panels
- State: view model or reducer-backed document state
- Async: background parsing and search indexing
- Packaging: jlink / jpackage desktop distribution
```

## Pattern selection

1. **Editor / document tool** — combine `javafx-rich-text-documents-editors`,
   `javafx-desktop-shell-integration`, and `javafx-testing-packaging-distribution`.
2. **Dashboard / analytics app** — combine `javafx-data-visualization-dashboards`,
   `javafx-concurrency-services`, and `javafx-theming-icons-styling`.
3. **Developer tool** — combine `javafx-ui-layout-navigation`, `javafx-devtools-inspection-debugging`,
   `javafx-reactive-binding-state`, and `javafx-testing-packaging-distribution`.
4. **Media / browser / content app** — combine `javafx-media-webview-3d`,
   `javafx-web-maps-embedded-integration`, and `javafx-desktop-shell-integration`.

## Setup notes

- Treat these as composed product blueprints, not substitute APIs.
- Choose a small number of skills that own the main product constraints instead of activating the
  entire catalog.
- Keep architecture, async work, and packaging decisions visible in the first project iteration.

## Gotchas

- Real products almost always combine several skill domains; forcing one mega-skill is usually worse
  than composing two or three focused ones.
- Workspace persistence, import/export, background work, and error reporting are what distinguish
  usable desktop apps from demos.
