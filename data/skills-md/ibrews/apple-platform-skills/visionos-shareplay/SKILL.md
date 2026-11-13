---
name: visionos-shareplay
description: |
  SharePlay and GroupActivities development for visionOS and iOS. Use when implementing collaborative experiences, synchronizing state across participants, managing GroupSession lifecycle, or building shared immersive spaces on Apple platforms.
---

# visionOS SharePlay Development

## GroupActivities Essentials

Core types: `GroupActivity` (your activity struct), `GroupSession` (the live session), `GroupSessionMessenger` (send/receive messages), `AsyncStream` (observe session and message events).

## Activity Type Definition

```swift
struct WatchTogetherActivity: GroupActivity {
    static let activityIdentifier = "com.example.app.watch-together"
    var metadata: GroupActivityMetadata {
        var m = GroupActivityMetadata()
        m.title = "Watch Together"
        m.type = .watchTogether
        m.fallbackURL = URL(string: "https://example.com/watch")
        return m
    }
}
```

## Session Lifecycle

```swift
// Activate (host)
let activity = WatchTogetherActivity()
switch await activity.prepareForActivation() {
case .activationPreferred:
    try await activity.activate()
case .activationDisabled:
    // Fallback — open locally
default: break
}

// Observe incoming sessions (all participants including host)
for await session in WatchTogetherActivity.sessions() {
    configureSession(session)
}

func configureSession(_ session: GroupSession<WatchTogetherActivity>) {
    // CRITICAL: always call join() or the session stays in .waiting
    session.join()
    // store session reference — don't let it deallocate
    self.groupSession = session

    Task {
        for await state in session.$state.values {
            if case .invalidated(let error) = state { handleEnd(error) }
        }
    }
}
```

**Common pitfall:** forgetting `session.join()` — session stays `.waiting` forever.

## Synchronizing State with GroupSessionMessenger

```swift
let messenger = GroupSessionMessenger(session: session)

// Send
struct MoveMessage: Codable { let position: SIMD3<Float> }
try await messenger.send(MoveMessage(position: pos))

// Receive
Task {
    for await (message, context) in messenger.messages(of: MoveMessage.self) {
        apply(message, from: context.source)
    }
}
```

## visionOS-Specific

**Spatial Personas** — enabled automatically in FaceTime when app has GroupActivities entitlement. Access via `session.participants`.

**ImmersiveSpace in SharePlay:**
```swift
// Open immersive space when session becomes active
.task {
    for await session in MyActivity.sessions() {
        session.join()
        await openImmersiveSpace(id: "SharedSpace")
    }
}
```

**Windowed vs Volumetric:** Windowed windows are shared/mirrored automatically. Volumetric windows are independent per device — use messenger to keep them in sync manually.

## Required Entitlements & Info.plist

In your `.entitlements` file:
```xml
<key>com.apple.developer.group-activities</key>
<true/>
```

No special entitlement request needed — available to all Apple Developer accounts.

## Simulator Limitations

GroupActivities **does not work in Simulator**. Testing requires:
- Two physical devices (iPhone/iPad/Apple Vision Pro)
- An active FaceTime call between them
- Or: use `GroupActivitySharingController` to test the activation UI in isolation

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Session stays `.waiting` | Always call `session.join()` |
| Session deallocates | Store strong reference to `GroupSession` |
| Messages not received | Check `messenger` is retained too |
| Activation does nothing | Check `prepareForActivation()` result first |
| visionOS persona missing | Requires FaceTime call, not just same-network |
