---
name: flutter-plan
description: Turns an app idea, a design or a feature request into screens, user flows and journeys (Mermaid diagrams) and an ordered build plan of small slices with backend, service, native and design needs, acceptance checks and effort ranges. Use when asked to plan, map flows or journeys, break work into steps or milestones, or write a build plan, for a whole app or for one feature; do not start planning during other tasks.
license: Apache-2.0
---

# Flutter plan

A plan is for the developer to read and correct before code is written. It names the order, the unknowns and the things that wait on other people. It does not write code and does not invent numbers.

## Steps

1. **Pick the scope.**
   - **App-wise:** a new app or a large part of one. Use all of the steps below, including the foundation and ship slices.
   - **Feature-wise:** one feature in an existing project. Read the project profile and the closest existing feature first (`flutter-project-profile`, `flutter-feature`), and plan only what is new.
   - **Flows only:** the developer wants the journey drawn, not a build plan. Do steps 2 to 4 and stop.
2. **Collect what exists.** If the input is a requirements document, ticket or design brief, first list its acceptance criteria and the questions it leaves open, and show them before drafting slices. Collect: the brief or idea, a design or screenshots, a backend contract or list of endpoints, the project profile, store or compliance constraints. Ask at most five questions, and only those whose answer changes the order or the size (platforms, roles, offline, who owns the backend, design ready or not). If the developer is not there to answer, state the assumption you took and go on.
3. **List the screens and states** for each flow: entry points, the screens, and the states that need their own handling (loading, empty, error, offline, permission denied, session expired). Use `references/flows-and-journeys.md` for the diagram shapes and the checklist of paths people forget.
4. **Draw the flows.** One Mermaid flowchart per flow (happy path plus the failure and exit paths). Add a journey or state diagram only when it explains something the flowchart cannot. Keep each diagram small enough to read; split by flow, not by screen.
5. **Cut into slices** with `references/slicing-and-order.md`: each slice is a thin, working path through screen, state, data and navigation that can be run and checked on its own. Put the riskiest unknown first (a native SDK, a backend that does not exist yet, a store approval), not last.
6. **Fill the plan template** in `references/plan-template.md` for every slice: goal, screens, data and API needs, services and native setup, design needs, acceptance checks (observable, not "works well"), risks, and the skill that does it. List anything that waits on other people (backend, design, store accounts, review) as an elapsed-time blocker, separate from build effort. Use `flutter-service-setup` for consoles and keys and `flutter-release` for store steps instead of restating them.
7. **Add effort ranges.** If `flutter-estimate` is installed, run it on the slices that carry real uncertainty. If it is not, or for the other slices, say "small, medium or large" and what would change that. Never give a single number.
8. **Report** in this order: assumptions and open questions, the flow diagrams, the ordered slice table, blockers, the first slice to build and why. Offer to save the plan to `docs/plans/<name>.md` in the project; do not create the folder or file unasked, but when the developer named a path or asked for the plan to be saved, write it there. Each slice should read as a request that `flutter-feature` can take as it is.

## Rules

- No code, no package choices without checking (`flutter-feature-notes` has the dated feature entries; say when an entry is unverified).
- Do not plan design work inside the plan. Name the screens that need design and point to `flutter-design`; logo, icon and screenshots go to `flutter-store-assets`.
- Do not plan tests unless the developer asked for them; if they did, add a test line to the slice and point to `flutter-testing`.
- Say plainly when a part is not realistic on Flutter or needs a platform owner's approval, and what to do instead.
- A plan is a hypothesis. When a slice teaches something that changes the next ones, update the plan and say what changed.
