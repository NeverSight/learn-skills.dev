---
name: foundation-models
description: iOS 26 FoundationModels framework guide for on-device LLM integration. Covers model availability, guided generation, streaming, and tool calling.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# FoundationModels Framework (iOS 26+)

On-device LLM framework. Integrates AI capabilities into your app while preserving privacy through Apple Intelligence.

## Model Availability Check

Always check model availability before use.

```swift
import FoundationModels

private var model = SystemLanguageModel.default

func checkAvailability() {
    switch model.availability {
    case .available:
        // Show AI feature UI
        showAIFeatures()

    case .unavailable(.deviceNotEligible):
        // Device not supported (requires A17 Pro or later)
        showFallbackUI()

    case .unavailable(.appleIntelligenceNotEnabled):
        // Apple Intelligence is disabled
        showEnableIntelligencePrompt()

    case .unavailable(.modelNotReady):
        // Model is downloading or not yet ready
        showDownloadingUI()

    @unknown default:
        showFallbackUI()
    }
}
```

## Basic Text Generation

```swift
import FoundationModels

let session = LanguageModelSession()

// Simple text generation
let response = try await session.respond(to: "Tell me a fun fact about cats")
print(response.content)  // Access via .content!
```

## Guided Generation (Structured Output)

Use the `@Generable` macro to enforce structured output.

```swift
@Generable(description: "Cat profile information")
struct CatProfile {
    var name: String

    @Guide(description: "Cat age (0-20 years)", .range(0...20))
    var age: Int

    @Guide(description: "Describe personality in one sentence")
    var personality: String
}

// Generate a structured response
let response = try await session.respond(
    to: "Generate a cute rescue cat profile",
    generating: CatProfile.self
)

let profile = response.content  // CatProfile type
print(profile.name)        // "Whiskers"
print(profile.age)         // 3
print(profile.personality) // "Curious and affectionate, loves following people around"
```

### @Generable Rules

```swift
// Supported types
@Generable
struct Recipe {
    var title: String           // String
    var cookingTime: Int        // Int
    var isVegetarian: Bool      // Bool
    var rating: Double          // Double

    @Guide(.range(1...10))
    var difficulty: Int         // Range constraint

    @Guide(.options(["Korean", "Chinese", "Western", "Japanese"]))
    var category: String        // Option constraint
}

// Nested Generable
@Generable
struct Ingredient {
    var name: String
    var amount: String
}

@Generable
struct RecipeWithIngredients {
    var title: String
    var ingredients: [Ingredient]  // Nested array
}
```

## Snapshot Streaming

Display partial generation results in real time with streaming.

```swift
@Generable
struct TripIdeas {
    var destination: String
    var activities: [String]
    var estimatedBudget: Int
}

let stream = session.streamResponse(
    to: "Recommend a weekend trip near the city",
    generating: TripIdeas.self
)

for try await partial in stream {
    // partial: Partial generation type (all properties are optional)
    if let destination = partial.destination {
        updateDestinationUI(destination)
    }
    if let activities = partial.activities {
        updateActivitiesUI(activities)
    }
}
```

### SwiftUI Streaming

```swift
struct AIGeneratorView: View {
    @State private var result: TripIdeas?
    @State private var isGenerating = false

    var body: some View {
        VStack {
            if let result {
                Text(result.destination)
                ForEach(result.activities, id: \.self) { activity in
                    Text(activity)
                }
            }

            Button("Generate") {
                Task {
                    isGenerating = true
                    defer { isGenerating = false }

                    let stream = session.streamResponse(
                        to: "Recommend a trip",
                        generating: TripIdeas.self
                    )

                    for try await partial in stream {
                        // UI updates automatically (@Observable or @State)
                        if let dest = partial.destination {
                            result = TripIdeas(
                                destination: dest,
                                activities: partial.activities ?? [],
                                estimatedBudget: partial.estimatedBudget ?? 0
                            )
                        }
                    }
                }
            }
            .disabled(isGenerating)
        }
    }
}
```

## Tool Calling

Enable the model to call external functions.

```swift
@Tool(description: "Fetches current weather information")
func getWeather(city: String) async throws -> String {
    let weather = try await weatherService.fetch(city: city)
    return "\(city): \(weather.temperature)°C, \(weather.condition)"
}

let session = LanguageModelSession(tools: [getWeather])
let response = try await session.respond(to: "What's the weather like in Seoul?")
// The model calls the getWeather tool and responds based on the result
```

## Session Management

```swift
// Manage conversation sessions
let session = LanguageModelSession()

// First message
let response1 = try await session.respond(to: "I like cats")

// Second message (previous context is retained)
let response2 = try await session.respond(to: "Explain why")

// Reset the session
session.reset()
```

## Error Handling

```swift
do {
    let response = try await session.respond(to: prompt)
    handleResponse(response.content)
} catch let error as LanguageModelSession.GenerationError {
    switch error {
    case .modelNotAvailable:
        showModelUnavailable()
    case .contentFiltered:
        showContentFilteredMessage()
    case .tokenLimitExceeded:
        showTruncationWarning()
    @unknown default:
        showGenericError()
    }
} catch {
    showGenericError()
}
```

## Best Practices

### DO:
- Always check model availability first
- Use `@Generable` for structured output (more reliable than free text)
- Use streaming to minimize user wait time
- Handle errors properly (unsupported device, content filter, etc.)
- Emphasize on-device processing in your UI to highlight privacy

### DON'T:
- Do not show AI features without checking model availability
- Do not include sensitive personal information in prompts
- Do not blindly trust model responses (hallucinations are possible)
- Do not rely on generating large amounts of text (on-device model has limitations)
- Do not start long generations without streaming (degrades user experience)

## Availability

```swift
if #available(iOS 26.0, *) {
    // Use FoundationModels
} else {
    // Fall back to server-side AI API or disable the feature
}
```

---

> FoundationModels is a core AI framework in iOS 26.
> It enables structured AI capabilities while preserving privacy through on-device processing.
> Always refer to the Apple Developer Documentation for the latest API details.
