---
name: progressive-blur-header-swiftui
description: Drop-in SwiftUI sticky header component with progressive blur effect matching Apple Music, Photos, and App Store styles.
triggers:
  - add progressive blur header to my SwiftUI app
  - sticky header with blur effect in SwiftUI
  - how to use ProgressiveBlurHeader
  - apple music style blur header swiftui
  - progressive blur sticky navigation bar
  - StickyBlurHeader component setup
  - scroll view header blur effect swift
  - variable blur header swiftui
---

# ProgressiveBlurHeader SwiftUI Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A drop-in SwiftUI package for sticky headers with progressive (variable-radius) blur — replicating the Apple Music, Photos, and App Store style where content scrolls underneath the header with increasing blur and tint. No clipping, no hard edges.

## Installation

### Swift Package Manager (Xcode)

**File → Add Package Dependencies** → paste:
```
https://github.com/dominikmartn/ProgressiveBlurHeader
```
Select branch: `main`

### Package.swift

```swift
dependencies: [
    .package(url: "https://github.com/dominikmartn/ProgressiveBlurHeader", branch: "main"),
]
```

Then add to your target:
```swift
.target(
    name: "YourApp",
    dependencies: ["ProgressiveBlurHeader"]
)
```

**Requirements:** iOS 16+, Swift 5.9+

---

## Core API

### `StickyBlurHeader`

The primary component. Takes two `ViewBuilder` closures: `header` and `content`.

```swift
StickyBlurHeader(
    maxBlurRadius: Double,     // Default: 5
    fadeExtension: CGFloat,    // Default: 64
    tintOpacityTop: Double,    // Default: 0.7
    tintOpacityMiddle: Double  // Default: 0.5
) {
    // header view (NO opaque background)
} content: {
    // scrollable content
}
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `maxBlurRadius` | `Double` | `5` | Max blur at the top edge. 5 = subtle, 10 = moderate, 20 = strong |
| `fadeExtension` | `CGFloat` | `64` | Points below the header the blur extends |
| `tintOpacityTop` | `Double` | `0.7` | Tint behind Dynamic Island / status bar |
| `tintOpacityMiddle` | `Double` | `0.5` | Tint at the header's vertical center |

The tint color adapts automatically to light/dark mode.

---

## Basic Usage

```swift
import SwiftUI
import ProgressiveBlurHeader

struct ContentView: View {
    let items = (1...50).map { "Item \($0)" }

    var body: some View {
        StickyBlurHeader {
            // Header — NO opaque background
            HStack {
                Button("Back") { }
                Spacer()
                Text("Library").font(.headline)
                Spacer()
                Button("Settings") { }
            }
            .padding()
        } content: {
            ForEach(items, id: \.self) { item in
                Text(item)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color(.secondarySystemBackground))
                    .cornerRadius(8)
                    .padding(.horizontal)
            }
        }
        .background(Color(.systemBackground))
    }
}
```

---

## Common Patterns

### Navigation-Style Header with Back Button

```swift
import SwiftUI
import ProgressiveBlurHeader

struct AlbumDetailView: View {
    let albumTitle: String
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        StickyBlurHeader(
            maxBlurRadius: 8,
            fadeExtension: 80,
            tintOpacityTop: 0.75,
            tintOpacityMiddle: 0.55
        ) {
            HStack {
                Button {
                    dismiss()
                } label: {
                    Image(systemName: "chevron.left")
                        .fontWeight(.semibold)
                }
                Spacer()
                Text(albumTitle)
                    .font(.headline)
                    .lineLimit(1)
                Spacer()
                Button {
                    // action
                } label: {
                    Image(systemName: "ellipsis.circle")
                }
            }
            .padding(.horizontal)
            .padding(.vertical, 12)
        } content: {
            LazyVStack(spacing: 0) {
                ForEach(0..<30) { index in
                    SongRow(index: index)
                    Divider().padding(.leading)
                }
            }
        }
        .background(Color(.systemBackground))
    }
}
```

### Subtle Blur (Apple Photos Style)

```swift
StickyBlurHeader(
    maxBlurRadius: 5,
    fadeExtension: 56,
    tintOpacityTop: 0.6,
    tintOpacityMiddle: 0.4
) {
    HStack {
        Text("Photos")
            .font(.largeTitle)
            .fontWeight(.bold)
        Spacer()
        Button {
            // action
        } label: {
            Image(systemName: "plus")
        }
    }
    .padding(.horizontal)
    .padding(.top, 8)
    .padding(.bottom, 12)
} content: {
    LazyVGrid(columns: [GridItem(.adaptive(minimum: 100))], spacing: 2) {
        ForEach(photos) { photo in
            PhotoThumbnail(photo: photo)
        }
    }
    .padding(2)
}
.background(Color(.systemBackground))
```

### Strong Blur (App Store Style)

```swift
StickyBlurHeader(
    maxBlurRadius: 12,
    fadeExtension: 72,
    tintOpacityTop: 0.85,
    tintOpacityMiddle: 0.6
) {
    VStack(spacing: 4) {
        HStack {
            Text("Today")
                .font(.largeTitle)
                .fontWeight(.bold)
            Spacer()
            Button {
                // profile action
            } label: {
                Image(systemName: "person.crop.circle.fill")
                    .font(.title2)
            }
        }
        HStack {
            Text(Date(), style: .date)
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .textCase(.uppercase)
            Spacer()
        }
    }
    .padding(.horizontal)
    .padding(.vertical, 12)
} content: {
    LazyVStack(spacing: 16) {
        ForEach(featuredApps) { app in
            AppCard(app: app)
        }
    }
    .padding()
}
.background(Color(.systemBackground))
```

### Dynamic Header (Height Changes)

Header height is measured automatically via `GeometryReader` + `PreferenceKey` — no manual sizing needed:

```swift
StickyBlurHeader {
    VStack(alignment: .leading, spacing: 4) {
        Text("Title").font(.headline)
        if showsSubtitle {
            Text("Subtitle").font(.subheadline).foregroundStyle(.secondary)
        }
    }
    .padding()
    // Header auto-adjusts when showsSubtitle toggles
} content: {
    contentList
}
.background(Color(.systemBackground))
```

---

## Architecture

The component uses a three-layer `ZStack`:

| Layer | Component | Purpose |
|-------|-----------|---------|
| Back | `ScrollView` | Content scrolls freely, never clipped |
| Middle | `VariableBlurView` + gradient | Progressive blur + adaptive tint |
| Front | Your header view | Floats above blur, transparent background |

The blur engine is [VariableBlur by nikstar](https://github.com/nikstar/VariableBlur), which uses the same private API Apple uses internally. It is App Store approved.

---

## Critical Rules

### ❌ Never add an opaque background to the header
```swift
// WRONG — hides the blur effect
StickyBlurHeader {
    Text("Header")
        .background(Color.white) // ❌ Breaks the blur
}

// CORRECT — no background on header views
StickyBlurHeader {
    Text("Header") // ✅ Transparent, blur shows through
}
```

### ❌ Never clip the content hierarchy
```swift
// WRONG
StickyBlurHeader { ... } content: {
    VStack { ... }
        .clipped() // ❌ Content becomes invisible under header
}

// CORRECT — let content remain visible under blur
StickyBlurHeader { ... } content: {
    VStack { ... } // ✅ No clipping
}
```

### ✅ Always set a background on the outer container
```swift
StickyBlurHeader { ... } content: { ... }
    .background(Color(.systemBackground)) // ✅ Required for tint to work correctly
```

---

## Troubleshooting

### Blur not visible / header looks opaque
- Remove any `.background(...)` modifier from your header view
- Ensure no parent view adds a background before `StickyBlurHeader`

### Content disappears under header
- Remove any `.clipped()` from the content or its ancestors
- Do not wrap content in a `ScrollView` — `StickyBlurHeader` provides its own

### Header height is wrong
- Do not set explicit heights on the header; let it size naturally
- `GeometryReader` measures the header automatically

### Tint color looks wrong in dark mode
- The tint adapts automatically; ensure `.background(Color(.systemBackground))` is set on the outer view so the adaptive color has a reference

### Build error: "No such module 'ProgressiveBlurHeader'"
- Confirm the package is added in Xcode under **Package Dependencies**
- Clean build folder: **Product → Clean Build Folder** (⇧⌘K)
- Check the target membership of the package in your app target

### iOS version compatibility
- Minimum deployment target must be **iOS 16.0** or higher
- Set in Xcode: Target → General → Minimum Deployments

---

## iOS 26 Comparison

iOS 26 adds `.safeAreaBar(edge: .top)` — a native one-liner for sticky blur bars. Use `ProgressiveBlurHeader` when you need:
- Custom blur radius
- Adjustable tint intensity
- Extended fade below the header
- iOS 16–25 support
