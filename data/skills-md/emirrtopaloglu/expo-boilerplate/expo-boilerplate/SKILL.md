---
name: expo-boilerplate
description: >
  Interactive Expo project bootstrapper. Use when a user wants to start a new Expo/React Native project from scratch
  and needs help making architecture decisions and setting up the project structure. This skill guides the user through
  15 decision categories (project basics, folder structure, design system, state management, navigation, API/network,
  libraries, authentication, CI/CD, testing, code standards, performance, security, analytics, offline-first) by asking
  targeted questions, then scaffolds the complete project structure so the user can immediately start adding features.
  Triggers on: "new expo project", "expo boilerplate", "start expo app", "expo setup", "bootstrap expo", "expo initialization",
  "from scratch expo", "setup expo architecture".
---

# Expo Boilerplate Skill

> **Target:** Expo SDK 53+ / React Native 0.79+

Interactive bootstrapper that collects architecture decisions via questions, then scaffolds a production-ready Expo project.

## References

```
references/
  questions.md                All questions grouped into 3 tiers with defaults
  setup-guide.md              Package commands, config files, and boilerplate code
  architecture-templates.md   Folder structures and complete file contents
```

## Workflow

### Phase 0: Initialize Project

Before anything else, create the Expo project if it doesn't exist:

```bash
npx create-expo-app@latest {{APP_NAME}} --template blank-typescript
```

### Phase 1: Collect Decisions

Read `references/questions.md`. Ask questions **one tier at a time**:

**Tier 1 — Required (always ask):**

1. Project Basics — name, bundle ID, platforms, workflow
2. Folder & Architecture — feature-based vs domain-based
3. State & Data — global state, server state, persist storage
4. Navigation — tabs, drawer, auth flow, deep linking
5. API & Network — REST/GraphQL, client, token management

**Tier 2 — Recommended (ask "Would you like to make recommended architecture decisions?"):** 6. Design System — colors, typography, spacing, UI kit 7. Authentication — methods, backend provider, token storage 8. Libraries — forms, animation, image, i18n, date 9. CI/CD & Deploy — EAS, build profiles, OTA channels 10. Testing — unit, E2E, coverage target

**Tier 3 — Advanced (ask "Would you like to make advanced decisions, or use defaults?"):** 11. Code Standards — naming, lint, commit format, branch strategy 12. Security — root detection, SSL pinning, log filtering 13. Analytics & Logging — provider, crash reporting 14. Offline First — cache strategy, sync mechanism

> **Shortcut:** If user says "fast setup" or "use defaults", apply **Recommended Defaults** from `questions.md` and only ask project name + bundle ID.

### Phase 2: Summarize & Confirm

Show all decisions as a summary table and get user approval:

```
| Category | Choice |
|----------|--------|
| App Name | MyApp |
| State    | Zustand |
| ...      | ...    |
```

### Phase 3: Scaffold Project

After approval, read `references/setup-guide.md` and `references/architecture-templates.md`, then:

1. **Install packages** — run `npx expo install` and `npm install` for selected libraries
2. **Create folder structure** — directories and files per template
3. **Write config files** — `tsconfig.json`, `.eslintrc.js`, `.prettierrc`, `app.json`, `eas.json`, `.gitignore`
4. **Set up design system** — theme tokens in `src/theme/`
5. **Create state stores** — boilerplate store files per selected state manager
6. **Set up navigation** — Expo Router layouts in `app/`
7. **Set up API client** — base URL, interceptors, error handler
8. **Set up auth flow** — login/register screens, token storage, protected routes
9. **Create demo screen** — `app/(tabs)/index.tsx` showing design system
10. **Set up error handling** — ErrorBoundary, splash screen, font loading

### Phase 4: Completion Report

Show the user:

- ✅ Created files/directories list
- 🚀 Start command (`npx expo start`)
- 📋 Next steps (how to add your first feature)
- ⚠️ Manual steps if needed (Apple Developer account, Firebase config, etc.)

## Important Rules

- Follow **building-native-ui** skill conventions (kebab-case files, expo-image, expo-router)
- Use **ui-ux-pro-max** skill when creating design system
- TypeScript always — never offer JS option
- Expo Router always — never React Navigation
- Default to `src/` with feature-based structure
- Default to `StyleSheet.create` for styling (Unistyles as advanced option)
- Default to `Tabs` from `expo-router/tabs` (NativeTabs only for iOS 26+ projects)
- Write real file contents, never leave files empty
- Feature-specific state → `src/features/xxx/store/`, app-wide state → `src/store/`
