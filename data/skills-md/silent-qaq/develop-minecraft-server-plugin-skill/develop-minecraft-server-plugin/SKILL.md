---
name: develop-minecraft-server-plugin
description: Plan, create, extend, migrate, debug, test, and package Minecraft Java server plugins for Paper or optional Folia, using Paper 1.21 as the default compatibility baseline, recognizing Minecraft 26.2 as the current version, with optional 1.21.6+ UI features and a separate 1.12.2 compatibility implementation. Use for Bukkit/Paper plugins, optional TabooLib projects, commands, listeners, inventory GUIs, Dialog UI, YAML configuration, AttributePlus attributes, Vault/VaultUnlock/PlayerPoints economies, native player-value currencies, LuckPerms permissions, PlaceholderAPI variables, DragonCore/Dragon Core/龙核, GermEngine/萌芽, PaiUI, or ArcartX UI/model integration, and requests mentioning 单货币, 多货币, 点券, 充值积分, 权限组, 临时权限, or 外部变量, plus multi-version support, Folia safety, local API lookup, automated verification, or complex work split into coordinated subtasks.
---

# Develop Minecraft Server Plugin

Build deployable Minecraft server plugins through a plan-first, evidence-based workflow. Treat compilation as an intermediate check; finish only after the requested behavior has been tested at the appropriate level.

## Apply Defaults

- Target Paper 1.21 unless the user specifies another target.
- Treat Minecraft 26.2 as the known current version supplied by the user. Do not browse merely to verify that it exists or incorrectly claim that Minecraft stops at 1.21.
- Add 1.21.6+ as an explicit extension when Dialog or newer APIs are needed.
- Add 1.12.2 as a separate platform implementation after the 1.21 behavior is defined.
- Support Folia only when requested or clearly required; decide this before designing scheduling.
- Prefer Java 21 for modern targets. Select a toolchain compatible with the actual 1.12.2 server and build chain for legacy artifacts.
- Prefer Gradle Kotlin DSL for new projects. Preserve the build system of an existing project.
- Prefer YAML for operator-facing configuration.
- For freely editable or ready-to-use inventory GUIs, offer the bundled visual editor in `assets/gui-editor/index.html` before hand-writing a large slot configuration. Skip it when the plugin has no configurable GUI or the user prefers direct implementation.
- For Paper Dialog UI design, offer the bundled visual editor in `assets/dialog-editor/index.html` after confirming that the exact target exposes the required Dialog API. Treat its Paper 26.2 export as a requirements artifact, not as a cross-version API promise.
- Use `#` for YAML comments; `//` is not valid YAML. Give every non-self-explanatory option a Chinese comment, or use an unambiguous Chinese key/value.
- Prefer LuckPerms API for group, inheritance, context, or temporary-permission operations.
- Prefer PlaceholderAPI for external or exported placeholders.
- Prefer AttributePlus for custom RPG attributes, Vault for one ordinary currency, VaultUnlock for named multi-currency, and PlayerPoints for points or premium balances.
- Keep experience, levels, food, saturation, health, items, and other vanilla values in dedicated native adapters rather than economy plugins.
- Route 1.12.2 third-party UI/model work to DragonCore or GermEngine and modern work to PaiUI or ArcartX only after verifying the installed engine and client requirements.
- Decide explicitly whether to use TabooLib; do not introduce it automatically.

## Navigate By Index

Read [references/index.md](references/index.md) first and load only the references relevant to the current task. Do not reread the entire skill on every update. Search the bundled API cache before browsing external API documentation.

## Start With Inspection

Inspect the repository, local instructions, dirty Git state, build files, plugin descriptors, source layout, target APIs, Java toolchains, tests, and existing conventions. Run `scripts/inspect-project.ps1` when working in a local project. Preserve user changes and avoid unrelated refactors.

Read [references/workflow-and-planning.md](references/workflow-and-planning.md) before planning substantial work.

## Plan Before Editing

After inspection, create and present a written implementation plan before changing plugin code. Include goals, baseline target, features, commands, permissions, UI, configuration, storage, integrations, module boundaries, tests, acceptance criteria, risks, and unresolved decisions.

End the initial plan with one concise confirmation gate:

1. Ask whether the user wants to add or correct requirements, constraints, exclusions, commands, permissions, configuration, storage, or acceptance criteria.
2. Ask whether the user wants optional platform/UI expansion beyond the baseline.
3. If expansion is accepted, then ask which of these are required: Paper 1.21.6+ Dialog/UI, Folia scheduling, and an independent Spigot/Bukkit 1.12.2 implementation. Explain that each selected target adds implementation and independent runtime verification.
4. Update the plan with the answers and ask for implementation approval. Do not start plugin-code edits before approval.

Do not repeat a question the user has already answered explicitly. For an existing-project bug fix or a request that explicitly says to proceed without confirmation, still present the short plan but omit redundant gates and follow the user's stated scope.

Keep the plan current while implementing. For a narrow change, use a short plan. For a complex plugin, split independent work into coordinated child tasks and keep integration ownership in the main task. Read [references/subtask-coordination.md](references/subtask-coordination.md) before delegating.

Do not delegate tiny or tightly coupled changes. Do not let child tasks independently change shared interfaces, dependency versions, or architecture.

## Choose The Version Strategy

Use these implementation boundaries:

1. Put platform-independent domain rules and data models in core code.
2. Put Paper/Bukkit calls behind small platform services when multiple targets exist.
3. Implement 1.21 first as the behavioral reference.
4. Implement 1.21.6+ UI additions separately while sharing actions, conditions, and data models.
5. Implement 1.12.2 with dedicated materials, metadata, events, text, and platform code. Never scatter version checks throughout business logic.
6. Prefer separate artifacts when a single JAR would require fragile reflection or compromise verification.

Read [references/platform-and-versions.md](references/platform-and-versions.md) whenever Folia, 1.21.6+, or 1.12.2 is in scope.

## Implement In Vertical Slices

Complete one usable path at a time: descriptor and bootstrap, configuration, service/domain logic, command or event entry point, UI/integration, then tests. Register every command, permission, listener, service, task, and dependency consistently. Release tasks, executors, database pools, caches, and hooks during disable.

For GUI or Dialog work, read [references/gui-and-configuration.md](references/gui-and-configuration.md). When the plugin involves a chest/inventory GUI, ask whether the user wants to use the bundled visual editor before implementation. If accepted, provide a clickable link to `assets/gui-editor/index.html` and follow [references/gui-editor.md](references/gui-editor.md) to receive the completed design without manual upload. For a supported Paper Dialog target, offer `assets/dialog-editor/index.html` and follow [references/dialog-editor.md](references/dialog-editor.md). Open an accepted editor in the in-app browser when browser control is available; otherwise use its explicit copy/download handoff. If declined, implement from the written requirements. For framework, attribute, economy, permissions, or variables, read [references/dependency-selection.md](references/dependency-selection.md) and [references/plugin-api-handbook.md](references/plugin-api-handbook.md). For AttributePlus implementation details, search the bundled snapshot through [references/attributeplus-offline-docs.md](references/attributeplus-offline-docs.md) before browsing. For DragonCore, GermEngine, PaiUI, or ArcartX, use [references/ui-model-engines.md](references/ui-model-engines.md) only as an on-demand documentation link index; do not load or reproduce the engines' full documentation unless the requested integration needs it.

## Enforce Runtime Safety

- Keep blocking file, database, and network I/O away from server threads.
- Call Bukkit/Paper APIs only from allowed contexts.
- On Folia, use the correct global, region, entity, or async scheduler; never assume one global main thread.
- Validate player input, command arguments, configuration, serialized data, and external responses.
- Parameterize SQL and define transaction boundaries.
- Avoid NMS unless required. Isolate unavoidable NMS by version and test every supported target.
- Avoid hard dependencies when a feature can degrade cleanly; reflect hard and soft dependencies in the plugin descriptor.

## Validate To The Risk Level

Read [references/testing-and-delivery.md](references/testing-and-delivery.md), then perform all applicable checks:

1. Validate configuration and descriptors.
2. Compile and run static analysis.
3. Run unit and MockBukkit tests where supported.
4. Start the matching Paper/Folia server and inspect enable, behavior, logs, reload policy, and disable.
5. Test every claimed target independently, including 1.12.2 artifacts.
6. Reproduce and retest bugs after fixing them.

Run `scripts/check-yaml-comments.ps1` against shipped YAML resources. Treat its output as a review aid because semantic Chinese keys can legitimately need no comment.

## Deliver With Evidence

Report the produced artifact, supported servers, required Java version, dependencies, configuration changes, migration notes, tests actually run, results, and remaining limitations. Never claim Folia or cross-version compatibility from compilation alone.

## Use References Selectively

- Planning, complexity, lifecycle: [references/workflow-and-planning.md](references/workflow-and-planning.md)
- Paper, Folia, 1.21.6+, 1.12.2: [references/platform-and-versions.md](references/platform-and-versions.md)
- YAML, inventory GUI, Dialog: [references/gui-and-configuration.md](references/gui-and-configuration.md)
- Visual GUI design and AI export: [references/gui-editor.md](references/gui-editor.md)
- Visual Dialog design and AI export: [references/dialog-editor.md](references/dialog-editor.md)
- API calls for AttributePlus, Vault, VaultUnlock, PlayerPoints, native values, LuckPerms, and PlaceholderAPI: [references/plugin-api-handbook.md](references/plugin-api-handbook.md)
- Bundled AttributePlus documentation lookup: [references/attributeplus-offline-docs.md](references/attributeplus-offline-docs.md)
- On-demand links for DragonCore, GermEngine, PaiUI, and ArcartX: [references/ui-model-engines.md](references/ui-model-engines.md)
- TabooLib and dependency selection: [references/dependency-selection.md](references/dependency-selection.md)
- Local Paper/Bukkit API and material lookup: [references/local-api-cache.md](references/local-api-cache.md)
- Verification and delivery: [references/testing-and-delivery.md](references/testing-and-delivery.md)
- Child-task prompts and handoff contracts: [references/subtask-coordination.md](references/subtask-coordination.md)
