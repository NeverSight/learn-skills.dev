---
name: apple-design-ios
description: "Design, implement, or review iPhone interfaces using Apple’s iOS Human Interface Guidelines. Use for iOS screen structure, touch ergonomics, adaptive behavior, and integration with iPhone system experiences."
---

# Design for iOS

## Apply the skill

Establish the primary task, supported iPhone configurations, minimum iOS version, and existing framework. When an app or design artifact is provided, inspect it before proposing changes; for a new concept, work from the brief and state necessary assumptions. Preserve the chosen stack, including SwiftUI, UIKit, React Native, or another framework; translate native behavior into that stack instead of replacing it.

Model the main destinations, navigation state, and any scoped modal task before arranging controls. Specify what happens after Back, cancellation, backgrounding, an interrupted operation, and reentry through a deep link. Use the iOS reference for device-specific priorities.

For implementation work, use platform components where they satisfy the interaction and verify API availability against the target SDK. For visual design, annotate interaction states and adaptation instead of presenting a single idealized screenshot.

Read the implementation review reference when delivering screens or reviewing an existing flow. Inspect the relevant linked HIG component page before prescribing version-sensitive navigation, search, materials, sizes, or system integration. For companion iPad work, also read [Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados) and account for its windowing and input model.

## Topic references

Select the topic that matches the design decision; do not load this entire list by default.

- [Designing for iOS](references/designing-for-ios.md)
- [Implementation and review](references/implementation-review.md) — for screen delivery, adaptation checks, and implementation review.

## Source use

These references are original operational summaries of Apple’s public HIG, checked on 2026-09-08. They are guidance for design decisions, not a reproduced manual or a guarantee of App Store acceptance.

Read only the topic references relevant to the current task. Each links to the full official page. Consult that page for exact specifications, platform exceptions, assets, and version-sensitive behavior; use current official developer documentation for APIs and availability. If live documentation is unavailable, state the snapshot date and identify assumptions instead of inventing current requirements.

The user’s product goals, selected framework, and authorized scope remain controlling. Distinguish a source recommendation from a hard platform requirement and from your own proposed implementation.
