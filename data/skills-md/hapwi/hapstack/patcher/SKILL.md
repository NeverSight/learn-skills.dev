---
name: patcher
description: Run React Doctor and configured shadcn lint diagnostics, with an optional
  Improve audit, local implementation plans, and tracked fixes. Use when the user
  invokes patcher or patcher improve, asks for React Doctor review or fixes, or requests
  a React Doctor score such as 100/100.
metadata:
  version: 0.3.2
  short-description: Diagnose and fix React and design-system findings
license: MIT
---

# Patcher

Use React Doctor, existing project checks, and applicable `@shadcn/lint` rules to inspect React projects and make focused fixes when requested. Detect and report the stack before running diagnostics. Preserve the project’s package manager, framework, and configured linter by default. Vite+ with Bun and bundled Oxlint is an optional setup choice, not a requirement for diagnosis or a score of 100. Use Vite+ commands only in configured projects.
`$patcher` selects React Doctor. `$patcher until 100` or a follow-up such as "fix until 100" means diagnose, fix, and recheck until the project scores 100/100, then run the agreed project checks and fix their findings. This complete workflow is implied without the user repeating the check request; stop when the score and agreed checks pass or a concrete blocker prevents further safe progress.

Read [references/cli-reference.md](references/cli-reference.md) when exact flags, configuration, or output handling details are needed.

## Select the mode

Run an **Improve audit** only when the user explicitly requests it. Do not offer it or ask whether to include it during a patcher workflow, follow-up, or fix loop. An explicit `patcher improve` selects Improve immediately and runs the audit without asking for confirmation or automatically running React Doctor or lint; a request for both selects both.

Read [references/improve.md](references/improve.md) only when Improve is selected or its findings, plans, or status are requested. Improve supports numbered findings, local plans, `improve 1–4` / `fix 1–4`, `fix until done`, and `improve status`. In an active Improve workflow, “until done” refers to selected Improve plans; “until 100” retains the React Doctor workflow below. Report the two outcomes separately.

Perform patcher work with the same agent in the current working directory and branch, preserving staged, unstaged, and relevant untracked changes. Do not spawn subagents, require a clean tree, or automatically create branches/worktrees, stash, commit, merge, or push. Plans and selected fixes remain local.

## Portable configuration

Read [the runtime contract](../hap-mode/references/runtime.md) for host features, action authority, and T3 PR registration/watching.

Read [configuration](../setup-hapstack/references/configuration.md) when that bundled file is available. Project settings take precedence over global settings. With no configuration, preserve the current tooling, follow repository checks, and offer optional changelog policy setup only when the user requests it. If this skill was installed alone, these defaults are sufficient. A configured tooling preference does not authorize migration or dependency changes.

## Project changelog policy setup

For all modes, including Improve, inspect the target project's root `AGENTS.md`
for a `agent-changelog` block or an existing changelog policy. The bundled
[policy template](assets/changelog-AGENTS.md) is the authoritative text.
Read [policy setup](references/changelog-policy.md) when installation,
reconciliation, or an update is needed. An identical marked block needs no work.

Offer missing policy setup only when the user requests policy setup or has selected that preference in the package configuration. Offer it once alongside other setup choices; reuse prior
acceptance or refusal in the conversation and continue independent diagnostics
while awaiting a choice. An explicit request such as “patcher, set up the changelog
policy” authorizes this setup without running diagnostics. Diagnosis, review, and
status-only requests remain read-only for policy files unless setup is explicitly
selected. Do not treat authorization for code fixes as initial policy consent.

## Detect the project and agree on setup

1. Read repository instructions and inspect the working tree, preserving existing user changes. Identify the app and workspace roots.
2. Inspect dependencies, framework configuration, scripts, package-manager declarations and lockfiles, and lint configuration. Report the framework (such as Next.js or React with Vite), package manager, Vite+ presence, Oxlint/ESLint setup, Tailwind version, shadcn/ui or custom design-system usage, and which checks actually run. Classify Vite+ as absent, incomplete, or configured: inspect the project dependency, effective configuration, script integration, bundled Oxlint, and package-manager consistency rather than treating a global `vp` executable alone as project setup. Distinguish installed tools from configured and enabled rules. For conflicting package-manager evidence, explain the conflict and resolve it before dependency changes.
3. Compare the detected setup with any explicitly configured tooling preference. With no preference, keep the existing setup. Vite+ with Bun and bundled Oxlint is an available option; `@shadcn/lint` applies to supported Tailwind v4 design systems (shadcn/ui is not required). Next.js and React with Vite remain supported frameworks. Tooling preferences are not diagnostic findings or authorization to replace the framework.
4. For an empty or unconfigured project, ask whether to set up Next.js or React with Vite, clarifying package-manager, linter, and shadcn choices; propose a concrete setup appropriate to the selected framework. Reuse choices already supplied by the user. Do not ask an established Next.js project to choose its framework again merely because lint setup is missing. Without React source there is nothing to diagnose yet; explain that setup is needed before scanning.
5. If tooling required for requested diagnostics is missing, or the user explicitly asks about a different setup, present one combined choice: keep the current setup and run available diagnostics, or configure the proposed tooling. Offer Vite+ migration or completion only when the user requests it or has selected it as a setup preference, stating the intended scope and changes. A general preference for Vite+ or invoking patcher is not project-specific migration approval. If declined or unanswered, preserve existing tools and continue the requested audit and available checks; Vite+ absence alone is not a diagnostic failure or blocker. State the exact changes and coverage gaps. For `@shadcn/lint`, use the base-install or guided-policy choices below; installation alone does not authorize enabling rules. Honor a previous choice to keep the setup; do not repeatedly ask during the fix loop. Continue independent diagnostics while awaiting a setup decision.

Example stack report: “Next.js · Bun · standalone Oxlint · shadcn detected, lint plugin not enabled. Vite+ is not configured. React Doctor and existing lint can run now; shadcn rule coverage requires setup.”

### Authorized setup and migration

This skill requires confirmation before installing project tooling, enabling rules, scaffolding, or migrating configuration because those actions expand a diagnostic/fix request. Prior explicit setup authorization is sufficient. Use `vp install`, `vp add`, and `vp remove` to orchestrate Bun in Vite+ projects, `vp run` for package scripts (including `vp run dev`), `vp exec` for local binaries, and `vp dlx` for external one-off tools. Preserve existing checks and framework commands. Use latest packages for authorized setup, checking compatibility; this is not permission to upgrade unrelated application dependencies.

- For Next.js with Bun, keep Next.js dev/build commands and use the project's existing check scripts. Standalone Oxlint is valid when Vite+ is absent.
- For Vite+ projects, use its bundled Oxlint; do not add a duplicate standalone installation. Register applicable shadcn rules through its lint configuration.
- When Vite+ migration is selected, read the current [migration guide](https://viteplus.dev/guide/migrate) and [migration rules](https://viteplus.dev/guide/migrate-rules), and inspect `vp help migrate`. Use `vp migrate` with options matching the approved scope. Explain dependency, script, config, formatting, and workspace-wide effects before running it. Migration targets the workspace root; approval for one app does not authorize changing unrelated workspace members. Preserve Bun or the approved existing package manager, user edits, and ongoing package updates; reconcile migration changes without overwriting unrelated work. Verify framework compatibility and do not treat migration as converting Next.js to Vite: keep Next.js dev/build commands and invoke their scripts with `vp run dev` and `vp run build`, rather than substituting built-in `vp dev` or `vp build`. Follow current migration preflight and review the changed dependencies, scripts, configuration, and lockfiles. Existing Vite+ setup may need scoped completion rather than a fresh migration; inspect current upgrade versus full-setup behavior and do not select `--full` implicitly. Complete applicable verification with `vp install`, `vp check`, configured tests, and the actual framework build script (or `vp build`/`vp pack` where appropriate); report manual follow-up.

### Detect and set up @shadcn/lint

Inspect dependencies, plugin registration, effective rules and overrides, lint file scope, component imports, and Tailwind theme discovery. Report one of these states:

- **Not applicable:** no supported Tailwind v4 design system. Skip setup prompts and explain the compatibility limitation where relevant; do not upgrade Tailwind implicitly.
- **Absent or incomplete:** the package is missing, unregistered, incompatible, or fails to load. Name the exact missing piece.
- **Base install:** the plugin loads, but no rules are enabled for the relevant UI files. State that setup is complete but design-system enforcement is not enabled.
- **Active:** the plugin loads and configured rules apply to the relevant files. Report those rules and run them without another setup prompt. Scope or discovery gaps must still be reported.

For missing or incomplete setup, offer a concise choice: **base install only**, **guided rule setup**, or **keep current setup and continue patcher**. For a base install already present, offer rule setup or continuing as-is. Combine this with other missing-tooling questions rather than asking twice. Reuse prior choices, including “base install for now”; do not prompt again during the same workflow. Continue available diagnostics regardless of whether optional setup is declined.

Before authorized installation, read the current [official setup guide](https://github.com/shadcn-ui/lint/blob/main/SETUP.md) and [requirements/configuration](https://github.com/shadcn-ui/lint#readme). Check Tailwind v4, Node.js, and linter compatibility, including Vite+'s bundled Oxlint when applicable. Requirements checked on 2026-09-15: Node.js 20.19+, Oxlint 1.80+ or ESLint 9.30+; verify current requirements when installing latest packages. Bun as package manager does not replace this compatibility check.

**Base install:** install the latest compatible `@shadcn/lint` and register it with the existing linter that checks UI files. Preserve ESLint when that is the existing choice; if both linters exist, avoid duplicate registration. If neither exists, propose Oxlint. Use the package owning the lint config, its package manager, and existing workspace conventions. Preserve parsers, scripts, rules, and ignores. Do not enable presets, new rules, or policy overrides. Resolve only necessary component/theme discovery settings from `components.json`, aliases, exports, and source; custom Tailwind components are supported too. Run the relevant lint command to verify configuration loading, separating setup errors from existing findings. Report “base install complete; no new rules enabled,” show where rules belong, and resume patcher with available coverage.

**Guided rule setup:** ask only for unresolved design-policy choices in small steps. Read the existing components, variants, theme, and design guidance first; propose concrete rules, severities, component-directory scopes, and styling contracts with examples. Explain choices such as whether Button callers may change padding or should use an existing size variant. Get approval for the specific policy before enabling it; base-install approval alone is insufficient. Preserve approved exceptions and app-specific workspace settings. Verify enabled rules actually check the intended UI files, then report coverage. Do not invent variants, tokens, contracts, or suppressions merely to silence findings; those can require a design decision. Keep policy guidance grounded in the official [design-system configuration guide](https://github.com/shadcn-ui/lint/blob/main/docs/design-systems.md).

## Diagnose

1. Confirm React source or dependencies and select the app root or supported `--project <name>` in a monorepo. Skip established non-React projects with an explanation.
2. Select the package runner from the existing setup. Examples below use `vp dlx` for Vite+; use `bunx` for Bun without Vite+, or the existing npm/pnpm/Yarn equivalent elsewhere. Keep `react-doctor@latest`; report the resolved version when available and check current help if reference flags differ.
3. Run a full diagnostic inventory unless the user requested changed-file scope:

```bash
vp dlx react-doctor@latest <project-dir> --json --blocking none --diff false
```

For a readable report, replace `--json` with `--verbose`. For changed files, replace `--diff false` with `--diff <base>` or `--staged`; never combine `--diff` and `--staged`.

4. Parse JSON after package-manager progress text. Report the actual score, scope, and error/warning counts. A successful exit with `--blocking none` does not mean there are no findings.
5. Run the configured lint command in the requested scope. For Vite+, inspect `lint.jsPlugins`, `lint.rules`, and `lint.overrides` in `vite.config.*` and use `vp lint`; elsewhere inspect the existing linter configuration and scripts. For applicable Tailwind v4 projects, classify `@shadcn/lint` setup as above and report enabled-rule findings separately from React Doctor. Missing coverage follows the setup choice above and does not prevent other diagnostics.
6. For diagnostics or review only, stop after the report. For fixes or a target score, continue below.

Use `--no-score` or `--no-telemetry` when the score service should not be contacted; explain that a numeric score and share URL will be unavailable. Fetching `@latest` may itself require network access.

## Fix and verify

1. Inspect each finding in context before editing. Make focused manual fixes that preserve intended behavior and follow repository requirements, including changelog and validation rules.
2. Rerun React Doctor and relevant project checks after each coherent batch of changes. Separate targeted validation from repository-wide failures, and investigate whether failures predate the edits.
3. For requests such as "until 100", continue without pausing after each finding. Once a full React Doctor scan confirms 100/100, run the agreed project checks: `vp check` in Vite+ projects (use its package script when appropriate), or the existing lint, type, and formatting check scripts elsewhere. Fix all findings from those checks, including pre-existing warnings, with focused behavior-preserving edits. Include applicable configured shadcn rules, running their separate command if necessary; zero exit status with warnings is not clean. Rerun checks until clean. If fixes changed code or configuration, rerun the full React Doctor scan and resolve regressions. Finish when the final tree has a verified 100/100 and clean agreed checks. If the user keeps a setup with missing checks, report “100/100; available checks passed” with the exact missing coverage rather than claiming full coverage. An inapplicable Tailwind setup is not missing coverage. An accepted base install with no enabled rules is not design-system enforcement; report that limitation without blocking other agreed checks. Never disable checks to obtain a pass; report checks skipped by configuration and remaining React Doctor warnings even at 100.
4. Do not inflate the score by broadly disabling rules or excluding real application code. Use narrow, documented overrides only for verified false positives, generated files, or intentional framework patterns. Use supported `doctor.config.*` files or the `reactDoctor` key in `package.json`.
5. If a fix would require a material product decision or changes beyond the authorized scope, explain the specific issue and ask only for the missing decision. If progress is blocked by tooling or external services, report the last verified score and blocker; never claim an unverified 100. If a fix/check cycle repeats the same finding without progress, stop repeating that approach. Explain the finding, attempted fix, why it remains unresolved, and the specific decision or external change needed. Continue other independent findings when safe; do not loop indefinitely or weaken rules to escape the blocker.

A score-only confirmation is available when a full finding inventory has already been reviewed:

```bash
vp dlx react-doctor@latest <project-dir> --score --blocking none --diff false
```

Do not run `install` or `setup` unless the user asks to install React Doctor guidance into the project.

## Report

Lead with the score and outcome. Keep findings in plain language and avoid raw JSON unless requested. Include:

- Score, framework, package manager, lint/tooling setup, differences from an explicitly selected setup preference, scan scope, and error/warning counts.
- Significant problems or fixes, their impact, and relevant file paths.
- Checks performed, shadcn rule coverage and finding counts, and any failures or remaining limitations.
- The next action only when work remains.

For completed fixes, summarize what changed and the final verified result. For diagnostics only, describe what each significant finding means and how to fix it.
