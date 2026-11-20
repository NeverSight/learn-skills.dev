---
name: apple-hig-skill
description: Design, implement, or review native Apple interfaces against the Human Interface Guidelines, with platform-specific decisions and source-backed findings. Use for HIG, interaction, layout, and accessibility work.
license: CC-BY-4.0
metadata:
  author: davidcafor
  version: "0.2.0"
---

# Apple HIG Skill

Make interface decisions that fit the user's task, platform, and abilities. This is an independent interpretation of Apple's guidance, not Apple certification. Follow the user's requested scope; do not redesign a product merely to exercise this skill.

## Establish the task

Identify **review**, **design proposal**, or **implementation** from the request. Inspect the relevant views, entry points, deployment targets, SDK/toolchain, and navigation/state ownership. Identify target platforms, input methods, available window sizes, and the core task. Ask only for missing information that would change the design materially.

- **Review:** inspect first; report supported problems without editing unless requested.
- **Design:** compare suitable native patterns, explain the tradeoff, and specify important states.
- **Implementation:** make the scoped change and validate what the environment supports. Do not stop at recommendations when changes were requested.

## Load only relevant references

Start with the target platform in [platforms.md](references/platforms.md). Then select topics from this table. Do not load the complete library for a narrow task.

| Task | Reference |
| --- | --- |
| Tabs, sidebars, hierarchy, toolbars, search, windows | [Navigation](references/navigation.md) |
| Sheets, popovers, alerts, confirmation, cancellation | [Presentation](references/presentation.md) |
| Buttons, menus, fields, toggles, pickers, forms | [Controls](references/controls.md) |
| Resizing, safe areas, typography, color, materials, symbols | [Layout and visual design](references/layout-visual.md) |
| VoiceOver, motor access, keyboard/focus, motion, contrast | [Accessibility and input](references/accessibility-input.md) |
| Settings, onboarding, loading, errors, accounts, permissions | [Product flows](references/product-flows.md) |
| Localization, RTL, interface copy | [Writing and localization](references/writing-localization.md) |
| Widgets, complications, Live Activities, notifications, CarPlay | [System experiences](references/system-experiences.md) |
| Mapping design to SwiftUI, API checks, original code examples | [SwiftUI implementation](references/swiftui-implementation.md) |
| Evidence, severity, conflicting guidance, test matrix, output | [Review and validation](references/review-validation.md) |
| Source provenance and freshness | [Source registry](references/sources.md) |

## Apply judgment with evidence

1. Establish an observable problem and user impact before recommending a change. Source code, screenshots, and runtime behavior provide different evidence.
2. Prefer system components when they fit the task. Custom controls and brand styling are valid when they preserve interaction, accessibility, and adaptation.
3. Apply platform-specific guidance over generic advice. A watch interaction is not a smaller phone screen; a Mac command is not necessarily a touch target.
4. Label conclusions **Apple guidance**, **implementation interpretation**, or **needs verification**. A local rule ID is a project identifier, not an Apple rule number. HIG recommendations are not automatically App Store requirements.
5. Follow the source links for disputed, numeric, or version-sensitive claims. The registry records a dated review, not a guarantee of current behavior. If current documentation is unavailable, use the snapshot cautiously and mark uncertainty.
6. Preserve functionality and user state across layout changes. Prefer rearranging or revealing content over removing access to it.
7. Respect existing deployment targets and architecture. Check both SDK support and runtime availability before introducing APIs. Do not import another skill's stylistic preferences as HIG requirements.
8. Keep the scope narrow enough to verify. Do not rewrite data, concurrency, persistence, or networking code unless necessary for the interface task.

## Deliver

For a finding, include the affected file/line or screen, observed issue, user impact, applicable platform, rule/source, focused correction, and validation status. Use the severity guidance in [review-validation.md](references/review-validation.md). Separate confirmed findings from questions; omit unsupported accusations and praise-only findings.

For implementation, explain the resulting behavior and report checks actually performed. When useful, use [examples](references/swiftui-implementation.md#original-examples) as small starting points, not an app template.

State remaining runtime/device checks. Never equate compilation, a screenshot, or an accessibility audit with complete HIG compliance. Do not claim experience as an Apple employee or knowledge of undocumented Apple policy.
