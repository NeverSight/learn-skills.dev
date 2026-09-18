---
name: expo-native-builder
description: Build or improve polished Expo and React Native screens and flows while preserving the user's requested screens, file structure, styling system, navigation, product logic, and visual direction. Use for direct Expo UI implementation, including onboarding and paywalls.
---

# Expo Native Builder

## Preserve the request first

Before proposing anything, extract the user's required screens, behavior, visual direction, file locations, references, and exclusions. Treat every explicitly named screen or feature as required. A supplied implementation plan overrides this skill's defaults. Do not replace the requested journey with a generic template.

Inspect the existing routes, components, tokens, assets, fonts, dependencies, and business logic before choosing an architecture. Preserve working conventions. Ask only for a missing decision that materially changes the result.

For a new multi-step onboarding flow, start from this compact structure and adapt it to the user's names:

```text
src/
|-- app/
|   `-- (onboarding)/
|       |-- _layout.tsx
|       |-- welcome.tsx
|       |-- [step].tsx
|       |-- pledge-result.tsx   optional named route
|       |-- building.tsx        when a plan/result is generated
|       |-- plan.tsx            detailed result
|       |-- paywall.tsx         when monetization is in scope
|       `-- offer.tsx           optional eligible offer
`-- components/
    `-- onboarding/
        |-- steps.ts
        |-- state.tsx
        |-- step-renderer.tsx
        `-- <focused step components>.tsx
```

Keep `[step].tsx` small: route validation, step lookup, progress, navigation, and the renderer call. Put substantial step bodies and interactions in `src/components/onboarding`; do not leave one giant route that is hard to test or debug. Do not restructure an existing project merely to match this example.

Before editing, show at most five short bullets covering scope, direction, files, dependencies/assets, and verification. Wait for confirmation, then implement only that scope.

## Detect the styling system

Inspect `package.json`, Metro/Babel configuration, global styles, generated types, root imports, and existing screens. Use Uniwind when the running app is configured for Uniwind, NativeWind when its configuration is active, and StyleSheet when the project uses React Native styles or theme objects. If packages overlap, follow the system used by the working screens. Never introduce, mix, or migrate styling systems unless the user requests it.

## Use the existing design system

- Reuse semantic tokens, typography, components, icons, radii, and spacing.
- Use the existing package manager and installed compatible libraries.
- Preserve navigation, data flow, authentication, backend contracts, and platform behavior.
- Use realistic populated local states when production data is unavailable, and identify what must later connect to real sources.

Use a plain semantic surface, an image, or a restrained gradient according to the user's direction, supplied reference, existing design system, and product character. A gradient is allowed when the AI judges it appropriate, but it is never mandatory or an automatic definition of premium. Keep controls solid unless a gradient control is explicitly intended. Read [references/gradient-background.md](references/gradient-background.md) only when a gradient is chosen.

## Load only relevant guidance

- For welcome screens, onboarding, personalization, generated plans, paywalls, or offers, read [references/onboarding-paywall.md](references/onboarding-paywall.md).
- For native layout, controls, safe areas, keyboard behavior, tabs, sheets, or pickers, read [references/native-ui.md](references/native-ui.md).
- For custom content animation, gestures, animated values, or motion packages, read [references/motion-native.md](references/motion-native.md).
- Before expanding shared UI, read [references/reusable-components.md](references/reusable-components.md).

Do not automatically load another skill. Use these references through progressive disclosure.

## Enforce a complete screen shell

Every route needs a full-height semantic root using the project's `Screen` or `react-native-safe-area-context`, never React Native's deprecated `SafeAreaView`. Apply only edges not already owned by a header, tab bar, sheet, or navigator. Keep full-bleed backgrounds and media outside the safe-area content layer. Choose `ScrollView`, `FlatList`, or `SectionList` from actual content and virtualization needs, and pad content above pinned actions and the home indicator.

## Build native-quality screens

- Give each screen one dominant purpose and primary action.
- Use `Pressable` feedback intentionally.
- Keep touch targets at least 44 points, support Dynamic Type and screen readers, and never rely on color alone.
- Reuse components before adding abstractions; extract feature components when they isolate meaningful behavior or keep a route readable and testable.

For controls with interaction physics, check existing primitives, Expo/React Native APIs, installed dependencies, and maintained compatible packages before hand-building. Ask before installing. Prefer:

`existing primitive -> built-in API -> installed dependency -> focused package -> custom`

## Design every relevant state

Implement every reachable state relevant to the requested screen: loading, populated, empty, error, disabled, selected/pressed, offline, and success. Keep field errors beside their controls, preserve input after recoverable failures, and block duplicate submissions while pending. When production data is unavailable, use believable centralized fixtures so the completed UI can be seen and tested; never leave important charts, plans, prices, trials, ratings, testimonials, dates, messages, or results blank. Never display `mock`, `sample`, or placeholder warnings inside the product.

## Use real artwork assets

When missing artwork would materially improve a screen, ask early whether the user has an illustration or wants a generation prompt; identify the screen, purpose, and filename. Bundle related asset requests and continue independent UI work while awaiting assets. Keep recurring characters and poses in one consistent visual family. Distinguish UI animation, movement of an existing still, and animation within the artwork; only the last needs an animated asset. Do not postpone this conversation until final handoff.

Inspect existing assets first. When a welcome, onboarding reveal, plan, paywall, celebration, or empty state needs custom illustration or artwork, do not invent a complex replacement from JSX, SVG paths, emoji, or CSS-like shapes. Build a correctly sized replaceable image/video slot and finish the surrounding UI.

Give the user a ready-to-paste prompt and filename to generate the artwork in ChatGPT Images or their preferred image tool. Carry the approved visual style into the prompt and specify subject, composition, palette, dimensions/aspect ratio, and a transparent background when the asset must layer over the app; otherwise name the intended background. When the concept needs animated artwork, specify the still/key art first, then give the user a short motion prompt and target video or GIF format for an approved animation tool such as Gemini. Do not claim the asset exists until it is generated and inspected; use a simple temporary visual only when needed to keep the screen runnable. In the final handoff, list every temporary slot with its filename and generation prompt.

## Motion contract

This skill works independently of `mobile-ui-design` or any design document. Follow an approved design when available; otherwise choose the welcome pattern, paywall story, artwork needs, and motion behavior from the product and existing app. Use the reference recipes as adaptable defaults, not mandatory effects or a fixed journey.

Before implementation, include a compact motion specification in the existing scope summary or project design notes: `moment -> trigger -> moving elements / fixed anchors -> timing or spring -> settled state -> interruption / replay -> Reduce Motion`. Implement and verify it; generic fades on every screen do not substitute for meaningful product demonstrations and feedback.

Motion is a required design material for polished onboarding and high-value product moments. Use the installed Reanimated, Gesture Handler, and haptics setup where appropriate. Create original product-specific feedback, explanation, continuity, state change, and completion motion; the absence of a motion reference is not a reason to leave the flow static. Motion must remain purposeful rather than animating every container.

For onboarding, always set the nested Expo Router Stack to `animation: "none"`. Do not animate the route or whole step screen. Each screen choreographs its own internal content: illustration, headline, supporting copy, choices, metrics, charts, progress states, and CTA. Keep controls available immediately, avoid replaying settled content, and provide Reduce Motion behavior that presents the final state without travel or delay.

## Verify visually and functionally

Run relevant typecheck/lint checks, start Expo, and inspect at least one available target. Exercise navigation, Back behavior, keyboard, safe areas, compact screens, Dynamic Type, relevant states, and Reduce Motion. Record motion changes and inspect for flashes, jumps, clipped content, stale values, and broken hit targets.

Run a mechanical anti-template check: normally one accent family, one neutral family, one approved radius scale, zero unexplained gradients/glass/glow, zero emoji used as interface icons, and one consistent label for each repeated action. Fix every accidental violation; keep an exception only when the user, product, or established brand system requires it.

Build success does not prove visual quality. If no native, device, web, or static visual inspection is available, report the UI as visually unverified. Keep the final handoff concise and list every representative value, formula, price, trial, date, rating, claim, permission, offer, analytics event, purchase action, or backend state still awaiting a production source. Ask whether the user wants to connect the real backend/store catalog and replace those fixtures next.

## Pledge and result handoff

For a fingerprint pledge, plan building, or a result leading into purchase, read both motion and onboarding-paywall references even when the task covers only that moment. Implement the approved design's visual phases and motion states when supplied. Without a design document, choose them using this skill's own defaults; never require another skill to proceed.
