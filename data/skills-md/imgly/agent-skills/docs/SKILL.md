---
name: docs
description: |
  Look up IMG.LY SDK (CE.SDK) docs: guides, API signatures, config options, setup and
  licensing for Web, Swift, Android, Flutter and React Native. Use for "how do I…" or
  exact-API questions about an existing CE.SDK integration.
argument-hint: "[search-topic]"
---

## Version Notice

> CE.SDK `1.85.2` · generated `2026-11-03` · plugin `imgly-sdk`
> · canonical update source `imgly/agent-skills`.
>
> If this bundle is over six weeks old, or the user asks about updates, follow
> `references/update-check.md` once per task and reuse the result for all CE.SDK
> skills. Keep the check read-only. Never install, update, overwrite, or delete
> anything without explicit user approval. Continue with this bundle unless an
> update is approved.

# CE.SDK Documentation

**Query**: $ARGUMENTS

Covers Web (React, Vue.js, Svelte, Angular, Electron, Vanilla JavaScript, Node.js, Nuxt.js, Next.js, SvelteKit); Flutter (Dart) on iOS and Android; React Native (TypeScript) on iOS and Android; Swift on iOS, macOS, and Mac Catalyst; Kotlin and Jetpack Compose on Android.

## Platform Detection

Detect the platform from the project files, then read the matching reference folder.

| Project files | Platform | Reference folder |
|---------------|----------|------------------|
| `pubspec.yaml` (its `android/` and `ios/` folders belong to the Flutter app) | Flutter (Dart; native editor on iOS and Android) | `references/flutter/` |
| `react-native` in `package.json` dependencies (its `android/` and `ios/` folders belong to the React Native app) | React Native (TypeScript; native editor on iOS and Android) | `references/react-native/` |
| `Package.swift`, `*.xcodeproj`, or `*.xcworkspace` | Swift (iOS, macOS, Mac Catalyst) | `references/swift/` |
| `build.gradle`, `build.gradle.kts`, or `settings.gradle*` | Android (Kotlin, Jetpack Compose) | `references/android/` |
| `package.json` | Web — pick the framework from its dependencies (table below) | `references/web/<framework>/` |

Match the rows in the order listed. A Flutter or React Native project also
holds `android/` and `ios/` folders, and a React Native project lists
`react` in `package.json`; those files belong to the wrapper app, so its row
wins over the Swift, Android, and Web rows.

### Web framework from `package.json` dependencies

Check in this order: `react-native` → React Native (the row above, not Web), then `next` → Next.js, `nuxt` → Nuxt.js, `@sveltejs/kit` → SvelteKit,
`@angular/core` → Angular, `svelte` → Svelte, `vue` → Vue.js, `react` → React,
`electron` → Electron, `@cesdk/node` or a server project → Node.js, none → Vanilla JS.

| Framework | Reference folder |
|-----------|------------------|
| React | `references/web/react/` |
| Vue.js | `references/web/vue/` |
| Svelte | `references/web/svelte/` |
| Angular | `references/web/angular/` |
| Electron | `references/web/electron/` |
| Vanilla JavaScript | `references/web/js/` |
| Node.js | `references/web/node/` |
| Nuxt.js | `references/web/nuxtjs/` |
| Next.js | `references/web/nextjs/` |
| SvelteKit | `references/web/sveltekit/` |

A monorepo with several of these files or an empty folder is ambiguous: **ask the user which platform and framework to target**
instead of guessing. Never mix content from two platforms in one answer, except
that a Flutter or React Native answer adds the Swift and Kotlin code its native
mapping calls for.

## How to Use

1. Detect the platform and framework as above.
2. Read `README.md` in the matching reference folder. It holds the lookup
   workflow, the API index, and the agent rules for that platform. The page
   index of the docs site (`<platform>.md`) sits beside it.
3. Follow that workflow: pick pages from the index and fetch them from the docs
   site as Markdown, or read the bundled API digests.
4. Answer with the relevant section and code examples. Verify types and package
   names against the fetched pages and the API digests, never against memory.

## Related Skills

- Use `/imgly-sdk:build` when the user needs implementation help, not just docs
- Use `/imgly-sdk:explain` for conceptual explanations beyond what docs cover
