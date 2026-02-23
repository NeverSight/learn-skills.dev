---
name: app-intent-driven-development
description: WHEN designing features App Intent-first so Siri/Shortcuts, widgets, and SwiftUI share logic; NOT UI-first; reuse intents across app.
---

# App Intent–First Driven Development

Design features as App Intents first, then reuse those intents across Shortcuts, widgets, and SwiftUI views so automation and UI stay in lockstep.

## Core Ideas

- **Entities first**: model the data users act on (events, categories, records) as `AppEntity` so intents, widgets, and the app share one source of truth.
- **Intent-first feature**: build the App Intent + entity query before UI; SwiftUI screens call those intents instead of duplicating service code.
- **Single action, single intent**: keep intents focused; avoid mega-intents that are hard to compose in Shortcuts.
- **Predictable UI**: supply `DisplayRepresentation`, `typeDisplayRepresentation`, and icons so Siri/Shortcuts can render rich cards without opening the app.
- **Fast queries**: `EntityQuery` must be quick and cancellable; avoid blocking the main actor.
- **Reuse business logic**: intents call the same services your views use; do not fork logic inside the intent.

## Minimal Entity Blueprint

```swift
import AppIntents

struct TaskEntity: AppEntity, Identifiable {
    static let typeDisplayRepresentation = TypeDisplayRepresentation(name: "Task")
    static let defaultQuery = TaskQuery()

    let id: UUID
    let title: String
    let isComplete: Bool

    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(
            title: title,
            subtitle: isComplete ? "Completed" : "Open",
            image: .init(systemName: isComplete ? "checkmark.circle.fill" : "circle")
        )
    }
}

struct TaskQuery: EntityQuery {
    func entities(for identifiers: [UUID]) async throws -> [TaskEntity] {
        try await TaskStore.shared.fetch(ids: identifiers) // fast path
    }

    func suggestedEntities() async throws -> [TaskEntity] {
        try await TaskStore.shared.fetchRecent()
    }
}
```

**Key points:** stable identifier, meaningful representation, and fast queries that avoid launching heavy app flows.

## Intent Pattern

```swift
import AppIntents

struct CompleteTaskIntent: AppIntent {
    static let title: LocalizedStringResource = "Complete Task"
    static let description = IntentDescription("Marks a task as done and returns the updated item.")

    @Parameter(title: "Task", requestValueDialog: "Which task should I complete?")
    var task: TaskEntity

    // Used so we can call the intent from SwiftUI using .perform()
    init(task: TaskEntity) { self.task = task }

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<TaskEntity> {
        let updated = try await TaskStore.shared.complete(task.id)
        return .result(value: updated)
    }

    static var parameterSummary: some ParameterSummary {
        Summary("Complete \(\.$task)")
    }
}
```

- **Parameters**: keep them few; provide `requestValueDialog` to make Siri prompts natural.
- **Results**: return entities when possible; system surfaces render them nicely.
- **Isolation**: mark with `@MainActor` only if you must touch UI-bound objects; otherwise keep work off the main actor.

## Reusing Intents in SwiftUI

- Prefer calling intents from UI so automation and in-app flows share one path.
- Use `AppIntentButton` to invoke intents directly from views.
- Translate entity selections into view state so widgets/Shortcuts and in-app pickers present the same objects.

```swift
import AppIntents
import SwiftUI

struct EventRow: View {
    let event: EventEntity

    var body: some View {
        HStack {
            Text(event.name)
            Spacer()
            AppIntentButton(intent: UndoLastEventOccuranceIntent(event: event)) {
                Label("Undo", systemImage: "arrow.uturn.backward")
            }
        }
    }
}
```

- For more control, invoke intents imperatively with `perform` (e.g., to show progress or handle errors):

```swift
import AppIntents
import SwiftUI

struct EventRow: View {
    @Environment(\.intentExecutor) private var executor
    @State private var isWorking = false
    @State private var error: Error?

    let event: EventEntity

    var body: some View {
        HStack {
            Text(event.name)
            Spacer()
            Button {
                Task {
                    isWorking = true
                    defer { isWorking = false }
                    do {
                        try await executor.perform(UndoLastEventOccuranceIntent(event: event))
                    } catch {
                        self.error = error
                    }
                }
            } label: {
                if isWorking {
                    ProgressView()
                } else {
                    Label("Undo", systemImage: "arrow.uturn.backward")
                }
            }
        }
        .alert("Undo failed", isPresented: .init(
            get: { error != nil },
            set: { if !$0 { error = nil } }
        )) {
            Button("OK", role: .cancel) { error = nil }
        } message: {
            Text(error?.localizedDescription ?? "Unknown error")
        }
    }
}
```

- Keep the intent signature identical between Shortcuts and SwiftUI usage.
- Avoid reimplementing service calls in views; route through the intent to keep analytics, validation, and side effects consistent.

## Development Flow

1. Model the domain type as `AppEntity` with `DisplayRepresentation` and `EntityQuery`.
2. Implement a focused `AppIntent` that calls shared services; avoid duplicate data access layers inside the intent.
3. Add previews in Shortcuts or the App Intents preview panel; ensure suggested entities show immediately.
4. Expose the same entity in widgets/Live Activities to keep automation and UI consistent.
5. Localize strings early (`LocalizedStringResource`) to keep Siri responses natural in all supported languages.

## Quick Checklist

- [ ] Entity has stable `id`, `typeDisplayRepresentation`, and rich `displayRepresentation`.
- [ ] Queries are fast, cancellable, and return suggestions without opening the app.
- [ ] Intent reuses shared domain services; no duplicated business logic.
- [ ] Parameters are minimal and well phrased with `requestValueDialog`.
- [ ] Results return entities when possible for better system rendering.
- [ ] Strings are localized; tests cover queries and perform paths.
