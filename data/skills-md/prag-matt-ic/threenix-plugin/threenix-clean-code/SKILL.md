---
name: threenix-clean-code
description: Review and refactor TypeScript and React code for readability. Use for unclear naming, complex control flow, oversized functions, and focused code-quality reviews.
---

## Task

Begin first by identifying any violations of the checklist items. Then, refactor the code to address these issues.

---

### Full Documentation

- [Clean Code TypeScript](https://github.com/labs42io/clean-code-typescript)

---

## Checklist

- [ ] Use meaningful names – variable and function names should clearly communicate what the code does. Avoid abbreviations or cryptic identifiers; clear naming makes the code self‑documenting. Boolean variables should be named to imply true/false (e.g. isVisible, hasItems). Don't add unecessary prefixes or suffixes - e.g do not add 'Ref' to a useRef variable.

- [ ] Be consistent – use the same vocabulary for the same type of entity (e.g. always call the current player position playerPos instead of mixing currentPos, position, and pos).

- [ ] Write small, pure functions – each function should have a single responsibility. Break complex logic into smaller helpers rather than nesting conditionals.

- [ ] If a function has 3 or more parameters, use an object to group them - this makes it easier to understand what each parameter means.

- [ ] Prefer early returns over deep nesting – return early to avoid if/else pyramids.

- [ ] Prefer immutability – never mutate objects or arrays directly. When updating state, return new objects instead of modifying existing ones.

- [ ] Avoid magic numbers and strings – declare constants (e.g. LANE_COUNT = 3) so that values are descriptive and changeable. The exception to this rule is animation timing values (e.g. duration: 0.5, delay: 0.2) and inline copy which can be left inline.

- [ ] Comment judiciously – write code that is self‑explanatory. When comments are needed, make them precise and consider using // TODO to mark work that should be improved later.

- [ ] Avoid creating expensive objects/classes in loops or animation frames - reuse objects where sensible to reduce garbage collection. For example: never create a new Vector3() inside useFrame().

- [ ] Review imports and ensure that types/interfaces are imported as types (e.g. `import { type MyType } from '...'`). Classes should not be marked as types. Remove any unused imports.

- [ ] React arrow function components should be declared as `type FC` from `react`.

- [ ] In React 19+ ref can be passed as a prop. So remove forwardRef and define the ref as a normal prop. e.g:

```tsx
type Props = {
  ref?: React.RefObject<HTMLElement | null>
}
```

- [ ] Prefer 'type' over 'interface' for defining object shapes (and props) unless you need declaration merging.
