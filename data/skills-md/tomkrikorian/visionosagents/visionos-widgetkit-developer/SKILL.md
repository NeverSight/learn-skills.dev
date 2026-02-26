---
name: visionos-widgetkit-developer
description: Build and debug WidgetKit widgets for Apple Vision Pro (visionOS), including mounting styles (elevated/recessed), textures (glass/paper), proximity-aware layouts via LevelOfDetail, and timeline update troubleshooting.
---

# visionOS WidgetKit Developer

## Description and Goals

This skill helps you design, implement, and troubleshoot **WidgetKit widgets for Apple Vision Pro**. On visionOS, widgets are spatial objects that people pin to real surfaces, and they can be viewed from different distances. visionOS adds widget-specific capabilities like **mounting styles** (elevated vs recessed), **textures** (glass vs paper), and **proximity-aware layouts** via `LevelOfDetail`.

### Goals

- Help you choose the right widget strategy for Vision Pro (visionOS app vs compatibility widgets).
- Implement visionOS-specific widget presentation: mounting styles, textures, and families.
- Ensure glanceability at distance using `LevelOfDetail`-driven layouts.
- Provide a practical debugging checklist for timelines, refreshes, and rendering issues.

## What This Skill Should Do

When you ask to build or debug a Vision Pro widget, this skill should:

1. **Clarify scope and platform**: Is this a visionOS app widget, or an iOS/iPadOS widget running on Vision Pro in compatibility mode? Which widget families must be supported?
2. **Choose layout strategy**: Define a “default” layout (close) and a “simplified” layout (far) using `@Environment(\.levelOfDetail)`.
3. **Configure visionOS widget presentation**:
   - Set `supportedMountingStyles` (elevated/recessed) appropriately.
   - Choose `widgetTexture` (glass/paper) where available/appropriate.
4. **Validate legibility and content density**: Ensure the simplified layout remains readable from across the room.
5. **Handle updates**: Implement a sound timeline strategy and define when/how the widget reloads.
6. **Debug and iterate**: Provide concrete checks for common failure modes (missing families, bad Info.plist, broken layouts in recessed mode, stale timelines).

Load the most relevant reference file(s) below based on the specific issue.

## Information About the Skill

### Core Concepts

#### Widgets in visionOS are spatial objects

On Vision Pro, widgets are pinned to horizontal or vertical surfaces and behave like physical objects in the room. This changes how you design for legibility, contrast, and layout compared to 2D-only platforms.

#### Mounting styles: elevated vs recessed

On vertical surfaces, a widget can appear **recessed** (embedded into a wall) or **elevated** (sitting on top of the surface). Some widget designs only make sense in one mode.

#### Textures: glass vs paper

For widgets your visionOS app offers, you can typically choose a **glass** or **paper** texture. This affects background treatment, contrast, and how “poster-like” your widget feels.

#### Proximity awareness with `LevelOfDetail`

visionOS can change a widget’s `LevelOfDetail` based on **user proximity**. Treat this as a first-class requirement:

- `.default`: more information, smaller typography, richer layout.
- `.simplified`: less information, larger typography, fewer elements, more contrast.

#### Family support differences for extra-large widgets

visionOS supports system widget families including extra-large, but the correct family to declare depends on whether your widget is part of a visionOS app vs a compatible iOS/iPadOS app.

### Reference Tables

| Reference | When to Use |
|---|---|
| [`REFERENCE.md`](references/REFERENCE.md) | Overview, decision points, and a quick checklist for Vision Pro widgets. |
| [`mounting-styles.md`](references/mounting-styles.md) | When deciding elevated vs recessed support and avoiding layout breakage. |
| [`textures-and-rendering.md`](references/textures-and-rendering.md) | When choosing glass vs paper, and ensuring legibility in different render modes. |
| [`proximity-levelofdetail.md`](references/proximity-levelofdetail.md) | When implementing near/far layouts using `LevelOfDetail`. |
| [`debugging-and-updates.md`](references/debugging-and-updates.md) | When widgets don’t refresh, don’t appear, or appear stale/broken. |

### Implementation Patterns

#### Configure a visionOS widget with mounting + texture

```swift
import SwiftUI
import WidgetKit

struct MyVisionOSWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "MyVisionOSWidget", provider: Provider()) { entry in
            MyWidgetView(entry: entry)
        }
        .configurationDisplayName("My Widget")
        .description("Glanceable info in your space.")
        .supportedMountingStyles([.elevated, .recessed])
        .widgetTexture(.glass)
        // Choose families intentionally; see references for Vision Pro rules.
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}
```

#### Proximity-aware widget layout

```swift
import SwiftUI
import WidgetKit

struct MyWidgetView: View {
    @Environment(\.levelOfDetail) private var levelOfDetail
    let entry: Provider.Entry

    var body: some View {
        if levelOfDetail == .simplified {
            SimplifiedView(entry: entry)
        } else {
            DetailedView(entry: entry)
        }
    }
}
```

### Pitfalls and Checks

- Don’t ship a single dense layout: always consider `.simplified` for distance readability.
- Don’t assume recessed mode “just works”: test layouts and backgrounds in recessed mounting.
- Avoid tiny typography and low-contrast UI; pinned widgets are often viewed from far away.
- Don’t forget to include the right widget families (especially extra-large differences).
- If timelines seem stale, confirm your timeline policy and reload strategy.

