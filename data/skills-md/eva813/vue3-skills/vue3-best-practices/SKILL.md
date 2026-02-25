---
name: vue3-best-practices
description: Vue 3 performance optimization and best practices guidelines for modern frontend applications. This skill should be used when writing, reviewing, or refactoring Vue 3 code to ensure optimal performance patterns, proper Composition API usage, and modern development practices. Triggers on tasks involving Vue 3 components, Composition API, reactivity, state management, or performance optimization.
license: MIT
metadata:
  author: Eva
  version: "1.0.0"
---

# Vue 3 Best Practices

Comprehensive performance optimization and development guide for Vue 3 applications. Contains 45 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Vue 3 components or composables
- Implementing reactive data and computed properties
- Reviewing code for performance issues
- Refactoring from Vue 2 to Vue 3
- Optimizing bundle size or load times
- Working with state management (Pinia/Vuex)
- Implementing async operations in components

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Reactivity Performance | CRITICAL | `reactivity-` |
| 2 | Component Optimization | CRITICAL | `component-` |
| 3 | Bundle Size & Loading | HIGH | `bundle-` |
| 4 | Composition API | MEDIUM-HIGH | `composition-` |
| 5 | Template Performance | MEDIUM | `template-` |
| 6 | State Management | MEDIUM | `state-` |
| 7 | Lifecycle Optimization | LOW-MEDIUM | `lifecycle-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Reactivity Performance (CRITICAL)

- `reactivity-ref-vs-reactive` - Use ref for primitives, reactive for objects
- `reactivity-shallow-ref` - Use shallowRef for large immutable objects
- `reactivity-computed-caching` - Leverage computed property caching
- `reactivity-watch-vs-watcheffect` - Choose appropriate watcher
- `reactivity-unref-performance` - Minimize unref calls in hot paths
- `reactivity-readonly-immutable` - Use readonly for immutable data

### 2. Component Optimization (CRITICAL)

- `component-async-components` - Use defineAsyncComponent for heavy components
- `component-functional` - Use functional components for simple presentational logic
- `component-keep-alive` - Cache expensive components with keep-alive
- `component-lazy-hydration` - Implement lazy hydration for non-critical components
- `component-prop-validation` - Use efficient prop validation
- `component-emit-performance` - Optimize event emissions

### 3. Bundle Size & Loading (HIGH)

- `bundle-tree-shaking` - Structure imports for optimal tree-shaking
- `bundle-dynamic-imports` - Use dynamic imports for code splitting
- `bundle-plugin-imports` - Use unplugin-auto-import for better DX
- `bundle-lodash-imports` - Import lodash functions individually
- `bundle-moment-alternatives` - Use day.js instead of moment.js
- `bundle-icons-optimization` - Optimize icon imports and usage

### 4. Composition API (MEDIUM-HIGH)

- `composition-script-setup` - Prefer <script setup> for better performance
- `composition-composables-reuse` - Extract reusable logic into composables
- `composition-provide-inject` - Use provide/inject for dependency injection
- `composition-expose-selectively` - Expose only necessary properties
- `composition-reactive-transform` - Use reactive transform where appropriate
- `composition-auto-import` - Configure auto-imports for better DX

### 5. Template Performance (MEDIUM)

- `template-v-once` - Use v-once for static content
- `template-v-memo` - Use v-memo for expensive list rendering
- `template-key-optimization` - Optimize v-for keys for performance
- `template-conditional-rendering` - Choose v-if vs v-show appropriately
- `template-slot-performance` - Optimize slot usage and scoped slots
- `template-directive-optimization` - Create efficient custom directives

### 6. State Management (MEDIUM)

- `state-pinia-optimization` - Optimize Pinia store structure
- `state-store-composition` - Use store composition patterns
- `state-persistence` - Implement efficient state persistence
- `state-normalization` - Normalize complex state structures
- `state-subscription` - Optimize state subscriptions
- `state-devtools` - Configure devtools for debugging

### 7. Lifecycle Optimization (LOW-MEDIUM)

- `lifecycle-cleanup` - Properly cleanup resources in onUnmounted
- `lifecycle-async-setup` - Handle async operations in setup
- `lifecycle-watchers-cleanup` - Clean up watchers and effects
- `lifecycle-dom-access` - Access DOM safely in lifecycle hooks
- `lifecycle-ssr-considerations` - Handle SSR lifecycle differences

### 8. Advanced Patterns (LOW)

- `advanced-teleport-usage` - Use Teleport for portal patterns
- `advanced-suspense-async` - Implement Suspense with async components
- `advanced-custom-renderer` - Create custom renderers when needed
- `advanced-compiler-macros` - Use compiler macros effectively
- `advanced-plugin-development` - Develop efficient Vue plugins

## Framework Integration

### Vite Integration
- Utilize Vite's fast HMR and build optimizations
- Configure proper chunk splitting strategies
- Use Vite plugins for Vue-specific optimizations

### TypeScript Integration
- Leverage Vue 3's improved TypeScript support
- Use proper type definitions for better DX
- Configure TypeScript for optimal build performance

### Testing Integration
- Use Vue Test Utils with Composition API
- Implement efficient component testing strategies
- Optimize test performance and reliability

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/reactivity-ref-vs-reactive.md
rules/component-async-components.md
rules/composition-script-setup.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect Vue 3 code example with explanation
- Correct Vue 3 code example with explanation
- Performance impact and measurements
- Additional context and Vue 3-specific considerations

## Migration from Vue 2

Special considerations for migrating from Vue 2:
- Composition API vs Options API patterns
- Reactivity system changes and optimizations
- Component definition and registration updates
- Event handling and lifecycle changes

## Performance Monitoring

Tools and techniques for monitoring Vue 3 performance:
- Vue DevTools integration
- Performance profiling with browser tools
- Bundle analysis and optimization
- Runtime performance monitoring