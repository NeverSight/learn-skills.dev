---
name: ios-accessibility
description: 'Expert guidance on iOS accessibility best practices, patterns, and implementation. Use when developers mention: (1) iOS accessibility, VoiceOver, Dynamic Type, or assistive technologies, (2) accessibility labels, traits, hints, or values, (3) automated accessibility testing, auditing, or manual testing, (4) Switch Control, Voice Control, or Full Keyboard Access, (5) inclusive design or accessibility culture, (6) making apps work for users with disabilities.'
---

# iOS Accessibility

## Overview

This skill provides expert guidance on iOS accessibility, covering VoiceOver, Dynamic Type, assistive technologies, inclusive design practices, and both UIKit and SwiftUI implementations. Use this skill to help developers build apps that work for everyone.

## The Approach

- **Shift-left** — Accessibility is part of the process. It needs to be considered even in prototypes or MVPs.
- **User-centric** — Accessibility is about people. Checklists help, but the goal is not checklist compliance. The goal is to offer a great experience for users with disabilities.
- **Progress over perfection** — Anytime is a good time to start. Focus on iterative and incremental improvements as you go. It goes a long way.
- **Test as you go** — Manual testing is part of development.

## Agent Behavior Contract

1. **Accessibility is non-deterministic.** Propose potential solutions in order of confidence and present with clear pros, cons, and trade-offs.
2. Before proposing fixes, identify the platform (UIKit vs SwiftUI) and the assistive technology, accessibility feature, or design consideration in context.
3. Do not recommend accessibility fixes without considering the user experience impact.
4. Prefer manual testing guidance alongside code changes, together with any automated or semi-automated solutions.
5. Cross-reference multiple assistive technologies when relevant (VoiceOver, Voice Control, Switch Control, Full Keyboard Access).

### Anti-Patterns to Avoid

- **Do not add trait names to labels** — Say "Close", not "Close button" (VoiceOver adds "button" automatically, when using the button trait)
- **Do not use `.accessibilityHidden(true)` on interactive elements** — Users won't be able to access them
- **Do not use fixed font sizes** — Always use text styles for Dynamic Type support
- **Do not use hardcoded colors for text** — Use semantic colors (`.label`, `.secondaryLabel`) for contrast and Dark Mode
- **Do not group UIKit elements without a clear combined label** — If `isAccessibilityElement = true`, set `accessibilityLabel` (and value/traits as needed).
- **Do not group SwiftUI elements without a clear combined label** — If `.accessibilityElement(children: .ignore)` is used, provide label/value/traits manually.
- **Do not add hints unless needed** — It should be clear what a component expresses, and does, by its label/value/traits. Only configure for adding extra clarity or context.
- **Do not rely on `onTapGesture` alone** — Prefer semantic controls like `Button`. If gesture handling is unavoidable, add button traits and clear labels.
- **Do not scale chrome controls with Dynamic Type** — For navigation bars, toolbars, and tab bars, prefer Large Content Viewer (iOS 13+) using [`.accessibilityShowsLargeContentViewer`](https://developer.apple.com/documentation/swiftui/view/accessibilityshowslargecontentviewer(content:)) / [`UILargeContentViewerItem`](https://developer.apple.com/documentation/uikit/uilargecontentvieweritem).

### General Guidance

**Prefer native components:** Whenever possible, use Apple's native components and customize them to your needs instead of building custom components from scratch.

**Design system first:** Whenever the project uses a design system of its own (colors, text styles, component catalog), propose changes in the design system itself so the improvement snowballs everywhere in the app using an improved component.

**Platform parity:** The same accessibility principles apply to both UIKit and SwiftUI, but APIs and implementation details differ.

## Project Settings Intake (Evaluate Before Advising)

Before providing accessibility guidance, determine:

### Project Capabilities
- **Is the project using SwiftUI, UIKit, or a mix of both?**
- **iOS deployment target** — Some APIs require specific versions:
  - iOS 13+: [Large Content Viewer (`UILargeContentViewerInteraction`)](https://developer.apple.com/documentation/uikit/uilargecontentviewerinteraction), [SF Symbols](https://developer.apple.com/sf-symbols/)
  - iOS 14+: [Switch Control action images (`UIAccessibilityCustomAction.init(name:image:actionHandler:)`)](https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction/init(name:image:actionhandler:))
  - iOS 15+: [`AccessibilityFocusState`](https://developer.apple.com/documentation/swiftui/accessibilityfocusstate), [`.accessibilityRotor`](https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:entryid:entrylabel:))
  - iOS 16+: [`.accessibilityRepresentation`](https://developer.apple.com/documentation/swiftui/view/accessibilityrepresentation(representation:)), [`.accessibilityActions { }` syntax](https://developer.apple.com/documentation/swiftui/view/accessibilityactions(content:))
  - iOS 17+: [`.sensoryFeedback`](https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:))
- **Check minimum OS** — Look for `#available` checks and deployment target in project settings

### Project Conventions
- **Design system** — Does the project define its own design system (colors, text styles, UI component catalogue)? Propose changes in the design system when appropriate, not only per-feature.
- **Semantic colors and text styles** — Does the project use semantic colors (`.label`, `.systemBackground`) and text styles (`.preferredFont(forTextStyle:)` in UIKit, `.font(.body)` in SwiftUI) vs hardcoded values?
- **Existing accessibility patterns** — Search for `.accessibilityLabel`, `.accessibilityTraits`, etc. to match project style.
- **Localization** — Accessibility labels, values, and hints should be localized. Match the project's localization conventions.
- **UI construction** — Interface Builder (XIB/Storyboard) or code-only?
- **Custom gestures** — Identify if custom gestures need accessible alternatives.
- **Accessibility test coverage** — Existing UI tests auditing for accessibility?

### When Settings Are Unknown
If you can't determine the above, ask the developer to confirm before giving version-specific or framework-specific guidance.

## Quick Decision Tree

When a developer needs accessibility guidance, follow this decision tree:

1. **VoiceOver issues?**
   - Core concepts: Read `references/voiceover.md`
   - UIKit implementation: Read `references/voiceover-uikit.md`
   - SwiftUI implementation: Read `references/voiceover-swiftui.md`

2. **Dynamic Type, text scaling, or adaptive layout?**
   - Core concepts: Read `references/dynamic-type.md`
   - UIKit implementation: Read `references/dynamic-type-uikit.md`
   - SwiftUI implementation: Read `references/dynamic-type-swiftui.md`

3. **Other assistive technologies?**
   - Voice Control: Read `references/voice-control.md`
   - Switch Control: Read `references/switch-control.md`
   - Full Keyboard Access: Read `references/full-keyboard-access.md`

4. **Testing accessibility?**
   - Manual testing: Read `references/testing-manual.md`
   - Automated testing: Read `references/testing-automated.md`

5. **Cross-cutting concerns?**
   - Contrast, targets, motion, haptics: Read `references/good-practices.md`
   - Culture and mindset: Read `references/concepts-and-culture.md`

6. **Quick reference needed?**
   - Common mistakes, patterns, checklists: Read `references/playbook.md`

7. **Need definitions or sources?**
   - Glossary: Read `references/glossary.md`
   - Sources and further reading: Read `references/resources.md`

## Quick Playbook (Start Here)

1. Confirm **framework** (UIKit vs SwiftUI) and **iOS target**.
2. Identify **assistive technology** and **user-experience issue**.
3. Use the **Decision Tree** and jump into the relevant reference file.
4. Whenever it makes sense, provide **2-3 options** with trade-offs and expected UX impact.
5. Always include **testing guidance** alongside any code changes.

For common mistakes, inspector warnings, code patterns, version-specific APIs, and checklists, use `references/playbook.md`.

## Example Prompts and Expected Shape

**Example prompt:** “VoiceOver reads ‘button’ for my close button.”
**Expected response:**
- Confirm framework and iOS target if unknown.
- Provide options when there are multiple viable approaches (for example, add an accessibility label vs a labeled button using icon-only style), with trade-offs.
- Include a framework-appropriate snippet.
- Add testing steps (VoiceOver, Voice Control...).

**Example prompt:** “Dynamic Type breaks my header layout in UIKit.”
**Expected response:**
- Confirm `preferredContentSizeCategory` handling and iOS target.
- Suggest layout adaptation strategies (stack axis change vs constraints).
- Include a UIKit snippet and testing steps at Large Accessibility Sizes.

## Edge Cases and Gotchas

- Mixed UIKit/SwiftUI screens: use correct API set per view layer.
- Custom controls or gestures: always provide a VoiceOver/Voice Control alternative.
- Unknown iOS target: ask before suggesting version-specific APIs.
- No code context: ask for relevant view code or a screenshot of the Accessibility Inspector.
- Localization: all labels, values, and hints (and any other string parameter like custom content, or accessibility announcements, etc.) must be localized.
