---
name: apple-native-ui
description: "Build or review native Apple interfaces, including platform controls, accessibility, state, navigation, and macOS window behavior."
license: MIT
---

# Apple Native UI

Build and review interfaces that feel native because they use the platform's interaction, accessibility, and adaptation contracts—not because they imitate a screenshot.

## Start with the target

Identify the platforms, minimum OS versions, SwiftUI versus UIKit/AppKit boundary, supported input (touch, pointer, keyboard, VoiceOver, Digital Crown, remote, eye/hand), and primary form factors. Do not apply an iPhone convention to macOS, iPad multitasking, watchOS, tvOS, or visionOS without evidence that it transfers.

Prefer system controls, semantic colors, text styles, safe-area APIs, navigation containers, and presentation APIs before custom reconstructions. Custom UI must retain the equivalent accessibility, focus, state, and cancellation behaviour.

## Fresh platform guidance

Before prescribing or implementing APIs, behaviour, design conventions, or verification that may vary by SDK or OS release, search current primary Apple sources: Apple Developer Documentation, Human Interface Guidelines, and relevant WWDC sessions. Check the project's deployment target before recommending a newer API, and distinguish current Apple guidance from repository-local compatibility constraints. The examples here express durable contracts; they are not a substitute for release-specific documentation.

## macOS workflow

When macOS is an intended target, read [references/macos-native-workflows.md](references/macos-native-workflows.md) before planning, building, porting, or reviewing a non-trivial interface. It adds a Mac-specific workflow for commands, windows and documents, selection and focus, pasteboard and drag/drop, undo, state restoration, configuration, Finder interoperability, and behaviour-led verification.

Treat a Mac version as a distinct workflow even when it shares models or views with iPadOS. A resizable iPad layout is not by itself a complete Mac app.

## State and identity

Own state at the narrowest stable boundary. A child that only displays data receives a value; a child that edits parent state receives a binding. Keep side effects out of `body` and give lists stable identities.

```swift
@Observable final class ProfileModel {
    var name = ""
    var isSaving = false
}

struct ProfileScreen: View {
    @State private var model = ProfileModel()

    var body: some View {
        Form {
            TextField("Name", text: $model.name)
            Button("Save") { save() }
                .disabled(model.name.isEmpty || model.isSaving)
        }
    }
}
```

Do not turn an injected value into `@State`, use positional indices as mutable list identity, or use `onTapGesture` where `Button`, `NavigationLink`, `Toggle`, or another native control expresses the task.

## Platform contracts

- Use `NavigationStack`/`NavigationSplitView`, sheets, alerts, confirmation dialogs, and toolbars according to the target platform. Verify back, dismiss, cancel, and focus-restoration paths.
- Use semantic colors and Dynamic Type-aware typography. Test extra-large text before adding truncation, clipping, or fixed frames.
- Treat safe areas, split view, window resizing, rotation, external keyboard, pointer, and layout direction as input to the layout—not exceptional breakpoints.
- Prefer `@Observable`, `@State`, `@Binding`, and `@Bindable` where deployment targets permit; gate version-specific APIs and provide a real fallback.
- Make animations value-driven and task-preserving under Reduce Motion. Wait for the observable end state before testing or reporting it.

## Accessibility

Accessibility is expressed through the native accessibility tree, not ARIA. Check VoiceOver labels, values, hints, traits, grouping, reading order, adjustable actions, focus movement, and disabled controls. Hide decorative imagery; label meaningful images and ambiguous icons.

```swift
Button(action: play) {
    Image(systemName: "play.fill")
}
.accessibilityLabel("Play preview")

Image(systemName: "sparkles")
    .accessibilityHidden(true)
```

Read [references/apple-verification.md](references/apple-verification.md) for simulator, device, XCUITest, accessibility, and form-factor evidence. Read it before making native verification claims.

## Review output

Anchor findings to a source path or an observed target/device. State whether evidence is source-only or rendered. Name the affected platform and input method; an iOS finding is not automatically a macOS finding.

## Prefer / reject

| Prefer | Reject |
| --- | --- |
| System control with intentional styling | Clickable stacks or images standing in for controls |
| Semantic fonts, colors, and adaptive layout | Fixed dimensions that break at larger text or smaller windows |
| Stable IDs and explicit state ownership | Index identity and effects hidden in `body` |
| Platform-specific verification | Treating a simulator screenshot as proof for every target |
| Version gates with useful fallbacks | Unconditional new APIs that silently drop supported users |
