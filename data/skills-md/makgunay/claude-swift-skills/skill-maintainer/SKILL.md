---
name: skill-maintainer
description: Meta-skill for ingesting Apple developer documentation (WWDC transcripts, API docs, migration guides, release notes) and using it to create, update, or improve Swift/macOS development skills. Trigger when user uploads new Apple documentation, asks to update skills with new API information, requests skill creation from documentation, says "ingest this", "update skills with this", or provides markdown/text files containing Apple framework documentation. Also trigger when user asks to audit existing skills for staleness, merge overlapping skills, or check skills against new OS releases.
---

# Skill Maintainer — Documentation Ingestion & Skill Updater

Process new Apple developer documentation and route extracted knowledge into the correct skill files.

## Workflow

### Step 1: Classify Incoming Documentation

Read each uploaded document and classify it by answering:

| Question | Action |
|----------|--------|
| Which framework(s) does it cover? | Map to target skill(s) using the Skill Registry below |
| Is this a new API or an update to an existing one? | New → may need new skill; Update → patch existing |
| What's the minimum deployment target? | Tag patterns with OS version requirements |
| Does it deprecate anything? | Add to Critical Constraints in target skill |

If a document spans multiple skills (e.g., "SwiftUI-WebKit-Integration" touches both `swiftui-core` and a potential `swiftui-webkit` skill), extract relevant portions into each.

### Step 2: Extract Actionable Content

From each document, extract exactly these categories:

**Patterns** — Working, copy-pasteable code blocks with:
- The API call or view/modifier being demonstrated
- Required imports
- Minimum OS version (if not the latest)
- Inline comments on non-obvious behavior

**Constraints** — Things an LLM will get wrong:
- Deprecated APIs that the new one replaces (❌ old → ✅ new)
- Parameters that changed names or types
- Behaviors that differ from what the name implies
- Common mistakes visible in the doc's "Best Practices" or notes

**Decision Logic** — When to use which approach:
- If the doc presents multiple approaches (e.g., `.background` vs `.foreground(.dynamic)` intent modes), capture the decision tree
- If the doc distinguishes platform availability, capture the conditional

**References** — Source links:
- Apple Developer Documentation URLs
- WWDC session links with year

### Step 3: Diff Against Existing Skills

Before writing, read the target skill file(s) and check:

1. **Duplicate patterns** — Does this pattern already exist? If yes, check if the new version supersedes it
2. **Contradictions** — Does the new doc contradict existing constraints? If yes, the new doc wins (it's more recent)
3. **Gaps** — Does the existing skill lack coverage for this area? If yes, add a new section
4. **Deprecations** — Does the new doc make any existing patterns obsolete? If yes, move old pattern to constraints with ❌

### Step 4: Update Target Skills

Apply changes following the target skill's internal structure. Every skill should maintain these sections (add if missing):

```
## Critical Constraints        ← ❌ DO NOT / ✅ INSTEAD rules
## Decision Tree               ← When to use what
## Verified Patterns           ← Working code blocks
  ### Pattern: [Name]          ← Each with OS version tag
## Common Mistakes & Fixes     ← Table format
## References                  ← Apple doc + WWDC links
```

**Formatting rules for inserted content:**

- Tag every pattern with version: `<!-- Verified: macOS 26, Swift 6.2, Xcode 26 -->`
- Prefix new constraints with the source: `<!-- Source: SwiftUI-New-Toolbar-Features.md -->`
- Keep code blocks self-contained (include imports)
- Prefer short inline comments over paragraph explanations

### Step 5: Handle New Skills

If the document covers a framework with **no existing skill**, create one:

1. Use the Skill Registry to confirm no existing skill covers it
2. Create `SKILL.md` with proper frontmatter
3. Follow the standard section structure above
4. If content exceeds ~400 lines, split into `SKILL.md` (core workflow + index) and `references/` files
5. Register the new skill in the registry

### Step 6: Report Changes

After processing, output a summary:

```
## Ingestion Report

### Documents Processed
- [filename] → [target skill(s)]

### Changes Made
| Skill | Action | Details |
|-------|--------|---------|
| swift-lang | UPDATED | Added @concurrent attribute pattern, Swift 6.2 default MainActor isolation |
| liquid-glass | UPDATED | Added WidgetKit accented rendering mode |
| swiftui-webkit | CREATED | New skill — WebView/WebPage APIs from SwiftUI-WebKit-Integration.md |

### Deprecations Flagged
- `NavigationView` → `NavigationSplitView` (swiftui-core)
- `ObservableObject` → `@Observable` for macOS 14+ (swift-lang)

### Unresolved
- [any docs that didn't map cleanly — ask user for guidance]
```

## Skill Registry

Map frameworks/topics to target skills. Update this when creating new skills.

| Framework / Topic | Target Skill | Reference Files |
|---|---|---|
| Swift language, concurrency, value types, macros | `swift-lang` | — |
| SwiftUI views, navigation, state, toolbars, text | `swiftui-core` | — |
| SwiftData models, queries, inheritance, migration | `swiftdata` | — |
| macOS app lifecycle, windows, scenes, entitlements | `macos-app-structure` | — |
| AppKit bridging, NSView, NSPanel, NSEvent | `appkit-bridge` | — |
| Global hotkeys, CGEvent, keyboard monitoring | `global-hotkeys` | — |
| Clipboard, text insertion, paste simulation | `pasteboard-textinsertion` | — |
| macOS permissions, Accessibility, TCC | `macos-permissions` | — |
| Liquid Glass (SwiftUI, AppKit, UIKit, WidgetKit) | `liquid-glass` | Per-framework reference files |
| WebView, WebPage, WebKit in SwiftUI | `swiftui-webkit` | — |
| FoundationModels, on-device LLM, @Generable | `foundation-models` | — |
| AppIntents, Siri, Shortcuts, Spotlight | `app-intents` | — |
| StoreKit, IAP, subscriptions | `macos-distribution` | — |
| Swift Testing, @Test, #expect | `testing-swift` | — |
| MapKit, GeoToolbox, PlaceDescriptor | `mapkit-geo` (optional) | — |
| Charts, Chart3D, SurfacePlot | `charts-3d` (optional) | — |

**Unmapped content**: If a document doesn't fit any existing skill, flag it and ask the user whether to create a new skill or fold it into an existing one.

## Classification Heuristics

Use these signals to auto-classify documents:

| Signal in Document | Likely Target Skill |
|---|---|
| `import SwiftUI` + view/modifier patterns | `swiftui-core` |
| `import SwiftData` or `@Model` | `swiftdata` |
| `import AppKit` or `NS*` classes | `appkit-bridge` |
| `import FoundationModels` or `LanguageModelSession` | `foundation-models` |
| `import WebKit` + `WebView`/`WebPage` | `swiftui-webkit` |
| `import AppIntents` or `AppIntent` protocol | `app-intents` |
| `import StoreKit` | `macos-distribution` |
| `glassEffect`, `GlassEffectContainer`, `Liquid Glass` | `liquid-glass` |
| `@concurrent`, `nonisolated`, `Sendable`, actor isolation | `swift-lang` |
| `InlineArray`, `Span`, `MutableSpan` | `swift-lang` |
| `CGEvent`, `NSEvent.addGlobalMonitor` | `global-hotkeys` |
| `NSPasteboard`, `AXUIElement` | `pasteboard-textinsertion` |
| `AXIsProcessTrusted`, permission prompts | `macos-permissions` |
| `WindowGroup`, `MenuBarExtra`, `Settings` scene | `macos-app-structure` |
| `@Test`, `#expect`, `@Suite` | `testing-swift` |

## Quality Rules

When updating skills, enforce these standards:

1. **No orphan code** — Every code block must include required `import` statements
2. **No version ambiguity** — Every pattern tagged with minimum OS version
3. **No stale deprecations** — If adding a new way, mark the old way as ❌
4. **No duplicates** — Search existing skill before inserting; merge if similar
5. **Constraints > Patterns** — It's more valuable to tell the agent what NOT to do than to show one more example
6. **Size budget** — SKILL.md body stays under 500 lines; overflow goes to `references/`
7. **Self-contained patterns** — Each code block should compile independently if pasted into a fresh file with the right imports

## Batch Processing

When processing multiple documents at once:

1. Read all documents first to build a complete picture
2. Group by target skill to minimize file edits
3. Process in dependency order: `swift-lang` first (language level), then frameworks
4. Deduplicate across documents (e.g., Liquid Glass appears in 4 docs — consolidate)
5. Generate a single unified ingestion report at the end
