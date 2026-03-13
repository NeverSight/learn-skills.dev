---
name: react-native-doctor
description: Diagnose and fix React Native & Expo codebase health issues. Use when reviewing React Native code, fixing performance problems, auditing accessibility, or improving architecture.
version: 1.0.0
---

# React Native Doctor

Scans your React Native and Expo codebase for performance, accessibility, architecture, correctness, and security issues. Outputs a 0–100 score with actionable diagnostics.

## Usage

```bash
npx -y react-native-doc@latest . --verbose
```

For Expo projects:

```bash
npx -y react-native-doc@latest . --verbose --expo-only
```

## Workflow

1. Run the command above at the project root
2. Read every diagnostic with file paths and line numbers
3. Fix issues starting with errors (highest severity)
4. Re-run to verify the score improved

## Rules (70+)

### React Native

- **Correctness**: raw text outside `<Text>`, deprecated modules, removed APIs (`Dimensions.get`)
- **Performance**: inline `renderItem` functions, missing `keyExtractor`, `ScrollView` for long lists, inline style objects, anonymous JSX callbacks, heavy array chains in render, single-element style arrays, missing `React.memo` on list items, `Animated` API (prefer `react-native-reanimated`)
- **Architecture**: legacy shadow properties, hardcoded screen dimensions instead of `useWindowDimensions()`, excessive `Platform.OS` branching, hardcoded colors, prop drilling, god components, unnecessary `useEffect` for derived state
- **Images**: missing explicit width/height on `<Image>`

### Accessibility

- Missing `accessibilityLabel` on touchable elements
- Missing `accessibilityRole` on interactive components
- Non-descriptive labels ("button", "tap here", etc.)
- Images without `accessible` + `accessibilityLabel`
- Small tap targets without `hitSlop` (< 44pt)

### Navigation (React Navigation)

- Inline component definitions in `Stack.Screen`
- Missing `screenOptions` defaults on navigators

### Expo

- Hardcoded colors without `useColorScheme()` dark mode support
- `Constants.manifest` → `Constants.expoConfig`
- `_layout.tsx` missing `ErrorBoundary` export
- Hardcoded API keys in source code
- Missing `app/+not-found.tsx` for Expo Router

### React (applies to all projects)

- **Security**: `eval()`, secrets in client bundle
- **State & Effects**: derived state in `useEffect`, cascading `setState`, missing deps, `fetch` in effects, unnecessary `useEffect` for derived state
- **Architecture**: nested component definitions, giant components (>200 lines)
- **Performance**: missing `useMemo`/`useCallback`, non-lazy state init, inline objects to memoized components
- **Bundle Size**: barrel imports, full lodash, `moment.js`
- **Dead Code**: unused files, exports, types

## Score

- **75+**: Great
- **50–74**: Needs work
- **0–49**: Critical

## Fix with an AI agent

After scanning, hand off to an agent to fix all issues automatically.

### Ami

```bash
npx -y react-native-doc@latest . --fix
```

### Cline

```bash
npx -y react-native-doc@latest . --cline
```

If the `cline` CLI is installed (`npm install -g cline`), runs it directly. Otherwise copies the fix prompt to clipboard and opens VS Code/Cline extension.
