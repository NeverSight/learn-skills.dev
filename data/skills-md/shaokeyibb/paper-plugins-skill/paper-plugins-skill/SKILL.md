---
name: paper-plugins-skill
description: Guidance for building, updating, reviewing, or debugging Minecraft Paper server plugins in Java or Kotlin. Use when Codex works on Paper/PaperMC plugin projects, Gradle setup, paper-plugin.yml or plugin.yml descriptors, commands, Adventure components, Dialog API UI, PDC, item data components, registries, recipes, scheduler or Folia-safe code, events, plugin messaging, configuration, persistence, databases, or Paper API migration from Bukkit/Spigot patterns.
---

# Paper Plugins Skill

Use this skill to produce maintainable Paper plugins that follow current Paper conventions without assuming a specific project, namespace, command name, or gameplay domain.

## Workflow

1. Identify the target Minecraft/Paper version from `build.gradle`, `build.gradle.kts`, `gradle.properties`, `paper-plugin.yml`, `plugin.yml`, README, CI, or the user's request. Do not silently upgrade an existing plugin to the latest API.
2. Read only the references needed for the task:
   - Project setup, Gradle, descriptors, bootstrap, and lifecycle: `references/project-setup.md`
   - Commands and Brigadier registration: `references/commands.md`
   - Adventure text, MiniMessage, dialogs, display entities, and particles: `references/text-ui-and-effects.md`
   - Persistent data, configuration, serialization, and database boundaries: `references/data-storage.md`
   - Items, data components, registries, and recipes: `references/items-registries-recipes.md`
   - Scheduler, Folia, events, plugin messaging, and concurrency: `references/runtime-integrations.md`
   - Review and release checks: `references/review-checklist.md`
3. Prefer Paper APIs over legacy Bukkit or Spigot patterns when Paper provides a stable replacement.
4. Keep version-sensitive APIs behind small adapters or localized modules. This is especially important for experimental Paper APIs, data components, dialogs, and registry mutations.
5. Validate with the repository's build command. For Gradle projects, use `./gradlew build` on POSIX shells or `.\gradlew.bat build` on Windows PowerShell unless the repository documents another command.

## Defaults For New Projects

- Use Gradle with `compileOnly("io.papermc.paper:paper-api:<target-version>")`.
- Use the latest official Paper docs only when the user asks for a new plugin or explicitly requests an upgrade.
- Use Java toolchains matching the Paper docs for the chosen API version. As of the 2026 Paper docs, new examples use Java 25 and Paper API `26.1.2`, but existing projects may target older versions.
- Use `plugin.yml` for broad Bukkit-compatible plugins. Use `paper-plugin.yml` when the plugin intentionally depends on Paper-only features such as bootstrapper, loader, or lifecycle-era registry work.
- Use Adventure `Component` and MiniMessage for user-facing text. Avoid legacy color codes except at compatibility boundaries.
- Use `NamespacedKey` or Adventure `Key` with the plugin's own namespace. Never hard-code a source-project namespace.

## Paper-Specific Guardrails

- Treat `paper-plugin.yml` as Paper-only and experimental. Do not use it unless the plugin needs Paper-only descriptor features.
- Register Brigadier commands through `LifecycleEvents.COMMANDS` so command state survives reload-style lifecycle events.
- Do not call most Bukkit/Paper world, entity, inventory, or scheduler APIs from arbitrary async threads. Use the scheduler model appropriate to the server target.
- If Folia compatibility is required, avoid global-main-thread assumptions and prefer entity, region, or async schedulers as appropriate.
- Treat Dialog API and Data Component API as version-sensitive. Confirm the target version and official docs before large UI or item-model changes.
- Use Persistent Data Container for small plugin-owned metadata on items, blocks, entities, and chunks. Use files or databases for queryable, relational, or large data.
- For database work, keep JDBC and blocking I/O off the server tick thread, and return to the correct scheduler before touching live game state.

## Documentation Sources

Prefer official Paper documentation and Javadocs when the local repository does not already pin the target behavior:

- Paper docs: https://docs.papermc.io/paper/dev/
- Project setup: https://docs.papermc.io/paper/dev/project-setup/
- Paper plugins: https://docs.papermc.io/paper/dev/getting-started/paper-plugins/
- Plugin descriptor docs: https://docs.papermc.io/paper/dev/plugin-yml/
- Paper Javadocs: https://jd.papermc.io/paper/

When online docs conflict with a pinned project version, prioritize the pinned version unless the user requested an upgrade.
