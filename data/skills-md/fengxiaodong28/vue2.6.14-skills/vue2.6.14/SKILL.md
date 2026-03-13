---
name: vue2.6.14
description: Vue 2.6.14 Options API best practices, reactivity system, component patterns, and ecosystem integration. Each reference shows Vue 2.6.14 specific solutions only.
version: 1.0.0
license: MIT
author: github.com/fengxiaodong28
---

# Vue 2.6.14 Options API & Best Practices

Vue 2.6.14 development guide focusing on the Options API with Object.defineProperty-based reactivity, component patterns, and Vue 2 ecosystem integration (Vue Router 3.x, Vuex 3.x).

## Reactivity System

**Can't detect property addition on objects** → See [reactivity/](reference/reactivity/reactivity-property-addition.md)

**Can't detect array index assignment** → See [reactivity/](reference/reactivity/reactivity-array-index-assignment.md)

**Can't detect array length changes** → See [reactivity/](reference/reactivity/reactivity-array-length-changes.md)

**Frozen objects can't be made reactive** → See [reactivity/](reference/reactivity/reactivity-frozen-objects.md)

**Adding reactive properties with Vue.set** → See [reactivity/](reference/reactivity/using-set-for-reactivity.md)

**Deleting reactive properties with Vue.delete** → See [reactivity/](reference/reactivity/using-delete-for-reactivity.md)

**Vue.observable() for minimal state** → See [reactivity/](reference/reactivity/reactivity-observable.md)

## Global API

**Vue.config global options** → See [global-api/](reference/global-api/vue2-config.md)

**Vue.nextTick for DOM updates** → See [global-api/](reference/global-api/vue2-nexttick.md)

**Creating custom directives** → See [global-api/](reference/global-api/custom-directives.md)

**Global component registration** → See [global-api/](reference/global-api/global-component-registration.md)

**Plugin development** → See [global-api/](reference/global-api/plugin-development.md)

**Global mixins (use with caution)** → See [global-api/](reference/global-api/global-mixins.md)

## Lifecycle

**Vue 2 specific lifecycle hooks** → See [lifecycle/](reference/lifecycle/vue2-lifecycle-hooks.md)

**Never use arrow functions in lifecycle hooks** → See [lifecycle/](reference/lifecycle/no-arrow-functions-in-lifecycle-hooks.md)

**Stateful methods shared across component instances** → See [lifecycle/](reference/lifecycle/stateful-methods-lifecycle.md)

**Async component error handling (Vue 2.6.0+)** → See [lifecycle/](reference/lifecycle/async-component-error-handling.md)

## Component Options

**Props validation with custom validators** → See [component-options/](reference/component-options/props-custom-validators.md)

**Default values for object and array props** → See [component-options/](reference/component-options/props-default-values-objects.md)

**Typing complex props with interfaces** → See [component-options/](reference/component-options/props-complex-types-interface.md)

**Props down, events up pattern** → See [component-options/](reference/component-options/component-communication-props-events.md)

**Using .sync modifier (Vue 2.3+)** → See [component-options/](reference/component-options/sync-modifier-two-way-binding.md)

**Event bus for sibling communication** → See [component-options/](reference/component-options/event-bus-pattern.md)

**Provide/Inject reactivity limitations** → See [component-options/](reference/component-options/provide-inject-not-reactive.md)

**Functional components (stateless)** → See [component-options/](reference/component-options/functional-components.md)

**Custom v-model with model option** → See [component-options/](reference/component-options/custom-model-option.md)

**inheritAttrs for attribute inheritance** → See [component-options/](reference/component-options/inheritAttrs-usage.md)

**Programmatic slot access ($slots/$scopedSlots)** → See [component-options/](reference/component-options/slots-scopedSlots-render.md)

**Transparent wrappers ($attrs/$listeners)** → See [component-options/](reference/component-options/attrs-listeners-advanced.md)

**Default and named slots** → See [component-options/](reference/component-options/slots-default-named.md)

**Scoped slots with slot props** → See [component-options/](reference/component-options/slots-scoped-slot-props.md)

**Deep and immediate watch options** → See [component-options/](reference/component-options/watch-options-deep-immediate.md)

## Directives

**v-model modifiers (.lazy, .number, .trim)** → See [directives/](reference/directives/v-model-modifiers.md)

**Event modifiers for v-on** → See [directives/](reference/directives/v-on-modifiers.md)

**Binding modifiers for v-bind** → See [directives/](reference/directives/v-bind-modifiers.md)

**v-html security considerations** → See [directives/](reference/directives/v-html-security.md)

**v-show vs v-if comparison** → See [directives/](reference/directives/v-show-vs-v-if.md)

**v-for with v-if priority issue** → See [directives/](reference/directives/v-for-v-if-priority.md)

**Missing :key on v-for** → See [directives/](reference/directives/v-for-missing-key.md)

**v-once for static content optimization** → See [directives/](reference/directives/v-once.md)

**v-cloak for hiding uncompiled templates** → See [directives/](reference/directives/v-cloak.md)

**v-pre for skipping compilation** → See [directives/](reference/directives/v-pre.md)

**key, ref, slot, is special attributes** → See [directives/](reference/directives/special-attributes.md)

## Instance API

**Template refs with $refs** → See [instance-api/](reference/instance-api/refs-usage.md)

**Custom events with $emit** → See [instance-api/](reference/instance-api/emit-patterns.md)

**Force re-rendering with $forceUpdate** → See [instance-api/](reference/instance-api/forceUpdate-usage.md)

**$data, $props, $el instance properties** → See [instance-api/](reference/instance-api/instance-data-props-el.md)

**$options, $parent, $root, $children, $isServer** → See [instance-api/](reference/instance-api/instance-options-parent-root-children.md)

## Built-in Components

**transition component for enter/leave animations** → See [components/](reference/components/transition-component.md)

**keep-alive component for caching** → See [components/](reference/components/keep-alive-component.md)

**transition-group for list transitions** → See [components/](reference/components/transition-group-component.md)

## Render Functions

**Render functions and createElement** → See [render-functions/](reference/render-functions/render-functions.md)

## TypeScript Integration

**Using Vue.extend() for TypeScript** → See [types/](reference/types/ts-vue-extend-pattern.md)

**Type-safe computed properties** → See [types/](reference/types/ts-computed-return-types.md)

**Type-safe event handlers** → See [types/](reference/types/ts-options-api-type-event-handlers.md)

**PropType for complex prop types** → See [types/](reference/types/ts-proptype-complex-types.md)

**Shims for .vue files** → See [types/](reference/types/ts-shims-vue-files.md)

**TypeScript improvements in Vue 2.6** → See [types/](reference/types/typescript-improvements-26.md)

## Build Tooling

**vue.config.js basic setup** → See [build-tooling/](reference/build-tooling/cli-vue-config-basic.md)

**Configuring Less preprocessor** → See [build-tooling/](reference/build-tooling/cli-less-configuration.md)

**Environment variables** → See [build-tooling/](reference/build-tooling/cli-environment-variables.md)

**vue-template-compiler version matching** → See [build-tooling/](reference/build-tooling/version-matching-template-compiler.md)

**Common build errors and solutions** → See [build-tooling/](reference/build-tooling/cli-common-build-errors.md)

## Ecosystem Integration

**Router setup and configuration** → See [ecosystem/](reference/ecosystem/router3-basic-setup.md)

**Dynamic routes with params** → See [ecosystem/](reference/ecosystem/router3-dynamic-routes.md)

**Navigation guards** → See [ecosystem/](reference/ecosystem/router3-navigation-guards.md)

**Lazy loading routes** → See [ecosystem/](reference/ecosystem/router3-lazy-loading.md)

**Store setup and modules** → See [ecosystem/](reference/ecosystem/vuex3-store-modules.md)

**State, getters, mutations, actions** → See [ecosystem/](reference/ecosystem/vuex3-core-concepts.md)

**Vuex reactivity gotchas** → See [ecosystem/](reference/ecosystem/vuex3-reactivity-gotchas.md)

## @vue/composition-api (Vue 2)

**Composition API plugin setup** → See [ecosystem/](reference/ecosystem/composition-api-setup.md)

**Ref vs Reactive for reactive state** → See [ecosystem/](reference/ecosystem/composition-api-ref-reactive.md)

**Creating reusable logic with composables** → See [ecosystem/](reference/ecosystem/composition-api-composables.md)

**Using Vuex with Composition API** → See [ecosystem/](reference/ecosystem/composition-api-vuex.md)

## vue-class-component (Vue 2)

**Class-based component definition** → See [ecosystem/](reference/ecosystem/vue-class-component-basics.md)

**Using mixins with class components** → See [ecosystem/](reference/ecosystem/vue-class-component-mixins.md)

**Composition API vs Class Component** → See [ecosystem/](reference/ecosystem/composition-vs-class-component.md)

## Vue 2 vs Vue 3 Differences

**Key syntax differences** → See [comparison/](reference/comparison/vue2-vs-vue3-syntax.md)

**Filters removed in Vue 3** → See [comparison/](reference/comparison/vue2-filters-deprecated.md)

**$listeners and $attrs changes** → See [comparison/](reference/comparison/vue2-listeners-attrs.md)
