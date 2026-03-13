---
name: zereight-react-native
description: Gateway skill for React Native development. Routes tasks to the right specialist skill — basics, animations, state, navigation, native modules, testing, deployment, or Storybook. Use when starting any React Native development task.
---

# zereight-react-native

This skill does not contain implementation details.
It routes you to the right specialist skill based on what you're building.

## Skill map

| Task | Use this skill |
|------|---------------|
| Components, styling, layout, Expo basics | `react-native-basics` |
| Animations, Reanimated, Gesture Handler | `react-native-animations` |
| State management (Zustand, Redux, TanStack Query) | `react-native-state` |
| Navigation, deep linking, tab/stack structure | `react-native-navigation` |
| Native modules, Turbo Modules, JSI, Fabric | `react-native-native-modules` |
| Testing (Jest, Testing Library, Detox) | `zereight-react-native-testing` / `react-native-testing` |
| Deployment (EAS Build, App Store, Play Store) | `react-native-deployment` |
| Storybook setup | `setup-react-native-storybook` |
| Writing Storybook stories | `writing-react-native-storybook-stories` |
| HeroUI Native components | `heroui-native` |
| Performance optimization guide (FPS, TTI, bundle) | `react-native-best-practices` / `vercel-react-native-skills` |
| **Performance regression detection during code review** | `zereight-react-native-optimizer` |

## When to delegate to optimizer

`zereight-react-native-optimizer` is a **review** tool, not a **development** guide.

Invoke the optimizer when:
- A PR diff touches list rendering, animation, or native module code
- Reviewing an RN PR alongside `zereight-review`

## Quick decision guide

```
Building a new feature?
  → Use the specialist skill matching the feature domain

Debugging a performance issue?
  → react-native-best-practices or vercel-react-native-skills

Reviewing a PR?
  → zereight-review + zereight-react-native-optimizer

UI component library?
  → heroui-native
```
