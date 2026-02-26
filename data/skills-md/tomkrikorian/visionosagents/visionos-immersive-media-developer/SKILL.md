---
name: visionos-immersive-media-developer
description: Implement immersive and spatial video experiences on Apple Vision Pro (visionOS), including RealityKit VideoPlayerComponent setup, portal/progressive/full immersive viewing modes, transitions and events, comfort mitigation, and Apple Immersive Video authoring workflows.
---

# visionOS Immersive Media Developer

## Description and Goals

This skill provides a practical playbook for building **immersive and spatial media** experiences on **Apple Vision Pro**. It focuses on RealityKit’s `VideoPlayerComponent` (with `AVPlayer`) for video playback that can move between **window/portal** playback and **immersive** playback, plus the event and comfort toolset that helps you ship a comfortable, accessible experience.

It also outlines how Apple’s **ImmersiveMediaSupport** framework fits into authoring and packaging **Apple Immersive Video** content.

### Goals

- Help you choose the right playback surface (2D window, portal, progressive immersive, full immersive).
- Implement RealityKit video playback using `VideoPlayerComponent` correctly.
- Handle immersive viewing mode transitions safely (including scene transitions when needed).
- Respond to video playback events and comfort mitigation events on visionOS 26+.
- Provide a foundation for Apple Immersive Video authoring workflows where relevant.

## What This Skill Should Do

When asked to add immersive/spatial video to a visionOS app, this skill should:

1. **Clarify the media experience**
   - Is this a “video on a surface” experience, a portal, or full immersive playback?
   - Is the content mono, stereo, spatial video, or immersive media?
   - Do you need passthrough tinting, captions/subtitles, or multi-user playback sync?
2. **Pick a playback architecture**
   - RealityKit `VideoPlayerComponent` + `AVPlayer` for video surfaces and immersive playback modes.
   - Escalate to CompositorServices only for custom engines or bespoke full-space rendering.
3. **Implement playback + UI**
   - Create a video entity, attach `VideoPlayerComponent`, and manage UI affordances.
   - Handle immersive-viewing mode transitions (portal ↔ immersive space).
4. **Handle events and comfort**
   - Subscribe to `VideoPlayerEvents` for viewing mode changes, transitions, and comfort mitigation.
5. **Validate comfort and accessibility**
   - Provide clear exit paths, reduce motion where appropriate, and support captions.

Load the appropriate reference file from the tables below for detailed usage, code examples, and best practices.

## Information About the Skill

### Core Concepts

#### `VideoPlayerComponent` is the backbone

RealityKit’s `VideoPlayerComponent` is a first-class video playback component powered by `AVPlayer`. It’s designed to support playback controls and visionOS-specific behaviors like passthrough tinting and immersive viewing modes.

#### Immersive viewing modes

For immersive media types, visionOS supports multiple immersive viewing modes:

- **Portal**: immersive media rendered as a portal window matching the containing entity transform.
- **Progressive**: partial-to-full coverage controlled via the Digital Crown (not used for Spatial Video).
- **Full**: immersive media fills the field of view.

You should treat switching between these modes as a **scene orchestration** problem as well as a component configuration problem.

#### Comfort mitigation (visionOS 26+)

visionOS can detect video comfort violations and trigger mitigation. Your app should subscribe to the event and respond:

- pause playback
- reduce immersion
- continue (play) depending on what the system reports and what UX you want

#### Authoring / packaging Apple Immersive Video

The **ImmersiveMediaSupport** framework provides tools and a workflow for authoring and packaging Apple Immersive Video content (typically as part of a content pipeline, not day-to-day app UI).

### Reference Tables

| Reference | When to Use |
|---|---|
| [`REFERENCE.md`](references/REFERENCE.md) | Decision tree: window vs portal vs progressive vs full immersive playback. |
| [`videoplayercomponent-basics.md`](references/videoplayercomponent-basics.md) | When you need to set up `VideoPlayerComponent` + `AVPlayer` correctly. |
| [`immersive-viewing-modes.md`](references/immersive-viewing-modes.md) | When implementing portal/progressive/full modes and related scene transitions. |
| [`events-and-transitions.md`](references/events-and-transitions.md) | When responding to `VideoPlayerEvents` and managing UI during transitions. |
| [`comfort-mitigation.md`](references/comfort-mitigation.md) | When handling comfort violations and mitigation strategies on visionOS 26+. |
| [`apple-immersive-video-authoring.md`](references/apple-immersive-video-authoring.md) | When you need Apple Immersive Video authoring/packaging references. |

### Implementation Patterns

#### Basic VideoPlayerComponent setup

```swift
import AVFoundation
import RealityKit

let videoEntity = Entity()
let player = AVPlayer(url: url)

var video = VideoPlayerComponent(avPlayer: player)
video.isPassthroughTintingEnabled = true

videoEntity.components.set(video)
player.play()
```

#### Subscribe to immersive viewing mode transitions

```swift
import RealityKit

var subscription: EventSubscription?

subscription = content.subscribe(to: VideoPlayerEvents.ImmersiveViewingModeWillTransition.self) { event in
    // Disable non-essential UI while transitioning.
}
```

#### Subscribe to comfort mitigation (visionOS 26+)

```swift
subscription = content.subscribe(to: VideoPlayerEvents.VideoComfortMitigationDidOccur.self) { event in
    switch event.comfortMitigation {
    case .pause:
        // Update UI to indicate playback paused.
        break
    case .reduceImmersion:
        // Offer a UI path back to portal / lower immersion.
        break
    case .play:
        break
    }
}
```

### Pitfalls and Checks

- Don’t treat immersive mode switching as “just a property change”; you may need to transition between window scenes and immersive spaces deliberately.
- Make sure you have an obvious “exit” affordance from immersive playback.
- Always test Spatial Video vs immersive media behavior (they differ; progressive isn’t used for Spatial Video).
- Subscribe to transitions/events early; many UX issues appear only during mode changes.
- For visionOS 26+, handle comfort mitigation events and align your UI with the system’s mitigation choice.

