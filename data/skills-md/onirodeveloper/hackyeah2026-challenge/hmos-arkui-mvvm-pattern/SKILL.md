---
name: "hmos-arkui-mvvm-pattern"
description: "HarmonyOS ArkUI MVVM architecture skill. Use for Model/ViewModel/View layering, directory planning, component responsibilities, data flow, and MVVM refactoring. Trigger for V1 or V2 state-management MVVM development, ViewModel extraction, state-ownership fixes, and testability improvements."
metadata:
  version: 1.0.0
  keywords:
    - ArkUI
    - MVVM
    - V1 state-management MVVM architecture
    - V2 state-management MVVM architecture
    - architecture layers
    - Model layer
    - ViewModel layer
    - View layer
---

# ArkUI MVVM Architecture Pattern

## Definition

| Field | Content |
| --- | --- |
| `skill_id` | `arkui-mvvm-pattern` |
| `skill_name` | `ArkUI MVVM Architecture Pattern` |
| `one_line_purpose` | `Develop or refactor MVVM implementations for V1 and V2 state-management versions` |
| `device_scope` | `phone / tablet / 2in1` |
| `problem_scope` | `MVVM three-layer separation: View, Model, ViewModel` |
| `not_in_scope` | `V1/V2 decorator usage and non-MVVM architecture patterns` |
| `primary_outputs` | `primary_scene`, `implementation_notes`, `code_touchpoints`, `verification_matrix` |

## Core Constraints

1. **Keep the current project version**: unless migration to V2 is explicit, keep the current state-management version and do not mix V1 and V2.
2. **Unidirectional data flow (UDF)**: data flows downward Model → ViewModel → View; events flow upward View → ViewModel → Model.
3. **Single source of truth (SSOT)**: data changes occur in the data layer; ViewModel is the sole source of UI state.
4. **View must not access Model directly**: access it through ViewModel.
5. **Minimize AppStorage**: use AppStorage/AppStorageV2 only when necessary; ViewModel should hold state directly.
6. **V1 `@Observed` + `@Track` cannot coexist with getters**: a V1 `@Observed` class with `@Track` properties must not define a `get` accessor, or runtime failure may occur.
7. **Access data through ViewModel types**: View/Page must not import Model types. Define an `@Observed` ViewModel class for each list item and convert Model → ViewModel there.

### Keep the Current Version

Determine whether the project uses V1 or V2 before acting. Search an `.ets` file for `@Component` or `@ComponentV2`; if both occur, choose one version and standardize it.

### State Variable Principles

Apply these principles to both new development and refactoring. This is commonly called **State Hoisting**: keep state close to its use and lift it only as needed.

1. If a value can be computed from existing properties, do not store it; use `@Computed` (V2) or a getter (V1).
2. If only one component needs independent data, keep it private with `@Local` (V2) or `@State` (V1).
3. If several components need UI-only state, lift it to their nearest common ancestor and pass it with `@Param` (V2) or `@Prop` (V1).
4. If it involves business logic or data access, make it a ViewModel property using `@Trace` (V2) or `@Track` (V1).

| Principle | Description | Avoid |
| --- | --- | --- |
| Do not store derived state | Compute values with `@Computed` or a getter | Store `allowClick` and synchronize it manually |
| Keep state local | Put state in the smallest required scope | Put one-component `isShowSheet` in ViewModel |
| Single source | Manage each value in one place | Store `inputContent` in both Page and ViewModel |
| Lift to common ancestor | Share state at the nearest common ancestor | Put sibling-only `selectedIndex` directly in ViewModel |

### Code File Principles

1. Business data entities belong in Model (entity classes and Repository).
2. UI state that drives rendering belongs in ViewModel (`@Observed`/`@ObservedV2`).
3. Pure logic and system-capability wrappers belong in `utils/`.

## Recommended Directory

```text
ets/
├── model/           # Data models + Repository
├── viewmodel/       # View models
├── views/           # Business components
├── pages/           # Page entry points
├── utils/           # Pure logic and system-capability wrappers
└── common/          # Shared constants and components
```

## Workflow

Follow the workflow strictly. For new pages or modules, use [references/add-func-workflow.md](references/add-func-workflow.md). For existing code, use [references/refactor-func-workflow.md](references/refactor-func-workflow.md).

| Tag | Phase | Focus |
| --- | --- | --- |
| `REQ` | Requirements and design | Architecture, layering, state ownership, V1/V2 selection |
| `DEV` | Development | Model/ViewModel/View/Page implementation, decorators, data flow |
| `VAL` | Validation | Data-flow compliance, Model isolation, decorator pairing, refresh behavior |

## Scene Index

### `MVVM-01` V1 MVVM Development

```yaml
scene_id: MVVM-01
name: V1 state-management MVVM development
phases: [REQ, DEV, VAL]
signals: [V1 state management, MVVM, architecture layers, Model/ViewModel/View]
not_when: V2 state management (MVVM-02) / non-MVVM architecture
ref: RSC_MVVM_01, RSC_MVVM_02
```

### `MVVM-02` V2 MVVM Development

```yaml
scene_id: MVVM-02
name: V2 state-management MVVM development
phases: [REQ, DEV, VAL]
signals: [V2 state management, MVVM, architecture layers, Model/ViewModel/View]
not_when: V1 state management (MVVM-01) / non-MVVM architecture
ref: RSC_MVVM_03, RSC_MVVM_04
```

## Reference Resources

| File | Content | Load when |
| --- | --- | --- |
| [references/anti-patterns.md](references/anti-patterns.md) | Architecture anti-patterns and scan checklist | Scanning an existing project |
| [references/v1-nested-observation.md](references/v1-nested-observation.md) | V1 nested object and array observation | Handling nested V1 observation |
| [references/v1-v2-mapping.md](references/v1-v2-mapping.md) | V1/V2 array behavior and decorator pairing | Handling array updates or mixed versions |
| [references/v2-advanced.md](references/v2-advanced.md) | AppStorageV2/PersistenceV2 signatures and selection | Using V2 global state |
| [references/multi-module.md](references/multi-module.md) | Three-layer architecture, modules, and devices | Multi-module or multi-device projects |

## Build Verification

Before building, run `devecocli --version`. Use `devecocli build` for modified `.ets` files, repair errors, and run a full build when needed. If the CLI is unavailable, confirm with the user before installing it.
