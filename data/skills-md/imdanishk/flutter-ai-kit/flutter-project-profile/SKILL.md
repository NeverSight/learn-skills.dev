---
name: flutter-project-profile
description: Detects a Flutter project's stack, folder layout, conventions and commands, and records a short profile in AGENTS.md. Use when asked to document a project's conventions, after the stack changes, or before a new feature, review or new project in a repository that has no profile. Not needed for a small bug fix or a question.
license: Apache-2.0
---

# Flutter project profile

The profile tells every later task how this project does things, so work matches the existing code instead of generic defaults. Existing project conventions always win over anything in these skills.

## Steps

1. **Read the evidence, do not guess.** Open `pubspec.yaml`, `.fvmrc` (if present), `analysis_options.yaml`, the top two levels of `lib/`, `build.yaml`, and the flavor entry points (`lib/main*.dart`). Note which packages are used for:
   state management, dependency injection, routing, networking or GraphQL, local storage, localization, code generation, and error reporting.
2. **Find the exemplar feature.** Pick the most complete, recently changed feature that has presentation, domain and data code, or the project's own layers (some apps have only a logic folder and a ui folder; describe what is there) (if the folder is a git repository, `git log --name-only -n 40 -- lib` helps; if it is not, judge by the folder structure). List its files. Later tasks copy this feature's shape.
   **If there is no feature yet** (a project fresh from `flutter create`, or only the template counter app): do not invent conventions. Record the stack from `pubspec.yaml` only, write `Exemplar: none yet (new project)` under Unknown, and ask the developer which stack to use (offer: Cubit with Freezed, or Riverpod; or their own). Then point to `flutter-new-project`, and skip step 3.
3. **Read the exemplar and write down how it does each of these**, citing the file:
   - how state is held and how load or submit progress is represented (Freezed or Equatable state classes, `ValueNotifier`, `ChangeNotifier`, a get_it logic class, signals, or the project's own pattern)
   - what repositories return (plain values, exceptions, a result or Either type)
   - how a page creates or reads its state holder (cubit, bloc, provider, notifier, controller, global service), and how side effects (snackbar, navigation) are handled
   - forms and validation, pagination, error messages, user-visible strings
   - how dependencies are registered and how routes are declared
   - import style (package or relative) and naming
4. **Find the commands.** Is the Flutter version pinned with FVM? What is the code generation command? Are there flavors or `--dart-define` files? Is there a format or lint step beyond `flutter analyze`?
5. **Write the profile** between these markers in the project's `AGENTS.md` (create the file if needed, never edit outside the markers). If the developer did not ask for the profile itself, show it first and write it once they agree:

```
<!-- flutter-ai-kit:profile:start -->
## Project profile
- Stack: <state, DI, routing, network, storage>
- Layout: <lib/ layers or feature folders>
- Exemplar feature: <path>
- Conventions: <5 to 10 short lines, each naming the file that shows it>
- Commands: <fvm prefix if any; codegen; analyze; run with flavor>
- Conflicts: <where the docs and the code disagree, for example a README command that does not match the launch configuration; do not resolve them>
- Unknown: <anything you could not determine>
<!-- flutter-ai-kit:profile:end -->
```

   If `AGENTS.md` has no `<!-- flutter-ai-kit:start` block (the skills-only and plugin installs do not write it), offer to add the always-on working rules from `assets/AGENTS.block.md`, with `__VERSION__` replaced by `manual`, above the profile. Ask first; `dart tool/install.dart` adds and updates the same block automatically.

6. **Check for the official Flutter and Dart skills.** Look in `.agents/skills/`, `.claude/skills/`, `.github/skills/`, `.grok/skills/` and the agent's plugin list for the skill sets from the Flutter team (`flutter/agent-plugins`) and the Dart team (`dart-lang/skills`); their skill names are listed in those repositories. Do not install anything. If they are missing, tell the developer once, with the commands below, and let them choose, because the two sets overlap each other and installing every skill is a lot of instructions to add to a repository. Record `Official skills: installed | not installed | not checked` under Unknown or Commands.
   - Any agent (installs into `.agents/skills`), from the project root: `npx skills add flutter/agent-plugins --skill '*' --agent universal --yes` and `npx skills add dart-lang/skills --skill '*' --agent universal --yes` (drop `--skill '*'` to choose skills). Claude Code: `claude plugin marketplace add flutter/agent-plugins`, then `claude plugin install dart-flutter@dart-flutter`. Other clients: https://docs.flutter.dev/ai/agent-skills
   - Skills bundled by the project's own dependencies: `dart run skills@ get` lists and installs them (https://dart.dev/blog/skills-cli-1-0-bundle-and-distribute-ai-agent-skills-for-your-packages).
   - Checked 2026-11-04. The install page did not list skill names or an update command; re-running the install command is the likely update, not confirmed.
7. **Ask at most five questions** about anything ambiguous or contradictory (for example two state management styles in one repo: which one is the target?). Do not fill gaps with assumptions; list them under `Unknown`.

## Rules

- Keep the profile under 40 lines. It is loaded into every task, so every line must change what an agent would do.
- Describe what the code does today, not what you would prefer.
- If `AGENTS.md` or another file already contains detailed project rules, do not restate them. Keep the profile to what the rules do not say: the exemplar feature, verified commands, and conflicts between the rules and the code. Never edit the existing rules.
- If the repository already has a profile block, update it in place and say what changed.
