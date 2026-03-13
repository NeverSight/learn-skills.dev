---
name: tech-stack-validator
description: "Validates and recommends technology stacks for native macOS/iOS app projects against PRD and architecture requirements. Reads the PRD and architecture documents (or gathers requirements interactively), then systematically checks every technology choice for: OS version availability, framework capability gaps, performance feasibility, distribution compatibility (sandbox vs direct), API deprecation risks, dependency conflicts, and timeline realism for the team size. Produces a structured validation report with go/no-go verdicts, risk flags, and alternative recommendations. Use when user says things like 'validate my tech stack', 'check if this architecture works', 'what should I build this with', 'is SwiftData the right choice', 'can I ship this on the App Store', 'review my architecture', or before starting implementation of any PRD. Also use when migrating between tech stacks or evaluating whether to adopt a new framework."
---

# Tech Stack Validator

## Overview

Validate that the chosen technology stack can actually deliver what the PRD promises. This skill catches the expensive mistakes — the ones you discover 6 weeks into implementation when a framework doesn't support a critical requirement.

**Core principle:** Every tech choice is a trade-off. The job isn't to find the "best" stack — it's to find the stack where the trade-offs align with the project's priorities.

## Workflow

```
Step 1: INGEST        → Read PRD + Architecture docs, extract requirements
Step 2: CONSTRAINT MAP → Map requirements to technology constraints
Step 3: VALIDATE      → Check each tech choice against constraints
Step 4: RISK SCAN     → Flag deprecations, gaps, compatibility issues
Step 5: REPORT        → Produce validation report with verdicts
```

### Entry Points

- **"Validate my tech stack"** → User provides PRD/architecture docs → Full workflow
- **"What should I build this with?"** → Gather requirements interactively → Recommend stack → Validate
- **"Is [framework X] the right choice for [requirement Y]?"** → Focused validation on specific choice
- **"Review my architecture doc"** → Read doc → Steps 2-5
- **"I'm deciding between X and Y"** → Comparative analysis against requirements

## Step 1: Ingest — Extract Requirements

### From Documents
If the user provides a PRD and/or architecture document, extract these requirement categories:

```
PLATFORM REQUIREMENTS
├── Target OS and minimum version (e.g., macOS 26+, iOS 18+)
├── Device targets (Mac, iPhone, iPad, Vision Pro, Watch)
├── Universal or platform-specific builds
└── Apple Silicon only or Intel support needed

DISTRIBUTION REQUIREMENTS
├── App Store (sandbox mandatory)
├── Direct distribution (notarized, no sandbox)
├── Both (dual binary or feature-gated)
└── TestFlight / Enterprise distribution

FUNCTIONAL REQUIREMENTS → TECH IMPLICATIONS
├── Local persistence → SwiftData, Core Data, SQLite, Realm, file-based
├── Cloud sync → CloudKit, custom server, third-party BaaS
├── Real-time collaboration → WebSockets, CloudKit sharing, custom
├── AI/ML features → Core ML, FoundationModels, Vision, NLP
├── Rich text editing → TextKit 2, AttributedString, custom
├── Web content → WebKit (new WebView vs WKWebView bridge)
├── Background processing → BGTaskScheduler, URLSession background
├── System integration → Hotkeys, Accessibility API, pasteboard
├── Notifications → Local, push (APNs), AlarmKit
└── Widgets / Extensions → WidgetKit, App Intents

PERFORMANCE REQUIREMENTS
├── Launch time budget
├── Memory budget
├── Search/query latency at expected data volume
├── Animation frame rate
└── Storage per unit of content

NON-FUNCTIONAL REQUIREMENTS
├── Accessibility (VoiceOver, keyboard nav, Dynamic Type)
├── Localization (RTL support, string extraction)
├── Security (encryption at rest, keychain, network security)
├── Privacy (privacy manifest, tracking transparency)
└── Offline capability (full, partial, online-only)

TEAM & TIMELINE
├── Solo developer or team size
├── Timeline to v1.0
├── Existing codebase or greenfield
├── Team's framework experience
└── Maintenance runway (who maintains this after launch?)
```

### From Conversation
If no documents exist, ask these questions (2-3 at a time):

1. What's the app? What platform and minimum OS?
2. App Store, direct distribution, or both?
3. What data does it persist? Does it sync across devices?
4. What system features does it need? (Hotkeys, clipboard, widgets, Siri, etc.)
5. What's the team size and timeline?
6. Any existing code or starting fresh?
7. Any strong preferences or constraints? (e.g., "must use SwiftUI only, no AppKit")

## Step 2: Constraint Map

Map each requirement to the technology dimensions it constrains:

### Constraint Categories

| Dimension | What It Determines |
|-----------|-------------------|
| **Language version** | Swift 6.2 features (default MainActor, @concurrent) need Xcode 26+ |
| **UI framework** | SwiftUI-only vs SwiftUI+AppKit bridge determines what's possible |
| **Persistence** | SwiftData vs Core Data vs SQLite — each has different sync, migration, and query capabilities |
| **Sync engine** | CloudKit (Apple-only) vs custom server vs third-party — determines offline strategy |
| **Minimum OS** | Gates which frameworks/APIs are available (see availability matrix) |
| **Distribution** | Sandbox restrictions eliminate certain capabilities |
| **Concurrency model** | Swift 6 strict concurrency vs 5.x — affects every file in the project |
| **Design system** | Liquid Glass requires macOS 26+ / iOS 26+ |

### OS Availability Matrix (Key Frameworks)

| Framework / API | macOS | iOS | Notes |
|----------------|-------|-----|-------|
| SwiftUI | 10.15+ | 13+ | Feature set varies significantly by version |
| SwiftData | 14+ | 17+ | Class inheritance: 15+ / 18+ |
| @Observable | 14+ | 17+ | Replaces ObservableObject |
| NavigationSplitView | 13+ | 16+ | Replaces NavigationView |
| Liquid Glass (.glassEffect) | 26+ | 26+ | New design system, not backportable |
| FoundationModels (on-device LLM) | 26+ | 26+ | Apple Silicon with Apple Intelligence |
| WebView (SwiftUI native) | 26+ | 26+ | Replaces WKWebView bridge pattern |
| AlarmKit | — | 18+ | iOS only |
| App Intents | 13+ | 16+ | Advanced features (modes, snippets) in 26+ |
| Swift Testing | Xcode 16+ | Xcode 16+ | Replaces XCTest |
| Swift 6.2 (default MainActor) | Xcode 26 | Xcode 26 | Language-level, not OS-gated |
| GlassEffectContainer | 26+ | 26+ | Required for multiple glass effects |
| Chart3D | 26+ | 26+ | 3D charts, visionOS volumetric |
| WidgetKit | 14+ | 14+ | Accented mode: 26+ |

### Sandbox Compatibility Matrix

| Capability | Sandboxed (App Store) | Direct Distribution |
|-----------|----------------------|-------------------|
| Global hotkeys (Carbon) | ⚠️ Needs entitlement | ✅ |
| Accessibility API (AX) | ⚠️ Entitlement + user permission | ✅ |
| CGEvent keystroke simulation | ❌ Blocked | ✅ (with Accessibility) |
| Clipboard read/write | ✅ | ✅ |
| File access (arbitrary) | ❌ User-selected only | ✅ |
| Network (outbound) | ⚠️ Needs entitlement | ✅ |
| Launch at login | ✅ SMAppService | ✅ |
| iCloud sync | ✅ | ✅ |
| Keychain | ✅ (app-scoped) | ✅ |
| Screen recording | ❌ | ✅ (with permission) |

## Step 3: Validate Each Choice

For every technology in the proposed stack, check:

### 3.1 Availability
- Is it available on the target OS version?
- If targeting multiple platforms, is it available on ALL of them?
- Are there feature gaps between OS versions? (e.g., SwiftData inheritance needs macOS 15+)

### 3.2 Capability
- Can this technology deliver the specific requirement?
- At the required scale? (e.g., SwiftData with 100K records — is @Query performant enough?)
- With the required latency? (e.g., full-text search in < 50ms)

### 3.3 Compatibility
- Does it work with the distribution model? (Sandbox restrictions?)
- Does it work with the other chosen technologies? (e.g., SwiftData + CloudKit sync — are there known limitations?)
- Does the concurrency model align? (Swift 6 strict checking + chosen frameworks)

### 3.4 Maturity
- Is this framework stable or still evolving rapidly?
- Are there known bugs or limitations in the current version?
- Is there sufficient documentation and community knowledge?

### 3.5 Maintenance
- Who maintains this dependency? (Apple framework vs third-party)
- What happens if it's deprecated? (Migration path?)
- Does the team have experience with it?

## Step 4: Risk Scan

### Deprecation Risks
Check for deprecated or soon-to-be-deprecated patterns:
- `NavigationView` → `NavigationSplitView` / `NavigationStack`
- `ObservableObject` + `@Published` → `@Observable`
- `WKWebView` + Representable → Native `WebView`
- `NSVisualEffectView` → `NSGlassEffectView` / `.glassEffect()`
- `XCTest` → Swift Testing
- `@StateObject` → `@State` with `@Observable`

### Common Mismatch Patterns

| PRD Says | Architecture Uses | Problem |
|----------|------------------|---------|
| "Works on macOS 14+" | Liquid Glass / .glassEffect() | Liquid Glass requires macOS 26+ |
| "App Store distribution" | CGEvent text insertion | Blocked by sandbox |
| "Offline-first with sync" | No local persistence layer | Can't work offline without local DB |
| "< 100ms search on 50K items" | SwiftData @Query | Needs benchmarking; may need raw SQLite for complex queries |
| "Solo developer, 8 weeks" | Custom sync server + REST API | Scope exceeds timeline — use CloudKit instead |
| "Privacy-focused, no cloud" | CloudKit sync | Contradicts privacy requirement |
| "Must support Intel Macs" | FoundationModels framework | Requires Apple Silicon + Apple Intelligence |
| "Real-time collaboration" | CloudKit only | CloudKit is eventual-consistency, not real-time |

## Step 5: Validation Report

Produce the report as a file. See `references/report-template.md` for the full template.

### Report Structure

```markdown
# Tech Stack Validation Report: [App Name]

## Verdict: ✅ GO / ⚠️ GO WITH CHANGES / ❌ STOP

## Stack Summary
[Table of every technology choice with verdict]

## Critical Issues (Must Fix Before Starting)
[Issues that will block the project if not addressed]

## Warnings (Should Address Soon)
[Issues that will cause pain but won't block]

## Recommendations
[Suggested changes with rationale]

## Compatibility Matrix
[Full matrix of requirements vs. tech choices]

## Alternative Options Considered
[For each flagged issue, what alternatives exist]
```

### Verdict Criteria

| Verdict | Criteria |
|---------|----------|
| ✅ **GO** | All critical requirements met, no blocking issues, warnings are manageable |
| ⚠️ **GO WITH CHANGES** | 1-3 specific changes needed, but core stack is sound |
| ❌ **STOP** | Fundamental mismatch — chosen stack cannot deliver PRD requirements |

## Decision Frameworks

### When to Use SwiftData vs Core Data vs SQLite

```
Need iCloud sync + simple models?
└── SwiftData (macOS 14+ / iOS 17+)

Need complex queries + large datasets (>100K rows)?
└── SQLite via GRDB or direct SQLite3

Need class inheritance in models?
└── SwiftData (macOS 15+ / iOS 18+)

Need to support macOS 13 or iOS 16?
└── Core Data

Need both complex queries AND sync?
└── Core Data + CloudKit, or SQLite + custom sync
```

### When to Use SwiftUI-Only vs SwiftUI + AppKit Bridge

```
App Store sidebar+detail app, standard controls?
└── SwiftUI-only

Need floating panel (NSPanel)?
└── SwiftUI + AppKit bridge

Need global hotkeys or CGEvent?
└── SwiftUI + AppKit (AppDelegate)

Need custom window chrome or levels?
└── SwiftUI + NSWindow/NSPanel

Need menu bar with popover?
└── MenuBarExtra (pure SwiftUI) OR NSStatusItem + NSPopover (more control)
```

### When to Use CloudKit vs Custom Server

```
Apple-only users, simple data, offline-first?
└── CloudKit (free, built-in, handles conflicts)

Need cross-platform (Android/Web)?
└── Custom server or Firebase/Supabase

Need real-time collaboration?
└── Custom WebSocket server or third-party (Supabase Realtime)

Need fine-grained access control?
└── Custom server

Solo developer, limited budget?
└── CloudKit (zero infrastructure cost)
```

## Interaction Style

- Be direct about risks — sugar-coating wastes the developer's time
- Quantify when possible ("SwiftData @Query on 50K records: ~200ms" not "might be slow")
- Always provide alternatives when flagging issues
- Distinguish between "this won't work" (hard blocker) and "this will hurt" (soft issue)
- If the user has strong preferences, respect them but flag trade-offs clearly
- Remember that the "right" stack depends on team skills, timeline, and priorities — not just technical optimality

## Key Principles

1. **Requirements drive choices, not preferences** — "I like SwiftData" is not a justification if Core Data fits the requirements better
2. **Validate at the boundaries** — Most tech works fine in isolation; problems emerge at integration points
3. **Time is a constraint** — A technically superior stack that takes 6 months to learn is worse than a familiar stack that ships in 8 weeks
4. **Distribution gates capabilities** — App Store sandbox restrictions are non-negotiable and must be checked early
5. **OS version is destiny** — Every API has a minimum OS; the lowest target version constrains everything
6. **Dependencies are debt** — Every third-party dependency is a maintenance commitment; prefer Apple frameworks when they're sufficient
7. **Check the edges, not the middle** — Basic CRUD works with anything; validate against the hardest requirements (performance, sync, offline, scale)
