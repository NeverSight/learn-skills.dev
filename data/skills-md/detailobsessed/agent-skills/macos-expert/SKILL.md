---
name: macos-expert
description: Comprehensive modern macOS app development guidance grounded in Apple's Human Interface Guidelines and official Apple developer documentation. Use when building, reviewing, or refactoring macOS software with SwiftUI, AppKit, AppKit-SwiftUI bridging, SwiftData, accessibility, menus, windows, toolbars, sidebars, document and file workflows, drag and drop, sandboxing, distribution, or other Mac-specific platform behavior.
---

# macos-expert

Use this skill to keep macOS work native, modern, and source-backed.

## When to use

- Building, reviewing, or refactoring a macOS app with SwiftUI, AppKit, or both
- Designing windows, toolbars, sidebars, menus, commands, or keyboard shortcuts for macOS
- Implementing document-based apps, file import/export, open/save panels, or Quick Look
- Working with drag and drop, clipboard, undo/redo, or context menus
- Adding or auditing VoiceOver, keyboard navigation, focus, contrast, or motion accessibility
- Choosing between SwiftData, Core Data, UserDefaults, or file-based persistence
- Bridging AppKit and SwiftUI with NSHostingView, NSViewRepresentable, or coordinators
- Configuring sandboxing, entitlements, security-scoped bookmarks, or App Groups
- Building menu bar apps with MenuBarExtra or NSStatusItem
- Setting up login items, extensions, signing, notarization, or distribution
- Reviewing whether a macOS app feels native or carries iOS anti-patterns

## Recommended companion tools

Using [Sosumi](https://sosumi.ai/) alongside this skill is highly recommended. Sosumi provides direct access to Apple Developer documentation and Human Interface Guidelines as Markdown, making it easy to verify APIs, symbols, and platform behavior referenced in this skill against current official sources.

## Source priority

Use sources in this order:

1. Apple Human Interface Guidelines and Apple Developer documentation
2. Reference files in this skill

If a named API, symbol, modifier, entitlement, or platform behavior is uncertain, verify it against current official Apple documentation before presenting it as fact.

Start with `references/official-sources.md` if you need the verification workflow or the canonical Apple source map.

## Core workflow

1. Classify the task: design review, implementation, migration, bug fix, architecture, or distribution
2. Identify the minimum macOS version, primary UI framework, and whether the app is document-based, window-based, or menu-bar-first
3. Load the reference files that match the task instead of reading everything
4. Prefer standard macOS behaviors before inventing custom UI or app flow
5. Call out version constraints, fallback paths, and trade-offs explicitly
6. Distinguish design guidance from API guidance

## Load the right references

- Read `references/designing-for-macos.md` for macOS-first product and UX decisions
  - *Triggers: design review, native feel, platform expectations, Mac vs iPad patterns, layout density*
- Read `references/windows-navigation.md` for windows, toolbars, sidebars, sheets, popovers, inspectors, and full-screen behavior
  - *Triggers: WindowGroup, DocumentGroup, NavigationSplitView, NSWindow, NSToolbar, NSSplitViewController, toolbar, sidebar, inspector, sheet, popover, full-screen, window resize*
- Read `references/menus-commands-input.md` for menu bar structure, commands, shortcuts, undo/redo, clipboard, pointer, keyboard, and drag-and-drop expectations
  - *Triggers: menu bar, NSMenu, .commands, CommandGroup, keyboard shortcut, ⌘, undo, redo, copy, paste, context menu, drag and drop, .draggable, .dropDestination, NSDraggingSource, Dock menu*
- Read `references/file-management-documents.md` for open/save/import/export, document workflows, file access, Quick Look, and Finder-facing behavior
  - *Triggers: DocumentGroup, FileDocument, ReferenceFileDocument, NSDocument, NSOpenPanel, NSSavePanel, .fileImporter, .fileExporter, UTType, Quick Look, Finder, open panel, save panel, recent documents*
- Read `references/accessibility.md` for VoiceOver, keyboard navigation, focus, contrast, motion, and testing
  - *Triggers: VoiceOver, accessibility, .accessibilityLabel, NSAccessibility, focus, keyboard navigation, contrast, reduce motion, assistive technology*
- Read `references/swiftui-macos.md` for modern SwiftUI patterns specific to macOS
  - *Triggers: SwiftUI on macOS, NavigationSplitView, Table, MenuBarExtra, Settings, .searchable, @FocusState, Observation, scene, SwiftUI commands, SwiftUI toolbar*
- Read `references/appkit-and-bridging.md` for AppKit-heavy work and AppKit-SwiftUI integration
  - *Triggers: AppKit, NSHostingView, NSHostingController, NSViewRepresentable, NSViewControllerRepresentable, coordinator, bridging, responder chain, NSTableView, NSOutlineView*
- Read `references/persistence-and-data.md` for SwiftData, Core Data, document data, settings, and migration choices
  - *Triggers: SwiftData, Core Data, @Query, ModelActor, FetchDescriptor, @AppStorage, UserDefaults, persistence, migration, schema, database*
- Read `references/platform-capabilities-distribution.md` for sandboxing, bookmarks, extensions, menu bar apps, login items, signing, notarization, and distribution
  - *Triggers: sandbox, entitlement, security-scoped bookmark, App Group, SMAppService, login item, MenuBarExtra, NSStatusItem, extension, Finder Sync, XPC, notarization, Developer ID, Hardened Runtime, Mac App Store, distribution*

## Non-negotiables

- Prefer Apple-standard windows, toolbars, menus, commands, shortcuts, dialogs, and file flows
- Do not import iOS interaction patterns onto macOS without a clear Mac-specific reason
- Treat accessibility as a default requirement, not a polish pass
- Treat keyboard support, context menus, drag and drop, and undo/redo as core Mac affordances
- If custom UI replaces a standard control, preserve discoverability, keyboard support, and accessibility semantics
- Avoid version-specific or newly announced platform claims unless verified against current official docs

## Common anti-patterns

- Hiding core actions behind a single overflow menu instead of using the menu bar and toolbar
- Giant touch-sized controls that waste space on desktop
- No keyboard navigation, no shortcuts, or no context menus
- Replacing standard window chrome or toolbar behavior without a strong reason
- Building custom file pickers instead of using system open/save panels
- Treating drag and drop as optional in workflows where files or lists are central
- Importing iOS tab bars, bottom sheets, or navigation stacks where Mac-native sidebars, inspectors, or split views belong

## Response expectations

- For reviews, explain what is non-native, why it matters on macOS, and the simplest native fix
- For implementation guidance, prefer native Apple APIs over third-party abstractions unless there is a strong reason not to
- For architecture questions, keep the answer proportional to app size and deployment target
- For file and sandbox questions, address both user experience and entitlement/security implications
