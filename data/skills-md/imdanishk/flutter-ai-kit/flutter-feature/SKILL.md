---
name: flutter-feature
description: Adds or changes a feature, screen, form or list in an existing Flutter project by following the project's own conventions, then regenerates code and runs the analyzer. Use when asked to build, extend or modify app functionality; for bug fixes, refactors and upgrades use flutter-fix, and for plans or flows use flutter-plan.
license: Apache-2.0
---

# Flutter feature

## Steps

1. **Load the project profile and the project's rules.** Read `AGENTS.md` fully (also `CLAUDE.md` and any rules folder the agent tool uses, such as `.cursor/rules` or `.claude/rules`). If there is no profile, run the `flutter-project-profile` skill first. Pick the rules that apply to this task (a short list, at most ten) and follow them. Where a project rule and this skill disagree, the project rule wins. Where a written rule and existing code disagree (for example an older feature that breaks the rule), do not quietly copy the existing code: follow the written rule if that is possible without changing code outside the task; if only the existing pattern fits (a shared contract or base class forces it), use it and record it as a rule conflict (step 6) with the file that forces it.
2. **Open the exemplar feature** named in the profile (if the request is to match a design or to design the look, use `flutter-design` for the visuals and this skill for the code) and the closest existing feature to this request. Plan the new files by mirroring it, layer by layer. For a change touching more than three files, or when the request is ambiguous, show the plan (file, purpose, one line each) and the assumptions before writing code. For a small, clear change, just do it. If the feature needs something outside the repo (Maps or Places keys, Firebase, social login, push, subscriptions or purchases), run the `flutter-service-setup` skill first and show its setup list with the plan.
3. **Reuse before creating.** Search for an existing status type, form field state, result type, validators, shared widgets, string table or localization keys. Use them. Do not introduce a second way of doing something the project already does.
4. **Implement in dependency order:** domain, data, state, cubit or bloc, page, dependency registration, route, strings. Keep business logic out of widgets.
5. **Generate and check.** Run code generation if you touched annotated files, then `flutter analyze` (with the `fvm` prefix when the version is pinned). Fix what the analyzer reports. Never edit generated files. If code generation or the full analyzer cannot run (missing generated files, missing environment values or secrets), do not work around it: analyze only the files you changed (`dart analyze <files>`) and say in the summary exactly what was not checked and why.
6. **Finish with a short summary:** files added and changed, assumptions made, and anything the developer must still do by hand (native configuration, backend changes, keys, store settings). Add a **Rule conflicts** line: `none`, or each place where your code departs from a written project rule or relies on a precedent that does, with the rule, the file, and why. Never leave a known departure unmentioned.

## Watch for these (the usual causes of rework)

- Using `BuildContext` after an `await` without checking `context.mounted`.
- Emitting state after a cubit or bloc is closed.
- A load or submit that can never leave the loading state because its error path is missing.
- One shared status for operations that run side by side (load list and delete item need their own).
- Controllers, focus nodes, timers or stream subscriptions that are never disposed or cancelled.
- User-visible text outside the project's string table or localization, or a plural built in code (`count == 1 ? '' : 's'`) instead of an ARB plural.
- A new package added without asking, or a new feature that needs Android or iOS configuration (permissions, manifest, `Info.plist`, entitlements) and does not say so.
- Business logic or data access called straight from a widget.
- A feature that adds API calls, token handling, paging, search or caches without reading the pitfalls list in the `flutter-review` skill (`api-auth-paging-pitfalls.md`, if that skill is installed) first (success codes, error mapping, one refresh at a time, caches cleared on sign-out, paging after cache hydration).

## References

- `references/bloc-freezed-recipe.md`: a complete feature slice for the Cubit, Freezed, injectable and auto_route stack.
- `references/riverpod-recipe.md`: a complete feature slice for Riverpod 3.
- `references/graphql-ferry-recipe.md`: Ferry (GraphQL) setup, code generation, repository mapping to `Result`, auth link and cache pitfalls; read it when the project uses Ferry or the feature adds GraphQL.
- `references/localization-recipe.md`: gen-l10n setup, ARB placeholders and plurals, right-to-left, Android and iOS native language settings, and per-language store listings; read it when the project or feature adds a language or user-visible text in an app that has localization.

Read the recipe that matches the project's stack only when the project has no suitable exemplar feature, or when asked to start a feature from scratch.
