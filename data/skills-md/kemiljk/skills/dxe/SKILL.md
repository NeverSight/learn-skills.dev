---
name: dxe
description: "Review a repository or UI surface for design engineering quality. Use for a DXE pass or broad interface review; fix only when requested and load specialist guidance from evidence."
license: MIT
---

# dxe

Review interface work in this precedence order:

1. Intent before decoration.
2. Correct semantics and accessibility before visual convenience.
3. Interaction feel before implementation technique; use the most native implementation that preserves the intended feel.
4. Production trust before prototype cleverness.

Read [references/dxe-core.md](references/dxe-core.md) before starting. It is the shared rubric for every mode. Do not load every sibling skill by default.

## Modes

Infer the mode from the request; use `review` when unspecified.

A path after `dxe` scopes any mode to that path. Treat “apply all skills” as `dxe exhaustive`.

| Mode | Scope | Mutation |
| --- | --- | --- |
| `dxe quick` | Shared rubric on one representative surface; load no sibling unless essential | No |
| `dxe` / `dxe review` | Full evidence matrix and representative repo sampling; progressively load triggered siblings | No |
| `dxe fix` | Review, then implement and verify bounded high-confidence fixes | Yes, within the requested scope |
| `dxe exhaustive` | Inspect every available surface and read the full sibling suite | No unless the user also asks to fix |

Review mode is strictly non-mutating. Do not edit files, install dependencies, start external mutations, or change production systems. Read-only inspection and local verification are allowed. In fix mode, preserve unrelated work and existing design-system materials.

## Scope and sampling

Identify the repository or paths, primary user tasks, stack, tokens, primitives, and interaction/runtime libraries. Prefer existing materials over invented replacements.

For a repository review, select representative surfaces rather than implying equal inspection of every screen:

- primary landing or task page;
- content/detail and list/index pages when present;
- one form or mutation flow;
- one overlay, dialog, or menu;
- an available loading, empty, or error state;
- primary and contrasting target form factors, relevant input methods, and reduced-motion variants.

State omissions in the report. In exhaustive mode, enumerate all discoverable surfaces and states before inspection.

## Evidence protocol

Write a short hypothesis and non-goals, then collect the minimum evidence appropriate to the mode. For normal review/fix, record:

| Evidence | Minimum |
| --- | --- |
| Materials | Stack, tokens, primitives, motion/runtime libraries |
| Source | Representative routes and shared components |
| Verification | Existing typecheck/tests and production build, when safe and available |
| Form factors | Rendered primary and contrasting layouts, clipping/overflow, and task hierarchy |
| Interaction | First meaningful input sequence; overlay/menu/sheet state, return, and touch/pointer/keyboard parity where relevant |
| Accessibility | Platform names, roles/traits/semantics, states, focus/return, and reduced motion |
| Production | Loading/error/empty behaviour, platform metadata, and platform-specific runtime logs |
| Confidence | `confirmed-rendered`, `confirmed-source`, `likely`, `unverified`, or `environment-only` |

Do not claim a rendered defect from source inspection alone. If rendering or a check is unavailable, label the limit instead of guessing.

Separate observations into:

1. confirmed product defects;
2. source-level risks;
3. environment or tooling failures;
4. unverified suspicions.

Reproduce a user-facing failure before promoting tooling noise to a product finding. Distinguish browser errors, server errors, expected local-service failures, and framework/tooling warnings.

For checks that trigger a state change, wait for an observable settled condition before recording state. Prefer the target platform accessibility/semantics value, focus destination, transition completion, or animation settlement over an arbitrary delay. Do not report the immediate post-action sample as final evidence when rendering or animation is still in flight.

Choose the verification lane that matches the delivered platform:

| Platform | Required runtime evidence |
| --- | --- |
| Web | Browser `console.error`, uncaught `pageerror`, server logs, responsive overflow, keyboard sequence |
| Apple native | Xcode build/tests when available, simulator/device diagnostics, accessibility inspection, Dynamic Type, target form factors |
| Android native | Gradle build/tests when available, Logcat errors/fatals, semantics/TalkBack checks, font scale, target window sizes |

## Compact cross-phase pass

Consider every phase, but do not manufacture a finding for each one.

### Intent

- State what the interface helps the user accomplish.
- Mark duplicate actions, unexplained chrome, and generated residue for removal.
- Preserve elements whose purpose is clear and useful.

### Platform

- Prefer native elements and state contracts over `div` plus ARIA reconstructions.
- Check navigation/focus order, names, roles, states, disabled behaviour, and form participation.
- Prefer native CSS/HTML where it can express the behaviour without weakening it.

### Feel

- Check input discoverability across keyboard, touch, and fine pointers.
- Motion should be responsive, interruptible where needed, and have a reduced-motion path.
- Delight should improve anticipation, reliability, or care—not add novelty without purpose.

### Bridge

- Check that design structure maps deliberately to code, tokens, primitives, rendering, and accessibility.
- Flag one-off values or abstractions that fight the existing system.

### Shipping

- Exercise relevant loading, empty, error, auth, validation, focus, metadata, and repeat-use paths.
- Separate prototype shortcuts from confirmed release risks.
- Look for tests around critical contracts rather than requiring blanket coverage.

## Progressive sibling routing

Load a sibling `SKILL.md` only when the materials map, initial evidence, or requested depth triggers it. Collection siblings are installed adjacent to this skill, so first resolve `../<skill-name>/SKILL.md` before treating a lens as unavailable. If a sibling exists and is readable, use its content even when this session’s discovery registry omits it. A registry refresh is needed only to expose it as a separately invocable skill, not to continue the current pass. If neither discovery nor the adjacent path provides a readable skill, continue with the shared rubric, disclose the missing lens, and avoid inventing its detailed guidance.

| Trigger | Read |
| --- | --- |
| Product intent is unclear or decisions need rationale | `dxe-write-first-design` |
| Decorative, redundant, or cognitively heavy UI | `dxe-subtractive-design` |
| A Danish functionalist design lens is requested | `dxe-humane-functionalism` |
| A Maslow-inspired needs lens or needs-based prioritisation is requested | `dxe-software-needs-hierarchy` |
| Web forms, menus, dialogs, custom controls, or semantic failures | `dxe-semantic-html-first` |
| Web responsive layout or CSS/HTML implementation questions | `dxe-modern-css-html` |
| SwiftUI, UIKit, AppKit, Xcode, or Apple-platform UI | `dxe-apple-native-ui` |
| Kotlin, Android Gradle, Jetpack Compose, Android Views, or Compose Multiplatform | `dxe-android-native-ui` |
| Gestures, springs, interruption, or shared-element motion | `dxe-fluid-design` |
| Weak discoverability, hover-only actions, or input mismatch | `dxe-interface-affordances` |
| A specific opportunity for useful polish | `dxe-product-delight` |
| Design/code structure or token translation is breaking down | `dxe-design-engineering` |
| Consequential interaction behaviour is unspecified or inconsistent | `dxe-interaction-contracts` |
| A shared component or token model needs a compatibility or migration decision | `dxe-design-system-evolution` |
| Recurring setup, waiting, or interruption makes repeated work costly | `dxe-design-for-repetition` |
| Placeholder or uniform content obscures hierarchy or layout decisions | `dxe-real-content-design` |
| Template-like or AI-generated residue needs judgement | `dxe-ai-output-judgement` |
| Auth, validation, state, resilience, or release concerns | `dxe-prototype-to-production` |

`dxe exhaustive` is the only mode that requires reading every sibling skill in the routing table.

## Severity and confidence

- **Critical:** blocks a primary task, risks data/security loss, causes a confirmed serious accessibility failure, or breaks production rendering.
- **Should fix:** confirmed damage to comprehension, navigation, semantics, resilience, or trust with a bounded correction.
- **Nice to have:** polish, consistency, dormant primitive risk, or non-blocking cleanup.

Every finding must include one confidence tag. Never classify `unverified` or `environment-only` observations as Critical. Quote only the smallest useful source snippet and anchor findings to a path or rendered surface.

## Report

```markdown
# dxe pass — [scope]

## Hypothesis
## Evidence collected
## Verified strengths
- [skill or core] path/surface — what should be preserved

## Findings
### Critical
- [confidence] [skill or core] path/surface — issue — bounded fix
### Should fix
### Nice to have

## Cuts
## Proposed changes
## Verification status
## Limits and unresolved observations
```

Verified strengths are evidence, not consolation: record systems that work and should survive later changes. An empty severity section is acceptable. Findings should never be failure quotas.

## Verification recipe

When tools and repository scripts permit:

1. Run the existing typecheck, tests, and production build.
2. Render the primary target and one contrasting viewport, window, device, or form factor.
3. Check clipping/overflow, safe areas/insets, and primary task hierarchy as the platform requires.
4. Record the first meaningful keyboard, touch, pointer, remote, or assistive-technology sequence.
5. Exercise one menu, dialog, sheet, or navigation transition; wait for settled state, then verify state and focus/return.
6. Repeat one motion-bearing task with reduced motion; wait for settlement before recording animation state or counts.
7. Capture the platform's runtime errors: browser `console.error`/`pageerror`, Apple simulator/device diagnostics, or Android Logcat errors/fatals. Classify them separately from tooling noise.
8. In fix mode, repeat affected checks and report exact results.

Never mutate production or external systems as part of a review.

## Done when

- Scope, hypothesis, non-goals, sampling, and limits are explicit.
- Every phase was considered; only triggered sibling skills were loaded.
- Claims are tied to evidence, severity, confidence, and a path or surface.
- Confirmed product defects are separated from tooling noise and suspicions.
- Existing strengths and subtractive cuts are recorded when warranted.
- Fixes, when authorized, are bounded and verified in proportion to risk.
