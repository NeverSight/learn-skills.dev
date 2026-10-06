---
name: to-prototype
description: "Create a lightweight multi-page HTML/CSS/JavaScript UI prototype from agreed Phat project requirements and context. Use when the user wants to visualize and validate navigation, page structure, UI states, content hierarchy, or interaction flow before finalizing a feature spec. Produces editable prototype files under docs/assets/prototype with stable page revision IDs."
---

# To Prototype

Turn agreed product requirements into a lightweight, navigable UI prototype that can be reviewed and edited before implementation planning.

This workflow is optional.

The prototype helps users validate:

* information architecture;
* navigation;
* page structure;
* content hierarchy;
* interaction flow;
* UI states;
* responsive behavior;
* visual direction.

Do not treat the prototype as production implementation.

Do not silently turn visual guesses into product requirements.

Do not implement backend behavior.

## Contents

- [Workflow](#workflow)
- [Read before creating](#read-before-creating)
- [UI design support](#ui-design-support)
- [Prototype conventions](#prototype-conventions)
- [Verification](#verification)
- [Finish](#finish)

## Workflow

Follow:

```text
Read project context
        ↓
Confirm prototype readiness
        ↓
Identify pages and important states
        ↓
Apply ui-design when composition decisions are needed
        ↓
Create prototype structure
        ↓
Assign page revision IDs
        ↓
Build HTML/CSS/JS prototype
        ↓
Verify navigation and interactions
        ↓
Report prototype IDs
        ↓
$edit-prototype
or
$spec-with-prototype
```

## Read before creating

Read `AGENTS.md` first if it exists.

Then inspect:

* `docs/requirement.md`;
* `CONTEXT.md`;
* relevant ADRs;
* existing specs if present;
* existing prototype files if present;
* existing brand/design guidance when available.

Use agreed project terminology.

If project context is not initialized, route to:

```text
$setup-project
```

If a material product or flow decision is still unresolved, route to:

```text
$grill-workflow
```

Do not invent a business rule merely to make the prototype complete.

## UI design support

Before choosing layout, hierarchy, or visual treatment for new screens, load
`$ui-design` when available and apply it inline to the prototype surface.
Pass the agreed content/flows, target pages and states, existing brand or
confirmed design direction, applicable Agreed UI Design Requirements from
`docs/requirement.md`, and prototype file/mock boundaries. Skip it when
only reproducing an already determined layout without new design decisions.

Keep ownership of requirement traceability, prototype IDs, navigation,
verification, and the final handoff. If the supporting skill is unavailable,
follow the prototype conventions and report the fallback; do not auto-install
it or block otherwise valid prototype work.

## Prototype conventions

When creating prototype files or checking prototype fidelity, read [the prototype conventions reference](references/prototype-conventions.md). It contains the file layout, mock boundaries, revision/navigation IDs, visual guidance, responsive/accessibility checks, and requirement traceability rules.

## Verification

Before finishing, verify:

* `index.html` opens correctly;
* all internal prototype navigation resolves;
* every page has a unique current prototype ID;
* navigation IDs match destination page IDs;
* shared CSS loads;
* shared JavaScript loads where used;
* important interactive demonstrations work;
* no obvious broken links exist;
* mobile layout remains usable;
* prototype controls do not obscure the actual UI.

## Finish

Report:

1. prototype directory;
2. pages created;
3. page IDs;
4. important interactions represented;
5. prototype proposals that are not requirements;
6. unresolved product questions;
7. next skill.

Use:

```text
user wants visual changes
    → $edit-prototype

prototype is acceptable
    → $spec-with-prototype

material product decision discovered
    → $grill-workflow
```

Do not create implementation tasks.

Do not implement production code.

Do not claim that visual prototype behavior is agreed merely because it exists.
