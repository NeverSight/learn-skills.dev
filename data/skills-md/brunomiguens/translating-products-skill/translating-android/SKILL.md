---
name: translating-android
description: Use when localizing Android resources and UI copy for strings.xml, plurals, Compose, views, TalkBack, pseudo-locales, and bidirectional layouts.
---

# Translating Android

## Overview

Define the Android resource, formatting, and UI contract around localized copy. Preserve resource identity and executable syntax while routing wording to core and installed language or script specialists.

Do not create target copy until the orchestrator confirms project setup and approval. This skill owns Android engineering semantics, not linguistic decisions.

## Capabilities

- `platform:android`
- `string-resources`
- `compose`
- `android-locales`

## Inspect Resources and Consumers

Inspect the base `res/values` resources, every relevant locale qualifier, Gradle/resource configuration, and the Compose or XML call sites that consume them:

- inventory resource name, type, file, locale, screen, component, state, developer comment, and fallback path
- record positional placeholders, types, examples, markup, escapes, XLIFF annotations when used, plural quantity semantics, and protected values
- find user-facing literals in Kotlin, Java, Compose, XML layouts, menus, notifications, widgets, and accessibility properties
- distinguish visible text, TalkBack name/hint/state/announcement, developer-only text, and values deliberately marked `translatable="false"`
- record supported device classes, width/height constraints, font scaling, and LTR or RTL layout behavior

Never infer meaning from a resource name alone. Send complete phrases and context to `translating-core`; preserve Android syntax while installed language specialists choose grammar and word order.

## Preserve the Resource Contract

Keep resource names and types, positional placeholder indices and types, markup topology, protected identifiers, URLs, product facts, and runtime data unchanged. Allow target text to reorder numbered string or integer format arguments; never replace them with translated names or unnumbered concatenation.

Keep non-user-facing constants such as endpoints in the base resources with `translatable="false"`; do not create locale copies. Confirm the value remains byte-equivalent where exact identity matters. Mark user-facing copy non-translatable only through an explicit product decision, not to silence missing-localization work.

Keep `strings.xml` well-formed and valid for Android resource parsing. Preserve required escapes and inline markup; escape XML-significant characters such as an ampersand in text, and test that styled spans render after formatting. Do not “fix” markup by flattening it or allow a translated placeholder to cross an invalid tag boundary.

In XML views, use Android string-resource references. In Compose, use `stringResource` or the corresponding resource API instead of hardcoded literals. Resource TalkBack descriptions too; use the platform's decorative/no-description behavior when an image conveys no additional meaning.

## Plurals and Quantity Semantics

Use `<plurals>` for grammatical quantity messages. The `quantity` argument selects the target-locale branch; it is not automatically inserted into output. Pass the count again as a formatting argument when the message includes it, using `getQuantityString` or Compose `pluralStringResource` with the correct argument order.

Describe what the count measures and its valid range. Provide the quantity categories required by the target locale and shipped Android/CLDR behavior, always including a valid `other`; do not mirror English branches or hand-code `count == 1`. Preserve placeholder schema in every applicable item and test target-locale boundary values, including zero and larger counts.

## Locale-Aware Formatting

Format numbers, dates, currency, units, and lists with Android/Java locale-aware APIs under the active app locale and an explicit business-owned currency or unit contract. A locale changes presentation, not which currency was charged. Do not concatenate symbols, labels, or separately localized fragments, and do not use a literal `$` unless the approved fact is specifically USD.

Keep the formatted value as a typed/opaque substitution inside one complete localizable message so target grammar can reorder it. Test sign, precision, grouping, decimal separators, spacing, and mixed-direction output.

## Layout, TalkBack, and RTL

- Replace physical left/right layout and padding rules with logical start/end where direction should follow the locale. Audit both XML constraints and Compose layout/alignment.
- Mirror directional navigation or progression imagery through supported Android behavior; do not mirror universally meaningful media, clock, brand, or other non-directional imagery without an explicit design rule.
- Test actual RTL with mixed Arabic/Hebrew text, Latin identifiers, placeholders, punctuation, digits, and currency. Route bidirectional decisions to the installed script specialist rather than inserting control characters by guesswork.
- Test TalkBack role, accessible name, state, value, hint, announcement timing, traversal/focus order, touch target, and dynamic updates. Visible and spoken actions must preserve the same meaning.
- Test compact and expanded screens, phones and supported larger/foldable devices, orientations or window sizes, maximum supported font scale, display size, and input/keyboard states.

## Pseudo-Locales and Fallback

Run the Android pseudo-locales `en-XA` for expansion/accent pressure and `ar-XB` for forced RTL/bidirectional pressure in a debuggable or test configuration. Exercise screenshots, navigation, formatted values, placeholders, plurals, markup, and TalkBack. Pseudo-locales validate engineering and are never target translations.

Do not copy English text into a target locale directory to make completeness checks pass. Missing target content must follow the approved fallback policy and remain detectable; unintended source-language or mixed-language customer output blocks release.

## Targeted Research

Use project configuration and pinned Android, Unicode, and CLDR-derived knowledge first. Research only a specific unresolved current Android/platform detail that affects the artifact, using authoritative documentation and recording the decision through the orchestrator. Do not browse for ordinary wording or grammar, and never install another skill at runtime.

## Authority Boundary

Explicit user requirements, approved project configuration, and semantic fidelity outrank Android convenience. Product owns meaning; engineering owns resource/build, value, and fallback contracts; accessibility ownership supplies interaction intent.

This skill owns Android resource classification, syntax, formatting, layout, and platform QA. `translating-core` owns target copy; language and script specialists own linguistic mechanics; `translating-mobile` owns shared mobile constraints; `reviewing-translations` owns final review.

## QA Handoff and Release Gates

Always perform file and structural checks, including:

- compile resources and lint all shipped variants; compare resource names/types, placeholders, plural schemas, markup, escapes, protected values, and `translatable="false"` policy
- execute every plural branch and representative formatted value under the target locale
- verify Compose and XML contain no unintended user-facing literals or physical-direction assumptions
- detect raw keys, copied-English targets, malformed resources, and accidental mixed-language target files

Perform the following runtime checks only after the orchestrator supplies a resolved `run` decision. Use the smallest relevant runtime scope for the affected resources and states; do not independently choose the runtime-review budget or expand it to the whole application:

- run `en-XA`, `ar-XB`, target-locale screenshots, TalkBack, font-scale, window-size, and RTL interaction tests
- detect unintended fallback, accidental mixed-language output, clipping, overlap, or inaccessible controls in rendered states

Pass base and target resources, call-site inventory, locale/build/device matrix, available screenshots, accessibility intent, and applicable results to `reviewing-translations` and CI.

Always block release on resource compile/lint failure; missing, renamed, or corrupted resources; placeholder/plural/quantity damage; invalid escapes or markup; altered protected constants; or hardcoded or incorrectly formatted values. When runtime review runs, also block on unintended English fallback, TalkBack meaning loss, start/end or RTL defects, or required content hidden by layout. Route the exact resource, consumer, configuration, and evidence to its responsible installed skill.
