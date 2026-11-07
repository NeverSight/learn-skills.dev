---
name: ui-grammar
description: "Describe or design a React UI as a source-grounded component system: its visual vocabulary, JSX tree, ownership, constraints, states, actions, effects, and proof. Use for visual-to-code design-system work or a disposable holistic read of an existing route; do not create persistent grammar artifacts by default."
---

# UI Grammar

Use UI Grammar to talk precisely about what a UI is, why it has that shape, and which React pieces may compose it. It is a reasoning and communication lens, not a schema, compiler, registry, or source of product truth. Code and the rendered product remain master.

## Choose the direction

- **Recover:** understand an existing route or component system from its rendered result and live source. An unqualified request such as “use UI Grammar to describe the Connections route” means Recover.
- **Design:** turn a visual reference or product intent into a React vocabulary and composition contract before or during implementation.

Use both only when the task genuinely moves from understanding an existing surface into redesigning it.

## Keep claims honest

Label material distinctions when they matter:

- **Observed:** directly visible in source, runtime, or rendered evidence.
- **Declared:** intended product or design-system law supplied by an owner or authoritative reference.
- **Derived:** a conclusion that follows from observed facts plus declared law.
- **Unknown:** not established by the available evidence.

Never promote current JSX topology into design intent merely because it exists. Never describe static source inspection as runtime, accessibility, or visual proof.

## Inspect the whole surface

Follow the route far enough to understand the visible outcome, without inventorying the entire repository:

- rendered route or supplied visual reference;
- route entry and composition-owning components;
- design-system components, variants, semantic tokens, slots, and specimens actually used;
- route-owned data, state, capabilities, and environment inputs;
- user actions, navigation, effects, loading, empty, error, and recovery behavior;
- tests, stories, debug fixtures, traces, or screenshots that witness consequential claims;
- external, dynamic, native, or runtime boundaries that remain unknown.

Prefer direct source inspection and the repository's existing tools. Do not introduce a scanner, registry, JSON grammar, fixture matrix, or dependency merely to produce the description.

## Describe it as a grammar

Start with a JSX-like tree. Use real component and product names where observed; mark proposed names as declared.

```text
ConnectionsRoute(inputs)
└─ RouteFrame
   ├─ ScreenHeader(title, action?)
   └─ ConnectionList
      └─ ConnectionRow(source, status, actions)
```

Then describe only the relations that make the tree meaningful:

- vocabulary: components, semantic props, slots, and roles;
- ownership: route placement, component internals, state, effects, and visual system;
- constraints: legal composition, forbidden composition, and forbidden consumer overrides;
- named causes: which product fact, content presence, state, or capability causes each visible delta;
- state/action matrix: only when state changes visible composition, available actions, transitions, or effects;
- evidence and unknowns.

Use this rule shape when prose would blur a consequential constraint:

```text
under <context>
<subject> <must | may | must-not> <relation> <object>
because <product or system reason>
owned by <owner>
witnessed by <source | test | runtime | rendered surface>
```

## Recover an existing UI

Return a compact, disposable overview in this shape:

```text
Surface: <one-sentence product and visual role>

Tree:
  <observed JSX-like composition>

System vocabulary:
  <components, semantic props/slots, variants, and their owners>

Route inputs and named causes:
  <data/state/capability -> visible consequence>

Actions and effects:
  <action -> owner -> transition/effect>, or none

Constraints:
  <meaningful must/may/must-not relations>

Evidence:
  <exact source symbols plus runtime/rendered witnesses actually inspected>

Unknowns:
  <unproved runtime, visual, accessibility, or ownership claims>

Persistence:
  Persist: <durable non-derivable law, or none>
  Encode instead in: <component/type/test/specimen/design-system owner, if applicable>
  Discard: <regenerable topology and observations>
```

Do not create or update repository files unless the user asks. Recover output is conversational working memory by default.

## Design a UI or design system

Translate the visual reference into reusable React building blocks without inventing a parallel styling language:

1. Separate invariants from intentional deltas across the supplied screens or states.
2. Reuse the target design system's existing vocabulary before naming new components.
3. Name semantic props and slots from product meaning, not screenshot dimensions or utility classes.
4. Give every placement, internal geometry, state, action, and effect one owner.
5. Make illegal compositions difficult through ordinary React and TypeScript contracts where valuable.
6. Implement or propose colocated specimens for component states.
7. Prove the complete rendered surface against the reference; component structure or types alone cannot prove visual fidelity.

Every visible delta should have one named cause. Content may derive internal geometry; containers own placement; components own their internal rendering. Avoid generic `className`, size, density, or variant escape hatches unless the owning design system deliberately exposes that semantic choice.

## Systematise a visual relationship

When a visual mismatch across states suggests missing design-system ownership:

For disputed action, feedback, recovery, or inline-control grouping, read [The gap was not spacing](references/action-owned-feedback-case-study.md).

1. Freeze the accepted state as the baseline.
2. Compare variants and name the only allowed cause of each visible delta.
3. Find the missing relationship owner.
4. Promote the relationship, not merely the observed CSS value.
5. Remove consumer-owned geometry that reconstructs the relationship.
6. Prove both unchanged and changed states in the rendered product.

Use **capture → compare → accept → encode → recheck** as the learning loop. Contact sheets are disposable evidence for comparing relevant rendered states; do not build a screenshot catalogue or new capture product. Keep human visual acceptance separate from automated checks. Encode accepted rules in component contracts, implementation, or consequential tests, then re-render the affected states. General reasoning belongs in skill guidance. `LOG.md` records chronological decisions and unresolved context; it is not durable teaching.

## Persist the law, not the map

Persist only a rule that is durable, non-derivable from current code, future-constraining, owned, witnessed, and useful for rejecting a real mistake. Prefer encoding it in the nearest living owner:

- React props or TypeScript types for component contracts;
- components and variants for visual vocabulary;
- tests for consequential state and interaction rules;
- specimens or stories for component states;
- design-system or product doctrine for genuinely cross-cutting law.

Create a dedicated grammar document only when the user explicitly requests one and no nearer owner can carry the law. Never create a grammar registry or exhaustive route catalog.

## Boundaries

- UI Grammar describes user-visible composition and meaning. It does not prescribe file layout or exact call wiring.
- `code-stacks` is independent. Use it only when the user asks for an implementation plan or the exact code seam remains unresolved; do not invoke it automatically after UI Grammar.
- State-machine or Effect libraries are implementation choices, not prerequisites.
- Concrete CSS, utilities, tokens, and dimensions may be cited as observed evidence; semantic design-system owners decide how they are rendered.
