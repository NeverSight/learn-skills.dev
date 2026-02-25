---
name: swiftui-design-principles
description: Design principles for building polished, native-feeling SwiftUI apps and widgets. Use this skill when creating or modifying SwiftUI views, iOS widgets (WidgetKit), or any native Apple UI. Ensures proper spacing, typography, colors, and widget implementations that look and feel like quality apps rather than AI-generated slop.
license: MIT
metadata:
  author: arjitj2
  version: "1.1.0"
---

This skill encodes design principles derived from comparing polished, production-quality SwiftUI apps against poorly-built ones. The patterns here represent what separates an app that feels "right" from one where the margins, spacing, and text sizes just look "off."

Apply these principles whenever building or modifying SwiftUI interfaces, WidgetKit widgets, or any native Apple UI.

## Core Philosophy

**Restraint over decoration.** Every pixel must earn its place. A polished app uses fewer colors, fewer font sizes, and fewer spacing values — but uses them consistently. Over-engineering visual elements (custom gradients, decorative borders, bespoke dividers) creates visual noise. Native components and system colors create harmony.

---

## 1. Spacing System: Use a Consistent Grid

**CRITICAL**: Use spacing values from a base-4/base-8 grid. Never use arbitrary values.

### Allowed spacing values
```
4, 8, 12, 16, 20, 24, 32, 40, 48
```

### Bad (arbitrary values that create visual dissonance)
```swift
// WRONG - these numbers have no relationship to each other
.padding(.bottom, 26)
.padding(.bottom, 34)
.padding(.bottom, 36)
HStack(spacing: 18)
.padding(14)
```

### Good (values from a consistent grid)
```swift
// RIGHT - predictable rhythm the eye can follow
.padding(.horizontal, 20)
.padding(.top, 8)
Spacer().frame(height: 32)
HStack(spacing: 4)  // or 8, 12, 16
.padding(.vertical, 12)
.padding(.horizontal, 16)
```

### Standard padding assignments
- **Outer content padding**: 16-20pt horizontal
- **Between major sections**: 24-32pt vertical
- **Within grouped components**: 4-12pt
- **Card/row internal padding**: 12-16pt vertical, 16pt horizontal

---

## 2. Typography: Hierarchy Through Weight, Not Just Size

### The principle
Use **fewer font sizes** with **clear weight differentiation**. Lighter weights at larger sizes; medium/regular at smaller sizes. This creates sophistication rather than visual chaos.

### Recommended type scale (for a data-focused app)
| Role | Size | Weight | Notes |
|------|------|--------|-------|
| Hero number | 36-42pt | `.light` | Large but visually light -- elegant, not heavy |
| Secondary stat | 20-24pt | `.light` | Same weight family as hero, smaller |
| Body / toggle label | 15pt | `.regular` | Standard iOS body size |
| Section header (uppercase) | 11pt | `.medium` | With tracking/letter-spacing |
| Caption / subtitle | 11-13pt | `.regular` | Secondary information |

### Bad (too many sizes, inconsistent weights)
```swift
// WRONG - 7 different sizes with no clear system
.font(.system(size: 60, weight: .ultraLight))   // hero
.font(.system(size: 44, weight: .regular))        // stat (too close to hero)
.font(.system(size: 31, weight: .ultraLight))     // percent symbol (odd ratio)
.font(.system(size: 18, weight: .regular))        // label (too big for a toggle)
.font(.system(size: 14, weight: .regular))        // header
.font(.system(size: 13, weight: .regular))        // another header
.font(.system(size: 12, weight: .regular))        // button (too small to read)
```

### Good (clear hierarchy, fewer sizes)
```swift
// RIGHT - 5 sizes, clear purpose for each
.font(.system(size: 42, weight: .light, design: .monospaced))    // hero
.font(.system(size: 24, weight: .light, design: .monospaced))    // stat value
.font(.system(size: 15, weight: .regular, design: .monospaced))  // body
.font(.system(size: 14, weight: .regular, design: .monospaced))  // secondary
.font(.system(size: 11, weight: .medium, design: .monospaced))   // label
```

### Font design consistency
Pick ONE font design and use it everywhere -- app AND widgets:
```swift
// If using monospaced, use it everywhere
design: .monospaced  // app views, widgets, lock screen -- all of them

// NEVER mix designs between app and widgets
// BAD: .monospaced in app, .rounded in lock screen widget
```

### Letter spacing (tracking)
Use at most 2 values, and only on uppercase labels:
```swift
.tracking(1.5)  // section labels: "NOTIFICATIONS", "DAY", "LEFT"
.tracking(3)    // navigation/toolbar titles
```

**Never use 3+ different tracking values** like `kerning(4)`, `kerning(4.5)`, `kerning(5)` -- the differences are imperceptible but the inconsistency registers subconsciously.

### Numeric formatting for identifiers
Years and other fixed identifiers should not be locale-grouped.
```swift
// RIGHT - stable, non-grouped identifier text
Text(String(year))                  // "2026"
Text(year, format: .number.grouping(.never))

// WRONG - locale grouping can render "2,026"
Text("\(year)")
```

---

## 3. Colors: System Semantic Colors Over Hardcoded Values

### The principle
Use SwiftUI's semantic color system. It automatically handles light/dark mode, accessibility, and looks native. Hardcoded colors with manual opacity values create maintenance nightmares and look artificial.

### Bad (hardcoded white with a dozen opacity values)
```swift
// WRONG - impossible to maintain, doesn't adapt to light mode
Color.black.ignoresSafeArea()           // forced dark
Color.white.opacity(0.08)               // ring background
Color.white.opacity(0.09)               // divider
Color.white.opacity(0.3)                // year text
Color.white.opacity(0.32)               // stat label
Color.white.opacity(0.42)               // percent symbol
Color.white.opacity(0.44)               // toggle tint
Color.white.opacity(0.72)               // button text
Color.white.opacity(0.88)               // toggle label
Color.white.opacity(0.9)                // stat value
Color.white.opacity(0.94)               // ring fill
```

### Good (semantic system colors)
```swift
// RIGHT - adapts automatically, looks native, easy to maintain
Color(.systemBackground)                 // main background
Color(.secondarySystemBackground)        // card/group backgrounds
Color(.separator)                        // dividers (with optional opacity)
Color.primary                            // primary text and UI elements
.foregroundStyle(.secondary)              // secondary text
.foregroundStyle(.tertiary)               // labels, captions
```

### When you do need opacity
Limit to 2-3 values with clear purposes:
```swift
.opacity(0.15)  // subtle background strokes
.opacity(0.3)   // separator lines
// That's it. If you need more, you're probably hardcoding what semantic colors handle.
```

---

## 4. Component Sizing: Proportional, Not Oversized

### Progress rings / circular indicators
```swift
// App main view: 200x200 with thin stroke
.frame(width: 200, height: 200)
Circle().stroke(..., lineWidth: 3)

// Widget (systemSmall): 90x90, same stroke
.frame(width: 90, height: 90)
Circle().stroke(..., lineWidth: 3)

// WRONG: oversized ring with thick inconsistent strokes
.frame(width: 260, height: 260)    // too large, dominates screen
Circle().stroke(..., lineWidth: 9)  // background
Circle().stroke(..., lineWidth: 8)  // fill -- WHY different from background?
```

### Stroke width consistency
**Always use the same lineWidth for background and foreground strokes of the same element:**
```swift
// RIGHT
Circle().stroke(background, lineWidth: 3)
Circle().trim(from: 0, to: fraction).stroke(fill, lineWidth: 3)

// WRONG - creates visual misalignment
Circle().stroke(background, lineWidth: 9)
Circle().trim(from: 0, to: fraction).stroke(fill, lineWidth: 8)
```

### List rows and toggle rows
```swift
// RIGHT - natural sizing with proper padding
Toggle(isOn: $value) {
    Text(title)
        .font(.system(size: 15, weight: .regular, design: .monospaced))
}
.padding(.horizontal, 16)
.padding(.vertical, 12)

// WRONG - fixed oversized height
HStack {
    Text(label)
        .font(.system(size: 18))   // too big for a toggle label
    Spacer()
    Toggle("", isOn: $isOn)
        .labelsHidden()             // why hide the label? Use Toggle properly
}
.frame(height: 70)                  // way too tall
```

---

## 5. Grouped Content & Cards: Use System Patterns

### Bad (over-engineered custom card)
```swift
// WRONG - custom gradient, overlay border, huge corner radius
VStack { ... }
    .padding(.vertical, 4)              // too tight
    .background(
        RoundedRectangle(cornerRadius: 22)   // too round
            .fill(LinearGradient(            // unnecessary gradient
                colors: [Color(white: 0.10), Color(white: 0.085)],
                startPoint: .topLeading, endPoint: .bottomTrailing
            ))
    )
    .overlay(
        RoundedRectangle(cornerRadius: 22)
            .stroke(Color.white.opacity(0.08), lineWidth: 1)  // decorative border
    )
```

### Good (native grouped style)
```swift
// RIGHT - simple, native, works in light and dark mode
VStack(spacing: 0) {
    row1
    Divider().padding(.leading, 16)
    row2
    Divider().padding(.leading, 16)
    row3
}
.background(Color(.secondarySystemBackground))
.clipShape(.rect(cornerRadius: 10))
```

### Key rules for grouped content
- **Corner radius**: 10pt for cards/groups (matches iOS system style). Never 22pt+.
- **Dividers**: Use the system `Divider()` with `.padding(.leading, 16)` for iOS-standard inset. Never build custom divider structs.
- **Card padding**: 12-16pt vertical, 16pt horizontal. Never 4pt vertical.
- **Background**: `Color(.secondarySystemBackground)` -- never custom gradients for standard cards.

---

## 6. Navigation: Use NavigationStack

```swift
// RIGHT - proper navigation with minimal toolbar
NavigationStack {
    ScrollView {
        content
    }
    .toolbar {
        ToolbarItem(placement: .principal) {
            Text("Title")
                .font(.system(size: 13, weight: .medium, design: .monospaced))
                .tracking(3)
                .foregroundStyle(.tertiary)
        }
    }
    .navigationBarTitleDisplayMode(.inline)
}

// WRONG - no navigation structure, just a ZStack
ZStack {
    Color.black.ignoresSafeArea()
    ScrollView {
        VStack {
            Text("2026").font(...) // manually placed "title"
            content
        }
    }
}
```

---

## 7. WidgetKit: Use Native Components

### Circular lock screen widget
```swift
// RIGHT - use Gauge, it's purpose-built for this
Gauge(value: entry.fraction) {
    Text("")
} currentValueLabel: {
    Text("\(Int(entry.percentage))%")
        .font(.system(size: 12, weight: .medium, design: .monospaced))
}
.gaugeStyle(.accessoryCircular)
.containerBackground(.fill.tertiary, for: .widget)

// WRONG - manual circle drawing for lock screen
ZStack {
    Circle().stroke(Color.primary.opacity(0.18), lineWidth: 4)
    Circle().trim(from: 0, to: progress).stroke(...)
    Text(percentText)
        .font(.system(size: 14, weight: .bold, design: .rounded)) // wrong font design!
}
```

### Rectangular lock screen widget
```swift
// RIGHT - use Gauge with linearCapacity
VStack(alignment: .leading, spacing: 4) {
    HStack {
        Text(year).font(.system(size: 13, weight: .semibold, design: .monospaced))
        Spacer()
        Text(percentage).font(.system(size: 13, weight: .medium, design: .monospaced))
            .foregroundStyle(.secondary)
    }
    Gauge(value: fraction) { Text("") }
        .gaugeStyle(.linearCapacity)
        .tint(.primary)
    HStack {
        Spacer()
        Text("\(dayOfYear)/\(totalDays)")
            .font(.system(size: 11, weight: .regular, design: .monospaced))
            .foregroundStyle(.secondary)
    }
}
.containerBackground(.fill.tertiary, for: .widget)

// WRONG - custom GeometryReader progress bar
GeometryReader { proxy in
    ZStack(alignment: .leading) {
        RoundedRectangle(cornerRadius: 2).fill(Color.primary.opacity(0.16))
        RoundedRectangle(cornerRadius: 2).fill(Color.primary)
            .frame(width: max(2, proxy.size.width * progress))
    }
}
.frame(height: 6)
```

### Widget background
```swift
// RIGHT
.containerBackground(.fill.tertiary, for: .widget)

// WRONG - hardcoded color
.containerBackground(.black, for: .widget)
```

### Widget family coverage
Support all relevant families -- don't skip common ones:
```swift
.supportedFamilies([
    .accessoryCircular,      // lock screen circle
    .accessoryRectangular,   // lock screen rectangle
    .accessoryInline,        // lock screen inline text
    .systemSmall,            // home screen small
    .systemMedium,           // home screen medium
    .systemLarge,            // home screen large
])
```

### Cross-family visual consistency
Medium and large home widgets should share the same structural layout:
- Header: year on the left, percentage on the right
- Middle: progress bar
- Footer: `day/total` right aligned

Do not re-invent hierarchy per family unless there is a hard size constraint.

Always include explicit internal padding on home widgets to avoid clipping near rounded edges:
```swift
.padding(.horizontal, 12)
.padding(.vertical, 12)
```

### Widget memory budget (hard limit)
Widget extensions have a tight memory budget (commonly around 30 MB). Dense visualizations can be killed by `EXC_RESOURCE` if built from too many nested views.

```swift
// RIGHT - draw dense dot grids in one pass
Canvas { context, size in
    // draw 365/366 dots here
}

// WRONG - hundreds of nested subviews (high memory overhead)
LazyVGrid(columns: columns) {
    ForEach(1...366, id: \.self) { day in
        ZStack { Circle(); partialFillLayer }
    }
}
```

### Timeline refresh (match data granularity)
```swift
// RIGHT - refresh at midnight for day-level data
let tomorrow = calendar.startOfDay(for: calendar.date(byAdding: .day, value: 1, to: now)!)
Timeline(entries: [entry], policy: .after(tomorrow))

// RIGHT - periodic refresh for time-of-day dependent percentages/partial fills
let refresh = Calendar.current.date(byAdding: .minute, value: 15, to: now)!
Timeline(entries: [entry], policy: .after(refresh))

// WRONG - minute-level refresh for static daily data
let tooFrequent = Calendar.current.date(byAdding: .minute, value: 1, to: now)!
Timeline(entries: [entry], policy: .after(tooFrequent))
```

---

## 8. Interactive Elements

### Toggles
```swift
// RIGHT - use Toggle with its built-in label, tint with a single accent color
Toggle(isOn: $value) {
    Text(title)
        .font(.system(size: 15, weight: .regular, design: .monospaced))
}
.tint(.green)

// WRONG - hidden label with manual HStack layout
HStack {
    Text(label).font(.system(size: 18))
    Spacer()
    Toggle("", isOn: $isOn)
        .labelsHidden()
        .tint(Color.white.opacity(0.44))  // low-contrast tint
}
```

### Mutually exclusive options
When options are exclusive (e.g. daily/weekly/monthly cadence), use one selected value, not three independent toggles.

```swift
// RIGHT - single source of truth
enum Cadence: String, CaseIterable { case daily, weekly, monthly }
@State private var cadence: Cadence = .daily

ForEach(Cadence.allCases, id: \.rawValue) { option in
    Button {
        cadence = option
    } label: {
        HStack {
            Image(systemName: cadence == option ? "checkmark.circle.fill" : "circle")
            Text(option.rawValue.capitalized)
        }
    }
}

// RIGHT - one preview action when content is shared
Button("Preview") { sendPreview() }

// WRONG - independent toggles allow contradictory state
Toggle("Daily", isOn: $daily)
Toggle("Weekly", isOn: $weekly)
Toggle("Monthly", isOn: $monthly)
```

### Animated transitions for changing numbers
```swift
// Add to any Text that displays a changing numeric value
Text(String(format: "%.2f", percentage))
    .contentTransition(.numericText())
```

---

## 9. Data Model: Share Between App and Widgets

```swift
// RIGHT - one model used everywhere
struct YearProgress {
    // shared calculation logic
    static func current() -> YearProgress { ... }
}
// Used by both ContentView and widget TimelineProvider

// If percentage is shown as live progress, include time-of-day in shared math
let dayProgress = elapsedInCurrentDay / totalSecondsInDay
let elapsedDays = Double(dayOfYear - 1) + dayProgress
let fraction = elapsedDays / Double(totalDays)

// WRONG - separate snapshot structs with duplicated date math
struct YearProgressSnapshot { ... }            // in app
struct YearProgressWidgetSnapshot { ... }      // in widget extension (duplicated!)
```

---

## 10. Quick Checklist

Before shipping any SwiftUI view, verify:

- [ ] All spacing values come from the grid (4, 8, 12, 16, 20, 24, 32)
- [ ] Font sizes limited to 5 or fewer distinct values
- [ ] One font design used consistently (including widgets)
- [ ] Colors use semantic system colors, not hardcoded values with opacity
- [ ] Background and foreground strokes use the same lineWidth
- [ ] Cards use `Color(.secondarySystemBackground)` with 10pt corner radius
- [ ] Dividers use system `Divider()` with leading padding
- [ ] Toggle rows use Toggle's built-in label (not `.labelsHidden()`)
- [ ] Lock screen widgets use `Gauge` (not manual circle drawing)
- [ ] Widget background uses `.containerBackground(.fill.tertiary, for: .widget)`
- [ ] Year/identifier text avoids locale grouping when grouping is not desired
- [ ] Tracking/kerning limited to 2 values max
- [ ] NavigationStack is used (not bare ZStack)
- [ ] Timeline refresh rate matches data granularity (midnight vs periodic)
- [ ] Large/dense widget visuals use `Canvas` or similarly lightweight rendering
- [ ] Medium and large widget families share consistent hierarchy and internal padding
- [ ] Exclusive choices use a single selected value (not multiple toggles)
- [ ] Percentages include time-of-day when UI implies live progress
- [ ] No `minimumScaleFactor` hacks -- fix the layout instead
