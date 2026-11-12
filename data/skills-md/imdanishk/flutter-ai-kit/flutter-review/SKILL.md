---
name: flutter-review
description: Reviews Flutter code changes as a careful senior reviewer and reports findings with file and line, without editing files. Use when asked to review a diff, branch, pull request or a set of Flutter files.
license: Apache-2.0
---

# Flutter review

Read-only. Never modify files while reviewing.

## Steps

1. Get the change: `git diff` against the base branch, or the files, folders or paths named. When the code is unchanged (a request to review a screen or folder as it is), review the named files in full and say there was no diff. Read the project profile and every rule in `AGENTS.md` (and `CLAUDE.md` or a rules folder if present). List the rules that apply to this change. Findings are judged against these rules first and the checklist below second, not general taste.
2. Read each changed file in full where it matters. Follow calls into the code the change depends on.
3. Check each applicable project rule against the diff, then the list below. A rule that existing code elsewhere already breaks is still a rule: if the diff breaks it, report it, and add "follows existing precedent in <file>" so the team can decide whether to fix the rule or the code. Do not excuse a violation because it was copied. Report only what you can point to in the code. If you suspect something you cannot confirm, say so and say what would confirm it.
4. Report in this format, most important first:

```
1. <severity: must fix | should fix | consider> <file>:<line> <one-line problem>
   Why it matters: <consequence>
   Fix: <specific change>
```

End with one line listing what you checked and found fine, and one line for anything you could not check. "No findings" is only acceptable with that list: name the project rules and checklist items you checked against the diff. If you wrote this code yourself in this session, say so: a review by the author misses what the author missed, so recommend a second review in a fresh session or by another agent.

## Checklist

**Correctness and lifecycle**
- `BuildContext` used after an `await` without `context.mounted`
- state emitted after a cubit or bloc is closed
- loading states with no error path, so a spinner can run forever
- `setState` after dispose; timers, streams, controllers, focus nodes, animation controllers not disposed or cancelled

**Architecture** (against the profile)
- presentation reaching into data code or calling the service locator outside the provider that creates a cubit
- business logic in widgets
- a second way of doing what the project already does (status, results, forms, navigation)

**State and data**
- one status shared by operations that run at the same time
- lists loaded without paging where the data can grow
- equality missing on state classes, so listeners never fire or always fire

**UI**
- user-visible text outside the string table or localization (also plurals built in code, left/right values in a right-to-left app, and fixed date or number formats; open `flutter-feature/references/localization-recipe.md` when this skill is installed and the code touches text, dates, numbers or layout direction)
- non-lazy lists for long data, missing `const`, unbounded widgets that can overflow, text that cannot scale, tap targets without labels

**Platform**
- new permission, deep link, push, camera, location or background feature without the matching Android manifest or iOS `Info.plist` and entitlement changes
- code that works on one platform only and is not guarded

**Security and privacy**
- secrets or tokens in source, tokens in plain preferences, personal data in logs, cleartext HTTP

**Dependencies**
- a new package: is it maintained, does it support every target platform, is the licence acceptable, is it really needed?

**Stack-specific checks** (apply only the one the project profile names)

- Cubit or bloc: a cubit created inside `build` or a `BlocProvider` that recreates it on every rebuild; `context.watch` used in a callback or `context.read` used to render; a `BlocListener` that does what a `BlocBuilder` should draw (or the reverse); state classes without equality; the same cubit instance shared by routes that should not share it.
- Riverpod: `ref.read` inside `build` for values the widget must react to, and `ref.watch` inside callbacks; writing to `state` after an `await` without checking `ref.mounted`; notifier methods called from `build`; one `AsyncValue` shared by operations that run side by side; providers that read `BuildContext`; missing `ProviderScope`; legacy providers (`StateProvider`, `StateNotifierProvider`) in new code; automatic retry left on for calls that must not repeat (payments, one-time actions).

- Any other state pattern (`ValueNotifier`, `ChangeNotifier`, Provider, get_it logic classes, signals): controllers, notifiers and their listeners disposed or removed; state replaced with a new object, not mutated in place; no value set or `notifyListeners` called during `build`; the project's own rules from the profile.

**Network, sessions, paging and caches** (when the change touches them; details in `references/api-auth-paging-pitfalls.md`)
- success treated as `== 200` only; a catch-all that hides the specific error or a parsing bug; error bodies assumed to be maps
- 401, 403 and expired session mapped to one error; sign-out decided by message text; auth failures handled for one client type only
- a refresh that can run twice at once; sign-out events sent per failed request; caches not cleared on sign-out
- a paged list that cannot load after cache hydration; cache keys shared between screens or users; search events that wipe filters
- the same checks for a shared base package: unused or exactly pinned dependencies, app-specific values inside it, no tests, machine files committed

**Generated code**
- generated files edited by hand, or annotated files changed without regenerating
