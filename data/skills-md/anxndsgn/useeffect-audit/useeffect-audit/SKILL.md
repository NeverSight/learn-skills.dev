---
name: useeffect-audit
description: "Audit and refactor React Effects using official React guidance: keep Effects for external synchronization, separate events from Effects, model each Effect as an independent start/stop process, fix dependency issues by changing code (not suppressing lint rules), and use useEffectEvent only for truly non-reactive Effect logic."
---

# useEffect Audit

## Overview

Run a structured review of every `useEffect` and `useLayoutEffect` in scope. For each one, decide whether to:
- keep it as an external synchronization process,
- move logic to an event handler,
- derive during render, or
- split/extract logic (including `useEffectEvent` where appropriate).

Apply the smallest behavior-preserving refactor that removes unnecessary Effects and fixes dependency/lifecycle bugs.

Primary references:
- https://react.dev/learn/synchronizing-with-effects
- https://react.dev/learn/lifecycle-of-reactive-effects
- https://react.dev/learn/separating-events-from-effects
- https://react.dev/learn/removing-effect-dependencies
- https://react.dev/reference/react/useEffectEvent
- https://react.dev/learn/you-might-not-need-an-effect

## Audit Workflow

1. Inventory Effects:
	- Scan for `useEffect(` and `useLayoutEffect(`.
	- Group by component and by synchronization intent.
2. Choose the right primitive first:
	- Event handler if logic is caused by a specific interaction.
	- Effect if logic is caused by rendering/visibility and synchronizes with an external system.
	- Render-time derivation if logic only computes UI data.
3. For each kept Effect, validate lifecycle semantics:
	- Treat it as an independent start/stop synchronization process.
	- Ensure cleanup fully undoes setup.
	- Ensure setup -> cleanup -> setup (development stress-test) is safe.
	- Split unrelated synchronization into separate Effects.
4. Fix dependencies by changing code, then dependencies:
	- Include every reactive value read by the Effect.
	- Never suppress `react-hooks/exhaustive-deps`.
	- If dependencies are undesirable, refactor:
		- Move event-specific logic to handlers.
		- Move non-reactive constants outside the component.
		- Move object/function creation inside the Effect or extract primitives.
		- Use state updater functions when reading state only to compute next state.
		- Extract non-reactive logic into `useEffectEvent` when needed.
5. Apply minimal refactors one Effect at a time:
	- Preserve behavior and user-visible semantics.
	- Remove redundant state and redundant re-renders.
6. Report decisions and verification notes using the output format below.

## Decision Rules

- Keep an Effect only for synchronization with systems outside React:
	- Browser/DOM APIs, subscriptions, sockets, timers, imperative widgets, network sync tied to visibility.
- Remove an Effect when it only transforms data:
	- Derive directly during render; avoid mirrored state.
- Remove an Effect when it only handles a user action:
	- Execute in the event handler that caused it.
- Split Effects by purpose:
	- One synchronization process per Effect.
- Treat dependency arrays as a description of code, not a scheduling knob:
	- If you want different dependencies, change the code first.
- Use `useEffectEvent` only for non-reactive logic that must read latest props/state without re-synchronizing:
	- Do not use it as a shortcut to hide real dependencies.
	- Do not pass Effect Events to other components/hooks.
	- Do not include Effect Events in dependency arrays.

## Output Format

For each audited effect, produce:

1. `file:line` and component name
2. Current effect intent (one sentence)
3. Classification: `Keep` or `Remove`
4. Trigger type: `Rendering-driven sync` or `Interaction-driven event`
5. Refactor pattern applied (from `references/checklist.md` and/or React docs)
6. Dependency rationale (reactive values read and why listed)
7. Code-level change summary
8. Verification notes (what to test)

## Guardrails

- Do not move logic out of Effects if it changes true external synchronization semantics.
- Do not silence `react-hooks/exhaustive-deps` to force desired timing.
- Do not use `useEffectEvent` to avoid legitimate dependencies.
- Do not use refs as a hack to prevent Effects from running in development.
- Do not add `useMemo`/`useCallback` unless required for correctness or measured performance.
- Prefer the smallest safe refactor and verify with targeted tests, including remount/re-sync behavior.
