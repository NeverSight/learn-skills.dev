---
name: ohos-dev-arkui-v1-v2-migration
description: Use when migrating OpenHarmony/HarmonyOS ArkUI state management from V1 (@Component, @State/@Prop/@Link/@Provide/@Consume/@Watch/@Observed) to V2 (@ComponentV2, @Local/@Param/@Event/@Provider/@Consumer/@Monitor/@ObservedV2/@Trace), or assessing migration feasibility. Trigger phrases include "迁移V1到V2", "V1V2迁移", "状态管理迁移", "将@Component改为@ComponentV2", "迁移@State/@Prop/@Link到V2", "migrate V1 to V2". Provides automated analysis (component structure, dependency tracing, API version detection, V1/V2 mixing validation), step-by-step migration guidance, and post-migration validation.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: arkui
  capability: v1-v2-migration
  version: 0.1.0
  status: draft
  tags:
    - arkui
    - componentv2
    - state-management
    - migration
  related-skills: []
---

# V1 → V2 State Management Migration Skill

Migrate OpenHarmony ArkUI `@Component` (V1) components to `@ComponentV2` (V2).

## When to Use

Activate this skill when the user expresses any of the following intents:
- 迁移 V1 组件到 V2 / V1V2 迁移 / 状态管理迁移 (migrate V1 components to V2 / state management migration)
- Change `@Component` to `@ComponentV2`
- Migrate decorators such as `@State`/`@Prop`/`@Link` to their V2 equivalents
- Analyze whether a component can be migrated to V2 / assess migration risk

---

## Overall Workflow

```
0. Confirm target → 1. Analyze → 2. Plan → 3. Execute → 4. Verify
```

Each phase is detailed below. Always proceed in this order; never skip analysis and jump straight to execution.

---

## Step 0: Confirm the Migration Target

Before any analysis, confirm the migration target in the following order.

### Case 1: The user only says "V1V2 migration" without a project path

**You must first ask the user for the project path**, e.g.:
> Please provide the HarmonyOS/OpenHarmony project path to migrate.

After receiving the path, proceed to Case 2. Do not assume or guess the project path.

### Case 2: The user provides a project path but no specific component

Run the scan script:
```bash
python3 {{SKILL_DIR}}/scripts/component_analyzer.py <project-path> --scan-v1
```

The script outputs the list of all V1 components in the project, plus an `instruction` field.
**You must present the V1 component list to the user and ask which component to migrate.** Do not skip this step.

If the list is empty, inform the user that the project contains no V1 components and no migration is needed.

### Case 3: The user provides both a project path and a component name

Proceed directly to Step 1 (Analysis).

---

## Step 1: Analyze

### 1.1 Detect the API version

```bash
python3 {{SKILL_DIR}}/scripts/api_version_checker.py <project-dir> --json
```

Key output fields:
- `mixingRules`: `"strict"` (API < 19) or `"relaxed"` (API >= 19)
- `compatibleApiVersion`: the minimum compatible API version
- `availableApis`: list of available compatibility APIs

**Decision points**:
- `strict` → complex types cannot cross the V1/V2 boundary during migration; a bridge pattern may be required
- `relaxed` → `UIUtils.enableV2Compatibility()` and `UIUtils.makeV1Observed()` can relax the constraints

### 1.2 Analyze the target component

```bash
python3 {{SKILL_DIR}}/scripts/component_analyzer.py <target-file-or-dir> --json
```

Output includes:
- Component version (V1/V2), decorator list, state variable types
- Child component references, rendering mode (ForEach/LazyForEach/Repeat)
- App-level state usage (LocalStorage/AppStorage/PersistentStorage/Environment/animateTo)

### 1.3 Trace the dependency chain

```bash
python3 {{SKILL_DIR}}/scripts/dependency_tracer.py <component-name> <project-dir> --json
```

Output:
- `mustMigrate`: list of components that must be migrated together due to data interaction
- State passing types between components (state_variable_ref / two_way_binding / callback / literal)
- Dependency graph (parent → child data flow)

**Decision points**:
- If `mustMigrate` contains only one component → it can be migrated independently
- If there are multiple components → evaluate whether to migrate them all or use a bridge pattern

### 1.4 Mixing validation (run once before and once after migration)

```bash
python3 {{SKILL_DIR}}/scripts/mixing_validator.py <project-dir> --json [--target <component-name>]
```

Output:
- `violations`: mixing issues that will cause compile/runtime errors
- `warnings`: mixing scenarios that may be risky
- `suggestions`: available compatibility API suggestions
- `summary.isCompliant`: whether all checks pass

---

## Step 2: Plan

Based on the analysis, report the migration scope and strategy to the user:

### Independent migration (preferred)
The target component has no external data interaction (`hasInput: false, hasOutput: false`), or all interactions use simple types.

### Joint migration
The target component exchanges complex types with its parent/child components. All components in `mustMigrate` must be migrated together.

### Bridge pattern (use when API < 19)
When V1 must pass an `@Observed`-decorated class to a V2 component:
```
V1Comp → V1BridgeComponent(@Component) → V2Comp(@ComponentV2)
```
The bridge is a **pure V1 component**: it destructures the `@Observed` class into simple-type fields and passes them to the V2 child's `@Param` (complex types cannot cross the V1→V2 boundary when API < 19). It must NOT hold an `@ObservedV2` object via a V1 decorator. For multi-component sharing, use a standalone `@ObservedV2`/`@Trace` singleton written by V1 and read by V2. See the bridge section in `references/mixing-rules.md`.

Confirm the strategy with the user before proceeding to execution.

---

## Step 3: Execute the Migration

Rewrite the code item by item in the following order. Each item maps to a reference document.

### 3.1 Component decorator

```
@Component  →  @ComponentV2
```

If the component has `@Entry`, leave it unchanged (`@Entry` works in both V1 and V2).
If the component has `@Reusable`, change it to `@ReusableV2`.

### 3.2 State variable decorator mapping

For the full mapping table, see `references/decorator-mapping.md`. Quick reference:

| V1 | V2 | Key points |
|----|-----|--------|
| `@State` simple type | `@Local` | Direct replacement |
| `@State` complex type | `@Local` + `@ObservedV2`/`@Trace` on the class | V2 `@Local` observes only itself, not its properties |
| `@State` needing external init | `@Param` `@Once` | `@Local` forbids external initialization |
| `@Prop` | `@Param` | `@Param` is passed by reference (not a deep copy); `@Param` is read-only |
| `@Link` | `@Param` + `@Event` | Replace two-way binding with a callback pattern |
| `@Provide`/`@Consume` | `@Provider`/`@Consumer` | V2 requires the `()` syntax; the alias is the unique match key |
| `@Watch` | `@Monitor` | V2 is asynchronous; supports multiple variables; provides before/after |
| `@Observed`/`@ObjectLink` | `@ObservedV2`/`@Trace` | Deep observation; no longer needs child-component decomposition |
| `$$` binding | `!!` binding | Direct replacement |

### 3.3 Data object migration

Change `@Observed` classes to `@ObservedV2` and add `@Trace` to the properties.

```typescript
// V1
@Observed
class Model {
  @Track public name: string = '';
  @Track public count: number = 0;
}

// V2
@ObservedV2
class Model {
  @Trace public name: string = '';
  @Trace public count: number = 0;
}
```

**Note**: `@Observed` and `@ObservedV2` cannot coexist on the same class. If the class is referenced by other V1 components, resolve those dependencies first.

For detailed rules, see `references/class-migration.md`.

### 3.4 Rendering control migration

| V1 | V2 |
|----|-----|
| `ForEach` | `Repeat(...).each(...).key(...)` |
| `LazyForEach` + `IDataSource` | `Repeat(...).each(...).key(...).virtualScroll()` + `@Local` array |

In V2 the data source is a plain `@Local` array; modifying the array triggers updates — no need to call `notifyDataAdd` and friends manually.

Use `.templateId()` + `.template()` for template rendering instead of manual `if` checks.

For detailed rules and code examples, see `references/rendering-migration.md`.

### 3.5 App-level state migration

| V1 | V2 |
|----|-----|
| `LocalStorage` | `@ObservedV2`/`@Trace` singleton |
| `AppStorage` | `AppStorageV2.connect()` |
| `@StorageProp`/`@StorageLink` | `AppStorageV2.connect()` + `@Local` + `@Monitor` |
| `PersistentStorage` | `PersistenceV2.globalConnect()` |
| `Environment` | Read directly from `UIAbilityContext.config` |

**Important: keep V1 API calls; only add V2 API calls.** During incremental migration, a single `.ts` file may contain V1 API calls for multiple keys. When migrating a component, add the corresponding V2 API (e.g. `AppStorageV2.connect()`) only for the keys that component uses, and **do not remove the original V1 API calls** (e.g. `AppStorage.setOrCreate()`), because other not-yet-migrated V1 components may still be using other keys in the same file. Only when `stateApiByKey` shows that all `decoratorUsage` for a key have been migrated to V2 may the V1 API calls for that key be removed.

For detailed rules, see `references/app-state-migration.md`.

### 3.6 Built-in objects and animateTo

- Wrap framework built-in objects (`ChildrenMainSize`/`WaterFlowSections`/`attributeModifier`) with `UIUtils.makeObserved()`.
- `animateTo` is incompatible with V2's asynchronous update mechanism; force a synchronous flush first with `animateToImmediately` (API < 22) or `UIUtils.applySync()` (API >= 22).

For detailed rules, see `references/advanced-topics.md`.

### 3.7 New V2 capabilities

After migration, consider adopting new V2 capabilities:
- `@Computed`: derived state with automatic result caching
- `Repeat` template rendering + `virtualScroll`: replaces ForEach/LazyForEach

---

## Step 4: Verify

### 4.1 Mixing validation

```bash
python3 {{SKILL_DIR}}/scripts/mixing_validator.py <project-dir> --json --target <component-name>
```

Ensure `summary.isCompliant` is `true` and all `violations` are empty.

### 4.2 Item-by-item checklist

- [ ] Component decorator: `@Component` → `@ComponentV2`
- [ ] All V1 state decorators replaced with their V2 equivalents
- [ ] Classes with complex types now have `@ObservedV2` + `@Trace`
- [ ] `@Link` two-way binding changed to `@Param` + `@Event` callback pattern
- [ ] `$$` replaced with `!!`
- [ ] `ForEach`/`LazyForEach` replaced with `Repeat`
- [ ] App-level state (if any) has V2 APIs added, and V1 API calls still used by other components were not removed
- [ ] `animateTo` (if any) has a synchronous-flush prefix added
- [ ] No V1/V2 decorators mixed within the same component
- [ ] No `@Observed` and `@ObservedV2` coexisting on the same class
- [ ] Data passing across V1/V2 component boundaries follows the mixing rules

---

## Reference document index

| File | Contents | When to consult |
|------|------|----------|
| `references/decorator-mapping.md` | Full decorator mapping table, migration rules for @State/@Prop/@Link/@Provide/@Watch | When rewriting state variables |
| `references/class-migration.md` | @Observed/@ObjectLink/@Track → @ObservedV2/@Trace, nested object observation, precise updates | When migrating data object classes |
| `references/mixing-rules.md` | V1/V2 mixing rules, API < 19 vs >= 19 differences, bridge pattern, enableV2Compatibility | When components coexist during migration |
| `references/rendering-migration.md` | ForEach/LazyForEach → Repeat, virtualScroll, template rendering, @Reusable → @ReusableV2 | When rewriting rendering logic |
| `references/app-state-migration.md` | LocalStorage/AppStorage/PersistentStorage/Environment → V2 alternatives | When migrating app-level state |
| `references/advanced-topics.md` | Built-in objects (makeObserved), animateTo migration, V1/V2 update mechanism differences | When handling special cases |
| `references/architecture.md` | Overall skill architecture, five-phase workflow, script responsibilities and import relationships | Maintainer reference: understanding script collaboration and data flow |
| `references/migration-overview.md` | Design overview, detailed JSON output fields of each script, Storage key tracing mechanism, end-to-end example walkthrough | Maintainer reference: interpreting script output and migration decisions |

## Example index

| Directory | Scenario | Migration points covered |
|------|------|-----------|
| `examples/simple-component/` | Simple component | @State→@Local, @Prop→@Param |
| `examples/component-with-props/` | Complex parent-child interaction | @Link→@Param+@Event, @Provide→@Provider, @Watch→@Monitor, $$→!! |
| `examples/observed-class/` | Data object | @Observed→@ObservedV2, @ObjectLink→@Trace, nested observation |
| `examples/localstorage/` | App-level state | LocalStorage→singleton, AppStorage→AppStorageV2, PersistentStorage→PersistenceV2 |
| `examples/partial-migration/` | Partial migration and coexistence | V1/V2 coexistence, bridge pattern, API version checks |

Each example directory contains `before.ets` (V1 code) and `after.ets` (V2 code) for side-by-side reference.

---

## Notes / Caveats

1. **Never mix V1/V2 decorators within the same component** — compile error.
2. **Never decorate the same class with both @Observed and @ObservedV2** — compile error.
3. **@Local forbids external initialization** — when a value must come from outside, use `@Param @Once`.
4. **@Param is read-only** — when the child needs to modify it, keep a local copy and sync via `@Monitor`.
5. **@Monitor is asynchronous** — different from the synchronous behavior of V1's @Watch.
6. **V2 deep observation** — `@ObservedV2/@Trace` can directly observe nested properties; you no longer need to decompose child components layer by layer.
7. **animateTo compatibility** — V2's async mechanism is incompatible with animateTo; a synchronous-flush prefix is mandatory.
8. **Migration is incremental** — partial migration is allowed, but the mixing rules must be followed (see `references/mixing-rules.md`).
