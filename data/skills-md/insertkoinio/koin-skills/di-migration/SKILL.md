---
name: di-migration
description: >
  Migrate Kotlin / Android / KMP projects to Koin 4.x with the Koin Compiler Plugin:
  Hilt, Dagger 2, Toothpick, Kodein and Metro to Koin, Koin 3.x to 4.x, the Compiler
  Plugin added to a Koin DSL project (every DSL form compile checked, Classic included),
  and Koin KSP annotations to the Compiler Plugin. Progressive, module by module, keeping
  the old container running until the last binding moves. Use when the user wants to
  migrate, convert or switch DI frameworks, remove Hilt / Dagger / Toothpick / Kodein /
  Metro, upgrade Koin, move off KSP, make the Koin graph compile safe or verified at
  build time, convert Koin DSL to Compiler Plugin DSL, or pastes Hilt / Dagger /
  Toothpick / Kodein / Metro module code to convert — "replace Hilt with Koin", "move
  away from Dagger", "Kodein to Koin", "Metro to Koin", "Koin KSP to compiler plugin",
  "upgrade to Koin 4", "make Koin compile safe". Adding Koin to a project with no DI is
  koin-setup.
---

# DI Migration Skill

Migrate Kotlin/Android/KMP projects between DI frameworks, targeting **Koin 4.x
with the Koin Compiler Plugin**. The per-source reference files in
`references/` hold the concrete mappings and examples — this file is the
contract and the workflow.

## Shared references — read first

Read `references/rules.md` first (non-negotiable). `references/index.md` lists
the other shared references and what each owns — read the owner of any detail
you need instead of inferring from memory.

## Migration rules

1. **Target style by source** — the default, stated to the user in the plan
   (Step 2); they can choose otherwise (`rules.md` §1, an explicit choice):
   - **Hilt / Dagger / Toothpick / Metro** → Annotations
   - **Koin KSP annotations** → Annotations
   - **Koin 3.x, Classic or Constructor DSL** → keep the current form. Compile
     safety comes from adding the Compiler Plugin (Step 3), which checks every
     DSL form. Converting to Compiler Plugin DSL is an optional style step, on
     the user's choice (`references/dsl-to-compiler.md`)
   - **Kodein** → Compiler Plugin DSL
2. **Koin KSP projects** — follow the removal checklist in
   `references/ksp-to-compiler.md`.
3. **Progressive migration is universal.** Never rewrite existing DI modules in
   place. Create a new Koin module alongside the old container, move definitions
   one feature/leaf-module at a time, validate after each one (see loop below),
   remove the old framework only when the last binding has moved (Step 8).
4. **Setup is part of the migration.** This skill sets Koin up itself — Step 3
   (Gradle, `references/gradle.md`) and Step 5 (wiring,
   `references/entry-points.md`) — with the style from rule 1.

## Supported Migration Paths

All target **Koin 4.x + Koin Compiler Plugin**. Read the relevant reference
before generating code. If the source is ambiguous, ask.

| Source                    | Reference File                     |
|---------------------------|------------------------------------|
| Hilt (+ Dagger)           | `references/hilt-to-koin.md`       |
| Dagger 2 (no Hilt)        | `references/dagger-to-koin.md`     |
| Toothpick                 | `references/toothpick-to-koin.md`  |
| Kodein                    | `references/kodein-to-koin.md`     |
| Metro                     | `references/metro-to-koin.md`      |
| Koin 3.x                  | `references/koin3-to-koin4.md`     |
| Koin DSL                  | `references/dsl-to-compiler.md`    |
| Koin KSP Annotations      | `references/ksp-to-compiler.md`    |

**Not covered by this skill:** greenfield projects and manual-DI /
service-locator code have no source framework to map from. Use the
`koin-setup` skill instead.

## Progressive Migration

### Where to start — module selection

**Recommended approach: leaf-first, smallest-first, then ack-and-grow.**

Two strategies exist for ordering a multi-module migration:

| Strategy | When | Trade-off |
|----------|------|-----------|
| **Leaf-first** (small leaf/feature modules first, then grow toward core) — **default** | Almost every project | Small early wins, validates the whole workflow on a low-risk module, builds team confidence with Koin idioms, surfaces tooling/Gradle gotchas before they hit critical code |
| **Bottom-up** (core / data first, then features above) | Rare — only if the core graph is tiny and unambiguous, and feature modules already compile against an interface boundary | Avoids bridging from core into Koin (because nothing depends *on* feature modules), but blocks all feature work until the foundational layer is rewritten and validated |

**Default recommendation: leaf-first.** Start with the **smallest, most peripheral
module** you can find, bridge any dependencies it still has back into the legacy
container, validate the full per-module loop end-to-end, then **get explicit user
acknowledgement** before picking the next target. Each subsequent target moves
one level toward `core` / `data` / `app`. Never jump straight to `AppModule`.

Rank candidates inside the leaf-first strategy and propose the top 1–3; ask
for confirmation before any code:

1. **Leaf modules with zero dependants** (nothing will break upstream)
2. **Few bindings** (≤5) — small blast radius, quick win
3. **Simple binding types only** — no custom scopes, assisted inject, multibindings, Workers
4. **Feature modules, not `core` / `common`** — limited call-site reach
5. **Self-contained call sites** — only used inside their own Gradle module

After each module migrates and passes validation (Step 7), **explicitly ask the
user before moving on**: "next target?", with a fresh ranked list reflecting
what's now eligible. This ack-per-module rhythm is what keeps the migration safe
— it prevents Claude from chaining several migrations without the user catching
a regression.

Defer: `AppModule`, `@EntryPoint`-exposed bindings, Worker/ContentProvider-used
bindings, custom component hierarchies.

Present a ranked table (`Rank | Module | Bindings | Dependants | Complexity |
Recommended?`) before proceeding.

### Runtime check setup

When: **Koin source** (Koin 3.x, Classic/Constructor DSL, Koin KSP) — after the
plan is confirmed, **before Step 3**, on the current version before any change.
**Other source** (Hilt, Dagger, Toothpick, Kodein, Metro) — before the first module.

Detect Kotzilla ("Detect first" in `references/kotzilla.md`). Not in place, or
MCP only (no SDK) → propose it **once, here** (handoff rules), because a
baseline can't be captured once code has changed. For a migration it checks
each moved module (loop item 5) and diagnoses a Koin crash, then shows how the
app behaves once migrated. Accepted → used from here on, no new offer.
Then, if the SDK is in place:

- **Koin source** — run the app on the current version to capture a
  **baseline**: the same definitions, before any change.
- **Other source** — run the app on the current version to capture an
  **app-level baseline** (startup, screens, ANRs): the SDK records them without
  Koin. The old container's instances aren't visible, so each migrated
  definition is checked against the behavior its source binding meant
  ("Expected behavior" in `references/kotzilla.md`, with the scope mapping of
  the per-source reference).

Declined → the loop runs without item 5, and Kotzilla isn't offered again.

### Per-module validation loop

Migration is a loop, not a waterfall. For **each** module (Steps 4, 6 and 7 of
the workflow):

1. Move the definitions into the new Koin module
2. Update call sites inside that module's Gradle scope
3. Compile — whole project green; fix what the Compiler Plugin reports
   (`references/rules.md` §6). When the report isn't enough and the Kotzilla
   MCP is connected, `koin_diagnose` on the full `[KOIN-…]` error text —
   optional
4. **Runtime smoke test** — run the app or tests, exercise one code path that
   uses the migrated bindings. A green build is not enough; wiring errors
   (missing `androidContext`, wrong scope, stale bridge call) only surface at
   runtime. A Koin crash: Kotzilla MCP connected → `koin_diagnose` with the full
   stack trace (MCP alone, no SDK); not connected → diagnose from the stack
   trace and `references/rules.md`, and propose the MCP once (handoff rules in
   `references/kotzilla.md`) unless already declined
5. **Kotzilla check** (SDK in place) — on a new app version, run the path that
   resolves the migrated definitions and check each one — lifetime, scope,
   performance, memory — against the baseline or its expected behavior
   (`references/kotzilla.md`). Report each definition
   as verified, a mismatch, or not verified (no session). A mismatch — a
   `@Singleton` migrated to a factory, a scope never closed, a new main-thread
   cost — is fixed before the commit. Bindings still behind a bridge are
   reported as not checkable yet.
6. Commit as a self-contained unit before picking the next module

The loop is `references/rules.md` §10 applied to migration: a small project
(one Gradle module, about five bindings) migrates in one verified step; a
single-module app with more is split by feature (a screen's ViewModel and what
it needs), the rest staying in the old container.

Do not batch un-validated migrations. If validation fails, fix or revert before
touching anything else.

### Bridging with the existing DI

Koin definitions that still need bindings from the old container use a bridge
co-located in the consumer module — per source, with startup ordering:
`references/bridging.md`.

## Migration Workflow

- **Once:** Steps 0 → 3. For a Koin source, Step 3 is the whole-project
  Gradle/plugin swap; for another source, it adds Koin next to the old framework.
  A Koin DSL source kept in its form needs only Step 3, a green build and the
  smoke test (loop items 3–5).
- **Per module:** Steps 4, 6 and 7 (the loop above). Step 5 (app wiring) runs
  with the first module, and again only when a new app entry point appears.
- **At the end:** Step 8, after every module has been migrated and validated.

### Step 0 — Detect

- Koin 4 + Compiler Plugin already in place, nothing else to move → nothing to
  migrate: the **`koin`** skill takes the task.
- No DI at all → **`koin-setup`**.
- Kotlin below `2.3.20` and the bump is impossible → stop and say so
  (`references/rules.md` §3); only the Koin runtime upgrade without the plugin
  remains (`references/koin3-to-koin4.md`).

### Step 1 — Inventory

Scan for every DI-related file: modules, components, entry points, qualifiers,
scopes, workers. Classify each binding (singleton, factory, scoped, assisted,
multibinding, viewModel). Flag anything needing manual attention (custom scopes,
reflection-based injection). Count total bindings.

Present as a table (`# | Source File | Binding Type | Scope | Notes`) before proceeding.

### Step 2 — Plan

Produce:
- Target style (migration rule 1) — the default for this source; the user can
  choose otherwise
- Mapping table: source construct → target (from reference file)
- **Ranked migration candidates** (see "Where to start" above) — top 1–3, ask
  user to confirm first target
- Risk flags: anything that can't be 1:1 translated
- Steps that can't be split: when the old container **constructs Activities or
  Receivers** (per-source reference), they move with the bindings they use, or
  stay behind "The other direction" in `references/bridging.md`. Say which
- Gradle changes and version requirements
- Bridging plan if bindings will cross containers during migration

**Stop here.** Present the inventory and the plan, then end your turn: no file
edits until the user confirms the plan, the first target and any Kotlin bump
(`references/rules.md` §3). Skip the stop only when the user's message already
confirms them. Declined → Koin source: **`koin`** continues the task in the
current setup. Other source (Hilt, Dagger, Toothpick, Kodein, Metro): the work stays in
the existing container — `koin` only if Koin already runs alongside it.

### Step 3 — Gradle Setup

Koin source: runtime check setup first (see above).

**Versions** — per `references/rules.md` §3 (latest on Maven Central, Kotlin
bump cascade).

Then produce the Gradle diff:

1. Add Koin per `references/gradle.md` — only the artifacts the project needs.
   The old framework stays until Step 8; a Koin source swaps Koin KSP for the
   Compiler Plugin here, for the whole project (`references/ksp-to-compiler.md`)
2. Present as a diff with the version source noted (latest Maven Central
   release, or defaults)

### Step 4 — Generate Module Code

Use the target style from migration rule 1. Produce BEFORE/AFTER blocks per
module, following the relevant per-source reference and the style's cheat
sheet. KMP → `expect`/`actual` at any granularity (`@Module` class, annotated
class, or plain function).

### Step 5 — Wire Up Application

Configuration per `references/rules.md` §5 — code in the style's cheat sheet
("App entry point"). Annotations: `@KoinApplication` + `startKoin<App>`, each
Gradle module root discovered. DSL: `startKoin` loads one app module that
`includes(...)` the migrated modules. Old container still running → both start
in the `Application` — "Two containers at startup" in `references/bridging.md`.

### Step 6 — Update Injection Sites

Field injection (`@Inject lateinit var`): at framework entry points (Activity,
Fragment, Service…) → the Koin API for that entry point (`references/entry-points.md`);
in normal classes → constructor injection, never `KoinComponent` (`references/rules.md` §8).
`hiltViewModel()` → `koinViewModel()`, scope access → `references/scopes.md`. Remove
`@AndroidEntryPoint` per entry point once it no longer uses the old container;
`@HiltAndroidApp` (and the Dagger component, Toothpick root scope, Kodein
`DI` creation or Metro graph) stays until Step 8 — bridges read through it. Show each changed file with before/after.

### Step 7 — Per-module validation

**Run after every module, not only at the end.**

1. Update the module's tests first: `KoinTestRule` or `startKoin` in test setup,
   mock replacement (`references/testing.md`). Graph verification is
   compile-time (Compiler Plugin) — no new `checkModules { }` / `verify()`
   tests. Show before/after for existing test files.
2. Run the loop's checks (items 3–5 of "Per-module validation loop" above),
   then commit (item 6).
3. **Stop and ask the user for explicit acknowledgement before picking the next
   target.** Re-rank the remaining candidates (something that was a leaf before
   may no longer be) and propose the top 1–3. Never chain multiple module
   migrations without an ack — the per-module rhythm is what makes regressions
   catchable.

### Step 8 — Final Cleanup

When the last module has been migrated and validated:

- [ ] All old DI annotations removed (`@Inject`, `@Module`, `@Component`, `@HiltAndroidApp`, etc.)
- [ ] No references to old DI generated classes (`Dagger*Component`, `*_Factory`, `*_MembersInjector`)
- [ ] No imports from old DI packages
- [ ] Every bridge call (`dagger<T>()` / `toothpick<T>()` / `kodein<T>()` / `@Component` delegation) removed, with `MetroBridgeModule` and the Metro graph holder
- [ ] Compile-time graph check on
- [ ] Old DI deps removed from `build.gradle.kts`; KSP/kapt plugins removed if no longer needed
- [ ] ViewModel injection works in Activities, Fragments, Composables
- [ ] Scoped bindings match original lifecycle semantics — checked in Kotzilla
      session data when the SDK is in place
- [ ] Tests pass

## Parameter Resolution

Constructor and function parameters (`T`, `T?`, `Lazy<T>`, `List<T>`,
`@InjectedParam`, qualifiers, properties) are resolved by the Compiler Plugin —
see "Parameter resolution" in `references/koin-compiler-plugin-dsl.md` and "Parameters &
qualifiers" in `references/koin-annotations.md`. JSR-330 annotations from the
source framework are reused as-is.

## Edge Cases

Read the relevant reference section:

- **Assisted Inject** → `@InjectedParam` + `parametersOf()`; an assisted
  ViewModel call site with a `key` keeps it (Compose in `references/entry-points.md`)
- **Multibindings (Set/Map)** → each element its own definition bound to `T`,
  consumers inject `List<T>` — "Multibindings" in `references/dagger-to-koin.md`
- **Custom Scopes, subcomponents, child graphs** → `references/scopes.md` —
  a child graph with its own lifetime maps to a scope, not a factory: the
  archetype when it follows an Activity, Fragment or ViewModel, otherwise a
  custom scope ("Choose the scope"); a runtime input → "Scope with a runtime value"
- **Graph inputs** (`@BindsInstance`, graph factory arguments) → "Values known
  at startup" in `references/entry-points.md`
- **Component Dependencies** → module includes + scoping
- **Lazy / Provider** → `Lazy<T>` constructor parameter (`references/principles.md` rule 7);
  `Provider<T>` for a fresh instance per call → "Lazy and Provider" in `references/dagger-to-koin.md`
- **WorkManager**, **Navigation** → `references/entry-points.md`
- **JSR-330 annotations** → handled natively by the Koin Compiler
- **Custom qualifiers** → reusable as-is

## Kotzilla

Proposed at "Runtime check setup", and the MCP once on a Koin crash (loop item
4) if not declined. Once in place, used for Koin crashes (loop item 4) and the
per-module check (loop item 5). A runtime question during the migration ("is it
slower now?") → Kotzilla when in place, otherwise proposed — unless declined,
then one line (handoff rules). Rules and expected behavior:
`references/kotzilla.md`.

## Context

### Koin Compiler Plugin

- Plugin ID: `io.insert-koin.compiler.plugin` — versions in `references/rules.md` §3
- Compile safety: full graph + call sites, no per-module check — `references/rules.md` §6
- Supports `@Module`, `@Configuration`, `@KoinApplication`, `@Monitor`, top-level functions
- Full KMP support — no per-target config

### Migration Benefits

When explaining why Koin: "Koin in short" in `references/index.md`. Plus, for a
migration: progressive — Koin and the old container coexist until the last
binding moves.
