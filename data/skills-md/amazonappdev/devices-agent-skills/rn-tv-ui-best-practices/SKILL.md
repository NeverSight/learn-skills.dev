---
name: rn-tv-ui-best-practices
description: React Native TV UI best practices for tvOS, Android TV, Fire TV, and Vega OS (covers react-native-tvos and @amazon-devices/react-native-kepler). Use when reviewing or building TV UI — focus management (TVFocusGuideView, hasTVPreferredFocus, trapFocus, FocusManager, Navigable, useTVEventHandler), D-pad / RCU navigation, swimlanes, hero banners, drawers, tabs, modals, overscan/safe zones, TV typography & contrast, HDR, and remote-driven text or voice input.
---

# React Native TV UI Best Practices

This skill helps an agent review or build React Native TV UI across tvOS, Android TV, Fire TV, and Vega OS. Use it when the user asks to audit a TV app, fix focus or D-pad issues, or build common TV components (swimlanes, hero banners, drawers, tabs, modals, focus traps, search/auth flows). The references cover focus management, layout patterns, typography & contrast, input handling, and Vega-specific gotchas — pick the relevant one rather than reading them all. Anything that requires a TV at viewing distance (overscan, contrast under HDR, animation feel, 10-foot legibility) the agent flags for human verification rather than performing.

**TV UX differs from mobile in ways the agent should keep in mind across every reference.** Users sit ~10ft from the screen with a 9-button remote — no touch, no gestures. Focus moves along directional axes; navigation is linear. Type that's legible at phone distance is invisible at couch distance. Pure black/white looks sharp on a phone but blooms on HDR TVs. Animations carry meaning (signalling focus or direction) rather than decorating a touch. The reference files apply these constraints to specific surfaces — focus, layout, typography, input — so the agent doesn't need to reason about TV-vs-mobile differences each time.

## Check before applying rules

1. **Runtime.** `package.json` will list `react-native-tvos` (→ tvOS + Android TV) or `@amazon-devices/react-native-kepler` (→ Vega). A monorepo may have both, scoped per package.
2. **Confirm it's a TV app.** No `Platform.isTV` and no TV runtime in deps → skill doesn't apply.

For Vega, defer to the live Amazon docs for API specifics. This skill only covers the non-obvious cross-runtime gotchas — see [`vega-specifics.md`](references/vega-specifics.md).

## Static helper

`node references/scripts/audit.js src` runs grep-style checks across all four sections (focus, input, layout, typography). Section selectable via `--only` / `--skip`. Zero deps, exits 1 on findings.

It's a helper, not a full review. It only catches statically detectable patterns — most rules in the reference files require judgement, hardware, or human review and won't be caught regardless of how clean the audit runs. Read each match in context.

## References

| Topic                                                          | File                                                          |
| -------------------------------------------------------------- | ------------------------------------------------------------- |
| Focus & D-pad navigation                                       | [navigation-and-focus.md](references/navigation-and-focus.md) |
| Vega gotchas + links to Amazon docs                            | [vega-specifics.md](references/vega-specifics.md)             |
| Drawers, tabs, modals, swimlanes, hero, safe zones, transition motion | [layout-patterns.md](references/layout-patterns.md)    |
| Font sizes, contrast, HDR, ambient light                       | [typography-and-color.md](references/typography-and-color.md) |
| Remote model, `TextInput`, search, login, voice, QR auth       | [input-handling.md](references/input-handling.md)             |

## Decision tree

```
Focus / navigation
├─ Pick the right mechanism            → navigation-and-focus.md
├─ Initial focus wrong                 → navigation-and-focus.md
├─ Focus jumps unexpectedly            → navigation-and-focus.md
├─ Modal/overlay leaks focus           → navigation-and-focus.md
├─ Back button doesn't restore focus   → navigation-and-focus.md
├─ Move focus programmatically         → navigation-and-focus.md
└─ Cross-platform differences          → vega-specifics.md + navigation-and-focus.md

Vega project? → vega-specifics.md FIRST.

Building screens
├─ Drawer / tabs / modals              → layout-patterns.md
├─ Cards / rows / swimlanes / hero     → layout-patterns.md
└─ Safe zones / aspect ratios          → layout-patterns.md

Visual design
├─ Typography                          → typography-and-color.md
├─ Color / contrast                    → typography-and-color.md
├─ HDR / ambient light                 → typography-and-color.md
├─ Focus / press animation             → navigation-and-focus.md (Motion and feedback)
└─ Drawer / modal / page transitions   → layout-patterns.md (Transition motion)

Input
├─ Remote model / button vocabulary    → input-handling.md (Remote interaction model)
├─ Reduce typing                       → input-handling.md
├─ Pick keyboardType                   → input-handling.md
├─ Voice                               → input-handling.md
└─ QR / companion-app pattern          → input-handling.md
```

## Output style

When showing code or recommending a fix:

- Name the runtime it targets (`react-native-tvos` or Vega via `@amazon-devices/react-native-kepler`).
- Note platform availability for any non-universal API.
- Link to the relevant reference section so the user can read further.
- Don't claim a hardware-required check is done — flag it for human verification (see below).

## Hand off to the human reviewer

Some checks require real hardware at viewing distance: overscan crop, focus-indicator visibility under ambient light, animation feel, contrast under HDR, 10-foot legibility. The agent cannot verify these.

When finishing a review or build, surface a checklist of human-verification items to the user. Each reference file ends with a _Hand off to the human reviewer_ section; pull from those. Frame items as outstanding work, not completed checks.

## Attribution

Based on _The Ultimate Guide to React Native TV Development_, co-authored by Amazon and Callstack — <https://www.callstack.com/ebooks/the-ultimate-guide-to-react-native-tv-development>.

Authors: Giovanni Laquidara ([@giolaq](https://github.com/giolaq)), Karol Latusek ([@Zahoq](https://github.com/Zahoq)), Anisha Malde ([@anishamalde](https://github.com/anishamalde)), Michal Pierzchala ([@thymikee](https://github.com/thymikee)).
