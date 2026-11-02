---
name: component-api-design
description: >-
  Framework-neutral standards for the public API of a reusable UI component: a
  minimal and stable props contract, slots and composition versus configuration
  props, controlled and uncontrolled value pairs, the compound-component pattern,
  and evolving a shared component without breaking its consumers. Sits between
  `architecture-and-design` and the framework skills. Use it when the user
  mentions component API, props design, a component library or design system,
  slots, render props, controlled vs uncontrolled, compound components, a
  "boolean prop explosion", or versioning a shared component.
license: CC-BY-4.0
metadata:
  author: danielteles
  version: "1.0"
---

# Component API Design — Engineering Skill

Standards for the surface a reusable component exposes to the code that uses it: which props exist,
how variation is expressed, who owns the state, and how the API changes over time. Framework-neutral
— the principles hold for React, Vue, and Angular; examples are TSX with the slot equivalent noted.

> **Builds on.** `architecture-and-design` for the design principles underneath (SOLID —
> especially open/closed, cohesion, dependency direction) and `react` / `angular` / `vue` for the
> framework's actual props, slots, and ref API. On a conflict, `architecture-and-design` decides
> the principle, the framework skill decides the API syntax, and this skill decides the shape of
> the component's public contract. Load a sibling only when the task turns on its layer; if it is
> not loaded, apply that layer from general knowledge and do not block.

This SKILL.md is self-sufficient: the **Ruleset** below is the complete, enforceable list. Each
`references/<topic>.md` holds that group's reasoning and `❌ / ✅` code, and
`references/worked-example.md` a full review pass; open them for depth when your runtime allows.

---

## How to Use This Skill

Pick the mode that matches the task. Do the steps in order.

| Mode | Steps |
|---|---|
| **Design** — design or extend a component's public API | 1. Write the smallest props contract that covers the real use cases; make illegal states unrepresentable (`props-contract`). 2. Express structural variation with slots, behavioural variation with props (`slots-vs-config`). 3. For any value the component holds, decide the controlled/uncontrolled contract up front (`controlled-uncontrolled`). 4. Reach for a compound component only when parts must vary independently and share state (`compound-components`). 5. Run the Ruleset as a checklist. Fix each fail before you hand off. |
| **Review** — check a component API in a diff | 1. Run the Ruleset against the diff. 2. Write one finding per fail, in the Output Format below. 3. Order the findings: `must-fix` first, then `consider`. 4. If nothing fails, say so in one line. Do not invent findings. |
| **Evolve** — change a shared component without breaking consumers | 1. Classify the change: additive (safe), behavioural (risky), or breaking (renamed/removed prop, changed default, changed markup contract). 2. For anything past additive, add the new API, deprecate the old with a pointer, and keep both for a release. 3. Ship a codemod for a rename; record it in the changelog with a version. 4. Never change a default value or the DOM/slot contract in a patch release. |

### Output Format

Write one finding per line:

```
<severity> · <topic> · <file>:<line> — <what is wrong>. <the fix as an action>.
```

- `<severity>` is `must-fix` (breaks a rule in this skill, or breaks a consumer) or `consider` (safe, but a rule prefers another form).
- `<topic>` is a Ruleset topic slug (`props-contract`, `slots-vs-config`, `controlled-uncontrolled`, `compound-components`, `versioning`).

### Rules for Every Mode

- Name the Ruleset topic when you enforce a rule.
- The public API is a contract with every consumer. Judge a change by what it costs them, not by how clean it looks in the component.
- Prefer removing a prop to adding one. Every prop is forever, is a test case, and is a thing the next reader must understand.

---

## Ruleset

### props-contract → `references/props-contract.md`

- [ ] The props type is the minimal set that covers real use cases; a speculative "might need it" prop is not added until a caller needs it.
- [ ] Illegal combinations are unrepresentable — a discriminated union over a `variant` prop, not four independent booleans that can all be true.
- [ ] A `variant` / `size` / `tone` axis is a string-literal union, not a boolean per value (`primary` / `secondary`, not `isPrimary` + `isSecondary`).
- [ ] Props are named for intent, stable, and consistent with the library's vocabulary — one name for one concept across every component.
- [ ] A handler follows the framework's event convention (`onChange` in React, a `valueChange` output in Angular, a `change` / `update:value` emit in Vue).
- [ ] A boolean prop reads as a state (`disabled`, `loading`), not a negated setting (`enabled={false}`).
- [ ] A prop's type is a deliberate public type, never the component's private implementation type.
- [ ] The props type is exported and documented, and `children` is typed explicitly.
- [ ] There is no single `config` / `options` object prop standing in for a real API; sensible defaults mean the common case needs almost no props.
- [ ] A prop that passes through to a DOM node (`className`, `aria-*`, `data-*`, `id`) is forwarded, and the component spreads remaining props onto its root or
      a named element deliberately.

### slots-vs-config → `references/slots-vs-config.md`

- [ ] Structural or content variation is a slot — `children`, named slots, or a render prop — not a `renderHeader` / `showFooter` / `leftIcon` / `rightIcon`
      pile of props.
- [ ] A slot is used when the caller supplies markup; a prop is used when the component decides the markup from a value.
- [ ] A component is open for extension without editing it: a new layout is a new composition of its slots, not a new boolean.
- [ ] A render prop or slot that exposes internal state passes a typed, minimal, stable argument object.
- [ ] Slot names describe the position or role (`header`, `actions`, `empty`), not a specific use (`searchBoxSlot`).

### controlled-uncontrolled → `references/controlled-uncontrolled.md`

- [ ] A value the component holds offers both modes: `value` + `onChange` for controlled, `defaultValue` for uncontrolled, and the component never switches an
      instance between them.
- [ ] `defaultValue` is read once on mount; after that the component owns the value until unmount.
- [ ] In controlled mode the component renders exactly what `value` says and calls `onChange` with the requested next value — it does not also keep its own
      copy.
- [ ] Uncontrolled is the default for a simple input; controlled is required only when the value drives other UI or is validated live.
- [ ] Any imperative escape hatch (`ref` with `focus()` / `scrollIntoView()` / `reset()`) is small, named, and documented — not a handle to the internals.

### compound-components → `references/compound-components.md`

- [ ] The compound pattern (`<Tabs><Tabs.List><Tabs.Tab/></Tabs.List></Tabs>`) is used only when the parts must be arranged or omitted by the caller *and* share
      implicit state.
- [ ] Shared state passes through context (or the framework equivalent), not cloned children or prop-drilling; a subcomponent used outside its parent fails with
      a clear error.
- [ ] For a fixed structure with no caller-controlled arrangement, a flat props API is simpler and is preferred.
- [ ] The composed whole is accessible as a unit — roles, `aria` wiring, and keyboard interaction span the subcomponents, per the relevant APG pattern
      (`accessibility`).
- [ ] Subcomponents are namespaced on the parent (`Tabs.Tab`) or exported together, and each is typed.

### versioning → `references/versioning.md`

- [ ] An additive change (a new optional prop, a new slot, a new variant value) is a minor release; a renamed or removed prop, a changed default, or a changed
      DOM/slot contract is a major.
- [ ] A prop being removed or renamed is first deprecated — kept working for one major, marked `@deprecated` with the replacement named, and warned on in
      development.
- [ ] A default value never changes in a patch or minor release; changing it is a breaking change because it alters existing renders.
- [ ] A rename ships with a codemod, and every breaking change is in the changelog with the version and the migration.
- [ ] The component's rendered DOM structure and class/slot contract are treated as API — consumers style and query against them.

---

## Limits

This skill is the public API of a reusable component. It does not cover:

- Broader architecture — layering, feature boundaries, where the design system sits, state management strategy. That is `architecture-and-design`.
- The framework's prop / slot / ref mechanics — `defineModel`, `forwardRef` vs `ref` as prop, `input()` / `output()`, `@ContentChild`. Those are `react` /
  `angular` / `vue`.
- Visual and interaction design of the component — spacing, motion, the design tokens it consumes (`styling-and-design-tokens`).
- Accessibility implementation of a widget pattern beyond "wire the composed whole as a unit" — the APG patterns and testing live in `accessibility`.
- Documentation tooling, Storybook, visual regression, and package publishing mechanics.
- Internal component structure and rendering performance (`web-performance`, and the framework skills).

This skill states what the component should expose. It is not a substitute for building the real use cases against the API and feeling where it fights back.

---

## References

This skill composes with:

- **`architecture-and-design`** — the design principles under these rules (open/closed, cohesion, dependency direction). On a conflict it decides the principle,
  this skill decides the contract shape.
- **`react`** / **`angular`** / **`vue`** — the framework mechanics that implement props, slots, controlled pairs, and compound state. On a conflict this skill
  decides the contract, the framework skill decides the API.
- **`accessibility`** — a compound or slotted component is wired as an accessible unit; the pattern requirements and testing live there.
- **`styling-and-design-tokens`** — the rendered DOM and class contract this skill treats as API is what that skill styles against.
