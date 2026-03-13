---
name: ionic-to-expo
description: Convert Angular/Ionic/Capacitor TypeScript code to React Native/Expo equivalents. Use when migrating mobile apps from Ionic to Expo, converting Angular components to React Native, mapping Capacitor plugins to Expo modules, or translating RxJS/Services patterns to React state management.
---

# Ionic to Expo Migration

Convert Angular/Ionic/Capacitor projects to React Native/Expo.

## Workflow

1. **Analyze** - Read source TypeScript files, identify patterns
2. **Map** - Match Ionic/Angular patterns to RN/Expo equivalents
3. **Convert** - Generate equivalent React Native/Expo code
4. **Validate** - Check for missing dependencies or incompatibilities

## Conversion Process

When given Angular/Ionic source files:

1. Identify the file type:
   - `.component.ts` → React functional component
   - `.service.ts` → Custom hook or context
   - `.page.ts` → Screen component
   - `.module.ts` → Usually not needed (note dependencies)
   - `.guard.ts` → Navigation guard logic

2. Extract and convert:
   - Template (`@Component.template`) → JSX return statement
   - Styles (`@Component.styles`) → StyleSheet or styled-components
   - Inputs (`@Input()`) → Props
   - Outputs (`@Output()`) → Callback props
   - Lifecycle hooks → useEffect patterns

3. Reference the mapping guides:
   - **Components**: See [references/components.md](references/components.md)
   - **Navigation**: See [references/navigation.md](references/navigation.md)
   - **Native Plugins**: See [references/plugins.md](references/plugins.md)
   - **State/Services**: See [references/state.md](references/state.md)

## Quick Reference

| Angular/Ionic | React Native/Expo |
|--------------|-------------------|
| `@Component` | Function component |
| `@Input()` | Props |
| `@Output()` | Callback props |
| `ngOnInit` | `useEffect(..., [])` |
| `ngOnDestroy` | `useEffect` cleanup |
| `ngOnChanges` | `useEffect` with deps |
| `*ngIf` | `{condition && <Component/>}` |
| `*ngFor` | `.map()` |
| `[(ngModel)]` | `value` + `onChangeText` |
| `[class.x]="cond"` | Conditional styles |
| `(click)` | `onPress` |
| `BehaviorSubject` | `useState` or context |
| `Observable.pipe()` | Custom hooks |

## Output Format

When converting, provide:

1. **Converted code** with equivalent functionality
2. **Required dependencies** to install
3. **Migration notes** for manual adjustments needed
4. **Type definitions** if applicable

## Anti-Patterns to Avoid

- Don't blindly translate class components; use hooks
- Don't create services as classes; use hooks/context
- Don't use `any` types; preserve TypeScript safety
- Don't ignore platform differences (iOS vs Android)
