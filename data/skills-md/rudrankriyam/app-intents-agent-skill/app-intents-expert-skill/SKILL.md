---
name: app-intents-expert-skill
description: Expert App Intents guidance for building Siri, Shortcuts, Spotlight, Apple Intelligence, and interactive snippet integrations on iOS 26+. Use when implementing AppIntent, AppEntity, AppEnum, EntityQuery, AppShortcutsProvider, SnippetIntent, SiriTipView, IndexedEntity, or when making an app work with Siri, Shortcuts, Spotlight, Apple Intelligence, Visual Intelligence, Action Button, or Apple Pencil. Also use when asked about App Intents architecture, intent-driven development, or migrating from SiriKit.
license: MIT
metadata:
  author: rudrankriyam
  version: "1.0"
---

# App Intents Expert Skill

Expert guidance for the App Intents framework on iOS 26+. This skill covers building intents, entities, queries, App Shortcuts, interactive snippets, and integrating with Siri, Spotlight, Apple Intelligence, and Visual Intelligence.

## When to use this skill

Use this skill when the developer is:
- Creating or modifying any `AppIntent`, `AppEntity`, `AppEnum`, or `EntityQuery`
- Adding Siri, Shortcuts, Spotlight, or Apple Intelligence support to an app
- Building `AppShortcutsProvider` or App Shortcuts
- Implementing interactive snippets with `SnippetIntent`
- Indexing entities for Spotlight with `IndexedEntity`
- Integrating with Visual Intelligence or image search
- Navigating with `TargetContentProvidingIntent` and `onAppIntentExecution`
- Migrating from SiriKit (`INIntent`) to App Intents
- Debugging App Intents build errors or runtime issues

## Task-based routing

Based on what the developer needs, read the relevant reference files.

### "I want to create my first App Intent"
1. Read [references/intent-fundamentals.md](references/intent-fundamentals.md)
2. Then [references/shortcuts-provider.md](references/shortcuts-provider.md) for discoverability

### "I want my app's content searchable in Siri and Spotlight"
1. Read [references/entities-and-queries.md](references/entities-and-queries.md)
2. Then [references/spotlight-indexing.md](references/spotlight-indexing.md)
3. Then [references/siri-integration.md](references/siri-integration.md)

### "I want to integrate with Apple Intelligence and the new Siri"
1. Read [references/apple-intelligence.md](references/apple-intelligence.md)
2. Then [references/siri-integration.md](references/siri-integration.md)
3. Then [references/intent-fundamentals.md](references/intent-fundamentals.md) if new to the framework

### "I want to build interactive snippets"
1. Read [references/interactive-snippets.md](references/interactive-snippets.md)
2. Then [references/intent-fundamentals.md](references/intent-fundamentals.md) if not familiar with intents

### "I want to add Shortcuts and Siri phrases to my app"
1. Read [references/shortcuts-provider.md](references/shortcuts-provider.md)
2. Then [references/siri-integration.md](references/siri-integration.md)

### "I want to structure my app around App Intents"
1. Read [references/intent-driven-architecture.md](references/intent-driven-architecture.md)
2. Then [references/entities-and-queries.md](references/entities-and-queries.md)
3. Then [references/intent-fundamentals.md](references/intent-fundamentals.md)

### "I want to support Visual Intelligence / image search"
1. Read [references/apple-intelligence.md](references/apple-intelligence.md) — image search section
2. Then [references/entities-and-queries.md](references/entities-and-queries.md)

### "I'm migrating from SiriKit"
1. Read [references/migration-from-sirikit.md](references/migration-from-sirikit.md)
2. Then [references/intent-fundamentals.md](references/intent-fundamentals.md)

### "I need to test my App Intents"
1. Read [references/testing-intents.md](references/testing-intents.md)

### "I'm hitting build errors or runtime issues"
1. Read [references/common-pitfalls.md](references/common-pitfalls.md)

## Quick-reference checklists

### Minimum viable App Intent
- [ ] Create a struct conforming to `AppIntent`
- [ ] Add a `static let title: LocalizedStringResource`
- [ ] Implement `func perform() async throws -> some IntentResult`
- [ ] Add `@Parameter` for any inputs
- [ ] Add a `ParameterSummary` for all required parameters
- [ ] Set `supportedModes` if the intent should foreground the app

### Minimum viable App Entity
- [ ] Create a struct conforming to `AppEntity`
- [ ] Add a persistent, unique `id` property
- [ ] Add `@Property` or `@ComputedProperty` for each exposed property
- [ ] Provide `typeDisplayRepresentation` and `displayRepresentation`
- [ ] Create an `EntityQuery` with `entities(for:)` method
- [ ] Set `static let defaultQuery` on the entity
- [ ] Register data dependencies with `AppDependencyManager`

### Minimum viable App Shortcut
- [ ] Create an `AppShortcutsProvider` with `static var appShortcuts`
- [ ] Create `AppShortcut` instances with intent, phrases, shortTitle, systemImageName
- [ ] Every phrase must include `\(.applicationName)`
- [ ] At most one `@Parameter` per phrase
- [ ] Call `updateAppShortcutParameters()` when suggested entities change

### Making an entity Spotlight-searchable
- [ ] Conform entity to `IndexedEntity`
- [ ] Add `indexingKey` parameter to `@Property` attributes
- [ ] Donate entities using the framework's indexing APIs
- [ ] Implement an `OpenIntent` so tapping results navigates to the entity

### Adding interactive snippets (iOS 26+)
- [ ] Create a struct conforming to `SnippetIntent`
- [ ] Mark all view-driving variables as `@Parameter`
- [ ] Return `.result(view:)` from `perform()`
- [ ] Use `Button(intent:)` or `Toggle(intent:)` in the snippet view
- [ ] Return `ShowsSnippetIntent` from the parent intent
- [ ] Do NOT mutate app state in the snippet intent's perform method

## Key decision tree

### Which protocol should my intent conform to?

```
Is it a basic action?
  → AppIntent

Does it open your app to show content?
  → OpenIntent + TargetContentProvidingIntent

Does it render an interactive view?
  → SnippetIntent

Should it support undo?
  → UndoableIntent

Does it match an Apple Intelligence domain?
  → Use @AppIntent macro with the appropriate schema
```

### Which entity type should I use?

```
Is the set of values fixed and known at compile time?
  → AppEnum

Is the set of values dynamic?
  → AppEntity

Do I need Spotlight indexing?
  → AppEntity + IndexedEntity

Do I need image search / Visual Intelligence?
  → AppEntity + Transferable + OpenIntent
```

### Which query type should I use?

```
Can all entities fit in memory?
  → EnumerableEntityQuery

Do I need text-based search?
  → EntityStringQuery

Do I need filtering by properties?
  → EntityPropertyQuery

Do I only need lookup by ID?
  → EntityQuery (base protocol)
```

### Should a property be @Property, @ComputedProperty, or @DeferredProperty?

```
Is the value stored on the entity struct?
  → @Property

Can the value be derived from another source (UserDefaults, model)?
  → @ComputedProperty (preferred — lower overhead)

Is the value expensive to compute (network call, heavy I/O)?
  → @DeferredProperty (async getter, only called when system requests it)
```

## Framework architecture notes

- App Intents uses **build-time metadata extraction**. Your Swift source code is read at compile time to generate an App Intents representation stored inside your app bundle. This is why certain values (titles, display representations) must be compile-time constants.
- The system reads this metadata **without running your app**. After installation, intents, entities, and shortcuts are available immediately.
- Each target in your app is processed independently. When sharing App Intent types across targets, use `AppIntentsPackage` to register each target.
- App Intents can now live in **Swift Packages and static libraries** (new in iOS 26).
- Register dependencies with `AppDependencyManager.shared.add { }` as early as possible in your app's lifecycle (typically in the `App.init()`).
