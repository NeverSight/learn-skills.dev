---
name: foundation-models
description: Apple's FoundationModels framework for on-device LLM integration in apps. Covers SystemLanguageModel availability checking, LanguageModelSession creation with instructions, prompt engineering, @Generable macro for structured output with @Guide constraints, snapshot streaming with PartiallyGenerated types, Tool protocol for custom tool calling, GenerationOptions (temperature), context window limits (4096 tokens), and error handling. Use when integrating Apple Intelligence text generation, building AI-powered features using on-device models, or implementing structured data generation. Critical note - always use response.content (NOT response.output) when accessing generated values.
---

# FoundationModels — On-Device LLM

Apple's framework for on-device generative AI. No cloud, no API keys, full privacy.

## Critical Constraints

- ❌ DO NOT use `response.output` → ✅ Use `response.content` to access generated values
- ❌ DO NOT skip availability check → ✅ Always check `SystemLanguageModel.default.availability` first
- ❌ DO NOT exceed 4,096 tokens per session → ✅ Break large tasks into multiple sessions
- ❌ DO NOT send concurrent requests on same session → ✅ Check `session.isResponding` first
- ❌ DO NOT confuse with OpenAI/Anthropic APIs → ✅ This is Apple's native framework, different API surface

## Availability Check (Required)
```swift
import FoundationModels

let model = SystemLanguageModel.default

switch model.availability {
case .available:
    // Show AI features
case .unavailable(.deviceNotEligible):
    // Device doesn't support Apple Intelligence
case .unavailable(.appleIntelligenceNotEnabled):
    // User needs to enable in Settings
case .unavailable(.modelNotReady):
    // Model downloading or not ready
case .unavailable(let other):
    // Other reason
}
```

## Basic Session & Response
```swift
let session = LanguageModelSession()
let response = try await session.respond(to: "What's a good month to visit Paris?")
print(response.content)  // ← ALWAYS .content, never .output
```

## Session with Instructions
```swift
let instructions = """
    You are a cooking assistant.
    Provide recipe suggestions based on ingredients.
    Keep suggestions brief and practical.
    """
let session = LanguageModelSession(instructions: instructions)
let response = try await session.respond(to: "I have chicken, rice, and broccoli")
print(response.content)
```

## Guided Generation (@Generable)

Receive structured Swift data instead of raw strings.

```swift
@Generable(description: "Profile information about a cat")
struct CatProfile {
    var name: String

    @Guide(description: "The age of the cat", .range(0...20))
    var age: Int

    @Guide(description: "One sentence personality profile")
    var profile: String
}

let session = LanguageModelSession()
let response = try await session.respond(
    to: "Generate a cute rescue cat",
    generating: CatProfile.self
)
print(response.content.name)     // ← .content, not .output
print(response.content.age)
print(response.content.profile)
```

### Collection with Count Constraint
```swift
@Generable
struct CookbookSuggestions {
    @Guide(description: "Cookbook Suggestions", .count(3))
    var suggestions: [String]
}

let response = try await session.respond(
    to: "What's a good name for a cooking app?",
    generating: CookbookSuggestions.self
)
print(response.content.suggestions)
```

## Snapshot Streaming

Stream partially-generated structured output. `@Generable` produces a `PartiallyGenerated` type with optional properties.

```swift
@Generable
struct TripIdeas {
    @Guide(description: "Ideas for upcoming trips")
    var ideas: [String]
}

let session = LanguageModelSession()
let stream = session.streamResponse(
    to: "What are some exciting trip ideas?",
    generating: TripIdeas.self
)

for try await partial in stream {
    // partial.ideas is [String]? — fills in as tokens generate
    print(partial)
}
```

### SwiftUI Integration with Streaming
```swift
struct StreamingView: View {
    @State private var partial: TripIdeas.PartiallyGenerated?

    var body: some View {
        VStack {
            if let ideas = partial?.ideas {
                ForEach(ideas, id: \.self) { Text($0) }
            }
        }
        .task { await streamIdeas() }
    }

    func streamIdeas() async {
        let session = LanguageModelSession()
        let stream = session.streamResponse(
            to: "Trip ideas for 2025",
            generating: TripIdeas.self
        )
        do {
            for try await snapshot in stream {
                partial = snapshot
            }
        } catch { print(error) }
    }
}
```

## Tool Calling
```swift
struct RecipeSearchTool: Tool {
    struct Arguments: Codable {
        var searchTerm: String
        var numberOfResults: Int
    }

    func call(arguments: Arguments) async throws -> ToolOutput {
        let recipes = await searchRecipes(term: arguments.searchTerm, limit: arguments.numberOfResults)
        return .string(recipes.map { "- \($0.name): \($0.description)" }.joined(separator: "\n"))
    }
}

let session = LanguageModelSession(tools: [RecipeSearchTool()])
let response = try await session.respond(to: "Find me some pasta recipes")

// Error handling
do {
    let answer = try await session.respond("Find a recipe for tomato soup.")
} catch let error as LanguageModelSession.ToolCallError {
    print(error.tool.name)
    print(error.underlyingError)
}
```

## Generation Options
```swift
let options = GenerationOptions(temperature: 2.0)  // Higher = more creative
let response = try await session.respond(to: prompt, options: options)
```

## Session Transcript
```swift
let transcript = session.transcript  // View model actions during session
```

## Context Limits
- 4,096 tokens per session (~12K-16K English characters)
- Instructions + prompts + outputs all count
- For large data: break into chunks across multiple sessions
- Error on overflow: `LanguageModelSession.GenerationError.exceededContextWindowSize`

## Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| `response.output` | `response.content` — always use content |
| Skipping availability check | Always check `SystemLanguageModel.default.availability` |
| Sending request while session is busy | Check `session.isResponding` first |
| Expecting cloud model quality | On-device model is smaller; keep prompts focused and simple |
| Trying to use on Simulator | Requires Apple Silicon device with Apple Intelligence enabled |

## References

- [Generating content with Foundation Models](https://developer.apple.com/documentation/FoundationModels/generating-content-and-performing-tasks-with-foundation-models)
- [Guided generation](https://developer.apple.com/documentation/FoundationModels/generating-swift-data-structures-with-guided-generation)
- [Tool calling](https://developer.apple.com/documentation/FoundationModels/expanding-generation-with-tool-calling)
- [WWDC 2025: Meet the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/)
